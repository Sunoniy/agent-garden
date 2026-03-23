#!/usr/bin/env python3
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
COMMUNITY = ROOT / 'community'
RUNS = ROOT / 'runs'
ARCHIVES = ROOT / 'docs' / 'archives'
REGISTRY = COMMUNITY / 'agents' / 'registry.json'
TOPIC_FILE = DATA / 'today-topic.md'


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r'\s+', '-', text)
    text = re.sub(r'[^\w\-\u4e00-\u9fff]', '', text)
    return text[:80] or 'untitled-topic'


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


def read_topic() -> str:
    if not TOPIC_FILE.exists():
        return '自由讨论'
    lines = [line.strip() for line in TOPIC_FILE.read_text(encoding='utf-8').splitlines() if line.strip()]
    if len(lines) >= 2:
        return lines[1]
    return lines[0] if lines else '自由讨论'


def load_registry():
    return json.loads(REGISTRY.read_text(encoding='utf-8'))['roles']


def simulate_role_output(role, topic):
    name = role['name']
    role_id = role['id']
    if role_id == 'host':
        return f"# {name}\n\n## 议题框定\n本轮围绕“{topic}”的真正问题边界展开。\n\n## 讨论边界\n暂不进入具体外部执行。\n\n## 关键分歧点\n- 自由度与治理边界\n- 学习与沉淀如何平衡\n"
    if role_id == 'architect':
        return f"# {name}\n\n## 你的核心观点\n应采用分层社区架构处理议题、讨论与归档。\n\n## 你的分析 / 方案\n建议将议题层、讨论层、实验层、归档层拆开。\n\n## 你认为最容易被忽略的问题\n角色同质化。\n\n## 结论等级\n待验证\n"
    if role_id == 'skeptic':
        return f"# {name}\n\n## 你的核心观点\n如果没有约束机制，自由交流很快会退化为空聊。\n\n## 你的分析 / 方案\n必须要求信息增量、证据标注与归档门槛。\n\n## 你认为最容易被忽略的问题\n假繁荣。\n\n## 结论等级\n待验证\n"
    if role_id == 'experimenter':
        return f"# {name}\n\n## 你的核心观点\n应先用低成本方式验证社区节奏，再提高自治。\n\n## 你的分析 / 方案\n先跑每日议题 + 角色回应 + 归档卡片三段式。\n\n## 你认为最容易被忽略的问题\n没有真实运行闭环。\n\n## 结论等级\n待验证\n"
    return f"# {name}\n\n## 本轮讨论摘要\n围绕“{topic}”形成了初步结构化意见。\n\n## 最有价值的观点\n社区必须把讨论变成归档资产。\n\n## 仍未解决的问题\n如何把真实 OpenClaw 多 session 编排接进来。\n\n## 建议归档等级\narchive\n\n## 可复用结论\n先半自动，再逐步提高自治。\n"


def main():
    topic = read_topic()
    registry = load_registry()
    today = datetime.now().strftime('%Y-%m-%d')
    slug = slugify(topic)
    run_dir = RUNS / today / slug
    run_dir.mkdir(parents=True, exist_ok=True)

    statuses = {}
    artifacts = {}

    (run_dir / 'topic.md').write_text(f'# Topic\n\n{topic}\n', encoding='utf-8')
    artifacts['topic'] = str((run_dir / 'topic.md').relative_to(ROOT))

    for role in registry:
        statuses[role['id']] = 'running'
        out = simulate_role_output(role, topic)
        path = run_dir / role['outputFile']
        path.write_text(out, encoding='utf-8')
        statuses[role['id']] = 'done'
        artifacts[role['id']] = str(path.relative_to(ROOT))

    final_summary = (run_dir / 'recorder.md').read_text(encoding='utf-8')
    (run_dir / 'final-summary.md').write_text(final_summary, encoding='utf-8')
    artifacts['finalSummary'] = str((run_dir / 'final-summary.md').relative_to(ROOT))

    manifest = {
        'topic': topic,
        'createdAt': utc_now(),
        'participants': [r['id'] for r in registry],
        'statuses': statuses,
        'artifacts': artifacts,
        'archiveDecision': 'archive'
    }
    (run_dir / 'run-meta.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'runDir': str(run_dir), 'manifest': manifest}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
