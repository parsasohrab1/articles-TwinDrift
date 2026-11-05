# TRL assessment – TwinDrift

**Claimed level: TRL 4** (laboratory validation on a public **simulated** dataset). Not TRL 5: no field data, no known drift onset.

Data: NASA C-MAPSS FD001 (100 engines, one operating condition) and FD002 (260 engines, six conditions). Mean over 20 random engine splits. "Lead" = cycles between the first alarm and the end of the engine's series (failure).

| Data | Rule | Threshold | False alarm (cycles 31–60) | Missed | Median lead (cycles) | Alarm at fraction of life |
|---|---|---|---|---|---|---|
| FD001 (34 test engines) | conformal_0.05 | 2.31 | 0.013 | 0.000 | 51 | 0.75 |
| FD001 (34 test engines) | conformal_0.1 | 1.96 | 0.063 | 0.000 | 56 | 0.73 |
| FD001 (34 test engines) | fixed_2 | 2.00 | 0.060 | 0.000 | 55 | 0.73 |
| FD001 (34 test engines) | fixed_3 | 3.00 | 0.003 | 0.000 | 43 | 0.79 |
| FD001 (34 test engines) | fixed_5 | 5.00 | 0.000 | 0.000 | 28 | 0.86 |
| FD002 (88 test engines) | conformal_0.05 | 1.91 | 0.033 | 0.000 | 57 | 0.72 |
| FD002 (88 test engines) | conformal_0.1 | 1.77 | 0.062 | 0.000 | 60 | 0.71 |
| FD002 (88 test engines) | fixed_2 | 2.00 | 0.024 | 0.000 | 56 | 0.73 |
| FD002 (88 test engines) | fixed_3 | 3.00 | 0.000 | 0.000 | 39 | 0.80 |
| FD002 (88 test engines) | fixed_5 | 5.00 | 0.000 | 0.000 | 22 | 0.89 |

## Findings and caveats
- Alarms come at roughly 70–75 % of engine life (lead of about 50–60 cycles) with the conformal 0.05/0.1 thresholds and no engine missed.
- The conformal threshold controls the false-alarm rate conservatively (FD001: 0.013 at alpha = 0.05; FD002: 0.033), but a fixed threshold of 3 gives no false alarm either, with a shorter lead (39–43 cycles). The calibrated rule buys about 10–20 more cycles of lead for a few percent false alarms; it is not a large advantage.
- **The false-alarm definition is weak.** C-MAPSS has no ground-truth drift onset: any alarm after cycle 60 is counted as a detection, even if it were early. "False alarm" means only an alarm in the cycles 31–60 that were used to calibrate the threshold.
- The twin is a simple standardised-residual reference, not a physics model; no claim that it explains the degradation.
- All data are simulated by NASA's turbofan model; results do not transfer to measured assets.
