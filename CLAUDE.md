# Project: BPMN+OPT State Abstraction

Research repo on ARIS. Human guide: docs/GUIDE.md (don't load it, except inside /help-aris). Load only the files the rule for the current task names.

## Pipeline Status

```yaml
stage: implementation  # idle | idea-discovery | implementation | training | review | paper
idea: "idea:language_derived_abstraction_levels (D-002)"
contract: ""
current_branch: ""
baseline: "BPMN+OPT hand-made abstraction (n_P1, n_P2, I); FIFO/SPT policies"
training_status: idle
language: en
active_tasks: ["Formalize Level 1 on Fig. 2, exponential durations (324 states)", "Verify chair release semantics in simpn (H-002)", "Abel bound for R6/R7 on uniformized safe-route model (H-003)"]
next: "Formalize Level 1 (R1-R4, R3b) on Fig. 2, exponential durations (324 states), per research/abstraction_rules.md; check chair release in simpn (H-002)"
last_updated: "2026-11-06"
```

## Rules

- Session start: read research/STATUS.md (last 3 sessions) and research-wiki/query_pack.md. Nothing else until a task needs it.
- Session end: run /stage-summarizer.
- Prior work, ideas, results ("did we try X?", "which paper…"): /research-wiki query "<topic>" first; open wiki pages only if the pack names them. Never read the whole wiki.
- "Was X decided / discarded / parked?": read research/backlog.md.
- "What's left / to-do / what do we still need to check?": read research/checklist.md. New open check → C-## item there; done → tick [x] with date + evidence.
- New file(s) in literature/ ("I added/sent a paper", "ingest the new files"): for each PDF not yet in research-wiki/index.md, read its first pages, get title/authors/year/venue (and arXiv id or DOI if printed), run `python3 .aris/tools/research_wiki.py ingest_paper research-wiki/ …` with them (prefer --arxiv-id), then /wiki-enrich the new page(s) from the PDF. Non-paper documents: ingest only if the user asks; otherwise just read them for the task. Reply with the new paper:<slug> ids.
- General concepts unrelated to the project: answer directly; no wiki, no state files.
- Methodology (design, metrics, baselines, seeds): read research/backlog.md, research/hypotheses.md; open research/decisions.md only for a D-id's rationale. New decision → D-### row in backlog.md "Decided" + full entry in decisions.md. New hypothesis → H-### in hypotheses.md.
- Idea discovery: read backlog.md first; don't re-propose Discarded items, or Parked items whose "Revisit when" isn't met. After selection: chosen → Decided; unselected → Parked (with revisit condition) or Discarded (with reason).
- Related work: /related-work-matrix → research/related_work_matrix.md.
- Experiments: write one JSON per run to experiments/results/ (format: experiments/results/README.md), then `python scripts/make_results_tex.py`.
- Writing paper/*.tex: read the relevant results JSON and STATUS.md. Numbers only via \res… macros from paper/results.tex; check with `python scripts/make_results_tex.py --lint-paper`.
- Friday / "weekly report": /weekly-report.
- "How do I use /x?", "which skill for…?", "make a new skill": /help-aris.
- Don't create figures, diagrams or schematics in state files.

## Files

- research/STATUS.md: last 3 sessions (did, files, results, decided, unfinished) + resume line. /stage-summarizer.
- research/backlog.md: ledger of Decided (D-), Discarded (X-), Parked (B-). One row each, never deleted.
- research/decisions.md: full rationale per D-id. research/hypotheses.md: H-ids + status.
- research/log/YYYY-MM-DD.md: archive of every session entry.
- research/related_work_matrix.md: papers × dimensions + gaps.
- research/checklist.md: the to-do list. Every open check, proof, computation and pending decision (C-##), grouped by phase, with done-when criteria.
- research/abstraction_rules.md: rule catalog R1–R7, R3b (level, route, ε, checks on Figs. 1–2). Add new rules in its template.
- research-wiki/: ARIS knowledge base (papers, ideas, experiments, claims); edit via ARIS skills only.
- RESEARCH_BRIEF.md: project direction (feeds query_pack).
- literature/: user's reference PDFs/docs (not in git). Read only the file a task names.

## Project Constraints

- Every abstraction must carry a stated guarantee (zero loss, computed bound, or estimated a posteriori) derived from BPMN+OPT annotations.
- Rules act on observable (elapsed) time, never on residual event times (latent in BPMN+OPT Def. 2).
- Report discounted bounds as a proxy; evaluate on the undiscounted H = 200 flow-time objective in simpn (github.com/bpogroup/simpn, branch bpmnopt) (D-007).
- Only Abel et al. 2016 has been re-read against the source; verify theorem numbers of other references before citing them.

## Non-Goals

- Level 4 (φ_π*) as a target; FIFO/SPT are baselines only.
- Claiming SMDP discounting or discrete-step finite-horizon bounds as novel (X-006, X-007).
- An LLM proposer as a core method (optional comparison, B-004).

## Compute Budget

- Not yet stated. Current work is tabular/theory on small fragments (Fig. 2 exact: 324 states).
<!-- ARIS:BEGIN -->
## ARIS Skill Scope
ARIS skills installed in this project: 82 entries.
Manifest: `.aris/installed-skills.txt`
ARIS repo root: `C:\Users\Camilo\Documents\Trabajo\Master projects\Auto-claude-code-research-in-sleep`
Project skill path: `.claude/skills/<skill-name>`
For ARIS workflows, prefer the project-local skills under `.claude/skills/`.
Do not edit or delete junctioned skills in place; update upstream or rerun:
`powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\Camilo\Documents\Trabajo\Master projects\Auto-claude-code-research-in-sleep\tools\install_aris.ps1" "C:\Users\Camilo\Documents\Trabajo\Master projects\ARIS" -Platform claude -Reconcile`
<!-- ARIS:END -->
