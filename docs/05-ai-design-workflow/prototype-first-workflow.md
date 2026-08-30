# 原型先行全流程实操

这是一条手把手教学路线：从竞品拆解出发，用 Figma Make 生成原型，人工评审后反写 PRD，再通过 Figma MCP 交给本地 Coding Agent 生成代码。它和 [PRD 到原型](../06-engineering-workflow/prd-to-prototype.md) 的区别是顺序：路径 A 里 PRD 是已验证原型的"记录"，不是设计的"前置输入"。需求已有完备 PRD 时走路径 B，不要把本文改成只剩 PRD 先行。

适用判断：

| 场景 | 是否用本流程 |
| --- | --- |
| 需求不确定、要快速验证交互 | 用 |
| 有设计师协作、需要可评审的视觉基准 | 用 |
| 强合规、需 PRD 签字后才能投入设计 | 不用，走 [工程工作流](../06-engineering-workflow/README.md) |
| 一次性 MVP、不追求视觉可控 | 不用，PRD 直接给 v0/Lovable，见 [工具矩阵](../07-tools/tool-matrix.md) |
| 已有完善 PRD、要用 Make 做高保真并落地代码 | 用路径 B，详见下文与 [Figma Make 高保真保姆级教程](figma-make-high-fidelity.md) |

Demo 案例：仓库贯穿案例「订单审批工作台」中的审批队列页 `/approvals`。跑通这一页，其余页面同理。

## 两条路径

- **路径 A**：需求不确定，走本文第 1–8 步（竞品拆解 → Make 原型 → 反写 PRD → MCP 落地）。PRD 是已验证原型的记录，不是设计的前置输入。
- **路径 B**：PRD 已完备，跳过探索性竞品定稿，从四件套 + 壳层 + 冻组件开始。操作逐步看 [Figma Make 高保真保姆级教程](figma-make-high-fidelity.md)；工程 SOP 见 [PRD 到原型](../06-engineering-workflow/prd-to-prototype.md)。

## 全景图

```text
① 竞品分析拆解 → ② 业务建模 → ③ 交互设计
      ↓ 产出：UI Brief + 页面清单 + 组件清单 + 状态矩阵（Make 的输入）
④ Figma Make 生成原型 + ⑤ 人工评审（覆盖全部状态）
      ↓
⑥ PRD 反写（AI 起草 + 人工定稿）
      ↓
⑦ Figma MCP + Code Connect → 本地 Coding Agent 生成代码
      ↓
⑧ 截图验收闭环
```

上图是路径 A。路径 B 从四件套进入，不经过①–③的探索性定稿，也不做⑥反写 PRD。

## 路径 B：PRD 已完备的高保真做法

人拥有契约（组件清单、Token、命名、状态矩阵）；AI 只在冻结契约内执行。逐步操作、可复制 Prompt、契约模板见 [Figma Make 高保真保姆级教程](figma-make-high-fidelity.md) Step A–K。工程入口见 [PRD 到原型](../06-engineering-workflow/prd-to-prototype.md)。

三个问题对应三个解法，不要弱化：

| # | 问题 | 解法 | 禁止 |
| --- | --- | --- | --- |
| 1 | PRD 太长一次生成会失真 | 先壳层 + 基本功能，再逐页、逐状态细化。Make 官方也要求 layout first、frame by frame、plan mode | 整份 PRD 一次生成整站 |
| 2 | 页面组件不规范 | 组件库先行并**人冻结**；缺组件必须提案、人批准后才入库；后续靠改组件保持一致 | 把「有则复用无则新建」交给 AI；「全局抽取组件并改所有引用」 |
| 3 | Make 文字传不了视觉 | Make 只验证交互；[Copy design](https://help.figma.com/hc/en-us/articles/35060759685015-Copy-a-Figma-Make-preview-as-design-layers) 把当前 preview 贴进 Design（单向快照，不自动绑设计系统、不可交互、不回写 Make）；人做 Auto Layout / 语义命名 / 组件实例 / Variables；MCP 读精修 Frame（选区链接含 node-id） | 把 Make 当生产；截图当间距来源；Copy design 当双向同步 |

Make 产出 = 验证用 code-backed 原型，**禁止当生产代码**。MCP `get_design_context` 是 React+Tailwind **中间表示**，要翻译进本仓库组件 + Token。无 [Code Connect](https://developers.figma.com/docs/code-connect/)（Org/Enterprise + Dev/Full）时，Agent 会发明长得像的 div，必须靠契约钉死。Make「改本地仓库」是封闭 beta，不是主路径。已有组件 npm 包时优先 [Make kits](https://help.figma.com/hc/en-us/articles/39241689698839-Get-started-with-Make-kits) + `guidelines.md`，不是必须。

「功能 demo 最后再 UI」适合交互未定（路径 A）。PRD 已定要高保真走 Make。推荐混合：骨架 ≈ 可点 demo（用已冻组件默认外观），精修放在组件冻结之后。

推荐流水线：

```text
契约冻结（四件套 + 组件契约 + AGENTS.md）
  → Make 骨架（Plan：壳 + /approvals 默认态）
  → 组件库人冻结（F1）
  → 逐页细化（一次一页、一次一态；缺组件走入库审批）
  → Copy design 精修（F2）
  → MCP 小批次落地（先计划后写码）
  → 验收
```

| 阶段 | 人做 | AI 做 | 禁止 AI | 出口门禁 |
| --- | --- | --- | --- | --- |
| 四件套 A | 定范围、批权限矩阵 | 从 PRD 填 Brief/清单/8 态 | 生成界面 | 路由锁死；8 态有原文案 |
| 灰度 B | 走查主任务 | 画纯文本线框 | 定色、进 Make | 空 ≠ 无结果；批量按钮带数量 |
| 壳层 C | 批准 DOM/类名 | 写 AppShell 契约 | 顺带做表格 | 内容槽为空 |
| 冻组件 D | **人冻结** F1；IDE 看 diff | 按批准名单一次一个组件 | 自行新建；全局抽取 | 契约已链进 `AGENTS.md` |
| Make E/F | 点预览走主流程 | 壳 + 默认态，再逐态 | 生成整站 | Make 代码未进生产 git |
| 入库 G | 书面批准或驳回 | 只提案，批准后才实现 | 页面里先做临时控件 | inventory 有新行 |
| 精修 H | Auto Layout / 命名 / 实例 / Variables | 只出检查单 | 未整理就 MCP | Frame = 路由 + 状态 |
| MCP I–K | 确认计划；IDE 底线 | 读选区链接；翻译进库存组件 | 把 Tailwind 中间表示当生产 | 生产代码不来自 Make zip |

Frame 命名 = 路由 + 状态，如 `/approvals/loading`。8 态：默认、加载、空数据、无结果、错误、无权限、成功、部分失败。一次一事；Prompt 必须有「禁止修改」；换页 = 新会话；未冻结组件库禁止多窗口并行。新任务先读 `AGENTS.md` 与每组件契约 md（模板见保姆级教程）。

对应保姆级教程：A 四件套 → B 灰度 → C 壳层 → D 冻组件 → E/F Make → G 入库 → H Copy design → I–K MCP 与验收。

| MCP | 端点 | 何时用 |
| --- | --- | --- |
| Remote（推荐） | `https://mcp.figma.com/mcp` | 默认。Cursor `/add-plugin figma`。看不到画布选区，必须 Copy link to selection |
| Desktop（可选） | `http://127.0.0.1:3845/mcp` | 特定企业内网。须开桌面端 Dev Mode |

路径 B 第一次进 Make 用下面这条，不要把整份 PRD 丢进去：

```text
这是验证用 code-backed 原型，不是生产代码。先出 Plan。
本轮只做 AppShell + /approvals 默认态。
本轮不做：其余 7 态、/orders 列表、设置页。
组件名对照 docs/component-inventory.md，禁止自行新建。禁止修改已冻结契约。
```

缺组件时 AI 只许提案：

```text
现有组件已冻结，不得自行新建。判断能否用现有组件完成当前缺口。
输出二选一，不要写代码：A 复用某某；B 申请入库某某（必须写出现有组件做不到的点）。
禁止修改任何文件。
```

和路径 A 的关系：第 4–5、7–8 步（Make、Copy design、MCP、验收）两边共用，只是路径 B 用四件套+冻库替换第 1–3 步和第 6 步反写 PRD。多页面时四件套+冻库一次做完，Make 之后按页循环。

路径 B 走完一页的出口：

- [ ] 组件清单已冻，`AGENTS.md` 已链接契约
- [ ] `/approvals` 至少覆盖默认 + 加载 + 空 + 无结果 + 错误 + 无权限 + 一条成功或部分失败
- [ ] Design Frame 名 = 路由 + 状态，已 Auto Layout，页面上是组件实例
- [ ] 生产代码来自 MCP 读精修 Frame，不是 Make zip，也不是截图像素还原
- [ ] 人用 IDE 看过 diff：无同义组件、无硬编码色、无页面私有表格 CSS

## 第 0 步：准备（15 分钟）

需要：Figma 账号（[Figma Make](https://www.figma.com/make/)，Make、Copy design、MCP、Code Connect 的席位以官方为准）、本地 Coding Agent（Claude Code 或 Cursor）。推荐 **Remote MCP** `https://mcp.figma.com/mcp`（Cursor 可用 `/add-plugin figma` 或 `mcp.json`）。[Figma 桌面端](https://www.figma.com/downloads/)用于 Design 精修；Desktop MCP `http://127.0.0.1:3845/mcp` 仅特定企业场景。安装以 [Remote 安装](https://developers.figma.com/docs/figma-mcp-server/remote-server-installation/) 与 [MCP Guide](https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server) 为准。

先把四份模板复制到项目目录并建好空文件：

```text
docs/
  ui-brief.md          ← 复制 [UI Brief 模板](../templates/ui-brief.md)
  page-inventory.md    ← 复制 [页面清单模板](../templates/page-inventory.md)
  component-inventory.md ← 复制 [组件清单模板](../templates/component-inventory.md)
  design-review.md     ← 复制 [设计评审记录模板](../templates/design-review.md)
```

Prompt 通用写法见 [Prompt 与上下文](prompting-and-context.md)：每轮都写清角色、任务、约束、输出、禁止修改和验收。

## 第 1 步：竞品分析拆解（时间盒 2 小时）

做什么：选 2-3 个竞品，各走一遍和你要做的任务相同的流程，记录"它怎么做"，再提炼"我借鉴什么"。先用 AI 提效，不靠 AI 定结论。

怎么做：

1. 每个竞品截图 3-5 张：任务入口、主列表页、关键操作、异常提示。
2. 把截图喂给任意 AI 对话工具，跑下面的 Prompt。
3. 人工裁决每一行：借鉴、避免、不适用（结合自己用户，见 [Agent 协作](agent-collaboration.md) 的人机边界）。

可复制 Prompt：

```text
你是产品分析师。这是竞品 X 的审批队列页面截图（按顺序：入口、列表、批量操作、空态）。
请输出 Markdown 表格，逐屏描述：
1. 页面结构和信息层级；2. 主操作和次操作的位置；
3. 状态覆盖（默认/加载/空/错误/无权限）；4. 危险操作如何防误触；
5. 值得借鉴的 3 点和可疑的 2 点（说明理由）。
不要建议加新功能；最后列出截图里看不出来、需要我补充的信息。
```

产出与检查：每个竞品一张拆解表，汇成一列"借鉴/避免"清单。检查标准：每条结论都能指到某张截图，说不出依据的删掉。

Demo 结果示例：竞品 A 把批量审批放筛选栏右侧并常显选中数（借鉴）；竞品 B 审批按钮藏在每行"更多"菜单（避免：批量任务变慢）。

## 第 2 步：业务建模（时间盒 1 小时）

做什么：把竞品结论 + 业务输入改写成五列模型，这是 [UI Brief](../templates/ui-brief.md) 的骨架。

可复制 Prompt：

```text
你是企业 SaaS 产品设计师。根据以下输入输出业务模型：
输入：[粘贴竞品拆解结论 + 业务方原始描述]
输出 Markdown 五列表：角色 | 对象 | 高频任务 | 风险任务 | 完成条件。
补充：每个风险任务的入口、前置条件、成功反馈、失败恢复。
权限不足按一种页面状态设计，不算异常分支。
不要新增输入里没有提到的业务能力；最后列出 5 个需要产品确认的问题。
```

产出与检查：填好 `ui-brief.md` 的"目标、角色与权限、对象与主任务"三节。检查：每个高频任务都有入口和完成条件；每个风险任务都有失败恢复。

Demo 结果示例：主管批量审批订单；风险任务 = 驳回（需理由，逐条可恢复）；完成条件 = 状态更新 + 审计记录。

## 第 3 步：交互设计（时间盒 2 小时）

做什么：产出 Make 需要的另外三份输入——页面清单、状态矩阵、组件清单。

怎么做：

1. 用第 2 步模型填 `page-inventory.md`（路由即未来代码路由，如 `/approvals`）。
2. 用下面的 Prompt 生成状态矩阵，贴进 UI Brief 的"页面状态"节。
3. 对照 [组件清单模板](../templates/component-inventory.md) 已填示例，列出本页组件。
4. 手画灰度线框（纯文本即可，方法见 [PRD 到原型](../06-engineering-workflow/prd-to-prototype.md)），先定容器和信息层级，不碰颜色。

可复制 Prompt（状态矩阵）：

```text
针对页面 /approvals（审批队列）输出状态矩阵。
每行一个状态：默认、加载、空数据、无结果、错误、无权限、成功、部分失败。
每列写：用户看到什么 | 能做什么 | 不能做什么。
不要新增业务状态；文字要能直接用于界面（真实长度，不写"这里显示错误"）。
```

产出与检查：`page-inventory.md`、`component-inventory.md`、状态矩阵、灰度线框四件套齐全。检查：空态和错误态都写了具体文案；每个组件在清单里有状态和键盘行为。

## 第 4 步：Figma Make 生成原型（时间盒 2 小时）

做什么：把四件套变成可交互原型。Make 的产出是 code-backed 原型，验证用，不直接当生产代码（见 [Figma 体系](figma-stack.md)）。

怎么做：

1. 打开 [figma.com/make](https://www.figma.com/make/)，新建一个 Make 项目（具体界面以官方为准）。复杂任务先开 **Plan mode**（入口以 [Use plan mode](https://help.figma.com/hc/en-us/articles/40830441709719-Use-plan-mode-in-Figma-Make) 为准）。
2. 一次只给 1–2 个 frame。第一次只做壳层 + `/approvals` 默认态，**禁止整份 PRD 一次生成整站**。已有组件 npm 包时优先用 [Make kits](https://help.figma.com/hc/en-us/articles/39241689698839-Get-started-with-Make-kits)，不是必须。
3. 粘贴下面的启动 Prompt（内容来自你的四件套，不要只写一句话）。后续一次一事迭代，每条写「禁止修改」；对话漂了就清上下文。
4. 生成后先预览主流程，再逐条补状态。8 态是覆盖目标，不是一次生成的范围。Make 只验证交互，产出禁止当生产代码。

可复制启动 Prompt（Demo 版，第一次只要壳 + 默认态）：

```text
为企业订单系统做「审批队列 /approvals」验证用原型（不是生产代码）。先出 Plan，不要直接生成整站。

本轮只做：AppShell（侧栏+顶栏+内容槽）+ /approvals 默认态。
角色与目标：主管筛选待审批订单，比较风险后批量批准或驳回。
页面结构：
- 顶部：标题"审批队列" + 待处理数量；右侧主按钮"批量审批（N）"，常显选中数。
- 筛选栏：状态、客户、日期范围；显示已选筛选条件数。
- 主体：订单表格（订单号、客户、金额、状态、更新时间、操作）；手机端变摘要卡片列表。
- 分页 + 每页数量。
本轮不做：加载/空数据/无结果/错误/无权限/成功/部分失败、/orders 列表、设置页。
约束：危险操作（驳回）弹确认框并要求填理由；只使用给定文案，不造新数据；
桌面 1440 宽优先。组件名对照组件清单，禁止自行新建同义组件。
```

可复制迭代 Prompt（一次只改一件事）：

```text
保持其他页面和布局不变。只修改空数据状态：
标题改为"暂无待审批订单"，副文案"新任务会出现在这里"，
提供"查看已审批"次级链接。主按钮在此状态下禁用。
```

产出与检查：原型最终覆盖状态矩阵里每个状态（靠迭代，不是一次生成）。检查：逐状态点一遍；长文案（客户名 20 字）不溢出；驳回流程能走完并回到列表。

## 第 5 步：人工评审与整理（时间盒 1 小时）

做什么：这一步决定第 7 步代码生成的精度，不能省。

怎么做：

1. 每个 state 截一张图，贴进 `design-review.md`，先评主任务、信息层级、危险操作，再评颜色。
2. 结论写"已确认决策 / 被拒绝方案"，未通过退回第 4 步迭代。
3. 用官方 **Copy design** 把当前 preview 贴进 Figma Design（单向快照：不自动绑设计系统、不可交互、不回写 Make）。每个状态、每个关键 Dialog 各 Copy 一次。入口以 [Copy a Figma Make preview as design layers](https://help.figma.com/hc/en-us/articles/35060759685015-Copy-a-Figma-Make-preview-as-design-layers) 为准。然后**人**整理（MCP 读的就是这份结构，不要未整理就 MCP）：
   - Frame 命名 = 路由 + 状态，如 `/approvals/loading`、`/approvals/empty`；
   - 布局用 Auto Layout，不许绝对定位裸摆；
   - 重复元素做成 Component，页面上是实例，不要 detach；
   - 颜色/间距存为 Variables（对应 [Design Token](../04-design-system/tokens.md)）；
   - 删隐藏层和无意义嵌套；长文案用真实长度。
   截图只做回归，不当间距来源。Make「改本地仓库」是封闭 beta，不是主路径。

产出与检查：评审记录有结论；设计文件里找不到未命名 Frame（Layer 面板逐个看）。这些对应 [原型到代码](../06-engineering-workflow/prototype-to-code.md) 列出的常见返工源。

## 第 6 步：PRD 反写（时间盒 1 小时）

做什么：从已验证原型 + 评审记录生成 PRD 草稿，再人工定稿。写的是验证过的决策，比拍脑袋的前置 PRD 准确。

可复制 Prompt：

```text
你是产品经理。根据以下材料起草 /approvals 页面 PRD：
材料：[粘贴/附上] 原型各状态截图、设计评审记录（已确认决策+被拒方案）、UI Brief、状态矩阵。
输出章节：背景与目标、角色与权限、页面与路由清单、每页状态说明、
交互与异常流、埋点事件、验收标准、开放问题。
约束：不引入截图和评审记录里没有的行为；被拒绝的方案写入"明确不做"；
每个验收标准可测试（写明前置条件和预期结果）。
```

人工定稿检查：权限矩阵和风险任务与业务方确认过；验收标准可执行；"明确不做"一节保留（防止范围蔓延）。

## 第 7 步：Figma MCP + Code Connect → Coding Agent（配置 1 小时）

做什么：让本地 Coding Agent 读取设计文件的结构化细节（Frame、组件、变量），而不是看截图猜。

怎么做：

1. 推荐 **Remote MCP**：端点 `https://mcp.figma.com/mcp`。Cursor 用 `/add-plugin figma` 或在 `mcp.json` 的 `mcpServers` 写入该 URL；Claude Code 用官方 plugin / `mcp add`（命令以 [Remote 安装](https://developers.figma.com/docs/figma-mcp-server/remote-server-installation/) 为准），例如：
   ```bash
   claude mcp add --transport http figma https://mcp.figma.com/mcp
   ```
   远程 MCP **必须 Copy link to selection**（链接含 node-id），看不到画布选区。席位与能力以 [MCP Guide](https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server) 为准。
2. **Desktop MCP** 可选：Figma 桌面端 Dev Mode 启用本地服务 `http://127.0.0.1:3845/mcp`（Dev/Full 席位，特定企业内网再用）。注册示例：
   ```bash
   claude mcp add --transport http figma-desktop http://127.0.0.1:3845/mcp
   ```
3. 项目已有组件库时配置 [Code Connect](https://developers.figma.com/docs/code-connect/)（Org/Enterprise + Dev/Full）：把设计组件钉到真实代码 import。无映射时 Agent 会发明长得像的 div。
4. 在 Figma 里右键目标 Frame → Copy link to selection，把链接交给 Agent。一次一个 Frame，不要整页丢给 `get_design_context`。MCP 返回的 React+Tailwind 是中间表示，必须翻译进本仓库组件和 Token。

可复制 Coding Agent Prompt：

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

产出与检查：Agent 先给计划再动手；生成的组件名和组件清单一一对应；没有出现临时颜色。人工必须确认的部分见 [原型到代码](../06-engineering-workflow/prototype-to-code.md) 的边界清单（权限、危险操作、键盘焦点、响应式）。

## 第 8 步：验收闭环（时间盒 1 小时）

用 fixture 渲染全部状态，固定视口截图（方法见 [视觉评审闭环](visual-review-loop.md)），对照 PRD 验收标准逐条勾选，问题记录进 [视觉验收记录](../templates/visual-acceptance.md)，最后过一遍 [交付验收清单](../06-engineering-workflow/acceptance-checklist.md)。截图与设计稿不一致时，先判断是代码问题还是设计问题，回到对应步骤，不整页重新生成。

## 常见坑

| 坑 | 后果 | 对策 |
| --- | --- | --- |
| 跳过竞品拆解和建模直接生成 | 原型好看但业务权限和异常流全是错的 | 第 1-3 步不许省 |
| 只生成"正常态" | 开发时才发现空态、错误态没有位置 | 状态矩阵作为 Make 输入的一部分 |
| Make 原型代码直接进生产 | 无测试、无权限校验、依赖不可控 | 原型验证完就丢，代码从第 7 步重新生成 |
| 设计文件 Frame 未命名 | MCP 返回的上下文无法映射路由和组件 | 第 5 步的命名规则 = 路由 + 状态 |
| 一次 Prompt 让 Agent 生成所有页面 | 单轮质量下降且难回滚 | 一页一任务，先计划后写码 |
| AI 自称复用实际复制 | 每页私货，改一处其它页不变 | 人冻结组件库；缺组件走提案审批；对照 DOM 契约 |
| 参照某页布局错 | `/orders` 做成详情卡片 | 只贴目标 Frame 链接，禁止「参考某页」 |
| 全局抽取失败 | 半成品 DOM 分叉 | 禁止「全局抽取组件并改所有引用」 |
| 多窗口未冻库 | 两套按钮、两套间距 | 未冻结组件库禁止并行 |
| Copy design 当双向同步 | Design 改了 Make 不会变 | 单向快照；Make 只作交互证据 |
| 把 MCP Tailwind 当生产代码 | 仓库出现一次性 div + 杂类 | 翻译进库存组件和 Token；无 Code Connect 更要钉契约 |
| 整页丢给 get_design_context | 读错节点、上下文爆 | 一次一个 Frame，必须 Copy link to selection |

全程约一个工作日（Demo 单页）。多页面时，第 1–3 步（路径 A）或四件套+冻库（路径 B）一次做完，Make 之后按页循环。技术选型和工具边界见 [工具矩阵](../07-tools/tool-matrix.md)。
