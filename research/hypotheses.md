# HYPOTHESES
<!-- Testable statements. Status: open | testing | supported | refuted | inconclusive | dropped.
Refuted/dropped → also add a Discarded row in backlog.md.
Format:
### H-### · title
Added · Statement · Test (experiment + metric) · Supported if · Refuted if · Status · Evidence (results file, wiki exp:/claim:) · Links -->

### H-001 · The paper's abstraction loses value against the exact Level-1 abstraction
- Added: 2026-11-06
- Statement: on Fig. 2 with exponential durations (queue cap 5), the policy from the 324-state exact abstraction (oncologist status in {idle, P1, P2}) has strictly better flow time than the optimal policy on the paper's 144-state (n_P1, n_P2, I).
- Test: solve both (value iteration after uniformization), evaluate in simpn on undiscounted H = 200; mean flow time with CIs over seeds.
- Supported if: the exact-abstraction policy is better with non-overlapping CIs.
- Refuted if: no difference, which would make the paper's abstraction value-preserving here although not model-exact.
- Status: open (the state counts 324 vs 144 are computed; the value gap is untested)
- Evidence: —
- Links: D-003, X-003; RQ1, RQ3

### H-002 · Chairs are held between infusion and observation in simpn
- Added: 2026-11-06
- Statement: in simpn (branch bpmnopt), a patient's chair is not released between infusion and observation, so R2's idle-chair count is exact on Fig. 1.
- Test: read whether infusion returns the chair token on completion, or trace for a chair taken by another patient between one patient's infusion and observation.
- Supported if: held.
- Refuted if: released, in which case R2 needs a reserved-chair count.
- Status: refuted (2026-11-06) as stated. The chair is released when infusion ends. The intended consequence does not follow, though: simpn's Observation has no chair guard, so chairs are a pooled resource and the idle-chair count is still exact for simpn's model. A reserved-chair count is needed only under the paper's guard `chair == patient.chair` combined with release. Chosen semantics: simpn pooled (D-009).
- Evidence: simpn bpmnopt @8776bf0. `simpn/prototypes.py:412`: the BPMNTask complete event puts the resource token back in its lane. `er_paper/models/fig1_problem.json`: Observation (uncontrolled) has no `resource_constraint`. `bind_chair` writes `chair_id`, which nothing reads. Trace: experiments/results/c15_chair_trace_fig1.json, 30 FIFO episodes, 2,095 patients: 0 observed in their infusion chair, 0 waits, 0 chairs taken in between.
- Links: D-003; research/abstraction_rules.md R2; C-15, C-28

### H-003 · Abel bound is non-vacuous for R6/R7 on the safe-route model
- Added: 2026-11-06
- Statement: on the uniformized (exponential/PH) Fig. 2 model, the Abel Lemma 2 bound for R6 and R7 merges is below 1/(1−γ) for practically relevant γ.
- Test: compute ε_R, ε_T and |S_A| for R6/R7 merges and evaluate 2ε_R/(1−γ)² + 2γ|S_A|ε_T/(1−γ)³.
- Supported if: bound < 1/(1−γ) (and ideally informative).
- Refuted if: vacuous, as with R5 (X-004).
- Status: open
- Evidence: —
- Links: D-004; RQ2

### H-004 · AIS gives the time-horizon guarantee as a corollary
- Added: 2026-11-06
- Statement: the AIS bounds (Subramanian et al. 2022) extend to a time horizon with random, policy-dependent N_H (G2) and a finite, computable Lipschitz constant (G4) without a new theorem.
- Test: AIS audit protocol (1–2 weeks), run after Level 1 is formalized.
- Supported if: G2 and G4 pass. It then joins this paper as the Level 2 rigorous-route guarantee.
- Refuted if: a new theorem is needed, in which case it becomes a separate paper.
- Status: open (gated; see B-003)
- Evidence: —
- Links: B-003, D-006

### H-005 · Phase-type fitting error is small at moderate phase counts
- Added: 2026-11-06
- Statement: replacing Fig. 2's uniform durations with Erlang fits using far fewer phases than the moment-matched k = 27–108 changes the simulated H = 200 flow time only slightly, while keeping the state far below 503,424.
- Test: sweep k per duration and compare simulated flow time (original uniform model vs PH-model policy) in simpn.
- Supported if: some k gives a small flow-time gap at a tractable state count.
- Refuted if: the gap stays large until the state is intractable.
- Status: open
- Evidence: —
- Links: D-004

### H-006 · Pharmacy load is irrelevant at the infusion gateway
- Added: 2026-11-06
- Statement: on Fig. 1, ground states that differ only in busy pharmacists (2 vs 4 of 6) have Q̂ within 1 per action at the infusion gateway.
- Test: Level 3 validation. Sample merged states visited under FIFO, compute Monte Carlo Q̂ per action, and the spread ε̂ with a CI.
- Supported if: the ε̂ CI upper bound ≤ 1.
- Refuted if: > 1, in which case pharmacy load is added back to the grouping.
- Status: open
- Evidence: —
- Links: D-005, B-005
