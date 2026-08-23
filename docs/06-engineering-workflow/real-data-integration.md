# 真实数据接入

静态原型只证明结构。接入真实数据时，要把网络、权限、延迟和部分失败映射成明确的界面状态。

## 推荐契约

### 列表

```http
GET /api/orders?status=pending&query=acme&sort=-createdAt&page=1&pageSize=20
```

```json
{
  "items": [{
    "id": "ord_1024",
    "customerName": "Acme 国际供应链（华东区域）",
    "amount": 128000.5,
    "currency": "CNY",
    "status": "pending",
    "updatedAt": "2026-08-20T10:30:00Z"
  }],
  "page": 1,
  "pageSize": 20,
  "total": 86,
  "permissions": {"canApprove": true, "canExport": false}
}
```

过滤、排序和分页应写入 URL，使页面可分享、刷新后可恢复，并在返回列表时保留上下文。字段缺失与 `null` 的含义要在契约中区分；界面不得把 `0` 当成空值。

### 批量操作

```http
POST /api/orders/bulk-approve
```

```json
{
  "ids": ["ord_1024", "ord_1025"]
}
```

```json
{
  "succeeded": ["ord_1024"],
  "failed": [{"id": "ord_1025", "code": "ALREADY_PROCESSED", "message": "订单已被其他人处理"}]
}
```

部分失败必须显示成功数量、失败原因和重试/刷新入口，不能只弹一个“操作失败”。

## API 状态到 UI 状态

| 数据状态 | 页面表现 | 用户下一步 |
| --- | --- | --- |
| 请求中 | Skeleton 保留表头和布局 | 等待或取消 |
| 空集合 | 空态说明没有订单 | 创建第一条 |
| 过滤无结果 | 保留筛选条件 | 清除筛选 |
| 401/403 | 登录提示或无权限说明 | 登录、申请权限或返回 |
| 429/5xx | 错误说明和重试 | 重试，保留已填条件 |
| 网络中断 | 显示离线提示，避免覆盖旧数据 | 恢复网络后重试 |
| 部分字段缺失 | 显示“未提供”并保留可用字段 | 查看详情或补录 |
| 更新成功 | 行内状态更新 + Toast | 继续处理 |

## 更新策略

- 默认使用悲观更新：服务端确认后再改变审批状态，适合有审计要求的操作。
- 可以乐观更新低风险收藏、排序偏好，但必须提供撤销和失败回滚。
- 提交期间禁用重复提交；请求取消或切换筛选时，丢弃过期响应。
- 详情页显示更新时间，冲突时提示“数据已被更新”，让用户刷新后再提交。
- 权限在前端用于隐藏或禁用入口，后端仍必须再次校验，不能把 UI 隐藏当作安全控制。

## Mock 与 fixture

为 [Web 工作台练习](../08-practice-projects/web-workbench.md) 准备至少六组 fixture：正常长文本、空集合、过滤无结果、服务端错误、无权限、部分失败。每组都能通过 URL 或开发开关复现，并在 [页面清单](../templates/page-inventory.md) 记录覆盖的状态。

接入完成后，按 [验收清单](acceptance-checklist.md) 记录网络、权限、状态和数据长度证据。
