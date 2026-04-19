# 开发参考

## 环境搭建

```bash
# 安装 uv（如果还没有）
pip install uv
# 或参考官网：https://github.com/astral-sh/uv

# 克隆并安装依赖
git clone https://github.com/Mark7766/ai-coding-ok-cc-demo.git
cd ai-coding-ok-cc-demo
uv sync

# 配置环境变量
cp .env.example .env
```

`.env` 内容（默认值即可本地运行）：

```ini
DATABASE_URL=sqlite+aiosqlite:///./data/ledger.db
DEBUG=false
```

## 常用命令

```bash
# 启动开发服务器（热重载）
uv run uvicorn src.main:app --reload

# 运行测试
uv run pytest

# 带覆盖率
uv run pytest --cov=src --cov-report=term-missing

# 只跑单元测试
uv run pytest tests/unit/

# 只跑集成测试
uv run pytest tests/integration/

# 代码检查
uv run ruff check .

# 自动格式化
uv run ruff format .

# 类型检查
uv run mypy src/
```

## 数据库

数据库文件存放在 `data/ledger.db`（首次启动自动创建，需先 `mkdir data`，启动时会自动创建）。

**无需运行迁移命令**，使用 SQLAlchemy `create_all` 自动建表。

如需重置数据：
```bash
rm data/ledger.db
# 重启服务即自动重建
```

## 项目约束（AI 和人类都要遵守）

详见 [`AGENTS.md`](../AGENTS.md)，核心约束：

1. **前端**：Jinja2 + 原生 HTML/CSS，不引入 React/Vue，不引入 Node.js 构建链
2. **数据库**：SQLite only，不引入 PostgreSQL/MySQL
3. **无认证**：单用户本地工具，不需要登录系统
4. **代码限制**：行宽 120 字符，单函数 ≤ 50 行，单文件 ≤ 500 行

## 测试规范

所有测试使用内存 SQLite，测试间完全隔离（每个测试前 create_all，测试后 drop_all）。

```python
# 测试命名格式
def test_<方法名>_<场景>_<预期结果>():
    ...

# 使用 AAA 模式
async def test_get_daily_total_excludes_income(db_session):
    # Arrange
    await _create_expense(db, amount=100, record_type="支出")
    await _create_expense(db, amount=5000, record_type="收入")

    # Act
    total = await expense_service.get_daily_total(db, target_date)

    # Assert
    assert total == pytest.approx(100.0)
```

## 提交规范

遵循 [Conventional Commits](https://www.conventionalcommits.org/)：

```
feat(dashboard): add income vs expense monthly breakdown
fix(service): exclude income from daily total calculation
refactor(models): add record_type field with server_default
test(service): add dashboard stats unit tests
chore(deps): bump fastapi to 0.115.0
```

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | 首页（今日记录） |
| GET | `/?date=YYYY-MM-DD` | 指定日期的记录 |
| POST | `/expenses/create` | 创建记录（支出或收入） |
| GET | `/stats` | 月统计页（当月） |
| GET | `/stats?year=&month=` | 指定月份统计 |
| GET | `/dashboard` | 月度看板（当月） |
| GET | `/dashboard?year=&month=` | 指定月份看板 |
| DELETE | `/api/expenses/{id}` | 删除记录 |

### POST /expenses/create 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `amount` | float | 金额（必须 > 0） |
| `category` | string | 分类（支出7类 / 收入5类） |
| `record_type` | string | `支出` 或 `收入`（默认 `支出`） |
| `note` | string | 备注（可选，最长 200 字） |
| `expense_date` | date | 日期（YYYY-MM-DD） |

## 目录结构说明

```
src/
├── main.py              # FastAPI app 实例、路由定义、模板渲染
├── config.py            # pydantic-settings 配置（读 .env）
├── database.py          # SQLAlchemy 异步引擎、Session 工厂、Base 类
├── models/
│   └── expense.py       # Expense ORM 模型
│                        # 字段：id, amount, category, record_type, note, date, created_at
├── schemas/
│   └── expense.py       # Pydantic schemas + 分类常量（CATEGORIES, INCOME_CATEGORIES 等）
├── services/
│   └── expense_service.py  # 所有数据库操作封装
│                           # create / list_by_date / delete
│                           # get_daily_total / get_daily_income
│                           # get_monthly_stats / get_dashboard_stats
├── api/
│   └── expenses.py      # REST API 路由（目前只有 DELETE）
└── templates/
    ├── base.html        # 全局布局、CSS 变量、通用组件样式
    ├── index.html       # 首页：日期导航 + 记录表单 + 今日明细
    ├── stats.html       # 月统计：月份导航 + 分类统计 + 每日明细
    └── dashboard.html   # 看板：收入/支出/净结余 + 分类占比
```
