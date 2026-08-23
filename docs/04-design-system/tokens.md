# Design Token

Token 是设计值的语义名称，不是散落在 CSS 里的数字。先定义原始值，再定义语义值；组件只引用语义值。

## 最小集合

```text
color.background / color.surface / color.text / color.border
color.action / color.success / color.warning / color.danger
space.1 ... space.6
font.body / font.heading / font.caption
radius.sm / radius.md
shadow.surface
```

## 示例结构

```json
{
  "primitive": {
    "blue.600": "#2563EB",
    "gray.100": "#F3F4F6",
    "space.4": "16px"
  },
  "semantic": {
    "color.action": "{primitive.blue.600}",
    "color.surface": "#FFFFFF",
    "color.text": "#111827",
    "space.control": "{primitive.space.4}"
  }
}
```

```css
:root {
  --color-action: #2563eb;
  --color-surface: #ffffff;
  --color-text: #111827;
  --space-control: 16px;
}
[data-theme="dark"] {
  --color-surface: #111827;
  --color-text: #f9fafb;
}
```

业务组件只使用 `--color-action`、`--space-control` 等语义变量，不直接写十六进制颜色或随意的 `margin`。为亮色、暗色和品牌变体预留映射，状态色不能成为唯一信息信号。

## 命名与迁移

命名按“用途”而不是“当前颜色”命名，例如 `color.action`，不要命名为 `color.blue`. 删除或修改 Token 前记录影响组件、截图和迁移方式；先新增兼容别名，再迁移引用，最后删除旧名称。Token 变更必须与 [组件规范](components.md) 和 [设计到代码](design-to-code.md) 一起评审。

## 检查

- [ ] 语义 Token 在 Figma、代码和文档中同名。
- [ ] 亮色/暗色映射通过对比度检查。
- [ ] 组件没有临时颜色、间距或圆角。
- [ ] 变更有受影响页面截图和版本记录。
