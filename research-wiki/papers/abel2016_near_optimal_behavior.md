---
type: paper
node_id: paper:abel2016_near_optimal_behavior
title: "Near Optimal Behavior via Approximate State Abstraction"
authors: ["David Abel", "D. Ellis Hershkowitz", "Michael L. Littman"]
year: 2016
venue: "ICML 2016"
external_ids:
  arxiv: "1701.04113"
  doi: null
  s2: null
tags: ["state-abstraction", "approximate-abstraction", "mdp", "bounds"]
added: 2026-11-06T16:32:38Z
---

# Near Optimal Behavior via Approximate State Abstraction

## One-line thesis
Relaxes exact abstraction types (model, Q*, a*, Boltzmann) to epsilon-approximate versions and bounds the value loss of the lifted abstract policy (Lemma 1: 2eps/(1-gamma)^2 for Q*; Lemma 2 for model-irrelevance with an |S| factor).

## Problem / Gap
Exact state abstractions need Q* (the ground MDP must be solved first) and give no compression when no two states are exactly alike; the paper studies approximate aggregation with tolerance ε.

## Method
Four approximate aggregation types, all instances of φ̃_{f,ε} (|f(s1,a) − f(s2,a)| ≤ ε for all a): φ̃_{Q*,ε}, φ̃_{model,ε}, φ̃_{bolt,ε}, φ̃_{mult,ε}. Value-loss analysis of the lifted abstract policy against the ground MDP; Lemmas 2–4 reduce to the Q* case with a derived bound. Experiments use greedy aggregation on Q*.

## Key Results
- Lemma 1 (Q*): loss ≤ 2ε/(1−γ)².
- Lemma 2 (model): loss ≤ (2ε + 2γε(|S_G| − 1))/(1−γ)³.
- Lemma 3 (Boltzmann) and Lemma 4 (multinomial): 2ε(|A|/(1−γ) + …)/(1−γ)² with extra normalizer constants k_bolt, k_mult; all bounds are 0 at ε = 0.

## Assumptions
- Finite, discounted MDP (experiments γ = 0.95).
- Rewards normalized; Boltzmann/multinomial types need a bound k on normalizing terms.

## Limitations / Failure Modes
- Model-type bound (Lemma 2) scales with |S_G| and (1−γ)⁻³, so it can be vacuous for large state spaces.
- All bounds diverge as γ → 1; no undiscounted or finite-horizon result.
- Empirically, goal-based Taxi degrades sharply past ε ≈ 0.02.

## Reusable Ingredients
- Generic φ̃_{f,ε} aggregation template and the reduction of model/distributional abstractions to a Q*-type bound.
- Greedy randomized-order aggregation procedure.

## Open Questions
- How to learn the abstractions online, and what necessary conditions give bounded error?
- Links to options and information-theoretic limits of abstraction.

## Claims
- claim:abel_lemma2_vacuous_time_bins (uses)
- claim:level1_horizon_independent (uses)

## Connections
_Edges are recorded in `graph/edges.jsonl`; summarize here for human readers._

## Relevance to This Project
Supplies the price tags for Levels 2–3: Lemma 1 bounds Level 3 (φ_Q*,ε) and Lemma 2 bounds Level 2 (φ_model,ε). Lemma 2 was re-read for the project and is vacuous on BPMN+OPT Fig. 2 with time bins (G3), which is why Level 2 follows the safe route (D-004).

## Abstract (original)

> The combinatorial explosion that plagues planning and reinforcement learning (RL) algorithms can be moderated using state abstraction. Prohibitively large task representations can be condensed such that essential information is preserved, and consequently, solutions are tractably computable. However, exact abstractions, which treat only fully-identical situations as equivalent, fail to present opportunities for abstraction in environments where no two situations are exactly alike. In this work, we investigate approximate state abstractions, which treat nearly-identical situations as equivalent. We present theoretical guarantees of the quality of behaviors derived from four types of approximate abstractions. Additionally, we empirically demonstrate that approximate abstractions lead to reduction in task complexity and bounded loss of optimality of behavior in a variety of environments.

