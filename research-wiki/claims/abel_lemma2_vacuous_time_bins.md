---
type: claim
node_id: claim:abel_lemma2_vacuous_time_bins
name: "Abel 2016 Lemma 2 is vacuous on BPMN+OPT Fig. 2 with time binning"
description: "Delta=0.5, K=5: |S_A|=18,468, |S_A|*eps_T ~ 923 > 1/(1-gamma) for all gamma; finer bins worse"
node_type: claim
status: verified
provenance: ""
tags: []
date: 2026-11-06
added: 2026-11-06T16:35:50Z
---

# Abel 2016 Lemma 2 is vacuous on BPMN+OPT Fig. 2 with time binning

**status:** `verified`

## Statement
loss <= 2 eps_R/(1-gamma)^2 + 2 gamma |S_A| eps_T/(1-gamma)^3; with eps_T <= Delta/10 and |S_A| ~ 1/Delta^2 the bound exceeds the value range for every gamma and grows as Delta shrinks.

## Honest scope
Applies to the |S_A|-scaled Abel bound with elapsed-time bins; says nothing about AIS-style bounds or R6/R7 merges.

## Evidence chain
Lemma 2 re-read against Abel et al. 2016 (ICML); arithmetic in notes 2026-11-05.

## Connections
_Edges are recorded in `graph/edges.jsonl`; summarize here for human readers._

