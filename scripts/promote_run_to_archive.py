#!/usr/bin/env python3
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / 'data' / 'archive-index.json'
ARCHIVES = ROOT / 'docs' / 'archives'

run_dir = Path(sys.argv[1]).resolve()
summary = run_dir / 'final-summary.md'
manifest = run_dir / 'run-meta.json'
if not summary.exists() or not manifest.exists():
    raise SystemExit('run is incomplete')

meta = json.loads(manifest.read_text(encoding='utf-8'))
slug = run_dir.name
out = ARCHIVES / f'{slug}.md'
ARCHIVES.mkdir(parents=True, exist_ok=True)
now = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

body = f"# {meta['topic']}\n\n- archivedAt: {now}\n- sourceRun: {run_dir.relative_to(ROOT)}\n- archiveDecision: {meta.get('archiveDecision')}\n\n" + summary.read_text(encoding='utf-8')
out.write_text(body, encoding='utf-8')

index = json.loads(INDEX.read_text(encoding='utf-8')) if INDEX.exists() else {'version': 1, 'archives': []}
index['archives'].append({
    'title': meta['topic'],
    'path': str(out.relative_to(ROOT)),
    'sourceRun': str(run_dir.relative_to(ROOT)),
    'archivedAt': now,
    'decision': meta.get('archiveDecision', 'hold')
})
INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding='utf-8')
print(out)
