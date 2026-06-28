# Downstream 4-7 -> 2-3 first-pass report

Dataset and scanner mode: `original_n_strict`, using the same 550-trajectory universe as the previous first-pass analyses.

All statements below are observational summaries of this finite scan. They are not mechanism claims or proof claims.

## Counts

- Trajectories in universe: `550`.
- Trajectories entering `4-7`: `550`.
- Trajectories with a first `4-7 -> 2-3` pass: `0`.
- Trajectories entering `4-7` without an observed `4-7 -> 2-3` pass: `550`.

## Dominant first-pass faces

- No `4-7 -> 2-3` pass was observed, so no first-pass face is defined for this target.

Top full signatures, including the requested longer windows:

| entry_route | transition_k | pre3 | pre5 | count | share | low_support |
| --- | ---: | --- | --- | ---: | ---: | ---: |

## Boundary shape

- Dominant compact face: `` with `0/0` rows.
- Compact-face count: `0`.
- Full-signature count with local windows: `0`.
- The requested boundary is not observed in this scan; this is a zero-pass result rather than a clean/diffuse face result.

## First 4-7 entry check

Because the target pass is absent, the first `4-7` entry transition is informative:
- `4-7 -> 0-1`: `545/550`
- `4-7 -> 4-7`: `5/550`

First `4-7` entry transition_k counts:
- `k=4`: `545/550`
- `k=3`: `5/550`

## Link from previous 64-95 class

Previous 64-95 class totals among downstream pass rows:
- `A_start`: `0`
- `A_inflow`: `0`
- `Other_start`: `0`
- `Other_inflow`: `0`
- `no_64_95_pass`: `0`
- `G0`: `0`


## Link from previous 8-15 face

Previous 8-15 face totals among downstream pass rows:
- `INFLOW_FROM_16-31 | k=5 | pre3=1,1,3+`: `0`
- `START_IN_LAYER | k=2 | pre3=1,1,2`: `0`
- `START_IN_LAYER | k=2 | pre3=3+,1,2`: `0`
- `INFLOW_FROM_16-31 | k=2 | pre3=3+,1,2`: `0`
- `NO_8_15_PASS`: `0`


## Support caution

- Low-support threshold used here: cells or faces with `count < 10`.
- Low-support cells are kept as observations, not promoted to claims.

## Output files

- `downstream4_step1_first_pass_table.csv`
- `downstream4_step2_signature_counts.csv`
- `downstream4_step3_wait_feature_table.csv`
- `downstream4_step4_link_from_64_95_class.csv`
- `downstream4_step5_link_from_32_63_face.csv`
- `downstream4_step6_link_from_16_31_face.csv`
- `downstream4_step7_link_from_8_15_face.csv`
- `downstream4_step8_postpass_windows.csv`
