from __future__ import annotations

import numpy as np
import pandas as pd

COLS = ["unit", "cycle", "op1", "op2", "op3"] + [f"s{i}" for i in range(1, 22)]


def load_cmapss(path: str) -> pd.DataFrame:
    """NASA C-MAPSS training file (simulated turbofan run-to-failure)."""
    return pd.read_csv(path, sep=r"\s+", header=None, names=COLS)


def engines(df: pd.DataFrame) -> dict[int, np.ndarray]:
    sensors = [c for c in COLS if c.startswith("s")]
    return {
        int(u): g.sort_values("cycle")[["op1", "op2", "op3"] + sensors].to_numpy(float)
        for u, g in df.groupby("unit")
    }
