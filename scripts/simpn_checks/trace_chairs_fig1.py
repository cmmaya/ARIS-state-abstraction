"""C-15 / H-002: trace chair tokens between infusion and observation on simpn's Fig. 1 model.

For every patient, record the chair used for infusion and the chair used for observation, whether
observation started later than the infusion ended (waited for a chair), and whether the infusion chair
was taken by another patient's infusion while this patient was waiting for observation.

Usage:
    git clone --depth 1 --branch bpmnopt https://github.com/bpogroup/simpn.git <dir>
    python scripts/simpn_checks/trace_chairs_fig1.py <dir> [n_episodes] [--out experiments/results/c15_chair_trace_fig1.json]

If `sortedcontainers` is not installed, a minimal stand-in from _shim/ is used.
"""
import argparse
import datetime
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

ap = argparse.ArgumentParser()
ap.add_argument("simpn_dir")
ap.add_argument("n_episodes", nargs="?", type=int, default=30)
ap.add_argument("--seed-base", type=int, default=42)
ap.add_argument("--out", default=None)
args = ap.parse_args()

SIMPN = os.path.abspath(args.simpn_dir)
sys.path[:0] = [os.path.join(SIMPN, "er_paper", "code"), SIMPN]
try:
    import sortedcontainers  # noqa: F401
except ImportError:
    sys.path.insert(0, os.path.join(HERE, "_shim"))

from simpn.simulator import SimProblem  # noqa: E402
from smdp_env import SMDPEnv            # noqa: E402
from solvers import FIFOPolicy          # noqa: E402

JSON_PATH = os.path.join(SIMPN, "er_paper", "models", "fig1_problem.json")
INFUSIONS = ("Standard_infusion", "Intensive_infusion")


def busy_pairs(problem, task):
    return [(tok.value[0]["id"], tok.value[1]["id"]) for tok in problem.id2node[task + "_busy"].marking]


totals = dict(patients=0, same_chair=0, other_chair=0, waited_for_chair=0, chair_taken_by_other=0)
examples = []
_orig_fire = SimProblem.fire

for ep in range(args.n_episodes):
    st = {"inf_chair": {}, "inf_end": {}, "obs_seen": set(), "taken": set()}

    def fire(self, binding, st=st, ep=ep):
        _orig_fire(self, binding)
        t = self.clock
        chair_holder = {}
        for task in INFUSIONS:
            for cid, rid in busy_pairs(self, task):
                st["inf_chair"].setdefault(cid, rid)
                chair_holder[rid] = cid
        for tok in self.id2node["waiting_observation"].marking:
            cid = tok.value["id"]
            st["inf_end"].setdefault(cid, t)
            ch = st["inf_chair"].get(cid)
            if ch in chair_holder and chair_holder[ch] != cid:
                st["taken"].add(cid)
        for cid, rid in busy_pairs(self, "Observation"):
            if cid in st["obs_seen"]:
                continue
            st["obs_seen"].add(cid)
            ch = st["inf_chair"].get(cid)
            totals["patients"] += 1
            totals["same_chair" if ch == rid else "other_chair"] += 1
            waited = t - st["inf_end"].get(cid, t) > 1e-9
            totals["waited_for_chair"] += waited
            totals["chair_taken_by_other"] += cid in st["taken"]
            if len(examples) < 3:
                examples.append(f"ep{ep} patient {cid}: infusion {ch} -> observation {rid} at t={t:.2f}")

    SimProblem.fire = fire
    SMDPEnv(json_path=JSON_PATH).run_with_policy(FIFOPolicy(), seed=args.seed_base + ep)

SimProblem.fire = _orig_fire

try:
    commit = subprocess.run(["git", "-C", SIMPN, "rev-parse", "--short", "HEAD"],
                            capture_output=True, text=True).stdout.strip()
except OSError:
    commit = ""

result = {
    "_meta": {
        "date": datetime.date.today().isoformat(),
        "simpn_commit": commit,
        "simpn_branch": "bpmnopt",
        "model": "er_paper/models/fig1_problem.json",
        "policy": "FIFO (solvers.FIFOPolicy)",
        "seeds": list(range(args.seed_base, args.seed_base + args.n_episodes)),
        "checklist": "C-15",
        "hypothesis": "H-002",
        "examples": examples,
        "notes": "Chair semantics trace. Code: BPMNTask complete event returns the chair to idle_chair; "
                 "Observation has no resource_constraint, so it takes any idle chair.",
    },
    "_format": {"same_chair_rate": "pct1"},
    **totals,
    "same_chair_rate": totals["same_chair"] / max(1, totals["patients"]),
    "n_episodes": args.n_episodes,
}

print(json.dumps(result, indent=2))
if args.out:
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
        f.write("\n")
