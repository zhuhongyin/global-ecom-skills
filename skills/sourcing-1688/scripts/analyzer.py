#!/usr/bin/env python3
"""
1688 Sourcing Script
1688货源查找和分析
"""

import json
from datetime import datetime
from typing import List, Dict

def analyze_sourcing(suppliers: List[Dict]) -> Dict:
    """
    分析1688供应商数据
    
    Args:
        suppliers: 供应商列表
        
    Returns:
        分析结果
    """
    if not suppliers:
        return {"error": "No supplier data provided"}
    
    prices = [s.get("price", 0) for s in suppliers]
    
    analysis = {
        "timestamp": datetime.now().isoformat(),
        "total_suppliers": len(suppliers),
        "price_analysis": {
            "min_price": min(prices),
            "max_price": max(prices),
            "avg_price": sum(prices) / len(prices),
            "recommended_price": min(prices) * 1.1
        },
        "top_suppliers": rank_suppliers(suppliers)[:5],
        "sourcing_tips": generate_sourcing_tips(suppliers)
    }
    
    return analysis

def rank_suppliers(suppliers: List[Dict]) -> List[Dict]:
    """供应商排名"""
    scored_suppliers = []
    
    for supplier in suppliers:
        score = 0
        
        price = supplier.get("price", 0)
        avg_price = sum(s.get("price", 0) for s in suppliers) / len(suppliers)
        if price < avg_price * 0.9:
            score += 30
        elif price < avg_price:
            score += 20
        
        if supplier.get("is_super_factory", False):
            score += 25
        elif supplier.get("is_trustworthy", False):
            score += 15
        
        years = supplier.get("trust_years", 0)
        if years >= 5:
            score += 15
        elif years >= 3:
            score += 10
        
        repurchase_rate = supplier.get("repurchase_rate", 0)
        if repurchase_rate >= 30:
            score += 15
        elif repurchase_rate >= 20:
            score += 10
        
        scored_suppliers.append({
            **supplier,
            "score": score
        })
    
    return sorted(scored_suppliers, key=lambda x: x["score"], reverse=True)

def generate_sourcing_tips(suppliers: List[Dict]) -> List[str]:
    """生成采购建议"""
    tips = []
    
    super_factories = [s for s in suppliers if s.get("is_super_factory", False)]
    if super_factories:
        tips.append(f"发现{len(super_factories)}家超级工厂，建议优先联系")
    
    avg_price = sum(s.get("price", 0) for s in suppliers) / len(suppliers)
    tips.append(f"市场均价约¥{avg_price:.2f}，建议议价空间5-10%")
    
    tips.append("建议先索要样品确认质量后再大批量采购")
    
    return tips

if __name__ == "__main__":
    sample_suppliers = [
        {
            "name": "工厂A",
            "price": 25.0,
            "moq": 50,
            "is_super_factory": True,
            "trust_years": 5,
            "repurchase_rate": 35
        },
        {
            "name": "工厂B",
            "price": 28.0,
            "moq": 30,
            "is_super_factory": False,
            "is_trustworthy": True,
            "trust_years": 3,
            "repurchase_rate": 25
        }
    ]
    result = analyze_sourcing(sample_suppliers)
    print(json.dumps(result, indent=2))
