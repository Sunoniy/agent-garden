#!/usr/bin/env python3
import json
import sys
from pathlib import Path

if len(sys.argv) < 2:
    raise SystemExit('Usage: export_run_for_github.py <run-dir>')

run_dir = Path(sys.argv[1])
meta = json.loads((run_dir / 'run-meta.json').read_text(encoding='utf-8'))
summary = (run_dir / 'final-summary.md').read_text(encoding='utf-8') if (run_dir / 'final-summary.md').exists() else '待补充'

body = f'''# {meta['topic']}\n\n## Run Info\n- runId: {meta['runId']}\n- participants: {', '.join(meta['participants'])}\n\n## Summary\n\n{summary}\n'''
print(body)
