# 🧠 Claude Code × Superpowers 演示仓库 — 项目长期记忆

> **用途**：存储项目的稳定事实、架构决策、关键约束和常见问题。
> AI Agent 在每次任务开始时应阅读此文件。
> 当项目发生重大变化时，必须同步更新此文件。

---

## 📋 项目基本信息

| 属性 | 值 |
|------|---|
| 项目名称 | Claude Code × Superpowers 演示仓库 |
| 项目类型 | 教学演示仓库 |
| 业务场景 | 演示如何在 Claude Code 中组合使用 superpowers 5.0.7 + ai-coding-ok，提升 AI 辅助开发效率 |
| 目标用户 | 知识星球成员，想学习 AI 辅助编程最佳实践的开发者 |
| 当前阶段 | v0.1.0 Todo Demo 完成 |
| 设计原则 | 极简实用，步骤可复制，拒绝过度设计 |
| 主语言 | Python 3.11（宿主机实际版本） |
| 后端框架 | FastAPI 0.115 |
| 数据库 | SQLite（零配置，适合演示） |
| 测试框架 | pytest 8.x |

---

## 🏗️ 架构概述

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

### 设计决策摘要
- 选用 SQLite 因为演示项目用户规模小、部署简单，零配置即可运行
- 选用 FastAPI 因为语法简洁、自带 OpenAPI 文档，适合教学演示
- 融合 superpowers + ai-coding-ok 解决两大核心痛点：工程纪律 + 跨会话记忆

---

## 🔄 核心业务流程

```
[演示流程]
克隆仓库 → 阅读 CLAUDE.md + AGENTS.md → 开始第一个任务
              ↓
    brainstorming → writing-plans → TDD 实现 → verification
              ↓
    更新记忆文件 → 下次任务自动载入上下文
```

---

## 📦 核心模块

| 模块 | 说明 | 状态 |
|------|------|------|
| `CLAUDE.md` | Claude Code 行为指令总入口，融合两套框架 | ✅ 完成 |
| `AGENTS.md` | 项目架构速查，Agent 任务开始必读 | ✅ 完成 |
| `.github/agent/memory/` | 三层记忆系统（长期/中期/短期） | ✅ 完成 |
| `.claude/plugins/superpowers/` | superpowers 5.0.7 技能库 | ✅ 完成 |
| `src/database.py` | SQLite 连接管理与建表 | ✅ 完成 |
| `src/models.py` | Pydantic 数据模型（Todo/TodoCreate/TodoUpdate） | ✅ 完成 |
| `src/services.py` | 业务逻辑层（CRUD） | ✅ 完成 |
| `src/routers/todos.py` | FastAPI 路由层 + 依赖注入 | ✅ 完成 |
| `src/main.py` | 应用入口 + lifespan + 静态文件 | ✅ 完成 |
| `static/index.html` | Tailwind 单页前端 | ✅ 完成 |
| `tests/` | 22 个 pytest 测试（TDD） | ✅ 完成 |

---

## ⚠️ 关键约束

1. 演示项目保持轻量，禁止引入 Django ORM、Celery 等重量级依赖
2. 所有外部 API 调用必须有超时设置
3. SQLite 直接建表，无需 alembic 迁移工具
4. 敏感配置（API Key 等）必须通过 `.env` 管理，`.env` 加入 `.gitignore`

---

## 🐛 已知问题 & 常见坑

| 编号 | 问题 | 解决方案 | 日期 |
|------|------|---------|------|
| 1 | 项目初始化，无已知问题 | - | 2026-04-18 |
| 2 | FastAPI sync 路由在线程池运行，SQLite 连接跨线程报错 | `check_same_thread=False` | 2026-04-18 |

---

## 🔧 开发环境

### 启动方式
```bash
# 1. 克隆并进入项目
git clone <repo> && cd ai-coding-ok-cc-demo

# 2. 安装依赖
pip install -e ".[dev]"

# 3. 配置环境变量
cp .env.example .env
# 编辑 .env 填入必要配置

# 4. 启动服务
uvicorn src.main:app --reload
```

### 环境变量说明
| 变量 | 说明 | 是否必填 |
|------|------|---------|
| `DATABASE_URL` | SQLite 数据库路径，默认 `sqlite:///demo.db` | 选填 |
| `LOG_LEVEL` | 日志级别，默认 `INFO` | 选填 |

---

## 📊 项目健康指标

| 指标 | 目标 | 当前 |
|------|------|------|
| 测试覆盖率 | ≥80% | 待测量 |
| 测试用例数 | - | 22 |
| 线上事故 | 0 | 0 |
