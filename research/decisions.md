# DECISIONS
<!-- Full rationale for each D-id in backlog.md "Decided". Append-only; a changed decision gets a new entry with "Supersedes: D-###".
Format:
### D-### · title
Date · Context · Decision · Alternatives · Consequences · Links -->

### D-001 · Build the research repo on ARIS with project state files
- Date: 2026-11-05
- Context: need memory across agent sessions and a reproducible writing pipeline.
- Decision: ARIS skills + research wiki; research/ state files; custom skills stage-summarizer, related-work-matrix, weekly-report; results→LaTeX macros; GitHub LaTeX CI.
- Alternatives: devcontainer and rliable now → parked (B-001, B-002).
- Consequences: sessions start from STATUS.md + query_pack.md; paper uses only \res… macros.
- Links: S1
