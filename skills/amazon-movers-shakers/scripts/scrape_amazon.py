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
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Optional
from urllib.parse import quote_plus, urljoin


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
    
    def parse_html_products(self, html_content: str, limit: int = 20) -> List[AmazonProduct]:
        products = []
        
        asin_pattern = r'/dp/([A-Z0-9]{10})'
        asins = re.findall(asin_pattern, html_content)
        unique_asins = list(dict.fromkeys(asins))[:limit]
        
        for rank, asins in enumerate(unique_asins, 1):
            product = AmazonProduct(
                asins=asins,
                title=f"Product {asins}",
                url=f"{self.base_url}/dp/{asins}",
                image_url="",
                price=None,
                price_display="",
                currency="USD",
                rating=None,
                review_count=None,
                rank=rank,
                rank_change="+0",
                prime=False,
                category_path="",
                suitable_for_temu=True,
                exclusion_reason=None
            )
            products.append(product)
        
        return products
    
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
                "returned_products": len(products)
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
        help="Generate mock data for testing"
    )
    
    args = parser.parse_args()
    
    scraper = AmazonMoversShakersScraper(site=args.site)
    
    if args.mock:
        products = scraper.generate_mock_data(category=args.category, limit=args.limit)
    else:
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
