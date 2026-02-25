#!/usr/bin/env python3
"""
Product Recommender
选品推荐整合器
"""

import json
from datetime import datetime
from typing import List, Dict, Optional

class ProductRecommender:
    """选品推荐器"""
    
    MIN_PROFIT = 5.00
    
    def __init__(self):
        self.products = []
    
    def add_product(self, product: Dict) -> None:
        """添加产品数据"""
        self.products.append(product)
    
    def analyze_all(self) -> Dict:
        """分析所有产品并生成推荐"""
        recommendations = []
        
        for product in self.products:
            analysis = self.analyze_product(product)
            if analysis["passed"]:
                recommendations.append(analysis)
        
        recommendations.sort(key=lambda x: x["score"], reverse=True)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "total_analyzed": len(self.products),
            "passed_count": len(recommendations),
            "recommendations": recommendations[:5],
            "summary": self.generate_summary(recommendations)
        }
    
    def analyze_product(self, product: Dict) -> Dict:
        """分析单个产品"""
        score = 0
        passed = True
        reasons = []
        
        net_profit = product.get("net_profit", 0)
        if net_profit >= self.MIN_PROFIT:
            score += 40
            if net_profit >= 20:
                score += 20
            elif net_profit >= 10:
                score += 10
        else:
            passed = False
            reasons.append(f"净利润¥{net_profit}未达标(需>¥{self.MIN_PROFIT})")
        
        competition = product.get("competition_level", "中")
        if competition == "低":
            score += 30
        elif competition == "中":
            score += 20
        else:
            score -= 10
            reasons.append("竞争程度过高")
        
        amazon_rank = product.get("amazon_rank_change", 0)
        if amazon_rank >= 500:
            score += 20
        elif amazon_rank >= 200:
            score += 15
        elif amazon_rank >= 100:
            score += 10
        
        compliance = product.get("compliance_risk", "低")
        if compliance == "高":
            passed = False
            reasons.append("合规风险过高")
        elif compliance == "中":
            score -= 5
        
        return {
            "product_name": product.get("name", "Unknown"),
            "score": score,
            "passed": passed,
            "net_profit": net_profit,
            "competition_level": competition,
            "amazon_rank_change": amazon_rank,
            "compliance_risk": compliance,
            "reasons": reasons if not passed else ["符合所有筛选标准"]
        }
    
    def generate_summary(self, recommendations: List[Dict]) -> Dict:
        """生成汇总信息"""
        if not recommendations:
            return {
                "message": "没有符合条件的产品推荐",
                "suggestion": "请调整筛选条件或寻找其他品类"
            }
        
        return {
            "total_recommendations": len(recommendations),
            "avg_profit": sum(r["net_profit"] for r in recommendations) / len(recommendations),
            "top_category": "待分析",
            "message": f"共推荐{len(recommendations)}款产品"
        }

def generate_report(analysis_result: Dict) -> str:
    """生成Markdown格式报告"""
    report = []
    report.append("# 🛒 跨境电商选品推荐报告\n")
    report.append(f"**生成时间**: {analysis_result['timestamp']}\n")
    report.append(f"**分析产品数**: {analysis_result['total_analyzed']}\n")
    report.append(f"**推荐产品数**: {analysis_result['passed_count']}\n")
    report.append("---\n")
    
    for i, rec in enumerate(analysis_result["recommendations"], 1):
        report.append(f"\n## 📦 产品{i}: {rec['product_name']}\n")
        report.append(f"- **综合评分**: {rec['score']}分\n")
        report.append(f"- **净利润**: ¥{rec['net_profit']}\n")
        report.append(f"- **竞争程度**: {rec['competition_level']}\n")
        report.append(f"- **亚马逊飙升幅度**: {rec['amazon_rank_change']}\n")
        report.append(f"- **判定**: {'✅ 推荐上架' if rec['passed'] else '❌ 不推荐'}\n")
    
    return "".join(report)

if __name__ == "__main__":
    recommender = ProductRecommender()
    
    sample_products = [
        {
            "name": "桌垫 Desk Mat",
            "net_profit": 13.59,
            "competition_level": "低",
            "amazon_rank_change": 350,
            "compliance_risk": "低"
        },
        {
            "name": "显示器支架 Monitor Stand",
            "net_profit": 8.50,
            "competition_level": "中",
            "amazon_rank_change": 200,
            "compliance_risk": "低"
        },
        {
            "name": "某高风险产品",
            "net_profit": 15.00,
            "competition_level": "高",
            "amazon_rank_change": 100,
            "compliance_risk": "高"
        }
    ]
    
    for product in sample_products:
        recommender.add_product(product)
    
    result = recommender.analyze_all()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("\n" + "="*50 + "\n")
    print(generate_report(result))
