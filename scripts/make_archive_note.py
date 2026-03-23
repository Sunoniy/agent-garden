#!/usr/bin/env python3
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_DIR = ROOT / 'docs' / 'archives'
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
INDEX = ROOT / 'data' / 'archive-index.json'

title = sys.argv[1] if len(sys.argv) > 1 else 'untitled-discussion'
slug = title.strip().lower().replace(' ', '-').replace('/', '-')
now = datetime.utcnow().isoformat() + 'Z'
out = ARCHIVE_DIR / f'{slug}.md'

content = f'''# {title}\n\n- archivedAt: {now}\n- status: draft\n\n## Summary\n\n## Key Insights\n\n## Risks\n\n## Follow-ups\n'''
out.write_text(content, encoding='utf-8')

if INDEX.exists():
    data = json.loads(INDEX.read_text(encoding='utf-8'))
else:
    data = {'version': 1, 'archives': []}

data['archives'].append({'title': title, 'path': f'docs/archives/{slug}.md', 'archivedAt': now})
INDEX.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
print(out)
