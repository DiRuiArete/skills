#!/usr/bin/env python3
"""结构不变量 + token 预算 lint。

用法：python3 scripts/lint-skills.py [repo_root]

检查项：
  1. 每个 skills/<name>/ 有 SKILL.md，frontmatter 含 name/description/version，
     name 与目录名一致，且 disable-model-invocation: true
  2. SKILL.md 引用的每个 flows/*.md 存在；flows/ 无孤儿文件
  3. flow 里指向的 references/*.md、templates/*.md 存在；references/templates 无孤儿
  4. 字符预算：SKILL.md ≤5500，单 flow ≤3500，单 reference ≤4500，
     单交互路径峰值（SKILL + 最大 flow + 最大 reference）≤12000
  5. skills/ 下任何 .md 不得残留拼音命名（人名只以中文出现在内容里）
"""
import pathlib
import re
import sys

BUDGET_SKILL = 5500
BUDGET_FLOW = 3500
BUDGET_REF = 4500
BUDGET_PATH_PEAK = 12000
BANNED_STRINGS = ("lixiang", "liangning")


def frontmatter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    d = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            d[k.strip()] = v.strip().strip('"')
    return d


def md_files(d: pathlib.Path):
    return sorted(d.glob("*.md")) if d.exists() else []


def main() -> int:
    root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    skill_dirs = sorted(p for p in root.iterdir() if p.is_dir() and (p / "SKILL.md").exists())
    errors = []
    if not skill_dirs:
        print("LINT FAIL: 仓库根目录下没有找到任何含 SKILL.md 的 skill 目录")
        return 1

    for skill_dir in skill_dirs:
        name = skill_dir.name
        sk = skill_dir / "SKILL.md"
        if not sk.exists():
            errors.append(f"{name}: 缺 SKILL.md")
            continue
        text = sk.read_text(encoding="utf-8")
        fm = frontmatter(text)
        for key in ("name", "description", "version"):
            if key not in fm:
                errors.append(f"{name}: frontmatter 缺 {key}")
        if fm.get("name") != name:
            errors.append(f"{name}: frontmatter name={fm.get('name')!r} 与目录名不一致")
        if fm.get("disable-model-invocation") != "true":
            errors.append(f"{name}: 缺 disable-model-invocation: true")
        if len(text) > BUDGET_SKILL:
            errors.append(f"{name}/SKILL.md: {len(text)} 字符 > {BUDGET_SKILL}")

        flows_dir, refs_dir, tpl_dir = skill_dir / "flows", skill_dir / "references", skill_dir / "templates"
        mentioned_flows = set(re.findall(r"flows/([\w-]+\.md)", text))
        actual_flows = {p.name for p in md_files(flows_dir)}
        for f in sorted(mentioned_flows - actual_flows):
            errors.append(f"{name}: SKILL.md 引用的 flows/{f} 不存在")
        for f in sorted(actual_flows - mentioned_flows):
            errors.append(f"{name}: flows/{f} 是孤儿（SKILL.md 未引用）")

        ref_mentions = set(re.findall(r"references/([\w-]+\.md)", text))
        tpl_mentions = set(re.findall(r"templates/([\w-]+\.md)", text))
        max_flow = 0
        for p in md_files(flows_dir):
            t = p.read_text(encoding="utf-8")
            max_flow = max(max_flow, len(t))
            if len(t) > BUDGET_FLOW:
                errors.append(f"{name}/flows/{p.name}: {len(t)} 字符 > {BUDGET_FLOW}")
            for r in re.findall(r"references/([\w-]+\.md)", t):
                ref_mentions.add(r)
                if not (refs_dir / r).exists():
                    errors.append(f"{name}/flows/{p.name}: 指向不存在的 references/{r}")
            for r in re.findall(r"templates/([\w-]+\.md)", t):
                tpl_mentions.add(r)
                if not (tpl_dir / r).exists():
                    errors.append(f"{name}/flows/{p.name}: 指向不存在的 templates/{r}")

        max_ref = 0
        for p in md_files(refs_dir):
            t = p.read_text(encoding="utf-8")
            max_ref = max(max_ref, len(t))
            if len(t) > BUDGET_REF:
                errors.append(f"{name}/references/{p.name}: {len(t)} 字符 > {BUDGET_REF}")
            if p.name not in ref_mentions:
                errors.append(f"{name}: references/{p.name} 是孤儿（无 SKILL/flow 引用）")
        for p in md_files(tpl_dir):
            if p.name not in tpl_mentions:
                errors.append(f"{name}: templates/{p.name} 是孤儿（无 SKILL/flow 引用）")

        peak = len(text) + max_flow + max_ref
        if peak > BUDGET_PATH_PEAK:
            errors.append(f"{name}: 单交互路径峰值 {peak} 字符 > {BUDGET_PATH_PEAK}")

    for skill_dir in skill_dirs:
        for p in sorted(skill_dir.rglob("*.md")):
            t = p.read_text(encoding="utf-8")
            for cmd in BANNED_STRINGS:
                if cmd in t:
                    errors.append(f"{p.relative_to(root)}: 残留拼音命名 {cmd}")

    if errors:
        print(f"LINT FAIL ({len(errors)}):")
        for e in errors:
            print("  -", e)
        return 1
    print("LINT OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
