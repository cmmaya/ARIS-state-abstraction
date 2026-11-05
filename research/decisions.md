# Decisions

> Append-only log of methodology and project decisions. Read during methodology work.
> Never rewrite an old decision; if it changes, add a new one that says `Supersedes: D-###`.
> IDs are sequential: `D-001`, `D-002`, …

## Entry format

```markdown
### D-000 · <decision in one line>
- **Date:** YYYY-MM-DD
- **Context:** why a decision was needed
- **Decision:** what we chose
- **Alternatives considered:** what we didn't choose and why
- **Consequences:** what this commits us to / rules out
- **Links:** H-###, B-###, log/YYYY-MM-DD, wiki node ids (paper:…, idea:…)
- **Supersedes:** D-### (optional)
```

## Entries

### D-001 · Build the research repo on ARIS with project state files
- **Date:** 2026-11-05
- **Context:** Need persistent memory across agent sessions and a reproducible writing pipeline.
- **Decision:** Use ARIS skills + research wiki, add `research/` state files, three custom skills
  (stage-summarizer, related-work-matrix, weekly-report), a results→LaTeX macro script and a GitHub LaTeX workflow.
- **Alternatives considered:** Devcontainer/Docker pinned environment and rliable evaluation — deferred for now.
- **Consequences:** Session start reads only STATUS.md + query_pack.md; the paper never contains typed numbers.
- **Links:** log/2026-11-05
