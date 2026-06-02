#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_NAME="embodied-ai-textbook-editorial"
SRC_DIR="$ROOT_DIR/skills/$SKILL_NAME"

CODEX_HOME_DIR="${CODEX_HOME:-$HOME/.codex}"
DEST_ROOT="$CODEX_HOME_DIR/skills"
DEST_DIR="$DEST_ROOT/$SKILL_NAME"

if [[ ! -f "$SRC_DIR/SKILL.md" ]]; then
  echo "Missing skill source: $SRC_DIR/SKILL.md" >&2
  exit 1
fi

mkdir -p "$DEST_ROOT"
rm -rf "$DEST_DIR"
cp -R "$SRC_DIR" "$DEST_DIR"

echo "Installed project skill:"
echo "$DEST_DIR"
