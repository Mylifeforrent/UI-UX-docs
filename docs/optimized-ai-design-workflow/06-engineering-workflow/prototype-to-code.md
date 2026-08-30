# 原型到代码

← 返回 [工程工作流](README.md) · [原型先行全流程主文档](../imports/prototype-first-workflow.md)

两条路线共用的下半段：把已验证、已整理的设计文件，交给本地 Coding Agent 生成生产代码。重点在**如何避免返工**和**哪些必须人工确认**。优先用 Frame 选区链接 + MCP 读取精修结构，不要只丢截图。MCP `get_design_context` 是 React+Tailwind 中间表示；无 [Code Connect](https://developers.figma.com/docs/code-connect/) 时禁止把它当最终实现，必须翻译进本仓库组件 + Token。Make 产出禁止当生产代码。逐步操作见 [Figma Make 高保真保姆级教程](../imports/figma-make-high-fidelity.md) Step I–K。

## 前提（缺一不可）

- 设计文件已整理：Frame 命名 = 路由 + 状态，Auto Layout，组件与变量齐全（见 [Figma 体系](../imports/figma-stack.md)）。不要未整理就 MCP。
- 推荐 Remote MCP（`https://mcp.figma.com/mcp`，必须 Copy link to selection）；Desktop MCP 可选。有组件库且有席位的已配 Code Connect；无映射时禁止把 MCP 中间表示当最终实现。
- PRD、[组件清单](../templates/component-inventory.md)、[Design Token](../04-design-system/tokens.md) 就绪。

## 生成流程（先计划后写码）

1. 在 Figma 右键目标 Frame → Copy link to selection。
2. 给 Agent 下面的 Prompt，**要求先出计划**。
3. 人工审计划（尤其看有没有"新建同义组件""临时颜色"）。
4. 确认后再让它写码，一次一页。

## 可复制 Coding Agent Prompt

```text
实现审批队列页 /approvals。
上下文：Figma frame 链接 [粘贴]、PRD（docs/prd-approvals.md）、
组件清单（docs/component-inventory.md）、Design Token（src/tokens.css）、
API 契约 [粘贴或文件路径]。
先输出实现计划：路由、组件拆分（对照组件清单，禁止新建同义组件）、
每个状态的数据来源、测试清单。等我确认后再写代码。
约束：只用已有 Token 和组件；空态/错误/无权限按 PRD 文案；
数据先用 fixture，不接真实 API；驳回必须二次确认。
```

## 常见返工源（提前规避）

| 返工源 | 根因 | 规避 |
| --- | --- | --- |
| Agent 重写了已有组件 | 没给组件清单 / 没配 Code Connect | 喂清单 + 禁新建同义组件 |
| 出现临时颜色/间距 | 没给令牌 / 没约束硬编码 | 喂 tokens.css + 禁硬编码（见 [tokens](../04-design-system/tokens.md)） |
| 只实现了正常态 | 状态矩阵没进上下文 | 明确列出每个状态及数据来源 |
| Frame 无法映射路由 | 设计文件 Frame 未命名 | 命名 = 路由 + 状态 |
| 一轮生成全部页面 | 单轮任务过大 | 一页一任务，先计划后写 |

## 必须人工确认（AI 生成后逐条过）

对应 [Agent 协作](../imports/agent-collaboration.md) 的人机边界：

- **权限**：无权限态、按钮禁用/隐藏逻辑是否正确
- **危险/不可逆操作**：二次确认、填理由、失败可逐条恢复
- **键盘焦点**：Tab 顺序、焦点可见、对话框焦点陷阱、Esc/Enter 语义
- **响应式**：桌面/手机关键差异（表格→摘要卡片）

## 交付前

跑一遍 [视觉验收](../imports/visual-review-loop.md) 和 [交付验收清单](acceptance-checklist.md)。

## 相关文档

- [Figma 体系](../imports/figma-stack.md) · [Design Token](../04-design-system/tokens.md)
- [组件清单](../templates/component-inventory.md) · [Agent 协作](../imports/agent-collaboration.md)
