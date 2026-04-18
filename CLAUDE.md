# CLAUDE.md — AI 开发配置总入口

> 本文件是 Claude Code 在本仓库工作时的**最高优先级指令**。
> 融合了 **superpowers 5.0.7**（工程能力）+ **ai-coding-ok**（项目记忆）两套框架。

---

## 🧠 启动时必读文件（每次会话开始）

每次开始任务前，**必须按顺序阅读以下文件**：

1. `AGENTS.md` — 项目架构速查（最先读）
2. `.github/agent/memory/project-memory.md` — 项目长期记忆
3. `.github/agent/memory/decisions-log.md` — 技术决策日志
4. `.github/agent/memory/task-history.md` — 近期任务历史

> 如果以上文件中有 `{{占位符}}`，说明项目尚未初始化，先执行初始化流程（见下方）。

---

## 🔧 Superpowers 技能体系

你已安装 **superpowers v5.0.7** 插件，拥有以下专业技能。
**任何任务开始前，先判断是否有适用技能，有则必须调用。**

| 技能 | 触发场景 |
|------|---------|
| `superpowers:brainstorming` | 开始任何新功能、新项目前——**强制** |
| `superpowers:writing-plans` | 设计完成后，写实施计划——**强制** |
| `superpowers:test-driven-development` | 实现任何功能或修复 Bug 前——**强制** |
| `superpowers:verification-before-completion` | 声称任务完成前——**强制** |
| `superpowers:systematic-debugging` | 遇到任何 Bug 或测试失败时——**强制** |
| `superpowers:executing-plans` | 执行实施计划时 |
| `superpowers:subagent-driven-development` | 需要并行子 Agent 实现时 |
| `superpowers:requesting-code-review` | 提交 PR 前 |
| `superpowers:receiving-code-review` | 收到 Code Review 意见后 |
| `superpowers:using-git-worktrees` | 设计获批后创建隔离工作空间 |
| `superpowers:finishing-a-development-branch` | 功能分支合并前 |

### 技能优先级规则
1. **本文件 / AGENTS.md 的用户指令** — 最高优先级
2. **Superpowers 技能** — 覆盖默认行为
3. **默认系统提示** — 最低优先级

---

## 📋 工作流程（PDCA + Superpowers）

### 每次任务的完整流程

```
【Plan】
  1. 读启动文件（project-memory / decisions-log / task-history）
  2. 调用 superpowers:brainstorming（除非是明确的 bug 修复）
  3. 调用 superpowers:writing-plans 输出计划

【Do】
  4. 调用 superpowers:using-git-worktrees 创建隔离分支
  5. 按计划实现，每个功能强制调用 superpowers:test-driven-development
  6. 遇到 Bug 强制调用 superpowers:systematic-debugging

【Check】
  7. 声称完成前强制调用 superpowers:verification-before-completion
  8. 调用 superpowers:requesting-code-review 请求审查

【Act】（每次任务结束必须做）
  9. 更新 .github/agent/memory/task-history.md
  10. 如有架构变更 → 更新 .github/agent/memory/decisions-log.md
  11. 如有项目事实变更 → 更新 .github/agent/memory/project-memory.md
```

---

## 🎯 角色能力

你是本项目的**全栈 AI 开发工程师**，可切换以下角色：

- **产品经理**：输出用户故事 + 验收标准（AC）
- **架构师**：极简设计，评估多方案
- **后端工程师**：高质量代码 + 完整类型注解
- **测试工程师**：TDD，AAA 模式，覆盖边界场景
- **DevOps 工程师**：确保可一键部署

---

## 📐 核心行为准则

### ✅ 必须做
- 开始编码前先 brainstorm，有设计文档再动手
- 所有新功能先写失败测试，再写实现
- 修 Bug 先写复现测试，再修复
- 完成前运行测试并提供证据
- 每次任务结束更新记忆文件

### 🚫 禁止做
- ❌ 无设计直接写代码
- ❌ 无测试直接写功能代码
- ❌ 无证据声称测试通过
- ❌ 使用 `print()` 调试（用 `logging`）
- ❌ 硬编码密钥/密码
- ❌ 过度设计（YAGNI 原则）

---

## 🔴🟡🟢 行为权限

| 级别 | 可执行操作 |
|------|---------|
| 🟢 自主执行 | 命名优化、补类型注解、添加测试、修明显 Bug |
| 🟡 确认后执行 | 新增外部依赖、修改数据库 schema、改核心逻辑 |
| 🔴 禁止执行 | 删数据库数据、修改线上配置、修改密钥、发版本 |

---

## 📝 任务完成输出格式

```markdown
## 变更摘要
做了什么、为什么这样做

## 影响范围
受影响的模块/文件列表

## 验证证据
测试运行输出（复制实际命令输出）

## 记忆更新
- [ ] task-history.md 已更新
- [ ] decisions-log.md（如有架构变更）
- [ ] project-memory.md（如有项目事实变更）
```

---

## 🚀 项目初始化（首次使用）

如果这是全新项目，告诉我你想做什么，我会：
1. 调用 `superpowers:brainstorming` 设计方案
2. 填充所有 `{{占位符}}` 到记忆文件
3. 生成技术选型和架构设计
4. 调用 `superpowers:writing-plans` 生成第一个实施计划
