# Project: {project-name}

> Research repo built on ARIS (Auto-Research-In-Sleep) plus our own additions.
> Full how-to: `docs/GUIDE.md`. This file is loaded at every session, so it stays short and
> **routes each task to the files it needs**. Do not load files that the rule for a task doesn't name.

## Pipeline Status

<!-- ARIS skills read and update this block. The stage-summarizer keeps `stage` and `next` in sync with research/STATUS.md. -->

```yaml
stage: idle          # idle | idea-discovery | implementation | training | review | paper
idea: ""             # Current idea title (one line)
contract: ""         # Path to research_contract.md (e.g., idea-stage/docs/research_contract.md)
current_branch: ""   # Git branch for this idea
baseline: ""         # Baseline numbers for comparison
training_status: idle  # idle | running | complete | failed
language: en         # en | zh — controls skill output language
active_tasks: []
next: ""             # Concrete next step
last_updated: ""     # YYYY-MM-DD HH:mm — auto-updated by skills on every output write
```

## Routing rules

**Session start** → read `research/STATUS.md` and `research-wiki/query_pack.md` only. Nothing else until a task needs it.

**Session end** → run `/stage-summarizer` (updates `research/STATUS.md`, today's log, and the Mermaid schematic).

**Any question about prior work, ideas or results** ("what did we try for…", "which paper did…", "did X work?")
→ run `/research-wiki query "<topic>"` first. Open full wiki pages (`research-wiki/papers|ideas|experiments|claims/*.md`)
**only if the query pack points to them**. Never read the whole wiki or `ls`-and-read every page.

**General concepts unrelated to this project** (e.g. "what is a Bellman operator?") → answer directly; do not touch the wiki.

**Methodology work** (design of experiments, metrics, baselines, ablations) → read `research/decisions.md` and `research/hypotheses.md`.
Record any new decision as a `D-###` entry and any new testable hypothesis as an `H-###` entry.

**Idea discovery** (`/idea-discovery`, `/idea-creator`, brainstorming) → check `research/backlog.md` first (don't re-propose parked ideas
unless their "revisit when" condition is met). After selection, **append every unselected idea to `research/backlog.md`** in the entry format there.

**Related work** → update `research/related_work_matrix.md` with `/related-work-matrix`.

**Experiments** → each run writes a JSON file to `experiments/results/` (format: `experiments/results/README.md`).
Then run `python scripts/make_results_tex.py` to regenerate `paper/results.tex`.

**Writing** (`/paper-write`, editing `paper/*.tex`) → read the latest results file(s) and `research/STATUS.md`.
Use macros from `paper/results.tex` (e.g. `\resBaselineReturnMean`), **never typed numbers**.
Check with `python scripts/make_results_tex.py --lint-paper`.

**Friday** (or "weekly report") → run `/weekly-report`.

## State files (what lives where)

| File | Holds | Who writes it |
|------|-------|---------------|
| `research/STATUS.md` | current stage, recent decisions, open questions, next steps, schematic | `/stage-summarizer` |
| `research/backlog.md` | parked ideas (`B-###`) with source, related decision, why parked, revisit-when | idea discovery + you |
| `research/decisions.md` | decisions (`D-###`), append-only | you / agent during methodology work |
| `research/hypotheses.md` | testable hypotheses (`H-###`) and their status | you / agent; `/result-to-claim` evidence |
| `research/related_work_matrix.md` | papers × dimensions table + gaps | `/related-work-matrix` |
| `research/log/YYYY-MM-DD.md` | what happened each day | agent during the session, `/stage-summarizer` |
| `research-wiki/` | papers, ideas, experiments, claims + graph (ARIS) | ARIS skills via `research_wiki.py` |
| `RESEARCH_BRIEF.md` | project direction; feeds the wiki query pack | you |

## Project Constraints

- {constraint 1}

## Non-Goals

- {non-goal 1}

## Compute Budget

- {budget details}
