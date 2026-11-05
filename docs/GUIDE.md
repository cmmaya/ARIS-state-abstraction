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
  STATUS.md                   the last 3 sessions: what was done, files, results, unfinished + resume line
  backlog.md                  ledger of everything Decided (D-), Discarded (X-), Parked (B-)
  decisions.md                full rationale per D-id (append-only)
  hypotheses.md               hypotheses H-### and their status
  related_work_matrix.md      papers × dimensions table + gaps
  log/YYYY-MM-DD.md           daily log
  reports/weekly/             advisor reports (YYYY-Www.md)
research-wiki/                ARIS knowledge base (papers, ideas, experiments, claims, graph)
.claude/skills/
  stage-summarizer/           custom: end-of-session STATUS + log + backlog update
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
| **Session start** | nothing special: just start `claude` and ask | CLAUDE.md tells the agent to read only `research/STATUS.md` (last 3 sessions) + `research-wiki/query_pack.md` |
| **During work** | normal requests, ARIS slash commands | Routing rules in CLAUDE.md pick the files (see table below) |
| **Session end** | `/stage-summarizer` | Adds the session to STATUS.md (drops the 4th-oldest), archives it in the log, records decisions/discards/parked ideas in backlog.md |
| **Friday** | `/weekly-report` (or `/weekly-report — lang: es`) | One-page update in `research/reports/weekly/` |

Routing, i.e. what the agent reads for each kind of task (defined in `CLAUDE.md`):

| Task | Reads / does |
|------|--------------|
| Question about prior work, ideas, results | `/research-wiki query "<topic>"` first → opens only pages the pack points to |
| General concept unrelated to the project | answers directly, no wiki |
| "Was X decided/discarded?" | `backlog.md` |
| Methodology (design, metrics, baselines) | `backlog.md` + `hypotheses.md`; `decisions.md` only for a D-id's rationale; records new D-/H- entries |
| Idea discovery | `backlog.md` first (skips Discarded, and Parked not yet due); chosen → Decided, others → Parked/Discarded |
| Related work | updates `related_work_matrix.md` (`/related-work-matrix`) |
| Experiments | results JSON in `experiments/results/` → `python scripts/make_results_tex.py` |
| Writing | latest results file + STATUS.md; numbers only via `\res…` macros |

---

## 3. State files

Plain Markdown, editable by hand. Two files carry the agent's memory, and each does one job:

| File | Question it answers | Scope | Read |
|------|---------------------|-------|------|
| `STATUS.md` | "What exactly did we do in the last sessions, and where did we stop?" | last 3 sessions, rolling | every session start |
| `backlog.md` | "What has been decided, discarded or parked, ever?" | whole project, never shrinks | idea discovery, methodology, "did we decide X?" |

IDs link everything: `S#` sessions, `D-` decisions, `X-` discarded, `B-` parked, `H-` hypotheses.

### STATUS.md: the last 3 sessions
```markdown
**Resume:** run make_results_tex.py, then write Experiments §4.2 in paper/main.tex
**Stage:** implementation · **Updated:** 2026-11-14

## S7 · 2026-11-14 · Count bonus vs ε-greedy on maze
- Did: ran 5 seeds each; fixed reward bug in envs/maze.py (bonus was added twice)
- Files: envs/maze.py, experiments/results/count_bonus.json, experiments/results/egreedy.json
- Results: success = 93.4% (count_bonus.json) vs 61.0% (egreedy.json)
- Decided/discarded: D-004, X-003, H-001 → supported
- Unfinished: results.tex not regenerated; Experiments section not written
## S6 · …
## S5 · …
```
- Written by `/stage-summarizer` from the session itself (conversation + git diff), so it records **exactly** what was done.
- Keeps only the 3 newest sessions. Older ones are not lost: every entry is also archived in `research/log/YYYY-MM-DD.md`.
- The **Resume** line is the first thing the next session acts on.
- No current-idea essays, no diagrams: decisions live in backlog.md, knowledge in the wiki.

### backlog.md: the decided / discarded / parked ledger
Three tables, one row per item, rows never deleted:
```markdown
## Decided
| ID | Date | Decision | Why | Source |
| D-004 | 2026-11-14 | Evaluate with 5 seeds, success rate as main metric | budget; matches prior work | S7 |
## Discarded
| ID | Date | What | Why | Source |
| X-003 | 2026-11-12 | Curiosity (ICM) bonus | noisy-TV failure in our maze; needs dynamics model | S5, paper:pathak2017 |
## Parked
| ID | Date | Idea | Why parked | Revisit when | Source |
| B-004 | 2026-11-12 | Counts over learned abstraction | needs H-001 first | H-001 supported | /idea-discovery S5 #3 |
```
- **Decided**: every decision. Its full rationale lives in `decisions.md` under the same D-id.
- **Discarded**: rejected options, failed ideas, refuted hypotheses, each with the reason, so nobody retries them.
- **Parked**: deferred ideas with a checkable "Revisit when". Revived → row moves to Decided; dropped → to Discarded (noted "from B-###").
- Idea discovery reads it first; `/stage-summarizer` adds rows for everything decided/discarded/parked in the session.
- Prompts: *"Was ICM ever considered?"* · *"Park this idea until we have the baseline."* · *"Discard the PPO variant: unstable over seeds."*

### decisions.md: full rationale
ADR-style entry per D-id (Context · Decision · Alternatives · Consequences · Links). Changed decision → new entry with `Supersedes: D-###`.
The agent opens it only when it needs the *why* behind a D-id.

### hypotheses.md: what we're testing
Each `H-###` says in advance what would support or refute it; status `open → testing → supported | refuted | inconclusive`.
Refuted → also a Discarded row in backlog.md. *"Add a hypothesis: count-based bonuses beat ε-greedy on sparse-reward mazes."*

### log/YYYY-MM-DD.md: archive
Every session entry, forever. `/weekly-report` reads the week's entries from here.

### Why the agent files are terse
CLAUDE.md, the skills and the state files are written for the agent: short rules, one row per item, no figures or diagrams
(they cost context and the agent doesn't use them). This guide is the human-readable version; the agent never loads it.

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
/stage-summarizer stage -> implementation
```
Uses this session's conversation + `git status`/`git diff` (not memory of older sessions), then:
1. writes a session entry `S#` (did · files · results · decided/discarded · unfinished),
2. puts it at the top of `research/STATUS.md`, drops the oldest so 3 remain, sets the **Resume** line,
3. archives the entry in `research/log/<today>.md`,
4. adds backlog rows for every decision (Decided + decisions.md entry), rejection (Discarded) and deferral (Parked),
5. syncs `stage`, `idea`, `next` in the CLAUDE.md Pipeline Status block.

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
Decided/discarded · Questions for the advisor · Plan. Saved as `research/reports/weekly/2026-W45.md`.

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
| Paper figures | `/paper-figure` | for the paper only, not state files |
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
    → #2 → Decided (D-002); #1,#4 → Parked (B-003, B-004, with revisit conditions); #3,#5,#6 → Discarded (X-003…X-005, with reasons)
> "Add the hypotheses for idea #2."
    → H-001, H-002 in hypotheses.md
> /stage-summarizer stage -> implementation
    → STATUS.md gets S2: what was done, files, D-002/B-/X- ids, Resume: "write experiment plan for H-001"
```

**Tuesday, start a new session**
```
> "Where are we and what's next?"
    → agent read STATUS.md (last sessions + Resume line) + query_pack.md only; answers from them
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
