# Boundary differential report

Dataset/scanner mode: `original_n_strict`. This report compares observed first-pass descriptors across neighboring remaining_K boundaries. It is descriptive only and does not upgrade the tables into causal or proof-level claims.

## Direct answers

1. Most diffuse boundary: `96-127 -> 64-95` by compact-face entropy (`4.069`) and `24` compact faces.
2. Cleanest merged boundary: `16-31 -> 8-15` by dominant compact-face share (`0.998`).
3. `64-95 -> 32-63` stands out observationally because it combines a route split (`START_IN_LAYER` vs `INFLOW_FROM_96-127`) with a local-context split (`pre111` A face vs non-A tails). Its dominant share is not as clean as downstream merged faces, but its class separation is concentrated at the face definition itself.
4. The standout signal is a combination. In the sorting-power screen, the strongest `B_sort` feature is `full_face` with MI-like score `1.251` and purity `1.000`.
5. Major classes diverge most at `B_sort` in the class-distance table and then largely reconverge in downstream compact faces, especially where dominant downstream shares approach 1.
6. Upstream `96-127 -> 64-95` does not uniquely identify the later `A_inflow` class. It supplies the route label used later, but the later `64-95 -> 32-63` face still carries the observed A/non-A separation.
7. What remains unexplained: why these descriptors are distributed this way, why low-support tails appear where they do, and whether the same contrasts persist under larger or differently sampled universes.
8. What should not be claimed: avoid causal language, proof-level language, or statements that the boundary imposes downstream fate. The tables only show observed concentration, separation, and reconvergence in this scan.

## Neighbor contrast reading

The summed descriptive distance around `B_sort` is `4.676` versus downstream-neighbor average `5.996`. By the raw neighboring-distribution L1 distances, no: downstream boundaries also show large label changes because `transition_k`, `pre3`, and `entry_route` are boundary-specific labels. The clearer `B_sort` contrast is not larger raw neighbor distance; it is the combination of moderate face diversity with high 64-95 class separation.

## 64-95 forensic reading

- `A_start`: count `365`, median wait `10.000`, pre111 present share `1.000`, maintains-pre111 share `0.729`.
- `A_inflow`: count `104`, median wait `17.000`, pre111 present share `1.000`, maintains-pre111 share `0.548`.
- `Other_start`: count `66`, median wait `3.000`, pre111 present share `0.121`, maintains-pre111 share `0.000`.
- `Other_inflow`: count `3`, median wait `17.000`, pre111 present share `1.000`, maintains-pre111 share `0.000`.

Within `B_sort`, A_start and A_inflow are exactly the rows where the all-1 local context is present at pass (`k=1`, `pre3=1,1,1`) and the route differs. Other_start and Other_inflow are the observed complement at the same boundary. This is an association in the first-pass descriptor table, not a mechanism statement.

## Compact boundary table

| Boundary | role | dominant face | diversity | class separation | reading |
| --- | --- | --- | ---: | ---: | --- |
| `96-127 -> 64-95` | feeder | `START_IN_LAYER | k=1 | pre3=1` | 4.069 | 8.000 | diffuse upstream surface; route evidence is weak as a standalone separator |
| `64-95 -> 32-63` | sorting face | `START_IN_LAYER | k=1 | pre3=1,1,1` | 1.643 | 15.212 | route plus pre111/local-context split is concentrated here |
| `32-63 -> 16-31` | merged downstream | `INFLOW_FROM_64-95 | k=3 | pre3=1,1,3+` | 0.099 | 0.000 | mostly merged into a common downstream face |
| `16-31 -> 8-15` | merged downstream | `INFLOW_FROM_32-63 | k=4 | pre3=2,2,3+` | 0.019 | 0.000 | near-clean downstream continuation |
| `8-15 -> 4-7` | merged downstream | `INFLOW_FROM_16-31 | k=5 | pre3=1,1,3+` | 0.087 | 0.000 | near-clean downstream continuation with small START tails |
| `4-7 -> 0-1` | terminal drop | `INFLOW_FROM_8-15 | k=4 | pre3=1,3+,3+` | 0.075 | 0.000 | direct terminal drop for most rows |

## Output files

- `boundary_diff_step1_unified_events.csv`
- `boundary_diff_step2_boundary_feature_summary.csv`
- `boundary_diff_step3_neighbor_contrasts.csv`
- `boundary_diff_step4_sorting_power.csv`
- `boundary_diff_step5_class_trajectory_profiles.csv`
- `boundary_diff_step5_class_distance_by_boundary.csv`
- `boundary_diff_step6_64_95_forensic_timeline.csv`
- `boundary_diff_step6_64_95_forensic_summary.csv`
