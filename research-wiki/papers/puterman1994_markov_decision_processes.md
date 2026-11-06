---
type: paper
node_id: paper:puterman1994_markov_decision_processes
title: "Markov Decision Processes: Discrete Stochastic Dynamic Programming"
authors: ["Martin L. Puterman"]
year: 1994
venue: "Wiley (book)"
external_ids:
  arxiv: null
  doi: null
  s2: null
tags: ["mdp", "smdp", "uniformization", "book"]
added: 2026-11-06T16:32:41Z
---

# Markov Decision Processes: Discrete Stochastic Dynamic Programming

## One-line thesis
Reference text; Ch. 11 covers semi-Markov and continuous-time MDPs, including uniformization to an equivalent discrete-time MDP with per-step discount Lambda/(Lambda+beta).

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
_No claims tracked yet — populate via /proof-checker._

## Connections
_Edges are recorded in `graph/edges.jsonl`; summarize here for human readers._

## Relevance to This Project
Ch. 11 (SMDPs, uniformization) is the basis of the safe route: uniformize the finite CTMDP from exponential/PH durations, giving per-step discount Λ/(Λ+β), then apply Li/Abel (D-004). Also the source of the effective discount E[e^(−βτ)], which is a known result (X-007). Book not in literature/.

