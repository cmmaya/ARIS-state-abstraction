---
type: claim
node_id: claim:level1_horizon_independent
name: "Level 1 exact abstractions are horizon- and discount-independent"
description: "Exact bisimulation covers gamma=1, H=200 and preserves the joint law of next abstract state, holding time and reward"
node_type: claim
status: drafted
provenance: ""
tags: []
date: 2026-11-06
added: 2026-11-06T16:35:51Z
---

# Level 1 exact abstractions are horizon- and discount-independent

**status:** `drafted`

## Statement
Rules R1-R4 (and R3b on the PH model) yield model-irrelevance abstractions of the BPMN+OPT SMDP that preserve the joint distribution of (next abstract state, tau, reward), hence the optimal policy for any discount and any horizon.

## Honest scope
Corroborated against Li 2006 / Abel 2016 (bounds 0 at eps=0); formal proof on Figs. 1-2 still to write. PH guarantee holds on the model, not on the deployed system with unobservable phases.

## Evidence chain
Validation notes 2026-11-05; to formalize (phase 1).

## Connections
_Edges are recorded in `graph/edges.jsonl`; summarize here for human readers._

