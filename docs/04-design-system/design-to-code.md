# 设计到代码

把 Figma 的命名、变量和交互映射成可维护的工程资产，而不是让 AI 从一张截图猜完整系统。

## 建议映射

```text
Figma Variables      → tokens.css / theme object
Figma Components     → React/Vue components
Figma Variants       → props / state
Figma Sections       → page patterns
Prototype flows      → routes + interaction tests
```

## 命名契约

Frame 使用页面路由或模式名，Component 使用 PascalCase，Variant 使用稳定状态名（如 `state=loading`、`tone=danger`）。这些名称同时出现在 [组件清单](../templates/component-inventory.md)、代码 props、测试描述和验收记录中。

## 所有权边界

AI 可以生成重复的组件骨架、Token 引用、fixture 和测试草稿；人必须确认业务权限、危险操作、数据脱敏、焦点行为、响应式折叠和 API 契约。先建立组件和 Token，再生成页面；不要让页面代码反过来定义系统规则。

每次同步检查：命名、状态、响应式行为、可访问性、真实内容长度和数据异常。视觉问题进入 [视觉评审闭环](../05-ai-design-workflow/visual-review-loop.md)，数据问题进入 [真实数据接入](../06-engineering-workflow/real-data-integration.md)。
