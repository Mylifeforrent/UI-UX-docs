# 后端工程师 UI/UX 提效知识库

这是一套面向后端开发工程师的 **Web 优先 UI/UX 学习与交付工作流**。目标不是把你训练成全职视觉设计师，而是让你能独立完成企业产品中常见的页面分析、界面设计、交互定义、原型评审和 AI 辅助前端实现。

## 你会得到什么

完成主线后，你应该能：

- 从 PRD 提取角色、对象、任务、权限和页面状态。
- 设计企业 Web 中最常见的列表、详情、表单、审批和监控页面。
- 用 [Design Token](docs/04-design-system/tokens.md) 和 [组件规范](docs/04-design-system/components.md) 保持一致性。
- 用 Figma/Figma Make 建立视觉和交互上下文，再通过 [Figma MCP](docs/05-ai-design-workflow/figma-stack.md) 交给 Coding Agent。
- 接入真实 API，处理加载、空数据、错误、权限、部分失败和响应式变化。
- 用 [验收清单](docs/06-engineering-workflow/acceptance-checklist.md) 和截图证据完成视觉、键盘与数据验收。

核心路线：

```text
PRD → 信息架构 → 页面清单 → UI Brief → 灰度结构
→ Design Token/组件 → Figma/AI 原型 → AI Coding
→ API/真实数据 → 响应式与无障碍验收
```

仓库用“企业订单/审批工作台”作为贯穿案例，文档中的关键词尽量直接链接到对应的真实文件，方便边读边操作。

## 最快上手

1. 先看 [8 周学习路线](docs/00-learning-path/README.md)，按产出推进，不先收集工具。
2. 进入 [Web 设计](docs/02-web-design/README.md)，先读 [信息架构](docs/02-web-design/information-architecture.md) 和 [企业 SaaS 页面](docs/02-web-design/enterprise-saas.md)。
3. 复制 [UI Brief](docs/templates/ui-brief.md)、[页面清单](docs/templates/page-inventory.md) 和 [组件清单](docs/templates/component-inventory.md)。
4. 用 [PRD 到原型](docs/06-engineering-workflow/prd-to-prototype.md) 产出灰度线框和状态矩阵。
5. 阅读 [Figma 体系](docs/05-ai-design-workflow/figma-stack.md)；想直接跑通全流程，用 [原型先行全流程实操](docs/05-ai-design-workflow/prototype-first-workflow.md)，再进入 [原型到代码](docs/06-engineering-workflow/prototype-to-code.md)。
6. 按 [真实数据接入](docs/06-engineering-workflow/real-data-integration.md) 接 fixture/API，最后完成 [Web 工作台练习](docs/08-practice-projects/web-workbench.md)。
7. 用 [视觉验收记录](docs/templates/visual-acceptance.md) 留下截图和问题证据。

## 按场景阅读

| 目标 | 入口 |
| --- | --- |
| 视觉层级、布局、无障碍基础 | [基础能力](docs/01-foundations/README.md) |
| 企业后台、SaaS、运营系统 | [Web 设计](docs/02-web-design/README.md) |
| iOS/Android 配套 App | [App 设计](docs/03-app-design/README.md) |
| 颜色、间距、组件和页面模式 | [Design System](docs/04-design-system/README.md) |
| Figma、Figma Make、MCP、AI Coding | [AI 设计工作流](docs/05-ai-design-workflow/README.md) |
| 从 PRD 落到前端代码和 API | [工程工作流](docs/06-engineering-workflow/README.md) |
| 选择和评估工具 | [工具定位](docs/07-tools/README.md) |
| 完整交付练习 | [练习项目](docs/08-practice-projects/README.md) |

## 可复制资产

- [UI Brief](docs/templates/ui-brief.md)
- [页面清单](docs/templates/page-inventory.md)
- [组件清单](docs/templates/component-inventory.md)
- [设计评审记录](docs/templates/design-review.md)
- [视觉验收记录](docs/templates/visual-acceptance.md)

## 文档维护

所有本地文档链接使用相对路径。新增主题时，同时在所属目录的 `README.md` 增加入口；关键字应链接到具体正文或模板，而不是只写成不可点击的工具名。运行下面的检查，脚本会报告缺失文件、空 Markdown 和不存在的标题锚点：

```bash
python3 scripts/check-doc-links.py
```

外部产品能力（例如 Figma AI、Figma Make）只引用官方入口，不把会变化的产品功能当作仓库内固定事实。
