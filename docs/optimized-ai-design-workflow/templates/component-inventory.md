# 组件清单模板

← 返回 [原型先行全流程主文档](../imports/prototype-first-workflow.md)

列出本页需要的每个组件，及其状态、键盘行为和令牌映射。这份清单是防止"AI 到处新建同义组件"的关键——生成原型和写代码时都要对照它。复制到 `docs/component-inventory.md`。

| 组件名 | 职责 | 状态/变体 | 键盘行为 | 令牌映射 | 复用来源 |
| --- | --- | --- | --- | --- | --- |
| `OrderTable` | 展示订单列表，支持多选 | 默认/加载(骨架)/空/错误；行 hover、选中 | 上下箭头移动行焦点，空格选中，Enter 打开详情 | `--color-border`, `--space-2`, `--radius-md` | 项目组件库 |
| `StatusBadge` | 订单状态标签 | 待审批/已批准/已驳回/部分失败 | 不可聚焦（纯展示） | `--color-status-*` 语义令牌 | 项目组件库 |
| `BulkActionBar` | 批量操作栏，常显选中数 | 默认/禁用(无选中) | Tab 进入，Enter 触发主操作 | `--color-surface`, `--space-3` | 新建（填补空缺） |
| `ConfirmDialog` | 危险操作二次确认 | 默认/提交中/错误 | 打开时聚焦首个输入，Esc 关闭，焦点陷阱 | `--color-danger`, `--radius-lg` | 项目组件库 |
| ______ | ______ | ______ | ______ | ______ | ______ |

## 各列填写要点

- **组件名**：PascalCase，与代码一致。优先复用已有组件，只有真缺才写"新建"。
- **状态/变体**：把 UI Brief 页面状态落到组件级——表格的空态、加载态属于 `OrderTable`。
- **键盘行为**：企业级必填。焦点顺序、快捷键、Esc/Enter/空格语义、焦点陷阱（对话框）。参考 [Design Token](../04-design-system/tokens.md) 与无障碍要求。
- **令牌映射**：组件用哪些令牌。写清后，代码生成时不会出现临时颜色/间距（见 [tokens.md](../04-design-system/tokens.md)）。
- **复用来源**：`项目组件库` / `设计系统` / `新建`。凡"新建"都要在评审时确认是否真有必要。

## 防同义组件规则

生成原型或写代码前，把这份清单连同一句约束一起喂给 AI：

```text
只使用组件清单里已定义的组件，禁止新建同义组件；确需新增时先说明理由并等我确认。
```

## 相关文档

- [UI Brief 模板](ui-brief.md) · [页面清单模板](page-inventory.md)
- [Design Token](../04-design-system/tokens.md) · [Prompt 与上下文](../imports/prompting-and-context.md)
