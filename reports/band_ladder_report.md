# Band ladder summary

Dataset and scanner mode: `original_n_strict`. This report integrates existing CSV/report outputs only; it does not rescan trajectories.

All statements are observational summaries of this finite scan. They are not mechanism claims or proof claims.

## Main Summary

| band_transition | entered | first_pass | dominant_compact_face | dominant_share | role |
| --- | ---: | ---: | --- | ---: | --- |
| `96-127 -> 64-95` | 107 | 107 | `START_IN_LAYER | k=1 | pre3=1` | 0.178 | upstream diffuse feeder |
| `64-95 -> 32-63` | 538 | 538 | `START_IN_LAYER | k=1 | pre3=1,1,1` | 0.678 | main sorting face |
| `32-63 -> 16-31` | 545 | 545 | `INFLOW_FROM_64-95 | k=3 | pre3=1,1,3+` | 0.987 | merged downstream face |
| `16-31 -> 8-15` | 546 | 546 | `INFLOW_FROM_32-63 | k=4 | pre3=2,2,3+` | 0.998 | merged downstream face |
| `8-15 -> 4-7` | 550 | 550 | `INFLOW_FROM_16-31 | k=5 | pre3=1,1,3+` | 0.991 | merged downstream face |
| `4-7 -> 2-3` | 550 | 0 | `none` | NA | absent transition |
| `4-7 -> 0-1` | 550 | 545 | `4-7 -> 0-1` | 1.000 | terminal direct drop |

## Answers

1. The main split is at `64-95 -> 32-63`: this is where the named A_start / A_inflow / Other_start / Other_inflow classes are defined. The upstream `96-127 -> 64-95` surface is more diffuse.
2. The merged downstream faces are `32-63 -> 16-31`, `16-31 -> 8-15`, and the main part of `8-15 -> 4-7`. A_start, A_inflow, and Other_start stay merged across these rows in the observed tables.
3. The k/pre3 face changes by band: `64-95 -> 32-63` is led by k=1/pre111, `32-63 -> 16-31` by k=3/pre113+, `16-31 -> 8-15` by k=4/pre223+, and `8-15 -> 4-7` by k=5/pre113+.
4. The ladder terminates at the first `4-7` entry in this scan: the requested `4-7 -> 2-3` transition is absent, while `545/550` rows go directly `4-7 -> 0-1`.
5. A compact descriptive name would be `observed first-pass band ladder`: a main sorting face at `64-95 -> 32-63`, followed by merged downstream faces and a terminal direct drop.

## Support Notes

- Low-support threshold used in source analyses: count < 10.
- G0 remains the small, least stable group: it partly merges downstream but also carries the low-support side outcomes near the bottom of the ladder.
- Empty link tables for `4-7 -> 2-3` reflect an absent target transition, not a failed calculation.

## Output Files

- `band_ladder_summary.csv`
- `band_ladder_class_propagation.csv`
- `band_ladder_summary.png`
