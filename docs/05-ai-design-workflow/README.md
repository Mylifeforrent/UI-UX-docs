# AI 设计工作流

AI 的价值在于缩短探索、实现和修正循环，但设计约束、业务权限和最终验收仍需要人负责。

推荐闭环：

```text
PRD → [UI Brief](../templates/ui-brief.md) → Figma/Figma Make
→ [Design System](../04-design-system/README.md) → 原型评审
→ [Figma MCP](figma-stack.md) / 共享上下文 → AI Coding
→ 浏览器截图 → [视觉验收](../templates/visual-acceptance.md)
```

- [原型先行全流程实操](prototype-first-workflow.md)：竞品拆解 → 业务建模 → Figma Make 原型 → PRD 反写 → MCP 生成代码的手把手教学。
- [Figma 体系](figma-stack.md)：Figma、Figma Make、Figma MCP 的职责和生产边界。
- [Prompt 与上下文](prompting-and-context.md)：可复制 Prompt、输出格式和数据护栏。
- [Agent 协作](agent-collaboration.md)：产品分析、设计、评审和 Coding Agent 的分工。
- [视觉评审闭环](visual-review-loop.md)：固定视口、问题分级和前后截图。

产品功能会变化，实际接入前请以 [Figma 官方 AI 文档](https://www.figma.com/ai/) 和 [Figma Make](https://www.figma.com/make/) 为准。
