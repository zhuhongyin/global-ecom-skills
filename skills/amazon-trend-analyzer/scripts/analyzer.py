#!/usr/bin/env python3
"""
Amazon Movers & Shakers Analyzer
分析亚马逊飙升榜数据
"""

import json
import re
from datetime import datetime

def analyze_amazon_trends(product_data: dict) -> dict:
    """
    分析亚马逊产品趋势数据
    
    Args:
        product_data: 包含产品信息的字典
        
    Returns:
        分析结果字典
    """
    analysis = {
        "timestamp": datetime.now().isoformat(),
        "products": [],
        "summary": {}
    }
    
    for product in product_data.get("products", []):
        product_analysis = {
            "name": product.get("name", ""),
            "asin": product.get("asin", ""),
            "price": product.get("price", 0),
            "rank_change": product.get("rank_change", 0),
            "category": product.get("category", ""),
            "rating": product.get("rating", 0),
            "review_count": product.get("review_count", 0),
            "opportunity_score": calculate_opportunity_score(product)
        }
        analysis["products"].append(product_analysis)
    
    analysis["summary"] = {
        "total_products": len(analysis["products"]),
        "avg_price": sum(p["price"] for p in analysis["products"]) / len(analysis["products"]) if analysis["products"] else 0,
        "high_opportunity_count": sum(1 for p in analysis["products"] if p["opportunity_score"] >= 7)
    }
    
    return analysis

def calculate_opportunity_score(product: dict) -> float:
    """
    计算产品机会评分 (0-10)
    
    评分标准：
    - 飙升幅度 (30%)
    - 评论数量 (25%) - 评论少机会大
    - 评分 (20%)
    - 价格区间 (25%)
    """
    score = 0
    
    rank_change = product.get("rank_change", 0)
    if rank_change >= 500:
        score += 3
    elif rank_change >= 200:
        score += 2
    elif rank_change >= 100:
        score += 1
    
    review_count = product.get("review_count", 0)
    if review_count < 50:
        score += 2.5
    elif review_count < 100:
        score += 2
    elif review_count < 200:
        score += 1
    
    rating = product.get("rating", 0)
    if rating >= 4.5:
        score += 2
    elif rating >= 4.0:
        score += 1.5
    elif rating >= 3.5:
        score += 1
    
    price = product.get("price", 0)
    if 10 <= price <= 50:
        score += 2.5
    elif 50 < price <= 100:
        score += 2
    elif price < 10:
        score += 1
    
    return round(score, 1)

if __name__ == "__main__":
    sample_data = {
        "products": [
            {
                "name": "Sample Product",
                "asin": "B0XXXXX",
                "price": 25.99,
                "rank_change": 350,
                "category": "Home & Kitchen",
                "rating": 4.5,
                "review_count": 45
            }
        ]
    }
    result = analyze_amazon_trends(sample_data)
    print(json.dumps(result, indent=2))
