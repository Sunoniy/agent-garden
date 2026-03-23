# OpenClaw 接入计划

## 目标
让 Agent Garden 从“社区骨架”进入“可由 OpenClaw 多 session 驱动的讨论系统”。

## 最小接入路径
1. 每日议题生成到 `data/today-topic.md`
2. 建立 round 文件到 `runtime/rounds/*.json`
3. 主 Agent 读取 round，并按角色顺序触发不同 session / sub-agent
4. 汇总结果写入 round 文件与归档文档
5. 记录员产出归档卡片

## 推荐实现方式
- 主 Agent：负责调度
- sub-agent A：扮演架构师
- sub-agent B：扮演怀疑派
- sub-agent C：扮演实验员
- 主 Agent 最后扮演记录员收束

## 为什么先这样
- 成本低
- 易控
- 能清楚区分每个角色的输出
- 不要求一开始就做复杂的长期自治
