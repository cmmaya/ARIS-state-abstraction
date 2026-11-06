---
type: paper
node_id: paper:subramanian2022_approximate_information_state
title: "Approximate information state for approximate planning and reinforcement learning in partially observed systems"
authors: ["Jayakumar Subramanian", "Amit Sinha", "Raihan Seraj", "Aditya Mahajan"]
year: 2022
venue: "JMLR 23(12)"
external_ids:
  arxiv: "2010.08843"
  doi: null
  s2: null
tags: ["ais", "pomdp", "approximate-planning", "state-abstraction", "bounds"]
added: 2026-11-06T16:32:16Z
---

# Approximate information state for approximate planning and reinforcement learning in partially observed systems

## One-line thesis
A history compression that approximately predicts reward (eps) and the next compressed state (delta, measured as a distance between distributions) yields an approximate DP with bounded loss, including a finite-horizon bound.

## Problem / Gap
Planning and RL in partially observed systems: belief states need the model, and deep recurrent RL lacks guarantees.

## Method
Defines an information state by properties (P1, P2) and relaxes them to an approximate information state (AIS): (AP1) reward-prediction error ε_t and (AP2) next-AIS prediction error δ_t, measured with an integral probability metric (total variation, Kolmogorov, Wasserstein, MMD). An AIS yields an approximate dynamic program; AIS can be learned with multi-timescale policy-gradient methods (LSTM/feed-forward, actor-only and actor-critic).

## Key Results
- Finite-horizon (Theorem 9) and infinite-horizon discounted (Theorem 27) bounds on the loss of the AIS policy, accumulating the per-step ε_t and δ_t over the horizon (theorem numbers per the alphaxiv overview; verify against the JMLR version).
- Claims tighter bounds than prior work for state aggregation and belief approximation, often by a factor of 1/(1−γ) or more.

## Assumptions
_Not stated in source beyond the AIS definitions (AP1, AP2) and a chosen IPM._

## Limitations / Failure Modes
_Not stated in source._

## Reusable Ingredients
- AIS definitions with δ measured as a distance between whole next-state distributions, which avoids an |S_A|-type factor.
- Unified view: state aggregation, model approximation, belief approximation and observation compression as AIS special cases.

## Open Questions
- Value-based (DQN/distributional) and model-based (Dyna) AIS RL; adaptive choice of the IPM.
- (Project) Does the finite-horizon result extend to a horizon in continuous time with a random number of epochs N_H?

## Claims
_No claims tracked yet — populate via /proof-checker._

## Connections
_Edges are recorded in `graph/edges.jsonl`; summarize here for human readers._

## Relevance to This Project
The theory for the rigorous route: general (non-Markovian) durations with abstracted elapsed time. The parked AIS audit (B-003, H-004) checks G2 (random N_H) and G4 (finite Lipschitz constant); AIS does not help Level 3 (X-009).

## Abstract (original)

> We propose a theoretical framework for approximate planning and learning in partially observed systems. Our framework is based on the fundamental notion of information state. We provide two equivalent definitions of information state -- i) a function of history which is sufficient to compute the expected reward and predict its next value; ii) equivalently, a function of the history which can be recursively updated and is sufficient to compute the expected reward and predict the next observation. An information state always leads to a dynamic programming decomposition. Our key result is to show that if a function of the history (called approximate information state (AIS)) approximately satisfies the properties of the information state, then there is a corresponding approximate dynamic program. We show that the policy computed using this is approximately optimal with bounded loss of optimality. We show that several approximations in state, observation and action spaces in literature can be viewed as instances of AIS. In some of these cases, we obtain tighter bounds. A salient feature of AIS is that it can be learnt from data. We present AIS based multi-time scale policy gradient algorithms. and detailed numerical experiments with low, moderate and high dimensional environments.

