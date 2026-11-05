# Research repo guide

How this repo works: ARIS (the skill library) plus our additions (state files, custom skills, rigor tooling,
LaTeX workflow). Read sections 1–4 first. The rest is reference.

- [0. Finish the setup (one time)](#0-finish-the-setup-one-time)
- [1. Map of the repo](#1-map-of-the-repo)
- [2. The working loop](#2-the-working-loop)
- [3. State files: STATUS, backlog, decisions, hypotheses, log](#3-state-files)
- [4. The knowledge wiki, and how to invoke knowledge](#4-the-knowledge-wiki)
- [5. Custom skills](#5-custom-skills)
- [6. Experiments → numbers in the paper](#6-experiments--numbers-in-the-paper)
- [7. Writing: live preview and the GitHub LaTeX workflow](#7-writing)
- [8. ARIS workflows cheat sheet](#8-aris-workflows-cheat-sheet)
- [9. Example: one week end to end](#9-example-one-week-end-to-end)
- [10. Updating ARIS and troubleshooting](#10-updating-aris-and-troubleshooting)

---

## 0. Finish the setup (one time)

ARIS lives next to this repo in `..\Auto-claude-code-research-in-sleep` (the upstream clone). Its skills are
**linked** into `.claude\skills\` (junctions), so `git pull` there updates them here.

Run these in a **PowerShell** terminal (Developer Mode must stay on, because the installer creates one symlink):

```powershell
# 1. Link the 87 ARIS skills + the fan-out agent into this project (also adds an ARIS block to CLAUDE.md)
& "..\Auto-claude-code-research-in-sleep\tools\install_aris.ps1" . -Platform claude -All -Quiet

# 2. Make `python3` work in Git Bash (ARIS skills call python3; on Windows that name is a Microsoft Store stub)
New-Item -ItemType Directory -Force "$env:HOME\bin" | Out-Null
Set-Content -NoNewline -Encoding ascii "$env:HOME\bin\python3" "#!/bin/sh`nexec /c/Users/Camilo/AppData/Local/Programs/Python/Python312/python.exe `"`$@`"`n"

# 3. Create the research wiki
python ..\Auto-claude-code-research-in-sleep\tools\research_wiki.py init research-wiki/
```

> Step 2 path: your Git Bash `$HOME` is `C:\Users\Camilo\AppData\Roaming\SPB_Data`, and `~/bin` is already first on its PATH.
> Alternative: Settings → Apps → Advanced app settings → App execution aliases → turn off the two `python3.exe` entries,
> then copy `python.exe` to `python3.exe` in `C:\Users\Camilo\AppData\Local\Programs\Python\Python312\`.

Check: start `claude` in this folder and type `/` — you should see `/research-wiki`, `/idea-discovery`, `/stage-summarizer`, etc.

**Optional, needed for the review-loop skills** (`/auto-review-loop`, `/research-review`, `/kill-argument`…): ARIS uses a second
model as reviewer through the Codex CLI. One-time setup (needs a ChatGPT account):

```powershell
npm install -g @openai/codex; codex login
claude mcp add codex -s user -- python "C:\Users\Camilo\Documents\Trabajo\Master projects\Auto-claude-code-research-in-sleep\mcp-servers\codex-exec\server.py"
claude mcp list   # must show codex ... ✔ Connected (restart Claude Code first)
```

**For the LaTeX preview**: install [MiKTeX](https://miktex.org/download) (or TeX Live) and the VS Code extension
*LaTeX Workshop* (VS Code suggests it when you open the folder, via `.vscode/extensions.json`).

**For the GitHub workflow**: create an empty GitHub repo and push this one (`git remote add origin …; git push -u origin main`).

---

## 1. Map of the repo

```
CLAUDE.md                     always loaded; routes each task to the files it needs (+ ARIS block)
RESEARCH_BRIEF.md             your project direction (feeds the wiki query pack, /idea-discovery)
research/
  STATUS.md                   current stage, idea, decisions, open questions, next steps, schematic
  backlog.md                  parked ideas B-###
  decisions.md                decisions D-### (append-only)
  hypotheses.md               hypotheses H-### and their status
  related_work_matrix.md      papers × dimensions table + gaps
  log/YYYY-MM-DD.md           daily log
  reports/weekly/             advisor reports (YYYY-Www.md)
research-wiki/                ARIS knowledge base (papers, ideas, experiments, claims, graph)
.claude/skills/
  stage-summarizer/           custom: end-of-session STATUS update + Mermaid schematic
  related-work-matrix/        custom: papers × dimensions matrix, gap, related-work hooks
  weekly-report/              custom: one-page advisor update
  <87 ARIS skills>            linked from ../Auto-claude-code-research-in-sleep (not committed)
experiments/results/          one JSON per experiment → LaTeX macros
paper/
  main.tex, references.bib
  results.tex                 GENERATED macros (never edit by hand)
scripts/make_results_tex.py   results JSON → paper/results.tex (+ --check, --lint-paper)
.github/workflows/latex.yml   on push: macro check, PDF build, chktex, latexdiff PDF
.vscode/                      LaTeX Workshop live preview config
```

Deliberately left out for now: the pinned devcontainer environment and rliable evaluation.

---

## 2. The working loop

| When | You type | What happens |
|------|----------|--------------|
| **Session start** | nothing special: just start `claude` and ask | CLAUDE.md tells the agent to read only `research/STATUS.md` + `research-wiki/query_pack.md` |
| **During work** | normal requests, ARIS slash commands | Routing rules in CLAUDE.md pick the files (see table below) |
| **Session end** | `/stage-summarizer` | Writes today's log summary, rewrites STATUS.md + schematic, syncs CLAUDE.md `stage`/`next` |
| **Friday** | `/weekly-report` (or `/weekly-report — lang: es`) | One-page update in `research/reports/weekly/` |

Routing, i.e. what the agent reads for each kind of task (defined in `CLAUDE.md`):

| Task | Reads / does |
|------|--------------|
| Question about prior work, ideas, results | `/research-wiki query "<topic>"` first → opens only pages the pack points to |
| General concept unrelated to the project | answers directly, no wiki |
| Methodology (design, metrics, baselines) | `decisions.md` + `hypotheses.md`; records new D-/H- entries |
| Idea discovery | `backlog.md` first; appends unselected ideas to it afterwards |
| Related work | updates `related_work_matrix.md` (`/related-work-matrix`) |
| Experiments | results JSON in `experiments/results/` → `python scripts/make_results_tex.py` |
| Writing | latest results file + STATUS.md; numbers only via `\res…` macros |

---

## 3. State files

These are plain Markdown and you can edit them yourself at any time. The IDs (`D-`, `H-`, `B-`) link everything together:
STATUS cites them, the weekly report cites them, backlog entries point to the decision that parked them.

### STATUS.md: "where are we?"
- **Read at every session start**, so keep it short (< 150 lines).
- **Written by `/stage-summarizer`**, not by hand (you can, but the next summary rewrites it).
- Sections: Current idea · Schematic (Mermaid) · Recent decisions · Open questions · Next steps.
- Every line cites a source (`log/2026-11-05`, `D-003`, `H-002`, `experiments/results/x.json`), so nothing is invented.
- The Mermaid block renders on GitHub and in VS Code (with the *Markdown Mermaid* extension).

### backlog.md: "ideas we're not doing (yet)"
Entry format:
```markdown
### B-004 · Use curiosity bonus instead of count-based exploration
- **Added:** 2026-11-12
- **Source:** /idea-discovery 2026-11-12, IDEA_REPORT.md #3
- **Related decision:** D-006 (chose count-based for interpretability)
- **Why parked:** needs a learned dynamics model; too costly before the baseline works
- **Revisit when:** H-002 is supported and we have > 50 GPU-h left
- **Status:** parked
```
- Idea discovery **reads it first** and won't re-propose a parked idea unless its "revisit when" is met.
- After you pick an idea, **all unselected candidates are appended** automatically (CLAUDE.md rule).
- `/stage-summarizer` flags entries whose condition looks met ("Revisit B-004?").
- Never delete; change `Status` to `revived (→ H-007)` or `dropped (reason)`.

### decisions.md: "why did we do it this way?"
Append-only ADR-style entries (`Context / Decision / Alternatives / Consequences / Links`). A changed decision gets a new
entry with `Supersedes: D-###`. Write one whenever you choose a baseline, metric, environment, number of seeds, etc.
Prompt: *"Record a decision: we evaluate on 10 seeds with IQM because…"*

### hypotheses.md: "what are we testing?"
Each `H-###` states in advance what would support or refute it, and has a status
(`open → testing → supported | refuted | inconclusive`). When `/result-to-claim` gives a verdict, update the status and link
the results file. Prompt: *"Add a hypothesis: count-based bonuses improve success rate on sparse-reward mazes over ε-greedy."*

### log/YYYY-MM-DD.md: "what happened today"
Short bullets with pointers. The agent appends during the session; `/stage-summarizer` adds a "Session summary".
STATUS and the weekly report are built from these.

---

## 4. The knowledge wiki

### What it is
`research-wiki/` is ARIS's persistent memory: a small graph of **papers, ideas, experiments and claims**, one Markdown
page each, connected by typed edges in `graph/edges.jsonl`.

```
research-wiki/
  index.md         categorical index (auto)
  log.md           append-only timeline
  gap_map.md       field gaps with stable IDs G1, G2, …
  query_pack.md    ≤ 8000-char compressed summary: direction, top gaps, paper clusters, FAILED ideas, top papers
  papers/<slug>.md     one-line thesis, problem, method, results, assumptions, limitations, relevance
  ideas/<id>.md        proposed/tested ideas and their outcome (failed ideas are kept: anti-repetition memory)
  experiments/<id>.md  experiment records linked to ideas
  claims/<id>.md       testable claims and their status
  graph/edges.jsonl    relationships (extends, contradicts, tested_by, supports, invalidates, …)
```

**Wiki vs state files.** The wiki holds *knowledge* (what papers say, which ideas failed and why, which claims hold).
`research/` holds *project management* (where we are, what we decided, what's next). They link through ids:
a hypothesis `H-002` cites wiki `exp:…`/`claim:…`; a backlog item cites `paper:…`.

### How it fills up (mostly automatically)
| ARIS skill | Writes to the wiki |
|-----------|---------------------|
| `/research-lit`, `/arxiv`, `/semantic-scholar`, `/alphaxiv`, `/deepxiv`, `/exa-search` | paper pages (auto-ingest) |
| `/idea-creator`, `/idea-discovery` | reads the query pack first, writes ideas back |
| `/result-to-claim` | experiment nodes + supports/invalidates edges, idea outcome |
| `/proof-checker` | claim nodes |
| `/wiki-enrich` | fills TODO sections of thin paper pages |

### The query discipline (why sessions stay cheap)
Agents **never load the whole wiki**. They go: `query_pack.md` → `index.md` if needed → only the specific pages the pack
names. That rule lives in CLAUDE.md, so it applies to every session.

### How to invoke knowledge: commands and examples

| You want… | Type | Result |
|-----------|------|--------|
| Ask about prior work in plain language | *"What did we learn about reward shaping so far?"* | Agent runs the wiki query first (CLAUDE.md rule), answers citing `paper:`/`idea:` ids, opens pages only if needed |
| Force a fresh knowledge pack on a topic | `/research-wiki query "reward shaping in sparse-reward navigation"` | Rebuilds `query_pack.md` and summarizes it |
| Add one paper | `/research-wiki ingest "Never Give Up" — arxiv: 2002.06038` | Creates `papers/<slug>.md` with metadata + abstract |
| Add many papers | `/research-wiki sync — arxiv-ids 2002.06038,1810.12894` | Batch ingest |
| Search + ingest at once | `/research-lit "count-based exploration deep RL"` | Literature review, ingests papers it finds |
| Mark a paper as core | `/research-wiki update paper:<slug> — relevance: core` (slug = page filename) | Updates the page, rebuilds the pack |
| Record an idea outcome | `/research-wiki update idea:003 — outcome: negative` | Failed ideas stay in the pack forever |
| Health check | `/research-wiki lint` | `LINT_REPORT.md`: orphans, stale claims, contradictions, missing links |
| Quick numbers | `/research-wiki stats` | counts of papers/ideas/claims/edges |
| Fill thin pages | `/wiki-enrich` | completes TODO sections |
| See the gaps | open `research-wiki/gap_map.md` or ask *"what gaps does the wiki show?"* | G-ids, also used by the matrix |

Tips:
- Be specific in queries: `"partial observability + intrinsic reward"` beats `"RL"`.
- Fill in `RESEARCH_BRIEF.md`: its sections go first in the query pack, so every idea-generation run is aimed at your problem.
- Questions that aren't about this project (*"explain PPO clipping"*) are answered directly, without the wiki.

---

## 5. Custom skills

### `/stage-summarizer` (end of every session)
```
/stage-summarizer
/stage-summarizer stage -> implementation; we chose the count-based idea
```
Reads the logs since the last update, new decisions, open hypotheses and new backlog items, then:
1. appends a *Session summary* to today's log,
2. rewrites `research/STATUS.md` (sourced, < 150 lines),
3. redraws the Mermaid schematic of the **current idea** (problem → method parts → metrics, with H-ids on edges; failed parts dashed),
4. syncs `stage`, `idea`, `next` in the CLAUDE.md Pipeline Status block.

### `/related-work-matrix` (formulation stage, then whenever you add papers)
```
/related-work-matrix
/related-work-matrix add 2002.06038 1810.12894
/related-work-matrix refresh
```
Builds `research/related_work_matrix.md`: one row per paper, columns **Formulation · State space · Reward · Evaluation ·
Key limitation** (edit the `## Dimensions` list to change columns), plus a final *Ours* row. Then:
- **Gaps exposed**: empty/rare combinations across columns, with G-ids shared with `research-wiki/gap_map.md`;
- **Narrative hooks**: paragraph topics for the related-work section, citing `paper:` ids.
Paper facts come from the wiki pages; unknown cells are `?`, never guessed. Papers not in the wiki are ingested first.

### `/weekly-report` (Fridays)
```
/weekly-report
/weekly-report — lang: es
/weekly-report — since: 2026-11-01
```
One page (≤ 400 words): TL;DR · Done (✅/❌ against last week's plan) · Results table (every number cites its JSON) ·
Decisions · Questions for the advisor · Plan. Saved as `research/reports/weekly/2026-W45.md`.

---

## 6. Experiments → numbers in the paper

1. Each experiment writes `experiments/results/<name>.json` (format and options in `experiments/results/README.md`):
   ```json
   {"_meta": {"commit": "abc1234", "seeds": [0,1,2,3,4], "hypothesis": "H-002"},
    "_format": {"success_rate": "pct1"},
    "return": {"mean": 412.37, "std": 18.2}, "success_rate": 0.934}
   ```
2. Regenerate the macros:
   ```bash
   python scripts/make_results_tex.py
   ```
   → `paper/results.tex` gets `\resCountBonusReturnMean` = 412.37, `\resCountBonusSuccessRate` = 93.4\%, …
3. In the paper: `Our method reaches $\resCountBonusReturnMean \pm \resCountBonusReturnStd$.`
4. Check for typed numbers that slipped in:
   ```bash
   python scripts/make_results_tex.py --lint-paper
   ```
5. CI runs `--check` on every push: if you changed a JSON but forgot to regenerate `results.tex`, the job fails.

Then `/result-to-claim` decides whether the result supports the hypothesis and records it in the wiki; update `H-###` status.

`experiments/results/example.json` and the example sentence in `paper/main.tex` only demonstrate the workflow; delete both when real results exist.

---

## 7. Writing

**Live preview (LaTeX visualizer).** Open the repo folder in VS Code → open `paper/main.tex` → save → the PDF rebuilds
and shows in a tab (`.vscode/settings.json`: latexmk on save, SyncTeX; Ctrl+Alt+J jumps from source to PDF).
chktex warnings show in the Problems panel.

**GitHub Action** (`.github/workflows/latex.yml`, runs on pushes touching `paper/`, results, or the script):

| Job | Does | Output |
|-----|------|--------|
| results.tex is up to date | `make_results_tex.py --check` + typed-number lint | fails if macros are stale |
| Build PDF | latexmk on `paper/main.tex` | artifact **paper-pdf** |
| Lint (chktex) | chktex on `paper/*.tex` | warnings in the run summary; fails only on errors |
| Diff PDF | `latexdiff --flatten` vs the previous push (or the PR base) | artifact **paper-diff-pdf** (red = removed, blue = added) |

Download the PDFs from the run page → *Artifacts*.

ARIS writing skills work on `paper/`: `/paper-plan`, `/paper-write`, `/paper-compile`, `/auto-paper-improvement-loop`,
`/citation-audit`, `/paper-claim-audit`. They should use `\res…` macros (CLAUDE.md rule).

---

## 8. ARIS workflows cheat sheet

| Stage | Command | Notes |
|-------|---------|-------|
| Direction → ideas | `/idea-discovery "specific direction"` | reads backlog + wiki first; writes IDEA_REPORT.md |
| Novelty | `/novelty-check "idea"` | |
| Refine method | `/research-refine "idea"` | |
| Plan experiments | `/experiment-plan` | |
| Implement + run | `/experiment-bridge`, `/run-experiment`, `/monitor-experiment` | |
| Analyze | `/analyze-results`, `/result-to-claim` | updates wiki claims/ideas |
| Review loop | `/auto-review-loop "scope"` | needs the Codex reviewer (section 0) |
| Paper | `/paper-writing "NARRATIVE_REPORT.md"` or step by step `/paper-plan` → `/paper-write` → `/paper-compile` | |
| Figures | `/paper-figure`, `/mermaid-diagram` | |
| Everything | `/research-pipeline "direction"` | long-running, chains all of the above |

Full list: type `/` in Claude Code, or see `..\Auto-claude-code-research-in-sleep\README.md`.

---

## 9. Example: one week end to end

**Monday, start**
```
> (fill RESEARCH_BRIEF.md first: problem, constraints, papers you know)
> /research-lit "count-based and curiosity exploration for sparse-reward navigation"
    → ~15 papers ingested into research-wiki/papers/
> /related-work-matrix
    → matrix with 15 rows; gap G3: "no method combines partial observability with count-based bonuses and >5 seeds"
> /idea-discovery "exploration bonuses under partial observability for sparse-reward navigation"
    → reads backlog (empty) + query pack; proposes 6 ideas; you pick #2
    → ideas #1,#3–#6 appended to backlog.md as B-001…B-005 with "revisit when" conditions
> "Record the decision to pursue idea #2 and add its hypotheses."
    → D-002 in decisions.md; H-001, H-002 in hypotheses.md
> /stage-summarizer stage -> implementation
    → STATUS.md: current idea, schematic Problem → Count bonus over belief state → Success rate (H-001)
```

**Tuesday, start a new session**
```
> "Where are we and what's next?"
    → agent read STATUS.md + query_pack.md only; answers from them
> "Did any paper already try counts over belief states?"
    → /research-wiki query "count-based bonus belief state POMDP" → cites paper:… pages, opens two of them
> /experiment-plan   then   /run-experiment
    → experiments/results/count_bonus.json, baseline_egreedy.json
> python scripts/make_results_tex.py
> /result-to-claim
    → wiki: exp node + supports edge; you set H-001 status: supported
> /stage-summarizer
```

**Friday**
```
> /weekly-report — lang: es
    → research/reports/weekly/2026-W46.md, one page, every number cited to its JSON
```

**Weeks later, writing**
```
> /paper-write "Related Work"   (uses the matrix's narrative hooks)
> /paper-write "Experiments"     (uses \resCountBonus... macros)
> git push                       → GitHub builds paper-pdf + paper-diff-pdf
```

---

## 10. Updating ARIS and troubleshooting

**Update ARIS** (PowerShell):
```powershell
cd "..\Auto-claude-code-research-in-sleep"; git pull      # linked skills update immediately
& .\tools\install_aris.ps1 ..\ARIS -Reconcile             # picks up NEW/removed upstream skills (asks per new skill)
```
Our three custom skills are real folders, not links, so updates never touch them.

| Problem | Fix |
|---------|-----|
| `python3: Python was not found` inside a skill | do step 2 of section 0 |
| Installer: *failed to create … symbolic link* | Developer Mode off: Settings → System → For developers |
| `/research-wiki`: *research_wiki.py not found* | rerun the installer (creates `.aris\tools`), or set the env var `ARIS_REPO` to the ARIS clone path before starting `claude` |
| Review skills complain about the reviewer | set up the Codex MCP (section 0) |
| CI "results.tex is out of date" | `python scripts/make_results_tex.py` and commit `paper/results.tex` |
| ARIS skills missing after cloning this repo on another machine | upstream skills aren't committed; clone ARIS next to it and rerun the installer |
