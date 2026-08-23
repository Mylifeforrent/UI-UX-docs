# 练习项目：企业 Web 工作台

这是本仓库的主练习，建议用 1--2 周完成。目标是独立交付一个可评审、可接数据、可验收的订单审批工作台，而不是只画一张漂亮首页。

## 业务设定

运营专员负责筛选和编辑订单；主管负责审批；审计员只能查看历史。订单包含客户、金额、状态、更新时间和审批记录。状态为 `draft`、`pending`、`approved`、`rejected`、`cancelled`。

| 角色 | 可做的事 |
| --- | --- |
| 运营专员 | 查看、创建、编辑草稿、提交审批 |
| 主管 | 查看、审批、驳回、查看审计记录 |
| 审计员 | 查看详情和历史，不可修改 |

## 页面范围

- `/orders`：筛选、排序、分页、列设置、批量操作、空态和错误态。
- `/orders/:id`：摘要、字段、审批时间线、关联对象和危险操作。
- `/orders/new`、`/orders/:id/edit`：分组表单、字段校验、草稿、离开保护。
- `/approvals`：待审批队列、批量审批、部分失败和审计入口。

先完成 [信息架构](../02-web-design/information-architecture.md)，再填写 [UI Brief](../templates/ui-brief.md)、[页面清单](../templates/page-inventory.md) 和 [组件清单](../templates/component-inventory.md)。

## 必须覆盖的状态

```text
loading → ready → empty / no-result / error / no-permission
提交中 → 成功 / 失败 / 部分失败
```

测试数据必须包含：长客户名、金额为 0、缺失可选字段、重复更新时间、超长备注和权限不同的用户。接口和部分失败示例见 [真实数据接入](../06-engineering-workflow/real-data-integration.md)。

## 交付节奏

| 时间盒 | 产出 | 通过标准 |
| --- | --- | --- |
| 2 小时 | 角色、对象、任务、权限表 | 每个任务有完成和失败恢复 |
| 1 天 | 页面清单和灰度线框 | 主任务、入口、状态可读 |
| 1--2 天 | Token、组件和高保真原型 | 组件状态和响应式行为明确 |
| 2--4 天 | 前端页面与 fixture | 所有状态可复现 |
| 1--2 天 | API/mock 接入 | 筛选、分页、批量操作正确 |
| 1 天 | 视觉、键盘和响应式验收 | [验收清单](../06-engineering-workflow/acceptance-checklist.md) 无高严重级别问题 |

## 提交物

- [UI Brief](../templates/ui-brief.md)、[页面清单](../templates/page-inventory.md)、[组件清单](../templates/component-inventory.md)。
- 原型链接或截图、Token 文件、页面代码和 fixture。
- API 状态映射、键盘 walkthrough、四个固定视口截图。
- [设计评审记录](../templates/design-review.md) 和 [视觉验收记录](../templates/visual-acceptance.md)。

## 评分标准

| 项目 | 权重 | 合格线 |
| --- | ---: | --- |
| 业务流程与信息架构 | 25% | 角色、权限、失败恢复完整 |
| 视觉层级与一致性 | 20% | Token 和组件复用，主任务清晰 |
| 状态与数据行为 | 25% | 7 类页面状态和部分失败可操作 |
| 响应式与无障碍 | 20% | 桌面/手机不溢出，主流程可键盘完成 |
| 证据与复盘 | 10% | 截图、问题记录和修复前后对比齐全 |

实现顺序参见 [原型到代码](../06-engineering-workflow/prototype-to-code.md)，最终按 [交付验收](../06-engineering-workflow/acceptance-checklist.md) 关闭项目。
