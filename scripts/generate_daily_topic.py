#!/usr/bin/env python3
import json
import random
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
TOPICS_FILE = DATA / 'topics.json'
TODAY_FILE = DATA / 'today-topic.md'
LOG_FILE = DATA / 'topic-log.jsonl'

with TOPICS_FILE.open('r', encoding='utf-8') as f:
    topics = json.load(f).get('seedTopics', [])

if not topics:
    raise SystemExit('No seed topics found')

topic = random.choice(topics)
now = datetime.utcnow().isoformat() + 'Z'

TODAY_FILE.write_text(f'# Today Topic\n\n{topic}\n\nGenerated at: {now}\n', encoding='utf-8')
with LOG_FILE.open('a', encoding='utf-8') as f:
    f.write(json.dumps({'generatedAt': now, 'topic': topic}, ensure_ascii=False) + '\n')

print(topic)
