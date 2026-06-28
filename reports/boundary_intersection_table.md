# Boundary Intersection Table

| Boundary | role | active axes | dominant face | reading |
| --- | --- | --- | --- | --- |
| `96-127 -> 64-95` | diffuse feeder | k split, pre3 split, all-1 context (minor), class separation (minor), face diversity | `START_IN_LAYER | k=1 | pre3=1` | Diffuse upstream surface; not a standalone A separator. |
| `64-95 -> 32-63` | intersection row | route split, k split, pre3 split, all-1 context, class separation, face diversity | `START_IN_LAYER | k=1 | pre3=1,1,1` | Route and all-1/local-context axes intersect with class separation. |
| `32-63 -> 16-31` | reconvergence face | all-1 context (minor), reconvergence | `INFLOW_FROM_64-95 | k=3 | pre3=1,1,3+` | Previously separated classes reconverge into a common downstream face. |
| `16-31 -> 8-15` | clean downstream face | all-1 context (minor), reconvergence | `INFLOW_FROM_32-63 | k=4 | pre3=2,2,3+` | Near-clean downstream continuation with changed k/pre3 face. |
| `8-15 -> 4-7` | downstream face | reconvergence | `INFLOW_FROM_16-31 | k=5 | pre3=1,1,3+` | Downstream continuation with small low-support side branches. |
| `4-7 -> 0-1` | terminal drop | reconvergence | `INFLOW_FROM_8-15 | k=4 | pre3=1,3+,3+` | Terminal direct drop. |
