#!/usr/bin/env python3
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / 'data' / 'archive-index.json'
ARCHIVE_DIR = ROOT / 'docs' / 'archives'
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

if len(sys.argv) < 2:
    raise SystemExit('Usage: promote_run_to_archive.py <run-dir>')

run_dir = Path(sys.argv[1]).resolve()
meta = json.loads((run_dir / 'run-meta.json').read_text(encoding='utf-8'))
summary_path = run_dir / 'final-summary.md'
summary = summary_path.read_text(encoding='utf-8') if summary_path.exists() else '待补充总结'
slug = run_dir.name
out = ARCHIVE_DIR / f'{slug}.md'

content = f'''# {meta['topic']}\n\n- archivedAt: {datetime.utcnow().isoformat()}Z\n- sourceRun: {run_dir.relative_to(ROOT)}\n- conclusionLevel: tentative\n\n{summary}\n'''
out.write_text(content, encoding='utf-8')

data = json.loads(INDEX.read_text(encoding='utf-8')) if INDEX.exists() else {'version': 1, 'archives': []}
data['archives'].append({
    'title': meta['topic'],
    'path': str(out.relative_to(ROOT)),
    'archivedAt': datetime.utcnow().isoformat() + 'Z',
    'sourceRun': str(run_dir.relative_to(ROOT)),
    'level': 'tentative'
})
INDEX.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
print(out)
