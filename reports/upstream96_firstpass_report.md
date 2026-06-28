# Upstream 96-127 -> 64-95 first-pass report

Dataset and scanner mode: `original_n_strict`, using the same 550-trajectory universe as the 64-95 first-pass analysis.

All statements below are observational summaries of this finite scan. They are not mechanism claims or proof claims.

## Counts

- Trajectories in universe: `550`.
- Trajectories entering `96-127`: `107`.
- Trajectories with a first `96-127 -> 64-95` pass: `107`.
- Trajectories entering `96-127` without an observed `96-127 -> 64-95` pass: `0`.

## Dominant first-pass faces

- `START_IN_LAYER | k=1 | pre3=1`: `19` (0.178)
- `START_IN_LAYER | k=2 | pre3=2`: `13` (0.121)
- `START_IN_LAYER | k=2 | pre3=1,2,2`: `8` (0.075) LOW_SUPPORT
- `START_IN_LAYER | k=1 | pre3=1,1,1`: `8` (0.075) LOW_SUPPORT
- `START_IN_LAYER | k=2 | pre3=1,3+,2`: `7` (0.065) LOW_SUPPORT
- `START_IN_LAYER | k=2 | pre3=1,2`: `6` (0.056) LOW_SUPPORT
- `START_IN_LAYER | k=2 | pre3=2,1,2`: `5` (0.047) LOW_SUPPORT
- `START_IN_LAYER | k=2 | pre3=2,2`: `5` (0.047) LOW_SUPPORT
- `START_IN_LAYER | k=1 | pre3=1,1`: `5` (0.047) LOW_SUPPORT
- `START_IN_LAYER | k=4 | pre3=3+`: `5` (0.047) LOW_SUPPORT

Top full signatures, including the requested longer windows:

| entry_route | transition_k | pre3 | pre5 | count | share | low_support |
| --- | ---: | --- | --- | ---: | ---: | ---: |
| `START_IN_LAYER` | `2` | `1,3+,2` | `2,2,1,3+,2` | 4 | 0.037 | 1 |
| `START_IN_LAYER` | `2` | `2,1,2` | `2,1,2` | 3 | 0.028 | 1 |
| `START_IN_LAYER` | `2` | `2` | `2` | 3 | 0.028 | 1 |
| `START_IN_LAYER` | `2` | `1,2,2` | `2,1,1,2,2` | 3 | 0.028 | 1 |
| `START_IN_LAYER` | `2` | `2` | `2` | 2 | 0.019 | 1 |
| `START_IN_LAYER` | `1` | `1,1,1` | `1,1,1` | 2 | 0.019 | 1 |
| `START_IN_LAYER` | `2` | `1,1,2` | `1,1,2` | 2 | 0.019 | 1 |
| `START_IN_LAYER` | `3` | `1,1,3+` | `1,1,3+` | 2 | 0.019 | 1 |
| `START_IN_LAYER` | `2` | `2,2` | `2,2` | 2 | 0.019 | 1 |
| `START_IN_LAYER` | `2` | `2,1,2` | `1,2,1,2` | 2 | 0.019 | 1 |

## A_start analogue check

- `START_IN_LAYER` upstream first passes: `107/107`.
- `START_IN_LAYER & transition_k=1 & pre_k_window_3=1,1,1`: `8/107`.
- Any-route `transition_k=1 & pre_k_window_3=1,1,1`: `8/107`.
- A clean all-1 `START_IN_LAYER` analogue is not supported above the low-support cutoff in this pass-level table.

## Link to later 64-95 -> 32-63 class

Downstream first `64-95 -> 32-63` classes among upstream pass rows:
- `A_start`: `0` (0.000)
- `A_inflow`: `104` (0.972)
- `Other_start`: `0` (0.000)
- `Other_inflow`: `3` (0.028)
- `no_64_95_pass`: `0` (0.000)

The cross-tab in `upstream96_step5_link_to_64_95_face.csv` flags both low-support upstream faces and low-support cells. Treat cells below 10 rows as descriptive only.

## Comparison with the 64-95 all-1 face

- The upstream `96-127 -> 64-95` first pass has `8/107` all-1 rows under `transition_k=1 & pre_k_window_3=1,1,1`.
- The leading upstream faces should be read from the count table rather than projected from the 64-95 A_start definition.
- If the leading rows are not dominated by `k=1/pre111`, this upstream boundary has a different first-pass surface from the 64-95 all-1 face in this scan.

## Support caution

- Low-support threshold used here: cells or faces with `count < 10`.
- The upstream boundary is less suitable as a load-bearing claim when interpretation depends on a single low-count face or a low-count downstream class cell.
- The generated files keep the longer local windows so candidate faces can be inspected without upgrading them into claims.

## Output files

- `upstream96_step1_first_pass_table.csv`
- `upstream96_step2_signature_counts.csv`
- `upstream96_step3_wait_feature_table.csv`
- `upstream96_step4_downstream_to_64_95.csv`
- `upstream96_step5_link_to_64_95_face.csv`
