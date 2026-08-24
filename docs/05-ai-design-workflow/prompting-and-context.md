# Prompt 与上下文工程

AI 结果的稳定性主要取决于上下文是否完整。**上下文工程**（Context Engineering）是企业级 AI 工作流的核心能力：将业务知识、设计规范、技术约束结构化为 AI 可理解的输入。

## 核心原则

1. **上下文 > Prompt**：90% 的质量来自完整的上下文（Brief、Token、清单），10% 来自 Prompt 技巧
2. **版本化**：上下文文件与代码一起进入 Git，不是每次重新粘贴
3. **分层管理**：稳定的规则放仓库，易变的细节放任务描述
4. **可复现**：同样的上下文 + Prompt，不同人、不同时间得到一致的结果
5. **可审计**：每次 AI 交互都记录输入（Prompt + 上下文文件）和输出

## Prompt 基础结构（CRAFT 框架）

每个有效的 Prompt 都包含 5 个要素，用助记词 **CRAFT** 记忆：

```text
C - Context（上下文）：AI 需要知道什么背景信息？
R - Role（角色）：AI 应该以什么身份思考？
A - Action（任务）：AI 要完成什么具体工作？
F - Format（格式）：输出应该是什么结构？
T - Test（验收）：怎么判断输出是否合格？
```

### 标准模板

```markdown
## Context（上下文）
项目：企业订单管理系统
用户：内部运营人员（非技术背景）
当前阶段：G5 开发实现
相关文档：@docs/ui-brief.md, @docs/component-inventory.md, @src/tokens.css

## Role（角色）
你是一位有 10 年经验的前端工程师，熟悉 React + TypeScript + Tailwind CSS，
专注于企业内部工具开发，重视可维护性和无障碍性。

## Action（任务）
实现审批队列页面（/approvals）的默认状态和空数据状态。
- 使用 docs/ui-brief.md 中定义的业务逻辑
- 复用 component-inventory.md 中列出的 OrderTable 和 FilterBar 组件
- 只使用 tokens.css 中定义的颜色和间距，不创建新 Token

## Format（输出格式）
1. 先输出实现计划（3-5 个步骤）
2. 列出将修改的文件和新增的文件
3. 等我确认后，再输出完整代码
4. 每个文件用 Markdown 代码块，标注文件路径

## Test（验收标准）
- [ ] 代码通过 ESLint 和 TypeScript 检查
- [ ] 默认状态显示 20 条订单，支持筛选和分页
- [ ] 空数据状态显示引导文案"暂无待审批订单"和次级操作
- [ ] 键盘可通过 Tab 导航所有交互元素
- [ ] 没有硬编码颜色（#hex 或 rgb）

## Constraints（约束，不能改变的部分）
- 不修改 OrderTable 组件的 props 接口
- 不添加新的 npm 依赖
- 路由结构保持 /approvals/:tab 格式
- 数据先用 fixture，不连接真实 API
```

### CRAFT 应用示例

**场景 1：产品分析**

```markdown
## Context
竞品：Salesforce Approval Center 的截图（已上传）
我们的目标：为中小企业简化审批流程

## Role
产品分析师，专注于 B2B SaaS 的用户体验

## Action
从截图中提取：
1. 信息架构（页面分区、导航结构）
2. 主操作和次操作的位置
3. 状态覆盖（默认/空/错误/加载）
4. 3 个值得借鉴的设计点
5. 2 个不适合我们的点（说明理由）

## Format
Markdown 表格，每行一个发现

## Test
- [ ] 每个结论都能指到截图的具体区域
- [ ] "不适合"的理由考虑了我们的用户特点（中小企业）
- [ ] 列出了我需要补充的信息（截图看不出的部分）
```

**场景 2：代码修复**

```markdown
## Context
Bug: 审批队列页面在移动端（390px）下，批量操作按钮被遮挡
相关文件：src/pages/ApprovalQueue.tsx (已读取)
视觉验收记录：docs/visual-acceptance.md 第 3 条

## Role
前端工程师，擅长响应式布局

## Action
只修复移动端布局问题，保持其他视口不变

## Format
1. 先说明根因（为什么会被遮挡）
2. 提出修复方案（最小改动）
3. 输出 git diff 格式的代码变更
4. 说明如何验证（复现步骤）

## Test
- [ ] 390px 下批量操作按钮完全可见且可点击
- [ ] 1440px 和 768px 视口无变化
- [ ] 没有引入新的布局问题

## Constraints
- 不修改 Tailwind 配置
- 不改变按钮的视觉样式（颜色、间距）
- 保持按钮文本不换行
```

### 常见错误

| 错误 Prompt | 问题 | 正确做法 |
| --- | --- | --- |
| "帮我设计一个表格" | 过于宽泛，AI 不知道什么业务 | 提供业务上下文、字段清单、状态要求 |
| "用红色表示错误" | 硬编码颜色 | "使用 `var(--color-error)` 表示错误" |
| "做成 Airbnb 那样" | 主观且不可执行 | 上传截图或描述具体特征（如"卡片带阴影，圆角 8px"） |
| "尽量完善" | 无边界，AI 会过度设计 | 明确"只实现默认态和错误态，其他状态后续迭代" |
| "参考我之前说的" | AI 可能忘记或理解错误 | 重新粘贴关键上下文或引用文件 |

## 上下文分层架构

不要在每次对话中重复粘贴相同的规则。按照变化频率分层管理上下文：

```text
第 0 层：通用规则（几乎不变）
  ↓ 存储在：项目根目录 CLAUDE.md / .cursorrules
  ↓ 内容：技术栈、代码规范、禁止项、通用约束
  ↓ 加载方式：工具自动读取

第 1 层：设计系统（季度更新）
  ↓ 存储在：docs/design-system/ 或 src/tokens.*
  ↓ 内容：Design Token、组件清单、命名规范
  ↓ 加载方式：通过 Figma MCP 或文件引用

第 2 层：项目上下文（项目开始时确定）
  ↓ 存储在：docs/ 目录
  ↓ 内容：UI Brief、页面清单、API 契约、状态矩阵
  ↓ 加载方式：在 Prompt 中 @引用

第 3 层：任务上下文（每次任务不同）
  ↓ 存储在：Prompt 本身
  ↓ 内容：具体页面、要修复的 Bug、当前阶段
  ↓ 加载方式：直接写在 Prompt 中

第 4 层：实时上下文（动态）
  ↓ 存储在：当前对话
  ↓ 内容：刚生成的代码、刚运行的测试结果
  ↓ 加载方式：工具自动追踪
```

### 第 0 层：通用规则文件

**示例：`CLAUDE.md`**（放在项目根目录）

```markdown
# AI 开发规则

## 技术栈
- React 18 + TypeScript 5
- Tailwind CSS（Utility-First）
- React Router 6（文件路由）
- Tanstack Query（数据获取）
- Vitest + Testing Library（测试）

## 代码规范

### 禁止项
- ❌ 内联样式（`style={{ ... }}`）
- ❌ 硬编码颜色（`#hex` 或 `rgb()`）
- ❌ `any` 类型（除非有注释说明原因）
- ❌ `console.log`（使用 logger）
- ❌ 绝对定位布局（`absolute`，除非必需）

### 必须项
- ✅ 所有颜色和间距使用 Token（`var(--color-*)`, `var(--spacing-*)`）
- ✅ 组件优先复用（新建前检查 docs/component-inventory.md）
- ✅ 交互元素有 aria-label
- ✅ 表单有完整的错误处理（前端校验 + 后端错误显示）
- ✅ 加载和错误状态明确（不显示空白）

## 组件模式

### 数据获取组件
```tsx
// 标准模式：使用 Tanstack Query
export function OrderList() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['orders'],
    queryFn: fetchOrders
  })

  if (isLoading) return <LoadingState />
  if (error) return <ErrorState error={error} onRetry={refetch} />
  if (!data?.length) return <EmptyState />

  return <OrderTable data={data} />
}
```

### 表单组件
```tsx
// 使用 React Hook Form + Zod
const schema = z.object({
  email: z.string().email('请输入有效的邮箱'),
  password: z.string().min(8, '密码至少 8 位')
})

export function LoginForm() {
  const { register, handleSubmit, formState: { errors } } = useForm({
    resolver: zodResolver(schema)
  })
  // ...
}
```

## 文件结构
```
src/
  components/       # 可复用组件
    Button/
      Button.tsx
      Button.test.tsx
      Button.stories.tsx
  pages/            # 页面组件
    ApprovalQueue/
      ApprovalQueue.tsx
      ApprovalQueue.test.tsx
  hooks/            # 自定义 Hooks
  utils/            # 工具函数
  tokens.css        # Design Token
```

## 测试要求
- 每个组件有基础测试（渲染、交互）
- 每个页面有状态测试（默认/加载/空/错误）
- 关键业务逻辑覆盖率 > 90%

## AI 工作约定
1. 先输出计划，等确认后再写代码
2. 一次只改一件事（不在修 Bug 时顺便重构）
3. 修改代码后说明修改原因和影响范围
4. 遇到不确定的业务逻辑，明确提问而不是猜测
```

**Claude Code 会自动读取此文件**，你不需要每次粘贴。

### 第 1 层：Design Token 文件

**示例：`src/tokens.css`**

```css
:root {
  /* Colors - Semantic */
  --color-primary: #0066FF;
  --color-secondary: #6B7280;
  --color-success: #10B981;
  --color-warning: #F59E0B;
  --color-error: #EF4444;
  --color-info: #3B82F6;

  /* Colors - Neutral */
  --color-gray-50: #F9FAFB;
  --color-gray-100: #F3F4F6;
  --color-gray-900: #111827;

  /* Spacing */
  --spacing-xs: 0.25rem;   /* 4px */
  --spacing-sm: 0.5rem;    /* 8px */
  --spacing-md: 1rem;      /* 16px */
  --spacing-lg: 1.5rem;    /* 24px */
  --spacing-xl: 2rem;      /* 32px */
  --spacing-2xl: 3rem;     /* 48px */

  /* Typography */
  --font-size-xs: 0.75rem;    /* 12px */
  --font-size-sm: 0.875rem;   /* 14px */
  --font-size-base: 1rem;     /* 16px */
  --font-size-lg: 1.125rem;   /* 18px */
  --font-size-xl: 1.25rem;    /* 20px */
  --font-size-2xl: 1.5rem;    /* 24px */

  /* Border Radius */
  --radius-sm: 0.25rem;   /* 4px */
  --radius-md: 0.5rem;    /* 8px */
  --radius-lg: 0.75rem;   /* 12px */

  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);

  /* Z-index */
  --z-dropdown: 1000;
  --z-modal: 1050;
  --z-tooltip: 1100;
}
```

在 Prompt 中引用：
```text
约束：只使用 src/tokens.css 中定义的颜色和间距
```

### 第 2 层：项目文档

这些文档在项目启动时创建，AI 任务时引用：

- `docs/ui-brief.md` - 业务上下文
- `docs/page-inventory.md` - 页面清单
- `docs/component-inventory.md` - 组件清单
- `docs/api-contract.md` - 后端接口契约

**在 Prompt 中引用**（Claude Code 支持 @ 语法）：
```text
Context: @docs/ui-brief.md, @docs/component-inventory.md, @src/tokens.css
```

### 第 3 层：任务 Prompt

这部分每次任务都不同，直接写在 Prompt 中：

```markdown
## 当前任务
实现审批队列页面（/approvals）的默认状态

## 具体要求
- 显示待审批订单列表（字段见 API 契约）
- 顶部筛选栏（状态、客户、日期范围）
- 批量操作按钮（右上角，常显选中数量）
- 分页（20 条/页）

## 不在本次范围
- 详情页（下个任务）
- 批量审批的确认弹窗（下个任务）
- 历史记录标签（暂不做）
```

### 第 4 层：对话上下文

工具自动管理，无需手动维护：
- 刚才生成的代码
- 刚才运行的测试结果
- 你的反馈（"这里有问题"）

## 上下文优化技巧

### 1. 最小必要原则

❌ **不好**：每次都粘贴 1000 行的完整 PRD

✅ **好**：只引用当前任务相关的章节
```text
Context: 
- 完整业务：@docs/ui-brief.md
- 本次焦点：第 3.2 节"批量审批流程"
```

### 2. 增量引用

第一次任务时提供完整上下文，后续任务只引用变化部分：

**第一次**（实现第一个页面）：
```text
Context: @docs/ui-brief.md, @docs/component-inventory.md, @src/tokens.css
```

**后续**（实现第二个页面）：
```text
Context: 延续上次对话的技术栈和规范
新增：本页特殊要求（见 page-inventory.md 第 5 页）
```

### 3. 使用别名

为常用文档创建别名，减少重复：

```markdown
<!-- 在 Prompt 开头定义 -->
别名定义：
- [Brief] = docs/ui-brief.md
- [组件] = docs/component-inventory.md
- [Token] = src/tokens.css
- [契约] = docs/api-contract.md

<!-- 后续使用 -->
Context: [Brief], [组件], [Token]
约束：遵循 [契约] 中的 /api/orders 接口
```

### 4. 分离事实与意见

**事实**（必须遵守）：
- API 字段名：`order_id`（不是 `orderId`）
- 颜色 Token：`var(--color-primary)`
- 路由格式：`/approvals/:tab`

**意见**（可以讨论）：
- 筛选栏放顶部还是侧边？
- 批量操作按钮文案："批量审批"还是"批量操作"？

在 Prompt 中明确标注：
```text
## 必须遵守（事实）
- API 字段名、Token 名称、路由结构

## 可以建议（意见）
- 按钮位置、文案措辞、动画效果
- 如有更好的方案，请说明理由
```

### 5. 版本化关键决策

当 AI 提出方案并被采纳后，将决策记录到文档中：

```markdown
<!-- docs/design-decisions.md -->
## 决策记录

### DR-001: 批量操作按钮位置
**日期**: 2026-08-24
**决策**: 放在页面右上角，常显选中数量
**理由**: 用户调研显示，批量操作是高频任务，需要常显
**替代方案**: 悬浮按钮（被拒，会遮挡内容）
**影响**: 所有列表页遵循此模式
```

下次遇到类似问题时，引用这个决策：
```text
Context: 批量操作按钮参考 docs/design-decisions.md #DR-001
```

## 可复制任务模板库

根据常见任务类型，提供开箱即用的 Prompt 模板。

### 模板 1：产品分析

**适用场景**：从 PRD 或竞品截图提取结构化信息

```markdown
## Context
输入材料：[PRD 文档 / 竞品截图 / 用户调研报告]
目标用户：[描述]
业务场景：[描述]

## Role
产品分析师，专注于 [领域] 的用户体验

## Action
从输入材料中提取：
1. 角色与权限矩阵（角色 | 权限 | 典型任务）
2. 对象模型（核心对象 | 属性 | 状态 | 操作）
3. 高频任务与风险任务（任务 | 频率 | 失败恢复）
4. 页面结构建议（页面 | 主要内容 | 入口）
5. 3 个值得借鉴的点 + 2 个需要注意的坑

## Format
每个部分用 Markdown 表格输出

## Test
- [ ] 每个结论都能追溯到输入材料的具体位置
- [ ] 角色权限矩阵没有遗漏或冲突
- [ ] 列出了我需要补充确认的信息

## Constraints
- 不新增输入中未提及的功能
- 不做视觉设计建议（仅关注信息架构和交互）
```

### 模板 2：状态矩阵生成

**适用场景**：为页面枚举所有可能的状态

```markdown
## Context
页面：[页面名称和路由]
主要功能：[简短描述]
数据来源：[API 或本地状态]
相关文档：@docs/ui-brief.md

## Role
交互设计师，专注于状态覆盖的完整性

## Action
为该页面输出状态矩阵，包括：
1. 默认态（首次加载，有数据）
2. 加载态（数据请求中）
3. 空数据态（首次使用，无历史数据）
4. 无结果态（筛选后无匹配）
5. 错误态（网络错误、服务器错误）
6. 无权限态（用户无访问权限）
7. 成功态（操作成功后的反馈）
8. 部分成功态（批量操作部分失败）

每个状态描述：
- 用户看到什么（UI 元素和文案）
- 能做什么（可用操作）
- 不能做什么（禁用的操作）

## Format
Markdown 表格：状态 | 看到什么 | 能做什么 | 不能做什么

## Test
- [ ] 8 种标准状态都有覆盖
- [ ] 文案可直接用于界面（真实长度，不写”这里显示...”）
- [ ] 错误态提供了恢复路径（如”重试”按钮）
- [ ] 空态和无结果态有明确区分

## Constraints
- 不添加输入中未提及的业务状态
- 文案符合用户语言习惯（非技术术语）
```

### 模板 3：Coding Agent（新功能开发）

**适用场景**：从设计稿或 PRD 实现新页面/组件

```markdown
## Context
任务：实现 [页面/组件名称]
设计来源：[Figma 链接 / PRD 章节]
相关文档：@docs/ui-brief.md, @docs/component-inventory.md, @src/tokens.css
当前阶段：G5 开发实现

## Role
前端工程师，React + TypeScript + Tailwind CSS，10 年经验

## Action
实现该页面/组件，包括：
1. 布局和样式（按设计稿）
2. 状态管理（默认/加载/空/错误）
3. 交互逻辑（点击、筛选、分页等）
4. 数据获取（使用 fixture，标注 TODO 连接真实 API）
5. 基础测试（渲染测试 + 交互测试）

**分步输出**：
- 第 1 步：输出实现计划（文件结构、组件拆分、技术选型）
- 等我确认后...
- 第 2 步：输出完整代码（按文件分块）
- 第 3 步：输出测试代码
- 第 4 步：说明如何运行和验证

## Format
- 实现计划：Markdown 列表
- 代码：Markdown 代码块，标注文件路径
- 测试：独立的代码块

## Test（验收标准）
- [ ] 通过 ESLint 和 TypeScript 检查
- [ ] 所有状态都有对应的 UI（8 种标准状态）
- [ ] 只使用 component-inventory.md 中的组件（禁止新建同义组件）
- [ ] 只使用 tokens.css 中的颜色和间距（无硬编码）
- [ ] 交互元素有 aria-label
- [ ] 键盘可通过 Tab 导航
- [ ] 加载和错误状态有 fixture 可测试

## Constraints（禁止修改）
- API 接口路径和字段名（见 docs/api-contract.md）
- 既有组件的 props 接口
- 路由结构
- Design Token 名称
- 不添加新的 npm 依赖（需要时先问我）
```

### 模板 4：Bug 修复

**适用场景**：修复已知问题

```markdown
## Context
Bug 描述：[问题现象]
复现步骤：[1. 2. 3.]
期望行为：[应该怎样]
相关文件：[已读取的文件]
视觉验收记录：@docs/visual-acceptance.md 第 X 条

## Role
前端工程师，专注于快速定位和修复问题

## Action
定位并修复该 Bug，保持其他功能不变

**分步输出**：
- 第 1 步：说明根因（为什么会出现这个 Bug）
- 第 2 步：提出修复方案（最小改动原则）
- 等我确认后...
- 第 3 步：输出代码变更（git diff 格式）
- 第 4 步：说明如何验证（复现步骤 + 验证步骤）

## Format
- 根因分析：1-2 段文字
- 修复方案：简短描述 + 将修改的文件列表
- 代码变更：```diff 格式

## Test
- [ ] Bug 已修复（按复现步骤验证）
- [ ] 没有引入新的问题（回归测试）
- [ ] 相关的其他视口/状态也检查过

## Constraints
- 只修复这一个问题，不顺便重构
- 不修改不相关的文件
- 保持 API 调用逻辑不变
```

### 模板 5：视觉还原

**适用场景**：从设计稿实现像素级还原

```markdown
## Context
设计稿：[Figma 链接或截图]
目标视口：[1440px / 768px / 390px]
相关组件：@docs/component-inventory.md
Design Token：@src/tokens.css

## Role
前端工程师，专注于像素级还原和响应式布局

## Action
实现该设计稿的 HTML + CSS，要求：
1. 间距、字号、颜色与设计稿一致
2. 响应式适配（如需要）
3. 悬停和焦点状态
4. 使用 Design Token（不硬编码）

**输出内容**：
- 布局分析（Grid / Flex / 嵌套层级）
- Token 映射表（设计稿颜色 → Token 变量）
- 完整代码（HTML + Tailwind classes 或 CSS）

## Format
Markdown + 代码块

## Test
- [ ] 视觉对比截图（实现 vs 设计稿）差异 < 2px
- [ ] 所有颜色来自 Token（无 #hex 或 rgb）
- [ ] 间距符合 8px 网格（4/8/16/24/32...）
- [ ] 长文本不溢出（测试最长边界值）
- [ ] 悬停和焦点状态明确

## Constraints
- 使用 Tailwind CSS utility classes
- 禁止内联样式
- 禁止 `!important`（除非有注释说明）
```

### 模板 6：测试用例生成

**适用场景**：为组件或页面生成测试代码

```markdown
## Context
被测对象：[组件/页面名称]
代码文件：@src/[path]
业务逻辑：@docs/ui-brief.md 相关章节

## Role
QA 工程师，熟悉 Vitest + Testing Library

## Action
生成完整的测试用例，覆盖：
1. 渲染测试（各状态能正常渲染）
2. 交互测试（点击、输入、提交）
3. 边界测试（空值、极长文本、特殊字符）
4. 无障碍测试（键盘导航、aria 属性）
5. 错误处理测试（API 失败、网络错误）

## Format
```typescript
// [ComponentName].test.tsx
import { render, screen, userEvent } from '@testing-library/react'
import { [ComponentName] } from './[ComponentName]'

describe('[ComponentName]', () => {
  describe('渲染', () => { ... })
  describe('交互', () => { ... })
  describe('边界情况', () => { ... })
  describe('无障碍', () => { ... })
})
```

## Test
- [ ] 测试覆盖率 > 80%
- [ ] 每个状态都有测试
- [ ] 关键业务逻辑有断言
- [ ] 使用有意义的测试描述

## Constraints
- 使用 Testing Library 的最佳实践（查询优先级）
- 不测试实现细节（不依赖内部 state）
- Mock 外部依赖（API 调用、localStorage）
```

### 模板 7：文档生成

**适用场景**：为组件生成使用文档或 Storybook

```markdown
## Context
组件代码：@src/components/[ComponentName]
设计稿：[Figma 链接]
使用场景：[简短描述]

## Role
技术文档工程师

## Action
生成该组件的使用文档，包括：
1. 组件概述（用途、适用场景）
2. Props API（名称、类型、默认值、说明）
3. 使用示例（基础用法 + 常见场景）
4. 无障碍说明（键盘操作、屏幕阅读器）
5. 注意事项（常见错误、性能建议）

如果生成 Storybook，提供：
- 所有 Props 的 Controls
- 典型场景的 Stories（Default, Loading, Error, etc.）

## Format
Markdown（文档）或 TypeScript（Storybook）

## Test
- [ ] Props 说明与实际代码一致
- [ ] 示例代码可直接运行
- [ ] 覆盖了主要使用场景

## Constraints
- 不虚构不存在的 Props
- 示例代码使用真实的 Token 和组件
```

### 模板 8：代码审查

**适用场景**：审查 AI 或人工生成的代码

```markdown
## Context
待审查代码：[文件路径或 PR 链接]
审查重点：[代码质量 / 安全 / 性能 / 无障碍]
项目规范：@CLAUDE.md, @docs/component-inventory.md

## Role
Senior 前端工程师，负责代码审查

## Action
审查代码并给出反馈，关注：
1. **正确性**：逻辑是否符合需求
2. **规范性**：是否遵循项目规范（Token、组件复用）
3. **完整性**：状态覆盖是否完整（8 种标准状态）
4. **安全性**：输入校验、XSS 防护
5. **性能**：不必要的渲染、大列表优化
6. **可维护性**：命名、注释、复杂度
7. **无障碍**：键盘、屏幕阅读器、颜色对比度

## Format
按优先级分组：
### 🔴 必须修改（P0）
- [文件:行号] 问题描述 + 建议修改

### 🟡 建议改进（P1）
- [文件:行号] 问题描述 + 建议修改

### 💡 可选优化（P2）
- [文件:行号] 改进建议

## Test
- [ ] 每条反馈都指向具体的代码位置
- [ ] 提供了可操作的修改建议（不只是指出问题）
- [ ] P0 问题会导致功能不可用或安全风险

## Constraints
- 只关注实质问题，不纠结代码风格（ESLint 已处理）
- 建议要考虑投入产出比（不过度优化）
```

## 失败模式与应对

AI 常见的失败模式及如何通过 Prompt 预防：

### 失败模式 1：过度设计

**现象**：你让 AI 实现一个简单表格，它给你加了排序、筛选、导出、虚拟滚动...

**原因**：Prompt 没有明确边界

**应对**：
```markdown
## Action
实现订单表格，**只包括**：
- 显示 5 列（订单号、客户、金额、状态、操作）
- 固定 20 条/页的分页
- 无排序、无筛选、无导出

## Constraints
- 本次不实现：排序、筛选、导出、批量操作（后续迭代）
- 如果你觉得某个功能必须有，明确提出并说明理由，而不是直接加上
```

### 失败模式 2：忽略边界情况

**现象**：只实现了”正常态”，空态、错误态、极长文本都没处理

**原因**：Prompt 没有要求状态覆盖

**应对**：
```markdown
## Test（验收标准）
必须实现以下状态（每个状态有 fixture 可测试）：
- [ ] 默认态（20 条数据）
- [ ] 加载态（skeleton）
- [ ] 空数据态（引导文案 + 次级操作）
- [ ] 错误态（错误信息 + 重试按钮）
- [ ] 长文本边界测试（客户名 50 字、订单号 30 字）

未实现任何一个状态，输出不合格。
```

### 失败模式 3：硬编码魔法值

**现象**：代码里到处是 `#3B82F6`、`padding: 16px`

**原因**：没有强制要求使用 Token

**应对**：
```markdown
## Constraints（硬约束）
- 所有颜色必须使用 `var(--color-*)` Token
- 所有间距必须使用 `var(--spacing-*)` Token
- 如果现有 Token 无法满足，**停下来问我**，而不是硬编码

## Test
- [ ] grep 检查：代码中无 `#` 开头的颜色
- [ ] grep 检查：CSS 中无裸数字间距（如 `16px`）
```

### 失败模式 4：忽略无障碍

**现象**：按钮没有 aria-label，键盘无法导航，错误提示屏幕阅读器读不到

**原因**：Prompt 没有提及无障碍要求

**应对**：
```markdown
## Test（验收标准）
无障碍要求（不可妥协）：
- [ ] 所有交互元素可通过 Tab 键导航
- [ ] 焦点顺序符合视觉顺序
- [ ] 图标按钮有 aria-label
- [ ] 表单错误提示使用 aria-invalid 和 aria-describedby
- [ ] 动态内容更新使用 aria-live

运行 `npm run test:a11y` 必须通过（0 个 serious/critical 违规）。
```

### 失败模式 5：偏离需求

**现象**：你要一个登录页，AI 给你做了注册页和忘记密码页

**原因**：AI “自作主张”补充了需求

**应对**：
```markdown
## Scope（范围边界）
**本次实现**：登录页（/login）
**明确不做**：注册页、忘记密码页、OAuth 登录（后续迭代）

如果你认为某个功能对登录流程是必需的（如”忘记密码”链接），
可以保留入口但链接到 TODO 页面，并在输出中说明。

**不要自行扩展范围。**
```

### 失败模式 6：依赖未声明的库

**现象**：代码里 `import` 了项目里没有的包

**原因**：AI 假设常用库已安装

**应对**：
```markdown
## Constraints
当前项目依赖（仅限以下）：
- react, react-dom, react-router-dom
- @tanstack/react-query
- zod, react-hook-form
- tailwindcss

**禁止使用其他库**。如需新依赖，必须：
1. 停下来明确告诉我需要什么库
2. 说明为什么现有依赖无法满足
3. 等我批准后再继续
```

## 高级技巧

### 技巧 1：Chain of Thought（思维链）

让 AI “思考出来”，提高复杂任务的准确性：

```markdown
## Action
分析这个 Bug 的根因，**逐步推理**：
1. 先描述观察到的现象
2. 列出可能的 3 个原因
3. 逐个排查（说明如何验证）
4. 确定最可能的根因
5. 提出修复方案
```

### 技巧 2：Few-Shot Examples（示例学习）

提供 1-2 个正确示例，AI 会模仿：

```markdown
## Format
参考以下示例格式输出：

**示例 1**：
```tsx
// 正确：使用 Token
<button className=”bg-[var(--color-primary)] px-[var(--spacing-md)]”>
  提交
</button>
```

**示例 2**（错误，禁止）：
```tsx
// 错误：硬编码
<button className=”bg-blue-500 px-4”>提交</button>
```

按示例 1 的方式输出代码。
```

### 技巧 3：Role Personas（角色人格）

给 AI 更具体的角色定位，影响输出风格：

```markdown
## Role
你是一位有 10 年经验的前端架构师，曾在 Stripe 和 Figma 工作，
专注于**可维护的大型前端系统**。你的代码特点：
- 优先简单方案，避免过度抽象
- 重视类型安全和错误处理
- 注重无障碍和性能
- 代码注释简洁但关键位置必有

以这样的视角审查代码。
```

### 技巧 4：Negative Prompting（反向提示）

明确不要什么，和明确要什么一样重要：

```markdown
## Constraints
**禁止**：
- ❌ 使用 `any` 类型
- ❌ 使用 `// @ts-ignore`
- ❌ 使用 `!important` 覆盖样式
- ❌ 使用 `setTimeout` 模拟异步（用 Promise）
- ❌ 使用 inline 事件处理器（`onClick={()=>...}`，抽取到函数）

违反任何一条，输出不合格。
```

### 技巧 5：Iterative Refinement（迭代细化）

复杂任务分多轮，每轮只做一件事：

```markdown
<!-- 第 1 轮：规划 -->
先输出实现计划，**不要写代码**。

<!-- 收到计划后，第 2 轮：实现核心 -->
实现计划中的第 1-3 步（组件结构和布局），**暂不实现交互**。

<!-- 收到代码后，第 3 轮：补充交互 -->
在现有代码基础上，补充交互逻辑（点击、筛选）。

<!-- 第 4 轮：补充测试 -->
为以上代码生成测试用例。
```

## 总结：打造你的 Prompt 工具箱

建立一个项目级的 Prompt 库，积累可复用的模板：

```text
prompts/
  product-analysis.md      # 产品分析模板
  state-matrix.md          # 状态矩阵模板
  coding-new-feature.md    # 新功能开发模板
  coding-bug-fix.md        # Bug 修复模板
  visual-restore.md        # 视觉还原模板
  test-generation.md       # 测试生成模板
  code-review.md           # 代码审查模板
  doc-generation.md        # 文档生成模板
```

每次任务：
1. 选择对应模板
2. 填充具体信息（Context、Action、Test）
3. 执行并记录结果
4. 根据反馈优化模板

3 个月后，你会有一套为你的团队定制的、经过实战验证的 Prompt 库。

**记住**：好的 Prompt 不是一次写对，而是迭代出来的。每次失败都是优化模板的机会。
