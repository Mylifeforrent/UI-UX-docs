# 工具矩阵

← 返回 [原型先行全流程主文档](../imports/prototype-first-workflow.md)

选工具的依据是**你要的可控性、协作方式和交付形态**，不是"哪个最火"。这份矩阵帮你在几条主流路线里选对。具体能力与定价以各产品官方为准。

## 主流工具对比

| 工具 | 定位 | 视觉可控性 | 输出 | 最适合 | 边界/代价 |
| --- | --- | --- | --- | --- | --- |
| **Figma Make** | 自然语言生成 code-backed 原型 | 高（可转 Figma Design 精修） | 原型（验证用） | 需可评审视觉基准、要走 MCP→代码 | 原型不进生产；需付费席位 |
| **v0** | Prompt 生成 React/Tailwind 组件 | 中 | 可用代码片段 | 一次性 MVP、快速起页面 | 视觉体系较难长期统一 |
| **Lovable** | 生成全栈可部署应用 | 中 | 可部署应用 | 端到端快速上线的小产品 | 深度定制/合规场景受限 |
| **Cursor** | AI IDE，本地改真实代码库 | —（跟随你的代码） | 生产代码 | 在已有工程里落地、接 MCP | 需要工程上下文喂养 |
| **Claude Code** | 终端/IDE 内的 Coding Agent | —（跟随你的代码） | 生产代码 | 本地 Agent 读 Figma MCP 生成代码 | 同上 |

## 按场景选路线

| 场景 | 选择 | 说明 |
| --- | --- | --- |
| 需求不确定、要先验证交互 | Figma Make → MCP → Cursor/Claude Code | 走[原型先行全流程](../imports/prototype-first-workflow.md) |
| 强合规、PRD 已签字 | PRD → Make → 代码 | 走 [PRD 到原型](../06-engineering-workflow/prd-to-prototype.md) |
| 一次性 MVP、不追求视觉可控 | PRD 直接给 v0 / Lovable | 跳过精细设计阶段 |
| 已有工程，只补页面 | Cursor / Claude Code + 组件库 | 直接在代码库里做，配 Code Connect |

## 关键判断维度

1. **可控性**：要长期维护、多人协作、统一视觉 → 选可控性高、能出 Figma Design 的路线（Make）。
2. **交付形态**：要原型还是生产代码？原型验证用 Make，生产代码永远用本地 Agent 重新生成（见 [Figma 体系](../imports/figma-stack.md)）。
3. **合规**：需签字流程 → PRD 先行；探索性 → 原型先行。

## 相关文档

- [原型先行全流程](../imports/prototype-first-workflow.md) · [工程工作流](../06-engineering-workflow/README.md)
- [Figma 体系](../imports/figma-stack.md)
