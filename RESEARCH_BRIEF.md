# Research Brief: Language-Derived State Abstraction for BPMN+OPT

> Source: literature/notes_2026-11-05_state_abstraction_context.pdf (merges the proposal "Language-Derived State Abstraction Levels for BPMN+OPT", 2026-10-24, with a later validation against the primary literature). Rule catalog: research/abstraction_rules.md. Keep this brief under ~6k chars (it feeds query_pack.md).

## Problem Statement
BPMN+OPT (paper:dijkman2026_bpmnopt_conceptual_modeling) adds an optimization layer to BPMN: case/resource attributes, stochastic durations, decision moments, decision variables, constraints and objectives. Its execution semantics is an SMDP whose state holds queues, resources, case attributes and the event calendar Q_t. The paper solves its Figure 2 fragment (P1/P2 patients, ~exp(10) arrivals, two oncologists with uniform durations) with the hand-made abstraction (n_P1, n_P2, I), where I is the set of idle oncologists, and never states what that abstraction preserves.

We derive abstractions from the model's annotations and attach a guarantee to each. Li, Walsh & Littman (2006) give the ladder of exact abstraction types, and Abel, Hershkowitz & Littman (2016) give ε-relaxations with loss bounds. Both assume someone supplies the abstraction φ. Our contribution is the derivation: syntactic rules over BPMN+OPT annotations that decide the level of an abstraction and, where possible, compute its ε from the model.

## Abstraction levels (Li's hierarchy φ_model ⪰ φ_Q^π ⪰ φ_Q* ⪰ φ_a* ⪰ φ_π*)
| Level | Type | From syntax | Guarantee | Status |
|---|---|---|---|---|
| 1 | φ_model exact (R1–R4, R3b) | fully | zero loss | Validated; ready to formalize |
| 2 | φ_model,ε (R5–R7) | partially (user picks Δ, δ, K) | computed bound | Corrected: Abel bound is vacuous with time bins; safe route now |
| 3 | φ_Q*,ε, φ_a* (propose, then validate) | no, needs Q* | estimated a posteriori | Validated as a secondary contribution |
| 4 | φ_π* | no | none | Out of scope; FIFO/SPT serve as baselines |

## Two routes for Level 2
- **Safe route (current):** exponential or phase-type durations. The phase index replaces elapsed time (R3b), and the ground process is a finite CTMDP. After uniformization, Li and Abel apply directly. Bounds certify a discounted proxy; validate on the undiscounted H = 200 objective in simpn.
- **Rigorous route (parked, gated by the AIS audit):** general durations with abstracted elapsed time. Needs an AIS bound (Subramanian et al. 2022) extended to a time horizon with a random, policy-dependent number of epochs N_H (G2), plus a finite Lipschitz constant (G4).

## Background
- **Field**: RL / MDP theory applied to business process management (BPM).
- **Sub-area**: state abstraction for SMDPs; model-derived abstractions.
- **Key papers**: Dijkman et al. (BPMN+OPT); Li et al. 2006; Abel et al. 2016; Subramanian et al. 2022 (AIS); Puterman 1994 Ch. 11 (uniformization); Ravindran & Barto 2003; Buchholz et al. 2017 (CTMDP aggregation with phase-type sojourns).
- **What was already done**: the proposal (2026-10-24) and a validation pass. Only Abel 2016 was re-read against the source; verify theorem numbers of the other references before citing them.
- **What didn't work**: Abel Lemma 2 with time binning (R5) on Figure 2. With Δ = 0.5 and K = 5, |S_A| = 18,468 and |S_A|·ε_T ≈ 923, so the bound exceeds 1/(1−γ) for every γ. Finer bins make it worse, because ε_T falls like Δ while |S_A| grows like 1/Δ².

## Existing Results (computed, not yet in experiments/results/)
- The paper's (n_P1, n_P2, I) is not exact even with exponential durations, because completion rates depend on the patient type in service. The exact Level-1 state needs each oncologist's status in {idle, P1, P2}: 324 states (queue cap 5) vs 144 for the paper's abstraction.
- State counts on Figure 2 (queue cap 5): exponential exact 324; elapsed time binned (Δ = 0.5) 18,468; moment-matched Erlang (k = 27, 48, 75, 108) exact 503,424.
- Abel bound split: loss ≤ 2ε_R/(1−γ)² + 2γ|S_A|ε_T/(1−γ)³. Example: ε_T ≤ Δ/10 against exp(10) arrivals; gap 0.035 at Δ = 0.5. d_TV(U(2,4), U(3,5)) = 0.5, so P1/P2 stay separate on φ₁.

## Constraints
- **Compute**: tabular methods on small fragments; simulation via simpn (github.com/bpogroup/simpn, branch bpmnopt). Budget not yet stated.
- **Timeline / venue**: not yet stated.
- Rules must act on observable (elapsed) time. Residual event times are latent in BPMN+OPT (Def. 2).

## Domain Knowledge
- R1 doubles as a model-validation check: `measurements` is never read, so either routing ignores clinical state on purpose or a constraint is missing.
- Phase-type phases are unobservable. The PH guarantee holds on the model, and deployment needs a belief over phases. Exponential durations do not have this caveat.
- The SMDP-to-MDP effective discount E[e^(−βτ)] is a known corollary (Schweitzer 1971; Puterman Ch. 11), not a contribution.

## Non-Goals
- Level 4 (φ_π*) as a target.
- Claiming the continuous-time discounting or discrete-step finite-horizon bounds as novel; both already exist.
- An LLM proposer as a core method (optional, non-reproducible experiment only).

## Research Questions
- **RQ1 (state-space size):** count states at Level 0 (ground), Level 1 and Level 2. Hypotheses: H-001 (324 vs 144). Checks: research/checklist.md C-20.
- **RQ2 (bound vs empirical loss):** on Fig. 2, compare the empirical loss with the theoretical bound as the discretization parameter and K (queue cap) vary. The discretization parameter follows the route (D-008): δ (R6) with the Abel bound on the safe route (active), Δ (R5) with the AIS bound on the rigorous route (if B-003 is revived). Hypotheses: H-003. Checks: C-21.
- **RQ3 (derived vs hand-made abstraction):** compare the derived φ with the paper's s̃ = (n_P1, n_P2, I), reproducing the paper's Table 1 (H = 200, 5 × 30 episodes: Q-learning 85.7 [81.6, 89.7], EVI 85.7, FIFO 86.8, SPT 86.7, Random 96.5). Hypotheses: H-001. Checks: C-22.

## Research phases
1. Level 1 exact rules R1–R4 plus R3b, formalized on Figures 1 and 2.
2. SMDP lifting and Level 2 ε-bounds for R6–R7 via the safe route; AIS audit in parallel.
3. Abstraction pass in the JSON-to-SMDP pipeline; test RQ1–RQ3.
4. Level 3 proposer and write-up; optional LLM-proposer comparison.
