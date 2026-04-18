# AGENTS.md — {{项目名称}}

> AI Agent 在每次任务开始时首先读取本文件。
> 这是项目的「作战地图」，告诉 Agent 系统在哪里、怎么运转、怎么操作。

---

## 项目概述

**{{项目名称}}** 是一个 **{{项目类型简述}}**。
{{一句话描述：面向什么用户，解决什么问题，核心价值是什么}}。

**设计原则：** {{极简实用 / 稳定可靠 / 高性能 / 其他}}

---

## 系统架构

```
{{在此绘制系统架构 ASCII 图，例如：}}

  用户请求
     │
     ▼
  Web 服务器 ({{框架}})
     │
  ┌──┴──────────────┐
  │  业务逻辑层      │
  │  services/      │
  └──┬──────────────┘
     │
  ┌──┴──────────────┐
  │  数据存储层      │
  │  {{数据库}}     │
  └─────────────────┘
```

### 核心模块说明

| 模块/目录 | 职责 | 状态 |
|---------|------|------|
| `{{入口文件}}` | {{说明}} | ✅ 完成 |
| `src/models/` | 数据模型定义 | ⬜ 待开发 |
| `src/services/` | 业务逻辑层 | ⬜ 待开发 |
| `src/api/` | API 路由层 | ⬜ 待开发 |
| `tests/` | 自动化测试 | ⬜ 待开发 |

---

## 常用命令

```bash
# 安装依赖
{{安装命令，例如：pip install -e ".[dev]" 或 npm install}}

# 启动开发服务
{{启动命令，例如：uvicorn src.main:app --reload}}

# 运行测试
{{测试命令，例如：pytest -v}}

# 查看测试覆盖率
{{覆盖率命令，例如：pytest --cov=src --cov-report=term-missing}}

# 代码检查
{{lint 命令，例如：ruff check src/ tests/}}

# 代码格式化
{{format 命令，例如：ruff format src/ tests/}}

# 数据库迁移（如适用）
{{迁移命令，例如：alembic upgrade head}}
```

---

## 代码约定

- **{{约定1}}**：例如：所有文件开头必须有 `from __future__ import annotations`
- **{{约定2}}**：例如：数据库操作使用异步 session，API 使用 `async def`
- **{{约定3}}**：例如：日志使用 `logging.getLogger(__name__)`，禁止 `print()`
- **{{约定4}}**：例如：环境变量通过 `.env` 文件管理，禁止硬编码敏感信息
- **{{约定5}}**：例如：单函数不超过 50 行，单文件不超过 500 行

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

- **禁止引入的依赖**：{{列出不允许的重量级依赖}}
- **数据库迁移策略**：{{说明迁移方式}}
- **敏感数据处理**：所有凭据通过环境变量，绝不硬编码
- **代码限制**：行宽 {{N}} 字符，单函数 ≤ {{N}} 行，单文件 ≤ {{N}} 行
- **测试覆盖率目标**：核心逻辑 ≥ {{N}}%

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
