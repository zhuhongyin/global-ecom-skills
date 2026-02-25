# Global E-Commerce Skills

跨境电商选品智能体Skills集合，为Claude Code提供专业的跨境电商选品能力。

## 📦 包含的Skills

| Skill | 描述 |
|-------|------|
| `amazon-trend-analyzer` | 亚马逊飙升榜分析，识别热销趋势产品 |
| `temu-competitor-analyzer` | Temu竞品分析，评估市场竞争程度 |
| `supply-platform-analyzer` | 4Supply平台分析，了解B2B定价 |
| `sourcing-1688` | 1688货源查找，获取工厂批发价格 |
| `profit-calculator` | V4.1利润计算，判断产品盈利能力 |
| `product-recommender` | 选品推荐整合，生成最终选品报告 |

## 🚀 安装方式

### 方式一：NPM安装（推荐）

```bash
npm install global-ecom-skills
npx global-ecom-skills install
```

### 方式二：直接安装

```bash
npx skills add global-ecom-skills/global-ecom-skills
```

### 方式三：手动安装

```bash
git clone https://github.com/global-ecom-skills/global-ecom-skills.git
cd global-ecom-skills
node scripts/install.js
```

## 📖 使用方法

安装后重启Claude Code，然后可以直接使用：

```
帮我分析亚马逊飙升榜，找出适合搬到Temu的产品
```

```
分析Temu上"desk mat"的竞争情况
```

```
帮我在1688找"桌垫"的货源
```

```
计算产品利润：Temu卷王价$12.99，1688拿货价¥25
```

```
推荐5款适合从亚马逊搬到Temu的产品
```

## 💰 V4.1核价模型

```
回款预估 = Temu卷王价 × 45%
收入(人民币) = 回款预估 × 7.2
总成本 = 1688拿货价 + ¥3.50
净利润 = 收入(人民币) - 总成本

【铁律】净利润必须 > ¥5.00
```

## 📁 目录结构

```
global-ecom-skills/
├── skills/
│   ├── amazon-trend-analyzer/
│   │   ├── SKILL.md
│   │   └── scripts/
│   ├── temu-competitor-analyzer/
│   ├── supply-platform-analyzer/
│   ├── sourcing-1688/
│   ├── profit-calculator/
│   └── product-recommender/
├── scripts/
│   └── install.js
├── package.json
└── README.md
```

## 🔧 技术栈

- Agent Skills标准（SKILL.md格式）
- Python 3.x（辅助脚本）
- Node.js（安装脚本）

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！
