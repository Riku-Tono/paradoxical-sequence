# Downstream 8-15 -> 4-7 first-pass report

Dataset and scanner mode: `original_n_strict`, using the same 550-trajectory universe as the previous first-pass analyses.

All statements below are observational summaries of this finite scan. They are not mechanism claims or proof claims.

## Counts

- Trajectories in universe: `550`.
- Trajectories entering `8-15`: `550`.
- Trajectories with a first `8-15 -> 4-7` pass: `550`.
- Trajectories entering `8-15` without an observed `8-15 -> 4-7` pass: `0`.

## Dominant first-pass faces

- `INFLOW_FROM_16-31 | k=5 | pre3=1,1,3+`: `545` (0.991)
- `START_IN_LAYER | k=2 | pre3=1,1,2`: `3` (0.005) LOW_SUPPORT
- `START_IN_LAYER | k=2 | pre3=3+,1,2`: `1` (0.002) LOW_SUPPORT
- `INFLOW_FROM_16-31 | k=2 | pre3=3+,1,2`: `1` (0.002) LOW_SUPPORT

Top full signatures, including the requested longer windows:

| entry_route | transition_k | pre3 | pre5 | count | share | low_support |
| --- | ---: | --- | --- | ---: | ---: | ---: |
| `INFLOW_FROM_16-31` | `5` | `1,1,3+` | `3+,3+,1,1,3+` | 545 | 0.991 | 0 |
| `START_IN_LAYER` | `2` | `1,1,2` | `1,1,2` | 1 | 0.002 | 1 |
| `START_IN_LAYER` | `2` | `1,1,2` | `2,1,1,2` | 1 | 0.002 | 1 |
| `START_IN_LAYER` | `2` | `1,1,2` | `1,2,1,1,2` | 1 | 0.002 | 1 |
| `START_IN_LAYER` | `2` | `3+,1,2` | `1,3+,1,2` | 1 | 0.002 | 1 |
| `INFLOW_FROM_16-31` | `2` | `3+,1,2` | `2,1,3+,1,2` | 1 | 0.002 | 1 |

## Boundary shape

- Dominant compact face: `INFLOW_FROM_16-31 | k=5 | pre3=1,1,3+` with `545/550` rows.
- Compact-face count: `4`.
- Full-signature count with local windows: `6`.
- At the compact-face level, this boundary is dominant but not exhaustive in this scan.

## Link from previous 64-95 class

Previous 64-95 class totals among downstream pass rows:
- `A_start`: `365`
- `A_inflow`: `104`
- `Other_start`: `66`
- `Other_inflow`: `3`
- `no_64_95_pass`: `0`
- `G0`: `12`

- `A_start` top downstream face: `INFLOW_FROM_16-31 | k=5 | pre3=1,1,3+` = `365/365`
- `A_inflow` top downstream face: `INFLOW_FROM_16-31 | k=5 | pre3=1,1,3+` = `104/104`
- `Other_start` top downstream face: `INFLOW_FROM_16-31 | k=5 | pre3=1,1,3+` = `66/66`
- `Other_inflow` top downstream face: `INFLOW_FROM_16-31 | k=5 | pre3=1,1,3+` = `3/3` LOW_SUPPORT_SOURCE
- `G0` top downstream face: `INFLOW_FROM_16-31 | k=5 | pre3=1,1,3+` = `7/12`

## Link from previous 32-63 face

Previous 32-63 face totals among downstream pass rows:
- `INFLOW_FROM_64-95 | k=3 | pre3=1,1,3+`: `538`
- `START_IN_LAYER | k=3 | pre3=1,1,3+`: `7`
- `NO_32_63_PASS`: `5`

- Previous `INFLOW_FROM_64-95 | k=3 | pre3=1,1,3+` top downstream face: `INFLOW_FROM_16-31 | k=5 | pre3=1,1,3+` = `538/538`
- Previous `START_IN_LAYER | k=3 | pre3=1,1,3+` top downstream face: `INFLOW_FROM_16-31 | k=5 | pre3=1,1,3+` = `7/7` LOW_SUPPORT_SOURCE
- Previous `NO_32_63_PASS` top downstream face: `START_IN_LAYER | k=2 | pre3=1,1,2` = `3/5` LOW_SUPPORT_SOURCE

## Link from previous 16-31 face

Previous 16-31 face totals among downstream pass rows:
- `INFLOW_FROM_32-63 | k=4 | pre3=2,2,3+`: `545`
- `START_IN_LAYER | k=2 | pre3=2`: `1`
- `NO_16_31_PASS`: `4`

- Previous `INFLOW_FROM_32-63 | k=4 | pre3=2,2,3+` top downstream face: `INFLOW_FROM_16-31 | k=5 | pre3=1,1,3+` = `545/545`
- Previous `START_IN_LAYER | k=2 | pre3=2` top downstream face: `INFLOW_FROM_16-31 | k=2 | pre3=3+,1,2` = `1/1` LOW_SUPPORT_SOURCE
- Previous `NO_16_31_PASS` top downstream face: `START_IN_LAYER | k=2 | pre3=1,1,2` = `3/4` LOW_SUPPORT_SOURCE

## Support caution

- Low-support threshold used here: cells or faces with `count < 10`.
- Low-support cells are kept as observations, not promoted to claims.

## Output files

- `downstream8_step1_first_pass_table.csv`
- `downstream8_step2_signature_counts.csv`
- `downstream8_step3_wait_feature_table.csv`
- `downstream8_step4_link_from_64_95_class.csv`
- `downstream8_step5_link_from_32_63_face.csv`
- `downstream8_step6_link_from_16_31_face.csv`
- `downstream8_step7_postpass_windows.csv`
