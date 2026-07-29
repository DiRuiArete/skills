# skills — 会追问你的产品方法论

**中文** | [English](README_EN.md)

一个持续生长的 skill 集合，给做产品的人用。每个 skill 都是一个面试官：你呼出它，它一步步问你，问透了给你能直接用的产出。每个 skill 自包含，只装你要的那个就行。

## 目前有什么

| 命令 | 是什么 | 用来做什么 |
|---|---|---|
| `/product-lifecycle` | 产品全周期 | 找定位、做第一款产品、规模化，14 个动作走完全程 |
| `/product-thinking` | 产品思维 | 判断机会、看懂用户、设计体验、找创新切入点 |
| `/growth-thinking` | 增长思维 | 认清位置、找破局点、设计增长模式、借势上台阶 |

会陆续添加新的。

## 安装

**Claude Code**

```bash
git clone https://github.com/DiRuiArete/skills.git ~/dev/skills
cd ~/dev/skills && ./install.sh
```

只装一个：`./install.sh product-thinking`。卸载：删掉 `~/.claude/skills/` 里对应的软链接。

**Codex / Cursor 等（任何支持 SKILL.md 的 agent）**

```bash
npx skills add DiRuiArete/skills
```

只装一个：`npx skills add DiRuiArete/skills --skill product-thinking`。装到用户级加 `-g`。

## 怎么用

1. **呼出**：输入 skill 名，比如 `/product-thinking`。想省一步，直接带上你的处境：`/product-thinking 我在做一个给自由职业者的记账工具，不知道值不值得做`。
2. **它先问你**：开场是一个选择题菜单，之后每个决策点固定三个选项，各带完整度评分和一句理由，外加一个推荐。回字母就行；选项之外有想法，直接说话。
3. **plan mode**：在 Claude Code 里，skill 会自动进入 plan mode，整场面试只读不写，结论你确认后才落成文档。没有 plan mode 的环境自动转为纯对话面试，规则不变。
4. **拿产出**：每条流问到 9/10 完整度收尾，问你要哪种交付：产出文档、PRD、可直接执行的任务清单，或者只存结论。
5. **只要模板**：不想走流程就直说，比如"给我复盘模板"。
6. **语言**：面试跟随你的语言。内容底稿是中文，你用英文聊它就用英文问。

## 仓库约定

每个根目录文件夹是一个自包含 skill，结构一致：

```
<skill>/
├── SKILL.md        # 入口：开场、交互规则、路由表
├── flows/          # 对话剧本（决策点序列），按需加载
├── references/     # 方法论正文：框架、步骤、反模式、mermaid 图
└── templates/      # 产出物骨架（收尾时生成的文档模板）
```

新增一个 skill = 照这个结构建一个文件夹，跑 `python3 scripts/lint-skills.py .` 全绿即收录；`install.sh` 和 `npx skills` 都会自动发现它。

## 内容来源与版权

本仓库的 skill 都源自我学习各家方法论时做的笔记，全部用自己的话重写，不含课程原文与配图（图用 mermaid 重画）；发布前跑 `scripts/check-overlap.py` 做逐字重合检测，14 字符连续重合即报警。来源登记：

- `product-lifecycle`：李想《产品实战课》（得到 App）
- `product-thinking` / `growth-thinking`：梁宁《产品思维》《增长思维》（得到 App）

原课程值得购买。权利方如有异议请提 issue，会及时处理。

## License

[CC BY-NC-SA 4.0](LICENSE)
