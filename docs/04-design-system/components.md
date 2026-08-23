# 组件规范

组件规范至少包含用途、结构、属性、状态、尺寸、内容规则、键盘行为和示例。组件状态应与 [Token](tokens.md) 和代码 API 同名。

## 高频组件

优先建设 Button、Input、Select、DatePicker、Table、Pagination、Modal、Drawer、Toast、Tabs、Badge、Empty、Skeleton、Alert。

## Button 示例

| 项目 | 约定 |
| --- | --- |
| 变体 | primary、secondary、tertiary、danger |
| 状态 | default、hover、focus、loading、disabled |
| 内容 | 动作 + 对象，如“批量审批” |
| 键盘 | 原生 button，Enter/Space 触发，loading 时保持名称 |
| 危险操作 | danger 变体 + 明确确认，不用颜色单独表达 |
| 响应式 | 文字过长可换行或变成稳定图标+Tooltip，不挤压相邻控件 |

```tsx
<Button variant="danger" loading={isSubmitting} aria-describedby="approval-impact">
  批量审批（3）
</Button>
```

## Input 示例

| 项目 | 约定 |
| --- | --- |
| 结构 | label、输入框、帮助文本、错误文本 |
| 状态 | default、focus、filled、error、disabled |
| 键盘 | Tab 可进入，Enter 行为明确，错误后焦点可定位 |
| 内容 | 展示格式示例，不用 placeholder 代替 label |
| 无障碍 | `label`、`aria-describedby`、错误关联 |

## 每个组件都要回答

- 什么时候使用，什么时候用页面模式或原生元素替代。
- 默认、悬停、聚焦、加载、禁用、错误和成功如何表现。
- 长文本、窄容器、无数据和权限受限时如何表现。
- 哪些 props 是业务数据，哪些是视觉变体；命名与 [组件清单](../templates/component-inventory.md) 一致。
- 是否需要恢复焦点、读屏名称、键盘快捷键或触控替代操作。

不要为单页临时复制同义组件；跨页面结构放入 [页面模式](patterns.md)，再由代码实现。
