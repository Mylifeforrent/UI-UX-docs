# PRD 到原型

← 返回 [工程工作流](README.md) · [原型先行全流程主文档](../imports/prototype-first-workflow.md)

PRD 先行路线（路径 B）：已有签字 PRD，据此生成原型。与[原型先行路径 A](../imports/prototype-first-workflow.md)相反——这里 PRD 是设计的前置输入。适用于强合规、需求已定的场景。逐步操作见 [Figma Make 高保真保姆级教程](../imports/figma-make-high-fidelity.md) Step A–K。

人拥有契约（组件清单、Token、命名、状态矩阵）；AI 只在冻结契约内执行。三个解法必须按序做实，不要弱化：

| # | 问题 | 解法 | 禁止 |
| --- | --- | --- | --- |
| 1 | PRD 太长一次生成会失真 | 先壳层 + 基本功能，再逐页、逐状态细化。Make 官方也要求 layout first、frame by frame、plan mode | 整份 PRD 一次生成整站 |
| 2 | 页面组件不规范 | 组件库先行并**人冻结**；缺组件提案、人批准后才入库；后续靠改组件 | 把「有则复用无则新建」交给 AI；全局抽取 |
| 3 | Make 文字传不了视觉 | Make 只验证交互；[Copy design](https://help.figma.com/hc/en-us/articles/35060759685015-Copy-a-Figma-Make-preview-as-design-layers) 贴进 Design（单向快照）；人精修后 MCP 读选区链接 | 把 Make 当生产；截图当间距来源 |

Make 产出 = 验证用 code-backed 原型，**禁止当生产代码**。MCP `get_design_context` 是 React+Tailwind 中间表示，要翻译进本仓库组件 + Token。无 [Code Connect](https://developers.figma.com/docs/code-connect/) 时 Agent 会发明长得像的 div。

## 前提

- PRD 已定稿，含：角色权限、页面清单、每页状态、交互与异常流、验收标准。
- 若 PRD 缺状态说明（只写了"正常态"），先补状态矩阵再进原型，否则原型只会有正常态。
- Frame 命名 = 路由 + 状态，如 `/approvals/loading`。8 态：默认、加载、空数据、无结果、错误、无权限、成功、部分失败。

## 步骤

1. **PRD → 四件套**：用下面的 Prompt 把 PRD 转成 [UI Brief](../templates/ui-brief.md)、[页面清单](../templates/page-inventory.md)、[组件清单](../templates/component-inventory.md)、状态矩阵。**禁止本轮生成界面。**
2. **手画灰度线框**（见下）。骨架 ≈ 可点 demo 的结构，不定色。
3. **冻结壳层 + 组件清单 / 契约**：先冻 AppShell，再按批准名单一次一个组件写 `docs/contracts/`，由 `AGENTS.md` 链接。缺组件走入库审批，**禁止 AI 自行新建**。
4. **Make：先壳 + 一页，再逐页逐态**：同保姆级教程 [Step E / F](../imports/figma-make-high-fidelity.md)，不要指望一次生成全部。已有组件包时优先 [Make kits](https://help.figma.com/hc/en-us/articles/39241689698839-Get-started-with-Make-kits)，不是必须。Make「改本地仓库」是封闭 beta，不是主路径。
5. **Copy design → 人精修**：单向快照，不回写 Make。清单见 [Figma 体系](../imports/figma-stack.md) 与保姆级 [Step H](../imports/figma-make-high-fidelity.md)。不要未整理就 MCP。
6. **MCP → 代码**：Remote 优先；一次一个 Frame；先计划后写码。见 [原型到代码](prototype-to-code.md) 与保姆级 [Step I–K](../imports/figma-make-high-fidelity.md)。

## 可复制 Prompt（PRD → 四件套）

```text
你是企业 SaaS 产品设计师。以下是已定稿 PRD：[粘贴/给路径]。
本轮任务：把 PRD 转成设计四件套，禁止本轮生成界面、不写前端、不打开 Figma Make。
输出四个 Markdown 区块：
1. UI Brief（目标、角色与权限、对象与主任务、约束）；
2. 页面清单（路由 | 页面名 | 职责 | 需覆盖状态 | 关键组件 | 优先级）；
3. 组件清单（组件名 | 职责 | 状态 | 键盘行为 | 令牌映射）；
4. 状态矩阵（每页每状态：看到什么 | 能做什么 | 不能做什么）。
约束：只依据 PRD，不新增 PRD 未提及的能力；PRD 未写的状态标注"PRD 缺失，需补充"，不要臆造。
禁止把「看起来能复用」写成新组件；组件名以清单为准。
```

## 可复制 Prompt（禁止新建组件）

```text
对照 docs/component-inventory.md 与 docs/contracts/。
本任务只实现页面结构，必须使用清单中的组件名。
禁止新建同义组件（例如库存是 Dialog 时禁止 Modal.tsx）。
若现有组件做不到：停止实现，输出入库提案（方案 | 理由 | 改哪些文件），等我书面批准。
禁止修改：已冻结组件的 props、tokens.css、未点名的页面。
```

## 可复制 Prompt（Make 只做壳 + `/approvals/default`）

```text
这是验证用 code-backed 原型，不是生产应用。先出 Plan，不要直接生成整站。
本轮只做：AppShell + /approvals 默认态（FilterBar + 已选 N 项 + 批量审批 + OrderTable + Pagination）。
本轮不做：其余 7 态、/orders 列表、设置页、暗色主题。
组件名对照组件清单，禁止自行新建。危险操作必须显示选中数量。
```

## 可复制 Prompt（缺组件只提案）

```text
当前任务：[例如 /approvals 日期筛选]。现有组件已冻结，不得自行新建。
判断能否用现有组件完成。输出二选一，不要写代码：
A. 复用某某（列出需补的 props）
B. 申请新组件某某（必须写出现有组件做不到的点）
禁止修改任何文件；禁止在页面里先做临时控件。
```

## 灰度线框（纯文本画法）

线框先定**容器和信息层级，不碰颜色**。后端开发者用纯文本/ASCII 就能画，无需设计工具：

```text
┌───────────────────────────────────────────────┐
│ 审批队列  待处理 12        [ 批量审批 (3) ]      │  ← 标题栏：左标题+计数，右主操作
├───────────────────────────────────────────────┤
│ [状态▾] [客户▾] [日期范围▾]        已选筛选 2    │  ← 筛选栏
├───────────────────────────────────────────────┤
│ ☐ 订单号  客户      金额     状态    更新   操作  │  ← 表头
│ ☑ #1024  华东公司  ¥12,400  待审批  2h   ⋯      │
│ ☐ #1025  ……                                    │
├───────────────────────────────────────────────┤
│                         ‹ 1 2 3 › 每页 20 ▾     │  ← 分页
└───────────────────────────────────────────────┘
```

要点：一个框=一个容器；标注主/次操作位置；每个状态各画一版（空态、错误态框里写具体文案）。

## 完成标准

- 每个主流程都有入口、完成条件、失败恢复。
- **组件清单已冻**；`AGENTS.md` 已链接契约；缺组件有人批准记录。
- Frame 按路由 + 状态命名，8 态可点。
- **生产代码不来自 Make zip**；MCP 中间表示已翻译进库存组件 + Token。
- 产品评审通过后，才进入 [原型到代码](prototype-to-code.md)。

## 相关文档

- [UI Brief](../templates/ui-brief.md) · [页面清单](../templates/page-inventory.md) · [组件清单](../templates/component-inventory.md)
- [Prompt 与上下文](../imports/prompting-and-context.md) · [原型到代码](prototype-to-code.md)
- [Figma Make 高保真保姆级教程](../imports/figma-make-high-fidelity.md) · [Figma 体系](../imports/figma-stack.md)
