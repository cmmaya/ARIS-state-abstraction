---
name: weekly-report
description: "One-page advisor update from the week's session logs, backlog changes and results files, saved to research/reports/weekly/YYYY-Www.md. Use on Fridays or when the user says \"weekly report\", \"update for my advisor\", \"informe semanal\"."
argument-hint: "[— lang: es|en] [— since: YYYY-MM-DD]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(git log:*), Bash(date:*), Bash(ls:*)
---

# Weekly Report

Options: $ARGUMENTS. Default: lang en, since = today − 7 days.

## 1. Read

- research/log/*.md dated in [since, today] (session entries).
- research/backlog.md rows dated in the window.
- research/hypotheses.md entries whose status changed in the window.
- experiments/results/*.json changed in the window (`git log --since=<since> --name-only -- experiments/results/`); copy headline numbers.
- Previous report in research/reports/weekly/ (to mark last week's plan done/not done).

## 2. Write research/reports/weekly/<YYYY>-W<ww>.md (ISO week), ≤400 words

```
# Weekly update — week <ww> (<since> → <today>)
TL;DR: ≤3 bullets (main result, main decision, main blocker)
## Done        (✅/❌ against last week's plan)
## Results     table: what | value | source JSON
## Decided / discarded   (D-/X-/B- ids, one line each)
## Questions for advisor
## Next week
```

Rules: every number from a results JSON, cited. Plain language; no skill names or wiki ids. No progress → say so and why.

## 3. Reply

TL;DR + file path. Append "Weekly report: reports/weekly/<file>" to today's log.
