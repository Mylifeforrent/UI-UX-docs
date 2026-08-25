# Figma 体系

← 返回 [原型先行全流程主文档](prototype-first-workflow.md)

这套流程横跨 Figma 的几个产品/能力。后端开发者容易把它们混为一谈，结果用错工具。这份文档划清各自定位与边界。以下能力、席位与端点均以 [Figma 官方文档](https://www.figma.com/) 为准。

## 四层能力速览

| 能力 | 定位 | 在本流程中的角色 | 边界 |
| --- | --- | --- | --- |
| **Figma Make** | 用自然语言生成 code-backed 原型 | 第 4 步：把四件套变成可交互原型 | 产出是验证用原型，**不直接进生产** |
| **Figma Design** | 传统矢量设计文件（Frame/组件/变量） | 第 5 步：把定稿原型转为可编辑、可被 MCP 读取的结构 | 需要人工整理命名与 Auto Layout |
| **Dev Mode MCP Server** | 桌面端本地服务，把设计结构暴露给 Coding Agent | 第 7 步：让 Agent 读结构而非猜截图 | 仅桌面端运行，需 Dev/Full 席位 |
| **Code Connect** | 把设计组件映射到真实代码组件 | 第 7 步：MCP 返回"用你的 OrderTable" | 需项目已有组件库 |

## 后端类比

- **Figma Make ≈ 快速起的可运行 Demo / POC**：验证思路用，验证完就丢，不当生产代码。
- **Figma Design ≈ 规范化的接口定义（含类型和结构）**：Frame 命名=路由，组件=可复用类，变量=常量/令牌。
- **MCP Server ≈ 一个本地 API**：Coding Agent 通过它拿到结构化的"设计事实"，而不是对着截图做 OCR 猜测。
- **Code Connect ≈ 依赖映射表**：告诉 MCP"设计里这个组件 = 代码里 `src/components/OrderTable.tsx`"，避免 Agent 重写轮子。

## 为什么 Make 原型不能直接进生产

| Make 原型 | 生产代码要求 |
| --- | --- |
| 无测试 | 需单元/集成测试 |
| 无权限校验 | 需真实鉴权 |
| 依赖不可控、数据是假的 | 需接真实 API、可控依赖 |
| 为"看起来对"而生成 | 为"长期可维护"而设计 |

所以第 7 步的代码是**重新生成**的——但有了 MCP + Code Connect，Agent 是照着结构化设计事实生成，而非从零。

## 准备清单

- Figma 账号（Make 与 Dev Mode MCP 需付费席位，以官方为准）
- [Figma 桌面端](https://www.figma.com/downloads/)（MCP server 只在桌面端运行）
- 本地 Coding Agent（Claude Code / Cursor）
- 已有组件库时，配置 [Code Connect](https://www.figma.com/developers/code-connect)

## 第 5 步整理规则（MCP 读的就是这份结构）

- Frame 命名 = 路由 + 状态，如 `/approvals/loading`、`/approvals/empty`
- 布局一律 Auto Layout，禁止绝对定位裸摆
- 重复元素抽成 Component；颜色/间距存为变量（对应 [Design Token](../04-design-system/tokens.md)）
- Layer 面板逐个检查，不留未命名 Frame

## 相关文档

- [原型先行全流程主文档](prototype-first-workflow.md)
- [原型到代码](../06-engineering-workflow/prototype-to-code.md)
- [工具矩阵](../07-tools/tool-matrix.md)
