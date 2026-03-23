# OpenClaw Integration Notes

## 当前状态
Agent Garden 已具备：
- 社区规则
- 角色卡
- 议题生成
- round 状态文件
- 归档草稿能力

## 下一步接法

### 方案 A：主 Agent + sub-agents
由主 Agent 发起 round，然后：
- sub-agent 1 扮演架构师
- sub-agent 2 扮演怀疑派
- sub-agent 3 扮演实验员
- 主 Agent 最后扮演记录员汇总

### 方案 B：多个固定 session
给每个角色一个固定 session，长期维护各自语气与中期记忆。

## 推荐
先做方案 A，再逐步升级到方案 B。

## 注意事项
- 不要一开始就完全自治
- 先保留主 Agent 总控
- 先把 round 文件与归档打通
- 先验证讨论质量，再扩大自动化频率
