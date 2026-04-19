# AGENTS.md — 记账本

## 项目概述

记账本 是一个 **个人记账小工具，供单用户记录和查看每日消费明细**。供个人用户记录每日消费，支持分类与历史查询。

## 系统架构与数据流

```
用户浏览器 ──▶ FastAPI Web 服务器 ──▶ SQLite 数据库（本地文件）
             (Jinja2 模板渲染)
```

- **`src/main.py`** — FastAPI 应用入口，负责路由注册与应用启动
- **`src/models/expense.py`** — 支出数据模型（Expense ORM）
- **`src/services/expense_service.py`** — 业务逻辑层，封装记录、查询、统计操作

## 常用命令

```bash
# 安装 & 运行
uv sync
uv run uvicorn src.main:app --reload

# 测试
uv run pytest
uv run pytest --cov=src --cov-report=term-missing

# 代码检查 & 格式化
uv run ruff check .
uv run ruff format .

# 构建 / 部署
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000
```

## 约定与模式

- **所有文件** 开头必须有 `from __future__ import annotations`。
- **异步优先**：数据库操作使用异步 session，API 使用 `async def`。
- **测试数据库**：`conftest.py` 提供内存数据库 fixture 和测试客户端。
- **日志**：使用 `logging.getLogger(__name__)`，禁止 `print()`。
- **配置**：环境变量通过 `.env` 文件管理，禁止硬编码敏感信息。

## 测试模式

```python
# 测试数据初始化辅助函数
async def _seed_test_data(db: AsyncSession) -> list[Expense]:
    items = [
        Expense(amount=10.5, category="餐饮", note="午饭"),
        Expense(amount=5.0, category="交通", note="地铁"),
    ]
    db.add_all(items)
    await db.flush()
    return items

# 时间敏感测试使用 freezegun
from freezegun import freeze_time

@freeze_time("2026-01-05 10:00:00")
async def test_something(db_session):
    ...
```

## 重要约束

- **禁止重量级依赖** — 不引入 React/Vue 等前端框架；不使用 PostgreSQL/MySQL（SQLite 即可）
- **敏感数据** — 单用户本地工具，无需用户认证，无需密钥管理
- **数据库迁移** — 使用 SQLAlchemy `create_all` 自动建表，无需 Alembic
- **代码限制** — 行宽 120 字符，单函数不超过 50 行，单文件不超过 500 行
