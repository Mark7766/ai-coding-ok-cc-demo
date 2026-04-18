# 📜 {{项目名称}} — 任务历史（短期记忆）

> **用途**：记录近期任务摘要，为 AI Agent 提供跨会话的短期上下文记忆。
> 保留最近 30 条任务记录，超出后归档至 `task-history-archive.md`。
> **每次任务结束，AI Agent 必须在此追加一条记录。**

---

## 记录格式

```markdown
### [TASK-{编号}] {任务标题}
- **日期**：YYYY-MM-DD
- **类型**：feat / fix / refactor / docs / chore / test
- **摘要**：一句话说明做了什么
- **变更文件**：列出核心变更文件（最多 5 个）
- **设计文档**：docs/superpowers/specs/YYYY-MM-DD-xxx.md（如有）
- **实施计划**：docs/superpowers/plans/YYYY-MM-DD-xxx.md（如有）
- **关联 Issue**：#xxx（如有）
- **注意事项**：后续需要特别关注的事项
```

---

## 任务记录

### [TASK-001] 项目框架初始化
- **日期**：{{初始化日期}}
- **类型**：chore
- **摘要**：融合 superpowers 5.0.7 + ai-coding-ok，建立 AI 辅助开发的完整框架
- **变更文件**：
  - `CLAUDE.md`（AI 行为指令总入口）
  - `AGENTS.md`（项目架构速查）
  - `.github/agent/memory/project-memory.md`（长期记忆）
  - `.github/agent/memory/decisions-log.md`（技术决策日志）
  - `.github/agent/memory/task-history.md`（本文件）
  - `.claude/plugins/superpowers/`（superpowers 插件）
- **注意事项**：
  - 填充所有 `{{占位符}}` 后框架才算真正激活
  - 第一个真实功能开发前，先用 brainstorming 技能完成设计
