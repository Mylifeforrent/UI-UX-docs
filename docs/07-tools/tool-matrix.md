# 工具矩阵

工具按工作流位置选择，不按“谁生成代码最多”选择。产品功能、套餐和权限会变化，采购或接入前应查看官方文档并做企业数据评估。

| 工具/层 | 最适合阶段 | 输入 | 输出 | 验证方式 | 企业注意事项 | 生产定位/替代 |
| --- | --- | --- | --- | --- | --- | --- |
| Figma Design | 视觉设计、组件、协作、评审 | 页面结构、品牌、组件规范 | 设计稿、组件、原型 | 人工评审、组件检查 | 权限、外部分享、客户数据 | 生产设计；替代是本地设计工具 |
| Figma AI | 设计探索、文案和局部修改 | Prompt、选中对象、已有设计 | 变体、文案、局部调整 | 对照 Brief 和状态矩阵 | 不上传敏感数据；确认生成内容 | 探索和加速；人工定稿 |
| Figma Make | 原型与 code-backed 探索 | PRD、页面目标、数据、交互 | 可交互原型 | 真实流程、状态、视觉评审 | 代码质量、依赖和权限需复核 | 原型优先；生产代码需工程化 |
| Figma MCP | Design Context 连接 Agent | Frame、组件、Token、文件 | Agent 可引用的设计上下文 | 检查命名、权限和上下文完整性 | 最小权限、敏感文件隔离 | 连接层；无 MCP 可导出规范 |
| Claude Code / Codex / Cursor | 工程实现和修正 | Brief、组件、Token、API、测试 | React/Vue 代码、测试、修复 | lint、测试、浏览器截图 | 源码、密钥、网络访问边界 | 生产辅助；必须人工 review |
| UI UX Pro Max / Taste | Coding Agent 设计增强 | 设计规则、任务、代码上下文 | 设计建议、页面实现约束 | 对照 Design System 和截图 | 技能来源、规则维护和上下文泄露 | 能力增强层；替代是仓库内 design.md |
| Impeccable | UI 审查和修复建议 | 页面、截图、问题描述 | 可执行的 UI 修复项 | 逐项回归截图 | 不将敏感截图发到外部 | 审查辅助；人工判断 |
| OpenPrototype / OpenUI | 快速探索 | PRD、Prompt、组件约束 | 原型或 Playground | 丢弃性验证、可用性评审 | 许可证、外部服务和数据 | 探索用途；生产需重建 |

## 选择决策

- 要建立可协作的视觉基准：先选 Figma Design + [Design System](../04-design-system/README.md)。
- 要快速验证流程：选 Figma Make 或 OpenPrototype，但把输出视为原型。
- 要从设计进入代码：选 Figma MCP + Coding Agent，并准备 [API 契约](../06-engineering-workflow/real-data-integration.md)。
- 要修正已有页面：使用截图驱动的评审闭环，而不是重新生成整页。
- 不能发送业务数据时：使用脱敏 fixture、仓库本地规则和离线截图。

## 三个练习

1. 同一订单列表分别用 Figma Make 和 Coding Agent 探索，比较状态覆盖和可维护性。
2. 将现有组件库接入 Agent，要求它只使用已存在的 Token 和组件，并检查是否产生临时颜色。
3. 用固定视口截图记录一个视觉问题，交给 UI 审查工具生成修复建议，再按 [视觉验收](../templates/visual-acceptance.md) 回归。
