# AGENTS.md — Claude Code × Superpowers 演示仓库

> AI Agent 在每次任务开始时首先读取本文件。
> 这是项目的「作战地图」，告诉 Agent 系统在哪里、怎么运转、怎么操作。

---

## 项目概述

**Claude Code × Superpowers 演示仓库** 是一个 **教学演示仓库 — 展示 superpowers + ai-coding-ok 在 Claude Code 中的最佳实践**。
面向知识星球成员，解决 AI 跨会话失忆 + 缺乏工程纪律两大痛点，演示如何让 Claude Code 像资深工程师一样持续稳定地工作。

**设计原则：** 极简实用，步骤可复制，便于成员理解并迁移到自己的项目

---

## 系统架构

```
  演示用户（知识星球成员）
         │
         ▼
  FastAPI 服务 (src/main.py)
         │
  ┌──────┴──────────────────┐
  │    业务逻辑层            │
  │    src/services/        │
  └──────┬──────────────────┘
         │
  ┌──────┴──────────────────┐
  │    数据存储层            │
  │    SQLite (demo.db)     │
  └─────────────────────────┘
```

### 核心模块说明

| 模块/目录 | 职责 | 状态 |
|---------|------|------|
| `src/main.py` | FastAPI 应用入口 | ⬜ 待开发 |
| `src/models/` | 数据模型定义 | ⬜ 待开发 |
| `src/services/` | 业务逻辑层 | ⬜ 待开发 |
| `src/api/` | API 路由层 | ⬜ 待开发 |
| `tests/` | 自动化测试 | ⬜ 待开发 |

---

## 常用命令

```bash
# 安装依赖
pip install -e ".[dev]"

# 启动开发服务
uvicorn src.main:app --reload

# 运行测试
pytest -v

# 查看测试覆盖率
pytest --cov=src --cov-report=term-missing

# 代码检查
ruff check src/ tests/

# 代码格式化
ruff format src/ tests/

# 数据库迁移（如适用）
# SQLite 演示项目无需迁移，直接建表
```

---

## 代码约定

- **类型注解**：所有函数必须有完整类型注解，文件开头加 `from __future__ import annotations`
- **异步优先**：API 层使用 `async def`，IO 操作使用异步
- **日志规范**：使用 `logging.getLogger(__name__)`，禁止 `print()`
- **环境变量**：通过 `.env` 文件管理，禁止硬编码敏感信息
- **代码限制**：单函数 ≤ 50 行，单文件 ≤ 500 行，行宽 ≤ 120 字符

---

## 测试模式

```python
# 测试命名格式
def test_<被测方法>_<场景>_<期望结果>():
    ...

# AAA 模式（必须遵守）
def test_example():
    # Arrange — 准备数据
    ...
    # Act — 执行操作
    ...
    # Assert — 验证结果
    ...

# 时间敏感测试
from freezegun import freeze_time

@freeze_time("2026-01-05 10:00:00")
def test_time_sensitive():
    ...
```

---

## 重要约束

- **禁止引入的依赖**：Django ORM、Celery 等重量级框架，演示项目保持轻量
- **数据库迁移策略**：SQLite 演示项目直接 CREATE TABLE，无需 alembic
- **敏感数据处理**：所有凭据通过环境变量，绝不硬编码
- **代码限制**：行宽 120 字符，单函数 ≤ 50 行，单文件 ≤ 500 行
- **测试覆盖率目标**：核心逻辑 ≥ 80%

---

## 关键文件索引

| 文件 | 用途 |
|------|------|
| `CLAUDE.md` | Claude Code 行为指令（本机器的最高指令） |
| `AGENTS.md` | 本文件，项目地图 |
| `.github/agent/memory/project-memory.md` | 长期记忆：架构、约束、已知问题 |
| `.github/agent/memory/decisions-log.md` | 中期记忆：技术决策日志 |
| `.github/agent/memory/task-history.md` | 短期记忆：近 30 条任务记录 |
| `.github/agent/coding-standards.md` | 编码规范 |
| `.github/copilot-instructions.md` | Copilot 全局行为指令 |
| `docs/superpowers/specs/` | 功能设计文档（brainstorming 输出） |
| `docs/superpowers/plans/` | 实施计划文档（writing-plans 输出） |
