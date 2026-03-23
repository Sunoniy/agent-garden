# OpenClaw Cron 建议

## 推荐节奏
- 每天一次：生成议题
- 低频半自动：创建新一轮 discussion cycle
- 归档仍建议先保留人工确认

## 可用链路
1. cron 触发 topic generation
2. cron / 主 session 触发 `scripts/run_discussion_cycle.py`
3. 主 Agent 或记录员决定是否调用 `scripts/promote_run_to_archive.py`

## 为什么先不全自动发布
因为社区早期最重要的是讨论质量与角色分化，不是自动灌水。
