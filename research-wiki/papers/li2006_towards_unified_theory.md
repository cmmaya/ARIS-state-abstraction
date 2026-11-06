---
type: paper
node_id: paper:li2006_towards_unified_theory
title: "Towards a Unified Theory of State Abstraction for MDPs"
authors: ["Lihong Li", "Thomas J. Walsh", "Michael L. Littman"]
year: 2006
venue: "ISAIM 2006"
external_ids:
  arxiv: null
  doi: null
  s2: null
tags: ["state-abstraction", "mdp", "hierarchy"]
added: 2026-11-06T16:32:39Z
---

# Towards a Unified Theory of State Abstraction for MDPs

## One-line thesis
Orders exact state abstractions from finest to coarsest (model-irrelevance, Q^pi, Q*, a*, pi*) and shows which preserve the optimal policy and Q-learning convergence; pi*-irrelevance gives no learning guarantee.

## Problem / Gap
_TODO._

## Method
_TODO._

## Key Results
_TODO._

## Assumptions
_TODO._

## Limitations / Failure Modes
_TODO._

## Reusable Ingredients
_TODO._

## Open Questions
_TODO._

## Claims
- claim:paper_abstraction_not_exact (uses)
- claim:level1_horizon_independent (uses)

## Connections
_Edges are recorded in `graph/edges.jsonl`; summarize here for human readers._

## Relevance to This Project
The ladder behind the four levels: φ_model ⪰ φ_Q^π ⪰ φ_Q* ⪰ φ_a* ⪰ φ_π*. It gives Level 1's zero-loss guarantee (optimal policy and Q-learning convergence preserved) and the reason Level 4 (φ_π*) is out of scope (X-005). Source PDF not in literature/; other sections await the paper.

