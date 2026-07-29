#!/usr/bin/env bash
# 把 skill 目录 symlink 到 ~/.claude/skills/。
# 用法：./install.sh              安装全部
#       ./install.sh product-thinking [其他名字…]   只装指定的
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="${HOME}/.claude/skills"

mkdir -p "$SKILLS_DIR"

linked=0
for d in "$REPO_DIR"/*/; do
  [ -f "$d/SKILL.md" ] || continue
  name="$(basename "$d")"
  if [ "$#" -gt 0 ]; then
    case " $* " in
      *" $name "*) ;;
      *) continue ;;
    esac
  fi
  ln -sfn "${d%/}" "$SKILLS_DIR/$name"
  echo "linked  $name  ->  ${d%/}"
  linked=$((linked + 1))
done

if [ "$linked" -eq 0 ]; then
  echo "no matching skills. available:"
  for d in "$REPO_DIR"/*/; do
    [ -f "$d/SKILL.md" ] && echo "  $(basename "$d")"
  done
  exit 1
fi

echo "done: $linked skill(s) linked into $SKILLS_DIR"
