# Downstream 32-63 -> 16-31 first-pass report

Dataset and scanner mode: `original_n_strict`, using the same 550-trajectory universe as the 64-95 first-pass analysis.

All statements below are observational summaries of this finite scan. They are not mechanism claims or proof claims.

## Counts

- Trajectories in universe: `550`.
- Trajectories entering `32-63`: `545`.
- Trajectories with a first `32-63 -> 16-31` pass: `545`.
- Trajectories entering `32-63` without an observed `32-63 -> 16-31` pass: `0`.

## Dominant first-pass faces

- `INFLOW_FROM_64-95 | k=3 | pre3=1,1,3+`: `538` (0.987) REPORTED_FACE
- `START_IN_LAYER | k=3 | pre3=1,1,3+`: `7` (0.013) LOW_SUPPORT

Top full signatures, including the requested longer windows:

| entry_route | transition_k | pre3 | pre5 | count | share | low_support |
| --- | ---: | --- | --- | ---: | ---: | ---: |
| `INFLOW_FROM_64-95` | `3` | `1,1,3+` | `1,1,1,1,3+` | 538 | 0.987 | 0 |
| `START_IN_LAYER` | `3` | `1,1,3+` | `1,1,1,1,3+` | 7 | 0.013 | 1 |

## Reported face check

- Reported compact face `INFLOW_FROM_64-95 | k=3 | pre3=1,1,3+` appears in `538/545` first passes.
- Share among all first `32-63 -> 16-31` passes: `0.987`.
- In this first-pass scan the reported compact face is dominant, but not exhaustive.

## Link from previous 64-95 class

Previous class totals among downstream pass rows:
- `A_start`: `365`
- `A_inflow`: `104`
- `Other_start`: `66`
- `Other_inflow`: `3`
- `no_64_95_pass`: `0`
- `G0`: `7`

The cross-tab in `downstream32_step4_link_from_64_95_face.csv` flags low-support previous classes and low-support cells. Treat cells below 10 rows as descriptive only.

## Class-level downstream reading

- `A_start` top downstream face: `INFLOW_FROM_64-95 | k=3 | pre3=1,1,3+` = `365/365`
- `A_inflow` top downstream face: `INFLOW_FROM_64-95 | k=3 | pre3=1,1,3+` = `104/104`
- `Other_start` top downstream face: `INFLOW_FROM_64-95 | k=3 | pre3=1,1,3+` = `66/66`
- `Other_inflow` top downstream face: `INFLOW_FROM_64-95 | k=3 | pre3=1,1,3+` = `3/3` LOW_SUPPORT_CLASS
- `G0` top downstream face: `START_IN_LAYER | k=3 | pre3=1,1,3+` = `7/7` LOW_SUPPORT_CLASS

## Clean face versus diffuse surface

- Compact-face count: `2`.
- Full-signature count with local windows: `2`.
- If the compact face is nearly exhaustive while full signatures split by longer local windows, the boundary is clean at route/k/pre3 level but more diffuse at the longer-window level.

## Support caution

- Low-support threshold used here: cells or faces with `count < 10`.
- Low-support cells are kept as observations, not promoted to claims.

## Output files

- `downstream32_step1_first_pass_table.csv`
- `downstream32_step2_signature_counts.csv`
- `downstream32_step3_wait_feature_table.csv`
- `downstream32_step4_link_from_64_95_face.csv`
- `downstream32_step5_postpass_windows.csv`
