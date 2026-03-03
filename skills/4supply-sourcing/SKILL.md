---
name: 4supply-sourcing
description: 4supply 平台商品与机会位洞察工具。当用户需要在乐歌公司 B2B 平台 4supply 查找竞品、分析市场机会、判断产品是否适合上架时使用此 skill。输入产品关键词，输出商品列表、价格区间、市场机会判断，为选品决策提供数据支持。
---

# 4supply 平台商品与机会位洞察

## 核心定位

这是 Loctek 公司自有的 B2B 平台分析工具。在 4supply 平台查找同类产品，判断市场机会和竞争格局，为选品决策提供重要参考。

## 平台信息

- **平台名称**: 4supply (乐歌 B2B 平台)
- **网站地址**: https://www.4supply.com
- **平台定位**: 跨境电商 B2B 批发平台
- **主要类目**: 家居办公、健身器材、升降桌等

## 输入参数

```json
{
  "keyword": "standing desk converter",
  "category": "Home Office",
  "limit": 20,
  "min_price": 50.0,
  "max_price": 500.0
}
```

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `keyword` | string | 是 | - | 搜索关键词 |
| `category` | string | 否 | 全类目 | 商品类目 |
| `limit` | int | 否 | 20 | 返回商品数量 |
| `min_price` | float | 否 | 无 | 最低价格筛选 |
| `max_price` | float | 否 | 无 | 最高价格筛选 |

## 输出格式

```json
{
  "metadata": {
    "keyword": "standing desk converter",
    "search_time": "2026-02-26T10:30:00Z",
    "platform": "4supply.com",
    "total_results": 45,
    "returned_results": 20
  },
  "summary": {
    "lowest_price": 89.00,
    "highest_price": 459.00,
    "average_price": 189.50,
    "median_price": 165.00,
    "price_range": "$89 - $459",
    "competition_level": "medium",
    "opportunity_score": 7.5
  },
  "market_insights": {
    "market_status": "有空间",
    "existing_sellers": 12,
    "top_seller": "Loctek Official",
    "market_saturation": "35%",
    "growth_trend": "上升",
    "opportunity_gaps": [
      {
        "type": "price_gap",
        "description": "$120-150 价格区间产品较少",
        "potential": "medium"
      },
      {
        "type": "feature_gap",
        "description": "电动升降款型较少",
        "potential": "high"
      }
    ]
  },
  "products": [
    {
      "rank": 1,
      "product_id": "4s_123456",
      "title": "Electric Standing Desk Converter with Memory Presets",
      "url": "https://www.4supply.com/product/123456",
      "image_url": "https://cdn.4supply.com/xxx.jpg",
      "price": 189.00,
      "original_price": 259.00,
      "currency": "USD",
      "moq": 10,
      "seller": {
        "name": "Loctek Official",
        "verified": true,
        "rating": 4.8,
        "location": "Ningbo, China"
      },
      "specifications": {
        "material": "Steel + MDF",
        "color": "Black/White",
        "size": "120cm x 60cm",
        "weight_capacity": "100kg"
      },
      "trade_info": {
        "min_order": 10,
        "lead_time": "15-20 days",
        "payment_terms": ["T/T", "L/C", "PayPal"],
        "shipping": "FOB Ningbo"
      },
      "ratings": {
        "average": 4.6,
        "count": 128
      },
      "sales_data": {
        "monthly_sales": "500+",
        "repeat_rate": "45%"
      },
      "certifications": ["CE", "FCC", "UL"],
      "is_bestseller": true,
      "is_new": false
    }
  ],
  "opportunity_analysis": {
    "market_status": "有空间",
    "recommendation": "建议上架",
    "reasons": [
      "价格区间有空间，$120-150 区间竞争较少",
      "电动款型需求上升",
      "平台自有品牌优势"
    ],
    "risks": [
      "需与现有 Loctek 产品差异化",
      "价格需有竞争力"
    ],
    "suggested_price_range": "$120-180",
    "estimated_margin": "35-45%"
  },
  "comparison_with_temu": {
    "temu_king_price": 29.99,
    "supply4_price": 189.00,
    "price_gap": "5.3x",
    "market_difference": "4supply 为 B2B 批发，价格高于 Temu 零售",
    "strategy_suggestion": "可在 4supply 做高端批发，Temu 做零售走量"
  }
}
```

## 关键输出字段

### 市场机会判断 (opportunity_analysis)

| 市场状态 | 说明 | 建议 |
|----------|------|------|
| `蓝海` | 竞品 < 10，需求存在 | 优先上架 |
| `有空间` | 竞品 10-30，有差异化机会 | 建议上架 |
| `中度竞争` | 竞品 30-50，需强差异化 | 谨慎评估 |
| `红海` | 竞品 > 50，价格战激烈 | 不建议上架 |

### 机会评分 (opportunity_score)

综合评分（1-10分），考虑因素：
- 竞争密度（30%）
- 价格空间（25%）
- 市场需求（25%）
- 差异化机会（20%）

### 与 Temu 对比 (comparison_with_temu)

提供 4supply 与 Temu 的价格对比，帮助制定双平台策略。

## 使用方式

### 方式一：Web 搜索获取

```
搜索词: "site:4supply.com standing desk"
```

### 方式二：WebFetch 获取

```
URL: https://www.4supply.com/search?q=standing+desk
```

### 方式三：API 获取（如有）

```bash
python scripts/scrape_4supply.py --keyword "standing desk" --limit 20
```

### 方式四：Mock 数据（开发/测试）

```bash
python scripts/scrape_4supply.py --source mock --keyword "desk converter"
```

## 与其他 Skills 协作

- 接收 `amazon-movers-shakers` 的产品关键词
- 与 `temu-competitor-search` 结果对比分析
- 为 `ecom-product-orchestrator` 提供多平台决策依据

## 注意事项

1. **平台特性**：4supply 是 B2B 平台，价格通常高于零售平台

2. **自有品牌优势**：Loctek 产品在平台有品牌优势

3. **MOQ 要求**：注意最小起订量要求

4. **认证要求**：出口产品需确认认证证书

5. **价格策略**：B2B 价格与 Temu 零售价格需差异化定位

## 示例用法

**示例 1：查找产品机会**
```
用户：帮我看看 "standing desk" 在 4supply 上有没有机会

执行：
1. 搜索 4supply 上的 standing desk 产品
2. 分析竞争格局和价格空间
3. 返回机会分析报告
```

**示例 2：双平台对比**
```
用户：对比 "desk mat" 在 Temu 和 4supply 上的情况

执行：
1. 分别查询两个平台的产品
2. 对比价格、竞争程度
3. 给出双平台策略建议
```

**示例 3：价格定位**
```
用户：我的产品成本 $50，在 4supply 上应该卖多少钱？

执行：
1. 查询同类产品价格区间
2. 分析竞争格局
3. 给出定价建议
```
