---
type: idea
node_id: idea:language_derived_abstraction_levels
title: "Language-derived state abstraction levels for BPMN+OPT"
stage: active
outcome: pending
added: 2026-11-06T16:35:49Z
based_on: ["paper:dijkman2026_bpmnopt_conceptual_modeling", "paper:li2006_towards_unified_theory", "paper:abel2016_near_optimal_behavior"]
target_gaps: ["gap:G1", "gap:G2", "gap:G3"]
tags: ["state-abstraction", "bpmn", "smdp", "bounds"]
---

# Language-derived state abstraction levels for BPMN+OPT

**stage:** `active`  ·  **outcome:** `pending`

Syntactic rules over BPMN+OPT annotations decide the abstraction level (Li hierarchy) and compute its epsilon

## Thesis
Four levels on Li's hierarchy. L1 exact (R1 relevance slicing, R2 exchangeability, R3/R3b memoryless and phase-type durations on elapsed time, R4 reward as rate): zero loss, fully syntactic, validated. L2 epsilon-approximate (R5 time bins, R6 near-identical objects, R7 queue truncation): safe route via exponential/PH durations + uniformization + Abel bounds for R6/R7; rigorous route via AIS parked. L3 value-based: static-analysis proposer + Monte Carlo validation. L4 out of scope. Details: research/abstraction_rules.md.

## Key risks
Abel Lemma 2 vacuous with time bins (|S_A| factor). Discounted bounds certify only a proxy for the gamma=1, H=200 objective. PH phases unobservable at deployment. Novelty must be narrowed: SMDP discounting and discrete finite-horizon bounds are known.

## Connections
_Edges are recorded in `graph/edges.jsonl`; summarize here for human readers._

