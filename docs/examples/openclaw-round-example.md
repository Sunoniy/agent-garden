# OpenClaw Round Example

当前推荐的真实接入路径：

1. 主调度器读取 `data/today-topic.md`
2. 生成一轮 `runs/YYYY-MM-DD/<topic-slug>/`
3. 为每个角色构造独立 prompt
4. 用 OpenClaw sub-agent 或其他 session 扮演角色
5. 将角色输出写回 run 目录
6. 记录员生成 `final-summary.md`
7. 再把这一轮提升到 `docs/archives/`

在完全接通真实 sub-agent 之前，`scripts/run_openclaw_round_stub.py` 提供了一条近似的本地演练路径。
