#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

python3 scripts/generate_daily_topic.py
python3 scripts/run_discussion_cycle.py
latest_run="$(find runs -type f -name run-meta.json | sort | tail -n 1 | xargs dirname)"
python3 scripts/promote_run_to_archive.py "$latest_run"

echo "Daily cycle completed: $latest_run"
