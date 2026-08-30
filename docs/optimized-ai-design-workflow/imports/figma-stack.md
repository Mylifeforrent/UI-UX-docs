# Figma 体系

← 返回 [原型先行全流程主文档](prototype-first-workflow.md)

这套流程横跨 Figma 的几个产品/能力。后端开发者容易把它们混为一谈，结果用错工具。这份文档划清各自定位与边界。以下能力、席位与端点均以 [Figma 官方文档](https://www.figma.com/) 为准。高保真逐步操作见 [Figma Make 高保真保姆级教程](figma-make-high-fidelity.md)。

## 四层能力速览

| 能力 | 定位 | 在本流程中的角色 | 边界 |
| --- | --- | --- | --- |
| **Figma Design** | 传统矢量设计文件（Frame/组件/Variables） | Copy design 之后：人精修，作为 MCP 的视觉源 | 需要人工整理命名与 Auto Layout |
| **Figma AI** | 局部生成、改写和探索 | 在已有 Design 上改文案/变体，不替代 Make 验证 | 业务准确性、Token 和状态仍要人审 |
| **Figma Make** | 用自然语言生成 code-backed 原型 | 把四件套变成可交互原型，**只验证交互** | 产出是验证用原型，**不直接进生产** |
| **Figma MCP + Code Connect** | 把精修结构暴露给 Coding Agent；组件钉到真实 import | 让 Agent 读结构而非猜截图 | Remote 必须选区链接；无映射时禁止把中间表示当最终实现 |

Copy design（[官方说明](https://help.figma.com/hc/en-us/articles/35060759685015-Copy-a-Figma-Make-preview-as-design-layers)）把 Make 当前 preview 贴进 Design：**单向快照**，不自动绑设计系统、不可交互、不回写 Make。不要当成双向同步。Make「改本地仓库」是封闭 beta，不是主路径。

## 后端类比

- **Figma Make ≈ 快速起的可运行 Demo / POC**：验证思路用，验证完就丢，不当生产代码。
- **Figma Design ≈ 规范化的接口定义（含类型和结构）**：Frame 命名=路由，组件=可复用类，变量=常量/令牌。
- **MCP Server ≈ 一个 API**：Coding Agent 通过它拿到结构化的"设计事实"，而不是对着截图做 OCR 猜测。`get_design_context` 返回 React+Tailwind **中间表示**，必须翻译进本仓库组件 + Token。
- **Code Connect ≈ 依赖映射表**：告诉 MCP"设计里这个组件 = 代码里 `src/components/OrderTable.tsx`"。无映射时 Agent 会发明长得像的 div。席位：Org/Enterprise + Dev/Full。[Code Connect](https://developers.figma.com/docs/code-connect/)

## Remote MCP vs Desktop MCP

以 [MCP Guide](https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server) 与 [Remote 安装](https://developers.figma.com/docs/figma-mcp-server/remote-server-installation/) 为准。现有文档若只写桌面端，以本节为准。

| | Remote（推荐） | Desktop（可选） |
| --- | --- | --- |
| 端点 | `https://mcp.figma.com/mcp` | `http://127.0.0.1:3845/mcp` |
| 接入 | Cursor：`/add-plugin figma` 或 `mcp.json`；Claude Code：官方 plugin / `mcp add` | 须开 [Figma 桌面端](https://www.figma.com/downloads/) Dev Mode MCP |
| 选区 | **看不到画布选区**，必须 Copy link to selection | 可选「实现当前选区」 |
| 适用 | 默认路径 | 特定企业内网 / 必须走本地 |

截图只做回归，不当间距来源。一次一个 Frame，不要整页丢给 `get_design_context`。

## Make kits / Guidelines（可选）

已有组件 npm 包时，优先用 Make kits + `guidelines.md` 提保真，不是必须。[Get started with Make kits](https://help.figma.com/hc/en-us/articles/39241689698839-Get-started-with-Make-kits)

## 为什么 Make 原型不能直接进生产

| Make 原型 | 生产代码要求 |
| --- | --- |
| 无测试 | 需单元/集成测试 |
| 无权限校验 | 需真实鉴权 |
| 依赖不可控、数据是假的 | 需接真实 API、可控依赖 |
| 为"看起来对"而生成 | 为"长期可维护"而设计 |

所以生产代码是**重新生成**的——但有了精修 Design + MCP + Code Connect，Agent 是照着结构化设计事实生成，并把中间表示翻译进库存组件，而非从零，也不是拷贝 Make zip。

## 准备清单

- Figma 账号（Make、Copy design、MCP、Code Connect 席位以官方为准）
- 推荐 Remote MCP；桌面端用于 Design 精修，Desktop MCP 可选
- 本地 Coding Agent（Claude Code / Cursor）
- 已有组件库且有席位时，配置 [Code Connect](https://developers.figma.com/docs/code-connect/)

## MCP 可读性精修清单（Copy design 之后、MCP 之前）

人做这些，不要未整理就 MCP：

- Frame 命名 = 路由 + 状态，如 `/approvals/loading`、`/approvals/empty`
- 布局一律 Auto Layout，禁止绝对定位裸摆
- 重复元素抽成 Component；页面上是 **实例**，不要 detach
- 颜色/间距存为 Variables（对应 [Design Token](../04-design-system/tokens.md)）
- 删隐藏层和无意义嵌套
- Layer 面板逐个检查，不留未命名 Frame

## 相关文档

- [原型先行全流程主文档](prototype-first-workflow.md)
- [Figma Make 高保真保姆级教程](figma-make-high-fidelity.md)
- [原型到代码](../06-engineering-workflow/prototype-to-code.md)
- [工具矩阵](../07-tools/tool-matrix.md)
