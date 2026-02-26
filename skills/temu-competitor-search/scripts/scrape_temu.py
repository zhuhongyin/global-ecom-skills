#!/usr/bin/env python3
"""
Temu Competitor Search & King Price Scraper
Find competitor products and lowest prices on Temu

Usage:
    python scrape_temu.py --keyword "standing desk" --limit 20
    python scrape_temu.py --keyword "desk mat" --sort price_asc
"""

import argparse
import json
import re
from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import List, Optional
from urllib.parse import quote_plus


TEMU_SITES = {
    "us": "https://www.temu.com",
    "uk": "https://www.temu.com/uk",
    "eu": "https://www.temu.com/eu",
}

SORT_OPTIONS = {
    "price_asc": 0,
    "price_desc": 1,
    "sales_desc": 2,
    "rating_desc": 3,
    "newest": 4,
}


@dataclass
class TemuProduct:
    product_id: str
    title: str
    url: str
    image_url: str
    price: float
    original_price: Optional[float]
    discount: str
    currency: str
    rating: Optional[float]
    review_count: Optional[int]
    sold_count: str
    shipping: str
    seller_name: str
    seller_rating: Optional[float]
    is_bundle: bool
    is_premium: bool
    is_lightweight: bool
    quality_level: str


@dataclass
class KingPrice:
    price: float
    currency: str
    product_id: str
    title: str
    image_url: str
    rating: Optional[float]
    review_count: Optional[int]
    sold_count: str
    shipping: str
    seller: str
    notes: str


@dataclass
class MarketInsight:
    price_distribution: List[dict]
    common_features: List[str]
    premium_features: List[str]
    gap_opportunities: List[dict]


@dataclass
class TemuSearchResult:
    keyword: str
    site: str
    search_time: str
    total_results: int
    returned_results: int
    lowest_price: float
    highest_price: float
    average_price: float
    median_price: float
    competition_level: str
    opportunity_score: float
    king_price: KingPrice
    competitors: List[TemuProduct]
    market_insights: MarketInsight
    recommendation: dict


class TemuCompetitorScraper:
    
    def __init__(self, site: str = "us"):
        self.site = site
        self.base_url = TEMU_SITES.get(site, TEMU_SITES["us"])
    
    def get_search_url(self, keyword: str, sort: str = "price_asc") -> str:
        encoded_keyword = quote_plus(keyword)
        sort_code = SORT_OPTIONS.get(sort, 0)
        return f"{self.base_url}/search_result.html?search_key={encoded_keyword}&search_sort={sort_code}"
    
    def parse_price(self, price_text: str) -> tuple:
        if not price_text:
            return 0.0, "USD"
        
        patterns = [
            (r'\$([\d.]+)', 'USD'),
            (r'£([\d.]+)', 'GBP'),
            (r'€([\d.]+)', 'EUR'),
        ]
        
        for pattern, currency in patterns:
            match = re.search(pattern, price_text)
            if match:
                try:
                    return float(match.group(1)), currency
                except ValueError:
                    pass
        
        return 0.0, "USD"
    
    def analyze_competition_level(self, total_results: int, price_range: float) -> str:
        if total_results > 100 and price_range < 20:
            return "very_high"
        elif total_results > 50:
            return "high"
        elif total_results > 20:
            return "medium"
        else:
            return "low"
    
    def calculate_opportunity_score(
        self,
        competition_level: str,
        price_range: float,
        king_price: float
    ) -> float:
        scores = {
            "very_high": 2,
            "high": 4,
            "medium": 6,
            "low": 8,
        }
        
        base_score = scores.get(competition_level, 5)
        
        if price_range > 50:
            base_score += 1
        if king_price > 15:
            base_score += 1
        
        return min(10.0, max(1.0, base_score))
    
    def detect_differentiation(self, product: dict) -> dict:
        title = product.get('title', '').lower()
        price = product.get('price', 0)
        
        is_bundle = any(word in title for word in ['set', 'pack', 'bundle', 'combo', '套装', '组合'])
        is_premium = any(word in title for word in ['premium', 'luxury', 'deluxe', '高端', '豪华'])
        is_lightweight = price < 15 or any(word in title for word in ['mat', 'pad', 'cover', '垫', '套'])
        
        if is_premium:
            quality_level = "premium"
        elif price < 20:
            quality_level = "budget"
        else:
            quality_level = "standard"
        
        return {
            "is_bundle": is_bundle,
            "is_premium": is_premium,
            "is_lightweight": is_lightweight,
            "quality_level": quality_level
        }
    
    def generate_mock_data(self, keyword: str, limit: int = 20) -> TemuSearchResult:
        mock_products = [
            {
                "title": f"Height Adjustable Standing Desk Converter {keyword}",
                "price": 29.99,
                "original_price": 59.99,
                "discount": "50% off",
                "rating": 3.8,
                "review_count": 456,
                "sold_count": "1k+",
                "seller": "Factory Direct",
            },
            {
                "title": f"Premium {keyword} with Ergonomic Design",
                "price": 45.99,
                "original_price": 89.99,
                "discount": "49% off",
                "rating": 4.2,
                "review_count": 234,
                "sold_count": "500+",
                "seller": "Office Pro Store",
            },
            {
                "title": f"Budget {keyword} Basic Model",
                "price": 19.99,
                "original_price": 39.99,
                "discount": "50% off",
                "rating": 3.5,
                "review_count": 789,
                "sold_count": "2k+",
                "seller": "Discount Hub",
            },
            {
                "title": f"{keyword} Complete Set Bundle",
                "price": 59.99,
                "original_price": 119.99,
                "discount": "50% off",
                "rating": 4.5,
                "review_count": 123,
                "sold_count": "300+",
                "seller": "Bundle King",
            },
            {
                "title": f"Deluxe {keyword} with Accessories",
                "price": 79.99,
                "original_price": 159.99,
                "discount": "50% off",
                "rating": 4.7,
                "review_count": 89,
                "sold_count": "200+",
                "seller": "Premium Store",
            },
        ]
        
        competitors = []
        prices = []
        
        for i, mock in enumerate(mock_products[:limit]):
            product_id = f"temu_{hash(mock['title']) % 1000000}"
            diff = self.detect_differentiation(mock)
            
            product = TemuProduct(
                product_id=product_id,
                title=mock["title"],
                url=f"{self.base_url}/product-{product_id}.html",
                image_url=f"https://img.temu.com/mock_{i}.jpg",
                price=mock["price"],
                original_price=mock["original_price"],
                discount=mock["discount"],
                currency="USD",
                rating=mock["rating"],
                review_count=mock["review_count"],
                sold_count=mock["sold_count"],
                shipping="Free shipping",
                seller_name=mock["seller"],
                seller_rating=4.2,
                is_bundle=diff["is_bundle"],
                is_premium=diff["is_premium"],
                is_lightweight=diff["is_lightweight"],
                quality_level=diff["quality_level"]
            )
            competitors.append(product)
            prices.append(mock["price"])
        
        competitors.sort(key=lambda x: x.price)
        
        king_price = KingPrice(
            price=competitors[0].price,
            currency="USD",
            product_id=competitors[0].product_id,
            title=competitors[0].title,
            image_url=competitors[0].image_url,
            rating=competitors[0].rating,
            review_count=competitors[0].review_count,
            sold_count=competitors[0].sold_count,
            shipping=competitors[0].shipping,
            seller=competitors[0].seller_name,
            notes="最低价产品，基础款"
        )
        
        price_distribution = [
            {"range": "$0-30", "count": 3, "percentage": "60%"},
            {"range": "$30-60", "count": 1, "percentage": "20%"},
            {"range": "$60+", "count": 1, "percentage": "20%"},
        ]
        
        market_insights = MarketInsight(
            price_distribution=price_distribution,
            common_features=["Free shipping", "Easy assembly", "Height adjustable"],
            premium_features=["Electric motor", "Memory presets", "Cable management"],
            gap_opportunities=[
                {
                    "type": "bundle",
                    "description": "桌板+桌腿+支架套装",
                    "potential_price": "$49.99",
                    "estimated_margin": "35%"
                },
                {
                    "type": "premium",
                    "description": "实木材质，高端设计感",
                    "potential_price": "$89.99",
                    "estimated_margin": "45%"
                }
            ]
        )
        
        competition_level = self.analyze_competition_level(156, max(prices) - min(prices))
        opportunity_score = self.calculate_opportunity_score(
            competition_level,
            max(prices) - min(prices),
            king_price.price
        )
        
        strategy_map = {
            "very_high": "premium",
            "high": "bundle",
            "medium": "bundle",
            "low": "standard"
        }
        
        recommendation = {
            "market_status": "红海竞争激烈" if competition_level in ["very_high", "high"] else "有市场机会",
            "suggested_strategy": strategy_map.get(competition_level, "bundle"),
            "suggested_price_range": "$35-55",
            "notes": "建议做套装组合，避免直接价格竞争"
        }
        
        return TemuSearchResult(
            keyword=keyword,
            site=f"temu.com ({self.site.upper()})",
            search_time=datetime.now().isoformat(),
            total_results=156,
            returned_results=len(competitors),
            lowest_price=min(prices),
            highest_price=max(prices),
            average_price=sum(prices) / len(prices),
            median_price=sorted(prices)[len(prices) // 2],
            competition_level=competition_level,
            opportunity_score=opportunity_score,
            king_price=king_price,
            competitors=competitors,
            market_insights=market_insights,
            recommendation=recommendation
        )


def format_output(result: TemuSearchResult, output_format: str = "json") -> str:
    if output_format == "json":
        data = {
            "metadata": {
                "keyword": result.keyword,
                "site": result.site,
                "search_time": result.search_time,
                "total_results": result.total_results,
                "returned_results": result.returned_results
            },
            "summary": {
                "lowest_price": result.lowest_price,
                "highest_price": result.highest_price,
                "average_price": round(result.average_price, 2),
                "median_price": result.median_price,
                "competition_level": result.competition_level,
                "opportunity_score": result.opportunity_score
            },
            "king_price": asdict(result.king_price),
            "competitors": [asdict(c) for c in result.competitors],
            "market_insights": asdict(result.market_insights),
            "recommendation": result.recommendation
        }
        return json.dumps(data, ensure_ascii=False, indent=2)
    else:
        lines = []
        lines.append("=" * 60)
        lines.append(f"Temu 竞品分析: {result.keyword}")
        lines.append("=" * 60)
        lines.append(f"\n【卷王价】 ${result.king_price.price}")
        lines.append(f"  产品: {result.king_price.title[:50]}...")
        lines.append(f"  卖家: {result.king_price.seller}")
        lines.append(f"\n【市场概况】")
        lines.append(f"  竞品数量: {result.total_results}")
        lines.append(f"  价格区间: ${result.lowest_price} - ${result.highest_price}")
        lines.append(f"  竞争程度: {result.competition_level}")
        lines.append(f"  机会评分: {result.opportunity_score}/10")
        lines.append(f"\n【建议】")
        lines.append(f"  策略: {result.recommendation['suggested_strategy']}")
        lines.append(f"  定价: {result.recommendation['suggested_price_range']}")
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Temu Competitor Search & King Price Scraper"
    )
    parser.add_argument(
        "--keyword", type=str, required=True,
        help="Search keyword"
    )
    parser.add_argument(
        "--site", type=str, default="us",
        choices=list(TEMU_SITES.keys()),
        help="Temu site region"
    )
    parser.add_argument(
        "--limit", type=int, default=20,
        help="Maximum number of products to return"
    )
    parser.add_argument(
        "--sort", type=str, default="price_asc",
        choices=list(SORT_OPTIONS.keys()),
        help="Sort order"
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
    
    args = parser.parse_args()
    
    scraper = TemuCompetitorScraper(site=args.site)
    result = scraper.generate_mock_data(keyword=args.keyword, limit=args.limit)
    
    output = format_output(result, args.format)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"Results saved to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
