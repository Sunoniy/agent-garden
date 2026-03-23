#!/usr/bin/env python3
import json
import uuid
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
RUNTIME = ROOT / 'runtime'
ROUNDS = RUNTIME / 'rounds'
TOPIC_FILE = DATA / 'today-topic.md'
STATE_FILE = RUNTIME / 'community-state.json'

text = TOPIC_FILE.read_text(encoding='utf-8') if TOPIC_FILE.exists() else '# Today Topic\n\n自由讨论\n'
lines = [line.strip() for line in text.splitlines() if line.strip()]
topic = lines[1] if len(lines) > 1 else '自由讨论'
round_id = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ') + '-' + uuid.uuid4().hex[:6]

round_data = {
    'roundId': round_id,
    'topic': topic,
    'createdAt': datetime.utcnow().isoformat() + 'Z',
    'mode': 'local-simulated',
    'participants': ['host', 'architect', 'skeptic', 'experimenter', 'recorder'],
    'stages': [
        {'agent': 'host', 'purpose': 'frame-topic', 'status': 'pending'},
        {'agent': 'architect', 'purpose': 'propose-structure', 'status': 'pending'},
        {'agent': 'skeptic', 'purpose': 'challenge-assumptions', 'status': 'pending'},
        {'agent': 'experimenter', 'purpose': 'propose-validation', 'status': 'pending'},
        {'agent': 'recorder', 'purpose': 'summarize-and-archive', 'status': 'pending'}
    ]
}

ROUNDS.mkdir(parents=True, exist_ok=True)
out = ROUNDS / f'{round_id}.json'
out.write_text(json.dumps(round_data, ensure_ascii=False, indent=2), encoding='utf-8')

state = json.loads(STATE_FILE.read_text(encoding='utf-8')) if STATE_FILE.exists() else {}
state['currentRound'] = round_id
state['lastTopic'] = topic
state['updatedAt'] = datetime.utcnow().isoformat() + 'Z'
STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')

print(json.dumps(round_data, ensure_ascii=False, indent=2))
