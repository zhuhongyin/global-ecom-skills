#!/usr/bin/env python3
"""
Temu Competitor Analyzer
分析Temu平台竞品情况
"""

import json
from datetime import datetime
from typing import List, Dict

def analyze_temu_competition(competitors: List[Dict]) -> Dict:
    """
    分析Temu竞品数据
    
    Args:
        competitors: 竞品列表
        
    Returns:
        分析结果
    """
    if not competitors:
        return {"error": "No competitor data provided"}
    
    prices = [c.get("price", 0) for c in competitors]
    sales = [c.get("sales", 0) for c in competitors]
    
    analysis = {
        "timestamp": datetime.now().isoformat(),
        "total_competitors": len(competitors),
        "price_analysis": {
            "min_price": min(prices),
            "max_price": max(prices),
            "avg_price": sum(prices) / len(prices),
            "price_range": max(prices) - min(prices)
        },
        "sales_analysis": {
            "total_sales": sum(sales),
            "avg_sales": sum(sales) / len(sales),
            "top_seller_sales": max(sales)
        },
        "market_saturation": calculate_saturation(len(competitors)),
        "opportunity_assessment": assess_opportunity(competitors)
    }
    
    return analysis

def calculate_saturation(competitor_count: int) -> str:
    """计算市场饱和度"""
    if competitor_count < 100:
        return "低"
    elif competitor_count < 1000:
        return "中"
    elif competitor_count < 5000:
        return "较高"
    else:
        return "高"

def assess_opportunity(competitors: List[Dict]) -> Dict:
    """评估上架机会"""
    prices = [c.get("price", 0) for c in competitors]
    min_price = min(prices)
    
    low_quality_count = sum(1 for c in competitors if c.get("rating", 0) < 4.0)
    differentiation_potential = "高" if low_quality_count > len(competitors) * 0.3 else "中"
    
    return {
        "king_price": min_price,
        "differentiation_potential": differentiation_potential,
        "recommendation": "建议上架" if min_price > 8 else "需谨慎定价"
    }

if __name__ == "__main__":
    sample_competitors = [
        {"name": "Product A", "price": 12.99, "sales": 500, "rating": 4.2},
        {"name": "Product B", "price": 15.99, "sales": 300, "rating": 3.8},
        {"name": "Product C", "price": 10.99, "sales": 800, "rating": 4.5}
    ]
    result = analyze_temu_competition(sample_competitors)
    print(json.dumps(result, indent=2))
