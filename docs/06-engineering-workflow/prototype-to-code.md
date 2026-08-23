# 原型到代码

把已评审原型翻译成路由、组件、状态和测试。目标是让代码表达设计系统，而不是把截图硬编码成一次性页面。

## 映射表

| 设计资产 | 工程资产 | 检查点 |
| --- | --- | --- |
| Figma Frame | 路由或页面模式 | URL、权限和数据依赖明确 |
| Auto Layout | CSS Grid/Flex 布局 | 容器和间距来自 Token |
| Component | React/Vue 组件 | API、状态和可访问名称一致 |
| Variant | props 或状态机 | 默认、加载、错误、禁用齐全 |
| Prototype flow | 路由 + 交互测试 | 返回、关闭、成功和失败可复现 |
| Variable/Style | CSS 变量或主题对象 | 禁止业务组件写临时颜色 |

## 推荐实现顺序

1. 建立页面壳：导航、顶栏、内容容器和响应式规则。
2. 实现 [Design Token](../04-design-system/tokens.md) 与高频组件。
3. 按 [组件清单](../templates/component-inventory.md) 实现列表、筛选、详情抽屉和确认对话框。
4. 先用 fixture 渲染所有状态，再接入 [真实数据](real-data-integration.md)。
5. 为主流程写键盘、路由和错误恢复测试。
6. 使用固定视口截图进入 [视觉评审闭环](../05-ai-design-workflow/visual-review-loop.md)。

## 状态优先的组件接口

```tsx
<OrderTable
  rows={rows}
  state={loading ? "loading" : error ? "error" : rows.length === 0 ? "empty" : "ready"}
  selectedIds={selectedIds}
  onSelectionChange={setSelectedIds}
  onOpen={openOrder}
  onRetry={reload}
/>
```

状态名称应来自同一套 [页面状态](../02-web-design/responsive-states.md)，不要让每个页面发明 `isBusy`、`hasProblem` 等含义模糊的布尔值。

## 给 Coding Agent 的边界

可以让 Agent 生成：组件骨架、重复的 Token 引用、fixture、表格列配置和测试样例。必须人工确认：业务权限、危险操作、数据脱敏、键盘焦点、响应式折叠、错误恢复和 API 契约。共享上下文参见 [Agent 协作](../05-ai-design-workflow/agent-collaboration.md)。

## 常见返工源

- Frame 没有命名，导致路由和组件职责无法映射。
- 只提供默认态，开发后才发现空态和失败态没有位置。
- 用截图尺寸代替布局规则，窗口变化时文字和按钮互相挤压。
- 组件复制出多个同义版本，没有回收到 [页面模式](../04-design-system/patterns.md)。
- 用真实生产数据喂给外部 Agent。练习时使用脱敏 fixture，权限边界见 [真实数据接入](real-data-integration.md)。

完成后进入 [验收清单](acceptance-checklist.md)。
