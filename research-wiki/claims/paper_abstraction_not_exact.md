---
type: claim
node_id: claim:paper_abstraction_not_exact
name: "BPMN+OPT's Fig. 2 abstraction (n_P1, n_P2, I) is not exact"
description: "Completion rates depend on type in service; exact L1 state needs oncologist status: 324 vs 144 states (queue cap 5)"
node_type: claim
status: verified
provenance: ""
tags: []
date: 2026-11-06
added: 2026-11-06T16:35:50Z
---

# BPMN+OPT's Fig. 2 abstraction (n_P1, n_P2, I) is not exact

**status:** `verified`

## Statement
Even with exponential durations, (n_P1, n_P2, I) is not a model-irrelevance abstraction of the Fig. 2 SMDP; the exact Level-1 abstraction tracks each oncologist's status in {idle, P1, P2}, giving 324 states at queue cap 5 versus 144.

## Honest scope
Model-exactness only; whether the paper's abstraction loses value is untested (H-001).

## Evidence chain
State count computed during validation (notes 2026-11-05); not yet a results JSON.

## Connections
_Edges are recorded in `graph/edges.jsonl`; summarize here for human readers._

