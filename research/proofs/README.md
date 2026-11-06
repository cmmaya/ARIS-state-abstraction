# research/proofs

One folder for each checklist item that ends in a proof or formal statement, for example C-01–C-06, C-10, C-11, C-13, C-24 and C-25.

## Layout

```
research/proofs/
  C-01_level1_exactness/
    main.tex              statement + assumptions + proof (standalone article, compiles on its own)
    PROOF_AUDIT.md        written by /proof-checker (cumulative audit log)
    PROOF_SKELETON.md     written by /proof-checker
    PROOF_CHECK_STATE.json
    proof_audit_report.tex / .pdf
```

- Name each folder `<C-id>_<short_slug>`, using the id from research/checklist.md. Make one folder per item, even when a later item reuses an earlier result. In that case `\input` or cite the earlier folder.
- `main.tex` is the file of record. Its first lines are a comment header:

  ```latex
  % C-id: C-01   Status: draft | checked | unrecoverable
  % Links: D-003, claim:level1_horizon_independent, rules R1-R4
  % Assumptions: exponential durations, Fig. 2, elapsed-time state (no residuals)
  ```

- Put each result in a `\begin{theorem}...\label{thm:...}` block (or lemma/proposition), so that /proof-checker's statement table can find it.

## Workflow

1. Draft: `/proof-writer` with the target `research/proofs/<C-id>_<slug>/main.tex`. Without a target it writes `PROOF_PACKAGE.md` in the repo root, so always pass the target.
2. Check: run `/proof-checker` on that folder. Its audit files land next to `main.tex`.
3. When the acceptance gate passes, set `Status: checked` in the header. Then tick the C-id in research/checklist.md with `evidence: research/proofs/<folder>/main.tex + PROOF_AUDIT.md`, and update the linked wiki claim status.
4. If the proof fails, set `Status: unrecoverable`. Leave the C-id open and add a new C-## item for the missing assumption or lemma.

Numbers that come out of a proof (ε values, bound constants evaluated on Fig. 2) still go to experiments/results/*.json, so the paper reads them through `\res…` macros.
