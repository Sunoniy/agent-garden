#!/usr/bin/env python3
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
data = json.loads(path.read_text(encoding='utf-8'))

lines = []
lines.append(f"# Round {data['roundId']}")
lines.append('')
lines.append(f"- Topic: {data['topic']}")
lines.append(f"- Mode: {data.get('mode', 'unknown')}")
lines.append(f"- Created: {data['createdAt']}")
lines.append('')
lines.append('## Stages')
for stage in data.get('stages', []):
    lines.append(f"- `{stage['agent']}` · {stage['purpose']} · {stage['status']}")
print('\n'.join(lines))
