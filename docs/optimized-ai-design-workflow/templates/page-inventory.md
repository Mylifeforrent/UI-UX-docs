# 页面清单模板

← 返回 [原型先行全流程主文档](../imports/prototype-first-workflow.md)

列出本次要做的所有页面。**路由即未来的代码路由**——这里定的 `/approvals` 会一路贯穿到 Figma Frame 命名和最终代码。复制到 `docs/page-inventory.md` 填写。

| 路由 | 页面名 | 一句话职责 | 需覆盖的状态 | 关键组件 | 优先级 |
| --- | --- | --- | --- | --- | --- |
| `/approvals` | 审批队列 | 主管筛选并批量处理待审批订单 | 默认/加载/空/无结果/错误/无权限/成功/部分失败 | OrderTable, FilterBar, BulkActionBar | P0 |
| ______ | ______ | ______ | ______ | ______ | ______ |

填写要点：

- **路由**用小写 kebab，与代码路由一致；带参数的用 `/orders/:id`。
- **状态**直接引用 UI Brief 第 4 节的状态矩阵，不要漏"空/错误/无权限"。
- **关键组件**用 [组件清单](component-inventory.md) 里的组件名，不要临时造名。
- **优先级** P0=主流程必须，P1=重要，P2=可延后。第 4 步后按页循环时，按优先级排。

## 命名与路由对照（贯穿到 Figma 和代码）

| 阶段 | 命名形态 | 示例 |
| --- | --- | --- |
| 页面清单 | 路由 | `/approvals` |
| Figma Frame | 路由 + 状态 | `/approvals/empty` |
| 代码路由 | 同路由 | `/approvals` |
| 代码组件 | PascalCase | `OrderTable` |

## 相关文档

- [UI Brief 模板](ui-brief.md) · [组件清单模板](component-inventory.md)
- [Figma 体系](../imports/figma-stack.md)（Frame 命名规则）
