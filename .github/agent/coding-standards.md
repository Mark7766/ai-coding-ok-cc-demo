# 📏 {{项目名称}} — 编码规范

> 所有人类和 AI 提交的代码都应遵守本文件中的规范。
> AI Agent 在写代码前必须阅读本文件。

---

## 1. 通用规范

### 1.1 导入顺序（以 Python 为例，其他语言类似分层）

```python
# 第一组：标准库
from __future__ import annotations
import logging
from datetime import datetime
from pathlib import Path

# 第二组：第三方库
from fastapi import APIRouter, Depends

# 第三组：项目内部
from src.config import settings
from src.models import User
```

- 三组之间空一行
- 禁止 `from xxx import *`
- 使用绝对导入

### 1.2 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 模块/包 | snake_case | `user_service.py` |
| 类 | PascalCase | `UserService` |
| 函数/方法 | snake_case | `get_user_by_id()` |
| 变量 | snake_case | `user_count` |
| 常量 | UPPER_SNAKE | `MAX_RETRY_COUNT` |
| 私有成员 | _leading_under | `_parse_token()` |
| API 路由 | kebab-case | `/api/user-profiles` |
| 数据库表 | snake_case 复数 | `user_profiles` |
| 环境变量 | UPPER_SNAKE | `DATABASE_URL` |

### 1.3 类型注解（强制）

```python
# ✅ 正确
def get_users(limit: int | None = None) -> list[User]:
    ...

# ❌ 错误 — 缺少类型注解
def get_users(limit=None):
    ...
```

### 1.4 Docstring（Google 风格，必须）

```python
def process_payment(order_id: str, amount: float) -> PaymentResult:
    """处理订单支付。

    Args:
        order_id: 订单唯一标识。
        amount: 支付金额（人民币元）。

    Returns:
        PaymentResult 对象，包含交易号和状态。

    Raises:
        PaymentError: 支付失败时抛出。
        ValueError: amount 不合法时抛出。
    """
```

### 1.5 错误处理

```python
# ✅ 正确 — 具体异常 + 有意义的处理
try:
    result = await payment_service.charge(amount)
except TimeoutError:
    logger.warning("支付超时，订单 %s 将重试", order_id)
    raise PaymentRetryableError(order_id)

# ❌ 错误 — 裸 except（禁止！）
try:
    result = await payment_service.charge(amount)
except:
    pass
```

### 1.6 日志（禁止 print）

```python
import logging

logger = logging.getLogger(__name__)

# 正确用法
logger.info("用户登录: user_id=%s", user.id)
logger.error("支付失败: order_id=%s, error=%s", order_id, exc, exc_info=True)

# 🚫 禁止
logger.info("密码: %s", password)  # 禁止记录敏感信息
print("debug:", data)              # 禁止 print
```

---

## 2. 代码结构约束

- 单个函数 / 方法：**≤ 50 行**（超出则拆分）
- 单个文件：**≤ 500 行**（超出则重构模块）
- 行宽：**≤ 120 字符**
- 嵌套层级：**≤ 4 层**（超出则提取函数）

---

## 3. 测试规范

### 3.1 测试命名

```python
# 格式：test_<被测方法>_<场景>_<期望结果>
def test_create_order_with_valid_input_returns_order_id():
    ...

def test_create_order_with_zero_amount_raises_value_error():
    ...
```

### 3.2 AAA 模式（必须）

```python
def test_calculate_discount_vip_user_gets_20_percent():
    # Arrange — 准备
    user = User(level="vip")
    original_price = 100.0

    # Act — 执行
    discounted = calculate_discount(user, original_price)

    # Assert — 验证
    assert discounted == 80.0
```

### 3.3 测试覆盖要求

- 核心业务逻辑：**≥ 90%**
- 整体覆盖率：**≥ 80%**
- 所有新功能必须附带测试
- 所有 Bug 修复必须先写复现测试

---

## 4. Git 规范

### 4.1 Commit Message（Conventional Commits）

```
<type>(<scope>): <description>

类型：feat / fix / refactor / test / docs / chore / perf / style
```

示例：
```
feat(auth): 添加 JWT 登录接口
fix(payment): 修复金额精度丢失问题
test(user): 补充边界值测试用例
docs(api): 更新接口文档
```

### 4.2 分支策略（GitHub Flow）

- `main`：生产就绪代码，禁止直接推送
- `feature/<name>`：新功能开发（superpowers worktree 自动创建）
- `fix/<name>`：Bug 修复
- PR 合并前必须通过 CI + Code Review

---

## 5. 安全规范

- **禁止**硬编码 API Key、密码、Token
- **禁止**在日志中输出用户密码、Token 等敏感信息
- 所有敏感配置通过环境变量（`.env` 文件）管理
- `.env` 必须加入 `.gitignore`
- 提供 `.env.example` 作为配置模板
