# 📏 记账本 — 编码规范

> 所有人类和 AI 提交的代码都应遵守本文件中的规范。

---

## 1. 通用规范

### 1.1 导入

```python
# 标准库
from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path

# 第三方库
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

# 项目内部
from src.config import settings
```

- 导入分三组：标准库 → 第三方 → 项目内部，组间空一行
- 禁止使用 `from xxx import *`
- 使用绝对导入

### 1.2 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 模块/包 | snake_case | `expense_service.py` |
| 类 | PascalCase | `ExpenseService` |
| 函数/方法 | snake_case | `get_expenses()` |
| 变量 | snake_case | `total_amount` |
| 常量 | UPPER_SNAKE | `MAX_NOTE_LENGTH` |
| 私有成员 | _leading_under | `_parse_amount()` |
| API 路由 | kebab-case | `/api/expenses` |
| 数据库表 | snake_case 复数 | `expenses` |
| 环境变量 | UPPER_SNAKE | `DATABASE_URL` |

### 1.3 类型注解

```python
# ✅ 正确
def get_expenses(limit: int | None = None) -> list[Expense]:
    ...

# ❌ 错误 — 缺少类型注解
def get_expenses(limit=None):
    ...
```

- 所有函数参数和返回值必须有类型注解
- 使用 Python 3.12+ 语法：`list[int]` 而非 `List[int]`
- 使用 `X | None` 而非 `Optional[X]`

### 1.4 Docstring（Google 风格）

```python
def process_expense(expense: Expense, priority: int) -> Result:
    """Process an expense record with given priority.

    Args:
        expense: The expense to process.
        priority: Processing priority (1=highest).

    Returns:
        The processing result.

    Raises:
        ValueError: If priority is out of range.
    """
```

### 1.5 错误处理

```python
# ✅ 正确 — 具体异常 + 有意义的处理
try:
    result = await service.fetch_data()
except TimeoutError:
    logger.warning("Service timeout, will retry")
    return []

# ❌ 错误 — 裸 except
try:
    result = await service.fetch_data()
except:
    pass
```

### 1.6 日志

```python
import logging

logger = logging.getLogger(__name__)

logger.info("Expense recorded: id=%s, amount=%s", expense.id, expense.amount)
logger.error("Failed to save expense: %s", exc, exc_info=True)

# ⚠️ 禁止记录敏感信息
```

- 使用 `logging` 模块，禁止 `print()`
- 每个模块创建独立 logger
- 日志级别：DEBUG(调试) / INFO(业务操作) / WARNING(可恢复) / ERROR(错误) / CRITICAL(致命)

---

## 2. Web 框架规范

### 2.1 路由层

```python
router = APIRouter(prefix="/api/expenses", tags=["expenses"])

@router.get("/")
async def list_expenses(db: AsyncSession = Depends(get_db)) -> list[ExpenseResponse]:
    """List all expenses."""
    ...
```

- 路由函数只做：参数校验 → 调用 service → 返回响应
- 业务逻辑放在 service 层
- 使用依赖注入获取数据库 session

---

## 3. 数据库规范

### 3.1 Model 定义

```python
class Expense(Base):
    """Expense record model."""

    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[float] = mapped_column(nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    note: Mapped[str | None] = mapped_column(String(200))
    date: Mapped[date] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
```

### 3.2 注意事项
- 使用 WAL 模式提升并发读性能（SQLite）
- 不做复杂的并发写操作（单用户工具无需担心）
- 数据库文件定期手动备份即可

---

## 4. 测试规范

### 4.1 测试命名

```python
# 格式：test_<被测方法>_<场景>_<期望结果>
def test_create_expense_with_valid_input_returns_expense():
    ...

def test_create_expense_with_negative_amount_raises_error():
    ...
```

### 4.2 测试结构（AAA 模式）

```python
async def test_get_daily_total_returns_correct_sum(db_session):
    # Arrange — 准备数据
    expenses = [
        Expense(amount=10.0, category="餐饮", date=date(2026, 4, 19)),
        Expense(amount=5.0, category="交通", date=date(2026, 4, 19)),
    ]
    db_session.add_all(expenses)
    await db_session.flush()

    # Act — 执行操作
    total = await expense_service.get_daily_total(db_session, date(2026, 4, 19))

    # Assert — 验证结果
    assert total == 15.0
```

### 4.3 Mock 策略
- 外部服务：使用 `unittest.mock.AsyncMock` 模拟
- 时间相关：使用 `freezegun.freeze_time` 固定时间
- 数据库：使用内存 SQLite fixture（`:memory:`）

---

## 5. Git 规范

### 5.1 Commit Message
- 遵循 Conventional Commits
- 格式：`<type>(<scope>): <subject>`
- 类型：`feat` / `fix` / `docs` / `style` / `refactor` / `test` / `chore`
