---
name: weekly-report
description: "Turns research/STATUS.md and the week's logs into a one-page update for the advisor, saved to research/reports/weekly/. Use on Fridays or when the user says \"weekly report\", \"update for my advisor\", \"informe semanal\", \"what did I do this week\"."
argument-hint: "[optional: — lang: es | en, — since: YYYY-MM-DD]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(git log:*), Bash(date:*), Bash(ls:*)
---

# Weekly Report

Options: $ARGUMENTS
- `— lang: es` writes the report in Spanish (default: English).
- `— since: YYYY-MM-DD` overrides the start date (default: 7 days before today).

## Step 1 — Gather

1. `research/STATUS.md`.
2. `research/log/*.md` with dates in [since, today].
3. `research/decisions.md`, `research/hypotheses.md`, `research/backlog.md` — only entries added or changed in the window
   (use dates in entries; `git log --since=<since> -p -- research/` if it's a git repo).
4. `ls experiments/results/` — results files modified in the window. Open each one to copy its headline numbers.
5. The previous report in `research/reports/weekly/` (if any) — to check what was promised last week.

## Step 2 — Write `research/reports/weekly/<YYYY>-W<ww>.md` (ISO week)

One page, **≤ 400 words**, this structure:

```markdown
# Weekly update — <Name/project> — week <ww> (<since> → <today>)

**TL;DR**
- (3 bullets max: the most important result, decision, and blocker)

## Done this week
- … (link D-/H- ids; mark items promised last week as ✅ or ❌)

## Results
| What | Value | Source |
|------|-------|--------|
| … | … | `experiments/results/<file>.json` |

## Decisions
- `D-###` … (one line each)

## Blockers / questions for you
- … (concrete, answerable questions)

## Plan for next week
- [ ] … (from STATUS.md next steps)
```

Rules:
- Every number must come from a results file and cite it. No numbers from memory or logs alone.
- Plain language for the advisor; no internal tool names (`/skill`, wiki node ids) except D-/H- ids.
- If the week had no progress, say so plainly and state why.

## Step 3 — Record and report

Append "Weekly report written: reports/weekly/<file>" to today's log. Reply with the TL;DR and the file path.
