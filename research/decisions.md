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

### D-002 · Research direction: language-derived state abstraction levels for BPMN+OPT
- Date: 2026-11-06 (proposal 2026-10-24; validation before 2026-11-05)
- Context: BPMN+OPT compiles a process model into an SMDP but solves its Fig. 2 example with the hand-made abstraction (n_P1, n_P2, I) and states no guarantee. Li et al. 2006 give the ladder of exact abstraction types; Abel et al. 2016 give ε-relaxations with loss bounds. Both assume φ is given.
- Decision: derive φ from the model's annotations with syntactic rules and attach a guarantee per level: L1 φ_model (exact, fully syntactic, zero loss); L2 φ_model,ε (partly syntactic, user picks Δ, δ, K; computed bound); L3 φ_Q*,ε / φ_a* (proposed, then validated a posteriori); L4 φ_π* out of scope.
- Alternatives: hand-made abstractions (status quo); learned abstractions without guarantees.
- Consequences: rule catalog in research/abstraction_rules.md; four research phases in RESEARCH_BRIEF.md.
- Links: paper:dijkman2026_bpmnopt_conceptual_modeling, paper:li2006_towards_unified_theory, paper:abel2016_near_optimal_behavior; literature/notes_2026-11-05_state_abstraction_context.pdf

### D-003 · Level 1 exact rules R1–R4 + R3b on observable time
- Date: 2026-11-06
- Context: validation confirmed that L1 is zero-loss, horizon-independent (covers γ = 1, H = 200) and SMDP-exact (joint law of next abstract state, τ and reward preserved). It also found that BPMN+OPT (Def. 2) treats sampled, unrevealed event times as latent.
- Decision: keep R1 relevance slicing, R2 exchangeability, R3 memoryless durations and R4 reward as a rate. R3 acts on elapsed time. Add R3b: the phase-type phase index replaces elapsed time (R3 is the single-phase case).
- Alternatives: R3 on residual time (X-008).
- Consequences: with uniform durations the exact state is infinite, so it needs L2 discretization (rigorous route) or Markovian durations (safe route). Pending checks: chair release semantics for R2 (H-002) and the `measurements` attribute that R1 drops (confirm intent with the BPMN+OPT authors).
- Links: research/abstraction_rules.md; X-003, X-008

### D-004 · Level 2 follows the safe route (Markovian durations)
- Date: 2026-11-06
- Context: Abel 2016 Lemma 2 has an |S| factor. On Fig. 2 with Δ = 0.5 and K = 5, |S_A| = 18,468 and |S_A|·ε_T ≈ 923, which exceeds 1/(1−γ) for every γ, and finer bins make it worse. With exponential or phase-type durations the ground process is a finite CTMDP.
- Decision: annotate durations as exponential/PH, uniformize (Puterman Ch. 11, per-step discount Λ/(Λ+β)), and apply Li/Abel directly. Use Abel's bound only for R6/R7 merges and check that it is non-vacuous numerically. R5 (time bins) belongs only to the rigorous route.
- Alternatives: rigorous route with AIS (parked, B-003); Abel + time bins (discarded, X-004).
- Consequences: state cost on Fig. 2 (queue cap 5): exponential exact 324; moment-matched Erlang exact 503,424. PH fitting error must be measured in simpn. Phases are unobservable, so decide whether guarantees are claimed on the model only. Bounds are stated in continuous-time units.
- Links: paper:puterman1994_markov_decision_processes, paper:buchholz2017_bounded_aggregation_continuous, paper:subramanian2022_approximate_information_state

### D-005 · Level 3 as a secondary, propose-then-validate contribution
- Date: 2026-11-06
- Context: Q* abstractions need Q*, which no annotation provides. Lemma 1 (2ε/(1−γ)²) is confirmed, and both Lemma 1 and the Bertsekas aggregation bound diverge at γ = 1 (roughly N²ε̂ over N epochs).
- Decision: the proposer is static analysis (control-flow reachability downstream of the decision point plus the read/write sets of the reached elements). Validate with Monte Carlo Q̂ on states visited under FIFO, compute the spread ε̂ with a CI, and accept or add features back.
- Alternatives: LLM proposer (parked, B-004); AIS for L3 (discarded, X-009).
- Consequences: the guarantee is only estimated a posteriori. Implemented after Level 2 (phase 4).
- Links: paper:abel2016_near_optimal_behavior, paper:bertsekas2012_dynamic_programming_optimal; H-006, B-005

### D-006 · Narrow the novelty claim
- Date: 2026-11-06
- Context: the SMDP-to-MDP effective discount E[e^(−βτ)] is a known corollary (Schweitzer 1971; Puterman Ch. 11), and Abel et al. 2020 already extend abstractions to semi-Markov options. Discrete-step finite-horizon bounds already exist (quadratic in the horizon). Identity-bound actions are handled by SMDP homomorphisms (Ravindran & Barto 2003).
- Decision: claim (a) abstractions and bounds derived from annotations, and (b) the time-horizon setting with a random, policy-dependent number of epochs N_H, including zero-length epochs from same-time sequential decisions.
- Alternatives: claiming the finite-horizon bound (X-006) or continuous-time discounting (X-007) as contributions.
- Consequences: the related-work section must cite these as known. Only Abel 2016 was re-read; verify the theorem numbers of the other references before citing them. Ni et al. 2023 (JMLR 24) was checked through alphaxiv on 2026-11-06. Its Theorem 8 bounds the H-step policy-evaluation error of a learned abstraction by O(H²), which supports the citation.
- Links: paper:schweitzer1971_iterative_solution_functional, paper:abel2020_value_preserving_stateaction, paper:ni2023_learning_good_state, paper:ravindran2003_smdp_homomorphisms_algebraic

### D-007 · Evaluate on the undiscounted H = 200 objective
- Date: 2026-11-06
- Context: Li and Abel bounds are for discounted MDPs, while BPMN+OPT uses γ = 1 and H = 200 (cumulative flow time).
- Decision: treat discounted bounds as certificates for a discounted flow-time proxy. Every abstraction is also evaluated by simulation in simpn on the original undiscounted H = 200 objective, against FIFO/SPT baselines.
- Alternatives: report discounted values only.
- Consequences: Level 1 is unaffected because it is exact. Experiments report both the proxy bound and the simulated undiscounted objective.
- Links: paper:dijkman2026_bpmnopt_conceptual_modeling

### D-008 · RQ2's discretization axis depends on the Level 2 route
- Date: 2026-11-06
- Context: RQ2 asks how empirical loss compares with the theoretical bound as Δ and K vary. Time bins Δ (R5) exist only in the rigorous route (D-004). On that route the Abel bound is vacuous (X-004), so the bound there has to be the AIS time-horizon bound (B-003). The safe route has no Δ; its approximate merges are δ-close ptimes (R6) and the queue cap K (R7).
- Decision (user, 2026-11-06): RQ2 is defined per route.
  - Safe route (active, D-004): grid over (δ, K). Bound = Abel Lemma 2 on the uniformized model (C-08). The empirical-loss reference is the exact optimum of the uniformized ground model, which is finite and computable.
  - Rigorous route (only if B-003 is revived after the AIS audit, C-24/C-25): grid over (Δ, K). Bound = AIS time-horizon bound. The reference is not computable exactly for uniform durations; choose one then (finest feasible Δ, or simulation).
- Alternatives: a single Δ axis on every route (Δ is undefined on the safe route); a Δ axis used only to show Abel's vacuity (still possible as a side remark, not the RQ2 result).
- Consequences: C-21 now waits on C-07 (zero-length epochs), C-08 and C-09 (ε for R7) for the safe-route grid. The rigorous-route grid waits on the AIS audit. RESEARCH_BRIEF.md RQ2 updated.
- Links: D-004, X-004, B-003, H-003; research/checklist.md C-21

### D-009 · Fig. 1 chair semantics follow simpn (pooled chairs)
- Date: 2026-11-06
- Context: the paper's Fig. 1 binds a patient's chair from infusion to observation (guard `chair == patient.chair`). simpn bpmnopt @8776bf0 does not implement this guard. BPMNTask returns the chair to `idle_chair` at infusion end (`simpn/prototypes.py:412`). Observation has no `resource_constraint`, so it takes any idle chair, and `bind_chair` writes a `chair_id` that nothing reads. FIFO trace: 0/2,095 patients observed in their infusion chair, 0 waits, 0 chairs taken in between (C-15, X-010).
- Decision (user, 2026-11-06): Fig. 1 is modelled and evaluated with simpn's pooled-chair semantics as implemented. simpn is not patched.
- Alternatives:
  - paper guard + hold: the idle count is exact, but the simpn builder would need a change so the chair stays busy through observation;
  - paper guard + release: R2 needs reserved-chair counts. The builder supports the guard, but infusion assignment ignores reservations.
- Consequences:
  - R2 on Fig. 1 is a plain idle-chair count with zero loss, so no reserved-chair state is needed.
  - Results on Fig. 1 are for simpn's model, so the paper must state that this deviates from the paper's Fig. 1 guard.
  - Pooling and hold differ only if every chair is taken at the instant infusion ends. That never happened under FIFO, but it can under other policies or heavier load.
  - Reporting the deviation to the BPMN+OPT authors is optional and can go with the C-16 question.
- Links: H-002, X-010, D-003, D-007; research/abstraction_rules.md R2; research/checklist.md C-15, C-28

### D-010 · C-01 is stated on unbounded queues, with a corollary at K = 5
- Date: 2026-11-06
- Context: simpn's Fig. 2 has no queue cap (C-14). The state counts 324 / 144 / 18,468 / 503,424 all assume each queue is truncated at K = 5 (C-29).
- Decision (user, 2026-11-06): the Level 1 exactness theorem (C-01) is stated on the unbounded-queue model, which has a countable state space, as simpn implements it. The 324-state count, and 144 for the paper's (n_P1, n_P2, I), are a corollary for the model truncated at K = 5 per queue.
- Alternatives: state everything on the truncated model. That is simpler and finite, but it proves exactness for a model that blocks arrivals, which is not simpn's model.
- Consequences:
  - Truncation stays an R7 approximation (Level 2) and is not part of Level 1.
  - Value iteration and H-001 run on the truncated model, so they must report K.
  - The RQ1 state-count JSONs (C-20) record K.
- Links: C-01, C-20, C-29, R7, H-001, D-003

### D-011 · Level 1 proofs use generic exponential rates
- Date: 2026-11-06
- Context: the 324-state Level 1 model needs exponential durations, while simpn's Fig. 2 uses uniform ones.
- Decision (user, 2026-11-06): proofs use symbolic parameters: arrival rate λ > 0, P(P1) = p ∈ (0,1), and service rates μ(o, type) > 0 depending only on (oncologist, patient type). The numeric instance for experiments matches the uniform means:
  - φ₁ × P1 = 3, φ₁ × P2 = 4;
  - φ₂ × P1 = 5, φ₂ × P2 = 6;
  - arrivals mean 10, p = 0.5.
- Alternatives: prove only for the numeric instance. That is no simpler and less general.
- Consequences:
  - The theorem claims exactness, not minimality. For degenerate rates, e.g. μ(φ₁, ·) = μ(φ₂, ·), the oncologists become exchangeable and could be merged further; the proof names this case.
  - Experiments (H-001, C-20, C-22) use the numeric instance.
- Links: C-01, D-003, D-004, H-001; research/abstraction_rules.md "Model parameters"
