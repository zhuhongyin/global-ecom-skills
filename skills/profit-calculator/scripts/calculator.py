#!/usr/bin/env python3
"""
Profit Calculator V4.1
跨境电商利润计算器
"""

import json
from datetime import datetime
from typing import Dict, Optional

class ProfitCalculator:
    """V4.1核价模型利润计算器"""
    
    PAYMENT_RATE = 0.45
    EXCHANGE_RATE = 7.2
    FULFILLMENT_FEE = 3.50
    MIN_PROFIT = 5.00
    
    def __init__(self, temu_price: float, price_1688: float):
        """
        初始化计算器
        
        Args:
            temu_price: Temu卷王价（美元）
            price_1688: 1688拿货价（人民币）
        """
        self.temu_price = temu_price
        self.price_1688 = price_1688
    
    def calculate(self) -> Dict:
        """计算利润"""
        payment_usd = self.temu_price * self.PAYMENT_RATE
        income_cny = payment_usd * self.EXCHANGE_RATE
        total_cost = self.price_1688 + self.FULFILLMENT_FEE
        net_profit = income_cny - total_cost
        profit_rate = (net_profit / total_cost * 100) if total_cost > 0 else 0
        
        return {
            "timestamp": datetime.now().isoformat(),
            "input": {
                "temu_price": self.temu_price,
                "price_1688": self.price_1688
            },
            "income": {
                "temu_price_usd": round(self.temu_price, 2),
                "payment_rate": f"{self.PAYMENT_RATE * 100}%",
                "payment_usd": round(payment_usd, 2),
                "exchange_rate": self.EXCHANGE_RATE,
                "income_cny": round(income_cny, 2)
            },
            "cost": {
                "price_1688": round(self.price_1688, 2),
                "fulfillment_fee": self.FULFILLMENT_FEE,
                "total_cost": round(total_cost, 2)
            },
            "result": {
                "net_profit": round(net_profit, 2),
                "profit_rate": round(profit_rate, 1),
                "is_profitable": net_profit > self.MIN_PROFIT,
                "verdict": "✅ GO" if net_profit > self.MIN_PROFIT else "❌ PASS"
            }
        }
    
    def get_recommendation(self) -> str:
        """获取推荐建议"""
        result = self.calculate()
        net_profit = result["result"]["net_profit"]
        
        if net_profit > 20:
            return "优秀利润空间，强烈推荐上架"
        elif net_profit > 10:
            return "良好利润空间，推荐上架"
        elif net_profit > self.MIN_PROFIT:
            return "利润达标，可以考虑上架"
        else:
            return "利润不足，不建议上架"

def batch_calculate(products: list) -> list:
    """批量计算多个产品"""
    results = []
    for product in products:
        calc = ProfitCalculator(
            product.get("temu_price", 0),
            product.get("price_1688", 0)
        )
        result = calc.calculate()
        result["product_name"] = product.get("name", "Unknown")
        results.append(result)
    return results

if __name__ == "__main__":
    calculator = ProfitCalculator(temu_price=12.99, price_1688=25.0)
    result = calculator.calculate()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"\n推荐建议: {calculator.get_recommendation()}")
