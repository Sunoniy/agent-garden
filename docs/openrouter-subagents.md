# OpenRouter 子代理配置说明

主人已明确要求：后续 Agent Garden 派出的工蜂优先使用 OpenRouter 模型，而不是默认主模型。

目标模型：
- provider: OpenRouter
- model: `stepfun/step-3.5-flash:free`

## 推荐接法

### 方案 A：网关默认 subagents 切换
在 OpenClaw 配置里把：
- `models.providers.openrouter`
- `agents.defaults.subagents.model.primary`

补进去。

### 方案 B：Agent Garden 调度器显式指定
在 `sessions_spawn(...)` 时显式传：
- `model: openrouter/stepfun/step-3.5-flash:free`

这比依赖全局默认更稳。

## 推荐结论
优先同时做：
1. **网关全局接入 OpenRouter provider**
2. **Agent Garden 派工时显式指定模型**

这样即使默认模型未来再改，社区工蜂仍会稳定走指定线路。
