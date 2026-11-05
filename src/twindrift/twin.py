from __future__ import annotations

import numpy as np
from sklearn.cluster import KMeans

N_OP = 3


class HealthyTwin:
    """Per-operating-condition healthy mean/std of each sensor, learnt from the first
    ``ref`` cycles of reference engines. The operating condition is found by k-means on the
    three operating settings (k = 1 for single-condition data)."""

    def __init__(self, n_conditions: int = 1, ref: int = 30):
        self.k, self.ref = n_conditions, ref

    def fit(self, engines: list[np.ndarray]):
        ops = np.vstack([e[: self.ref, :N_OP] for e in engines])
        self.km = KMeans(self.k, n_init=5, random_state=0).fit(ops) if self.k > 1 else None
        lab = self._cond(ops)
        S = np.vstack([e[: self.ref, N_OP:] for e in engines])
        self.mu = np.zeros((self.k, S.shape[1]))
        self.sd = np.ones((self.k, S.shape[1]))
        for c in range(self.k):
            m = lab == c
            self.mu[c] = S[m].mean(0)
            self.sd[c] = S[m].std(0)
        self.use = self.sd.min(0) > 1e-6  # drop constant sensors
        return self

    def _cond(self, ops):
        return self.km.predict(ops) if self.km is not None else np.zeros(len(ops), int)

    def residual_z(self, e: np.ndarray) -> np.ndarray:
        c = self._cond(e[:, :N_OP])
        z = (e[:, N_OP:] - self.mu[c]) / self.sd[c]
        return z[:, self.use]


def drift_score(z: np.ndarray, lam: float = 0.1) -> np.ndarray:
    """EWMA of the mean squared standardised residual over sensors (about 1 when healthy)."""
    q = (z**2).mean(1)
    out = np.empty_like(q)
    acc = q[0]
    for t, v in enumerate(q):
        acc = lam * v + (1 - lam) * acc if t else v
        out[t] = acc
    return out


def first_alarm(score: np.ndarray, thr: float, persist: int = 3, start: int = 0):
    above = score > thr
    run = 0
    for t in range(start, len(score)):
        run = run + 1 if above[t] else 0
        if run >= persist:
            return t
    return None


def conformal_threshold(max_stats: np.ndarray, alpha: float) -> float:
    n = len(max_stats)
    k = int(np.ceil((n + 1) * (1 - alpha)))
    s = np.sort(max_stats)
    return float(s[k - 1]) if k <= n else float("inf")
