# 视觉验收记录模板

← 返回 [原型先行全流程主文档](../imports/prototype-first-workflow.md)

第 8 步用。用 fixture 渲染全部状态、固定视口截图后，逐条对照 PRD 验收标准，把结果记在这里。复制到 `docs/visual-acceptance.md`。方法见 [视觉评审闭环](../imports/visual-review-loop.md)。

## 验收矩阵

| 页面/状态 | 视口 | PRD 验收标准 | 预期 | 实际（截图） | 结论 | 问题分类 |
| --- | --- | --- | --- | --- | --- | --- |
| `/approvals` 默认 | 1440 | 待处理数量与列表一致，主按钮显示选中数 | 一致 | `approvals-default-1440.png` | ✅ 通过 | — |
| `/approvals` 空 | 1440 | 显示"暂无待审批订单"，主按钮禁用 | 文案+禁用 | `approvals-empty-1440.png` | ❌ 不通过 | 代码：按钮未禁用 |
| `/approvals` 空 | 375 | 手机端摘要卡片，空态文案不溢出 | 不溢出 | ______ | ______ | ______ |
| ______ | ______ | ______ | ______ | ______ | ______ | ______ |

## 问题分类与去向

| 分类 | 判定 | 回到哪一步 |
| --- | --- | --- |
| 代码问题 | 数据绑定、状态切换、样式实现错 | 第 7 步改代码 |
| 设计问题 | 信息层级、文案、缺状态 | 第 4 步迭代原型 |

> 切忌：发现不一致就整页重新生成。先分类，只改对应部分。

## 收尾

- [ ] 所有 P0 状态两档视口均通过
- [ ] 遗留问题都标了分类和去向
- [ ] 过一遍 [交付验收清单](../06-engineering-workflow/acceptance-checklist.md)

## 相关文档

- [视觉评审闭环](../imports/visual-review-loop.md) · [设计评审记录](design-review.md)
- [交付验收清单](../06-engineering-workflow/acceptance-checklist.md)
