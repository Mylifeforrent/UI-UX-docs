# Figma Make 高保真保姆级教程

场景：PRD 已完备。用 Figma Make 做接近可评审的高保真页面，再落到生产前端。贯穿 Demo：订单审批工作台的 `/approvals`（审批队列）与 `/orders`（订单列表，证明复用）。

硬边界：**Make 产出只做验证用 code-backed 原型，禁止当生产代码。** 生产代码经精修后的 Figma Design + [Figma MCP](figma-stack.md) +（如有）Code Connect，由本地 Coding Agent 生成。`get_design_context` 返回的是 React + Tailwind **中间表示**，必须翻译进本仓库组件和 Token，禁止原样合入。

界面会改版。点不到按钮时打开文中官方 URL，**以官方为准，不要编菜单**。工程 SOP 见 [PRD 到原型](../06-engineering-workflow/prd-to-prototype.md)；探索性需求走 [原型先行路径 A](prototype-first-workflow.md)。Prompt 写法见 [Prompt 与上下文](prompting-and-context.md)。

人机边界：**人拥有契约**（组件清单、Token、命名、状态矩阵）；AI 只在冻结契约内执行。

## 三个解法（必须按这个顺序）

| # | 问题 | 正确解法 | 禁止 |
| --- | --- | --- | --- |
| 1 | PRD 太长，一次生成会失真 | 先壳层 + 基本功能，再逐页、逐状态细化。Make 官方也要求 layout first、frame by frame、plan mode | 把整份 PRD 丢进 Make「生成整站」 |
| 2 | 页面组件不规范、每页长得不一样 | 组件库先行并**人冻结**；缺组件必须提案、人批准后才入库；后续一致性靠改组件 | 把「有则复用无则新建」交给 AI；「全局抽取组件并改所有引用」 |
| 3 | Make 文字传不了视觉密度 | Make 只验证交互；官方 **Copy design** 把当前 preview 贴进 Figma Design（单向快照）；人做 Auto Layout / 语义命名 / 组件实例 / Variables；再用 MCP 读精修 Frame（选区链接含 node-id）改生产代码 | 把 Make zip/源码当生产；截图当间距来源；把 Copy design 当双向同步 |

贯穿硬规则：

1. 组件库、类名、DOM、Token 是硬规则。Agent 不得自行发明同义组件。
2. 一次一事。Prompt 必须有「禁止修改」。先计划后写码。换页 = 新会话。
3. 每个组件一份契约 md；`AGENTS.md` 链接这些契约；**新任务开始必须先读**。人用 IDE 做 diff 底线。
4. 未冻结组件库禁止多窗口并行。
5. Frame 命名 = 路由 + 状态，如 `/approvals/loading`。8 态固定：默认、加载、空数据、无结果、错误、无权限、成功、部分失败。
6. 「功能 demo 最后再 UI」适合交互未定；PRD 已定要高保真走 Make。推荐混合：骨架 ≈ 可点 demo（用已冻组件默认外观），精修放在组件冻结之后。
7. 已有组件 npm 包时，优先用 Make kits + `guidelines.md` 提保真，不是必须。见 [Get started with Make kits](https://help.figma.com/hc/en-us/articles/39241689698839-Get-started-with-Make-kits)。
8. Make「改本地仓库」是封闭 beta，**不是主路径**。主路径：Make 验证 → Copy design → 人精修 → MCP → 本地仓库。

Copy design 官方说明：[Copy a Figma Make preview as design layers](https://help.figma.com/hc/en-us/articles/35060759685015-Copy-a-Figma-Make-preview-as-design-layers)。限制：图层不回写 Make、不可交互、**组件与样式不自动挂设计系统**。但**变量会自动匹配绑定**——粘贴前先在目标 Design 文件挂上含 Variables 的库，能省掉大半手工绑 Token 的活。

## 准备清单

### 账号与席位（以官方为准）

| 能力 | 官方入口 | 席位与可用性 |
| --- | --- | --- |
| Figma Make | [Explore Figma Make](https://help.figma.com/hc/en-us/articles/31304412302231-Explore-Figma-Make) | 付费计划的 Full 席位；其他席位与计划可试用 |
| Copy design | [Copy design](https://help.figma.com/hc/en-us/articles/35060759685015-Copy-a-Figma-Make-preview-as-design-layers) | 所有付费计划可用 |
| Remote MCP（推荐） | [Guide to the Figma MCP server](https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server) · [Remote 安装](https://developers.figma.com/docs/figma-mcp-server/remote-server-installation/) | 端点 `https://mcp.figma.com/mcp`。所有席位与计划都能连，但用量差别极大，见下 |
| Desktop MCP（可选） | 同上 Guide · [Desktop 安装](https://developers.figma.com/docs/figma-mcp-server/local-server-installation/) | 付费计划的 Dev/Full 席位 + 桌面端，`http://127.0.0.1:3845/mcp`。特定企业内网再用 |
| Code Connect | [Code Connect](https://developers.figma.com/docs/code-connect/) | Org/Enterprise + Dev/Full。无映射时 Agent 会发明长得像的 div；无套餐则靠契约 + 组件清单硬约束 |

**先算用量再排期。** MCP 的读取类工具有配额（[Rate limits & access](https://developers.figma.com/docs/figma-mcp-server/rate-limits-access/)）：Dev/Full 席位在 Professional / Organization 约 200 次/天，Enterprise 约 600 次/天；View / Collab 席位只有约 6 次/月，等于跑不动本流程。开工前让 Agent 调 `whoami` 确认账号席位。配额会调整，以官方表为准。

取设计上下文是**链接式**：右键 Frame → **Copy link to selection**，客户端只解析其中的 node-id，不会打开 URL。桌面端额外支持「实现当前选区」。

企业数据先脱敏。不要把真实订单号、客户手机号、API Key 贴进 Make 聊天。

### 仓库模板

从本仓库复制，不要另起命名：

| 复制自 | 落到 |
| --- | --- |
| [UI Brief](../templates/ui-brief.md) | `docs/ui-brief.md` |
| [页面清单](../templates/page-inventory.md) | `docs/page-inventory.md` |
| [组件清单](../templates/component-inventory.md) | `docs/component-inventory.md` |
| [设计评审](../templates/design-review.md) | `docs/design-review.md` |
| [视觉验收](../templates/visual-acceptance.md) | `docs/visual-acceptance.md` |

再约定：`docs/contracts/`（每组件一份 md）、仓库根 `AGENTS.md`、`src/tokens.css`（与 Figma Variables 同名）。

Frame 命名：

```text
/approvals/default
/approvals/loading
/approvals/empty
/approvals/no-results
/approvals/error
/approvals/forbidden
/approvals/success
/approvals/partial-failure
```

`/orders` 同一套 8 态。

### 配置 Remote MCP（Cursor 推荐）

官方：[Set up the remote server](https://developers.figma.com/docs/figma-mcp-server/remote-server-installation/)。Cursor 可用 `/add-plugin figma`，或在 `mcp.json` 写入：

```json
{
  "mcpServers": {
    "figma": {
      "url": "https://mcp.figma.com/mcp"
    }
  }
}
```

Claude Code 以官方 plugin / `mcp add` 为准，例如：

```bash
claude mcp add --transport http figma https://mcp.figma.com/mcp
```

桌面端点仍可用：`http://127.0.0.1:3845/mcp`（须开 Figma 桌面端 Dev Mode MCP）。验证：Agent 能调 `get_design_context`、`get_screenshot`、`get_variable_defs`。[Tools and prompts](https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/)

### 准备检查

- [ ] 能打开 Make 与 Design 文件
- [ ] 席位与 MCP 配额够用（View/Collab 先升 Dev/Full，否则本流程跑不动）
- [ ] Cursor 已连 Remote MCP（或书面选用 Desktop）
- [ ] 四件套已复制；`AGENTS.md` + `docs/contracts/` 将在 Step A/D 写
- [ ] PRD 已脱敏
- [ ] Code Connect：有席位则稍后映射；无席位则写进 Brief「MCP 示例必须改写成库存组件」

## 全景时间盒

范围：`/approvals` 全 8 态 + `/orders` 默认/加载/空数据作复用证明。单人串行约 **17 小时**，对应文末「今天只做这些」的 6 个半天。F1 之后可两人分页并行缩短墙钟时间，但组件仍须串行，总工时不变。不要压缩 Step D 和 H。

```text
 0.5h   准备（账号 / Remote MCP / 四件套空文件）
 1.5h   Step A  PRD → 四件套（禁止生界面）
 0.5h   Step B  灰度骨架
 1.0h   Step C  冻结壳层 AppShell
 2.5h   Step D  组件库先行 + 契约  →  【冻结点 F1】
 1.5h   Step E  Make：Plan → 壳 + /approvals 默认态
 2.0h   Step F  逐页逐态；缺组件 → Step G（人批准才入库）
 2.5h   Step H  Copy design → 人精修  →  【冻结点 F2】
 0.5h   Step I  确认 MCP；有席位则 Code Connect
 3.0h   Step J  本地 Agent：先计划后写码
 1.5h   Step K  视觉验收（代码问题 vs 设计问题分流）
```

```text
 PRD（已完备）──只抽取──► 四件套 + 灰度 + 契约 + AGENTS.md
                          │
                          ▼
              Figma Make（验证交互）──x──► 禁止进生产 git
                          │ Copy design（当前预览快照，单向）
                          ▼
              Figma Design（人：Auto Layout / Variables / 组件 / 命名）
                          │ Copy link to selection
                          ▼
              Figma MCP (+ Code Connect) → 本地 Agent → 生产代码
                          │                         │
                          └──── visual-acceptance ──┘
```

每步 Prompt 点出：Context / Role / Action / Format / Test / Constraints。不要指望一条 Prompt 做完全程。

## Step A 从 PRD 抽出四件套

**做什么**：把长 PRD 压成四件套。本步只出文档，不进 Make。这是解法 1。

**点哪里**：本地打开四件套空文件 + Cursor。不要打开 Make。

**可复制 Prompt**：

```text
Context：企业「订单审批工作台」。已有较完善 PRD（下方粘贴）。模板见 docs/templates/。
Frame/路由 = 路由+状态；8 态名称固定。本步只抽文档。
Role：企业 SaaS 产品设计师。不发挥、不补业务。
Action：只输出四件套——UI Brief、page-inventory（本阶段仅 /approvals 与 /orders，不要加详情/设置/仪表盘）、component-inventory（只允许 AppShell, Button, Input, Table, FilterBar, Dialog, StatusBadge, OrderTable, ApprovalDialog, EmptyState, Pagination；缺的标「待 Step D」）、两页 8 态矩阵（每格：看到什么 / 主按钮是否可用 / 空文案原文）。
Format：四个 Markdown 代码块，文件名标在块首。最后列 5 个必须产品确认的问题。
Test：Brief 有非目标；无权限是页面状态不是 toast；部分失败必须逐条说明；组件无同义名。
Constraints：不生成界面、不写前端、不打开 Make、不写颜色数值、不把「看起来能复用」写成新组件。禁止判断「哪些组件可复用」（清单即硬规则）。

[粘贴 PRD]
```

- 坏：`根据 PRD 做一套完整高保真，越全越好。`
- 出口：[ ] 四件套齐；[ ] 只有约定路由；[ ] 8 态有原文案；[ ] 人扫过权限（审计员不能批准）；[ ] 未打开 Make。

## Step B 灰度骨架

**做什么**：纯文本确认容器、信息层级、主按钮位置。仍不定色。

**可复制 Prompt**：

```text
Context：已批准的四件套 @docs/ui-brief.md @docs/page-inventory.md @docs/component-inventory.md
Role：B2B 信息架构师。用等宽文本画线框，不讨论美观。
Action：为 /approvals 的 8 态 + /orders/default 各画一张桌面 1440 线框。每张必须标出：筛选条件、结果数量、单行主动作、批量操作（始终可见「已选 N 项」）、分页、本态主按钮是否禁用。
Format：每张一个 text 代码块，第一行写 Frame 名。不要 hex、不要「现代感」。
Test：空数据文案「暂无待审批订单」；无结果「没有符合筛选条件的订单」+ 清除筛选；forbidden 不展示订单行；partial-failure 列出失败订单号+原因；两页壳层分区相同。
Constraints：不定色、不写 Tailwind、不生成 Figma、不把批量审批放进行内「更多」。
```

- 坏：`画一个漂亮的审批后台，参考 Linear。`
- 出口：[ ] 9 张骨架；[ ] 空 ≠ 无结果；[ ] 批量按钮在筛选栏右侧带数量；[ ] 决策写入 `design-review.md`。

## Step C 冻结壳层

**做什么**：先冻所有页共用的 AppShell。没有壳就进业务页，导航会每页分叉。

**点哪里**：可在 Design 建 `AppShell/desktop`（Shift+A 加 Auto Layout，内容槽留空）。不会 Design 时本步只冻文档 + Token 名，视觉壳放到 Step E 第一次 Make。官方：[Toggle on auto layout](https://help.figma.com/hc/en-us/articles/5731482952599-Toggle-on-auto-layout-in-designs)

**可复制 Prompt**：

```text
Context：@docs/ui-brief.md @docs/component-inventory.md。本步只定义 AppShell，不做表格/筛选/对话框。
Role：设计系统工程师。壳层类名与 DOM 一旦写下，后续页面不得分叉。
Action：写 docs/contracts/AppShell.md。DOM 必须为 app-shell / app-shell__nav / app-shell__main / app-shell__topbar / app-shell__content。导航只允许：订单 → /orders、审批 → /approvals。顶栏左侧标题槽、右侧用户槽。不要搜索框、不要通知铃。Token 只引用语义名。先给 5 步计划，等我回复「做」再改文件。
Test：契约含 desktop/compact；没有订单表格；导航 2 项。
Constraints：禁止改路由和 8 态名称；禁止全局扫描「抽取布局组件」；一次只交付 AppShell。
```

- 坏：`先把后台框架和审批列表一起做了。`
- 出口：[ ] `docs/contracts/AppShell.md`；[ ] inventory 里 AppShell 一行填完；[ ] 内容槽是空的。

## Step D 组件库先行（冻结点 F1）

**做什么**：解法 2。先入库再做页。**人批准组件名之后**才允许写契约和骨架。禁止「做着页面顺便抽组件」。一次一个组件：Button → Input → StatusBadge → Table → FilterBar → Dialog。其余 `OrderTable`、`EmptyState`、`Pagination`、`ApprovalDialog` 同模式。

**点哪里**：`docs/contracts/<Name>.md`；Design 文件 `Components` 页建 Component set；Variables 集合名与 `src/tokens.css` 对齐。创建组件与变体以官方为准：[Create components](https://help.figma.com/hc/en-us/articles/360038663154-Create-components-to-reuse-in-designs)、[Variables](https://help.figma.com/hc/en-us/articles/15145852043927-Create-and-manage-variables-and-collections)。

**可复制 Prompt（只做 StatusBadge；其它组件换名字重复）**：

```text
Context：@AGENTS.md @docs/component-inventory.md。订单状态枚举硬规则：pending_approval / approved / rejected / draft。Badge 只展示，不可点击。
Role：设计系统工程师。写契约和最小实现，不写页面。
Action：只做 StatusBadge：docs/contracts/StatusBadge.md（用本文契约模板）+ src/components/StatusBadge.tsx + 更新 inventory。DOM：<span class="status-badge status-badge--{status}">文本</span>。文本映射：待审批 / 已批准 / 已驳回 / 草稿。颜色用语义 Token，且文本必须存在。先计划，等「做」再写文件。
Test：四个 status 都有中文；非交互；无新依赖；无硬编码 hex。
Constraints：禁止修改 AppShell/页面；禁止发明 Chip/Tag/Pill；禁止全局抽取。
```

- 坏：`扫描整个项目，把重复 UI 抽成组件库。`
- 出口（F1）：[ ] 本步组件有状态/键盘/无障碍列；[ ] 每组件一份契约且已链进 `AGENTS.md`；[ ] Figma Components 页变体名与契约一致；[ ] 人打开 `Button.tsx` 确认原生 `<button>`、无 inline color；[ ] **宣布组件库冻结**，之后新建走 Step G。

## Step E Make：壳 + 一页默认态

**做什么**：解法 1 在 Make 里执行。先壳 + `/approvals/default`，不要 8 态一起生。Make 只验证交互。

**点哪里**（入口以官方为准）：[Create a Figma Make file](https://help.figma.com/hc/en-us/articles/31304485164695-Create-a-Figma-Make-file)、[Use plan mode](https://help.figma.com/hc/en-us/articles/40830441709719-Use-plan-mode-in-Figma-Make)。复杂任务先 Plan，看完计划再 Build。一次 1–2 个 frame。已有组件包时优先挂 Make kits。[Make kits](https://help.figma.com/hc/en-us/articles/39241689698839-Get-started-with-Make-kits)

**不要**把 Make 代码同步进 git 生产目录。不要把「改本地仓库」当主路径。

**可复制 Prompt（第一次：Plan + 壳 + 默认态）**：

```text
Context：这是验证用 code-backed 原型，不是生产应用。不接真实 API。组件名硬规则：AppShell, Button, Input, FilterBar, OrderTable, StatusBadge, Pagination, EmptyState, ApprovalDialog。侧栏「审批」→ /approvals；「订单」→ /orders（本轮 /orders 只放占位标题）。
Role：企业后台 UI 实现者。优先扫描、比较、重复操作。不要营销页。
Action：先出计划，不要直接写全部页面。计划只含：A. AppShell；B. /approvals 默认态（FilterBar + 已选 N 项 + 批量审批 + OrderTable 约 20 行假数据 + Pagination）；C. 本轮不做：其余 7 态、Dialog 流程、/orders 列表、暗色主题。
Format：plan.md：步骤、改哪些界面、不做清单。等我点 Build。
Test：首屏能勾选 3 行并看到「已选 3 项」和「批量审批（3）」；没有 KPI 卡和插画。
Constraints：禁止生成整站；禁止设置页/消息中心；一次只做壳 + /approvals 默认态。
```

计划批准后只执行 A+B。补 loading 另发一条，写清「禁止同时做 empty/error」。

- 坏：`做一个完整的订单审批后台，包含所有页面和状态，要很精美。`
- 出口：[ ] 能点侧栏看到默认态；[ ] 已选数量随勾选变；[ ] Make 代码未合入生产；[ ] 人实际点过勾选和批量按钮。

## Step F 逐页细化

**做什么**：同一 Make 文件，一次一页、一次一态。官方建议 frame by frame，不要一次贴所有屏。对话漂了就清上下文。换页建议新会话。

**可复制 Prompt（只做 /orders 默认态，证明复用）**：

```text
Context：组件库已冻结。/orders 必须复用 AppShell、FilterBar、OrderTable、StatusBadge、Pagination、Button。差异仅允许：顶栏标题「订单」；主按钮「创建订单」（可禁用并说明本原型未实现创建）。
Role：设计系统使用者。不得新建同义组件。
Action：只实现 /orders 默认态。表格列与 /approvals 相同。若缺组件，停止并输出「需要 Step G」，不要自己建。
Format：列出复用的组件名。
Test：DOM 仍是同一套壳/筛选/表类名；没有新的卡片布局替代表格。
Constraints：禁止修改 /approvals 任何状态；禁止「优化」共享组件视觉；禁止全局检查两页差异并自动抽取。
```

- 坏：`把 /orders 也做了，顺便把两页表格统一一下，再检查所有间距。`
- 出口：[ ] `/approvals` 至少 default + loading + empty + no-results + error + forbidden + 一条成功或部分失败；[ ] `/orders/default` 壳层一致；[ ] 没有第三种按钮样式。

## Step G 缺组件入库（人批准后才新建）

**做什么**：AI **不得**自行判断复用。发现缺口 → 提案 → **人书面批准** → 契约 → 实现 → 更新 inventory → 再回页面任务。

**可复制 Prompt（只提案、不实现）**：

```text
Context：@docs/component-inventory.md。当前任务：/approvals 日期筛选。现有组件已冻结。不得自行新建。
Role：设计系统管理员。你只提案。
Action：判断日期筛选能否用现有 Input（type=date）+ FilterBar 完成。输出二选一，不要实现代码：A 复用 Input（列出需补的 props）；B 申请新组件 DatePicker（必须写出 Input 做不到的点）。
Format：表格：方案 | 改哪些文件 | 风险 | 是否破坏冻结。不要写代码。
Test：没有「我先写一个再看」；没有修改任何文件。
Constraints：禁止修改任何文件；禁止页面里先做临时日期控件。
```

人批准后再单独一条 Prompt 只做该组件；下一个任务才接入 FilterBar。

- 坏：`日期筛选我顺手写了个 Calendar 放在页面里。`
- 出口：[ ] inventory 新行完整；[ ] 契约已链进 `AGENTS.md`；[ ] 页面任务重开时 Prompt 写死组件名。

## Step H Copy design → 人精修（冻结点 F2）

**做什么**：解法 3。把 **当前预览快照** 变成可编辑图层。人改 Auto Layout、命名、组件实例、Variables。**不要未整理就 MCP。**

官方限制：[Copy design](https://help.figma.com/hc/en-us/articles/35060759685015-Copy-a-Figma-Make-preview-as-design-layers) —— 图层不连回 Make；不可交互；组件与样式不自动挂设计系统。每个状态、每个关键 Dialog **各 Copy 一次**。

**点哪里**：**先**在目标 Design 文件挂上含 Variables 的库（官方会自动匹配并绑定可用变量，少一半手工活）→ Make preview 走到目标态 → 顶部 **Copy design**（复杂界面可能要等，以官方提示为准）→ 粘贴到 Design → 最外层改名为 `/approvals/default`。精修清单：

- Auto Layout（Shift+A），禁止绝对定位裸摆
- Frame 命名 = 路由 + 状态
- 重复元素做成 Component，页面上是 **instance**，不要 detach
- 颜色/间距绑 Variables：挂库后自动绑上的核对一遍，没绑上的手工补，对应 [Design Token](../04-design-system/tokens.md)
- 删隐藏层和无意义嵌套；长文案用真实长度
- 建议 Pages：`Cover` / `Components` / `Approvals` / `Orders`

**可复制 Prompt（只出检查单，不改代码）**：

```text
Context：已 Copy design 到 Figma Design，图层尚未整理。目标 Frame：/approvals/default。契约在 docs/contracts/。
Role：设计系统 QA，不是插画师。
Action：根据我接下来的图层/MCP 截图，只输出「人必须手改」清单：P0 结构（Auto Layout 断裂、未命名）；P1 未成 Component；P2 裸 hex；P3 假数据太短。不要生成代码。
Format：表格：问题 | 点哪个图层 | 在 Figma 做什么（只使用 Auto Layout、Variables、Create component、Rename）。
Constraints：禁止建议回到 Make 重新生成整站。
```

- 坏：`导出 PNG 让前端按像素还原。`
- 出口（F2）：[ ] 每个要开发的状态有独立 Frame，名字 = 路由 + 状态；[ ] 页面里是 instance；[ ] 抽查 3 个间距能在 Variables 找到；[ ] Make 只作交互演示，不再当视觉源。

## Step I 确认 MCP + Code Connect

**做什么**：让 Agent 读到精修后的 Design。远程 MCP **必须**右键 **Copy link to selection**（含 node-id），不要只丢文件级 Share 链接。Desktop 才支持「实现当前选区」。

有席位时把 Figma 组件钉到真实代码 import，见 [Code Connect](https://developers.figma.com/docs/code-connect/)。无映射时 Agent 会发明长得像的 div。人 review `.figma.ts` 后再 publish。

**可复制 Prompt（只验证能读，不写业务码）**：

```text
Context：请使用 Figma MCP。目标 Frame 链接：[粘贴 Copy link to selection]。硬规则 @AGENTS.md @docs/component-inventory.md
Role：接线工程师。本轮只读取，不实现页面。
Action：调用 get_design_context / get_screenshot / get_variable_defs（以实际可用工具为准）。报告 Frame 名、两层图层树、variables、识别到的 instance。对照 inventory 列出已匹配/未匹配。未匹配标成 Step G 候选，不要发明组件。不要改文件。
Format：表格：Figma 图层/组件 | inventory 名称 | 匹配? | 备注
Constraints：禁止改仓库；禁止下载整文件切图。
```

- 坏：`看看 Figma 里那个审批页，按你理解做成 React。`（无链接、无 MCP）
- 出口：[ ] 回报的 Frame 名是 `/approvals/default`；[ ] variables 能对上 `tokens.css`；[ ] 未匹配项进入 G，不进入 J。

## Step J 本地 Agent 写生产代码

**做什么**：顺序：Token 已有 → 组件已有 → 页面组起来。禁止从 MCP 示例贴一个内含私有 Tailwind 的整页。截图只做回归，不当间距来源。映射见 [原型到代码](../06-engineering-workflow/prototype-to-code.md)。

换页 = 新会话。新任务第一条必须读契约。

**可复制 Prompt（先计划；确认后再把「禁止现在改文件」拿掉，一次只做 /approvals 默认态）**：

```text
Context：@AGENTS.md @docs/ui-brief.md @docs/component-inventory.md @docs/contracts/*.md @src/tokens.css
Figma Frame（必须 MCP 读取）：[粘贴 /approvals/default 的 Copy link to selection]
Make 仅作交互参考，禁止把 Make 代码拷进本仓库。
Role：企业后台前端。MCP 的 React+Tailwind 只作中间表示，必须翻译进库存组件和 Token。
Action：只输出实现计划，不改文件：将读哪些 MCP 工具、将改文件列表、8 态如何用 fixture（建议 ?state=loading 与 Frame 名对应）、本任务不做清单。然后停下。
Test：计划里没有「生成整个应用」；组件全部来自 inventory。
Constraints：禁止现在改文件；禁止新增依赖；禁止接真实 API；禁止把 MCP Tailwind 当生产实现。
```

人回复「做」后，下一条只实现默认态，Constraints 写：禁止同时做 8 态；禁止改组件 props（除非停下走 G）；冲突以契约为准。

- 坏：`对照 Figma 把审批和订单都做了，顺便重构组件。`
- 出口：[ ] 人看过 diff：页面文件薄、组件文件稳；[ ] `?state=` 能切态；[ ] 生产代码中没有 Make 项目结构原样拷贝。

## Step K 视觉验收

**做什么**：固定视口截图，对照同名 Design Frame，记入 `visual-acceptance.md`。不一致先分流，一次只修一类。方法见 [视觉评审闭环](visual-review-loop.md)，最后过 [交付验收清单](../06-engineering-workflow/acceptance-checklist.md)。

| 现象 | 判为 | 回哪一步 |
| --- | --- | --- |
| 代码写了 inline 色 / 没用契约 class | 代码 | Step J |
| 代码忠实，但 Design 未 Auto Layout | 设计 | Step H |
| MCP 读错 Frame | 流程 | 改名，重 Copy link |
| 两页组件表现不一致 | 未冻结或页面私改 | 删私改；必要时 G |
| Make 交互对、Design 快照旧 | 源不同步 | 重新 Copy design 该态 |

**可复制 Prompt（只修一条视觉单）**：

```text
Context：视觉验收 UI-001 见 @docs/visual-acceptance.md。区域：筛选栏；视口：1440。当前：批量按钮与表格边线错位。期望：与内容容器左右对齐。Figma：[粘贴 /approvals/default 链接]。@docs/contracts/FilterBar.md
Role：前端工程师。最小改动。
Action：只修 UI-001。先 MCP 核间距。若是设计问题：停止改代码，告诉我回 Step H。
Constraints：禁止顺手修 UI-002；禁止全局检查所有对齐。
```

- 坏：`整体感觉不对，按设计再生成一遍页面。`
- 出口：[ ] P0/P1 全关或有延期；[ ] 默认+空+错误+无权限+部分失败有截图；[ ] Make 不在生产包里。

## 组件契约模板

每个组件一份，放到 `docs/contracts/StatusBadge.md`。**新任务开始必须先读相关契约。**

~~~~markdown
# 组件契约：StatusBadge

> 状态：冻结 / 草案
> 库存名：StatusBadge（禁止别名：Chip / Tag / Pill）
> 代码：src/components/StatusBadge.tsx
> Figma：Components 页 / StatusBadge（Copy link to selection：【粘贴】）
> Code Connect：src/components/StatusBadge.figma.ts（无套餐则写「无」）

## 用途
表达订单业务状态。非交互。用于 OrderTable 单元格。

## 变体与状态
| 属性 | 取值 |
| --- | --- |
| status | pending_approval / approved / rejected / draft |

无 size、禁止再加 `tone`。自身无 hover 强调。

## props

`type OrderStatus = "pending_approval" | "approved" | "rejected" | "draft"`

`type StatusBadgeProps = { status: OrderStatus; className?: never }`

文本：pending_approval→待审批；approved→已批准；rejected→已驳回；draft→草稿。

## Token
只允许 `--color-warning` `--color-success` `--color-danger` `--color-text` `--color-surface` `--space-1` `--space-2` `--radius-sm`。禁止 hex / 任意 px。

## DOM
`<span class="status-badge status-badge--pending_approval">待审批</span>`
根节点必须是 `span.status-badge`；内部无第二层 wrapper；不用 inline style。

## 禁止
禁止点击；禁止只用色块不写字；禁止为某一页改圆角；禁止新建 `ApprovalBadge.tsx`。

## 键盘 / a11y
非交互，不进入 Tab 序；颜色不是唯一通道。

## 变更流程
改 props 或 DOM = 破坏性变更：先改本契约 → 改 Figma 变体 → 改代码 → 回归 /approvals 与 /orders。
~~~~

## AGENTS.md 硬规则（15–25 行）

放到仓库根。不要写成「可以忽略的建议」。

```markdown
# 订单审批工作台 · Agent 硬规则

新任务开始必须先读：本文件、docs/ui-brief.md、docs/page-inventory.md、docs/component-inventory.md，以及本次涉及的 docs/contracts/*.md。未读契约不得写 UI。

1. 组件名、类名、DOM、Token 以契约与 component-inventory 为准。禁止自行判断「有没有可复用组件」。缺组件必须停下：提案 → 人批准 → 契约 → 实现 → 再改页面。
2. 禁止「全局检查并抽取组件」。禁止一次大规模重构。大任务拆小批次；一次只改一件事。
3. 每个 Prompt 必须写「禁止修改」列表。未列出的文件默认禁止改。
4. Frame / 路由命名 = 路由 + 状态，例如 /approvals/loading。8 态名称固定：默认、加载、空数据、无结果、错误、无权限、成功、部分失败。
5. Figma Make 只是验证用 code-backed 原型，禁止把 Make 代码合入生产。生产实现必须依据精修后的 Figma Design + MCP。
6. get_design_context 的 React+Tailwind 是中间表示，必须翻译进本仓库组件和 Token。与契约冲突时以契约为准。禁止 inline style 覆盖组件 class。
7. 先计划后写码。等人口头/书面确认再改文件。人用 IDE 做底线：TypeScript、ESLint、键盘走主流程、固定视口截图。
8. 多页并行前组件库必须已冻结。未冻结时禁止同时生成 /approvals 与 /orders。换页 = 新会话。
9. 危险操作必须显示选中数量；部分失败必须逐条说明。不要用纯颜色表达状态。
10. 数据用脱敏 fixture。禁止把密钥、真实客户 PII 发给外部模型。
11. 无 Code Connect 时禁止把 MCP 示例当最终实现。
12. 截图只做回归，不当间距来源。视觉问题一次只修一条；设计问题回 Figma，不要 magic number 凑。
13. 契约索引：docs/contracts/AppShell.md、Button.md、Input.md、FilterBar.md、Table.md、OrderTable.md、StatusBadge.md、Dialog.md、ApprovalDialog.md、EmptyState.md、Pagination.md。
14. 禁止新增依赖，除非任务明确批准。
15. 禁止改 page-inventory 已冻结的路由结构。
```

## 并行：对与错

前提：冻结点 F1 完成。否则禁止并行。

```text
冻结组件库
    ├─ 人 A：/approvals 8 态（一次一态）——只改 pages/approvals/* ，禁止改 src/components/*
    └─ 人 B：/orders 默认/加载/空数据——只改 pages/orders/*
发现缺组件 → 停 → Step G 单线程入库（全局锁）
```

页面并行，**组件串行**。两人 Prompt 都写 `禁止修改 src/components 与 src/tokens.css`。

| 错误 | 后果 |
| --- | --- |
| 未冻结就开两个 Agent 分别做两页 | 两套按钮、两套间距 |
| 「先做页面，回头再抽组件」 | 抽不干净，私有样式残留 |
| 两页并行时允许改 OrderTable | 互相覆盖 diff |
| 「全局检查两页并统一」一条 Prompt | 改一半停下，DOM 分叉 |
| 一个对话里同时贴 8 个 Frame 链接 | MCP 读错节点 |
| 两个 Make 文件各做一页 | 壳层分叉 |
| 用 /orders 的布局「参考」去改 /approvals | 参照错页 |

## 故障排查

| # | 症状 | 可能原因 | 怎么处理（一次一事） |
| --- | --- | --- | --- |
| 1 | AI 自称复用 FilterBar，实际页面有一份私有 class | 页面写了覆盖样式或复制 DOM | 搜 `className`/`style=`；删页面私有样式 |
| 2 | `/orders` 布局跟着详情稿走，表格变成卡片 | 贴错 Frame 或让它「参考某页」 | 只贴 `/orders/default`；禁止参考详情 |
| 3 | MCP 读不到 Frame | 贴了文件级 URL、未授权、Desktop 未开 | **Copy link to selection**；Remote 走 OAuth |
| 4 | 有上下文但间距仍错 | 没用 variables；或粘贴前没挂变量库 | `get_variable_defs`；回 Step H 挂库并补绑 |
| 5 | inline style 盖掉 class | MCP 示例被原样粘贴 | 本任务只删 inline；以契约 DOM 为准 |
| 6 | 一次改太多，只完成一半 | 一条 Prompt 含 8 态 + 重构 | git 还原；拆回一次一态 |
| 7 | Make 很漂亮，代码很丑 | 把 Make 当生产；或没经 Design 精修 | 走 Copy design + 人修 + MCP |
| 8 | 两页按钮圆角不一致 | 未成 Component 或页面改了 Button | 只改 Button 契约+组件；回归两页 |
| 9 | 空数据与无结果相同 | 未区分是否有筛选 | 用筛选条件分支；文案用 Brief 原文 |
| 10 | Agent 新建 `Modal.tsx` 而库存是 Dialog | 让模型自己判断复用 | 驳回 diff；指向 Dialog 契约 |
| 11 | Copy design 后无法成组件 | 图层碎、非 Auto Layout | 人从外向内 Shift+A；不要让 Agent「重绘」 |
| 12 | Code Connect Inspect 没有 snippet | 未 publish、席位不足 | 对照 [Code Connect](https://developers.figma.com/docs/code-connect/) |
| 13 | 对话越改越乱 | 上下文过长 | 清聊天；新对话只带冻结契约+当前 Frame |
| 14 | 部分失败只 toast | 未按 8 态做 Frame | 补 `/approvals/partial-failure`；独立任务 |
| 15 | 远程 MCP 看不到选区 | Remote 本来就看不到画布 | 必须 Copy link to selection |
| 16 | 整页丢给 get_design_context 后胡写 | 节点太大、无 Code Connect | 一次一个 Frame；无映射则强制库存组件 |
| 17 | MCP 突然全部调用失败或报配额 | 席位是 View/Collab，或当天读取超额 | `whoami` 查席位；升 Dev/Full；改用一次一个 Frame 省调用 |

## 专业设计师检查表（压缩）

对 `/approvals` 勾一轮，再对 `/orders` 勾一轮。不通过不要宣布高保真完成。

| 面 | 必须过的门 |
| --- | --- |
| 任务 | 3 秒内找到主任务；已选 N 项不滚动可见；危险操作含数量与后果 |
| 8 态 | 每态一张证据；空 ≠ 无结果；无权限不泄露行数据；部分失败逐条原因 |
| 布局 | Auto Layout / Fill；8px 节奏来自 Token；金额右对齐；无营销英雄区 |
| 组件 | 两页按钮一致；无 Dialog vs Modal；改一处 Button 两页一起变 |
| 字体色 | ≤ 3 档字号；状态不靠纯色；无随机 hex；焦点环可见 |
| 键盘 | Tab：筛选 → 表 → 批量 → 分页；Dialog 焦点陷阱；原生 button |
| 响应式 | 1440 表格；390 主按钮可点 |
| 工程 | Frame 名 = 路由 + 状态；MCP 对的是精修 Design 不是 Make 旧预览；Make 不在生产包 |

## 官方 URL（精简，界面以这些页为准）

| 你要做的事 | 官方文档 |
| --- | --- |
| 创建 Make、Plan、清上下文、frame by frame | [Create a Figma Make file](https://help.figma.com/hc/en-us/articles/31304485164695-Create-a-Figma-Make-file) |
| Plan mode | [Use plan mode](https://help.figma.com/hc/en-us/articles/40830441709719-Use-plan-mode-in-Figma-Make) |
| Copy design 与限制 | [Copy design](https://help.figma.com/hc/en-us/articles/35060759685015-Copy-a-Figma-Make-preview-as-design-layers) |
| Make kits（已有组件包时优先） | [Make kits](https://help.figma.com/hc/en-us/articles/39241689698839-Get-started-with-Make-kits) |
| Remote MCP、`https://mcp.figma.com/mcp`、Cursor `/add-plugin figma` | [Remote 安装](https://developers.figma.com/docs/figma-mcp-server/remote-server-installation/) · [MCP Guide](https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server) |
| Desktop MCP `http://127.0.0.1:3845/mcp` | [Desktop 安装](https://developers.figma.com/docs/figma-mcp-server/local-server-installation/) |
| MCP 席位与用量配额 | [Rate limits & access](https://developers.figma.com/docs/figma-mcp-server/rate-limits-access/) |
| Code Connect | [Code Connect](https://developers.figma.com/docs/code-connect/) |
| Auto Layout / 组件 / Variables | [Auto layout](https://help.figma.com/hc/en-us/articles/360040451373-Guide-to-auto-layout) · [Components](https://help.figma.com/hc/en-us/articles/360038663154-Create-components-to-reuse-in-designs) · [Variables](https://help.figma.com/hc/en-us/articles/15145852043927-Create-and-manage-variables-and-collections) |
| 产品入口 | [figma.com/make](https://www.figma.com/make/) |

## 今天只做这些

不熟 Figma 时按天切开。

| 天 | 做 | 出口 |
| --- | --- | --- |
| 1 | Step A → B → `design-review.md` → `AGENTS.md` 骨架。0 Make | 两页 8 态文案齐 |
| 2 | Step C → D（一次一个组件） | 冻结点 F1；人确认原生 `<button>` |
| 3 | Step E：Plan → 壳 + `/approvals/default`；另条加 loading、empty | 能勾选 3 行看到「批量审批（3）」 |
| 4 | Step F：Dialog、其余状态、`/orders/default`；缺组件走 G | 无擅自新建组件 |
| 5 | Step H：每态 Copy design → 人精修 | 冻结点 F2 |
| 6 | Step I 验证 MCP → Step J 先计划后写码 → Step K 按视觉单修 | 生产代码不来自 Make zip |

## 相关文档

- [原型先行全流程](prototype-first-workflow.md)（路径 A / 路径 B 入口）
- [PRD 到原型](../06-engineering-workflow/prd-to-prototype.md)
- [Figma 体系](figma-stack.md)
- [Prompt 与上下文](prompting-and-context.md)
- [原型到代码](../06-engineering-workflow/prototype-to-code.md)
- [视觉评审闭环](visual-review-loop.md)
- [UI Brief](../templates/ui-brief.md) · [页面清单](../templates/page-inventory.md) · [组件清单](../templates/component-inventory.md)
