# 质量门禁与自动化护栏

质量门禁的目标是**在问题进入下游前拦截**，而不是事后返工。自动化检查提供快速反馈，人工审查处理需要判断的部分。

## 设计原则

1. **左移**：越早发现问题，修复成本越低
2. **自动优先**：能自动检查的不依赖人工
3. **可执行**：每条检查项都有明确的通过/失败标准
4. **增量**：先建立基础门禁，再逐步提高标准

## 门禁分类

### 静态检查（开发时）

在代码提交前运行，IDE 和 Git Hooks 中执行。

#### 1. 代码规范

**工具**：ESLint + Prettier + Stylelint

**配置示例**（`.eslintrc.js`）：
```javascript
module.exports = {
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react/recommended',
    'plugin:jsx-a11y/recommended',
    'prettier'
  ],
  rules: {
    // 禁止硬编码颜色
    'no-restricted-syntax': [
      'error',
      {
        selector: 'Literal[value=/#[0-9a-f]{3,8}/i]',
        message: '禁止硬编码颜色，使用 Design Token'
      }
    ],
    // 禁止内联样式
    'react/forbid-dom-props': [
      'error',
      { forbid: ['style'] }
    ],
    // 必须有 aria-label
    'jsx-a11y/control-has-associated-label': 'error'
  }
}
```

**Pre-commit Hook**（`husky` + `lint-staged`）：
```json
{
  "husky": {
    "hooks": {
      "pre-commit": "lint-staged"
    }
  },
  "lint-staged": {
    "*.{ts,tsx}": ["eslint --fix", "prettier --write"],
    "*.css": ["stylelint --fix", "prettier --write"]
  }
}
```

**通过标准**：0 error，warning 数量不增加。

#### 2. 类型检查

**工具**：TypeScript strict mode

**配置**（`tsconfig.json`）：
```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "forceConsistentCasingInFileNames": true
  }
}
```

**通过标准**：`tsc --noEmit` 退出码为 0。

#### 3. Design Token 校验

**目的**：确保所有样式值来自 Token，没有硬编码。

**自定义 ESLint 规则示例**：
```javascript
// eslint-plugin-design-tokens/no-hardcoded-colors.js
module.exports = {
  meta: {
    type: 'problem',
    docs: {
      description: '禁止使用硬编码颜色值'
    }
  },
  create(context) {
    return {
      Property(node) {
        if (
          node.key.name === 'color' ||
          node.key.name === 'backgroundColor'
        ) {
          const value = node.value.value
          if (
            typeof value === 'string' &&
            (value.startsWith('#') || value.startsWith('rgb'))
          ) {
            context.report({
              node,
              message: `使用 Token 而不是硬编码颜色 "${value}"`
            })
          }
        }
      }
    }
  }
}
```

**Tailwind CSS 用户**：使用 `tailwind.config.js` 限制颜色值：
```javascript
module.exports = {
  theme: {
    colors: {
      // 只允许 Token 定义的颜色
      primary: 'var(--color-primary)',
      secondary: 'var(--color-secondary)',
      // 禁止使用原始颜色名
      red: undefined,
      blue: undefined
    }
  },
  safelist: [] // 不允许任意值
}
```

#### 4. 组件命名检查

**目的**：确保组件名与组件清单一致，避免重复造轮子。

**自定义脚本**（`scripts/check-components.js`）：
```javascript
const fs = require('fs')
const path = require('path')

// 从组件清单读取允许的组件名
const componentInventory = JSON.parse(
  fs.readFileSync('docs/component-inventory.json', 'utf-8')
)
const allowedComponents = new Set(
  componentInventory.components.map(c => c.name)
)

// 扫描 src/components 目录
const componentsDir = 'src/components'
const actualComponents = fs.readdirSync(componentsDir)

const violations = []

actualComponents.forEach(dir => {
  if (!allowedComponents.has(dir)) {
    violations.push(
      `未在组件清单中声明的组件: ${dir}，请先更新 component-inventory.json`
    )
  }
})

if (violations.length > 0) {
  console.error('❌ 组件命名检查失败:\n', violations.join('\n'))
  process.exit(1)
} else {
  console.log('✅ 组件命名检查通过')
}
```

**集成到 CI**：
```yaml
- name: Check component naming
  run: node scripts/check-components.js
```

### 动态检查（运行时）

在测试环境中运行，验证实际行为。

#### 5. 无障碍检查

**工具**：Axe + Jest + Testing Library

**集成测试示例**：
```typescript
import { render } from '@testing-library/react'
import { axe, toHaveNoViolations } from 'jest-axe'
import { ApprovalQueue } from './ApprovalQueue'

expect.extend(toHaveNoViolations)

describe('ApprovalQueue 无障碍', () => {
  it('无 WCAG 2.1 AA 违规', async () => {
    const { container } = render(<ApprovalQueue />)
    const results = await axe(container)
    expect(results).toHaveNoViolations()
  })

  it('键盘导航可用', async () => {
    const { getByRole } = render(<ApprovalQueue />)
    const firstButton = getByRole('button', { name: /批量审批/ })
    
    firstButton.focus()
    expect(document.activeElement).toBe(firstButton)
    
    // Tab 到下一个可聚焦元素
    userEvent.tab()
    expect(document.activeElement).toHaveAttribute('role', 'button')
  })

  it('屏幕阅读器标注正确', () => {
    const { getByRole } = render(<ApprovalQueue />)
    expect(getByRole('main')).toHaveAttribute('aria-label', '审批队列')
    expect(getByRole('table')).toHaveAttribute('aria-describedby')
  })
})
```

**CI 集成**：
```yaml
- name: Accessibility tests
  run: npm run test:a11y -- --coverage
```

**通过标准**：
- 0 个 serious 或 critical 级别的 axe 违规
- 主流程可完全通过键盘操作（Tab/Enter/Esc）
- 所有交互元素有可访问名称

#### 6. 视觉回归测试

**工具**：Percy / Chromatic / Playwright

**目的**：确保代码修改不会意外改变视觉呈现。

**Playwright 视觉回归示例**：
```typescript
import { test, expect } from '@playwright/test'

test.describe('视觉回归', () => {
  // 固定视口
  test.use({ viewport: { width: 1440, height: 900 } })

  test('审批队列 - 默认状态', async ({ page }) => {
    await page.goto('/approvals?fixture=default')
    await page.waitForLoadState('networkidle')
    
    // 截图对比
    await expect(page).toHaveScreenshot('approvals-default.png', {
      maxDiffPixels: 100 // 允许 100 像素差异
    })
  })

  test('审批队列 - 空数据状态', async ({ page }) => {
    await page.goto('/approvals?fixture=empty')
    await expect(page).toHaveScreenshot('approvals-empty.png')
  })

  test('审批队列 - 错误状态', async ({ page }) => {
    await page.goto('/approvals?fixture=error')
    await expect(page).toHaveScreenshot('approvals-error.png')
  })

  test('审批队列 - 响应式 (390px)', async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 })
    await page.goto('/approvals?fixture=default')
    await expect(page).toHaveScreenshot('approvals-mobile.png')
  })
})
```

**Chromatic 集成**（推荐用于团队）：
```yaml
- name: Visual regression
  uses: chromaui/action@v1
  with:
    projectToken: ${{ secrets.CHROMATIC_TOKEN }}
    autoAcceptChanges: false # 需要人工批准变更
    exitOnceUploaded: false
```

**通过标准**：
- 像素差异 < 0.1%（约 1440px 屏幕的 100 像素）
- 所有状态（8 种标准状态）都有基线截图
- 4 个标准视口（390/768/1024/1440）都通过

#### 7. 状态覆盖率

**目的**：确保所有状态矩阵中定义的状态都有对应的测试和截图。

**自定义检查脚本**：
```javascript
const stateMatrix = require('../docs/state-matrix.json')
const testFiles = require('glob').sync('**/*.test.tsx')

const requiredStates = [
  'default', 'loading', 'empty', 'no-results',
  'error', 'unauthorized', 'success', 'partial-failure'
]

const missingStates = []

stateMatrix.pages.forEach(page => {
  requiredStates.forEach(state => {
    const testName = `${page.route}-${state}`
    const hasTest = testFiles.some(file =>
      fs.readFileSync(file, 'utf-8').includes(testName)
    )
    
    if (!hasTest) {
      missingStates.push(`${page.route}: 缺少 ${state} 状态测试`)
    }
  })
})

if (missingStates.length > 0) {
  console.error('❌ 状态覆盖率不足:\n', missingStates.join('\n'))
  process.exit(1)
}
```

### 集成检查（CI/CD）

在 Pull Request 时运行，合并前必须通过。

#### 8. 测试覆盖率

**工具**：Jest / Vitest + Coverage

**配置**（`jest.config.js`）：
```javascript
module.exports = {
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.test.{ts,tsx}',
    '!src/**/*.stories.{ts,tsx}'
  ],
  coverageThresholds: {
    global: {
      statements: 80,
      branches: 75,
      functions: 80,
      lines: 80
    },
    // 关键组件更高标准
    './src/components/ApprovalQueue/**': {
      statements: 90,
      branches: 85,
      functions: 90,
      lines: 90
    }
  }
}
```

**通过标准**：
- 全局覆盖率 ≥ 80%
- 关键业务组件 ≥ 90%
- 无未测试的危险操作（删除、批量修改）

#### 9. 性能预算

**工具**：Lighthouse CI / size-limit

**配置**（`.lighthouserc.js`）：
```javascript
module.exports = {
  ci: {
    collect: {
      url: ['http://localhost:3000/approvals'],
      numberOfRuns: 3
    },
    assert: {
      assertions: {
        'categories:performance': ['error', { minScore: 0.9 }],
        'categories:accessibility': ['error', { minScore: 0.9 }],
        'first-contentful-paint': ['error', { maxNumericValue: 2000 }],
        'largest-contentful-paint': ['error', { maxNumericValue: 2500 }],
        'cumulative-layout-shift': ['error', { maxNumericValue: 0.1 }],
        'total-blocking-time': ['error', { maxNumericValue: 300 }]
      }
    }
  }
}
```

**Bundle Size 检查**（`size-limit` 配置）：
```json
{
  "size-limit": [
    {
      "name": "Initial JS",
      "path": "dist/js/main.*.js",
      "limit": "150 KB"
    },
    {
      "name": "Initial CSS",
      "path": "dist/css/main.*.css",
      "limit": "50 KB"
    }
  ]
}
```

**通过标准**：
- LCP < 2.5s
- FID < 100ms
- CLS < 0.1
- Bundle size 增量 < 50KB

#### 10. 安全扫描

**工具**：npm audit / Snyk / Dependabot

**CI 集成**：
```yaml
- name: Security audit
  run: npm audit --audit-level=high

- name: Snyk scan
  uses: snyk/actions/node@master
  env:
    SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
  with:
    args: --severity-threshold=high
```

**通过标准**：
- 0 个 high/critical 级别的漏洞
- 依赖项都在维护状态（无 deprecated packages）
- 无已知的供应链攻击风险

## 完整 CI 流水线

将所有检查集成到一条流水线，并行运行以节省时间。

```yaml
name: Quality Gate Pipeline

on:
  pull_request:
    branches: [main, develop]

jobs:
  # 并行运行的快速检查
  lint-and-type:
    name: Lint & Type Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
          cache: 'npm'
      
      - run: npm ci
      - run: npm run lint
      - run: npm run type-check
      - run: node scripts/check-components.js

  security:
    name: Security Scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
          cache: 'npm'
      
      - run: npm ci
      - run: npm audit --audit-level=high
      
      - name: Snyk scan
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}

  test:
    name: Unit & Integration Tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
          cache: 'npm'
      
      - run: npm ci
      - run: npm run test:coverage
      
      - name: Check coverage thresholds
        run: |
          COVERAGE=$(jq '.total.lines.pct' coverage/coverage-summary.json)
          if (( $(echo "$COVERAGE < 80" | bc -l) )); then
            echo "❌ Coverage $COVERAGE% < 80%"
            exit 1
          fi
          echo "✅ Coverage: $COVERAGE%"
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  a11y:
    name: Accessibility Tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
          cache: 'npm'
      
      - run: npm ci
      - run: npm run test:a11y
      
      - name: Check state coverage
        run: node scripts/check-state-coverage.js

  visual:
    name: Visual Regression
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0 # Chromatic 需要完整历史
      
      - uses: actions/setup-node@v3
        with:
          node-version: 18
          cache: 'npm'
      
      - run: npm ci
      - run: npm run build-storybook
      
      - name: Chromatic
        uses: chromaui/action@v1
        with:
          projectToken: ${{ secrets.CHROMATIC_TOKEN }}
          exitOnceUploaded: false
          autoAcceptChanges: false

  performance:
    name: Performance Budget
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
          cache: 'npm'
      
      - run: npm ci
      - run: npm run build
      
      - name: Bundle size check
        uses: andresz1/size-limit-action@v1
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Lighthouse CI
        run: |
          npm install -g @lhci/cli
          lhci autorun

  # 所有检查通过后的汇总
  quality-gate:
    name: Quality Gate Summary
    runs-on: ubuntu-latest
    needs: [lint-and-type, security, test, a11y, visual, performance]
    steps:
      - name: All checks passed
        run: |
          echo "✅ 所有质量门禁检查通过"
          echo "- 代码规范与类型检查"
          echo "- 安全扫描"
          echo "- 单元测试与覆盖率"
          echo "- 无障碍合规"
          echo "- 视觉回归"
          echo "- 性能预算"
```

## 本地开发护栏

让开发者在提交前就发现问题，而不是等 CI 失败。

### IDE 集成

**VS Code 配置**（`.vscode/settings.json`）：
```json
{
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true,
    "source.fixAll.stylelint": true
  },
  "eslint.validate": [
    "javascript",
    "typescript",
    "javascriptreact",
    "typescriptreact"
  ],
  "css.validate": false,
  "stylelint.validate": ["css", "scss", "less"]
}
```

**推荐扩展**（`.vscode/extensions.json`）：
```json
{
  "recommendations": [
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "stylelint.vscode-stylelint",
    "deque-systems.vscode-axe-linter",
    "figma.figma-vscode-extension"
  ]
}
```

### Git Hooks

**Husky 配置**：
```bash
# 安装
npm install -D husky lint-staged

# 初始化
npx husky install
npx husky add .husky/pre-commit "npx lint-staged"
npx husky add .husky/pre-push "npm run type-check && npm run test"
```

**Lint-staged 配置**（`package.json`）：
```json
{
  "lint-staged": {
    "*.{ts,tsx}": [
      "eslint --fix",
      "prettier --write",
      "jest --bail --findRelatedTests"
    ],
    "*.css": [
      "stylelint --fix",
      "prettier --write"
    ],
    "docs/**/*.md": [
      "node scripts/check-docs-completeness.js"
    ]
  }
}
```

## 门禁豁免机制

在特殊情况下，可以临时绕过某些检查，但必须留下记录和到期时间。

### 豁免请求模板

```markdown
## 质量门禁豁免请求

**请求人**: Alice
**日期**: 2026-08-24
**PR**: #123
**豁免门禁**: 测试覆盖率
**当前值**: 72% (目标 80%)
**原因**: 紧急修复生产 Bug，涉及第三方库的边界情况难以模拟
**风险**: 低，仅影响错误处理分支
**补救计划**: 
  - [ ] 2026-08-31 前补充集成测试
  - [ ] 与第三方库维护者沟通，获取测试工具
**批准人**: Bob (技术负责人)
**到期日期**: 2026-08-31
```

### 技术债务追踪

豁免通过的问题必须记录为技术债务，定期复审。

```markdown
# 技术债务登记表

| ID | 创建日期 | 问题 | 负责人 | 到期日期 | 状态 |
| --- | --- | --- | --- | --- | --- |
| TD-001 | 2026-08-24 | ApprovalQueue 覆盖率 72% | Alice | 2026-08-31 | 进行中 |
| TD-002 | 2026-08-20 | 缺少移动端视觉回归 | Carol | 2026-09-01 | 待开始 |
```

## 渐进式采用路径

不要一次性引入所有门禁，按优先级分阶段实施。

### 阶段 1：基础护栏（第 1-2 周）

- ✅ ESLint + Prettier
- ✅ TypeScript strict mode
- ✅ Pre-commit hooks
- ✅ 单元测试框架搭建

### 阶段 2：质量提升（第 3-4 周）

- ✅ 测试覆盖率要求（初始 60%，逐步提高）
- ✅ 无障碍基础检查（axe）
- ✅ 依赖安全扫描

### 阶段 3：视觉与性能（第 5-6 周）

- ✅ 视觉回归测试（先关键页面，再扩展）
- ✅ 性能预算（Lighthouse CI）
- ✅ Bundle size 监控

### 阶段 4：设计系统集成（第 7-8 周）

- ✅ Design Token 校验
- ✅ 组件命名检查
- ✅ 状态覆盖率检查

## 度量与改进

每两周回顾门禁数据，优化规则。

### 关键指标

- **误报率**：触发但经确认为误报的检查次数 / 总触发次数（目标 < 5%）
- **拦截有效性**：门禁拦截的问题数 / 生产环境发现的问题数（目标 > 10:1）
- **平均修复时间**：从门禁失败到通过的时间（目标 < 30 分钟）

### 优化示例

```markdown
## 门禁优化记录 - 2026-08-24

### 发现
- 无障碍检查误报率 12%（主要是 Axe 对第三方库的误判）
- 视觉回归因字体加载时序导致 8% 不稳定

### 行动
1. 为第三方库组件添加 axe 规则例外
2. 视觉回归测试增加字体预加载等待
3. 将 Token 校验从 warning 提升为 error

### 效果（预期）
- 误报率降至 5%
- 视觉回归稳定性提升至 99%
```

## 总结

质量门禁不是为了"卡人"，而是为了**让团队更快、更自信地交付**。记住：

1. **自动化优先**：机器做重复判断，人做需要权衡的决策
2. **快速反馈**：本地检查 < 5 秒，CI 检查 < 10 分钟
3. **可操作**：每个失败都有明确的修复路径
4. **持续优化**：用数据驱动门禁规则的调整

下一步：将这些检查集成到你的项目中，从最简单的 ESLint 开始。
