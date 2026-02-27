# E-Commerce Skills 选品系统 

## 📝 开发说明

本系统是一个基于 Skills 模块的跨境电商选品工具，通过多维度数据分析，帮助卖家快速筛选高利润产品。

---

## 🎯 快速开始

```bash
# 1. 克隆项目
git clone https://github.com/zhuhongyin/global-ecom-skills.git

# 2. 进入目录
cd lgskill3

# 3. 安装依赖
pip install requests beautifulsoup4 -i https://pypi.org/simple/

# 4. 使用 Skills
python3 skills/amazon-movers-shakers/scripts/scrape_amazon.py --site us --category home-garden --limit 10
```

---

## 📋 功能介绍

本系统通过多个独立的 Skills 模块，提供完整的选品分析功能：

| 功能模块 | 说明 |
|---------|------|
| Amazon 飙升榜数据获取 | 抓取 Amazon 热销产品，发现市场趋势 |
| Temu 竞品分析 | 分析 Temu 平台竞品价格，确定市场定价上限 |
| 1688 供应链查询 | 查询 1688 工厂批发价，确定采购成本 |
| V4.1 核价计算 | 自动计算净利润，判断产品是否值得做 |

---

## 📁 目录结构

```
lgskill3/
├── skills/                     # Skills 模块
│   ├── amazon-movers-shakers/
│   │   └── scripts/
│   │       └── scrape_amazon.py      # Amazon 飙升榜爬取
│   ├── temu-competitor-search/
│   │   └── scripts/
│   │       └── scrape_temu.py         # Temu 竞品分析
│   ├── ali1688-sourcing/
│   │   └── scripts/
│   │       └── scrape_1688.py          # 1688 供应链查询
│   └── temu-pricing-calculator/
│       └── scripts/
│           └── calculate_pricing.py      # V4.1 核价计算
└── README.md                   # 本文档
```

---

## 🔧 核心模块说明

### 1. Amazon 飙升榜爬取 (`scrape_amazon.py`)

**功能**：获取 Amazon 热销产品数据

**数据源优先级**：
1. 卖家精灵 API（需 API Key）
2. 真实爬取（requests + BeautifulSoup4）
3. Mock 数据（兜底方案）

**输出字段**：
```json
{
  "metadata": {
    "site": "amazon.com",
    "data_source": "scrape/mock/sellersprite",
    "total_products": 10
  },
  "products": [
    {
      "asins": "B06WWRCZXX",
      "title": "Queen Size 4 Piece Sheet Set",
      "price": 24.99,
      "rating": 4.5,
      "rank": 1,
      "rank_change": "+256"
    }
  ]
}
```

**支持类目**（10 个）：
- Home & Kitchen (家居用品)
- Electronics (电子产品)
- Sports & Outdoors (户外用品)
- Office Products (办公用品)
- Beauty & Personal Care (美妆个护)
- Toys & Games (玩具游戏)
- Clothing & Accessories (服装配饰)
- Jewelry & Watches (珠宝手表)
- Automotive (汽车用品)
- Pet Supplies (宠物用品)

**使用方法**：
```bash
python3 skills/amazon-movers-shakers/scripts/scrape_amazon.py \
  --site us \
  --category home-garden \
  --limit 10 \
  --source auto        # auto/mock/scrape/sellersprite
```

---

### 2. Temu 竞品分析 (`scrape_temu.py`)

**功能**：分析 Temu 平台竞品，获取「卷王价」

**数据源优先级**：
1. 真实爬取（requests + BeautifulSoup4）
2. Mock 数据（兜底方案）

**输出字段**：
```json
{
  "metadata": {
    "keyword": "Standing Desk",
    "site": "temu.com (US)",
    "data_source": "scrape/mock"
  },
  "king_price": {
    "price": 29.99,
    "currency": "USD",
    "product_id": "temu_123456",
    "title": "Height Adjustable Standing Desk Converter",
    "rating": 3.8,
    "sold_count": "1k+"
  },
  "competitors": [
    {
      "product_id": "temu_234567",
      "title": "Premium Standing Desk with Ergonomic Design",
      "price": 45.99,
      "discount": "49% off"
    }
  ],
  "market_insights": {
    "price_distribution": [...],
    "common_features": [...],
    "gap_opportunities": [...]
  }
}
```

**使用方法**：
```bash
python3 skills/temu-competitor-search/scripts/scrape_temu.py \
  --keyword "Standing Desk" \
  --limit 10 \
  --site us
```

---

### 3. 1688 供应链查询 (`scrape_1688.py`)

**功能**：查询 1688 工厂批发价

**数据源优先级**：
1. 真实爬取（requests + BeautifulSoup4）
2. Mock 数据（兜底方案）

**输出字段**：
```json
{
  "metadata": {
    "keyword": "Standing Desk",
    "search_time": "2026-02-27T14:00:00",
    "total_results": 1256,
    "data_source": "scrape/mock"
  },
  "wholesale_price": {
    "min_price": 105.0,
    "max_price": 105.0,
    "recommended_price": 105.0,
    "currency": "CNY",
    "unit": "件",
    "note": "建议以 ¥105 作为核价参考价"
  },
  "factories": [
    {
      "rank": 1,
      "company_name": "安吉县宏达家具有限公司",
      "location": {"province": "浙江", "city": "安吉"},
      "verified": true,
      "verification_type": "深度验厂",
      "rating": 4.8,
      "products": [
        {
          "title": "站立式办公桌 可折叠",
          "price_tiers": [
            {"quantity": "1-9", "price": 25.0},
            {"quantity": "10-49", "price": 20.0},
            {"quantity": "50+", "price": 18.0}
          ],
          "starting_price": 18.0,
          "moq": 10,
          "material": "冷轧钢+环保板材"
        }
      ]
    }
  ],
  "summary": {
    "lowest_price": 105.0,
    "highest_price": 105.0,
    "average_price": 105.0,
    "main_production_areas": ["浙江", "广东", "江苏"]
  }
}
```

**使用方法**：
```bash
python3 skills/ali1688-sourcing/scripts/scrape_1688.py \
  --keyword "Standing Desk" \
  --limit 10
```

---

### 4. V4.1 核价计算 (`calculate_pricing.py`)

**功能**：计算产品净利润，判断是否值得做

**核价公式**：
```
回款预估 = Temu 卷王价 × 平台费率 (45%) × 汇率 (7.2)
总成本 = 1688 批发价 + 履约费 (¥3.5)
净利润 = 回款 - 总成本
```

**决策规则**：
| 净利润 (¥) | 状态 | 说明 |
|-----------|------|------|
| > 10 | STRONG GO | 高利润，优先上架 |
| > 5 | GO | 利润达标，建议上架 |
| > 3 | MARGINAL | 利润边缘，需优化 |
| ≤ 3 | PASS | 利润不足，直接淘汰 |

**使用方法**：
```bash
# 默认阈值：¥5.0
python3 skills/temu-pricing-calculator/scripts/calculate_pricing.py \
  --temu-price 29.99 \
  --ali1688-price 20.0 \
  --profit-threshold 5.0

# 自定义阈值
python3 skills/temu-pricing-calculator/scripts/calculate_pricing.py \
  --temu-price 29.99 \
  --ali1688-price 20.0 \
  --profit-threshold 1.0
```

---

## 📊 选品流程

```
┌─────────────────────────────────────────────────────────────┐
│                                                         │
│  Step 1: Amazon 飙升榜                              │
│  ├─ 获取产品列表（ASIN/标题/价格/排名）            │
│                                                         │
│  Step 2: Temu 竞品分析（对每个候选产品）          │
│  ├─ 用产品标题关键词搜索 Temu                           │
│  ├─ 获取最低价竞品（卷王价）                          │
│  └─ 返回竞品数据（价格/评分/销量）                    │
│                                                         │
│  Step 3: 1688 供应链查询（对每个候选产品）          │
│  ├─ 用相同关键词搜索 1688                             │
│  ├─ 获取工厂批发价（阶梯价）                           │
│  └─ 返回供应链数据（最低价/推荐价）                │
│                                                         │
│  Step 4: V4.1 核价计算（对每个候选产品）          │
│  ├─ 输入：Temu 卷王价 + 1688 批发价                    │
│  ├─ 计算：回款 = 卷王价 × 45% × 7.2                  │
│  ├─ 计算：总成本 = 批发价 + ¥3.5                    │
│  ├─ 计算：净利润 = 回款 - 总成本                        │
│  └─ 返回：GO / PASS / MARGINAL / STRONG GO            │
│                                                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔍 核心业务逻辑

### 选品流程

```python
for each candidate_product in amazon_products:
    keyword = extract_keyword(candidate_product.title)
    
    # Step 2: Temu 竞品分析
    temu_data = search_temu(keyword)
    king_price = temu_data.king_price.price
    
    # Step 3: 1688 供应链查询
    ali1688_data = search_1688(keyword)
    ali1688_price = ali1688_data.wholesale_price.recommended_price
    
    # Step 4: V4.1 核价计算
    pricing_data = calculate_pricing(
        temu_price=king_price,
        ali1688_price=ali1688_price,
        profit_threshold=5.0
    )
    
    if pricing_data.decision.status in ['GO', 'STRONG GO']:
        go_products.append({
            amazon: candidate_product,
            temu: temu_data,
            ali1688: ali1688_data,
            pricing: pricing_data
        })

return go_products
```

### 核价决策矩阵

| Temu 卷王价 | 1688 批发价 | 回款 (45%) | 总成本 | 净利润 | 决策 |
|-----------|-------------|-------------|----------|--------|--------|------|
| $29.99 | ¥20.0 | ¥97.17 | ¥23.5 | ¥73.67 | STRONG GO |
| $45.99 | ¥25.0 | ¥148.87 | ¥28.5 | ¥120.37 | STRONG GO |
| $19.99 | ¥18.0 | ¥71.91 | ¥21.5 | ¥50.41 | STRONG GO |
| $12.99 | ¥15.0 | ¥46.75 | ¥18.5 | ¥28.25 | STRONG GO |
| $8.99 | ¥12.0 | ¥32.38 | ¥15.5 | ¥16.88 | STRONG GO |
| $6.99 | ¥10.0 | ¥25.27 | ¥13.5 | ¥11.77 | GO |
| $4.99 | ¥8.0 | ¥17.96 | ¥11.5 | ¥6.46 | MARGINAL |
| $2.99 | ¥6.0 | ¥10.79 | ¥9.5 | ¥1.29 | PASS |

---

## ⚙️ 配置说明

### 环境要求

- Python 3.9+
- requests
- beautifulsoup4

### 依赖安装

```bash
pip install requests beautifulsoup4 -i https://pypi.org/simple/
```

---

**文档版本**：v2.0  
**最后更新**：2026-02-27
