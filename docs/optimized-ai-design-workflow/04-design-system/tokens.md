# Design Token

← 返回 [原型先行全流程主文档](../imports/prototype-first-workflow.md)

Design Token（设计令牌）是把颜色、间距、字体等设计决策变成**命名常量**的机制。对后端开发者来说，它就是设计层的"配置中心 / 枚举常量"——所有界面引用同一批命名值，改一处全局生效，杜绝魔法数字。

企业级 UI 与"能跑就行"的最大区别之一，就是**是否有令牌体系**。硬编码 `#3B82F6` 到处散落，等于代码里到处写魔法数字。

## 原始令牌 vs 语义令牌（关键分层）

| 层级 | 作用 | 示例 | 后端类比 |
| --- | --- | --- | --- |
| 原始令牌（primitive） | 调色板/尺度的原子值 | `--blue-500: #3B82F6` | 常量池 |
| 语义令牌（semantic） | 按"用途"命名，引用原始令牌 | `--color-primary: var(--blue-500)` | 面向接口编程 |

**界面和组件只引用语义令牌**，不直接引用原始令牌。这样换主题/换品牌色时只改语义层的映射，组件代码不动——和"依赖抽象而非实现"一个道理。

## 令牌分类与命名规范

统一用 kebab-case，前缀标类别：

```css
:root {
  /* 颜色 · 语义 */
  --color-primary: var(--blue-500);
  --color-surface: var(--gray-0);
  --color-border: var(--gray-200);
  --color-text: var(--gray-900);
  --color-text-muted: var(--gray-500);
  --color-danger: var(--red-500);
  /* 状态语义（供 StatusBadge 等使用） */
  --color-status-pending: var(--amber-500);
  --color-status-approved: var(--green-500);
  --color-status-rejected: var(--red-500);

  /* 间距 · 4px 基准尺度 */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-6: 24px;

  /* 字体 */
  --font-sans: "Inter", system-ui, sans-serif;
  --text-sm: 14px;
  --text-base: 16px;
  --text-lg: 20px;

  /* 圆角 / 阴影 */
  --radius-md: 8px;
  --radius-lg: 12px;
  --shadow-sm: 0 1px 2px rgb(0 0 0 / 0.06);
}
```

命名规则：`--<类别>-<用途>[-<变体>]`。如 `--color-text-muted`、`--space-4`、`--color-status-pending`。

## Make 变量 ↔ 代码令牌对齐

MCP 能把设计事实喂给 Coding Agent 的前提，是设计和代码用**同一套命名**。

1. 第 5 步在 Figma Design 里把颜色/间距存为**变量**，变量名和代码令牌一致（`color/primary` ↔ `--color-primary`）。
2. 代码侧把令牌集中在 `src/tokens.css`（或 Tailwind v4 的 `@theme`），作为唯一来源。
3. 通过 [Code Connect](../imports/figma-stack.md) 让 MCP 返回令牌引用而非裸值。

## 喂给 AI 的约束（防硬编码）

生成原型/代码时，把令牌文件连同这句一起给：

```text
只使用 tokens.css 里已定义的语义令牌（--color-*, --space-*, --text-* …），
禁止出现任何硬编码颜色值（如 #3B82F6）或魔法数字间距（如 13px）；
需要新颜色/间距时先提出并等我确认，不要自行发明。
```

## 常见误区（后端视角）

| 误区 | 后果 | 纠正 |
| --- | --- | --- |
| 到处硬编码颜色 | 改主题要全局搜替换 | 只用语义令牌 |
| 组件直接引用原始令牌 | 换品牌色要改每个组件 | 组件只引语义层 |
| 间距用任意像素值 | 界面节奏乱、不成体系 | 用 4px 基准尺度 |
| Figma 变量名和代码令牌不一致 | MCP 无法映射 | 两侧命名对齐 |

## 相关文档

- [组件清单模板](../templates/component-inventory.md)（令牌映射列）
- [Figma 体系](../imports/figma-stack.md) · [原型到代码](../06-engineering-workflow/prototype-to-code.md)
