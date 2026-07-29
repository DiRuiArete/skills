# skills — product methodologies that interview you

[中文](README.md) | **English**

A growing collection of skills for product people. Each one is an interviewer: you invoke it, it questions you step by step, and hands over something you can actually use. Every skill is self-contained; install only the ones you want.

The content is maintained in Chinese; the interviewer follows your language.

## What's here

| Command | What it is | Use it for |
|---|---|---|
| `/product-lifecycle` | Full product lifecycle | positioning → first product → scaling, 14 moves end to end |
| `/product-thinking` | Product thinking | judging opportunities, understanding users, designing experience, finding an innovation angle |
| `/growth-thinking` | Growth thinking | knowing your position, finding the breakthrough point, designing growth loops, using leverage |

More on the way.

## Install

**Claude Code**

```bash
git clone https://github.com/DiRuiArete/skills.git ~/dev/skills
cd ~/dev/skills && ./install.sh
```

Just one: `./install.sh product-thinking`. Uninstall by deleting the symlinks in `~/.claude/skills/`.

**Codex / Cursor and other agents that support SKILL.md**

```bash
npx skills add DiRuiArete/skills
```

Just one: `npx skills add DiRuiArete/skills --skill product-thinking`. Add `-g` for a user-level install.

## How to use

1. **Invoke**: type the skill name, e.g. `/product-thinking`. Skip a step by bringing your situation along: `/product-thinking I'm building a bookkeeping tool for freelancers, not sure it's worth doing`.
2. **It asks first**: the opening is a multiple-choice menu. Every decision point offers exactly three options with completeness scores, one-line reasons and a recommendation. Reply with a letter, or just talk if your answer is off the menu.
3. **Plan mode**: in Claude Code the skill enters plan mode automatically; the whole interview is read-only and conclusions only land as documents after you confirm. Hosts without plan mode get a plain conversational interview with the same rules.
4. **Get the deliverable**: each flow wraps up at 9/10 completeness and asks what you want: a document, a PRD, an executable task list, or just the conclusions on file.
5. **Just want a template?** Say so ("give me the retro template").
6. **Language**: the interview follows yours. Content is maintained in Chinese; speak English and it interviews in English.

## Repo conventions

Every top-level folder is one self-contained skill with the same layout:

```
<skill>/
├── SKILL.md        # entry: opening, interaction rules, routing table
├── flows/          # dialogue scripts (decision-point sequences), loaded on demand
├── references/     # the methodology: frameworks, steps, anti-patterns, mermaid diagrams
└── templates/      # deliverable skeletons generated at the end of a session
```

Adding a skill = create a folder with this layout and get `python3 scripts/lint-skills.py .` to pass; `install.sh` and `npx skills` discover it automatically.

## Content and license

Every skill here is distilled from my study notes on the source methodology, fully rewritten in my own words. No original transcripts or course images; every release is checked with a verbatim-overlap detector (`scripts/check-overlap.py`). Source registry:

- `product-lifecycle`: Li Xiang's product course (Dedao app)
- `product-thinking` / `growth-thinking`: Liang Ning's product-thinking and growth-thinking courses (Dedao app)

The originals are worth buying. Takedown requests via issues will be honored.

Licensed under [CC BY-NC-SA 4.0](LICENSE).
