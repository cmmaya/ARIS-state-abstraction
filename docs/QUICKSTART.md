# Quick start: validating ideas, future work, methodology, formulation

For the current phase: validate initial ideas → sort future work → fix the methodology → write the math.
Details for any command: `/help-aris <skill>`. Full manual: [GUIDE.md](GUIDE.md).

> **✱ = needs a reviewer model.** These skills send your idea/proof to a second model for criticism.
> Reviewer = Codex with your ChatGPT account: **set up and working** (GUIDE §0). Reviews count against your ChatGPT usage.

---

## 0. Before the first session (10 min)

1. Fill **`RESEARCH_BRIEF.md`**: problem, what's missing in current approaches, constraints, non-goals. Every idea and wiki
   query is aimed by it.
2. In **`CLAUDE.md`** fill *Project Constraints*, *Non-Goals*, *Compute Budget*. If you have no GPU yet, write
   `No GPU pilots: validate ideas on paper only.`
3. Start `claude` in the repo folder. Each session then starts from `research/STATUS.md` + the wiki query pack automatically.

---

## 1. Ground yourself in the literature (fills the knowledge wiki)

| Command | What you get |
|---------|--------------|
| `/research-lit "state abstraction for sparse-reward RL"` | literature review; papers auto-ingested into `research-wiki/papers/` |
| `/research-wiki ingest "<title>" — arxiv: <id>` | add one specific paper you already know |
| `/wiki-enrich` | fills the empty sections of papers ingested as stubs |
| `/related-work-matrix` | papers × (formulation, state space, reward, evaluation) table, **gaps** with G-ids, related-work hooks |
| `/alphaxiv <arxiv id>` | quick summary of one paper |
| drop PDFs in `literature/`, then *"I added literature/<file>, ingest it"* | wiki page per paper, enriched from the PDF (dropping alone doesn't update the wiki) |
| `/research-lit "<topic>" — sources: local` | review of only your PDFs in `literature/` |

Ask in plain words afterwards: *"Which papers learn abstractions with bisimulation metrics?"* → the agent queries the wiki, not the web.

---

## 2. Validate initial ideas

You already have ideas → test them one by one. You don't → generate first.

| Step | Command | Output |
|------|---------|--------|
| Generate + rank ideas | `/idea-creator "<direction>" — pilot budget: 0h` | `idea-stage/IDEA_REPORT.md` (paper-only, no GPU) ✱ |
| Full pipeline (lit → ideas → novelty → review) | `/idea-discovery "<direction>" — AUTO_PROCEED: false` | same report, with checkpoints asking you ✱ |
| Has someone done it? | `/novelty-check "<idea in 3–5 sentences>"` | `NOVELTY_DOSSIER.md`: closest papers, what's new, risk ✱ |
| Is it any good? | `/research-review "<idea or file>"` | critical review: weaknesses, missing baselines, killer questions ✱ |
| Turn a vague idea into a method | `/research-refine "<idea>"` | `refine-logs/FINAL_PROPOSAL.md` after review rounds ✱ |

Tips:
- Be specific: *"bisimulation-based state abstraction with reward-free pretraining for sparse-reward navigation"*, not *"RL abstraction"*.
- Validate on paper first (novelty + review). Pilots only once the methodology (§4) is fixed.
- Write the idea as a hypothesis: *"Add H-001: … supported if …, refuted if …"* → `research/hypotheses.md`.

---

## 3. Categorize future work (the backlog)

Every idea ends up in exactly one table of `research/backlog.md`:

| Outcome | Table | Say |
|---------|-------|-----|
| We do it | **Decided** `D-` | *"Decide idea #2: …because…"* (full rationale goes to `decisions.md`) |
| Not now, maybe later | **Parked** `B-` | *"Park idea #4 until H-001 is supported."* (needs a checkable *revisit when*) |
| Never (and why) | **Discarded** `X-` | *"Discard idea #3: novelty-check found <paper> does it."* |

- After `/idea-creator` / `/idea-discovery`, the agent files every unselected idea as Parked or Discarded automatically (CLAUDE.md rule).
- Gaps from the matrix you won't pursue → *"Park gap G3 as future work."*
- Check anytime: *"What's parked and is any of it due?"* · *"Was <approach> ever discarded?"*
- Future-work section of the paper later = the Parked table.

---

## 4. Establish the methodology

| Step | Command | Output |
|------|---------|--------|
| Method + experiment plan in one go | `/research-refine-pipeline "<chosen idea>"` | `refine-logs/FINAL_PROPOSAL.md` + `EXPERIMENT_PLAN.md` ✱ |
| Experiment plan from a fixed method | `/experiment-plan` | `refine-logs/EXPERIMENT_PLAN.md`: claims, baselines, metrics, seeds, run order |
| Ablations reviewers will ask for | `/ablation-planner "<method or claim>"` | ablation list with priorities ✱ |
| Stress-test the plan | `/research-review "refine-logs/EXPERIMENT_PLAN.md"` | weaknesses before you spend compute ✱ |

Then record the choices: *"Record decisions: 3 baselines (…), metric …, 5 seeds, environments …"* → `D-` rows in backlog.md +
rationale in decisions.md. Each claim in the plan → an `H-` entry with its support/refute criterion.

---

## 5. Mathematical formulation

| Step | Command | Output |
|------|---------|--------|
| Build the formulation from notes | `/formula-derivation "<problem, objects, current equations or notes file>"` | `DERIVATION_PACKAGE.md`: objects, assumptions, derivation chain, or the exact blocker |
| Prove a statement | `/proof-writer "<theorem + assumptions>"` | `PROOF_PACKAGE.md`: proof, or corrected/weaker claim + what's missing |
| Check a proof rigorously | `/proof-checker <file.tex or .md>` | `PROOF_AUDIT.md`: gaps found and fixed ✱ |
| Hardest claims, formally | `/lean-formalize "<statement>"` | Lean proof + axiom check (needs Lean installed) |

Tips:
- Start with `/formula-derivation` while definitions still move (MDP, abstraction map φ, value-loss bound…); use
  `/proof-writer` only once the statement is fixed.
- These skills don't write into `paper/*.tex` unless you ask. Move the result into the paper when it's stable.
- Fixed definitions/assumptions are decisions: *"Record decision: abstraction is a deterministic map φ: S → Z, …"*.

---

## 6. Every session

| When | Do |
|------|----|
| Start | just ask *"Where are we?"* (reads STATUS = last 3 sessions + Resume line) |
| End | `/stage-summarizer` (logs the session, files every decided/discarded/parked item) |
| Friday | `/weekly-report — lang: es` (advisor update) |
| Lost | `/help-aris <goal in words>`, e.g. `/help-aris check if my bound is tight` |

## Suggested first week

1. `RESEARCH_BRIEF.md` → `/research-lit "<topic>"` → `/related-work-matrix`
2. Each initial idea → `/novelty-check` → `/research-review` → Decided / Parked / Discarded
3. Chosen idea → `/research-refine-pipeline` → record D-/H- entries
4. Core definitions → `/formula-derivation` → key lemma → `/proof-writer` → `/proof-checker`
5. `/stage-summarizer` at the end of every session
