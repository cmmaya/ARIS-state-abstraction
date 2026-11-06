# ABSTRACTION RULES
<!-- Catalog of syntactic abstraction rules over BPMN+OPT annotations. One block per rule in the template below.
Status labels: Validated | Corroborated | Corrected | Open | Check (meanings in RESEARCH_BRIEF.md source doc).
Route: safe = exponential/phase-type durations (Li/Abel after uniformization); rigorous = general durations (AIS, parked B-003).
Figures refer to Dijkman et al. (paper:dijkman2026_bpmnopt_conceptual_modeling): Fig. 1 = chemotherapy clinic, Fig. 2 = oncologist fragment.
Source: literature/notes_2026-11-05_state_abstraction_context.pdf. -->

## Template
```
### R<n>: <name>
- Level: 1 (exact) | 2 (approximate) | 3 (proposal)
- Route: safe | rigorous | both
- Status: <label>
- Syntactic precondition: <which annotations must hold>
- Abstraction φ: <what is dropped, counted, binned or merged>
- Parameters: none | Δ, δ, K
- ε_R: <formula from Obj, or 0>
- ε_T: <formula from the annotated distributions, or 0>
- Guarantee: zero loss | computed bound | estimated a posteriori
- Check on Fig. 2: <result>
- Check on Fig. 1: <result>
- Open questions: <...>
```

## Model parameters (simpn bpmnopt @8776bf0, er_paper/models/)
Fig. 2 (`fig2_problem.json`, `final_model_fig2.md`; C-14, checked 2026-11-06):
- Arrivals: exp with mean 10 (`expovariate(1/10)`), one Patient per arrival, type = `random.choice({P1, P2})`, so P(P1) = P(P2) = 0.5.
- Resources: φ₁ (`phi1`), φ₂ (`phi2`). Examination ptime: φ₁ × P1 = U(2,4), φ₁ × P2 = U(3,5), φ₂ × P1 = U(4,6), φ₂ × P2 = U(5,7). This confirms the inferred φ₂ values.
- Lifecycle: patient and oncologist are both busy during ptime, then the oncologist returns to `idle_oncologist`. Examination has no behavior.
- Decisions: sequential, one (patient, oncologist) pair per epoch. Mom = an unassigned waiting patient and an unassigned idle oncologist both exist. Con = at most one per patient and per oncologist. Same-time epochs return reward 0 (`smdp_env.step`, `same_time=True`), so zero-length epochs exist in the simulator (C-07).
- No queue cap in the model. K = 5 in our state counts is our truncation (R7), not a model feature (C-29).
- Routing and tie-breaking are not in the model; they live in the policies. FIFO picks the longest-waiting patient, ties broken by the lower resource id (`solvers.assign_fifo`). SPT picks the pair with the shortest expected ptime.
- Objective: minimize total cycle time over H = 200 with discount 1.0. The env pays `n_in_system × dt` per step.
- Env abstraction level 0 = (type counts, number of idle oncologists) = the paper's s̃ (n_P1, n_P2, I). Level 1 = type counts plus idle oncologist ids.
- simpn's own `code/output/fig2_results.md` (100 eval episodes, avg cycle time): FIFO 82.88, SPT 82.73, Random 94.55, Q-learning 85.47, VI 85.48. These differ from the paper's Table 1 values used as targets in C-22.

Fig. 1 (`fig1_problem.json`): interarrival exp(mean 6). 2 lab staff (senior U(2,8), junior U(10,20)), 2 oncologists U(5,15), 6 pharmacists U(20,40), 20 chairs. Standard infusion U(25,35), intensive U(70,110), observation U(30,40), uncontrolled. Scheduling offsets {0, 5, 10, 15, 20}. Chair semantics: see R2.

## Level 1: exact (φ_model)
Level-wide findings: zero loss, and the optimal policy and tabular Q-learning convergence are preserved (Li et al. 2006). Abel et al. (2016) bounds are exactly 0 at ε = 0. Horizon-independent (exact bisimulation), so γ = 1, H = 200 is covered — Corroborated. SMDP exactness needs the joint law of (next abstract state, τ, reward) preserved; R1–R4 do this — Corroborated.

### R1: relevance slicing
- Level: 1 · Route: both · Status: Validated
- Syntactic precondition: attribute is read by no condition, ptime, Con, Mom or Obj, directly or through a behavior that writes something read.
- Abstraction φ: drop the attribute.
- Parameters: none · ε_R: 0 · ε_T: 0 · Guarantee: zero loss
- Check on Fig. 2: —
- Check on Fig. 1: `complications` is written but never read, so it is dropped. `measurements` is never read either (Check).
- Open questions: is ignoring `measurements` in routing intended, or is a constraint missing? Confirm with the BPMN+OPT authors. R1 doubles as a model-validation check.

### R2: exchangeability
- Level: 1 · Route: both · Status: Validated (chairs: pooled, D-009)
- Syntactic precondition: cases with identical relevant attributes; resources of the same type with identical cond and ptime.
- Abstraction φ: replace the objects by counts.
- Parameters: none · ε_R: 0 · ε_T: 0 · Guarantee: zero loss
- Check on Fig. 2: oncologists φ₁ and φ₂ differ in ptime, so they are not counted. The exact state needs each oncologist's status in {idle, P1, P2}: 324 states (queue cap 5). The paper's (n_P1, n_P2, I) has 144 states and is not exact even with exponential durations (Corrected).
- Check on Fig. 1: the paper's guard `chair == patient.chair` is not implemented in simpn (bpmnopt @8776bf0). Infusion returns the chair to `idle_chair` on completion. Observation has no `resource_constraint`, so it takes any idle chair. `bind_chair` writes `chair_id`, which nothing reads. Trace: 2,095 patients over 30 FIFO episodes, none observed in their infusion chair (experiments/results/c15_chair_trace_fig1.json). So, by semantics:
  - simpn as implemented: chairs are pooled, and the idle-chair count is exact.
  - paper guard + release: R2 needs reserved-chair counts.
  - paper guard + hold: the idle count is exact, but simpn would need a builder change.
  (H-002 refuted as stated.) **Chosen: simpn pooled (D-009).** The 20 chairs become an idle-chair count with zero loss. Results are on simpn's model, not on the paper's guard.
- Open questions: none for Fig. 1 chairs. Optionally report the missing guard to the BPMN+OPT authors with C-16.

### R3: memoryless durations
- Level: 1 · Route: safe · Status: Corrected
- Syntactic precondition: event/duration annotated as exponential.
- Abstraction φ: drop the elapsed time of the exponential event. It must act on elapsed time (observable), not residual time, because sampled but unrevealed event times are latent in BPMN+OPT (Def. 2).
- Parameters: none · ε_R: 0 · ε_T: 0 · Guarantee: zero loss
- Check on Fig. 2: exp(10) arrival timing dropped.
- Check on Fig. 1: arrival timing dropped. simpn's fig1_problem.json uses interarrival exp(mean 6), not exp(10). Check against the paper's Fig. 1.
- Open questions: none. R3 is the single-phase case of R3b.

### R3b: phase-type durations
- Level: 1 · Route: safe · Status: Added
- Syntactic precondition: duration annotated as phase-type (e.g. Erlang-k, CV = 1/√k).
- Abstraction φ: replace elapsed time with the PH phase index. The merge is exact on the model.
- Parameters: none (phase count k is a modeling choice) · ε_R: 0 · ε_T: 0 on the model · Guarantee: zero loss on the PH model
- Check on Fig. 2: moment-matched Erlang (k = 27, 48, 75, 108; k ≈ 1/CV²) gives 503,424 states (queue cap 5).
- Check on Fig. 1: not done.
- Open questions: fewer phases shrink the state but add fitting error (measure in simpn). Phases are unobservable, so deployment needs a belief over phases. Decide whether guarantees are claimed on the model only (Check).

### R4: reward as a rate
- Level: 1 · Route: both · Status: Validated
- Syntactic precondition: Obj is cumulative flow time.
- Abstraction φ: rewrite Obj as −∫ n(u) du, so c.start need not be stored.
- Parameters: none · ε_R: 0 · ε_T: 0 · Guarantee: zero loss
- Check on Fig. 2 / Fig. 1: applies to both (flow-time objective).
- Open questions: none.

## Level 2: approximate (φ_model,ε)
Merge condition (Abel et al. 2016): |R(s₁,a) − R(s₂,a)| ≤ ε_R and |Σ_{g′∈G(s̃′)} [T(s₁,a,g′) − T(s₂,a,g′)]| ≤ ε_T.
Bound (Abel 2016, Lemma 2, rewards in [0,1]; Validated): V^{π*_G}_G(s) − V^{π_GA}_G(s) ≤ (2ε + 2γε(|S_G|−1))/(1−γ)³. Split through the proof's intermediate step: loss ≤ 2ε_R/(1−γ)² + 2γ|S_A|ε_T/(1−γ)³.
Vacuity (Corrected): finite |S_A| is not enough. On Fig. 2 with Δ = 0.5, K = 5: |S_A| = 36 × 19 × 27 = 18,468 and |S_A|·ε_T ≈ 923 > 1/(1−γ) for every γ. Finer bins make it worse (ε_T ∝ Δ, |S_A| ∝ 1/Δ²). Cause: the proof bounds the sum of per-cluster errors by |S_A| × max error.

### R5: time discretization
- Level: 2 · Route: rigorous only · Status: Validated (rule); guarantee Corrected (vacuous via Abel)
- Syntactic precondition: non-memoryless durations or appointment slots.
- Abstraction φ: bin elapsed times and appointment slots with width Δ.
- Parameters: Δ · ε_R: 0 on Fig. 2 · ε_T: ≤ Δ/10 against exp(10) arrivals (P(finish first | r) = e^{−r/10})
- Guarantee: computed bound, but vacuous under Abel Lemma 2. Needs an AIS-style bound (B-003).
- Check on Fig. 2: Δ = 0.5, r = 1.0 vs 1.4 gives 0.905 vs 0.869, a gap of 0.035. With e < 2 on uniform(2,4), shifting e by Δ shifts the residual law by Δ, so the same bound holds.
- Check on Fig. 1: not done.
- Open questions: rigorous route only (AIS audit G2, G4).

### R6: near-identical resources or case types
- Level: 2 · Route: both · Status: Validated
- Syntactic precondition: objects whose ptime distributions are within δ (total variation or Wasserstein).
- Abstraction φ: merge them.
- Parameters: δ · ε_R: from Obj · ε_T: from the ptime distance · Guarantee: computed bound
- Check on Fig. 2: P1 vs P2 on φ₁, U(2,4) vs U(3,5): d_TV = 0.5 (Validated), so they are kept separate, as the paper does.
- Check on Fig. 1: not done.
- Open questions: compute the Abel bound on the uniformized safe-route model and check non-vacuity.

### R7: queue truncation
- Level: 2 · Route: both · Status: Validated
- Syntactic precondition: unbounded queue counts.
- Abstraction φ: cap queue counts at K.
- Parameters: K · ε_R, ε_T: from the arrival/service annotations (to derive) · Guarantee: computed bound
- Check on Fig. 2: K = 5 used in all state counts.
- Check on Fig. 1: not done.
- Open questions: compute the Abel bound on the uniformized safe-route model and check non-vacuity. K also keeps the flow-time reward bounded (needed for AIS G4).

## Level 3: value-based (φ_Q*,ε, φ_a*): propose, then validate
Merge condition |Q*(s₁,a) − Q*(s₂,a)| ≤ ε ∀a. Cannot be certified from syntax, because no annotation provides Q* (Validated). Bounds: loss ≤ 2ε̂/(1−γ)² (Abel 2016, Lemma 1; Validated) and ‖J* − J̃‖∞ ≤ ε̂/(1−α) (Bertsekas 2012). Both diverge at γ = 1: N decision epochs give roughly N²ε̂ growth (Corroborated). AIS does not help here, because AIS bounds model-based abstractions.
1. Propose φ by static analysis: control-flow reachability downstream of the decision point plus read/write sets of the reached elements (R1 applied locally). LLM proposer optional (B-004).
2. Validate: sample merged ground states visited under a baseline (FIFO), estimate Q̂ per action by Monte Carlo, compute the spread ε̂ with a CI.
3. Decide: accept if ε̂ is small; else add the ignored feature back and repeat.
- Fig. 1 example: at the infusion gateway, downstream elements read chairs, infusion and the chair guard, so the grouping ignores pharmacy load. Accept if busy pharmacists 2 vs 4 (of 6) give Q̂ within 1 (H-006).
- Open: upstream activity can matter indirectly. A stronger result would show that local reachability implies small ε, e.g. when downstream resources are never saturated (B-005).
