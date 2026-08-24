# 治理与风险

AI 工具能显著提升效率，但也引入新的风险：数据泄露、合规违规、供应商依赖和不可预测的输出质量。本文提供企业级的治理框架和风险缓解措施。

## 核心原则

1. **最小权限**：只给 AI 工具访问完成任务所需的最小数据集
2. **数据分级**：敏感数据不进入外部 AI 服务
3. **可审计**：每次 AI 交互都有输入、输出、责任人的记录
4. **可回滚**：AI 生成的内容在验证前不影响生产环境
5. **供应商中立**：不依赖单一 AI 供应商的专有格式

## 数据分级与处理规则

根据敏感度对数据分级，决定能否用于 AI 训练或外部服务。

### 数据分级表

| 级别 | 定义 | 示例 | 外部 AI | 本地 AI | 截图/日志 | 保留期 |
| --- | --- | --- | --- | --- | --- | --- |
| **公开** | 已公开发布或无风险的信息 | 官网内容、公开 API | ✅ 允许 | ✅ 允许 | ✅ 允许 | 无限制 |
| **内部** | 非公开但泄露影响有限 | 内部工具名称、技术栈 | ⚠️ 脱敏后 | ✅ 允许 | ⚠️ 脱敏后 | 2 年 |
| **机密** | 泄露会影响业务竞争力 | 未发布产品、战略计划 | ❌ 禁止 | ✅ 允许 | ❌ 禁止 | 7 年 |
| **受监管** | 法律或行业要求保护的数据 | 用户个人信息、交易记录 | ❌ 禁止 | ⚠️ 需合规审批 | ❌ 禁止 | 按法规 |

### 脱敏规则

**禁止明文出现**：
- 真实用户姓名、邮箱、手机号、身份证号
- 密钥、密码、Access Token、API Secret
- 客户公司名称（B2B 场景）
- 真实交易金额、订单号、账号

**替换策略**：

```typescript
// 脱敏工具示例
const anonymize = {
  name: () => faker.name.findName(),
  email: () => faker.internet.email(),
  phone: () => '+86 138****' + faker.datatype.number({ min: 1000, max: 9999 }),
  amount: (original: number) => Math.round(original / 100) * 100, // 只保留数量级
  orderId: () => 'ORD-' + faker.random.alphaNumeric(8).toUpperCase(),
  companyName: () => faker.company.companyName()
}

// UI Fixture 使用脱敏数据
export const mockOrders = [
  {
    id: anonymize.orderId(),
    customer: anonymize.name(),
    email: anonymize.email(),
    amount: anonymize.amount(12580),
    status: 'pending' // 真实业务状态保留
  }
]
```

### 敏感文件清单

维护一份敏感文件列表，禁止 AI 工具访问：

```text
.ai-exclude
.env
.env.*
config/production.yml
secrets/
keys/
customer-data/
*.pem
*.key
*.p12
credentials.json
service-account.json
```

**Figma MCP 权限配置**：
```json
{
  "figma-mcp": {
    "allowedFiles": [
      "design-system-public",
      "ui-kit-internal"
    ],
    "deniedFiles": [
      "*-customer-*",
      "*-confidential-*"
    ]
  }
}
```

**Claude Code / Cursor 配置**（`.claudeignore` / `.cursorignore`）：
```text
# 敏感配置
.env*
config/production.*
secrets/

# 客户数据
data/customers/
reports/sensitive/

# 密钥与证书
*.pem
*.key
keys/
```

## AI 工具准入评估

引入新的 AI 工具前，必须通过以下评估。

### 评估清单

```markdown
## AI 工具准入评估表

**工具名称**: Figma Make
**供应商**: Figma Inc.
**用途**: 根据 PRD 生成交互原型
**评估日期**: 2026-08-24
**评估人**: Alice (安全团队) + Bob (技术负责人)

### 1. 数据安全
- [ ] 数据是否离开本地？ ✅ 是（Figma 云端）
- [ ] 是否用于训练模型？ ⚠️ 根据 Figma 用户协议，可选退出
- [ ] 是否支持 SSO/SAML？ ✅ 是（Enterprise 计划）
- [ ] 数据保留政策？ ✅ 删除文件后 30 天内可恢复，之后永久删除
- [ ] 是否符合 GDPR/SOC2？ ✅ 是

### 2. 访问控制
- [ ] 是否支持最小权限？ ✅ 可按文件/团队授权
- [ ] 是否有审计日志？ ✅ Enterprise 计划提供
- [ ] 是否可限制 IP/地域？ ✅ 可配置

### 3. 供应商风险
- [ ] 供应商是否有 SLA？ ✅ 99.9% 可用性（Enterprise）
- [ ] 是否有数据导出能力？ ✅ 支持 JSON/SVG/PDF 导出
- [ ] 是否依赖其他第三方服务？ ⚠️ 使用 OpenAI API（可选）

### 4. 合规
- [ ] 是否满足行业监管要求？ ✅ 已有 SOC2 Type II、ISO 27001
- [ ] 是否需要 DPA 签署？ ✅ 需要（已完成）
- [ ] 是否支持数据本地化？ ⚠️ 数据存储在 AWS 美国/欧洲区域

### 5. 成本与锁定风险
- [ ] 定价模型？ 按席位/月（$45/席位）
- [ ] 是否有供应商锁定风险？ ⚠️ 中等（设计文件可导出，但 Variables 需转换）
- [ ] 替代方案成本？ 高（迁移需 2-4 周）

### 决策
✅ **批准使用**，附加条件：
1. 只用于"内部"及以下级别数据
2. 启用 SSO 和审计日志
3. 禁用"用于训练"选项
4. 每季度复审一次使用范围

**批准人**: Carol (CISO)
**有效期**: 2026-08-24 ~ 2027-08-24
```

### 快速判断矩阵

| 工具类型 | 数据流向 | 风险等级 | 适用场景 | 示例 |
| --- | --- | --- | --- | --- |
| **本地优先** | 不离开本地 | 低 | 敏感项目、受监管行业 | Cursor (本地模式)、本地 LLM |
| **云端 - 可选退出训练** | 上传云端，不训练 | 中 | 一般企业项目 | Claude, Figma (opt-out) |
| **云端 - 用于训练** | 上传云端，用于训练 | 高 | 仅公开数据 | 免费版 ChatGPT |
| **第三方集成** | 经过第三方服务 | 高 | 需单独评估 | v0 (Vercel + OpenAI) |

## 密钥与凭证管理

AI 工具通常需要 API Key 或 Access Token，必须安全管理。

### 存储规则

❌ **禁止**：
- 硬编码在代码中
- 提交到 Git
- 存储在 Figma 文件或设计工具中
- 通过聊天记录分享

✅ **推荐**：
- 使用环境变量（本地开发）
- 使用密钥管理服务（生产环境：AWS Secrets Manager, Azure Key Vault, HashiCorp Vault）
- 使用 1Password CLI / Doppler（团队协作）

### 示例配置

**本地开发**（`.env.local`，已加入 `.gitignore`）：
```bash
FIGMA_ACCESS_TOKEN=figd_xxxxxxxxxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxx
OPENAI_API_KEY=sk-xxxxxxxxxxxx
```

**CI/CD**（GitHub Actions Secrets）：
```yaml
- name: Run AI-assisted tests
  env:
    ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
  run: npm run test:ai
```

**生产环境**（AWS Secrets Manager）：
```typescript
import { SecretsManager } from '@aws-sdk/client-secrets-manager'

const client = new SecretsManager({ region: 'us-east-1' })

const getSecret = async (secretName: string) => {
  const response = await client.getSecretValue({ SecretId: secretName })
  return JSON.parse(response.SecretString)
}

// 使用
const apiKey = await getSecret('prod/anthropic-api-key')
```

### 密钥轮换

定期更换密钥，减少泄露窗口：

- **个人 Access Token**：每 90 天轮换
- **服务账号 API Key**：每 180 天轮换
- **疑似泄露**：立即撤销并生成新密钥

**自动化轮换脚本示例**：
```bash
#!/bin/bash
# scripts/rotate-figma-token.sh

# 1. 生成新 Token（手动在 Figma 设置中）
echo "请在 Figma Settings > Personal Access Tokens 生成新 token"
read -p "输入新 token: " NEW_TOKEN

# 2. 更新 Secrets Manager
aws secretsmanager update-secret \
  --secret-id prod/figma-token \
  --secret-string "$NEW_TOKEN"

# 3. 验证新 Token
curl -H "X-Figma-Token: $NEW_TOKEN" \
  https://api.figma.com/v1/me

# 4. 撤销旧 Token（手动在 Figma 中）
echo "✅ 新 token 已生效，请在 Figma 设置中撤销旧 token"
```

## 审计与留痕

每次 AI 交互都应留下记录，用于问题追溯和合规审查。

### 审计日志格式

```json
{
  "timestamp": "2026-08-24T10:30:00Z",
  "session_id": "sess_abc123",
  "user": "alice@company.com",
  "tool": "claude-code",
  "action": "generate_component",
  "input": {
    "prompt": "实现审批队列页 /approvals",
    "context_files": ["docs/ui-brief.md", "docs/component-inventory.md"],
    "figma_frame": "https://figma.com/file/xxx?node-id=123"
  },
  "output": {
    "files_modified": ["src/pages/ApprovalQueue.tsx", "src/components/OrderTable.tsx"],
    "lines_added": 245,
    "lines_removed": 12
  },
  "review": {
    "status": "approved",
    "reviewer": "bob@company.com",
    "issues": []
  },
  "data_classification": "internal",
  "cost": {
    "input_tokens": 8500,
    "output_tokens": 3200,
    "estimated_usd": 0.85
  }
}
```

### 审计日志存储

**本地开发**：
```bash
# 每次会话后保存日志
~/.claude/sessions/2026-08-24-sess_abc123.json
```

**团队协作**：
- 推送到中心化日志系统（Elasticsearch, Splunk）
- 保留 2 年（合规要求）
- 支持按用户、项目、敏感度查询

### 关键事件告警

配置实时告警，监控异常行为：

```yaml
# 告警规则（DataDog / CloudWatch）
alerts:
  - name: 敏感数据访问
    condition: data_classification == "confidential" OR data_classification == "regulated"
    action: 
      - 发送邮件给安全团队
      - Slack 通知 #security-alerts
  
  - name: 大规模文件修改
    condition: files_modified.length > 50
    action:
      - 需要额外审批
      - 暂停自动合并
  
  - name: 异常成本
    condition: cost.estimated_usd > 10
    action:
      - 通知项目负责人
      - 记录到成本中心
```

## 许可证与知识产权

AI 生成的代码和设计可能涉及许可证和版权问题。

### 代码生成的法律风险

| 风险 | 场景 | 缓解措施 |
| --- | --- | --- |
| **训练数据污染** | AI 生成了与某开源项目高度相似的代码 | 使用代码相似度扫描工具（SonarQube, GitHub Copilot's filter） |
| **许可证不兼容** | AI 建议的依赖包使用 GPL，与你的 MIT 项目冲突 | 人工审查所有新增依赖的许可证 |
| **版权归属不明** | AI 生成内容的版权属于谁？ | 在用户协议中明确（大多数供应商声明用户拥有输出版权） |

### 依赖包许可证检查

**自动化扫描**：
```json
// package.json
{
  "scripts": {
    "check-licenses": "license-checker --onlyAllow 'MIT;Apache-2.0;BSD-2-Clause;BSD-3-Clause;ISC' --production"
  }
}
```

**CI 集成**：
```yaml
- name: Check licenses
  run: npm run check-licenses
```

**禁用许可证列表**（根据你的项目许可）：
- GPL / AGPL（强传染性，与商业产品冲突）
- 未知许可证（Unknown / UNLICENSED）
- 自定义许可证（需法务审查）

### AI 工具的用户协议

在使用前确认以下条款：

```markdown
## AI 工具用户协议检查清单

- [ ] 输出版权归属（理想：用户拥有）
- [ ] 是否用于训练（理想：可选退出）
- [ ] 数据保留期限（理想：< 90 天或用户控制）
- [ ] 责任限制（理想：供应商不对 AI 输出负责，但提供服务 SLA）
- [ ] 数据删除权（理想：用户可随时删除数据）
- [ ] 司法管辖区（注意：某些供应商仅受美国法律管辖）
```

示例：Claude 的[商业条款](https://www.anthropic.com/legal/commercial-terms)明确"你拥有输出版权"。

## 人工审查边界

AI 不能自主决策的事项，必须有人工审查。

### 必须人工审查

| 类别 | 示例 | 原因 |
| --- | --- | --- |
| **业务逻辑** | 审批规则、权限判断、计费逻辑 | AI 不理解业务语义 |
| **安全策略** | 认证机制、加密算法、访问控制 | 错误会导致重大安全事故 |
| **法律合规** | GDPR 同意流程、数据保留期 | 违规有法律后果 |
| **用户体验取舍** | 品牌色调、文案语气 | 需要人的主观判断 |
| **危险操作** | 数据删除、生产部署、权限提升 | 不可逆或影响面大 |
| **第三方依赖** | 新增 npm 包、API 调用 | 供应链安全风险 |

### 可信任 AI 输出（经验证后）

| 类别 | 示例 | 前提条件 |
| --- | --- | --- |
| **重复性代码** | CRUD 组件、表单验证 | 有完整单元测试 |
| **样式实现** | CSS/Tailwind 从设计稿 | 有视觉回归测试 |
| **文档生成** | API 文档、组件 Storybook | 人工抽查 20% |
| **测试用例** | 根据 PRD 生成测试场景 | 覆盖率达标 |

## 供应商依赖管理

避免过度依赖单一 AI 供应商。

### 多供应商策略

| 供应商 | 用途 | 备选方案 |
| --- | --- | --- |
| Figma (Make/MCP) | 原型生成、设计上下文 | Sketch + AI 插件, Penpot |
| Anthropic (Claude) | 代码生成、文档 | OpenAI, GitHub Copilot |
| OpenAI (GPT) | 产品分析、文案生成 | Anthropic, Gemini |
| Vercel (v0) | 快速原型 | 自建流程（Figma + Claude） |

### 数据可迁移性

确保关键产出物可以脱离 AI 工具独立使用：

- ✅ **设计文件**：定期导出为 Figma JSON + SVG
- ✅ **Design Token**：存储为标准 JSON，不依赖 Figma Variables
- ✅ **代码**：不使用供应商专有库（如避免 `import from '@vercel/ai'`）
- ✅ **文档**：Markdown 格式，不用供应商专有格式

### 退出计划

每个关键工具都应有退出计划：

```markdown
## Figma 退出计划

**触发条件**：
- Figma 涨价超过 50%
- 服务可用性 < 95%（连续 3 个月）
- 数据安全事件

**迁移步骤**（预计 4 周）：
1. 导出所有设计文件为 .fig + SVG
2. 将 Variables 转换为 CSS Variables（自动化脚本）
3. 迁移 Code Connect 映射到 Storybook
4. 更新团队工作流文档
5. 重新配置 MCP 连接到新工具

**成本**：约 $20,000（工时）+ $5,000（新工具年费）
**负责人**：设计系统团队
```

## 合规矩阵（按行业）

不同行业对 AI 使用有不同要求。

| 行业 | 主要法规 | AI 使用限制 | 推荐措施 |
| --- | --- | --- | --- |
| **金融** | PCI-DSS, SOX | 禁止处理信用卡号、交易密码 | 仅用于内部工具，生产代码需人工审查 |
| **医疗** | HIPAA, GDPR | 禁止处理 PHI（受保护健康信息） | 使用通过 HIPAA 认证的 AI 工具或本地部署 |
| **政府** | FedRAMP, ITAR | 数据不得离开国境 | 仅用本地 AI 或通过认证的云服务 |
| **教育** | FERPA, COPPA | 禁止学生个人信息 | 使用脱敏数据，家长同意后才处理 13 岁以下数据 |
| **一般企业** | GDPR, CCPA | 用户有权删除数据 | 确保 AI 供应商支持数据删除 |

### GDPR 合规要点

如果你的用户在欧盟：

- [ ] **数据处理协议 (DPA)**：与 AI 供应商签署
- [ ] **数据保护影响评估 (DPIA)**：高风险场景必须
- [ ] **用户同意**：明确告知"你的数据可能用于 AI 辅助开发"
- [ ] **数据删除**：用户请求删除时，也要删除 AI 工具中的副本
- [ ] **数据本地化**：某些成员国要求数据存储在欧盟境内

## 事故响应

AI 工具出现问题时的应对流程。

### 常见事故场景

| 事故 | 示例 | 响应 |
| --- | --- | --- |
| **数据泄露** | API Key 被提交到公开仓库 | 立即撤销密钥，扫描访问日志，通知安全团队 |
| **错误输出** | AI 生成了有漏洞的代码并上线 | 回滚版本，修复漏洞，复盘流程缺陷 |
| **成本失控** | AI 费用单月超出预算 300% | 暂停非关键任务，分析异常调用，设置费率限制 |
| **供应商宕机** | Figma MCP 不可用 48 小时 | 切换到手动流程，启用备选工具 |
| **合规违规** | 客户数据被误上传到 AI 服务 | 通知 DPO，启动 GDPR 通报流程（72 小时内） |

### 事故响应流程图

```text
发现事故 → 评估影响 → 立即止损 → 通知相关方 → 根因分析 → 改进措施
   ↓            ↓            ↓            ↓            ↓            ↓
 任何人      P0/P1/P2    撤销/回滚    用户/管理层   5 Why 分析   更新流程
```

### 事故复盘模板

```markdown
## AI 工具事故复盘

**事故编号**: INC-2026-08-24-001
**发现时间**: 2026-08-24 10:30 UTC
**影响等级**: P1（高）
**负责人**: Alice

### 事件描述
AI 生成的 SQL 查询在生产环境中缺少 `WHERE` 条件，导致全表扫描，数据库 CPU 飙升至 95%。

### 时间线
- 10:30 部署含 AI 生成代码的版本 v2.3.1
- 10:35 数据库告警触发
- 10:40 识别到是新部署的查询问题
- 10:45 回滚到 v2.3.0
- 10:50 服务恢复正常

### 根因分析（5 Why）
1. 为什么 SQL 查询没有 WHERE 条件？→ AI 生成时遗漏
2. 为什么 AI 会遗漏？→ Prompt 中没有明确"按用户 ID 过滤"
3. 为什么 Prompt 不完整？→ 开发者假设 AI "会理解业务逻辑"
4. 为什么没有在测试环境发现？→ 测试数据量小（1000 条），未暴露性能问题
5. 为什么没有代码审查拦截？→ 审查者信任 AI 输出，未仔细检查 SQL

### 影响
- 用户影响：约 500 个请求响应时间 > 10 秒
- 业务影响：无数据丢失，服务未中断
- 财务影响：数据库额外费用约 $50

### 改进措施
- [ ] 更新 Prompt 模板，强制包含"数据范围"约束
- [ ] 代码审查清单增加"AI 生成代码的 SQL 性能检查"
- [ ] 性能测试使用接近生产规模的数据（≥ 100 万条）
- [ ] 数据库增加慢查询告警（> 1 秒）

### 经验教训
1. 不要假设 AI "理解"业务规则，必须显式声明
2. AI 生成代码的审查标准应该更高，不是更低
3. 测试环境应模拟生产规模
```

## 成本控制

AI 服务按 Token 或请求计费，需要预算管理。

### 成本监控

**设置预算告警**：
```typescript
// 伪代码：成本跟踪
const monthlyBudget = 1000 // USD
let currentSpend = 0

const trackUsage = (tokens: number, model: string) => {
  const cost = calculateCost(tokens, model)
  currentSpend += cost
  
  if (currentSpend > monthlyBudget * 0.8) {
    alert('⚠️ AI 成本已达预算 80%')
  }
  
  if (currentSpend > monthlyBudget) {
    throw new Error('❌ AI 预算已耗尽，请联系管理员')
  }
}
```

**按项目分摊**：
```markdown
| 项目 | 本月使用 | 预算 | 使用率 |
| --- | --- | --- | --- |
| 审批工作流 | $320 | $500 | 64% ✅ |
| 客户门户 | $480 | $300 | 160% ⚠️ |
| 内部工具 | $120 | $200 | 60% ✅ |
```

### 成本优化建议

1. **缓存重复请求**：相同 Prompt 不重复调用
2. **使用更小模型**：简单任务用 Haiku/GPT-3.5
3. **压缩上下文**：只传递必要的文件和代码片段
4. **批量处理**：多个小任务合并为一个请求
5. **设置速率限制**：防止意外循环调用

## 总结检查清单

在项目中使用 AI 工具前，确认以下事项：

### 启动前
- [ ] 完成数据分级，明确哪些数据可以用于 AI
- [ ] 通过 AI 工具准入评估
- [ ] 配置密钥管理和访问控制
- [ ] 设置审计日志和成本告警
- [ ] 团队培训（数据安全、审查标准）

### 运行中
- [ ] 每次 AI 交互使用脱敏数据
- [ ] 关键代码有人工审查
- [ ] 新增依赖检查许可证
- [ ] 定期审查审计日志
- [ ] 监控成本和性能

### 定期复审
- [ ] 每季度复审 AI 工具使用范围
- [ ] 每年评估供应商合规性和定价
- [ ] 更新退出计划
- [ ] 收集事故和改进案例

通过系统化的治理，AI 工具能在安全可控的前提下显著提升效率。记住：**便利性和安全性不是二选一，而是通过正确的流程两者兼得**。
