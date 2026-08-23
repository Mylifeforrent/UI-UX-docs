# App 设计

App 设计单独成类，因为触控、屏幕尺寸、系统导航、生命周期和权限模型都不同于 Web。共享业务模型和 [Design Token](../04-design-system/tokens.md)，但重新设计任务入口和交互。

推荐顺序：

1. [信息架构](information-architecture.md)：从 Web 工作台抽取一个高频移动任务。
2. [导航与手势](navigation-gestures.md)：定义返回栈、中断恢复和手势替代方案。
3. [平台适配](platform-adaptation.md)：记录 iOS/Android、安全区、权限、键盘和通知差异。
4. 完成 [移动端配套应用](../08-practice-projects/mobile-companion.md)。

先完成 Web 主线，再把同一业务流程压缩成移动端任务，不要直接把桌面后台缩小。
