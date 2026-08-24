# 原型先行全流程实操

这是一条手把手教学路线：从竞品拆解出发，用 Figma Make 生成原型，人工评审后反写 PRD，再通过 Figma MCP 交给本地 Coding Agent 生成代码。它和 [PRD 到原型](../06-engineering-workflow/prd-to-prototype.md) 的区别是顺序：PRD 是已验证原型的"记录"，不是设计的"前置输入"。

适用判断：

| 场景 | 是否用本流程 |
| --- | --- |
| 需求不确定、要快速验证交互 | 用 |
| 有设计师协作、需要可评审的视觉基准 | 用 |
| 强合规、需 PRD 签字后才能投入设计 | 不用，走 [工程工作流](../06-engineering-workflow/README.md) |
| 一次性 MVP、不追求视觉可控 | 不用，PRD 直接给 v0/Lovable，见 [工具矩阵](../07-tools/tool-matrix.md) |

Demo 案例：仓库贯穿案例「订单审批工作台」中的审批队列页 `/approvals`。跑通这一页，其余页面同理。

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

## 第 0 步：准备（15 分钟）

需要：Figma 账号（[Figma Make](https://www.figma.com/make/)，Make 和 Dev Mode MCP 需要付费席位，以官方为准）、[Figma 桌面端](https://www.figma.com/downloads/)（MCP server 只在桌面端运行）、本地 Coding Agent（Claude Code 或 Cursor）。

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

1. 打开 [figma.com/make](https://www.figma.com/make/)，新建一个 Make 项目（具体界面以官方为准）。
2. 粘贴下面的启动 Prompt（内容来自你的四件套，不要只写一句话）。
3. 生成后先预览主流程，再逐条要求补状态，不要指望一次生成全部。

可复制启动 Prompt（Demo 版）：

```text
为企业订单系统做「审批队列 /approvals」高保真原型。

角色与目标：主管筛选待审批订单，比较风险后批量批准或驳回。
页面结构：
- 顶部：标题"审批队列" + 待处理数量；右侧主按钮"批量审批（N）"，常显选中数。
- 筛选栏：状态、客户、日期范围；显示已选筛选条件数。
- 主体：订单表格（订单号、客户、金额、状态、更新时间、操作）；手机端变摘要卡片列表。
- 分页 + 每页数量。
必须生成的状态（每个单独一屏）：默认、加载（骨架屏）、空数据（引导文案+入口）、
无结果（给清除筛选动作）、错误（可重试）、无权限（只读说明）、成功、部分失败（逐条说明失败原因）。
约束：危险操作（驳回）弹确认框并要求填理由；只使用给定文案，不造新数据；
桌面 1440 宽优先，附 375 宽手机版。先输出页面清单确认，再生成页面。
```

可复制迭代 Prompt（一次只改一件事）：

```text
保持其他页面和布局不变。只修改空数据状态：
标题改为"暂无待审批订单"，副文案"新任务会出现在这里"，
提供"查看已审批"次级链接。主按钮在此状态下禁用。
```

产出与检查：原型覆盖状态矩阵里每个状态。检查：逐状态点一遍；长文案（客户名 20 字）不溢出；驳回流程能走完并回到列表。

## 第 5 步：人工评审与整理（时间盒 1 小时）

做什么：这一步决定第 7 步代码生成的精度，不能省。

怎么做：

1. 每个 state 截一张图，贴进 `design-review.md`，先评主任务、信息层级、危险操作，再评颜色。
2. 结论写"已确认决策 / 被拒绝方案"，未通过退回第 4 步迭代。
3. 把定稿原型转为可编辑的 Figma Design 文件，然后整理（MCP 读的就是这份结构）：
   - Frame 命名 = 路由 + 状态，如 `/approvals/loading`、`/approvals/empty`；
   - 布局用 Auto Layout，不许绝对定位裸摆；
   - 重复元素抽成 Component，颜色/间距存为变量（对应 [Design Token](../04-design-system/tokens.md)）。

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

1. Figma 桌面端登录同一账号，在设置里启用 Dev Mode MCP Server（需 Dev/Full 席位；入口和端点以 [Figma 官方 MCP 文档](https://www.figma.com/mcp-cc-ai-code/) 为准，默认监听本地 127.0.0.1）。
2. 把本地端点注册进 Coding Agent，例如 Claude Code（命令与端点路径以官方文档为准）：
   ```bash
   claude mcp add --transport http figma-dev-mode http://127.0.0.1:3845/mcp
   ```
   Cursor 则在 `~/.cursor/mcp.json` 的 `mcpServers` 里加同名 URL 条目。
3. 项目已有组件库时配置 [Code Connect](https://www.figma.com/developers/code-connect)：把设计里的组件映射到真实代码组件，MCP 才会返回"用你的 `OrderTable`"而不是让 Agent 重写一个。
4. 在 Figma 里右键目标 Frame → Copy link to selection，把链接交给 Agent。

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

全程约一个工作日（Demo 单页）。多页面时，第 1-3 步一次做完，第 4 步之后按页循环。技术选型和工具边界见 [工具矩阵](../07-tools/tool-matrix.md)。
