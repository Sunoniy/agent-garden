#!/usr/bin/env python3
import json
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS_DIR = ROOT / 'runs'
TOPIC_FILE = ROOT / 'data' / 'today-topic.md'
REGISTRY = ROOT / 'community' / 'agents' / 'registry.json'


def read_topic():
    if not TOPIC_FILE.exists():
        return '自由讨论'
    lines = [line.strip() for line in TOPIC_FILE.read_text(encoding='utf-8').splitlines() if line.strip()]
    return lines[1] if len(lines) > 1 else '自由讨论'


def run(cmd):
    return subprocess.check_output(cmd, text=True)


def main():
    # create run skeleton first
    out = run(['python3', str(ROOT / 'scripts' / 'run_discussion_cycle.py')])
    info = json.loads(out)
    run_dir = Path(info['runDir'])
    run_id = info['runId']
    topic = info['topic']

    registry = json.loads(REGISTRY.read_text(encoding='utf-8'))['roles']
    meta_path = run_dir / 'run-meta.json'
    meta = json.loads(meta_path.read_text(encoding='utf-8'))

    for role in registry:
        prompt = run(['python3', str(ROOT / 'scripts' / 'build_role_prompt.py'), role['id'], topic, run_id])
        status = 'done'
        content = f"# {role['name']}\n\n> round: {run_id}\n\n{prompt}\n\n---\n\n当前为 OpenClaw 接入前的占位运行输出。下一步将替换为真实 sub-agent 返回内容。\n"
        (run_dir / role['output']).write_text(content, encoding='utf-8')
        meta['statuses'][role['id']] = status

    recorder_path = run_dir / 'recorder.md'
    (run_dir / 'final-summary.md').write_text(recorder_path.read_text(encoding='utf-8'), encoding='utf-8')
    meta['archiveDecision'] = 'archive'
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding='utf-8')

    print(json.dumps({'runId': run_id, 'runDir': str(run_dir), 'topic': topic, 'mode': 'openclaw-stub'}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
