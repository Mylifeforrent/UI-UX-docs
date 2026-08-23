# Figma 体系

Figma 不是“画完就丢”的静态交付物，而是设计上下文、原型评审和 Agent 协作的一部分。具体权限和产品功能会变化，接入前以 [Figma AI](https://www.figma.com/ai/) 与 [Figma Make](https://www.figma.com/make/) 官方资料为准。

| 层 | 作用 | 输入 | 输出 | 人工检查 |
| --- | --- | --- | --- | --- |
| Figma Design | 视觉设计、组件、协作 | 页面结构、品牌、组件规范 | Frame、组件、Prototype | 层级、状态、可访问性、真实内容 |
| Figma AI | 局部生成、改写和探索 | Prompt、选中对象、已有设计 | 变体、文案、局部调整 | 业务准确性、Token 和状态 |
| Figma Make | code-backed 原型 | PRD、页面目标、数据、交互 | 可交互原型 | 不把原型代码直接当生产代码 |
| Figma MCP | 设计上下文连接 Agent | Frame、组件、Token、文件 | Agent 可引用的上下文 | 权限、命名、敏感文件隔离 |

## 推荐闭环

```text
PRD → [UI Brief](../templates/ui-brief.md) → Figma/Make 原型
→ 人工评审 → [Design System](../04-design-system/README.md)
→ MCP/上下文 → AI Coding → 浏览器截图 → 回到 Figma 或验收记录
```

把“生成页面”与“通过生产验收”分开：生产代码仍需测试、权限校验、真实数据、性能和 [交付验收](../06-engineering-workflow/acceptance-checklist.md)。企业数据使用前先脱敏并确认分享权限。
