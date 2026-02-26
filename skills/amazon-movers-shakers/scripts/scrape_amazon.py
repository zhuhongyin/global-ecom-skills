#!/usr/bin/env python3
"""
Amazon Movers & Shakers Data Scraper
Fetch trending products from Amazon's Movers & Shakers list

Usage:
    python scrape_amazon.py --category home-garden --limit 20
    python scrape_amazon.py --search "standing desk" --limit 10
"""

import argparse
import json
import re
import sys
import time
import random
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Optional
from urllib.parse import quote_plus, urljoin

try:
    import requests
    from bs4 import BeautifulSoup
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    print("Warning: requests/beautifulsoup4 not installed, will use mock data")


AMAZON_SITES = {
    "us": "https://www.amazon.com",
    "uk": "https://www.amazon.co.uk",
    "de": "https://www.amazon.de",
    "jp": "https://www.amazon.co.jp",
}

CATEGORY_URLS = {
    "home-garden": "/Best-Sellers-Home-Kitchen/zgbs/home-garden",
    "electronics": "/Best-Sellers-Electronics/zgbs/electronics",
    "sports": "/Best-Sellers-Sports-Outdoors/zgbs/sporting-goods",
    "office": "/Best-Sellers-Office-Products/zgbs/office-products",
    "toys": "/Best-Sellers-Toys-Games/zgbs/toys-and-games",
    "health": "/Best-Sellers-Health-Personal-Care/zgbs/hpc",
    "beauty": "/Best-Sellers-Beauty-Personal-Care/zgbs/beauty",
    "pet-supplies": "/Best-Sellers-Pet-Supplies/zgbs/pet-supplies",
    "automotive": "/Best-Sellers-Automotive/zgbs/automotive",
    "garden": "/Best-Sellers-Patio-Lawn-Garden/zgbs/hi",
}

EXCLUDED_BRANDS = [
    "Amazon Basics",
    "AmazonBasics",
    "Apple",
    "Samsung",
    "Sony",
    "LG",
]

HIGH_COMPLIANCE_CATEGORIES = [
    "medical",
    "baby food",
    "infant",
    "pharmaceutical",
    "supplement",
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
]


@dataclass
class AmazonProduct:
    asins: str
    title: str
    url: str
    image_url: str
    price: Optional[float]
    price_display: str
    currency: str
    rating: Optional[float]
    review_count: Optional[int]
    rank: int
    rank_change: str
    prime: bool
    category_path: str
    suitable_for_temu: bool
    exclusion_reason: Optional[str]


class AmazonMoversShakersScraper:
    
    def __init__(self, site: str = "us"):
        self.site = site
        self.base_url = AMAZON_SITES.get(site, AMAZON_SITES["us"])
        self.session = None
        if HAS_REQUESTS:
            self.session = requests.Session()
            self.session.headers.update({
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
            })
    
    def _get_headers(self) -> dict:
        return {
            "User-Agent": random.choice(USER_AGENTS),
            "Referer": self.base_url,
        }
    
    def _fetch_page(self, url: str, retries: int = 3) -> Optional[str]:
        if not HAS_REQUESTS or not self.session:
            return None
        
        for attempt in range(retries):
            try:
                time.sleep(random.uniform(1, 3))
                response = self.session.get(
                    url,
                    headers=self._get_headers(),
                    timeout=30,
                    allow_redirects=True
                )
                
                if response.status_code == 200:
                    return response.text
                elif response.status_code == 503:
                    print(f"Amazon returned 503, retrying... ({attempt + 1}/{retries})")
                    time.sleep(random.uniform(3, 6))
                elif response.status_code == 404:
                    print(f"Page not found: {url}")
                    return None
                else:
                    print(f"HTTP {response.status_code} for {url}")
                    
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}, retrying... ({attempt + 1}/{retries})")
                time.sleep(random.uniform(2, 5))
        
        return None
    
    def get_movers_shakers_url(self, category: str = None) -> str:
        if category and category in CATEGORY_URLS:
            return urljoin(self.base_url, CATEGORY_URLS[category])
        return urljoin(self.base_url, "/Best-Sellers/zgbs")
    
    def get_search_url(self, keyword: str) -> str:
        encoded_keyword = quote_plus(keyword)
        return f"{self.base_url}/s?k={encoded_keyword}&s=exact-aware-popularity-rank"
    
    def parse_price(self, price_text: str) -> tuple:
        if not price_text:
            return None, "", "USD"
        
        price_text = price_text.strip()
        
        patterns = [
            (r'\$([\d,]+\.?\d*)', 'USD'),
            (r'£([\d,]+\.?\d*)', 'GBP'),
            (r'€([\d,]+\.?\d*)', 'EUR'),
            (r'¥([\d,]+\.?\d*)', 'JPY'),
        ]
        
        for pattern, currency in patterns:
            match = re.search(pattern, price_text)
            if match:
                price_str = match.group(1).replace(',', '')
                try:
                    return float(price_str), price_text, currency
                except ValueError:
                    pass
        
        return None, price_text, "USD"
    
    def parse_rating(self, rating_text: str) -> Optional[float]:
        if not rating_text:
            return None
        
        match = re.search(r'([\d.]+)\s*(?:out of|von|sur)\s*5', rating_text)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                pass
        return None
    
    def parse_review_count(self, count_text: str) -> Optional[int]:
        if not count_text:
            return None
        
        count_text = count_text.replace(',', '').replace('.', '')
        match = re.search(r'(\d+)', count_text)
        if match:
            try:
                return int(match.group(1))
            except ValueError:
                pass
        return None
    
    def parse_rank_change(self, change_text: str) -> str:
        if not change_text:
            return "+0"
        
        if 'up' in change_text.lower() or 'risen' in change_text.lower():
            match = re.search(r'(\d+)', change_text)
            if match:
                return f"+{match.group(1)}"
        elif 'down' in change_text.lower():
            match = re.search(r'(\d+)', change_text)
            if match:
                return f"-{match.group(1)}"
        
        return "+0"
    
    def is_suitable_for_temu(self, product: dict) -> tuple:
        title = product.get('title', '').lower()
        category = product.get('category_path', '').lower()
        brand = product.get('brand', '').lower()
        price = product.get('price')
        
        for excluded_brand in EXCLUDED_BRANDS:
            if excluded_brand.lower() in brand:
                return False, f"品牌垄断: {excluded_brand}"
        
        for excluded_cat in HIGH_COMPLIANCE_CATEGORIES:
            if excluded_cat in category or excluded_cat in title:
                return False, f"高资质门槛: {excluded_cat}"
        
        if price and price < 5:
            return False, "价格过低，利润空间不足"
        
        return True, None
    
    def _parse_product_card(self, card, rank: int) -> Optional[AmazonProduct]:
        try:
            asins = None
            link = card.find('a', href=True)
            if link:
                href = link['href']
                match = re.search(r'/dp/([A-Z0-9]{10})', href)
                if match:
                    asins = match.group(1)
            
            if not asins:
                asins_elem = card.get('data-asin') or card.get('id', '')
                if asins_elem and len(asins_elem) == 10:
                    asins = asins_elem
                else:
                    return None
            
            title = ""
            title_elem = (
                card.find('span', class_='a-size-base-plus') or
                card.find('span', class_='a-size-medium') or
                card.find('h2') or
                card.find('a', class_='a-link-normal')
            )
            if title_elem:
                title = title_elem.get_text(strip=True)
            
            if not title:
                title = f"Amazon Product {asins}"
            
            url = f"{self.base_url}/dp/{asins}"
            
            image_url = ""
            img = card.find('img')
            if img:
                image_url = img.get('src', '') or img.get('data-src', '')
            
            price = None
            price_display = ""
            currency = "USD"
            
            price_elem = (
                card.find('span', class_='a-price') or
                card.find('span', class_='p13n-sc-price') or
                card.find('span', class_='a-color-price')
            )
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                price, price_display, currency = self.parse_price(price_text)
            
            rating = None
            rating_elem = card.find('span', class_='a-icon-alt')
            if rating_elem:
                rating = self.parse_rating(rating_elem.get_text(strip=True))
            
            review_count = None
            review_elem = (
                card.find('span', class_='a-size-base') or
                card.find('a', class_='a-size-small')
            )
            if review_elem:
                review_text = review_elem.get_text(strip=True)
                if re.search(r'\d', review_text):
                    review_count = self.parse_review_count(review_text)
            
            rank_change = "+0"
            change_elem = card.find('span', class_='zg-bdg-up') or card.find('span', class_='zg-bdg-down')
            if change_elem:
                rank_change = self.parse_rank_change(change_elem.get_text(strip=True))
            
            prime = bool(card.find('i', class_='a-icon-prime'))
            
            category_path = ""
            cat_elem = card.find('span', class_='a-size-small')
            if cat_elem:
                category_path = cat_elem.get_text(strip=True)
            
            suitable, reason = self.is_suitable_for_temu({
                'title': title,
                'category_path': category_path,
                'brand': '',
                'price': price
            })
            
            return AmazonProduct(
                asins=asins,
                title=title,
                url=url,
                image_url=image_url,
                price=price,
                price_display=price_display,
                currency=currency,
                rating=rating,
                review_count=review_count,
                rank=rank,
                rank_change=rank_change,
                prime=prime,
                category_path=category_path,
                suitable_for_temu=suitable,
                exclusion_reason=reason
            )
            
        except Exception as e:
            print(f"Error parsing product card: {e}")
            return None
    
    def scrape_real_data(self, category: str = None, limit: int = 20) -> List[AmazonProduct]:
        if not HAS_REQUESTS:
            print("requests/beautifulsoup4 not available, falling back to mock data")
            return []
        
        url = self.get_movers_shakers_url(category)
        print(f"Fetching: {url}")
        
        html = self._fetch_page(url)
        if not html:
            print("Failed to fetch page, falling back to mock data")
            return []
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            products = []
            
            selectors = [
                ('div', {'id': 'gridItemRoot'}),
                ('div', {'class': 'zg-grid-general-faceout'}),
                ('div', {'class': 'p13n-sc-uncoverable-faceout'}),
                ('li', {'class': 'zg-item-immersion'}),
                ('div', {'data-component-type': 's-search-result'}),
            ]
            
            cards = []
            for tag, attrs in selectors:
                cards = soup.find_all(tag, attrs)
                if cards:
                    break
            
            if not cards:
                cards = soup.find_all('div', class_=re.compile(r'(product|item|card)', re.I))
            
            print(f"Found {len(cards)} product cards")
            
            for rank, card in enumerate(cards[:limit * 2], 1):
                product = self._parse_product_card(card, rank)
                if product:
                    products.append(product)
                    if len(products) >= limit:
                        break
            
            return products
            
        except Exception as e:
            print(f"Error parsing HTML: {e}")
            return []
    
    def scrape_search_results(self, keyword: str, limit: int = 20) -> List[AmazonProduct]:
        if not HAS_REQUESTS:
            return []
        
        url = self.get_search_url(keyword)
        print(f"Searching: {url}")
        
        html = self._fetch_page(url)
        if not html:
            return []
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            products = []
            
            cards = soup.find_all('div', {'data-component-type': 's-search-result'})
            
            for rank, card in enumerate(cards[:limit], 1):
                product = self._parse_product_card(card, rank)
                if product:
                    products.append(product)
            
            return products
            
        except Exception as e:
            print(f"Error parsing search results: {e}")
            return []
    
    def generate_mock_data(self, category: str = "home-garden", limit: int = 20) -> List[AmazonProduct]:
        mock_products = [
            {
                "title": "Standing Desk Converter, Height Adjustable Desk Riser",
                "price": 89.99,
                "rating": 4.5,
                "review_count": 1256,
                "rank_change": "+256",
            },
            {
                "title": "Monitor Stand Riser with Storage, Desktop Organizer",
                "price": 34.99,
                "rating": 4.3,
                "review_count": 892,
                "rank_change": "+189",
            },
            {
                "title": "Desk Mat Large, PU Leather Desk Protector Pad",
                "price": 19.99,
                "rating": 4.6,
                "review_count": 2341,
                "rank_change": "+145",
            },
            {
                "title": "Cable Management Box, Desktop Cord Organizer",
                "price": 24.99,
                "rating": 4.4,
                "review_count": 567,
                "rank_change": "+98",
            },
            {
                "title": "Keyboard Tray Under Desk, Ergonomic Keyboard Stand",
                "price": 45.99,
                "rating": 4.2,
                "review_count": 423,
                "rank_change": "+87",
            },
            {
                "title": "Desk Shelf Organizer, Wooden Desktop Bookshelf",
                "price": 39.99,
                "rating": 4.7,
                "review_count": 1567,
                "rank_change": "+76",
            },
            {
                "title": "Laptop Stand Adjustable, Aluminum Notebook Riser",
                "price": 29.99,
                "rating": 4.5,
                "review_count": 3456,
                "rank_change": "+65",
            },
            {
                "title": "Desk Drawer Organizer, Under Desk Storage Cabinet",
                "price": 54.99,
                "rating": 4.1,
                "review_count": 234,
                "rank_change": "+54",
            },
            {
                "title": "Foot Rest Under Desk, Ergonomic Office Footrest",
                "price": 22.99,
                "rating": 4.4,
                "review_count": 876,
                "rank_change": "+43",
            },
            {
                "title": "Desk Lamp with USB Charging Port, LED Office Light",
                "price": 32.99,
                "rating": 4.6,
                "review_count": 2134,
                "rank_change": "+32",
            },
        ]
        
        products = []
        for i, mock in enumerate(mock_products[:limit]):
            asins = f"B0MOCK{i:04d}XYZ"
            product = AmazonProduct(
                asins=asins,
                title=mock["title"],
                url=f"{self.base_url}/dp/{asins}",
                image_url=f"https://m.media-amazon.com/images/I/mock{i}.jpg",
                price=mock["price"],
                price_display=f"${mock['price']}",
                currency="USD",
                rating=mock["rating"],
                review_count=mock["review_count"],
                rank=i + 1,
                rank_change=mock["rank_change"],
                prime=True,
                category_path="Home & Kitchen > Home Office Furniture",
                suitable_for_temu=True,
                exclusion_reason=None
            )
            
            suitable, reason = self.is_suitable_for_temu({
                'title': product.title,
                'category_path': product.category_path,
                'brand': '',
                'price': product.price
            })
            product.suitable_for_temu = suitable
            product.exclusion_reason = reason
            
            products.append(product)
        
        return products


def format_output(products: List[AmazonProduct], output_format: str = "json") -> str:
    if output_format == "json":
        data = {
            "metadata": {
                "site": "amazon.com",
                "category": "Home & Kitchen",
                "scrape_time": datetime.now().isoformat(),
                "total_products": len(products),
                "returned_products": len(products),
                "data_source": "real" if any(p.asins and not p.asins.startswith("B0MOCK") for p in products) else "mock"
            },
            "products": [asdict(p) for p in products]
        }
        return json.dumps(data, ensure_ascii=False, indent=2)
    else:
        lines = []
        lines.append("=" * 60)
        lines.append("亚马逊飙升榜产品列表")
        lines.append("=" * 60)
        for p in products:
            status = "✅" if p.suitable_for_temu else "❌"
            lines.append(f"\n{p.rank}. {status} {p.title[:50]}...")
            lines.append(f"   ASIN: {p.asins}")
            lines.append(f"   价格: {p.price_display}")
            lines.append(f"   评分: {p.rating} ({p.review_count} 评论)")
            lines.append(f"   排名变化: {p.rank_change}")
            if p.exclusion_reason:
                lines.append(f"   排除原因: {p.exclusion_reason}")
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Amazon Movers & Shakers Data Scraper"
    )
    parser.add_argument(
        "--category", type=str, default="home-garden",
        choices=list(CATEGORY_URLS.keys()),
        help="Product category to scrape"
    )
    parser.add_argument(
        "--search", type=str,
        help="Search keyword instead of category"
    )
    parser.add_argument(
        "--site", type=str, default="us",
        choices=list(AMAZON_SITES.keys()),
        help="Amazon site region"
    )
    parser.add_argument(
        "--limit", type=int, default=20,
        help="Maximum number of products to return"
    )
    parser.add_argument(
        "--output", type=str,
        help="Output file path"
    )
    parser.add_argument(
        "--format", type=str, default="json",
        choices=["json", "text"],
        help="Output format"
    )
    parser.add_argument(
        "--mock", action="store_true",
        help="Force use mock data"
    )
    
    args = parser.parse_args()
    
    scraper = AmazonMoversShakersScraper(site=args.site)
    
    products = []
    
    if not args.mock:
        if args.search:
            products = scraper.scrape_search_results(args.search, args.limit)
        else:
            products = scraper.scrape_real_data(args.category, args.limit)
    
    if not products:
        print("Using mock data as fallback...")
        products = scraper.generate_mock_data(category=args.category, limit=args.limit)
    
    output = format_output(products, args.format)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"Results saved to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
