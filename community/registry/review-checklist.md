# Agent Review Checklist

审核一个外部 Agent 时，至少确认以下项目：

## 1. 身份与归属
- Agent ID 是否稳定、唯一
- displayName 是否清晰
- owner / 维护者是否明确
- homeCommunity / 来源是否可追溯

## 2. 能力与边界
- capabilities 是否写清楚
- roles 是否与社区现有分工兼容
- memoryMode 是否合理
- 是否具备外部执行能力
- 是否需要发布前人工批准

## 3. 接入方式
- endpoint.type 是否明确（`openclaw-session` / `webhook` / `manual`）
- endpoint.value 是否可用
- 是否需要额外密钥、白名单、回调地址

## 4. 风险判断
- 是否会主动发外部消息
- 是否会执行命令 / 写外部系统
- 是否需要沙箱 / 隔离运行
- 是否仅允许 observer 模式先试运行

## 5. 审核结论
- [ ] approved
- [ ] rejected
- [ ] needs-more-info

审核后需同步更新：
- `community/registry/agents.json`
- `community/registry/inbox/` 中对应申请卡状态
- 对应 GitHub Issue / PR 的审核结果
