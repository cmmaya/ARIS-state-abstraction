---
type: paper
node_id: paper:ni2023_learning_good_state
title: "Learning Good State and Action Representations via Tensor Decomposition"
authors: ["Chengzhuo Ni", "Yaqi Duan", "Munther Dahleh", "Anru Zhang", "Mengdi Wang"]
year: 2023
venue: "JMLR 24(115)"
external_ids:
  arxiv: "2105.01136"
  doi: null
  s2: null
tags: ["representation-learning", "state-abstraction", "tensor-decomposition"]
added: 2026-11-06T16:32:17Z
---

# Learning Good State and Action Representations via Tensor Decomposition

## One-line thesis
Learns low-dimensional state and action representations (and discrete abstractions) from trajectories via kernelized low-Tucker-rank tensor approximation, with statistical error bounds.

## Problem / Gap
Learn low-dimensional state and action representations, and a discrete abstraction, of a continuous MDP from trajectory data.

## Method
Kernelized tensor mean embedding of transitions with importance sampling, low-Tucker-rank approximation (HOOI), SVD-based embedding maps, and k-means clustering of state and action features into a discrete abstraction.

## Key Results
- Statistical error bounds for the estimated transition operator (Theorem 4) and for clustering/misclassification (Theorems 6–7).
- Theorem 8: worst-case H-step policy-evaluation error D ≤ 4 c̄ c⁻¹ H² M, where M measures partition mismatch, so the error grows at most quadratically in H, not exponentially.

## Assumptions
- Low Tucker rank of the transition operator (Assumption 1).
- Single sample path from a known behavior policy, with mixing time t_mix (Assumption 2).
- Block-piecewise-constant transitions for Theorems 6–8 (Assumption 3).

## Limitations / Failure Modes
- Needs known Tucker ranks and a large-sample regime.
- H² scaling of the abstraction error; exact recovery needs a separation gap.

## Reusable Ingredients
- The finite-horizon policy-evaluation reduction (Theorem 8): discrete-step abstraction error that is quadratic in the horizon.
- Matrix Bernstein for Markov samples via mixing-time blocking.

## Open Questions
_Not stated in source._

## Claims
_No claims tracked yet — populate via /proof-checker._

## Connections
_Edges are recorded in `graph/edges.jsonl`; summarize here for human readers._

## Relevance to This Project
Cited for the discrete-step finite-horizon result (Theorem 8, quadratic in H), which shows that a discrete-step finite-horizon bound is not novel (X-006). It also corroborates the ~N²ε̂ growth of Abel's induction at γ = 1 (D-005). Our open piece is the time horizon with random N_H (G2).

## Abstract (original)

> The transition kernel of a continuous-state-action Markov decision process (MDP) admits a natural tensor structure. This paper proposes a tensor-inspired unsupervised learning method to identify meaningful low-dimensional state and action representations from empirical trajectories. The method exploits the MDP's tensor structure by kernelization, importance sampling and low-Tucker-rank approximation. This method can be further used to cluster states and actions respectively and find the best discrete MDP abstraction. We provide sharp statistical error bounds for tensor concentration and the preservation of diffusion distance after embedding. We further prove that the learned state/action abstractions provide accurate approximations to latent block structures if they exist, enabling function approximation in downstream tasks such as policy evaluation.

