# Gap Map

_Field gaps with stable IDs._

- **G1** (open): Process-model SMDPs (BPMN+OPT) are solved with hand-made state abstractions whose guarantees are never stated. Li 2006 / Abel 2016 assume phi is given; nobody derives phi and its guarantee from model annotations. Targeted by idea:language_derived_abstraction_levels.
- **G2** (open): State-abstraction bounds for an SMDP over a time horizon with a random, policy-dependent number of decision epochs N_H (incl. zero-length epochs). Discrete-step finite-horizon bounds exist (AIS; quadratic in horizon) but not this setting. Gated by the AIS audit (backlog B-003).
- **G3** (open): Approximate-abstraction loss bounds that stay non-vacuous under time discretization. Abel 2016 Lemma 2 scales with |S_A| and is vacuous on BPMN+OPT Fig. 2; AIS-style distribution distances may remove the factor.
