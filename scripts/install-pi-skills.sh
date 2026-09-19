#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${PI_SKILLS_DIR:-$HOME/.pi/agent/skills}"

# Pi uses the Agent Skills package format, so reuse the generated packages that
# are also installed for Codex. The source workflows remain skills/*.md.
python3 "$ROOT/scripts/sync-codex-skills.py"
mkdir -p "$DEST"

for skill_dir in "$ROOT"/codex-skills/*; do
  [ -d "$skill_dir" ] || continue
  name="$(basename "$skill_dir")"
  rm -rf "$DEST/$name"
  cp -R "$skill_dir" "$DEST/$name"
done

chmod +x "$ROOT"/tools/*.py "$ROOT"/tools/*.sh 2>/dev/null || true

echo "Installed Pi skills to $DEST"
echo "Restart Pi to discover the new skills."
