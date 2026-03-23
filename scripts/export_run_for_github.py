#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
run_dir = Path(sys.argv[1]).resolve()
manifest = json.loads((run_dir / 'run-meta.json').read_text(encoding='utf-8'))
topic = manifest['topic']
summary = (run_dir / 'final-summary.md').read_text(encoding='utf-8')

body = []
body.append(f'# {topic}')
body.append('')
body.append('## Summary')
body.append('')
body.append(summary)
body.append('')
body.append('## Artifacts')
for key, value in manifest.get('artifacts', {}).items():
    body.append(f'- {key}: `{value}`')

out = run_dir / 'github-discussion.md'
out.write_text('\n'.join(body), encoding='utf-8')
print(out)
