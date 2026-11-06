---
name: stage-summarizer
description: "End-of-session summarizer: adds this session to research/STATUS.md (keeps the last 3 sessions), archives it in research/log/, and records every decision, discard and parked idea in research/backlog.md. Use when the user says \"end session\", \"wrap up\", \"update status\", \"summarize the session\", or at the end of every working session."
argument-hint: "[optional note, e.g. \"stage -> implementation\"]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(date:*)
---

# Stage Summarizer

Note: $ARGUMENTS

Source of truth = this session's conversation + `git status --short` + `git diff --stat` (+ `git log --oneline` for commits made this session). Read research/STATUS.md, research/backlog.md and research/checklist.md. Don't read other files unless a fact needs checking.

## 1. Session entry

Session number = highest S# in STATUS.md + 1. Exact facts only; no invention; numbers only if they're in a results file (cite it).

```
## S<n> · <YYYY-MM-DD> · <goal, ≤8 words>
- Did: <what was done, concrete, ≤3 lines>
- Files: <created/changed files, comma-separated>
- Results: <metric = value (experiments/results/x.json)> or —
- Decided/discarded: <D-/X-/B-/H- ids touched this session> or —
- Unfinished: <exactly where work stopped, next concrete action> or —
```

## 2. research/STATUS.md

Rewrite as:
```
# STATUS
<!-- keep existing comment line -->

**Resume:** <single next action, with file/command>
**Stage:** <stage> · **Updated:** <today>

<new entry>
<previous 2 entries, unchanged>
```
Keep exactly the 3 newest sessions; drop older ones (they're already in log/). No other sections.

## 3. research/log/<today>.md

Append the same entry (create the file with `# <today>` if missing).

## 4. research/backlog.md

For each item from this session add one row (next free ID in that section; Source = S<n>):
- Decision taken → Decided. If it has no full entry in research/decisions.md, append one.
- Option/idea/approach rejected, hypothesis refuted, idea failed → Discarded, with the reason.
- Idea deferred → Parked, with a checkable "Revisit when".
- Parked item revived/dropped → move its row (note "from B-###").
Update hypotheses.md status if a hypothesis changed.

## 5. research/checklist.md

Tick `[x]` every C-## item finished this session, appending `(S<n>, <date>, evidence: file/results/D-id)`. Add a new C-## item (next free ID, right section, with "Done when") for every new open check, proof, computation or pending decision. Never delete items. The STATUS `Unfinished` line names the C-ids it refers to.

## 6. CLAUDE.md

In the Pipeline Status YAML, update only `stage`, `idea`, `next` (= Resume line), `last_updated`.

## 7. Reply

3 lines max: session id, Resume line, new backlog and checklist ids.
