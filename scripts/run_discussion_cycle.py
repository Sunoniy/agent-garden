#!/usr/bin/env python3
import json
import re
import uuid
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOPIC_FILE = ROOT / 'data' / 'today-topic.md'
REGISTRY_FILE = ROOT / 'community' / 'agents' / 'registry.json'
RUNS_DIR = ROOT / 'runs'


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r'\s+', '-', text)
    text = re.sub(r'[^\w\-\u4e00-\u9fff]+', '', text)
    return text[:80] or 'untitled-topic'


def read_topic() -> str:
    if not TOPIC_FILE.exists():
        return '自由讨论'
    lines = [line.strip() for line in TOPIC_FILE.read_text(encoding='utf-8').splitlines() if line.strip()]
    return lines[1] if len(lines) > 1 else '自由讨论'


def main():
    topic = read_topic()
    date_part = datetime.utcnow().strftime('%Y-%m-%d')
    slug = slugify(topic)
    run_id = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ') + '-' + uuid.uuid4().hex[:6]
    run_dir = RUNS_DIR / date_part / slug
    run_dir.mkdir(parents=True, exist_ok=True)

    registry = json.loads(REGISTRY_FILE.read_text(encoding='utf-8'))
    roles = registry['roles']

    (run_dir / 'topic.md').write_text(f'# Topic\n\n{topic}\n', encoding='utf-8')

    artifacts = {'topic': str((run_dir / 'topic.md').relative_to(ROOT))}
    statuses = {}

    for role in roles:
        out_name = role['output']
        out_path = run_dir / out_name
        role_name = role.get('name', role['id'])
        content = (
            f"# {role_name}\n\n"
            f"- roleId: {role['id']}\n"
            f"- status: stub\n\n"
            f"## Topic\n{topic}\n\n"
            f"## Notes\n"
            f"这里将来由 OpenClaw 主调度器或 sub-agent 写入真实输出。\n"
        )
        out_path.write_text(content, encoding='utf-8')
        artifacts[role['id']] = str(out_path.relative_to(ROOT))
        statuses[role['id']] = 'pending'

    final_summary = run_dir / 'final-summary.md'
    final_summary.write_text('# Final Summary\n\n待记录员生成。\n', encoding='utf-8')
    artifacts['finalSummary'] = str(final_summary.relative_to(ROOT))

    manifest = {
        'runId': run_id,
        'topic': topic,
        'createdAt': datetime.utcnow().isoformat() + 'Z',
        'participants': [r['id'] for r in roles],
        'statuses': statuses,
        'artifacts': artifacts,
        'archiveDecision': None
    }

    meta_path = run_dir / 'run-meta.json'
    meta_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'runId': run_id, 'runDir': str(run_dir), 'topic': topic}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
