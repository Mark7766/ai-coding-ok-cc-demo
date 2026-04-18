# 📝 Claude Code × Superpowers 演示仓库 — 技术决策日志 (ADR)

> **用途**：记录项目中每个重要技术决策，使决策可追溯、可理解。
> 格式参考 [Architecture Decision Records](https://adr.github.io/)。
> AI Agent 在做技术方案选择时，必须先查阅本文件，避免重复踩坑。

---

## ADR 记录模板

```markdown
### ADR-{编号}: {标题}

- **日期**：YYYY-MM-DD
- **状态**：✅ 已采纳 / ❌ 已废弃 / 🔄 已替代
- **决策者**：{人员 / Agent}

#### 背景
为什么需要做这个决策？遇到了什么问题？

#### 方案对比

| 方案 | 优点 | 缺点 |
|------|------|------|
| 方案 A | ... | ... |
| 方案 B | ... | ... |

#### 决策
选择了哪个方案？

#### 理由
为什么选这个方案？

#### 影响
这个决策影响了哪些模块？后续需要注意什么？
```

---

## 决策记录

### ADR-001: 项目框架初始化

- **日期**：2026-04-18
- **状态**：✅ 已采纳
- **决策者**：Mark（项目所有者）

#### 背景
需要建立一套 AI 辅助开发的方法论框架，让 AI 能够像资深工程师一样工作，
同时解决 AI 跨会话失忆导致反复重复说明背景的问题。

#### 方案对比

| 方案 | 优点 | 缺点 |
|------|------|------|
| 纯 superpowers | 工程能力强，TDD/规划/调试全覆盖 | 无跨会话记忆，每次都要重新介绍项目背景 |
| 纯 ai-coding-ok | 记忆系统完整，规范清晰 | 缺乏 superpowers 的 TDD 和规划技能 |
| superpowers + ai-coding-ok 融合 | 工程能力 + 记忆系统双全 | 需要设计融合方案 |

#### 决策
采用 **superpowers 5.0.7 + ai-coding-ok 融合方案**。

#### 理由
- superpowers 提供 brainstorming→planning→TDD→verification 的完整开发工作流
- ai-coding-ok 提供三层记忆系统（长期/中期/短期），解决跨会话失忆问题
- 两者互补，覆盖「工程能力」和「项目记忆」两个核心痛点

#### 影响
- CLAUDE.md 作为融合入口，统一两套框架的优先级
- 每次任务结束必须更新记忆文件（task-history.md）
- 设计文档存入 docs/superpowers/specs/，计划存入 docs/superpowers/plans/

---

### ADR-002: 演示技术栈选型

- **日期**：2026-04-18
- **状态**：✅ 已采纳
- **决策者**：Mark + Claude Code Agent

#### 背景
演示仓库需要选择一套技术栈，既能展示 TDD 最佳实践，又要足够简单让知识星球成员快速上手。

#### 方案对比

| 方案 | 优点 | 缺点 |
|------|------|------|
| Python + FastAPI + SQLite | 轻量、零配置、自带 OpenAPI 文档 | 不适合高并发生产环境 |
| Python + Django + PostgreSQL | 功能完整、生态丰富 | 配置复杂，不适合演示 |
| Node.js + Express + SQLite | 前端友好 | 异步模型较复杂，不适合展示 TDD |

#### 决策
选择 **Python 3.12 + FastAPI + SQLite + pytest**。

#### 理由
- SQLite 零配置，`git clone` 后直接运行，降低演示门槛
- FastAPI 语法简洁，自动生成 OpenAPI 文档，直观展示 API 设计
- pytest 生态成熟，与 TDD 工作流配合最佳
- Python 是知识星球成员最熟悉的语言

#### 影响
- 所有示例代码使用 Python 3.11 语法（宿主机实际版本）
- 测试使用 `pytest` + `pytest-cov`，覆盖率目标 ≥ 80%
- 禁止引入 Django ORM、Celery 等重量级依赖

---

### ADR-003: SQLite 测试隔离方案

- **日期**：2026-04-18
- **状态**：✅ 已采纳
- **决策者**：Claude Code Agent

#### 背景
需要让 API 集成测试使用独立的 in-memory 数据库，避免测试污染生产数据，
同时 FastAPI 的 sync 路由会在线程池中运行，导致 SQLite 连接跨线程报错。

#### 方案对比

| 方案 | 优点 | 缺点 |
|------|------|------|
| 每个测试创建临时文件 DB | 真实文件行为 | 慢、需清理 |
| `:memory:` + `dependency_overrides` | 快、完全隔离 | 需处理跨线程问题 |
| 改用 async 路由 | 根本解决线程问题 | 增加复杂度，不适合入门演示 |

#### 决策
使用 **`:memory:` SQLite + `app.dependency_overrides` + `check_same_thread=False`**。

#### 理由
- in-memory DB 每个 fixture 独立，测试完全隔离，速度最快
- `check_same_thread=False` 允许同一连接在不同线程使用，适合演示场景
- `dependency_overrides` 是 FastAPI 官方推荐的测试注入方式，值得在演示中展示

#### 影响
- `src/database.py` 的 `create_connection()` 统一加 `check_same_thread=False`
- `tests/conftest.py` 中 `db` fixture 使用 `sqlite3.connect(":memory:", check_same_thread=False)`
- 生产环境如需高并发，应改用连接池方案（非本演示范围）
