---
type: paper
node_id: paper:dijkman2026_bpmnopt_conceptual_modeling
title: "BPMN+OPT: A Conceptual Modeling Language for Business Process Optimization"
authors: ["Remco Dijkman", "Arik Senderovich", "Stefanie Rinderle-Ma"]
year: 2026
venue: "Manuscript (LNCS format; venue not printed)"
external_ids:
  arxiv: null
  doi: null
  s2: null
tags: ["bpm", "bpmn", "smdp", "process-optimization", "resource-allocation", "scheduling", "routing", "conceptual-modeling"]
added: 2026-11-06T02:09:40Z
---

# BPMN+OPT: A Conceptual Modeling Language for Business Process Optimization

## One-line thesis
BPMN+OPT adds an optimization annotation layer (state, stochasticity, decision moments/variables, constraints, objectives) to unchanged BPMN models and gives it SMDP execution semantics.

## Problem / Gap
BPM offers rich process models (BPMN) but no optimization semantics, while OR/RL methods assume states, actions, constraints and rewards were already engineered outside the process model, so the decision structure is not traceable to the process. Neither side specifies sequential stochastic optimization problems such as scheduling, resource assignment, or routing at the process-model level.

## Method
A BPMN+OPT process is a tuple M = (T, E, G, F, C, R, auth, X, Obj, Con, Mom). Tasks/events carry conditions, stochastic update rules and processing-time distributions; case/resource object types carry typed attributes plus a `loc` attribute; X are decision variables, Obj objectives, Con constraints, Mom Boolean decision-moment expressions. The execution state is (O_t, Q_t), meaning the object valuation plus an event calendar that keeps non-memoryless durations Markovian. The induced SMDP observes execution only at epochs where some Mom is true, and its actions are feasible (decision-variable instance, value) pairs under Con. Decisions are primitive and sequential: one variable is assigned, moments are re-evaluated, then autonomous execution runs to the next epoch. P, holding times and rewards are estimated by Monte Carlo simulation through a colored-Petri-net backend (SimPN; JSON model spec).

## Key Results
- Resource-assignment fragment (2 oncologists, 2 patient types, H = 200, K = 5 × 30 episodes): avg. cycle time Q-learning 85.7 [81.6, 89.7] and empirical value iteration 85.7 [81.6, 89.7] vs FIFO 86.8, SPT 86.7, Random 96.5. SMDP methods are roughly at FIFO/SPT level; the authors frame this as pipeline validation, not a performance gain.
- The full outpatient chemotherapy process (scheduling + assignment + routing in one model) compiles to one SMDP interface with feasibility masks and flow-time rewards, but its sparse states expose the limits of tabular methods.

## Assumptions
- Event-calendar times the policy uses are operationally known. Latent sampled times would make the problem a POMDP, which is out of scope.
- Decisions are committed one primitive action at a time (online setting). Joint decisions are only possible through structured-domain variables.
- The evaluation horizon is supplied externally. The demo objective is cumulative patient flow time (area under the number-in-system curve).

## Limitations / Failure Modes
- Reachable state space blows up with cases, resources, attributes and pending events. Tabular methods do not scale to the full process.
- Out of scope: design-time redesign, strategic capacity/SLA planning, native batching, and tasks needing several resources at once. No finalized graphical notation or usability study.
- Evaluation is a proof of concept on a single synthetic example with no real data or calibration. The SMDP policies do not beat simple heuristics.

## Reusable Ingredients
- Recipe for deriving an SMDP from a process model: states = reachable execution states where a decision moment holds; actions = feasible (variable-instance, value) pairs; transitions, holding times and rewards come from simulating until the next decision epoch.
- Event calendar Q_t as an explicit state component, so that non-exponential durations become Markovian.
- Hand-built abstract state s~ = (n_P1, n_P2, idle oncologists) with longest-waiting tie-breaking, a concrete example of state abstraction for process control. Open-source code: github.com/bpogroup/simpn (branch bpmnopt).

## Open Questions
- Which decomposition or abstraction techniques can exploit process structure to shrink the induced SMDP while keeping traceability to the BPMN+OPT model? The authors name this as future work.
- How should BPMN+OPT parameters be calibrated from event logs via process/performance mining, and does function approximation make the full process tractable?

## Claims
_No claims tracked yet — populate via /proof-checker._

## Connections
_Edges are recorded in `graph/edges.jsonl`; summarize here for human readers._

## Relevance to This Project
_Project context not yet set — populate RESEARCH_BRIEF.md or gap_map.md to enable this section._

