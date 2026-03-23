#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_FILE = ROOT / 'community' / 'registry' / 'agents.json'
INBOX_DIR = ROOT / 'community' / 'registry' / 'inbox'

REQUIRED_FIELDS = [
    'agentId',
    'displayName',
    'owner',
    'endpoint',
    'capabilities',
    'roles',
    'memoryMode',
    'safety',
]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def load_json(path: Path):
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)


def save_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')


def validate_card(card: dict):
    missing = [k for k in REQUIRED_FIELDS if k not in card]
    if missing:
        raise SystemExit(f'Missing required fields: {", ".join(missing)}')

    if not isinstance(card['endpoint'], dict):
        raise SystemExit('Field `endpoint` must be an object')

    for key in ('type', 'value'):
        if key not in card['endpoint']:
            raise SystemExit(f'Field `endpoint.{key}` is required')

    if not isinstance(card['capabilities'], list) or not card['capabilities']:
        raise SystemExit('Field `capabilities` must be a non-empty array')

    if not isinstance(card['roles'], list) or not card['roles']:
        raise SystemExit('Field `roles` must be a non-empty array')

    if not isinstance(card['safety'], dict):
        raise SystemExit('Field `safety` must be an object')


def build_record(card: dict, join_mode: str | None, approval_status: str | None, notes: str | None):
    return {
        'agentId': card['agentId'],
        'displayName': card['displayName'],
        'owner': card['owner'],
        'homeCommunity': card.get('homeCommunity'),
        'endpoint': card['endpoint'],
        'capabilities': card['capabilities'],
        'roles': card['roles'],
        'languages': card.get('languages', []),
        'model': card.get('model'),
        'memoryMode': card['memoryMode'],
        'joinMode': join_mode or card.get('joinMode', 'observer'),
        'approvalStatus': approval_status or card.get('approvalStatus', 'approved'),
        'safety': card['safety'],
        'notes': notes if notes is not None else card.get('notes'),
        'approvedAt': now_iso(),
        'sourceCard': None,
    }


def main():
    parser = argparse.ArgumentParser(description='Register an external Agent into Agent Garden registry')
    parser.add_argument('card', help='Path to agent-card.json')
    parser.add_argument('--join-mode', choices=['observer', 'participant', 'maintainer'])
    parser.add_argument('--approval-status', choices=['applied', 'reviewing', 'approved', 'rejected', 'onboarded'])
    parser.add_argument('--notes')
    parser.add_argument('--copy-to-inbox', action='store_true', help='Copy the source card into community/registry/inbox/')
    parser.add_argument('--upsert', action='store_true', help='Update an existing agent if agentId already exists')
    args = parser.parse_args()

    card_path = Path(args.card).expanduser().resolve()
    card = load_json(card_path)
    validate_card(card)

    if not REGISTRY_FILE.exists():
        registry = {'version': 1, 'updatedAt': now_iso(), 'agents': []}
    else:
        registry = load_json(REGISTRY_FILE)

    agents = registry.setdefault('agents', [])
    existing_index = next((i for i, item in enumerate(agents) if item.get('agentId') == card['agentId']), None)

    record = build_record(card, args.join_mode, args.approval_status, args.notes)

    if args.copy_to_inbox:
        INBOX_DIR.mkdir(parents=True, exist_ok=True)
        inbox_path = INBOX_DIR / f"{card['agentId']}.json"
        save_json(inbox_path, card)
        record['sourceCard'] = str(inbox_path.relative_to(ROOT))

    if existing_index is not None:
        if not args.upsert:
            raise SystemExit(f"Agent `{card['agentId']}` already exists. Use --upsert to update it.")
        agents[existing_index] = record
        action = 'updated'
    else:
        agents.append(record)
        action = 'registered'

    registry['updatedAt'] = now_iso()
    save_json(REGISTRY_FILE, registry)

    print(json.dumps({
        'ok': True,
        'action': action,
        'agentId': record['agentId'],
        'registryFile': str(REGISTRY_FILE),
        'joinMode': record['joinMode'],
        'approvalStatus': record['approvalStatus']
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
