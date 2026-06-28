# Boundary Intersection Map Report

This is an observational intersection map, not a mechanism diagram.

## Thresholds

- Distribution axes use: 0 when the dominant value is at least 0.98; 1 when only one value has support of at least 10; 2 when multiple values have support of at least 10.
- Class separation uses the class-distance table: 2 for the 64-95 sorting row or total class-distance at least 8; 1 for nonzero but weaker separation.
- Reconvergence is marked 2 on downstream rows where major classes share the dominant compact face.
- Face diversity is marked 2 when compact-face entropy is at least 2 or at least 20 compact faces are present.

## Answers

1. Strongest intersection of active axes: `64-95 -> 32-63`, with active-axis count `6` and total score `12`.
2. `64-95 -> 32-63 is not identified here as special by maximal neighbor distance alone.`
3. `Its distinctive role is the co-location of route split, local all-1/context split, and class separation.`
4. The mainly reconvergent rows are `32-63 -> 16-31`, `16-31 -> 8-15`, and `8-15 -> 4-7`; the terminal row also preserves a near-single direct drop.
5. The diffuse upstream feeder is `96-127 -> 64-95`, where face diversity is high but the later class split is weak as a standalone separator.
6. The terminal row is `4-7 -> 0-1`.
7. Do not read the map as causal evidence, certainty-level evidence, or a diagram of imposed downstream fate. It only marks where observed descriptors co-locate in this scan.

## Outputs

- `boundary_intersection_axis_scores.csv`
- `boundary_intersection_heatmap.png` / `boundary_intersection_heatmap.svg`
- `boundary_intersection_ladder.png` / `boundary_intersection_ladder.svg`
- `boundary_intersection_table.md`
