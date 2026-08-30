# PRD 到原型

这一步是**路径 B** 的工程入口：已有完备 PRD，据此生成可评审原型，再落到代码。与 [原型先行路径 A](../05-ai-design-workflow/prototype-first-workflow.md) 相反——这里 PRD 是设计的前置输入。逐步操作、契约模板与 `AGENTS.md` 见 [Figma Make 高保真保姆级教程](../05-ai-design-workflow/figma-make-high-fidelity.md)。

人拥有契约（组件清单、Token、命名、状态矩阵）；AI 只在冻结契约内执行。下面的操作顺序依次消解路径 B 的三个典型失败：PRD 太长就先壳后逐页（步骤 1、4）；组件不规范就先冻库、缺则审批入库（步骤 3）；文字传不了视觉就 Copy design 精修后走 MCP（步骤 5、6）。三者的完整对照表在 [Figma Make 高保真保姆级教程](../05-ai-design-workflow/figma-make-high-fidelity.md)。

Make 产出 = 验证用 code-backed 原型，**禁止当生产代码**。MCP `get_design_context` 是 React+Tailwind 中间表示，要翻译进本仓库组件 + Token。

## 输入与产出

输入：PRD、角色、业务对象、权限规则、接口草案和已知限制。

产出：

1. [UI Brief](../templates/ui-brief.md)
2. [页面清单](../templates/page-inventory.md)
3. [组件清单](../templates/component-inventory.md)
4. 用户流程、页面状态矩阵和低保真线框
5. 可在 Figma/Make 中评审的高保真原型（验证用，不是生产代码）
6. 冻结的组件契约与 `AGENTS.md` 链接（路径 B 必做）

## 操作顺序

### 1. PRD → 四件套（禁止本轮生成界面）

把 PRD 改写成五列，避免直接从技术接口推页面：

| 项目 | 示例 |
| --- | --- |
| 角色 | 运营专员、主管、审计员 |
| 对象 | 订单、审批任务、客户 |
| 高频任务 | 筛选订单、查看详情、批量审批 |
| 风险任务 | 撤回、驳回、删除 |
| 完成条件 | 状态更新、有审计记录、失败可恢复 |

补齐每个任务的入口、前置条件、成功反馈和失败恢复。权限不足不是异常分支，而是页面设计的一种状态。

用下面的 Prompt 填 [UI Brief](../templates/ui-brief.md)、[页面清单](../templates/page-inventory.md)、[组件清单](../templates/component-inventory.md)、状态矩阵。订单工作台 Demo 最小范围可先锁 `/approvals` 与 `/orders`；完整清单示例：

```text
/orders              订单列表
/orders/:id          订单详情
/orders/new          创建订单
/orders/:id/edit     编辑订单
/approvals           审批队列
```

Frame 命名 = 路由 + 状态，如 `/approvals/loading`。8 态：默认、加载、空数据、无结果、错误、无权限、成功、部分失败。

可复制 Prompt（四件套，禁止生界面）：

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

### 2. 灰度骨架

先确认容器、信息层级和操作顺序，再进入 [Design Token](../04-design-system/tokens.md) 和品牌色。订单列表至少应能回答：当前筛选条件、结果数量、单行主动作、批量操作和下一页在哪里。

```text
页面标题 + 创建订单
筛选条件                              已选 3 项  批量审批
结果摘要
订单号 | 客户 | 金额 | 状态 | 更新时间 | 操作
--------------------------------------------------
分页 / 每页数量
```

### 3. 冻结壳层 + 组件清单 / 契约

先冻 AppShell（导航 / 顶栏 / 内容槽），再按批准名单一次一个组件写契约（`docs/contracts/`），并由 `AGENTS.md` 链接。**人冻结**之后才允许做页。缺组件必须提案、人批准后才入库。禁止 AI 自行新建；禁止「全局抽取组件并改所有引用」。

可复制 Prompt（禁止新建组件）：

```text
对照 docs/component-inventory.md 与 docs/contracts/。
本任务只实现页面结构，必须使用清单中的组件名。
禁止新建同义组件（例如库存是 Dialog 时禁止 Modal.tsx）。
若现有组件做不到：停止实现，输出入库提案（方案 | 理由 | 改哪些文件），等我书面批准。
禁止修改：已冻结组件的 props、tokens.css、未点名的页面。
```

可复制 Prompt（缺组件只提案）：

```text
当前任务：[例如 /approvals 日期筛选]。现有组件已冻结，不得自行新建。
判断能否用现有组件完成。输出二选一，不要写代码：
A. 复用某某（列出需补的 props）
B. 申请新组件某某（必须写出现有组件做不到的点）
禁止修改任何文件；禁止在页面里先做临时控件。
```

### 4. Make：先壳 + 一页，再逐页逐态

把四件套提供给 Figma Make。第一次只做壳 + `/approvals` 默认态；其余状态一次一事。Plan mode、frame by frame，见保姆级教程 [Step E / Step F](../05-ai-design-workflow/figma-make-high-fidelity.md)。不要只生成一张“正常态”截图；也不要一次生成整站。已有组件包时优先 [Make kits](https://help.figma.com/hc/en-us/articles/39241689698839-Get-started-with-Make-kits)，不是必须。Make「改本地仓库」是封闭 beta，不是主路径。

评审时使用 [设计评审记录](../templates/design-review.md)，先评审主任务、信息层级和危险操作，再评审颜色和装饰。

可复制 Prompt（Make 只做壳 + `/approvals/default`）：

```text
这是验证用 code-backed 原型，不是生产应用。先出 Plan，不要直接生成整站。
本轮只做：AppShell + /approvals 默认态（FilterBar + 已选 N 项 + 批量审批 + OrderTable + Pagination）。
本轮不做：其余 7 态、/orders 列表、设置页、暗色主题。
组件名对照组件清单，禁止自行新建。危险操作必须显示选中数量。
```

### 5. Copy design → 人精修

用官方 [Copy design](https://help.figma.com/hc/en-us/articles/35060759685015-Copy-a-Figma-Make-preview-as-design-layers) 把当前 preview 贴进 Figma Design（单向快照：不可交互、不回写 Make）。粘贴前先给目标 Design 文件挂上含 Variables 的库，官方会自动匹配绑定变量；组件与样式仍要人挂。之后人做 Auto Layout / 语义命名 / 组件实例 / 补绑 Variables。不要未整理就 MCP。清单见 [Figma 体系](../05-ai-design-workflow/figma-stack.md) 与保姆级教程 [Step H](../05-ai-design-workflow/figma-make-high-fidelity.md)。

### 6. MCP → 代码

推荐 Remote MCP `https://mcp.figma.com/mcp`（Cursor `/add-plugin figma`）；Desktop `http://127.0.0.1:3845/mcp` 可选。取上下文一律 Copy link to selection。有席位则配 [Code Connect](https://developers.figma.com/docs/code-connect/)。一次一个 Frame，先计划后写码——MCP 读取按席位限流，整页乱读会烧光当天配额。见 [原型到代码](prototype-to-code.md) 与保姆级教程 [Step I–K](../05-ai-design-workflow/figma-make-high-fidelity.md)。

## 完成标准

- 每个主流程都有入口、完成条件、失败恢复。
- 页面、组件和状态都能在模板中找到对应记录；**组件清单已冻**，缺组件有入库记录。
- Frame 按路由 + 状态命名，8 态可点。
- 原型中的层级、操作和异常状态通过 [视觉验收](../templates/visual-acceptance.md) 记录。
- **生产代码不来自 Make zip**；MCP 中间表示已翻译进本仓库组件 + Token。
- 产品评审通过后，才进入 [原型到代码](prototype-to-code.md)。
