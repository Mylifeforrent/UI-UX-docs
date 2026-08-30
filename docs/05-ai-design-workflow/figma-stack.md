# Figma 体系

Figma 不是“画完就丢”的静态交付物，而是设计上下文、原型评审和 Agent 协作的一部分。具体权限和产品功能会变化，接入前以 [Figma AI](https://www.figma.com/ai/) 与 [Figma Make](https://www.figma.com/make/) 官方资料为准。高保真逐步操作见 [Figma Make 高保真保姆级教程](figma-make-high-fidelity.md)。

## 四层能力

| 层 | 作用 | 输入 | 输出 | 人工检查 |
| --- | --- | --- | --- | --- |
| Figma Design | 视觉设计、组件、协作；MCP 的视觉源 | 页面结构、品牌、组件规范 | Frame、组件、Variables | 层级、状态、可访问性、真实内容 |
| Figma AI | 局部生成、改写和探索 | Prompt、选中对象、已有设计 | 变体、文案、局部调整 | 业务准确性、Token 和状态 |
| Figma Make | code-backed 原型，**只验证交互** | 四件套、已冻组件、交互 | 可交互原型 | **不把原型代码直接当生产代码**；禁止合入 git 生产目录 |
| Figma MCP + Code Connect | 把精修 Frame 交给 Coding Agent | Frame 选区链接、组件、Token | Agent 可引用的上下文；组件钉到真实 import | 权限、命名、敏感文件隔离；无映射时禁止把中间表示当最终实现 |

Copy design（[官方说明](https://help.figma.com/hc/en-us/articles/35060759685015-Copy-a-Figma-Make-preview-as-design-layers)）把 Make 当前 preview 贴进 Design：**单向快照**，不可交互、不回写 Make，组件与样式不自动挂设计系统。唯一的例外是变量——粘贴前先给目标 Design 文件挂上含 Variables 的库，官方会自动匹配并绑定，能省掉大半手工绑 Token 的活。不要当成双向同步。Make「改本地仓库」是封闭 beta，不是主路径。

## 后端类比

- **Figma Make ≈ 快速起的可运行 Demo**：验证思路用，验证完不当生产代码。
- **Figma Design ≈ 规范化的接口定义**：Frame 命名 = 路由，组件 = 可复用类，Variables = Token。
- **MCP ≈ API**：Agent 通过它拿到结构化设计事实，而不是对着截图做 OCR。`get_design_context` 返回 React+Tailwind **中间表示**，必须翻译进本仓库组件 + Token。
- **Code Connect ≈ 依赖映射表**：设计组件钉到真实代码 import。无映射时 Agent 会发明长得像的 div。席位：Org/Enterprise + Dev/Full。[Code Connect](https://developers.figma.com/docs/code-connect/)

## Remote MCP vs Desktop MCP

以 [MCP Guide](https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server) 与 [Remote 安装](https://developers.figma.com/docs/figma-mcp-server/remote-server-installation/) 为准。

| | Remote（推荐） | Desktop（可选） |
| --- | --- | --- |
| 端点 | `https://mcp.figma.com/mcp` | `http://127.0.0.1:3845/mcp` |
| 席位 | 所有席位与计划都能连 | 付费计划的 Dev/Full 席位 + 桌面端 |
| 接入 | Cursor：`/add-plugin figma` 或 `mcp.json`；Claude Code：官方 plugin / `mcp add` | 须开 Figma 桌面端 Dev Mode MCP |
| 取上下文 | 链接式：Copy link to selection（客户端只解析 node-id） | 链接式，另支持「实现当前选区」 |
| 适用 | 默认路径 | 特定企业内网 / 必须走本地 |

**能连上不等于跑得动。** 读取类工具按席位限流（[Rate limits & access](https://developers.figma.com/docs/figma-mcp-server/rate-limits-access/)）：Dev/Full 席位在 Professional / Organization 约 200 次/天，Enterprise 约 600 次/天；View / Collab 席位只有约 6 次/月，做不了持续的设计到代码闭环。排期前先用 `whoami` 确认席位，配额以官方表为准。

截图只做回归，不当间距来源。一次一个 Frame，不要整页丢给 `get_design_context`——既容易读错节点，也白烧配额。

## Make kits / Guidelines（可选）

已有组件 npm 包时，优先用 Make kits + `guidelines.md` 提保真，不是必须。[Get started with Make kits](https://help.figma.com/hc/en-us/articles/39241689698839-Get-started-with-Make-kits)

## 为什么 Make 原型不能直接进生产

| Make 原型 | 生产代码要求 |
| --- | --- |
| 无测试 | 需单元/集成测试 |
| 无权限校验 | 需真实鉴权 |
| 依赖不可控、数据是假的 | 需接真实 API、可控依赖 |
| 为"看起来对"而生成 | 为"长期可维护"而设计 |

生产代码仍需测试、权限校验、真实数据、性能和 [交付验收](../06-engineering-workflow/acceptance-checklist.md)。企业数据使用前先脱敏并确认分享权限。

## MCP 可读性精修清单（Copy design 之后、MCP 之前）

人做这些，不要未整理就 MCP：

- Frame 命名 = 路由 + 状态，如 `/approvals/loading`
- 一律 Auto Layout，禁止绝对定位裸摆
- 颜色/间距绑 Variables：挂库后自动绑上的核对一遍，没绑上的手工补，对应 [Design Token](../04-design-system/tokens.md)
- 页面上是 **组件实例**，不要 detach；主组件放 `Components` 页
- 删隐藏层和无意义嵌套；长文案用真实长度
- Layer 面板不留未命名 Frame

## 推荐闭环

```text
四件套 → Make 验证交互 → Copy design → 人精修 Design
→ MCP + Code Connect → 本地 Agent（翻译进库存组件）
→ 浏览器截图回归 → 回到 Design 或验收记录
```

路径 A / 路径 B 的选择见 [原型先行](prototype-first-workflow.md)。落地见 [原型到代码](../06-engineering-workflow/prototype-to-code.md)。
