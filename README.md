# 🤖 ai-coding-ok × Claude Code 真实案例

> **用一个完整的记账本 App，演示 [ai-coding-ok](https://github.com/Mark7766/ai-coding-ok) skill 如何在 Claude Code 中实现「有记忆、不乱改」的 AI 结对编程。**

---

## 这个项目是什么？

这是一个**可运行的真实项目 + 学习案例**，双重价值：

| 维度 | 内容 |
|------|------|
| 📱 **应用本身** | 个人记账 Web App — 支出/收入记录、分类统计、月度看板 |
| 🧠 **方法论演示** | 用 ai-coding-ok skill + Claude Code 构建，全程可溯源 |

**如果你想学习**如何让 Claude Code 有记忆、遵守规范、不在多轮对话中"越改越乱"——这个项目给你一个从零开始的完整示范。

---

## 功能截图

```
首页（记录支出/收入）        月度看板                    月统计
┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│ 💰 记账本  📊 看板  │    │ 💰 记账本  🏠 首页  │    │ 💰 记账本  🏠 首页  │
├─────────────────────┤    ├─────────────────────┤    ├─────────────────────┤
│  ‹ 2026年4月19日 ›  │    │   ‹  2026年4月  ›   │    │   ‹  2026年4月  ›   │
│                     │    │ ┌──────┬──────┬────┐│    │ 本月合计            │
│  ¥200.00   ¥5000.00 │    │ │收入  │支出  │净  ││    │   ¥1,280.00         │
│  今日支出  今日收入  │    │ │5000  │1280  │+3720││    │                     │
├─────────────────────┤    │ └──────┴──────┴────┘│    │ ● 餐饮  ¥580  45%  │
│ 记一笔               │    │                     │    │ ● 购物  ¥400  31%  │
│ [支出] [收入]        │    │ 收入来源             │    │ ● 交通  ¥200  16%  │
│ 金额  分类  日期     │    │ ● 工资  5000  100%  │    │ ● 其他  ¥100   8%  │
│ 备注          [记]  │    │                     │    │                     │
├─────────────────────┤    │ 支出分类             │    │ 每日明细            │
│ 今日明细             │    │ ● 餐饮  580   45%  │    │ 4月19日   3笔  ¥200│
│ 🍜 餐饮  ¥35.00     │    │ ● 购物  400   31%  │    │ 4月15日   2笔  ¥150│
│ 💼 工资 +¥5000 收入  │    │ ● 交通  200   16%  │    └─────────────────────┘
└─────────────────────┘    └─────────────────────┘
```

**核心功能：**
- 记录每日支出和收入，支持分类（支出7类 / 收入5类）
- 月度看板：收入 vs 支出 vs 净结余，分类占比进度条
- 月统计：每日明细、按分类汇总
- 删除记录，日期导航翻页

---

## 快速运行

### 环境要求

- Python 3.12+
- [uv](https://github.com/astral-sh/uv)（包管理器，`pip install uv` 或参考官网）

### 启动步骤

```bash
# 1. 克隆项目
git clone https://github.com/Mark7766/ai-coding-ok-cc-demo.git
cd ai-coding-ok-cc-demo

# 2. 安装依赖
uv sync

# 3. 配置环境变量（可选，默认值即可）
cp .env.example .env

# 4. 启动服务
uv run uvicorn src.main:app --reload
```

打开浏览器访问 **http://localhost:8000** 即可。

### 运行测试

```bash
# 运行所有测试
uv run pytest

# 带覆盖率报告
uv run pytest --cov=src --cov-report=term-missing

# 代码检查
uv run ruff check .
uv run ruff format --check .
```

---

## ai-coding-ok 是如何工作的？

这是本项目的核心学习内容。ai-coding-ok 解决了 AI 辅助编码的最大痛点：

> **"我上次让 Claude 做了 A，这次它把 A 改掉了……"**
> **"我说过不要用 PostgreSQL，它又加进来了……"**

### 三层记忆系统

```
.github/agent/memory/
├── project-memory.md    # 🧠 长期记忆 — 项目事实、技术栈、约束（不随任务变化）
├── decisions-log.md     # 📝 中期记忆 — 架构决策日志 ADR（为什么选 SQLite？）
└── task-history.md      # 📜 短期记忆 — 近期任务摘要（上次做了什么？）
```

**每次对话开始前**，Claude 自动读取这三个文件，带着上下文开始工作——就像一个有记忆的同事，不需要你每次重新解释项目背景。

### PDCA 工作流

```
Plan  ──▶  Do  ──▶  Check  ──▶  Act
读记忆      写代码    跑测试      更新记忆
加载上下文  写测试    验证通过    记录决策
```

**Plan**：读取 `AGENTS.md` + 三个记忆文件，理解约束  
**Do**：编写代码和测试（同步进行）  
**Check**：运行测试，确认无回归  
**Act**：更新 `task-history.md`，有架构变更则更新 `decisions-log.md`

### 实际对话示例

这个项目完整经历了三次对话，下面是真实的 prompt 和 Claude 的行为：

#### 第一轮：安装 ai-coding-ok

```
用户: install ai-coding-ok

Claude: [触发 Mode A — 安装流程]
→ 复制模板文件到项目
→ 询问：一句话说你在做什么？
用户: 给自己用的记账小工具，能记录每天花了多少钱
→ 自动推断技术栈：FastAPI + SQLite + Jinja2 + uv + ruff
→ 填充所有占位符，生成定制化配置
→ 写入 TASK-001 到 task-history.md
```

#### 第二轮：开发完整系统

```
用户: 你把整个系统开发出来吧

Claude: [触发 Mode B — 读记忆]
→ 读 AGENTS.md：了解架构（FastAPI + SQLite + Jinja2）
→ 读 project-memory.md：确认约束（禁 React/Vue、禁 PostgreSQL）
→ 读 decisions-log.md：ADR-001 SQLite 选型理由
→ 读 task-history.md：TASK-001 初始化记录

[然后开始开发，不违反任何约束]
→ 实现 14 个文件，24 个测试，全部通过

[触发 Mode C — 更新记忆]
→ 写入 TASK-002 到 task-history.md（含注意事项）
```

#### 第三轮：新增看板功能

```
用户: 新增一个个人开销看板，可以查看有哪些收入，有哪些支出，都是哪些分类

Claude: [触发 Mode B — 读记忆]
→ 读 task-history.md：知道 TASK-002 已完成了什么
→ 知道约束：不引入 React/Vue，不用 PostgreSQL
→ 知道 Starlette 1.0 的 TemplateResponse 新签名（上次踩过坑）

[正确地扩展功能，不破坏已有代码]
→ 新增 record_type 字段（server_default，存量数据不受影响）
→ 新增看板页面、收入分类
→ 35 个测试，全部通过

[触发 Mode C — 更新记忆]
→ 更新 task-history.md 和 project-memory.md
```

**关键结论：** 第三轮对话，Claude 没有忘记第二轮里踩过的坑，没有违反约束，直接复用了已有架构——这就是 ai-coding-ok 三层记忆的价值。

---

## 项目结构

```
ai-coding-ok-cc-demo/
│
├── src/                          # 应用源代码
│   ├── main.py                   # FastAPI 入口，路由定义
│   ├── config.py                 # 环境变量配置
│   ├── database.py               # SQLAlchemy 异步引擎
│   ├── models/
│   │   └── expense.py            # Expense ORM 模型
│   ├── schemas/
│   │   └── expense.py            # Pydantic schemas + 分类常量
│   ├── services/
│   │   └── expense_service.py    # 业务逻辑层
│   ├── api/
│   │   └── expenses.py           # REST API 路由
│   └── templates/
│       ├── base.html             # 基础布局 + 全局样式
│       ├── index.html            # 首页（记录 + 今日明细）
│       ├── stats.html            # 月统计页
│       └── dashboard.html        # 月度看板页
│
├── tests/
│   ├── conftest.py               # pytest fixtures（内存数据库）
│   ├── unit/
│   │   └── test_expense_service.py  # Service 层单元测试
│   └── integration/
│       └── test_api.py           # HTTP 集成测试
│
├── .github/
│   ├── copilot-instructions.md   # Copilot 全局行为指令
│   ├── agent/
│   │   ├── system-prompt.md      # AI Agent 人格 + PDCA 流程
│   │   ├── coding-standards.md   # 编码规范
│   │   ├── workflows.md          # 场景工作流
│   │   ├── prompt-templates.md   # Prompt 模板库
│   │   └── memory/               # 🧠 三层记忆系统
│   │       ├── project-memory.md
│   │       ├── decisions-log.md
│   │       └── task-history.md
│   └── workflows/
│       └── ci.yml                # GitHub Actions CI
│
├── AGENTS.md                     # 架构速查（AI 每次必读）
├── pyproject.toml                # 项目配置
├── .env.example                  # 环境变量模板
└── README.md                     # 本文件
```

---

## 技术栈

| 层面 | 选型 | 说明 |
|------|------|------|
| 语言 | Python 3.12 | 语法简洁，生态丰富 |
| Web 框架 | FastAPI | 轻量、异步、自带文档 |
| 数据库 | SQLite + aiosqlite | 零配置，文件即数据库 |
| ORM | SQLAlchemy 2 (async) | 成熟稳定，原生异步支持 |
| 模板 | Jinja2 | 服务端渲染，无需构建步骤 |
| 测试 | pytest + pytest-asyncio | Python 标准测试方案 |
| 代码质量 | ruff (lint + format) | 极速，统一工具链 |
| 包管理 | uv | 现代、极速，替代 pip/poetry |

---

## 学习 ai-coding-ok

想把这套方法用到自己的项目？

```
1. 安装 ai-coding-ok skill 到 Claude Code
2. 在你的项目里说：install ai-coding-ok
3. 告诉 Claude 一句话描述你的项目
4. 开始正常对话开发，记忆系统自动运转
```

详细教程见：[docs/ai-coding-ok-guide.md](docs/ai-coding-ok-guide.md)

---

## 开发规范

本项目由 ai-coding-ok 管理。修改前请阅读：

- [`AGENTS.md`](AGENTS.md) — 架构速查和约束
- [`.github/agent/coding-standards.md`](.github/agent/coding-standards.md) — 编码规范
- [`.github/agent/memory/`](.github/agent/memory/) — 三层记忆（了解历史决策）

---

## License

MIT
