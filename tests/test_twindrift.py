import numpy as np

from twindrift.twin import HealthyTwin, conformal_threshold, drift_score, first_alarm


def _engine(n=200, drift_at=None, seed=0):
    rng = np.random.default_rng(seed)
    ops = np.zeros((n, 3))
    s = rng.normal(0, 1, (n, 4)) + 50
    if drift_at:
        s[drift_at:] += np.linspace(0, 6, n - drift_at)[:, None]
    return np.hstack([ops, s])


def test_healthy_score_stays_near_one_and_no_alarm():
    eng = [_engine(seed=i) for i in range(20)]
    tw = HealthyTwin(1, ref=30).fit(eng)
    sc = drift_score(tw.residual_z(_engine(seed=99)))
    assert 0.5 < np.median(sc) < 2.0 and first_alarm(sc, 4.0) is None


def test_drift_is_detected_after_onset():
    eng = [_engine(seed=i) for i in range(20)]
    tw = HealthyTwin(1, ref=30).fit(eng)
    sc = drift_score(tw.residual_z(_engine(drift_at=100, seed=7)))
    a = first_alarm(sc, 4.0)
    assert a is not None and a >= 100


def test_conformal_threshold_rank():
    assert conformal_threshold(np.arange(1.0, 100.0), 0.1) == 90.0
