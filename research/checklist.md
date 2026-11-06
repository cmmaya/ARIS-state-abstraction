# CHECKLIST
<!-- Everything left to check, prove, compute or decide. One item per check; never delete — tick [x] with date + evidence.
IDs C-## are stable. Link H-/D-/B-/RQ ids and research/abstraction_rules.md rules. Updated by /stage-summarizer.
Order within a section = suggested order. "Blocks" = items that cannot finish before this one.
Where evidence lives: proofs → research/proofs/<C-id>_<slug>/ (main.tex + PROOF_AUDIT.md); numbers → experiments/results/*.json;
decisions → D-id in backlog.md; hypotheses → hypotheses.md; parameters and ε formulas → abstraction_rules.md. -->

Proof items (folder research/proofs/<C-id>_<slug>/): C-01–C-06, C-10, C-11, C-13, C-24, C-25.

Verified arithmetic on 2026-11-06, for reference. With φ₁: P1 ~ U(2,4), P2 ~ U(3,5) and φ₂: U(4,6), U(5,7) (inferred from Erlang k = 27, 48, 75, 108 = mean²/var):
- Exact exponential Level 1: 36 × 3 × 3 = 324.
- Binned at Δ = 0.5: 36 × (1+8+10) × (1+12+14) = 18,468.
- Erlang: 36 × (1+27+48) × (1+75+108) = 503,424.
- Paper's abstraction: 36 × 4 = 144.
- Other values: e^(−0.1) − e^(−0.14) = 0.035; d_TV(U(2,4), U(3,5)) = 0.5; 18,468 × 0.05 = 923.
- The φ₂ durations were inferred; confirmed against simpn's fig2_problem.json on 2026-11-06 (C-14).

## A. Level 1 theory (phase 1)
- [ ] **C-01 · Exactness theorem for R1–R4 on the SMDP.** Prove each rule preserves the joint law of (next abstract state, holding time τ, reward) for every action. That makes φ a model-irrelevance abstraction of the SMDP, not just of the embedded MDP. Done when: proof written and checked (/proof-checker). Links: D-003, claim:level1_horizon_independent. Assumptions fixed by D-010 (unbounded queues, corollary at K = 5) and D-011 (generic exponential rates). Blocks: C-02, C-20.
- [ ] **C-02 · Horizon and discount independence.** Show that exactness gives policy preservation for γ = 1 and finite H = 200 (time horizon), not only for discounted objectives. Done when: the statement and proof are in the formalization; the claim status moves from drafted to verified.
- [ ] **C-03 · R3 on elapsed time.** Show that dropping the elapsed time of an exponential event is exact when the state carries elapsed rather than residual time. Also show that residual times are latent under BPMN+OPT Def. 2. Done when: Def. 2 is re-read and quoted, and the argument is written. Links: X-008.
- [ ] **C-04 · R3b phase-type exactness.** Prove that the phase index makes the PH model Markov and the merge exact on the model. State clearly that the guarantee is for the PH model, not the original uniform model. Links: D-004, C-26.
- [ ] **C-05 · R2 with identity-bound actions.** Actions such as x_t(c₁, φ₁) name objects. Check that counting cases and resources keeps the action set well-defined, via an SMDP homomorphism (Ravindran & Barto 2003): a state-dependent action map that preserves feasibility masks (Con) and decision moments (Mom). Done when: the action mapping is defined for Figs. 1 and 2.

## B. Level 2 theory, safe route (phase 2)
- [ ] **C-06 · Uniformization of the safe-route model.** Build the CTMDP for exponential/PH Fig. 2, pick the uniformization rate Λ, and derive the per-step discount Λ/(Λ+β). Convert bounds to continuous-time units. Done when: Λ, β and the resulting γ are fixed and documented. Links: D-004, paper:puterman1994_markov_decision_processes.
- [ ] **C-07 · Zero-length epochs break γ_max < 1.** Same-time sequential decisions give τ = 0, so γ(s,a) = E[e^(−βτ)] = 1 and γ_max = 1. All Abel bounds then diverge, even on the safe route. Resolve by collapsing same-time decisions into one joint epoch, by bounding the number of consecutive zero-length epochs, or by defining the discount per uniformization step. Done when: a resolution is chosen and stated (new D-id). Blocks: C-08, C-21.
- [ ] **C-08 · Abel bound for R6 and R7 merges.** Compute ε_R, ε_T and |S_A| for R6 (δ-close ptimes) and R7 (cap K) on the uniformized model. Evaluate 2ε_R/(1−γ)² + 2γ|S_A|ε_T/(1−γ)³ and compare it with 1/(1−γ). Done when: a results JSON exists and H-003 is resolved.
- [ ] **C-09 · ε formulas for R7.** research/abstraction_rules.md gives no ε_R or ε_T for queue truncation. Derive them from the arrival and service annotations, including how blocked or lost arrivals affect the flow-time reward. Done when: R7's block is filled.
- [ ] **C-10 · Lemma 2 split into ε_R and ε_T.** The split loss ≤ 2ε_R/(1−γ)² + 2γ|S_A|ε_T/(1−γ)³ was derived through the proof's intermediate step, and it swaps |S_G| − 1 for |S_A|. Check this step against Abel et al. 2016 before using it. Done when: checked line by line (/proof-checker).
- [ ] **C-11 · Full ε_T for the Fig. 2 binning example.** The bound ε_T ≤ Δ/10 covers only the event "service finishes before the next exp(10) arrival", and only for elapsed time e < 2 on U(2,4). Extend it to every next abstract state, to e ≥ 2 (hazard changes inside the support), and to U(3,5), U(4,6), U(5,7). This affects the vacuity numbers for RQ2. Links: X-004, R5.

## C. Level 3 (phase 4)
- [ ] **C-12 · Monte Carlo protocol for ε̂.** Fix the baseline policy (FIFO), the state-sampling scheme, the number of rollouts per (state, action), the CI method, and the acceptance threshold. Done when: the protocol is written and H-006 is testable.
- [ ] **C-13 · Level 3 bound constants.** Verify Abel Lemma 1 (2ε/(1−γ)², confirmed) and the Bertsekas 2012 aggregation bound ε̂/(1−α), including the section number. Settle how either is reported at γ = 1. Links: D-005.

## D. Model and simulator (simpn, branch bpmnopt)
- [x] **C-14 · Fig. 2 parameters.** Read the exact distributions from the model or JSON: arrivals exp(10); oncologist × patient-type durations (φ₂'s U(4,6) and U(5,7) are inferred); routing and tie-breaking (longest waiting); queue cap. Done when: the parameters are recorded in research/abstraction_rules.md. Blocks: C-20, C-21, C-22. (2026-11-06, evidence: research/abstraction_rules.md "Model parameters"; simpn bpmnopt @8776bf0. φ₂ = U(4,6), U(5,7) confirmed; P(P1) = 0.5; no queue cap in the model (→ C-29); tie-breaking lives in the policies.)
- [x] **C-15 · Chair release semantics (H-002).** Check whether infusion returns the chair token on completion, or trace for a chair taken by another patient between one patient's infusion and observation. Held means the idle count is exact. Released means R2 needs reserved-chair counts. (2026-11-06, evidence: experiments/results/c15_chair_trace_fig1.json, simpn/prototypes.py:412, fig1_problem.json. Released, and Observation takes any idle chair because the guard is not implemented, so chairs are pooled and the idle count is exact for simpn. H-002 refuted as stated; semantics chosen in D-009.)
- [ ] **C-16 · `measurements` never read.** Confirm with the BPMN+OPT authors whether routing is meant to ignore clinical state or a constraint is missing. Done when: the answer is recorded and R1's Fig. 1 check is updated.

## E. Literature and novelty
- [ ] **C-17 · Theorem numbers of all references except Abel 2016.** Check Li 2006 (ladder, π* result), Subramanian 2022 (Thm 9 finite horizon, Thm 27; numbers came from an alphaxiv overview), Ni 2023 (Thm 8, H² growth), Puterman Ch. 11 sections, Bertsekas Vol. II aggregation section, Ravindran & Barto 2003, Schweitzer 1971. Done when: each is checked against the PDF and the wiki page is updated.
- [ ] **C-18 · Overlap with Buchholz et al. 2017.** Their aggregation bounds for CTMDPs with phase-type block sojourns are close to the safe route. Read the paper and state what the safe route adds: annotation-derived φ, BPMN+OPT semantics, and computed ε. Done when: the related-work matrix row and D-006 wording are checked.
- [ ] **C-19 · Missing PDFs.** Put Li 2006, Abel 2020, Ravindran & Barto 2003, Buchholz 2017, Schweitzer 1971 and the relevant chapters of Puterman and Bertsekas in literature/, then run /wiki-enrich. Also add the two working documents cited in the notes, the "AIS audit protocol" and the "Validation notes", which are not in the repo.

## F. Experiments (RQ1–RQ3; one JSON per run in experiments/results/)
- [ ] **C-20 · RQ1: state counts at Levels 0, 1 and 2.**
  - Define Level 0 so it is finite and countable. With uniform durations the ground state includes continuous event times, so it is infinite. Options: count Level 0 under exponential durations with object identities and queue order, or report it as infinite and count the reachable states of a discretized ground model.
  - Write a script that enumerates reachable states rather than relying on closed-form products. Reproduce 144, 324, 18,468 and 503,424, then add Fig. 1.
  - Done when: the JSONs and `\res…` macros exist. Depends on: C-01, C-14.
- [ ] **C-21 · RQ2: empirical loss vs bound as the discretization parameter and K vary (Fig. 2).**
  - [x] Axis per route: decided by D-008 (S2, 2026-11-06). Safe route: (δ, K) against the Abel bound. Rigorous route: (Δ, K) against the AIS bound, only if B-003 is revived.
  - Safe route: the empirical-loss reference is the exact optimum of the uniformized ground model. Needs C-07, C-08 and C-09 first.
  - Rigorous route: choose the reference when the route opens (finest feasible Δ, or simulation), since the ground optimum is not computable for uniform durations. Needs C-24 and C-25.
  - Fix β/γ for the bound against the undiscounted H = 200 evaluation (D-007).
  - Done when: for each active route, a grid with empirical loss ± CI and bound per point is in JSON.
  - Note: Table 1 of Dijkman et al. also uses "K" for its 5 × 30 runs. Use a different symbol for repetitions.
- [ ] **C-22 · RQ3: derived φ vs the paper's s̃, reproducing Table 1.**
  - First reproduce Table 1 in simpn: H = 200, 5 × 30 episodes, Q-learning and EVI on s̃, FIFO, SPT and Random. Target values: 85.7 [81.6, 89.7], 85.7, 86.8, 86.7, 96.5. Record seeds and CI method.
  - Then run the same learners on the derived φ. With uniform durations, Level 1 is infinite, so use the Level 2 φ (bins) or the PH or exponential variant. Decide and record which one.
  - Done when: the reproduction is within the reported CI and the comparison JSONs exist. Links: H-001.
- [ ] **C-23 · Results pipeline.** Move the computed numbers (state counts, d_TV, vacuity) from the brief into experiments/results/*.json so the paper can use `\res…` macros.

## G. Rigorous route (gated by B-003; start after C-01–C-05)
- [ ] **C-24 · AIS audit G2: time horizon.** Is there a bound with a random, policy-dependent number of epochs N_H, including zero-length epochs? This is the most likely point of failure. Links: H-004, gap G2.
- [ ] **C-25 · AIS audit G4: Lipschitz constant.** Is the constant finite and computable for the flow-time reward under queue truncation K? Done when: the audit verdict is "corollary" (joins this paper) or "new theorem" (separate paper), and B-003 is moved.

## H. Pending decisions
- [ ] **C-26 · Phase-type deployment caveat.** Phases are unobservable, so decide whether safe-route guarantees are claimed on the model only, or whether a belief-over-phases (POMDP) treatment is needed. Exponential durations have no such caveat. Done when: a D-id is added.
- [ ] **C-27 · Venue, timeline, compute budget.** Not yet stated in RESEARCH_BRIEF.md or CLAUDE.md.
- [x] **C-28 · Fig. 1 chair semantics: paper or simpn?** The paper's Fig. 1 binds the chair (guard `chair == patient.chair`). simpn releases it and lets Observation take any idle chair. The options give different R2 states: pooled (idle count exact), guard + release (reserved-chair counts), guard + hold (idle count exact, needs a simpn builder change). Decide which model the Fig. 1 results are on, and whether to report the gap to the BPMN+OPT authors with C-16. Done when: a D-id is added and R2's Fig. 1 check names the chosen semantics. Links: H-002, D-007. (2026-11-06, evidence: D-009 — simpn pooled; R2 Fig. 1 check updated; reporting to authors optional, with C-16.)
- [x] **C-29 · Queue cap K = 5 is ours, not the model's.** simpn's Fig. 2 has unbounded queues, so 324 (and 144, 18,468, 503,424) count states of a model truncated at K = 5. Decide whether C-01 states exactness on the truncated model (with R7 as the only approximation) or on the unbounded model (countable state space, with 324 as a truncated view). Done when: the C-01 statement fixes this and the RQ1 state-count JSONs record K. Links: C-01, C-20, R7. (2026-11-06, evidence: D-010 — unbounded model, 324 as a corollary at K = 5.)
