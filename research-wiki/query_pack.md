# Research Wiki Query Pack

_Auto-generated. Do not edit._

## Project Direction
**Problem**

BPMN+OPT (paper:dijkman2026_bpmnopt_conceptual_modeling) adds an optimization layer to BPMN: case/resource attributes, stochastic durations, decision moments, decision variables, constraints and objectives. Its execution semantics is an SMDP whose state holds queues, resources, case attributes and the event calendar Q_t. The paper solves its Figure 2 fragment (P1/P2 patients, ~exp(10) arrivals, two oncologists with uniform durations) with the hand-made abstraction (n_P1, n_P2, I), where I is the set of idle oncologists, and never states what that abstraction preserves.

We derive abstractions from the model's annotations and attach a guarantee to each. Li, Walsh & Littman (2006) give the ladder of exact abstraction types, and Abel, Hershkowitz & Littman (2016) give ε-relaxations with loss bounds. Both assume someone supplies the abstraction φ. Our contribution is the derivation: syntactic rules over BPMN+OPT annotations that decide the level of an abstraction and, where possible, compute its ε from the model.

**Constraints**

- **Compute**: tabular methods on small fragments; simulation via simpn (github.com/bpogroup/simpn, branch bpmnopt). Budget not yet stated.
- **Timeline / venue**: not yet stated.
- Rules must act on observable (elapsed) time. Residual event times are latent in BPMN+OPT (Def. 2).

**Background**

- **Field**: RL / MDP theory applied to business process management (BPM).
- **Sub-area**: state abstraction for SMDPs; model-derived abstractions.
- **Key papers**: Dijkman et al. (BPMN+OPT); Li et al. 2006; Abel et al. 2016; Subramanian et al. 2022 (AIS); Puterman 1994 Ch. 11 (uniformization); Ravindran & Barto 2003; Buchholz et al. 2017 (CTMDP aggregation with phase-type sojourns).
- **What was already done**: the proposal (2026-10-24) and a validation pass. Only Abel 2016 was re-read against the source; verify theorem numbers of the other references before citing them.
- **What didn't work**: Abel Lemma 2 with time binning (R5) on Figure 2. With Δ = 0.5 and K = 5, |S_A| = 18,468 and |S_A|·ε_T ≈ 923, so the bound exceeds 1/(1−γ) for every γ. Finer bins make it worse, because ε_T falls like Δ while |S_A| grows like 1/Δ².

**Non-goals**

- Level 4 (φ_π*) as a target.
- Claiming the continuous-time discounting or discrete-step finite-horizon bounds as novel; both already exist.
- An LLM proposer as a core method (optional, non-reproducible experiment only).

**Domain Knowledge**

- R1 doubles as a model-validation check: `measurements` is never read, so either routing ignores clinical state on purpose or a constraint is missing.
- Phase-type phases are unobservable. The PH guarantee holds on the model, and deployment needs a belief over phases. Exponential durations do not have this caveat.
- The SMDP-to-MDP effective discount E[e^(−βτ)] is a known corollary (Schweitzer 1971; Puterman Ch. 11), not a contribution.
## Open Gaps
# Gap Map

_Field gaps with stable IDs._

- **G1** (open): Process-model SMDPs (BPMN+OPT) are solved with hand-made state abstractions whose guarantees are never stated. Li 2006 / Abel 2016 assume phi is given; nobody derives phi and its guarantee from model annotations. Targeted by idea:language_derived_abstraction_levels.
- **G2** (open): State-abstraction bounds for an SMDP over a time horizon with a random, policy-dependent number of decision epochs N_H (incl. zero-length epochs). Discrete-step finite-horizon bounds exist (AIS; quadratic in horizon) but not this setting. Gated by the AIS audit (backlog B-003).
- **G3** (open): Approximate-abstraction loss bounds that stay non-vacuous under time discretization. Abel 2016 Lemma 2 scales with |S_A| and is vacuous on BPMN+OPT Fig. 2; AIS-style distribution distances may remove the factor.

## Key Papers (11 total)
- [paper:abel2016_near_optimal_behavior] Near Optimal Behavior via Approximate State Abstraction: Relaxes exact abstraction types (model, Q*, a*, Boltzmann) to epsilon-approximate versions and bounds the value loss of the lifted abstract policy (Le
- [paper:abel2020_value_preserving_stateaction] Value Preserving State-Action Abstractions: Identifies state-abstraction plus option pairings that keep near-optimal policies representable, extending approximate abstractions to semi-Markov opt
- [paper:bertsekas2012_dynamic_programming_optimal] Dynamic Programming and Optimal Control, Vol. II: Approximate Dynamic Programming: Reference text; its aggregation chapter bounds the error of aggregated DP by the within-aggregate value spread, ||J*-J~|| <= eps/(1-alpha).
- [paper:buchholz2017_bounded_aggregation_continuous] Bounded Aggregation for Continuous Time Markov Decision Processes: Partitions the state space of a CTMDP (discounted or average reward) into blocks, models the sojourn time in each block with a phase-type distribution
- [paper:dijkman2026_bpmnopt_conceptual_modeling] BPMN+OPT: A Conceptual Modeling Language for Business Process Optimization: BPMN+OPT adds an optimization annotation layer (state, stochasticity, decision moments/variables, constraints, objectives) to unchanged BPMN models an
- [paper:li2006_towards_unified_theory] Towards a Unified Theory of State Abstraction for MDPs: Orders exact state abstractions from finest to coarsest (model-irrelevance, Q^pi, Q*, a*, pi*) and shows which preserve the optimal policy and Q-learn
- [paper:ni2023_learning_good_state] Learning Good State and Action Representations via Tensor Decomposition: Learns low-dimensional state and action representations (and discrete abstractions) from trajectories via kernelized low-Tucker
## Recent Relationships (17 total)
  idea:language_derived_abstraction_levels --inspired_by--> paper:dijkman2026_bpmnopt_conceptual_modeling
  idea:language_derived_abstraction_levels --inspired_by--> paper:li2006_towards_unified_theory
  idea:language_derived_abstraction_levels --inspired_by--> paper:abel2016_near_optimal_behavior
  idea:language_derived_abstraction_levels --addresses_gap--> gap:G1
  idea:language_derived_abstraction_levels --addresses_gap--> gap:G2
  idea:language_derived_abstraction_levels --addresses_gap--> gap:G3
  claim:paper_abstraction_not_exact --addresses_gap--> gap:G1
  claim:paper_abstraction_not_exact --uses--> paper:dijkman2026_bpmnopt_conceptual_modeling
  claim:paper_abstraction_not_exact --uses--> paper:li2006_towards_unified_theory
  claim:abel_lemma2_vacuous_time_bins --addresses_gap--> gap:G3
  claim:abel_lemma2_vacuous_time_bins --uses--> paper:abel2016_near_optimal_behavior
  claim:a
