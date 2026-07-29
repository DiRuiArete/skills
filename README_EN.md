# skills — product methodologies that interview you

[中文](README.md) | **English**

Three product methodologies I keep coming back to, packaged as interviewer-style skills. Not a knowledge base: you invoke one, it questions you step by step, and only hands over a deliverable once it has asked enough.

The content is maintained in Chinese; the interviewer follows your language.

| Command | What it is | Use it for |
|---|---|---|
| `/product-lifecycle` | Full product lifecycle | positioning → first product → scaling, 14 moves end to end |
| `/product-thinking` | Product thinking | judging opportunities, understanding users, designing experience, finding an innovation angle |
| `/growth-thinking` | Growth thinking | knowing your position, finding the breakthrough point, designing growth loops, using leverage |

## Why

Frameworks are easy to nod along to and impossible to recall when you actually need them. I tried feeding my course notes to an AI as a knowledge base. It just lectured back at me and never asked the questions that mattered.

So these work the other way around. You invoke one, it asks where you are and what you're stuck on, then walks you through the relevant decision flow. Every decision point gives exactly three options with a recommendation, a completeness score and a one-line reason, then stops and waits for your call. Facts it can dig out of your repo, it digs out itself; decisions stay yours. You end up with a usable artifact: a positioning doc, a retro plan, a growth battle map, not a pile of advice. The interaction style borrows from mattpocock's grill-me and gstack's office-hours.

## Install

**Claude Code**

```bash
git clone https://github.com/DiRuiArete/skills.git ~/dev/skills
cd ~/dev/skills && ./install.sh
```

To uninstall, delete the symlinks in `~/.claude/skills/`.

**Codex and other agents that support SKILL.md** (Cursor, opencode, ...)

```bash
npx skills add DiRuiArete/skills
```

Pick the skills and the target agent when prompted.

## How to use

1. **Invoke**: type the skill name, e.g. `/product-thinking`. Skip a step by bringing your situation along: `/product-thinking I'm building a bookkeeping tool for freelancers, not sure it's worth doing`.
2. **It asks first**: the opening is a multiple-choice menu (what stage you're at / what you came with). Every decision point offers exactly three options with completeness scores, one-line reasons and a recommendation. Reply with a letter, or just talk if your answer is off the menu.
3. **Plan mode**: in Claude Code the skill enters plan mode automatically. The whole interview is read-only; conclusions accumulate in the plan and only land as documents after you confirm. In hosts without plan mode (Codex among them) it degrades to a plain conversational interview with the same rules.
4. **Get the deliverable**: each flow wraps up at 9/10 completeness and hands you something usable: a positioning doc, a retro plan, a growth battle map.
5. **Just want the template?** Say so ("give me the retro template") and it hands the template over as-is.
6. **Language**: the interview follows yours. Content is maintained in Chinese; speak English and it interviews in English.

## What it looks like

```
You:  /product-lifecycle
It:   Quick 30-second stage check.
      A. Nothing started yet   B. Building the first product
      C. Launched, planning what's next   D. Not sure, let me describe it
You:  A
It:   ✅ Stage confirmed: strategy
      [What to do next — 3 options]
      ★ A. Nail the positioning (9/10) …   B. Define team culture (4/10) …
        C. Jump straight into building (2/10 ⚠️)
      → My call: A
```

Translated for illustration; the actual session runs in Chinese. The other two skills open with a single question: "What are you here with today?" They route by what you're doing, not by course chapters.

## Repo structure

```
product-lifecycle/   # full product lifecycle
product-thinking/    # product thinking
growth-thinking/     # growth thinking
scripts/             # check-overlap.py (verbatim-overlap detector), lint-skills.py (structure and budget lint)
evals/               # behavior eval cases per skill
```

Each skill folder is self-contained and shares the same layout:

```
<skill>/
├── SKILL.md        # entry: opening, interaction rules, routing table
├── flows/          # dialogue scripts (decision-point sequences), loaded on demand
├── references/     # the methodology itself: frameworks, steps, anti-patterns, mermaid diagrams
└── templates/      # deliverable skeletons generated at the end of a session
```

## Content and license

These methodologies come from my study notes on Li Xiang's product course and Liang Ning's product-thinking and growth-thinking courses (all on the Dedao app). Everything here is distilled from those notes and fully rewritten in my own words. No original transcripts or course images are included, and every release is checked with a verbatim-overlap detector (`scripts/check-overlap.py`). The original courses are worth buying. Takedown requests via issues will be honored.

Licensed under [CC BY-NC-SA 4.0](LICENSE).
