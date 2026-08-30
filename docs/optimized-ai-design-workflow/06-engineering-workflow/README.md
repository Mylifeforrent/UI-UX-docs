# 工程工作流

← 返回 [原型先行全流程主文档](../imports/prototype-first-workflow.md)

这一章讲"从需求到可交付代码"的两条主线路，以及它们的取舍。核心区别是**顺序**：谁先谁后——PRD 先行，还是原型先行。

## 两条路线

| 路线 | 顺序 | 适用 | 详见 |
| --- | --- | --- | --- |
| **原型先行** | 竞品→建模→原型→评审→PRD 反写→代码 | 需求不确定、要快速验证交互；有设计协作需要可评审视觉基准 | [原型先行全流程](../imports/prototype-first-workflow.md) |
| **PRD 先行** | PRD→原型→代码 | 强合规、需 PRD 签字后才能投入设计 | [PRD 到原型](prd-to-prototype.md) |

两条线共用后半段：都要经过 [原型到代码](prototype-to-code.md) 和 [交付验收清单](acceptance-checklist.md)。

## 关键区别：PRD 是"记录"还是"输入"

- **原型先行**：PRD 是已验证原型的*记录*（反写），写的是验证过的决策，更准确。
- **PRD 先行**：PRD 是设计的*前置输入*，靠拍脑袋，需后续原型校正。

选错路线的代价：强合规项目跳过 PRD 签字直接做原型，会返工；探索性需求硬要先写完整 PRD，会写一堆没验证的假设。工具与路线取舍见 [工具矩阵](../07-tools/tool-matrix.md)。

## 本章文档

- [PRD 到原型](prd-to-prototype.md) —— PRD 先行路线（路径 B），含灰度线框与三解法；逐步操作见 [Figma Make 高保真保姆级教程](../imports/figma-make-high-fidelity.md)
- [原型到代码](prototype-to-code.md) —— 两条线共用的下半段与返工源清单
- [交付验收清单](acceptance-checklist.md) —— 最终交付前逐条勾选

## 相关文档

- [Agent 协作与人机边界](../imports/agent-collaboration.md)
- [Prompt 与上下文](../imports/prompting-and-context.md)
