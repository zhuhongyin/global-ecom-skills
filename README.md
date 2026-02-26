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

### 方式三：手动安装（推荐用于测试）

```bash
# 克隆仓库
git clone https://github.com/zhuhongyin/global-ecom-skills.git
cd global-ecom-skills

# 复制skills到项目目录
mkdir -p .claude/skills
cp -r skills/* .claude/skills/

# 验证安装
ls -la .claude/skills/
```

## 🧪 测试方法

### 测试1：验证Skills安装

```bash
# 查看已安装的skills
ls -la .claude/skills/

# 应该看到以下6个目录：
# - amazon-trend-analyzer
# - temu-competitor-analyzer
# - supply-platform-analyzer
# - sourcing-1688
# - profit-calculator
# - product-recommender
```

### 测试2：测试Profit Calculator

```bash
# 运行利润计算器
python3 .claude/skills/profit-calculator/scripts/calculator.py
```

**预期输出**：
```json
{
  "input": {
    "temu_price": 12.99,
    "price_1688": 25.0
  },
  "result": {
    "net_profit": 13.59,
    "profit_rate": 47.7,
    "verdict": "✅ GO"
  }
}
```

**判定**: 良好利润空间，推荐上架

### 测试3：测试Product Recommender

```bash
# 运行选品推荐器
python3 .claude/skills/product-recommender/scripts/recommender.py
```

**预期输出**：
```
推荐产品数: 2
平均利润: ¥11.045

产品1: 桌垫 Desk Mat
- 综合评分: 95分
- 净利润: ¥13.59
- 判定: ✅ 推荐上架

产品2: 显示器支架 Monitor Stand
- 综合评分: 75分
- 净利润: ¥8.5
- 判定: ✅ 推荐上架
```

### 测试4：在Claude Code中调用

重启Claude Code后，可以直接使用自然语言调用：

```
使用profit-calculator计算产品利润：Temu卷王价$12.99，1688拿货价¥25
```

```
使用product-recommender推荐适合上架的产品
```

```
使用amazon-trend-analyzer分析亚马逊飙升榜
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



统一验收标准：
交付验收材料-1：（为方便，人选可自己创建一个Public Repo Github，可以先不用加入乐歌企业的Github Repo，代码提交到个人的Repo，提交个人 github repo 及分支）skills 提交到 github 仓库“https://github.com/global-ecom-skills/global-ecom-skills”，自己新建分支，分支名称为“skills名称-zhonghongyin”，先别push到main分支，你自己先起一个branch名字，等该skill被测试能符合企业级实用后，再push到main分支；
交付验收材料-2：skills 做成可通过行命令安装到 claude code 的skills，一行命令安装这些skill，https://skills.sh/,类似“find_skills”这个skill可以通过“npx skills add GitHub - vercel-labs/skills: The open agent skills tool - npx skills --skill find-skills”；
交付验收材料-3：交付自己开发的作业涉及需求的完整产品的视频录屏，把skills的测试演示、完整产品的前端、后端等测试使用演示；
