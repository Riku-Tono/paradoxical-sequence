# Downstream 16-31 -> 8-15 first-pass report

Dataset and scanner mode: `original_n_strict`, using the same 550-trajectory universe as the previous first-pass analyses.

All statements below are observational summaries of this finite scan. They are not mechanism claims or proof claims.

## Counts

- Trajectories in universe: `550`.
- Trajectories entering `16-31`: `546`.
- Trajectories with a first `16-31 -> 8-15` pass: `546`.
- Trajectories entering `16-31` without an observed `16-31 -> 8-15` pass: `0`.

## Dominant first-pass faces

- `INFLOW_FROM_32-63 | k=4 | pre3=2,2,3+`: `545` (0.998)
- `START_IN_LAYER | k=2 | pre3=2`: `1` (0.002) LOW_SUPPORT

Top full signatures, including the requested longer windows:

| entry_route | transition_k | pre3 | pre5 | count | share | low_support |
| --- | ---: | --- | --- | ---: | ---: | ---: |
| `INFLOW_FROM_32-63` | `4` | `2,2,3+` | `1,3+,2,2,3+` | 545 | 0.998 | 0 |
| `START_IN_LAYER` | `2` | `2` | `2` | 1 | 0.002 | 1 |

## Boundary shape

- Dominant compact face: `INFLOW_FROM_32-63 | k=4 | pre3=2,2,3+` with `545/546` rows.
- `transition_k=3 & pre_k_window_3=1,1,3+` rows: `0/546`.
- Compact-face count: `2`.
- Full-signature count with local windows: `2`.
- At the compact-face level, this boundary is dominant but not exhaustive in this scan.

## Link from previous 64-95 class

Previous 64-95 class totals among downstream pass rows:
- `A_start`: `365`
- `A_inflow`: `104`
- `Other_start`: `66`
- `Other_inflow`: `3`
- `no_64_95_pass`: `0`
- `G0`: `8`

- `A_start` top downstream face: `INFLOW_FROM_32-63 | k=4 | pre3=2,2,3+` = `365/365`
- `A_inflow` top downstream face: `INFLOW_FROM_32-63 | k=4 | pre3=2,2,3+` = `104/104`
- `Other_start` top downstream face: `INFLOW_FROM_32-63 | k=4 | pre3=2,2,3+` = `66/66`
- `Other_inflow` top downstream face: `INFLOW_FROM_32-63 | k=4 | pre3=2,2,3+` = `3/3` LOW_SUPPORT_SOURCE
- `G0` top downstream face: `INFLOW_FROM_32-63 | k=4 | pre3=2,2,3+` = `7/8` LOW_SUPPORT_SOURCE

## Link from previous 32-63 face

Previous 32-63 face totals among downstream pass rows:
- `INFLOW_FROM_64-95 | k=3 | pre3=1,1,3+`: `538`
- `START_IN_LAYER | k=3 | pre3=1,1,3+`: `7`
- `NO_32_63_PASS`: `1`

- Previous `INFLOW_FROM_64-95 | k=3 | pre3=1,1,3+` top downstream face: `INFLOW_FROM_32-63 | k=4 | pre3=2,2,3+` = `538/538`
- Previous `START_IN_LAYER | k=3 | pre3=1,1,3+` top downstream face: `INFLOW_FROM_32-63 | k=4 | pre3=2,2,3+` = `7/7` LOW_SUPPORT_SOURCE
- Previous `NO_32_63_PASS` top downstream face: `START_IN_LAYER | k=2 | pre3=2` = `1/1` LOW_SUPPORT_SOURCE

## Support caution

- Low-support threshold used here: cells or faces with `count < 10`.
- Low-support cells are kept as observations, not promoted to claims.

## Output files

- `downstream16_step1_first_pass_table.csv`
- `downstream16_step2_signature_counts.csv`
- `downstream16_step3_wait_feature_table.csv`
- `downstream16_step4_link_from_64_95_class.csv`
- `downstream16_step5_link_from_32_63_face.csv`
- `downstream16_step6_postpass_windows.csv`
