#!/usr/bin/env bash
set -euo pipefail

# Install AI Berkshire WorkBuddy skills into the local WorkBuddy skill dir.
# Default destination: ${WORKBUDDY_HOME:-$HOME/.workbuddy}/skills
# Override with: WORKBUDDY_HOME=/path/to/dir ./install-workbuddy-skills.sh

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${WORKBUDDY_SKILLS_DIR:-${WORKBUDDY_HOME:-$HOME/.workbuddy}/skills}"
PREFIX="${WORKBUDDY_SKILL_PREFIX:-}"

PY="python3"
command -v python3 >/dev/null 2>&1 || PY="python"

ARGS=()
[ -n "$PREFIX" ] && ARGS+=(--prefix "$PREFIX")

"$PY" "$ROOT/scripts/sync-workbuddy-skills.py" "${ARGS[@]}"
mkdir -p "$DEST"

for skill_dir in "$ROOT"/workbuddy-skills/*; do
  [ -d "$skill_dir" ] || continue
  name="$(basename "$skill_dir")"
  rm -rf "$DEST/$name"
  cp -R "$skill_dir" "$DEST/$name"
done

chmod +x "$ROOT"/tools/*.py "$ROOT"/tools/*.sh 2>/dev/null || true

echo "Installed WorkBuddy skills to $DEST"
echo "Restart WorkBuddy (or reload skills) to pick up new skills."
