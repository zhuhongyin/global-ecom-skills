# Global E-Commerce Skills

Your AI toolkit for selling profitable products globally — no high barriers, just real profits.

跨境电商选品智能体 Skills 集合，用于 Claude Code 等 AI 编程助手。

## What I Do

This repository helps Chinese factories and sellers find **products that sell extremely well abroad** with **zero high barriers to entry**.

No complicated requirements, no expensive setup — just simple, proven skills to grow your global business.

## 快速开始

### 方式一：一键启动（推荐）

```bash
# 克隆仓库
git clone https://github.com/zhuhongyin/global-ecom-skills.git
cd global-ecom-skills

# 添加执行权限
chmod +x start.sh

# 一键启动（自动检查环境、安装 Skills、启动服务）
./start.sh
```

启动后打开浏览器访问：http://localhost:5000

### 方式二：手动启动

```bash
# 1. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 2. 安装依赖
pip install flask flask-cors

# 3. 启动服务
python frontend/api_server.py
```

### 启动脚本选项

```bash
./start.sh                  # 正常启动
./start.sh --install-skills # 强制安装 Skills
./start.sh --skip-skills    # 跳过 Skills 检查
./start.sh --help           # 显示帮助
```

## 安装 Skills 到 Claude Code

```bash
# 一行命令安装所有 skills（推荐）
npx skills add zhuhongyin/global-ecom-skills

# 安装特定 skill
npx skills add zhuhongyin/global-ecom-skills --skill temu-pricing-calculator
npx skills add zhuhongyin/global-ecom-skills --skill amazon-movers-shakers
npx skills add zhuhongyin/global-ecom-skills --skill temu-competitor-search
npx skills add zhuhongyin/global-ecom-skills --skill ali1688-sourcing
npx skills add zhuhongyin/global-ecom-skills --skill ecom-product-orchestrator

# 列出可用的 skills
npx skills add zhuhongyin/global-ecom-skills --list

# 安装到全局（所有项目可用）
npx skills add zhuhongyin/global-ecom-skills -g

# 安装到特定 Agent
npx skills add zhuhongyin/global-ecom-skills -a claude-code
```

## Key Skills

- Winning product research for international platforms
- High-converting, low-competition product ideas
- Easy-to-use, beginner-friendly systems
- Data-driven strategies for maximum profit

## 前端演示界面

本项目提供可视化前端界面，方便测试和使用 Skills：

| 功能 | 说明 |
|------|------|
| 核价计算器 | 输入 Temu 卷王价和 1688 拿货价，计算净利润 |
| 选品流程 | 自动执行完整选品流程，获取真实数据 |
| 选品报告 | 生成 5 款推荐产品报告，支持导出 JSON |
| 历史记录 | 保存所有操作记录 |

**技术架构：**
```
前端 (HTML/JS)  →  Flask API  →  本地 Skills 脚本
    ↓                  ↓                ↓
  用户界面         REST API 服务     真实数据获取
```

**API 端点：**
| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/health` | GET | 健康检查 |
| `/api/pricing/calculate` | POST | V4.1 核价计算 |
| `/api/amazon/movers-shakers` | GET | 亚马逊飙升榜 |
| `/api/temu/competitors` | GET | Temu 竞品查询 |
| `/api/1688/sourcing` | GET | 1688 供应链 |
| `/api/workflow/run` | POST | 完整选品流程 |
| `/api/report/generate` | POST | 生成选品报告 |

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

## Target Users

Chinese manufacturers & sellers ready to **sell globally, start fast, and earn real money**.

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
