# Global E-Commerce Skills

跨境电商选品智能体 Skills 集合，用于 Claude Code 等 AI 编程助手。

## 安装方式

```bash
# 安装所有 skills
npx skills add zhuhongyin/global-ecom-skills

# 安装特定 skill
npx skills add zhuhongyin/global-ecom-skills --skill temu-pricing-calculator
npx skills add zhuhongyin/global-ecom-skills --skill amazon-movers-shakers
npx skills add zhuhongyin/global-ecom-skills --skill temu-competitor-search
npx skills add zhuhongyin/global-ecom-skills --skill ali1688-sourcing
npx skills add zhuhongyin/global-ecom-skills --skill ecom-product-orchestrator

# 列出可用的 skills
npx skills add zhuhongyin/global-ecom-skills --list
```

## Skills 列表

### 1. temu-pricing-calculator (V4.1 核价计算器)

**用途**：计算产品在 Temu 平台的净利润，判断是否达到利润红线（净利 > ¥5）

**输入**：
- Temu 卷王价
- 1688 拿货价

**输出**：
- 详细利润计算过程
- GO/PASS 决策

**示例**：
```
帮我计算这个产品的利润：
- Temu 卷王价: $12.99
- 1688 拿货价: ¥25
```

### 2. amazon-movers-shakers (亚马逊飙升榜)

**用途**：获取亚马逊 Movers & Shakers 飙升榜数据，发现爆款趋势

**输入**：
- 站点（amazon.com 等）
- 类目（home-garden 等）

**输出**：
- 飙升商品列表
- 价格、排名、趋势数据

**示例**：
```
帮我看看亚马逊家居类最近有什么飙升的产品
```

### 3. temu-competitor-search (Temu 竞品查询)

**用途**：查找 Temu 竞品，获取卷王价，分析竞争格局

**输入**：
- 产品关键词

**输出**：
- 竞品列表
- 卷王价（最低价）
- 差异化机会

**示例**：
```
帮我查一下 "desk mat" 在 Temu 上的最低价
```

### 4. ali1688-sourcing (1688 供应链查询)

**用途**：查找 1688 工厂，获取批发价格，生成采购指令

**输入**：
- 产品关键词
- 材质/认证要求

**输出**：
- 工厂列表
- 起批价区间
- 采购找货指令

**示例**：
```
帮我找 "升降桌转换器" 在 1688 上的工厂和价格
```

### 5. ecom-product-orchestrator (选品编排器)

**用途**：串联完整选品流程，输出 5 款推荐产品报告

**输入**：
- 目标站点和类目
- 产品数量

**输出**：
- 完整选品报告
- 前端营销逻辑 + 后端生存逻辑

**示例**：
```
帮我推荐 5 款适合 Temu 上架的产品
```

## 工作流程

```
┌─────────────────────────────────────────────────────────────────┐
│                    选品智能体编排流程                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Step 1: amazon-movers-shakers                                  │
│  → 获取亚马逊飙升榜候选产品                                        │
│                                                                 │
│  Step 2: temu-competitor-search                                 │
│  → 查询 Temu 卷王价和竞争格局                                      │
│                                                                 │
│  Step 3: ali1688-sourcing                                       │
│  → 查询 1688 拿货价和供应链                                        │
│                                                                 │
│  Step 4: temu-pricing-calculator                                │
│  → V4.1 核价计算，判定 GO/PASS                                    │
│                                                                 │
│  Step 5: ecom-product-orchestrator                              │
│  → 输出完整选品报告                                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## V4.1 核价模型

```
回款预估 = Temu 前台卷王价 × 45%
回款预估(人民币) = 回款预估(美元) × 汇率(7.2)
总成本 = 1688 起批价 + 国内履约费(¥3.50)
净利润 = 回款预估(人民币) - 总成本

【铁律】净利润必须 > ¥5.00，否则直接淘汰
```

## 兼容性

| Agent | 支持 |
|-------|------|
| Claude Code | ✅ |
| Cursor | ✅ |
| Codex | ✅ |
| Cline | ✅ |
| Windsurf | ✅ |
| 其他 Agent Skills 兼容工具 | ✅ |

## 开发者

- **作者**: zhuhongyin
- **公司**: Loctek (乐歌)
- **用途**: 跨境电商选品

## 许可证

MIT License
