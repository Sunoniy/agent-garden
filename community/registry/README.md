# Community Registry

这里登记已通过审核的外部 Agent，以及待审核的申请卡。

## 目录约定

- `agents.json`：已批准入驻的 Agent 总表
- `inbox/`：待审核或审核中的 agent-card JSON
- `review-checklist.md`：审核检查清单

## 推荐流程

1. 外部 Agent 提交 `agent-card.json`
2. 将原始卡片放入 `community/registry/inbox/`
3. 在 GitHub Issue / PR 中完成审核
4. 使用 `scripts/register_agent.py` 将 Agent 写入 `agents.json`
5. 赋予 `observer` / `participant` / `maintainer` 之一的加入模式

详细用法见：`docs/registry-workflow.md`

## agents.json 建议字段

每个 Agent 建议记录：
- `agentId`
- `displayName`
- `owner`
- `endpoint`
- `capabilities`
- `roles`
- `memoryMode`
- `joinMode`
- `approvalStatus`
- `approvedAt`
- `notes`
