# BACKLOG
<!-- Ledger of everything decided, discarded and parked. One row per item; never delete rows.
Decided → full rationale in decisions.md (same D-id). Parked revived → move row to Decided, note "from B-###".
Parked dropped → move to Discarded, note "from B-###". Refuted hypotheses and failed ideas go to Discarded.
Source = session (S#), log date, /idea-discovery report, paper:<slug>, advisor. IDs sequential per section. -->

## Decided
| ID | Date | Decision | Why | Source |
|----|------|----------|-----|--------|
| D-001 | 2026-11-05 | Build repo on ARIS + research/ state files, custom skills, results macros, LaTeX CI | persistent memory across sessions; no typed numbers in paper | S1 |
| D-002 | 2026-11-06 | Direction: derive state abstractions for BPMN+OPT SMDPs from model annotations, organized as 4 levels on Li's hierarchy (L1 exact, L2 ε-approx, L3 value-based, L4 out of scope) | Li and Abel assume φ is given; the derivation from annotations, with a guarantee per level, is the gap | S2 (notes 2026-11-05: proposal 2026-10-24 + validation) |
| D-003 | 2026-11-06 | Level 1 = exact rules R1–R4 + R3b (phase-type), acting on elapsed (observable) time | validated: zero loss, horizon-independent, SMDP-exact; residual times are latent in BPMN+OPT | S2 (notes 2026-11-05: proposal 2026-10-24 + validation) |
| D-004 | 2026-11-06 | Level 2 guarantee follows the safe route: exponential/phase-type durations, uniformize, apply Li/Abel; Abel bound only for R6/R7; R5 only in the rigorous route | Abel Lemma 2 with time bins is vacuous on Fig. 2 (X-004); safe route avoids AIS, bins and latent times | S2 (notes 2026-11-05: proposal 2026-10-24 + validation) |
| D-005 | 2026-11-06 | Level 3 is a secondary contribution: static-analysis proposer + Monte Carlo validation of ε̂ under FIFO | needs Q*, so it cannot be certified from syntax; guarantee only a posteriori | S2 (notes 2026-11-05: proposal 2026-10-24 + validation) |
| D-006 | 2026-11-06 | Novelty claim narrowed to annotation-derived abstractions/bounds and the random time horizon N_H | SMDP discounting and discrete-step finite-horizon bounds already exist (X-006, X-007) | S2 (notes 2026-11-05: proposal 2026-10-24 + validation) |
| D-007 | 2026-11-06 | Discounted bounds certify a proxy; evaluate every abstraction on the undiscounted H = 200 flow-time objective in simpn | the paper's objective is γ = 1, H = 200; Level 1 unaffected because exact | S2 (notes 2026-11-05: proposal 2026-10-24 + validation) |
| D-008 | 2026-11-06 | RQ2's discretization axis follows the Level 2 route: safe route → vary δ (R6) and K (R7) against the Abel bound; rigorous route → vary Δ (R5) and K against the AIS bound. Only the safe route is active now (D-004) | Δ only exists in the rigorous route, and Abel + Δ is vacuous (X-004), so each route needs its own axis and bound | S2 (user, turn 3) |
| D-009 | 2026-11-06 | Fig. 1 chair semantics = simpn as implemented: chairs pooled, released at infusion end, Observation takes any idle chair | evaluation runs in simpn (D-007); under pooling R2's idle-chair count is exact; FIFO trace shows no waits, so in practice it behaves like hold (0/2,095 waits) | S3 (user; experiments/results/c15_chair_trace_fig1.json) |
| D-010 | 2026-11-06 | C-01 is stated on the unbounded-queue Fig. 2 model (as in simpn); the 324-state count is a corollary for the model truncated at K = 5 per queue | simpn has no queue cap; truncation changes the dynamics (blocked arrivals), which is R7's job, not Level 1's | S3 (user) |
| D-011 | 2026-11-06 | Level 1 proofs use generic exponential rates (λ, p, μ(o, type) > 0); the numeric instance for experiments keeps the uniform means (φ₁: 3, 4; φ₂: 5, 6; arrivals mean 10; p = 0.5) | exactness and the 324 count don't depend on the values; the means keep the exponential model comparable to the uniform one | S3 (user) |

## Discarded
| ID | Date | What | Why | Source |
|----|------|------|-----|--------|
| X-001 | 2026-11-05 | Mermaid schematic in STATUS.md | figures cost agent context and aren't used by it | S1 |
| X-002 | 2026-11-05 | STATUS.md as full project snapshot | replaced by last-3-sessions log + this ledger | S1 |
| X-003 | 2026-11-06 | Treat the paper's (n_P1, n_P2, I) as an exact abstraction | refuted: completion rates depend on type in service; exact needs oncologist status → 324 vs 144 states | S2 (notes 2026-11-05: proposal 2026-10-24 + validation) |
| X-004 | 2026-11-06 | Abel Lemma 2 + time binning (R5) as the Level 2 guarantee | vacuous: \|S_A\|·ε_T ≈ 923 at Δ = 0.5, K = 5; finer bins worse (ε_T ∝ Δ, \|S_A\| ∝ 1/Δ²) | S2 (notes 2026-11-05: proposal 2026-10-24 + validation) |
| X-005 | 2026-11-06 | Level 4 (φ_π*) as a target | no learning guarantee (Li et al. 2006); FIFO/SPT kept only as baselines | S2 (notes 2026-11-05: proposal 2026-10-24 + validation) |
| X-006 | 2026-11-06 | Discrete-step finite-horizon bound as the core theoretical result | already exists (quadratic in horizon; Subramanian et al. 2022, Ni et al. 2023); open piece is the time horizon with random N_H | S2 (notes 2026-11-05: proposal 2026-10-24 + validation) |
| X-007 | 2026-11-06 | SMDP effective discount E[e^(−βτ)] as a contribution | known corollary (Schweitzer 1971; Puterman Ch. 11); Abel et al. 2020 already cover semi-Markov options | S2 (notes 2026-11-05: proposal 2026-10-24 + validation) |
| X-008 | 2026-11-06 | Rules R3/R5 acting on residual event times | residual times are latent in BPMN+OPT (Def. 2); rules use elapsed time | S2 (notes 2026-11-05: proposal 2026-10-24 + validation) |
| X-009 | 2026-11-06 | AIS bounds for Level 3 | AIS bounds model-based abstractions; Level 3 is value-based | S2 (notes 2026-11-05: proposal 2026-10-24 + validation) |
| X-010 | 2026-11-06 | H-002: chairs held from infusion to observation in simpn | refuted: BPMNTask returns the chair at infusion end and Observation takes any idle chair (guard not implemented); 0/2,095 patients observed in their infusion chair. Idle count still exact for simpn (pooled chairs); ground truth → C-28 | S3 (experiments/results/c15_chair_trace_fig1.json) |

## Parked
| ID | Date | Idea | Why parked | Revisit when | Source |
|----|------|------|------------|--------------|--------|
| B-001 | 2026-11-05 | Pinned devcontainer/Docker environment | not needed before experiments | before the first experiment that goes in the paper | S1 |
| B-002 | 2026-11-05 | rliable evaluation (IQM + bootstrap CIs over seeds) | no experiments yet | first multi-seed comparison | S1 |
| B-003 | 2026-11-06 | Rigorous route: general durations with AIS (Subramanian et al. 2022) extended to a time horizon | open theory: G2 random N_H incl. zero-length epochs (likely failure point), G4 finite Lipschitz constant | after Level 1 is formalized: run the 1–2 week AIS audit; corollary → joins this paper, new theorem → separate paper | S2 (notes 2026-11-05: proposal 2026-10-24 + validation) |
| B-004 | 2026-11-06 | LLM proposer for Level 3 groupings | non-reproducible; static analysis is the core proposer | phase 4 (Level 3 write-up), as an optional comparison | S2 (notes 2026-11-05: proposal 2026-10-24 + validation) |
| B-005 | 2026-11-06 | Theorem: local reachability ⇒ small Level-3 ε (e.g. downstream resources never saturated) | upstream activity can matter indirectly; not needed for the main result | after the Level 3 proposer is implemented and ε̂ data exists | S2 (notes 2026-11-05: proposal 2026-10-24 + validation) |
