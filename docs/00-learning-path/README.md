# 8 周学习路线

用 8 周建立“能设计、能说明、能实现、能验收”的最低可用能力。每周都有可见产出，不以看完文章或安装工具作为完成标准。主案例是 [企业 Web 工作台](../08-practice-projects/web-workbench.md)。

## 阶段路线

| 周次 | 学习内容 | 时间盒 | 必须产出 | 通过标准 |
| --- | --- | --- | --- | --- |
| 1 | [视觉层级](../01-foundations/visual-hierarchy.md)、[布局/色彩/字体](../01-foundations/layout-color-type.md) | 3--5 小时 | 拆解 3 个企业页面 | 能说清层级、对齐、密度和状态 |
| 2 | [信息架构](../02-web-design/information-architecture.md) | 3--5 小时 | 角色、对象、任务、权限表 | 每个任务有入口和失败恢复 |
| 3 | [企业 SaaS](../02-web-design/enterprise-saas.md)、[表单与表格](../02-web-design/forms-tables.md) | 5--7 小时 | 列表、详情、表单灰度线框 | 主任务、批量动作和异常状态齐全 |
| 4 | [响应式与状态](../02-web-design/responsive-states.md)、[交互与无障碍](../01-foundations/interaction-accessibility.md) | 3--5 小时 | 状态矩阵、四个视口规则 | 键盘主流程和长内容行为明确 |
| 5 | [Tokens](../04-design-system/tokens.md)、[组件](../04-design-system/components.md) | 5--7 小时 | Token、组件、页面模式清单 | 新页面复用规则而不是复制粘贴 |
| 6 | [Figma 体系](../05-ai-design-workflow/figma-stack.md)、[Prompt 与上下文](../05-ai-design-workflow/prompting-and-context.md) | 5--7 小时 | 高保真原型和 Prompt 记录 | AI 有完整上下文，结果可评审 |
| 7 | [原型到代码](../06-engineering-workflow/prototype-to-code.md)、[真实数据接入](../06-engineering-workflow/real-data-integration.md) | 1--2 天 | 接 fixture/API 的工作台页面 | 数据状态、权限和部分失败可复现 |
| 8 | [验收清单](../06-engineering-workflow/acceptance-checklist.md)、[视觉评审](../05-ai-design-workflow/visual-review-loop.md) | 3--5 小时 | 截图、键盘路径、问题记录 | 无 P0/P1 阻塞项，有前后对比证据 |

## 每周节奏

```text
周一：拆解一个真实产品
周二：画信息架构和页面状态
周三：建立组件和视觉规则
周四：用 Figma/AI 做原型并评审
周五：实现、截图、按清单修正
```

完成 Web 主线后，再做 [App 信息架构](../03-app-design/information-architecture.md) 和 [移动端配套应用](../08-practice-projects/mobile-companion.md)，学习平台差异而不是把桌面后台直接缩小。

不要先比较哪个生成器“最强”。没有 [页面清单](../templates/page-inventory.md)、状态定义和 [Design Token](../04-design-system/tokens.md)，生成速度只会放大返工量。
