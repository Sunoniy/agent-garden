#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / 'community' / 'agents' / 'registry.json'

if len(sys.argv) < 3:
    raise SystemExit('Usage: build_role_prompt.py <role-id> <topic> [round-id]')

role_id = sys.argv[1]
topic = sys.argv[2]
round_id = sys.argv[3] if len(sys.argv) > 3 else 'manual-round'
registry = json.loads(REGISTRY.read_text(encoding='utf-8'))['roles']
role = next((r for r in registry if r['id'] == role_id), None)
if not role:
    raise SystemExit(f'Unknown role: {role_id}')

template = (ROOT / role['promptTemplate']).read_text(encoding='utf-8')
card = (ROOT / role['card']).read_text(encoding='utf-8')
text = template.replace('{{topic}}', topic).replace('{{round_id}}', round_id)
text = text.replace('{{role_name}}', role['name'])
text = text.replace('{{roleCard}}', card).replace('{{role_card}}', card)

# derive short mission from card first non-title line fallback
mission = ''
for line in card.splitlines():
    line = line.strip()
    if line and not line.startswith('#'):
        mission = line
        break
text = text.replace('{{role_mission}}', mission)
print(text)
