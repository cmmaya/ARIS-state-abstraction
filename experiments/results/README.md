# experiments/results

One JSON file per experiment (or per method × environment). `scripts/make_results_tex.py` turns every
number in these files into a LaTeX macro in `paper/results.tex`.

## Format

```json
{
  "_meta": {"commit": "abc1234", "date": "2026-11-05", "seeds": [0, 1, 2, 3, 4], "env": "CartPole-v1",
            "hypothesis": "H-001", "notes": "free text"},
  "_format": {"success_rate": "pct1"},
  "_precision": 2,
  "return": {"mean": 412.37, "std": 18.2, "ci_low": 398.1, "ci_high": 425.9},
  "success_rate": 0.934,
  "n_seeds": 5,
  "per_seed_return": [401.2, 433.0, 395.4, 420.8, 411.4]
}
```

- Keys starting with `_` are metadata and never become macros. Put the commit hash, seeds and the hypothesis id in `_meta`.
- Nested keys become CamelCase macro names: file `ppo_baseline.json`, key `return.mean` → `\resPpoBaselineReturnMean`.
- Lists (raw per-seed data) are kept for analysis but are not turned into macros.
- `_format` sets a per-key Python format (`".1f"`, `",d"`) or `pctN` (×100, N decimals, adds `\%`).
- `_precision` sets the default decimals for floats in that file (default 2).
- Subfolders are allowed: `cartpole/ppo.json` → `\resCartpolePpo…`.

After adding or changing a file:

```bash
python scripts/make_results_tex.py
```
