#!/usr/bin/env python3
import json
import sys
from datetime import datetime
from pathlib import Path

run_dir = Path(sys.argv[1]).resolve()
root = run_dir.parents[2] if run_dir.name else run_dir
summary_file = run_dir / 'final-summary.md'
meta_file = run_dir / 'run-meta.json'
archive_dir = root / 'docs' / 'archives'
index_file = root / 'data' / 'archive-index.json'
archive_dir.mkdir(parents=True, exist_ok=True)

if not summary_file.exists():
    raise SystemExit(f'Missing summary file: {summary_file}')
if not meta_file.exists():
    raise SystemExit(f'Missing manifest file: {meta_file}')

meta = json.loads(meta_file.read_text(encoding='utf-8'))
summary = summary_file.read_text(encoding='utf-8')
slug = run_dir.name
now = datetime.utcnow().isoformat() + 'Z'
out = archive_dir / f'{slug}.md'
out.write_text(
    f"# {meta['topic']}\n\n- archivedAt: {now}\n- roundId: {meta['roundId']}\n- source: runs/{run_dir.relative_to(root / 'runs')}\n\n{summary}\n",
    encoding='utf-8'
)

if index_file.exists():
    index = json.loads(index_file.read_text(encoding='utf-8'))
else:
    index = {'version': 1, 'archives': []}

index['archives'].append({
    'title': meta['topic'],
    'path': f'docs/archives/{slug}.md',
    'archivedAt': now,
    'roundId': meta['roundId']
})
index_file.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding='utf-8')
print(out)
