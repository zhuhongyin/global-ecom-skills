---
name: temu-ecom-skills-plan
overview: 基于亚马逊飙升榜与 Temu/4supply 模式，拆解需求并规划一组可被 Claude Code 自动调用的选品与核价相关 skills，同时满足题目中对调研、协议规范、交付形式的要求。
todos:
  - id: requirements-breakdown
    content: 从 requirement.md 进一步细化并锁定最终的小需求列表（N1–N13 可在实现前微调）
    status: pending
  - id: skills-research
    content: 在官方与社区渠道针对每个小需求系统性检索可复用的现有 skills，并形成评估表
    status: pending
  - id: skills-design
    content: 为需要自研的小需求设计具体的 Claude skill 接口（名称、输入输出、错误模型）
    status: pending
  - id: skills-implementation
    content: 按照 Claude Code 官方标准实现并本地测试各个自研 skills
    status: pending
  - id: orchestrator-flow
    content: 实现 orchestrator skill 串联数据抓取、策略分析与 V4.1 核价逻辑，输出 5 个完整推荐
    status: pending
  - id: repo-branch-setup
    content: 在指定 GitHub 仓库下创建符合规范的分支和目录结构，提交全部 skills 相关代码
    status: pending
  - id: install-command
    content: 实现并验证一行命令安装这些 skills 的脚本或配置
    status: pending
  - id: testing-and-demo
    content: 准备测试用例与 Demo 场景，并完成完整产品与 skills 的视频录屏
    status: pending
isProject: false
---

# Temu/4supply 选品智能体 skills 实施计划

## 一、背景与目标
- **背景**：根据 `[requirement.md](/Users/camel/Documents/GitHub/poc2026/lgskill3/requirement.md)` 中的描述，需要为 loctek 搭建一套围绕亚马逊飙升榜选品、Temu 与 4supply 定价及 1688 采购核价的智能选品 agent（通过一组 Claude skills 组合实现）。
- **总体目标**：
  - 将“大选品智能体”拆成若干 **独立、小粒度的 Claude skill**，每个 skill 聚焦一个清晰子能力。
  - 先系统性调研现有公开 skills（官方与社区渠道），能复用则优先复用，仅在缺口处自研。
  - 所有自研 skills 符合 Claude Code 官方 skill 标准，可被自动调用，并支持一行命令安装。
  - 交付包含：skills 源码 + GitHub 分支 + 安装命令 + 演示录屏。

## 二、需求拆解为具体小需求（对应潜在独立 skills）

### 2.1 数据获取类小需求
- **N1：亚马逊飙升榜数据抓取/查询 skill**
  - 输入：类目/关键词、区域站点、时间窗口。
  - 输出：近期飙升商品列表（标题、ASIN、价格、排名/销量趋势等）。
- **N2：Temu 竞品与“卷王价”查询 skill**
  - 输入：关键词/品名、类目。
  - 输出：Temu 同类产品列表、最低价（卷王价）、主要卖点摘要。
- **N3：4supply 平台商品与机会位洞察 skill**
  - 输入：关键词/品类。
  - 输出：当前在 4supply 是否有对应商品、价格区间、是否“卖爆”或仍有空间的简单判断信号。
- **N4：1688 工厂与拿货价查询 skill**
  - 输入：产品关键词/特征（材质、用途）。
  - 输出：主流工厂、起批价区间、典型运费/MOQ 情况，用于后续核价。

### 2.2 选品与差异化策略分析类小需求
- **N5：“非红海标品”识别与趋势分析 skill**
  - 基于 N1/N2 数据，识别不是纯红海标品、具备真实需求与增长势头的细分类目。
- **N6：选品差异化策略判定 skill**
  - 根据品类与竞品特征，判定更适合：
    - 组合拳（Bundle）、
    - 视觉欺诈（Premium 设计/材质）、
    - 极致轻小（Lightweight）。
  - 输出具体建议（例如建议组合哪些 SKU 做套装、可以升级哪些材质/设计点）。
- **N7：安全合规与资质门槛识别 skill**
  - 为候选产品给出是否涉及高门槛资质（如医疗/儿童产品）、需要的认证（CE/FCC/FDA 等）和风险提示。

### 2.3 V4.1 生存模型与核价类小需求
- **N8：V4.1 倒推核价计算 skill**
  - 输入：Temu 卷王价、1688 起批价、固定国内履约费（3.5 元）。
  - 按题目公式：
    - 回款预估 = Temu 卷王价 × 45%，再换算成人民币。
    - 总成本 = 1688 起批价 + 3.5。
    - 净利润 = (回款预估 × 7.2) - 总成本。
  - 输出：详细计算过程 + 净利值 + 是否满足净利 > 5 元的铁律（✅GO / ❌PASS）。
- **N9：利润敏感性分析与调价建议 skill（可选）**
  - 在基础核价之上，分析不同前台定价下的净利变化，给运营侧调价参考。

### 2.4 前端营销/运营话术生成类小需求
- **N10：前端营销逻辑生成 skill**
  - 严格按需求中的结构输出：
    - 亚马逊热度说明、适用场景、节日/趋势因素。
    - 蓝海竞争与 Temu 低价货差异点。
    - 安全合规要点梳理（可与 N7 协同）。
    - 给采购员的“义乌/工厂找货指令”话术（材质、功能、避坑点）。
- **N11：后端生存逻辑与核价结果说明 skill**
  - 结构化生成：Temu 卷王价、收入预估、成本拆解、净利、结论（GO/PASS），便于人快速审核。

### 2.5 Orchestrator 与工作流类小需求
- **N12：候选产品自动筛选与排序 orchestrator skill**
  - 串联 N1–N8/N10/N11 等基础 skills：
    - Step1：从亚马逊飙升榜获取候选池；
    - Step2：过滤纯红海、资质高门槛产品；
    - Step3：查询 Temu 与 4supply 竞品现状与卷王价；
    - Step4：调用 V4.1 生存模型核价，过滤不达标产品；
    - Step5：选择 5 个综合得分最高的产品并生成完整两部分输出（前端营销逻辑 + 后端生存逻辑）。
- **N13：人工校正/Review 辅助 skill（可选）**
  - 帮助 reviewer 快速浏览每个候选产品的关键指标与风险点，做最终上线决策。

## 三、现有 skills 调研与复用策略

### 3.1 渠道划分与搜索策略
- **官方与社区渠道**：
  - `https://github.com/anthropics/skills`
  - `https://skillsmp.com/`
  - `https://skills.sh/`
  - `https://skills.302.ai/zh`
  - `https://github.com/iOfficeAI/AionUi/tree/main`
- **调研方法**：
  - 针对每个小需求 N1–N13，列出对应的 **关键词**（如 "amazon", "pricing", "profit", "temu", "1688", "web-scraper" 等），逐一在上述渠道检索。
  - 记录：技能名称、功能简介、输入输出、维护活跃度、协议/权限需求。

### 3.2 复用优先级与自研触发条件
- **复用优先**：
  - 若某个现有 skill 在功能上能 70% 以上满足对应小需求且可扩展，通过 prompt/组合方式即可补齐，则优先直接复用。
- **自研条件**：
  - 无相关技能，或已有技能：
    - 不支持目标站点（如 Temu、4supply、1688）。
    - 接口不稳定或无法满足企业级使用要求（限流、鉴权、返回结构等）。
  - 此时设计并实现自研 skill，接口尽量贴合 Claude 官方规范，方便未来开放。

### 3.3 调研输出物
- **《skills 适配与复用评估表》**：
  - 行：N1–N13 小需求；
  - 列：是否有现成 skill、使用的具体 skill 名、复用方式（直接 / 组合 / 二次封装）、需自研项。

## 四、Claude Code skill 设计规范与实现计划

### 4.1 统一的 skill 设计规范
- **输入输出约定**：
  - 输入参数全部显式定义（避免依赖对话上下文），包含站点、类目、价格区间等关键参数。
  - 输出采用结构化 JSON，对接 orchestrator 与前端展示更方便。
- **错误处理与重试策略**：
  - 明确区分：网络错误、第三方接口错误、业务校验未通过（如未达到净利红线）。
- **安全与合规**：
  - 不直接暴露敏感凭证，统一通过环境变量或配置文件读入。

### 4.2 开发顺序建议
- **优先开发/集成**：
  - N1（亚马逊飙升榜） → N2/N4（Temu/1688） → N8（核价） → N12（orchestrator）。
- **并行可行部分**：
  - N7（合规识别）、N10/N11（文案/说明生成）可以在数据流基本打通后并行补充。

## 五、仓库结构与 GitHub 交付规划

### 5.1 仓库与分支策略
- **目标仓库**：`https://github.com/global-ecom-skills/global-ecom-skills`。
- **分支命名**：
  - 按要求：`<skills名称>-<候选人姓名拼音全称>`，例如：`temu-selection-suite-zhangsan`。
- **建议目录结构**（示意）：
  - `skills/`：按小需求或主题分子目录（如 `amazon/`, `temu/`, `pricing/`）。
  - `scripts/`：一键安装脚本、辅助工具。
  - `examples/`：示例 prompt 与调用脚本。
  - `docs/`：架构说明、使用说明、录屏脚本大纲。

### 5.2 与 Claude Code 的集成文件
- 提供：
  - 统一的 `skills.json` 或官方要求的 manifest/config 文件，声明每个 skill 的：名称、描述、入口命令、参数定义。
  - 针对常见编辑器或运行环境的简单集成说明。

## 六、一键安装与分发方案

### 6.1 一行命令安装设计
- 参考 `skills.sh` 的模式：
  - 设计类似：`npx skills add GitHub - global-ecom-skills/temu-selection-suite` 或包装脚本。
- 输出：
  - 清晰的 README 片段说明如何使用这一行命令完成安装（包括 Node 版本要求、权限提示等）。

### 6.2 打包与版本管理
- 约定每个 skill 的版本号策略（如 `0.1.0` 起步）。
- 若使用 npm/pypi 等生态，可考虑发布轻量 SDK 或 CLI（可选）。

## 七、测试、验证与 Demo 录屏

### 7.1 测试策略
- **单 skill 测试**：
  - 针对 N1–N13，每个 skill 至少准备 2–3 个典型输入案例和期望输出结构。
- **工作流测试**：
  - 从“给出选品请求”到“产出 5 个完整推荐”的端到端调用；
  - 覆盖利润达标与不达标两类样例，验证 ❌ PASS 时不会误推荐。

### 7.2 演示录屏脚本
- 录屏内容建议包括：
  1. 在本地或云端环境中安装 skills（展示一行命令）。
  2. 在 Claude Code 中调用 orchestrator skill，完成一次真实选品流程演示。
  3. 打开对应 GitHub 分支，简单说明目录结构与关键文件。
  4. 展示如何单独调用某个基础 skill（如核价或 Temu 卷王价查询）。

## 八、文档与交付物清单

- **文档类**：
  - 需求拆解与小需求–skill 对应关系文档。
  - skills 适配与复用评估表。
  - 使用说明（安装、配置、调用示例）。
- **代码类**：
  - 所有自研 skills 源码与配置；
  - 一键安装脚本/命令；
  - 示例 prompts 与测试脚本。
- **展示类**：
  - 完整产品与 skills 流程演示录屏文件；
  - 可选：关键界面截图或流程图，便于评审快速理解。
