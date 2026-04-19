# ai-coding-ok 实战指南

> 本文档详细拆解本项目的开发过程，展示 ai-coding-ok skill 在 Claude Code 中的每一个关键行为。
> 适合想把这套方法迁移到自己项目的开发者。

---

## 目录

1. [为什么需要 ai-coding-ok？](#1-为什么需要-ai-coding-ok)
2. [安装 ai-coding-ok（Mode A）](#2-安装-ai-coding-okmode-a)
3. [三层记忆文件详解](#3-三层记忆文件详解)
4. [开发时的 PDCA 循环（Mode B + C）](#4-开发时的-pdca-循环mode-b--c)
5. [本项目完整开发日志](#5-本项目完整开发日志)
6. [迁移到你自己的项目](#6-迁移到你自己的项目)
7. [常见问题](#7-常见问题)

---

## 1. 为什么需要 ai-coding-ok？

### 没有记忆系统时的典型问题

**场景：第一次对话**
```
你: 帮我做一个记账 App，用 SQLite，不要用 PostgreSQL
AI: 好的，我用 FastAPI + SQLite 实现 ✅
```

**场景：第二次对话（新开一个 session）**
```
你: 给我加一个统计功能
AI: 好的，我来扩展，顺便把数据库换成 PostgreSQL，性能更好 ❌
```

AI 没有记住"不要用 PostgreSQL"这个约束，因为每次对话上下文都是全新的。

### ai-coding-ok 的解法

把关键信息持久化到**项目文件**中：

```
你的约束 ──写入──▶ project-memory.md  ──每次读取──▶ AI 的工作上下文
你的决策 ──写入──▶ decisions-log.md   ──每次读取──▶ AI 不会推翻历史
上次的坑 ──写入──▶ task-history.md    ──每次读取──▶ AI 不会重蹈覆辙
```

这些文件存在你的项目 git 仓库里，跨 session 永久有效。

---

## 2. 安装 ai-coding-ok（Mode A）

### 前提条件

1. 已安装 [Claude Code](https://docs.anthropic.com/claude-code)（Claude 官方 CLI）
2. 已安装 ai-coding-ok skill（放到 `~/.claude/skills/ai-coding-ok/`）

### 安装命令

在 Claude Code 里输入：

```
install ai-coding-ok
```

Claude 会询问你一句话描述项目：

```
Claude: 一句话告诉我你想做一个什么东西？
        比如：'给自己用的记账小工具，能记录每天花了多少钱'

你: 给自己用的记账小工具，能记录每天花了多少钱
```

### Claude 自动完成的事情

基于这一句话，Claude 会自动推断并填充：

```yaml
# 推断结果示例
项目名称: 记账本
类型: 个人记账 Web 工具
技术栈:
  语言: Python 3.12        # 推断：Python 最适合快速开发小工具
  框架: FastAPI            # 推断：轻量异步，适合单用户工具
  数据库: SQLite           # 推断：零配置，个人工具无需服务器 DB
  ORM: SQLAlchemy (async)  # 推断：配合 FastAPI 的标准选择
  模板: Jinja2             # 推断：无构建步骤，极简前端
  测试: pytest             # 推断：Python 标准测试框架
  包管理: uv               # 推断：现代极速工具

设计原则: 极简实用（个人工具首选）
```

然后把这些信息写入所有配置文件，不留任何 `{{占位符}}`。

### 安装后的文件结构

```
.github/
├── copilot-instructions.md    # ← 已定制，包含你的技术栈和行为规则
├── agent/
│   ├── system-prompt.md       # ← 已定制，包含你的项目描述
│   ├── coding-standards.md    # ← 通用编码规范（Python 最佳实践）
│   ├── workflows.md           # ← 场景工作流（功能开发/修 bug/重构）
│   ├── prompt-templates.md    # ← 常用 Prompt 模板
│   └── memory/
│       ├── project-memory.md  # ← 已填入项目基本信息
│       ├── decisions-log.md   # ← 已写入 ADR-001（数据库选型）
│       └── task-history.md    # ← 已写入 TASK-001（安装记录）
AGENTS.md                      # ← 已填入架构信息（Claude 必读）
```

---

## 3. 三层记忆文件详解

### project-memory.md（长期记忆）

存储**不会经常变化**的项目事实。

**什么时候会更新：**
- 新增核心模块（新写了一个 `payment_service.py`）
- 技术栈变动（决定引入 Redis）
- 关键约束变化（之前限制 500 行/文件，现在调整为 800 行）

**实际内容示例（本项目）：**
```markdown
## 核心模块
| 模块 | 说明 | 状态 |
|------|------|------|
| src/models/expense.py | Expense ORM（含 record_type 区分收入/支出） | ✅ 已完成 |
| src/services/expense_service.py | 业务逻辑：记录、查询、月统计、看板统计 | ✅ 已完成 |

## 关键约束
1. 禁止引入 React/Vue：前端保持 Jinja2，无构建步骤
2. 禁止 PostgreSQL：坚持 SQLite，零配置
3. 无需用户认证：单用户本地工具
```

**价值**：Claude 每次任务开始都读这个文件，**永远不会**忘记这些约束。

---

### decisions-log.md（中期记忆）

存储**架构和技术决策**，ADR 格式（Architecture Decision Record）。

**什么时候会更新：**
- 选了某个技术方案（为什么用 SQLAlchemy 而不是 Tortoise ORM？）
- 推翻了某个之前的决定（从同步改成异步）
- 遇到了技术限制（Starlette 1.0 的 API 变更）

**实际内容示例（本项目）：**
```markdown
### ADR-001: 数据库选型 — SQLite vs PostgreSQL

- 日期：2026-04-19
- 状态：✅ 已采纳

#### 背景
记账本是单用户个人工具，需要选择数据库方案。

#### 决策
选择 SQLite。

#### 理由
单用户本地工具，不存在并发写场景。SQLite 零配置、无需服务器进程，
完全满足需求，且部署极简（复制文件即备份）。引入 PostgreSQL 属于过度设计。
```

**价值**：当 Claude 在未来某次对话里想"改进"数据库时，会看到这个决策和理由，**不会推翻它**。

---

### task-history.md（短期记忆）

记录**近期任务摘要**，为 AI 提供"上次做了什么"的上下文。

**什么时候会更新：**
- 每次任务完成后（必须更新）
- 特别要记录：踩过的坑、注意事项、遗留问题

**实际内容示例（本项目）：**
```markdown
### [TASK-002] 完整实现记账本系统
- 日期：2026-04-19
- 摘要：从零实现完整记账本系统，包含 FastAPI 后端、SQLite 数据库、Jinja2 前端、24 个测试。

- 注意事项：
  - Python 3.13 环境；SQLAlchemy async 需要 sqlalchemy[asyncio]（greenlet）
  - Starlette 1.0 的 TemplateResponse 新签名为 (request, name, context)
  - from __future__ import annotations 在 Pydantic 中若字段名与类型名相同会冲突
```

**价值**：第三轮对话开发看板功能时，Claude **直接知道**上次遇到了 Starlette API 变更的坑，不会再踩一遍。

---

## 4. 开发时的 PDCA 循环（Mode B + C）

每次开发任务都遵循这个循环：

```
┌─────────────────────────────────────────────────────────────┐
│                      PDCA 循环                               │
│                                                              │
│  P (Plan)          D (Do)          C (Check)   A (Act)      │
│  ─────────         ────────        ─────────   ──────────   │
│  读 AGENTS.md      写代码          运行测试     更新记忆     │
│  读 project-       写测试          验证通过     task-history │
│    memory.md       同步进行                     decisions-   │
│  读 decisions-                                    log        │
│    log.md                                       project-     │
│  读 task-                                         memory     │
│    history.md                                               │
│  ↑ 约 30 秒         ← 主要工作 →   验收门槛    ← 必须完成 → │
└─────────────────────────────────────────────────────────────┘
```

### Mode B：任务开始时（自动触发）

**触发条件**：项目里有 `.github/agent/memory/` 目录 + 用户发起开发任务

**Claude 的行为**：
1. 读 `AGENTS.md`（约 5 秒）
2. 读三个记忆文件（约 10 秒）
3. 输出约束摘要确认（约 5 秒）
4. 开始实际工作

```
Claude: [读取记忆后]
关键约束确认：
- 技术栈：FastAPI + SQLite + Jinja2 + uv
- 禁止引入：React/Vue、PostgreSQL
- 已完成：记账系统基础功能（TASK-002）
- 注意：Starlette 1.0 TemplateResponse 新签名

好，现在开始实现看板功能...
```

### Mode C：任务结束时（强制执行）

**触发条件**：一段代码工作完成，即将返回最终结果

**Claude 的行为**：
1. 更新 `task-history.md`（必须）
2. 如有架构变更 → 更新 `decisions-log.md`
3. 如有项目事实变化 → 更新 `project-memory.md`
4. 在回复中列出「记忆更新」小节

---

## 5. 本项目完整开发日志

### 第一轮：安装和初始化

**输入：**
```
install ai-coding-ok
```

**Claude 执行：**
- 复制 16 个模板文件
- 询问项目描述
- 推断并填充所有占位符（Python/FastAPI/SQLite/Jinja2/uv/ruff/pytest）
- 写入 ADR-001（数据库选型理由）
- 写入 TASK-001（安装记录）

**耗时**：约 2 分钟  
**产出**：完整的 `.github/` 配置体系，无任何 `{{占位符}}`

---

### 第二轮：完整系统开发

**输入：**
```
你把整个系统开发出来吧
```

**Claude 的 Plan 阶段（读记忆）：**
- 知道技术栈：FastAPI + SQLite + Jinja2
- 知道约束：不能引 React/Vue，不能用 PostgreSQL
- 知道项目状态：TASK-001 初始化完成，还没有实际代码

**Claude 的 Do 阶段（写代码）：**

```
src/
├── main.py           (路由 + 模板渲染)
├── config.py         (环境变量)
├── database.py       (SQLAlchemy 异步引擎)
├── models/expense.py (ORM 模型)
├── schemas/expense.py (Pydantic + 分类常量)
├── services/expense_service.py (业务逻辑)
├── api/expenses.py   (REST API)
└── templates/        (base/index/stats)

tests/
├── conftest.py       (内存数据库 fixture)
├── unit/test_expense_service.py
└── integration/test_api.py
```

**Claude 的 Check 阶段：**
```bash
$ uv run pytest
24 passed in 0.09s ✅
```

**Claude 的 Act 阶段（更新记忆）：**
```markdown
### [TASK-002] 完整实现记账本系统
- 注意事项：
  - Starlette 1.0 的 TemplateResponse 新签名 ← 这个很重要！
  - from __future__ import annotations 与 Pydantic 的冲突
```

**耗时**：约 10 分钟  
**产出**：14 个文件，24 个测试，全部通过

---

### 第三轮：新增看板功能

**输入：**
```
新增一个个人开销看板，可以查看有哪些收入，有哪些支出，都是哪些分类
```

**Claude 的 Plan 阶段（读记忆）：**
- 知道 Starlette 1.0 签名变更（TASK-002 的注意事项）→ **直接用新签名，没有踩坑**
- 知道不引入 JS 框架 → 用 Jinja2 + 纯 CSS 实现看板，没有加 React
- 知道 SQLite 约束 → 用 `server_default` 做 schema 迁移，没有换数据库

**Claude 的实现思路：**
```python
# 扩展 Expense 模型，用 server_default 保证存量数据不受影响
record_type: Mapped[str] = mapped_column(
    String(10), nullable=False, server_default="支出"
)
```

这个决策非常关键——如果没有看到"禁止换 PostgreSQL"的约束，Claude 可能会建议"换个支持 migration 的数据库"。

**Claude 的 Check 阶段：**
```bash
$ uv run pytest
35 passed in 0.15s ✅
```

**Claude 的 Act 阶段（更新记忆）：**
- 更新 `task-history.md`：TASK-003 看板开发记录
- 更新 `project-memory.md`：模块状态从"待开发"改为"已完成"

**耗时**：约 8 分钟  
**产出**：新增看板页面 + 收入支持，测试从 24 个增至 35 个

---

## 6. 迁移到你自己的项目

### Step 1：安装 ai-coding-ok skill

把 skill 文件放到 `~/.claude/skills/ai-coding-ok/`，或参考 ai-coding-ok 仓库的安装指南。

### Step 2：在你的项目里初始化

```
install ai-coding-ok
```

### Step 3：告诉 Claude 你在做什么（一句话）

```
一句话：用 Go + Gin 做一个团队内部的代码审查工具，记录每个 PR 的 review 意见
```

Claude 会自动推断 Go 技术栈并填充所有配置。

### Step 4：正常开发

之后每次开发任务，Claude 自动：
- 任务开始：读记忆，带约束开始工作
- 任务结束：更新记忆，记录决策和注意事项

### 最佳实践

**1. task-history.md 的注意事项要写详细**

```markdown
# ❌ 太简略，没有学习价值
- 注意事项：已修复 bug

# ✅ 写清楚踩了什么坑、如何解决
- 注意事项：
  - Go 1.21 的 context 包变更：context.WithTimeout 返回值必须显式 cancel
  - Gin 的 ShouldBindJSON 对空 body 不报错，需要手动检查
```

**2. decisions-log.md 要写"为什么不选"**

```markdown
# ❌ 只写了选了什么
选择 Redis 作为缓存

# ✅ 写了为什么不选其他方案
选择 Redis，而非：
- Memcached：不支持数据持久化，重启后缓存全失
- 本地内存缓存：多实例部署时不共享
```

**3. project-memory.md 的约束要具体**

```markdown
# ❌ 太模糊
不要引入不必要的依赖

# ✅ 明确列出禁止项
禁止引入：
- ORM 之外的数据库访问库（统一用 GORM）
- 任何 CSS 框架（统一用 Tailwind）
- 非标准库的日志库（统一用 slog）
```

---

## 7. 常见问题

**Q：每次对话都要 Claude 读这些文件，会很慢吗？**

A：整个 Plan 阶段约 30 秒（读 4 个文件）。与防止 AI 破坏已有功能相比，这 30 秒是值得的投入。

**Q：如果 Claude 没有自动读记忆文件怎么办？**

A：在 `AGENTS.md` 顶部有强制执行指令，Claude 读到这个文件时会自动触发 Plan 阶段。你也可以在对话开头显式说：`先读一下 AGENTS.md 和 memory 文件`。

**Q：记忆文件需要手动维护吗？**

A：Claude 负责在任务结束后（Mode C）自动更新。但建议你偶尔检查一下 `project-memory.md`，确保约束描述准确。

**Q：这套方法适合大型项目吗？**

A：完全适合。记忆文件的设计是渐进式的——项目越大，沉淀的内容越丰富，AI 的工作质量也越高。

**Q：GitHub Copilot 也能用吗？**

A：可以。Copilot 会自动加载 `.github/copilot-instructions.md`，这个文件里已经包含了所有约束和规范。记忆文件可以通过在 Copilot Chat 里粘贴内容来手动提供上下文。

---

*本文档由 ai-coding-ok Mode C 触发后人工审校，记录于 TASK-003 完成后。*
