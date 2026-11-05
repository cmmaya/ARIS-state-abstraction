---
name: stage-summarizer
description: "End-of-session summarizer. Reads the research logs, decisions.md, hypotheses.md and backlog.md, rewrites research/STATUS.md (stage, current idea, decisions, open questions, next steps) and redraws a Mermaid schematic of the current idea. Use when the user says \"end session\", \"wrap up\", \"summarize the stage\", \"update status\", or at the end of every working session."
argument-hint: "[optional: note to include, e.g. \"stage -> implementation\"]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(git log:*), Bash(git status:*), Bash(git diff:*), Bash(date:*), Bash(ls:*)
---

# Stage Summarizer

Extra note from the user (may be empty): $ARGUMENTS

Goal: leave `research/STATUS.md` as an accurate, short, **sourced** snapshot so the next session can start by reading
only `STATUS.md` + `research-wiki/query_pack.md`.

## Step 1 — Gather (read only what is listed)

1. `research/STATUS.md` (current version; note its `Last updated` date = **D0**).
2. All `research/log/*.md` files dated **on or after D0** (filename = date). If none, use the latest log file.
3. `research/decisions.md` — only entries dated on or after D0, plus any decision still referenced in STATUS.
4. `research/hypotheses.md` — every entry whose status is not `dropped` (title + status + evidence lines only).
5. `research/backlog.md` — entries added on or after D0, and any entry whose "Revisit when" condition now looks met.
6. The `## Pipeline Status` YAML block in `CLAUDE.md`.
7. `git log --since=<D0> --oneline` and `git status --short` (if the folder is a git repo) to see what changed.
8. `ls experiments/results/` — list results files modified since D0 (names only; open one only if a hypothesis status depends on it).

Do **not** read the research wiki pages, the paper, or code unless a log entry is ambiguous and one file resolves it.

## Step 2 — Write today's log

Append (or create) `research/log/<today YYYY-MM-DD>.md` with a `## Session summary` section: 3–6 bullets of what was done
this session, each with a pointer (file, D-/H-/B- id, results file). Include `$ARGUMENTS` if given.

## Step 3 — Rewrite `research/STATUS.md`

Keep exactly these sections, in this order, under ~150 lines total:

```markdown
# STATUS

> (keep the existing 3-line header note)

**Last updated:** <today> · **Stage:** <stage> (<sub-stage or one-word note>)

## Current idea
One paragraph (≤ 120 words): problem, approach, why it might work, current evidence. Cite H-/D- ids.

## Schematic
(mermaid flowchart — see Step 4)

## Recent decisions
- `D-###` one line (source). Keep the last ~5; older ones live in decisions.md.

## Open questions
- Concrete questions blocking progress. Mark ones for the advisor with **(advisor)**.

## Next steps
- [ ] Ordered, concrete, verifiable actions (≤ 7). Carry over unchecked items that still apply; drop done ones.
```

Rules:
- **Never invent.** Every sentence must trace to a gathered source; cite it inline (`log/2026-11-05`, `D-003`, `H-002`,
  `experiments/results/x.json`). If something is unknown, write it as an open question.
- Stage is one of: `idle | idea-discovery | implementation | training | review | paper` (same vocabulary as CLAUDE.md).
- Numbers: only copy a number if it appears in a results file; cite the file.
- If a backlog item's "Revisit when" condition looks met, add an open question: "Revisit B-### ? (condition met: …)".

## Step 4 — Mermaid schematic of the current idea

Draw a `flowchart LR` (or `TD` if > 8 nodes) of the **current idea**, not of the repo:
problem/gap → method components → what is measured → hypotheses being tested.

- ≤ 12 nodes. Node ids are plain `[A-Za-z0-9_]`; every label in double quotes: `M1["Reward shaping via ..."]`.
- Put hypothesis ids on edges or nodes they test: `M1 -->|H-002| E1`.
- Style refuted/failed parts with `:::failed` and add `classDef failed stroke-dasharray: 5 5,opacity:0.6;`.
- No parentheses, brackets or `"` inside labels (use `-` or `,`). No HTML.
- If no idea is selected yet, keep a 3-node Problem → Method → Evaluation placeholder.

## Step 5 — Sync CLAUDE.md

In the `## Pipeline Status` YAML block of `CLAUDE.md`, update **only** `stage`, `idea`, `next` (first unchecked next step)
and `last_updated`. Do not touch other fields or any other part of CLAUDE.md.

## Step 6 — Report

Reply with: the new stage, the 3 most important next steps, and any backlog items to revisit. No full file dump.
