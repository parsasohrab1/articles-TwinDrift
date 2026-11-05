"""NASA C-MAPSS (SIMULATED turbofan run-to-failure): drift monitoring of a healthy-reference twin.

usage: python research/run_study.py /path/to/CMAPSSData
FD001 (1 operating condition, 100 engines) and FD002 (6 conditions, 260 engines).
Engines are split in 3 groups (reference/twin fit, calibration, test). The twin is the healthy mean/std per
operating condition of the first 30 cycles; the score is an EWMA of the mean squared residual.
Alarm threshold: conformal quantile of the per-engine maximum score over cycles 31-60 (assumed healthy).
Reported: false-alarm rate in cycles 31-60 on test engines, detection lead (cycles before failure).
"""

import json
import sys
from pathlib import Path

import numpy as np

from twindrift.data import engines, load_cmapss
from twindrift.twin import HealthyTwin, conformal_threshold, drift_score, first_alarm

REF, HEALTHY_END = 30, 60


def run(path: str, k: int, seed: int):
    E = list(engines(load_cmapss(path)).values())
    rng = np.random.default_rng(seed)
    p = rng.permutation(len(E))
    third = len(E) // 3
    ref = [E[i] for i in p[:third]]
    cal = [E[i] for i in p[third : 2 * third]]
    tst = [E[i] for i in p[2 * third :]]
    tw = HealthyTwin(k, REF).fit(ref)
    sc = lambda e: drift_score(tw.residual_z(e))
    mx = np.array([sc(e)[REF:HEALTHY_END].max() for e in cal])
    rules = {f"conformal_{a}": conformal_threshold(mx, a) for a in (0.05, 0.1)}
    rules.update({f"fixed_{t}": float(t) for t in (2, 3, 5)})
    out = {}
    for name, thr in rules.items():
        fa, leads, rel, miss = 0, [], [], 0
        for e in tst:
            s = sc(e)
            a = first_alarm(s, thr, start=REF)
            if a is not None and a < HEALTHY_END:
                fa += 1
                continue
            if a is None:
                miss += 1
                continue
            leads.append(len(e) - a)
            rel.append(a / len(e))
        n = len(tst)
        out[name] = {
            "threshold": thr,
            "false_alarm_rate": fa / n,
            "missed_rate": miss / n,
            "median_lead_cycles": float(np.median(leads)) if leads else None,
            "median_alarm_fraction_of_life": float(np.median(rel)) if rel else None,
        }
    return out, len(tst)


def main(root: str):
    res = {
        "note": "SIMULATED turbofan data (NASA C-MAPSS); engine failure cycle is the end of each series; "
        "20 random engine splits; no ground truth for drift onset",
        "datasets": {},
    }
    for name, k in (("FD001", 1), ("FD002", 6)):
        runs = []
        n_test = 0
        for s in range(20):
            r, n_test = run(f"{root}/train_{name}.txt", k, s)
            runs.append(r)
        agg = {
            rule: {
                m: float(np.mean([x[rule][m] for x in runs if x[rule][m] is not None]))
                for m in runs[0][rule]
            }
            for rule in runs[0]
        }
        res["datasets"][name] = {"n_test_engines_per_split": n_test, "rules": agg}
        print(name, n_test)
        for rule, v in agg.items():
            print("  ", rule, {a: round(b, 3) for a, b in v.items()})
    Path(__file__).with_name("results.json").write_text(json.dumps(res, indent=1))


if __name__ == "__main__":
    main(sys.argv[1])
