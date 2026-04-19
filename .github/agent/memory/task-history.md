# 📜 记账本 — 任务历史

> **用途**：记录近期任务摘要，为 AI Agent 提供短期上下文记忆。
> 保留最近 30 条任务记录，超出后归档。

---

## 记录格式

```markdown
### [TASK-{编号}] {任务标题}
- **日期**：YYYY-MM-DD
- **类型**：feat / fix / refactor / docs / chore
- **摘要**：一句话说明做了什么
- **变更文件**：列出核心变更文件
- **关联 Issue**：#xxx（如有）
- **注意事项**：后续需要注意的事项（如有）
```

---

## 任务记录

### [TASK-004] 创建项目文档体系
- **日期**：2026-04-19
- **类型**：docs
- **摘要**：创建 README.md（含功能展示、快速运行、ai-coding-ok 工作原理、对话示例）、docs/ai-coding-ok-guide.md（完整实战指南，面向知识星球学员）、docs/development.md（开发参考手册），定位为 ai-coding-ok × Claude Code 的真实案例学习材料。
- **变更文件**：README.md（新增）, docs/ai-coding-ok-guide.md（新增）, docs/development.md（新增）
- **注意事项**：README 以中文为主，面向中文开发者社区；功能截图用 ASCII art 替代，无需实际截图

### [TASK-003] 新增个人开销看板（Dashboard）
- **日期**：2026-04-19
- **类型**：feat
- **摘要**：新增 `/dashboard` 看板页面，支持查看月度收入/支出/净结余及分类明细；同时扩展 `Expense` 模型，通过 `record_type` 字段区分支出和收入，首页表单新增支出/收入类型切换。
- **变更文件**：src/models/expense.py, src/schemas/expense.py, src/services/expense_service.py, src/main.py, src/templates/base.html, src/templates/index.html, src/templates/stats.html, src/templates/dashboard.html（新增）, tests/unit/test_expense_service.py, tests/integration/test_api.py
- **注意事项**：
  - `record_type` 使用 `server_default="支出"`，存量数据无需迁移
  - `get_daily_total` 和 `get_monthly_stats` 已更新为仅统计"支出"记录，保持 stats 页面语义不变
  - 收入分类：工资、奖金、副业、投资、其他收入
  - 35 个测试全部通过

### [TASK-002] 完整实现记账本系统
- **日期**：2026-04-19
- **类型**：feat
- **摘要**：从零实现完整记账本系统，包含 FastAPI 后端、SQLite 数据库、Jinja2 前端、24 个测试，全部通过。
- **变更文件**：pyproject.toml, src/main.py, src/config.py, src/database.py, src/models/expense.py, src/schemas/expense.py, src/services/expense_service.py, src/api/expenses.py, src/templates/base.html, src/templates/index.html, src/templates/stats.html, tests/conftest.py, tests/unit/test_expense_service.py, tests/integration/test_api.py
- **注意事项**：
  - Python 3.13 环境；SQLAlchemy async 需要 `sqlalchemy[asyncio]`（greenlet）。
  - Starlette 1.0 的 `TemplateResponse` 新签名为 `(request, name, context)`，不再需要在 context 中传 `request`。
  - `from __future__ import annotations` 在 Pydantic 模型中若字段名与类型名相同会冲突，用 `from datetime import date as Date` 解决。
  - `date` 参数名在 FastAPI 路由中需加 `# type: ignore[assignment]` 避免 mypy 告警。

### [TASK-001] 安装 ai-coding-ok 并完成项目初始化
- **日期**：2026-04-19
- **类型**：chore
- **摘要**：通过 ai-coding-ok skill 安装三层记忆系统和编码规范；根据用户需求（"给自己用的记账小工具，能记录每天花了多少钱"）自动推断并填充所有配置占位符。
- **变更文件**：AGENTS.md, .github/copilot-instructions.md, .github/project-metadata.yml, .github/agent/system-prompt.md, .github/agent/coding-standards.md, .github/agent/workflows.md, .github/agent/prompt-templates.md, .github/agent/memory/project-memory.md, .github/agent/memory/decisions-log.md, .github/workflows/ci.yml
- **注意事项**：首次运行。技术栈已推断为 FastAPI + SQLite + Jinja2 + uv + ruff。如后续架构调整，请同步更新 project-memory.md 和 decisions-log.md。
