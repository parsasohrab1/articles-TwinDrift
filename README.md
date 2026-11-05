# articles-TwinDrift

Drift monitoring of a sensor-level "digital twin" (healthy reference per operating condition) with an alarm threshold
calibrated by conformal quantile. Data: NASA C-MAPSS turbofan run-to-failure data (**simulation-based, not field data**).
TRL 4 (public simulation-based dataset, laboratory validation only).

```
pip install -e ".[dev]" && python -m pytest
# data: NASA Prognostics Data Repository, "Turbofan Engine Degradation Simulation Data Set" (not committed)
python research/run_study.py /path/to/CMAPSSData
```
