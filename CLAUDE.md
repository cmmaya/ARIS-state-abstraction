# Project: {project-name}

Research repo on ARIS. Human guide: docs/GUIDE.md (don't load it). Load only the files the rule for the current task names.

## Pipeline Status

```yaml
stage: idle  # idle | idea-discovery | implementation | training | review | paper
idea: ""
contract: ""
current_branch: ""
baseline: ""
training_status: idle
language: en
active_tasks: []
next: ""
last_updated: ""
```

## Rules

- Session start: read research/STATUS.md (last 3 sessions) and research-wiki/query_pack.md. Nothing else until a task needs it.
- Session end: run /stage-summarizer.
- Prior work, ideas, results ("did we try X?", "which paper…"): /research-wiki query "<topic>" first; open wiki pages only if the pack names them. Never read the whole wiki.
- "Was X decided / discarded / parked?": read research/backlog.md.
- General concepts unrelated to the project: answer directly; no wiki, no state files.
- Methodology (design, metrics, baselines, seeds): read research/backlog.md, research/hypotheses.md; open research/decisions.md only for a D-id's rationale. New decision → D-### row in backlog.md "Decided" + full entry in decisions.md. New hypothesis → H-### in hypotheses.md.
- Idea discovery: read backlog.md first; don't re-propose Discarded items, or Parked items whose "Revisit when" isn't met. After selection: chosen → Decided; unselected → Parked (with revisit condition) or Discarded (with reason).
- Related work: /related-work-matrix → research/related_work_matrix.md.
- Experiments: write one JSON per run to experiments/results/ (format: experiments/results/README.md), then `python scripts/make_results_tex.py`.
- Writing paper/*.tex: read the relevant results JSON and STATUS.md. Numbers only via \res… macros from paper/results.tex; check with `python scripts/make_results_tex.py --lint-paper`.
- Friday / "weekly report": /weekly-report.
- Don't create figures, diagrams or schematics in state files.

## Files

- research/STATUS.md: last 3 sessions (did, files, results, decided, unfinished) + resume line. /stage-summarizer.
- research/backlog.md: ledger of Decided (D-), Discarded (X-), Parked (B-). One row each, never deleted.
- research/decisions.md: full rationale per D-id. research/hypotheses.md: H-ids + status.
- research/log/YYYY-MM-DD.md: archive of every session entry.
- research/related_work_matrix.md: papers × dimensions + gaps.
- research-wiki/: ARIS knowledge base (papers, ideas, experiments, claims); edit via ARIS skills only.
- RESEARCH_BRIEF.md: project direction (feeds query_pack).

## Project Constraints

- {constraint}

## Non-Goals

- {non-goal}

## Compute Budget

- {budget}
