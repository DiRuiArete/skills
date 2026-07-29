#!/usr/bin/env bash
# 把仓库根目录下每个含 SKILL.md 的目录 symlink 到 ~/.claude/skills/，幂等可重复执行。
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="${HOME}/.claude/skills"

mkdir -p "$SKILLS_DIR"

linked=0
for d in "$REPO_DIR"/*/; do
  [ -f "$d/SKILL.md" ] || continue
  name="$(basename "$d")"
  target="${d%/}"
  ln -sfn "$target" "$SKILLS_DIR/$name"
  echo "linked  $name  ->  $target"
  linked=$((linked + 1))
done

echo "done: $linked skill(s) linked into $SKILLS_DIR"
