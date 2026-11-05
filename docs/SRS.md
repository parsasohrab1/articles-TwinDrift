# Software Requirements Specification – TwinDrift

- SR-1 `data.load_cmapss`/`engines`: C-MAPSS training files; per engine, operating settings and 21 sensors by cycle.
- SR-2 `twin.HealthyTwin`: k-means on the three operating settings (k = 1 or 6), healthy mean and standard deviation per condition and sensor from the first 30 cycles of reference engines; constant sensors dropped.
- SR-3 `twin.drift_score`: EWMA (lambda 0.1) of the mean squared standardised residual; `first_alarm`: first cycle with the score above the threshold for 3 consecutive cycles.
- SR-4 `twin.conformal_threshold`: conformal quantile of the per-engine maximum score over cycles 31–60 of calibration engines.
- SR-5 `research/run_study.py`: engines split in thirds (reference / calibration / test), 20 random splits; false alarm = alarm raised within cycles 31–60 of a test engine.
- SR-6 Three unit tests.
