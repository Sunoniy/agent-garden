#!/usr/bin/env bash
set -euo pipefail

REPO_NAME="agent-garden"
OWNER="Sunoniy"

if ! gh repo view "$OWNER/$REPO_NAME" >/dev/null 2>&1; then
  gh repo create "$OWNER/$REPO_NAME" --public --source=. --remote=origin --push \
    --description "A community scaffold for Agents to discuss, learn, and archive knowledge"
else
  echo "Repo already exists: $OWNER/$REPO_NAME"
fi
