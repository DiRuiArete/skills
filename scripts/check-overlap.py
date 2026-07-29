#!/usr/bin/env python3
"""14-gram 逐字重合检测：课程逐字稿 (source) vs 重写后的 skill markdown (target)。

用法：
  python3 scripts/check-overlap.py --source /abs/path/raw.txt --target product-thinking
  python3 scripts/check-overlap.py --source raw.txt --target product-lifecycle/references/pricing.md

判定（任一不满足即 exit 1）：
  - 每个 target 文件覆盖率 <= --max-rate（默认 1.5%）
  - 最长连续命中 span <= --max-span 字符（默认 19，即 <20）

覆盖率 = 归一化后 target 中落在任一命中 n-gram 内的字符数 / 归一化后总字符数。
归一化 = NFKC + 仅保留字母数字（含 CJK）+ 小写，剥离全部空白与标点。
source 永远从仓库外的绝对路径传入——逐字稿不进 repo。
"""
import argparse
import pathlib
import sys
import unicodedata


def normalize_with_map(text: str):
    """返回 (归一化字符串, 归一化位置 -> 原文位置 的映射)。"""
    out, idx = [], []
    for i, ch in enumerate(text):
        for c in unicodedata.normalize("NFKC", ch):
            if c.isalnum():
                out.append(c.lower())
                idx.append(i)
    return "".join(out), idx


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--source", required=True, help="课程逐字稿纯文本（仓库外绝对路径）")
    ap.add_argument("--target", required=True, help="待检目录（递归 *.md）或单个文件")
    ap.add_argument("--n", type=int, default=14, help="n-gram 窗口字符数（默认 14）")
    ap.add_argument("--max-rate", type=float, default=0.015, help="单文件覆盖率上限（默认 0.015）")
    ap.add_argument("--max-span", type=int, default=19, help="最长连续命中字符数上限（默认 19）")
    ap.add_argument("--top", type=int, default=5, help="失败时展示的最长 span 数")
    ap.add_argument(
        "--allow",
        default=str(pathlib.Path(__file__).parent / "overlap-allowlist.txt"),
        help="公开事实 allowlist（每行一条，# 注释；命中范围不参与 gram 匹配）",
    )
    args = ap.parse_args()

    allow_norms = []
    allow_path = pathlib.Path(args.allow)
    if allow_path.exists():
        for line in allow_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                norm_entry, _ = normalize_with_map(line)
                if norm_entry:
                    allow_norms.append(norm_entry)

    src_norm, _ = normalize_with_map(
        pathlib.Path(args.source).read_text(encoding="utf-8", errors="ignore")
    )
    n = args.n
    if len(src_norm) < n:
        print(f"source 归一化后仅 {len(src_norm)} 字符，无法建 {n}-gram 索引", file=sys.stderr)
        return 2
    grams = {src_norm[i : i + n] for i in range(len(src_norm) - n + 1)}

    target = pathlib.Path(args.target)
    files = sorted(target.rglob("*.md")) if target.is_dir() else [target]
    if not files:
        print(f"target 下没有 .md 文件：{target}", file=sys.stderr)
        return 2

    failed = False
    print(f"source grams: {len(grams):,} ({args.n}-gram) | targets: {len(files)}")
    for f in files:
        text = f.read_text(encoding="utf-8", errors="ignore")
        norm, idx = normalize_with_map(text)
        total = len(norm)
        if total < n:
            print(f"  OK    {f.name:44s} (仅 {total} 字符，跳过)")
            continue
        # allowlist 命中范围替换为哨兵字符：任何跨越/包含它的 gram 都无法匹配 source
        scan = norm
        for entry in allow_norms:
            pos = scan.find(entry)
            while pos != -1:
                scan = scan[:pos] + "\x00" * len(entry) + scan[pos + len(entry) :]
                pos = scan.find(entry, pos + len(entry))
        hit = [False] * total
        for i in range(total - n + 1):
            if scan[i : i + n] in grams:
                for j in range(i, i + n):
                    hit[j] = True
        covered = sum(hit)
        rate = covered / total
        spans = []
        i = 0
        while i < total:
            if hit[i]:
                j = i
                while j < total and hit[j]:
                    j += 1
                spans.append((i, j))
                i = j
            else:
                i += 1
        longest = max((b - a for a, b in spans), default=0)
        ok = rate <= args.max_rate and longest <= args.max_span
        print(f"  {'OK  ' if ok else 'FAIL'}  {f.name:44s} rate={rate:6.2%}  longest={longest:3d}  chars={total}")
        if not ok:
            failed = True
            for a, b in sorted(spans, key=lambda s: s[1] - s[0], reverse=True)[: args.top]:
                lo, hi = idx[a], idx[b - 1]
                ctx = text[max(0, lo - 20) : hi + 21].replace("\n", "⏎")
                print(f"          span {b - a:3d} 字符: …{ctx}…")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
