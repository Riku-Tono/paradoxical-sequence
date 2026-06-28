# First-Pass Faces and an Observational Boundary-Intersection Map of the `64-95 -> 32-63` Layer

**Status: draft for review. Observational / descriptive paper. Not a finished, camera-ready
manuscript — see §8 for open items.**

**Scanner mode for all reported numbers:** `original_n_strict`. **Universe:** 550 sampled accelerated
Collatz trajectories.

---

## Abstract

We report a finite, descriptive scan of first-pass events across dyadic `remaining_K` boundaries in
accelerated Collatz trajectories, under the `original_n_strict` scanner over a 550-trajectory
universe. The analysis is observational: it maps where descriptors co-locate, not why they do.
Boundaries organize into an observed band ladder running from a diffuse upstream feeder
(`96-127 -> 64-95`) through a single intersection row (`64-95 -> 32-63`) into merged downstream faces
and a terminal drop. The intersection row is distinctive not because it shows the largest neighbor
distance — its summed descriptive distance is in fact below the downstream-neighbor average — but
because several observable axes co-locate there: an entry-route split, a local all-1 pass-face
context, and concentrated class separation among `A_start`, `A_inflow`, `Other_start`, and
`Other_inflow`. We separate two conditions that earlier drafts conflated: **pass-face all-1**, which
holds by definition for the A classes, and **continuous pre111 maintenance**, which is strictly lower
(0.729 and 0.548). Downstream boundaries reconverge into compact common faces. We claim no mechanism,
no causal role, and no proof about the Collatz conjecture.

*(171 words)*

---

## 1. Introduction and stance

This paper reports a finite, descriptive scan of **first-pass events** across `remaining_K` boundaries
in accelerated Collatz trajectories. The question we ask throughout is *where* observable descriptors
co-locate, not *why* they do. We make no claim about mechanism, cause, or proof.

The headline observation, stated up front and developed in the sections that follow: the
`64-95 -> 32-63` boundary is where an entry-route split, a local all-1 pass-face context, and class
separation among four first-pass classes (`A_start`, `A_inflow`, `Other_start`, `Other_inflow`)
co-locate. Boundaries downstream of it mostly reconverge into a small number of compact faces.

**Relation to prior work.** This paper is part of a larger Collatz-trajectory research program that
also includes a broad actual-vs-iid finite-block discrepancy analysis and a separate
localization/diagnostic ("delta") analysis identifying *where on the `remaining_K` axis* an
actual-vs-surrogate difference signal concentrates. Both of those analyses exist as their own chapters
and are not reproduced or re-derived here; we use them only to motivate the present zoom-in (the delta
analysis is what originally pointed at the `64-95` band as the most readable region). The present
paper takes that localization as a starting point and asks a narrower, purely descriptive question
about first-pass structure *within and around* the `64-95 -> 32-63` boundary. No claim from the
finite-block or delta chapters is imported into this paper, and no claim made here is asserted to hold
for those chapters; reconnecting the three is left to later work (§8).

**Stance.** We restrict ourselves to observational language throughout: *we observe*, *we find*, *is
concentrated in*, *is carried by*, *co-locates with*, *is consistent with*. We do not use *because*,
*mechanism*, *causes*, *forces*, or *proof* **as affirmative explanatory claims** — that is, we never
assert that a boundary or face *is* a mechanism, *causes* a downstream outcome, or *proves* something
about Collatz. (We do use these terms in their negated form, e.g. "not a mechanism," "no causal role,"
as limitation statements; that usage is explicitly permitted and recurs throughout this paper.) We do
not claim that any boundary "sorts" trajectories as an action it performs. We use **"intersection
row"** as the reader-facing label for the observed pattern at `64-95 -> 32-63` throughout this paper;
"sorting face" / "sorting row" survive only as legacy or internal-analysis labels (e.g. the table
column `B_sort`) and are not used as the paper's own descriptive claim. Low-support cells are flagged
and treated as candidate structure, not as load-bearing claims.

**Figures/tables:** none in this section.

---

## 2. Definitions and scanner mode

All quantities below are defined operationally and are specific to the `original_n_strict` scanner
mode over the 550-trajectory universe. Definitions are stated here, in full, before any result is
reported.

**2.1 Coordinate.** For an odd integer trajectory under the accelerated Collatz map,

$$
x_{t+1} = \frac{3x_t + 1}{2^{k_t}}, \qquad k_t = v_2(3x_t + 1),
$$

with valuation word $w = (k_0, k_1, \ldots, k_{\tau-1})$ and total valuation mass
$K_\tau = \sum_{t=0}^{\tau-1} k_t$. The reported coordinate is the remaining mass before step $t$,

$$
R_t = K_\tau - \sum_{i<t} k_i .
$$

**2.2 `remaining_K` bins.** Half-open dyadic intervals. A transition $A \to B$ occurs at position $t$
when $R_t \in A$ and $R_{t+1} \in B$. The bins used in this paper, narrowest to widest in the active
range: `0-1`, `4-7`, `8-15`, `16-31`, `32-63`, `64-95`, `96-127`.

**2.3 `pass` vs. `stay`.** For a target transition from bin $A$ to bin $B$, an occurrence starting in
$A$ is a **pass** if its post-step bin is $B$, and a **stay** if its post-step bin is still $A$.

**2.4 `transition_k` and `pre_k_window_3`.** `transition_k` is the valuation step $k_t$ at the
transition occurrence; exact tests use `transition_k = 1` to mean $k_t = 1$ exactly.
`pre_k_window_3` $= (k_{t-2}, k_{t-1}, k_t)$. We write **`pre111`** for `pre_k_window_3 = 1,1,1`.

**2.5 `entry_route` and `START_IN_LAYER` (strict).** For a given `remaining_K` bin, let $s$ be the
first position whose pre-step `remaining_K` value lies in that bin. An occurrence at position $t$ in
that bin has entry route **`START_IN_LAYER`** if $s = 0$ — that is, **the valuation word begins
inside that `remaining_K` layer** — and otherwise `INFLOW_FROM_<previous bin>`.

> **Definition note (must not be weakened).** `START_IN_LAYER` means the word *begins* in the layer.
> It does **not** mean "first observed visit to the layer," "first occurrence in the layer," or "first
> entry into the layer." A plain-language gloss, where needed, is: *"the word begins in the `64-95`
> layer."* The alternative entry route used throughout this paper is `INFLOW_FROM_96-127`.

**2.6 `first pass`.** The first occurrence of a `64-95 -> 32-63` pass event for a given trajectory.
**`first pass` is not the same as `first entry`** into the `64-95` layer; see §4 for the empirical
relationship between the two.

**2.7 `compact face` vs. `full face`.** A *full face* is the full joint descriptor
(`entry_route`, `transition_k`, `pre_k_window_3`, …) observed at an occurrence. A *compact face* is a
coarser, capped summary used for tabulation (values above 2 reported as `3+`).

**2.8 `pass-face all-1` (= `all-1 at pass`).** The first `64-95 -> 32-63` pass has `transition_k = 1`
and `pre_k_window_3 = 1,1,1` (i.e. `pre111`). This condition is evaluated **at the pass event only**.

**2.9 `continuous pre111 maintenance`.** After `pre111` first appears within the window from first
`64-95` entry to first pass, `pre_k_window_3` remains `1,1,1` at **every** subsequent event through the
pass. This is a stricter, temporal condition, and is **numerically distinct** from §2.8.

**2.10 `1111 present at pass` (= `pass-event 1111`).** Whether the length-4 all-1 run `1111` is present
at the pass event. This is a **pass-presence judgment**, exactly analogous to §2.8 but at length 4, and
is **not** a maintenance measure.

> **Terminology lock (the central definitional decision of this paper).** §2.8, §2.9, and §2.10 name
> three different quantities. We never use the word *maintenance* for §2.8 or §2.10. We reserve
> *maintenance* exclusively for §2.9. Conflating these — in particular, reporting the by-definition
> `1.000` share of §2.8 as if it were the continuous share of §2.9 — is the single terminology error
> this paper is written to avoid; see §7.

**Tables/figures:** none required; an optional definitions glossary (Table D1) may be added keyed to
the terminology table in §9.

---

## 3. Observed band ladder

Across the sampled universe, first-pass coverage organizes into an observed band ladder running from
upstream to the terminal bins:

$$
96\text{-}127 \to 64\text{-}95 \to 32\text{-}63 \to 16\text{-}31 \to 8\text{-}15 \to 4\text{-}7 \to 0\text{-}1 .
$$

Table 1 gives the per-boundary role, dominant compact face, and dominant share. Roles are
**observational labels for the pattern found, not claims about a mechanism**: `feeder` describes a
diffuse upstream surface; `intersection row` describes the boundary where multiple axes co-locate
(§5–§6); `merged downstream face` / `terminal drop` describe rows that converge onto one dominant
compact face.

**Table 1. Observed compact boundary table.** *(Source: `boundary_differential_report.md`, compact
boundary table; cf. `boundary_intersection_table.md`.)*

| Boundary | Role | Dominant compact face | Dominant share | Face diversity (entropy) | Class separation |
| --- | --- | ---: | ---: | ---: | ---: |
| `96-127 -> 64-95` | feeder | `START_IN_LAYER \| k=1 \| pre3=1` | 0.178 | 4.069 | 8.000 |
| `64-95 -> 32-63` | intersection row | `START_IN_LAYER \| k=1 \| pre3=1,1,1` | 0.678 | 1.643 | 15.212 |
| `32-63 -> 16-31` | reconvergence / merged downstream | `INFLOW_FROM_64-95 \| k=3 \| pre3=1,1,3+` | 0.987 | 0.099 | 0.000 |
| `16-31 -> 8-15` | merged downstream (cleanest) | `INFLOW_FROM_32-63 \| k=4 \| pre3=2,2,3+` | 0.998 | 0.019 | 0.000 |
| `8-15 -> 4-7` | merged downstream | `INFLOW_FROM_16-31 \| k=5 \| pre3=1,1,3+` | 0.991 | 0.087 | 0.000 |
| `4-7 -> 0-1` | terminal drop | `INFLOW_FROM_8-15 \| k=4 \| pre3=1,3+,3+` | 0.991 | 0.075 | 0.000 |

Two observations follow directly from Table 1, stated descriptively:

- The feeder `96-127 -> 64-95` has the highest face diversity (entropy `4.069`) and the lowest
  dominant-face share (`0.178`) of any row — it is diffuse, not concentrated on one face.
- The intersection row `64-95 -> 32-63` has the lowest face diversity of the upper boundaries
  (`1.643`) together with the highest class separation in the table (`15.212`) — i.e. relatively few
  faces, but those faces line up closely with class identity. We do not yet say *why* this co-occurs
  (§5–§6 develop the reading).
- All three downstream merged rows and the terminal row have dominant shares ≥ 0.987 and class
  separation `0.000`: previously separated classes are observed to converge onto a shared compact face
  after the pass (§4).

**Figure 1 — Observed first-pass band ladder.** *Source: `updated band ladder summary.png` (actual
filename contains spaces; rename to `updated_band_ladder_summary.png` for the final manuscript if a
hyphen/underscore convention is required).* Shows,
per boundary, first-pass coverage counts (e.g. `64-95 -> 32-63`: `538/538`) separately from
representative compact-face counts, plus low-support tails at each row (e.g. `32-63 -> 16-31`: `7/545`
on the non-dominant side). **Caption tag: "Observed first-pass band ladder. Descriptive summary only;
not a mechanism diagram."**

**Do not use in this section:** `selection` or `sorting` as an action the ladder performs;
`mechanism`; `imposes`; any phrasing suggesting the ladder is a causal pathway rather than an
observed sequence of boundaries.

---

## 4. The `64-95 -> 32-63` first-pass face and its classes

**4.1 Entry partition.** Of the 550-trajectory universe, 12 trajectories never enter the `64-95` layer
(`G0`); the remaining 538 do enter it (`G1`), and every `G1` trajectory eventually performs a
`64-95 -> 32-63` pass.

**4.2 First pass vs. first entry.** The first event inside the `64-95` layer is almost always a
`64-95 -> 64-95` stay, not a pass; no trajectory's first-entry event is an A face (§4.3). Among
trajectories that ever satisfy the A face, it coincides with the **first** `64-95 -> 32-63` pass in
every observed case. We therefore describe the A face as a **within-layer first-pass face**: it is
defined at, and observed to coincide with, the first pass — never with first entry.

**4.3 Four-class partition of `G1`.** Classifying each `G1` trajectory by its first-pass descriptor
gives four classes that partition the 538 trajectories (Table 2). We use **A face** (not "A
signature") for the joint condition `from = 64-95`, `to = 32-63`, `transition_k = 1`,
`pre_k_window_3 = 1,1,1` (i.e. pass-face all-1, §2.8), observed under one of two entry routes.

**Table 2. First-pass face classes (`G1 = 538`).**

| Class | Count | Share of `G1` | Entry route | First-pass face | Pass-face all-1 |
| --- | ---: | ---: | --- | --- | ---: |
| `A_start` | 365 | 0.678 | `START_IN_LAYER` | `k=1`, `pre3=1,1,1` | 1.000 (by definition) |
| `A_inflow` | 104 | 0.193 | `INFLOW_FROM_96-127` | `k=1`, `pre3=1,1,1` | 1.000 (by definition) |
| `Other_start` | 66 | 0.123 | `START_IN_LAYER` | not A face | — |
| `Other_inflow` | 3 | 0.006 | `INFLOW_FROM_96-127` | not A face | — |

Checks: $365+104+66+3 = 538$; $538+12 = 550$.

`A_start` and `A_inflow` share the same local pass face (`k=1`, `pre3=1,1,1`) and differ **only** by
entry route. `Other_start` and `Other_inflow` are the observed non-A complement at the same boundary,
by route. We do not describe any of `Other_start`/`Other_inflow` collectively as "near-A failures";
within `Other_start`, the leading deformations keep `START_IN_LAYER` and often `k=1` but break the
all-1 pre-window (cf. Figure 2, "Other_start breakdown" panel).

**4.4 Shared downstream corridor.** After the first pass, `A_start` and `A_inflow` are observed to
follow a common coarse downstream path: their top next-3 and next-5 transition sequences are
predominantly `32-63 -> 32-63` stays, and the next boundary's dominant face is the same for both,
`INFLOW_FROM_64-95 | k=3 | pre3=1,1,3+` (cf. Table 1, row 3). We describe this as a shared downstream
**corridor**, an observed coarse-path similarity, not a claim that the pass-face *causes* the
downstream path.

**4.5 Scope footnote on `Other_inflow`.** > *`Other_inflow = 3` is part of the `G1 = 538` first-pass
> partition reported here and in the forensic summary (Table 6). It is, by contrast, excluded from the
> three-class all-1 formation table (`all1_formation_class_summary.csv`, §7) **by scope**, because it
> is a low-support cell (3 trajectories). This is an intentional scoping choice in that table, not a
> count discrepancy: $365 + 104 + 66 = 535$ rows are tabulated there against the $538$ in `G1`.*

**Figure 2 — `64-95` chamber / first-pass face taxonomy.** *Source: conceptual figures
("The Band Labyrinth of 64-95"; "From Δ-localization to the 64-95 chamber" / "Taxonomy of First-Pass
Faces"), redrawn for this paper.* **Editorial note:** these source figures use the legacy label "A
signature"; the redrawn version for this paper must relabel every occurrence as **A face** (and,
where the by-definition pass condition is shown, as **pass-face all-1**), consistent with §2.8 and the
terminology table (§9). Panels to retain: (i) entry of `A_start`/`A_inflow`/`Other_start`/
`Other_inflow` into the `64-95` chamber by route; (ii) the first-pass decision point; (iii) the
`Other_start` breakdown into "never reaches 111" vs. "reaches 111 but cannot maintain it" (the latter
panel is the natural home for the lost-`111` micro-cases referenced in §7); (iv) the observed counts
table (365/104/66/3, 538 total). **Caption tag: "Observational classification of first-pass faces; no
mechanism or causality claimed."**

**Do not use in this section:** `signature` as if it denoted a mechanism; `near-A failure` applied to
all of `Other_start`/`Other_inflow`; `maintenance` (reserved for §7); any phrasing that the A face
*forces* or *determines* the downstream corridor.

---

## 5. Boundary differential comparison

**5.1 Not a maximal-neighbor-distance claim.** The intersection row (`64-95 -> 32-63`) is **not**
singled out by raw neighbor distance. The summed descriptive distance around it is `4.676`, which is
*below* the downstream-neighbor average of `5.996` (Table 3, where it is listed under its internal
analysis label `B_sort`). Downstream boundaries show large raw label changes for an uninteresting
reason: `transition_k`, `pre3`, and `entry_route` are boundary-specific labels, so neighboring
boundaries differ in their labels almost by construction.

> **Required statement (verbatim).** `64-95 -> 32-63` is not identified here as special by maximal
> neighbor distance alone.

**5.2 What does single it out: a combination.** What distinguishes the intersection row
(`64-95 -> 32-63`) is the **combination** of moderate face diversity (`1.643`, Table 1) with high
class separation specifically among the four first-pass classes. Table 4 decomposes the class-distance
total (`15.212`) at this boundary by class pair: `A_start` vs `A_inflow` contributes `4.000` (driven by
`compact_face_l1` and `entry_route_l1`, since the two classes differ only by route); `A_start` vs
`Other_start` contributes `4.606`; `A_inflow` vs `Other_start` contributes `6.606` (the largest single
pair, combining a route difference with the all-1/non-all-1 split). At the upstream feeder
(`96-127 -> 64-95`), the *same* class-pair decomposition sums to only `8.000` overall, and is driven
almost entirely by the `A_inflow` vs. others contrast (`A_start` vs. `Other_start` is `0.000` there);
downstream of `64-95 -> 32-63`, all class-pair distances are `0.000` (Table 1).

> **Required statement (verbatim).** Its distinctive role is the co-location of route split, local
> all-1/pass-face context, and class separation.

**5.3 Feature-association screen (association, not mechanism).** A descriptive feature screen over the
`64-95 -> 32-63` occurrence table (internally, the "sorting-power" screen over boundary `B_sort`) finds
that the feature most strongly associated with class identity is `full_face`, with an MI-like
association score of `1.251` and purity `1.000`. We read this as: the full joint first-pass descriptor
aligns with class membership almost exactly, which is close to a restatement of how the classes were
defined (§4.3) rather than a new discovery; we report it as an **association in the descriptor
table**, not as evidence of a causal or generative mechanism, and not as evidence that the boundary
performs any sorting action.

**5.4 Other boundary-level extremes.** The most diffuse boundary by face-diversity is the feeder
`96-127 -> 64-95` (entropy `4.069`, `24` compact faces); the cleanest merged boundary is
`16-31 -> 8-15` (dominant share `0.998`). The upstream feeder supplies the route label
(`START_IN_LAYER` vs. `INFLOW_FROM_96-127`) used at `64-95 -> 32-63`, but it does **not** by itself
uniquely identify the later `A_inflow` class; the A/non-A separation is carried at the
`64-95 -> 32-63` face itself (cf. Table 4, where the upstream feeder's `A_start`-vs-`Other_start`
distance is `0.000`).

**Table 3. Neighbor-contrast summary.**

| Quantity | Value |
| --- | ---: |
| Summed descriptive distance, `64-95 -> 32-63` neighbors (internal label `B_sort`) | 4.676 |
| Downstream-neighbor average descriptive distance | 5.996 |
| Class-distance total at `64-95 -> 32-63` (`B_sort`) | 15.212 |
| Class-distance total at upstream feeder `96-127 -> 64-95` (`B_up`) | 8.000 |
| Class-distance total, all downstream rows | 0.000 |

**Table 4. Class-pair decomposition of class distance at `B_sort` (and `B_up` for contrast).**
*(Source: `boundary_diff_step5_class_distance_by_boundary.csv`.)*

| Boundary | Class pair | `compact_face_l1` | `transition_k_l1` | `pre3_l1` | `entry_route_l1` | Row total |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `B_sort` | `A_start` vs `A_inflow` | 2.0 | 0.0 | 0.0 | 2.0 | 4.000 |
| `B_sort` | `A_start` vs `Other_start` | 2.0 | 0.606 | 2.0 | 0.0 | 4.606 |
| `B_sort` | `A_inflow` vs `Other_start` | 2.0 | 0.606 | 2.0 | 2.0 | 6.606 |
| `B_up` | `A_start` vs `A_inflow` | 1.0 | 1.0 | 1.0 | 1.0 | 4.000 |
| `B_up` | `A_start` vs `Other_start` | 0.0 | 0.0 | 0.0 | 0.0 | 0.000 |
| `B_up` | `A_inflow` vs `Other_start` | 1.0 | 1.0 | 1.0 | 1.0 | 4.000 |

**Figure 3 — Boundary differential comparison.** A small-multiple or bar-chart rendering of Table 3
and Table 4: (i) the `64-95 -> 32-63` boundary vs. downstream-average neighbor distance, visually
showing `4.676 < 5.996`; (ii) class-distance total by boundary, with `64-95 -> 32-63` (`15.212`) the
clear maximum and downstream rows flat at `0.000`. **Caption tag: "Descriptive comparison of
neighboring boundaries; not evidence of a causal mechanism."**

**Do not use in this section:** `maximal neighbor distance` as the reason for the `64-95 -> 32-63`
boundary's status; `mechanism`; `because` in a causal sense; `proof`; "MI" stated as if it measured
causal information transfer (call it an "MI-like association score"); "sorting" as an action the
boundary performs (`B_sort`/`sorting-power` survive only as internal analysis labels, not as
reader-facing claims).

---

## 6. Boundary intersection map

**6.1 Thresholds.** The intersection map scores six observable axes (route split, k split, pre3 split,
all-1 context, class separation, face diversity) per boundary on a 0/1/2 scale: distribution axes use
0 if the dominant value's share is ≥ 0.98, 1 if only one non-dominant value has support ≥ 10, 2 if
multiple values have support ≥ 10; class separation is 2 for the `64-95` row or total class-distance
≥ 8, 1 for nonzero but weaker separation; reconvergence is 2 on downstream rows where major classes
share the dominant compact face; face diversity is 2 when compact-face entropy ≥ 2 or ≥ 20 compact
faces are present.

**6.2 Result.** `64-95 -> 32-63` has the strongest intersection of active axes in the table: active-
axis count `6` and total score `12` — the only row that scores on **all** of route split, k split,
pre3 split, all-1 context, class separation, and face diversity simultaneously (Table 5; Figure 4).
Downstream rows score mainly, and in several cases solely, on reconvergence. The upstream feeder
`96-127 -> 64-95` is diffuse (high face diversity) but scores only `3/8` overall, and is explicitly
weak as a standalone separator of the later A/non-A classes (cf. §5.4, Table 4).

> **Required statement (verbatim).** This is an observational intersection map, not a mechanism
> diagram.

**Table 5. Boundary intersection axis scores (display columns).** *(Source:
`boundary_intersection_axis_scores.csv`, `boundary_intersection_table.md`.)*

| Boundary | Role | Active axes (score 2) | Active-axis count | Total score | Dominant face |
| --- | --- | --- | ---: | ---: | --- |
| `96-127 -> 64-95` | diffuse feeder | k split, pre3 split, face diversity | 3 | 8 | `START_IN_LAYER \| k=1 \| pre3=1` |
| `64-95 -> 32-63` | intersection row | route split, k split, pre3 split, all-1 context, class separation, face diversity | 6 | 12 | `START_IN_LAYER \| k=1 \| pre3=1,1,1` |
| `32-63 -> 16-31` | reconvergence face | reconvergence | 1 | 3 | `INFLOW_FROM_64-95 \| k=3 \| pre3=1,1,3+` |
| `16-31 -> 8-15` | clean downstream face | reconvergence | 1 | 3 | `INFLOW_FROM_32-63 \| k=4 \| pre3=2,2,3+` |
| `8-15 -> 4-7` | downstream face | reconvergence | 1 | 2 | `INFLOW_FROM_16-31 \| k=5 \| pre3=1,1,3+` |
| `4-7 -> 0-1` | terminal drop | reconvergence | 1 | 2 | `INFLOW_FROM_8-15 \| k=4 \| pre3=1,3+,3+` |

**Figure 4 — Boundary intersection heatmap.** *Source: `boundary_intersection_heatmap.png`.* Axis grid
(rows = boundaries, columns = the six observable axes), `64-95 -> 32-63` row highlighted as the only
full-intensity row. **Caption tag: "Observable-axis grid; observational summary, not a mechanism
diagram."**

**Figure 5 — Boundary intersection ladder.** *Source: `boundary_intersection_ladder.png`.* The band
ladder of Figure 1, re-annotated with active-axis badges per boundary; `64-95 -> 32-63` shown with all
six badges active. **Caption tag: "Ladder with active-axis badges; observational summary only."**

**Do not use in this section:** `causal evidence`; `certainty-level evidence`; `imposed downstream
fate`; any reading of the map beyond marking where observed descriptors co-locate in this scan.

---

## 7. All-1 formation, pass-face all-1, and continuous maintenance

This section states the central terminology resolution of the paper explicitly and gives the
supporting numbers.

**7.1 Pass-face all-1 is true by definition.** For `A_start` and `A_inflow`, pass-face all-1 (§2.8) is
`1.000` because it is how the classes are defined: the first pass *is* `k=1`, `pre3=1,1,1`. This is a
**pass-event** quantity (§2.8) and is distinct from Table 6's "pre111 ever appears before pass" column,
which instead reports whether `pre111` is reached **anywhere in the entry-to-pass window**, not
necessarily at the pass itself (Table 6 below; source field `share_first_pre111_present`).

**7.2 Continuous pre111 maintenance is strictly lower.** Once `pre111` first appears within the
entry-to-pass window, whether it is held at **every** subsequent event through the pass is a different
and strictly harder condition. The observed shares are `A_start = 0.729`, `A_inflow = 0.548`,
`Other_start = 0.000`, `Other_inflow = 0.000` (Table 6). This is **not a contradiction** of §7.1 — it
is a different, stricter, temporal quantity, and the two must never be reported as the same number.

**7.3 Break statistics.** Where continuous maintenance fails for `A_start`/`A_inflow`, the
interrupting break is one of two kinds: `pre3` goes to `1,1,2` or to `1,1,3+`. For `A_start`: `1,1,2`
in 59 cases (0.596 of breaks), `1,1,3+` in 40 (0.404). For `A_inflow`: `1,1,2` in 29 (0.617), `1,1,3+`
in 18 (0.383). In both classes, the same final step is the one perturbed; the run interrupts rather
than collapses.

**7.4 Formation timing.** Across the all-1 formation analysis (`all1_formation_class_summary.csv`),
the median distance from the first appearance of `111` to the pass is `1` event for both `A_start` and
`A_inflow` — that is, the first `111` often appears close to the pass, rather than early in the
entry-to-pass window.

**7.5 `1111 present at pass` is a separate, third quantity.** The class-summary column
`share_maintaining_1111_until_pass` reports `A_start = 0.564`, `A_inflow = 0.548`. Despite its column
name, this is a **pass-presence judgment** — whether the length-4 run `1111` is present *at* the pass
— directly analogous to §7.1 but one digit longer, and is **not** a continuous/strict maintenance
measure (§2.10). It must be reported as "1111 present at pass" or "pass-event 1111," never as "strict"
or "continuous" maintenance, and must be kept visually and verbally distinct from §7.2's `0.729/0.548`.

**7.6 Where the separator lives.** Among `START_IN_LAYER` rows, `Other_start` mostly never reaches
`111` before the pass at all (share with `pre111` ever appearing before pass = `0.121`, Table 6) — only
a small subset (8 of 66) reach it and then lose it (the lost-`111` micro-cases; cf. Figure 2's
"Other_start breakdown" panel).
The observational reading is therefore: the separator between `A_start` and same-route `Other_start`
lives **at the pass**, in the local all-1 context, not in some earlier formation event.

**7.7 Scope note (repeated from §4.5).** The forensic summary (Table 6) reports four classes including
`Other_inflow = 3`; the all-1 formation class summary tabulates only the three larger classes
(`A_start`, `A_inflow`, `Other_start`), excluding `Other_inflow` **by scope** (low support), not
because of any count discrepancy.

**Table 6. Forensic class summary — pass-face all-1, continuous maintenance, and pass-event 1111.**
*(Sources: `boundary_diff_step6_64_95_forensic_summary.csv`; `all1_formation_class_summary.csv`. The
`1111 present at pass` and median-distance-to-pass columns are populated only for the three classes in
scope there; see §7.7.)*

| Class | Count | Median wait (events) | Pass-face all-1 (by def.) | `pre111` ever appears before pass | **Continuous pre111 maintenance** | `1111` present at pass | Dominant pass face |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `A_start` | 365 | 10.0 | 1.000 | 1.000 | **0.729** | 0.564 | `START_IN_LAYER \| k=1 \| pre3=1,1,1` (1.000) |
| `A_inflow` | 104 | 17.0 | 1.000 | 1.000 | **0.548** | 0.548 | `INFLOW_FROM_96-127 \| k=1 \| pre3=1,1,1` (1.000) |
| `Other_start` | 66 | 3.0 | — | 0.121 | **0.000** | — (not A face) | heterogeneous; leading `k=1 \| pre3=3+,1,1` (0.424) |
| `Other_inflow` | 3 | 17.0 | — | 1.000 | **0.000** | not tabulated (out of scope, §7.7) | low support |

**Table 6 note.** The "`pre111` ever appears before pass" column reports whether `pre111` is reached
**anywhere in the entry-to-pass window**, not whether it is present *at* the pass; it is a different
quantity from "pass-face all-1" (§2.8) and from "`1111` present at pass" (§2.10). `Other_inflow`'s
share of `1.000` on this column means `pre111` was reached at some point before the pass for all 3
rows — it does **not** imply that `Other_inflow` satisfies the A face or has pre111 at the pass itself;
by definition, `Other_inflow` is precisely the non-A complement at this boundary (Table 2), and its
continuous-maintenance share is `0.000` regardless.

**Figure 6 — Pass-face all-1 vs. continuous maintenance.** A paired bar chart, scoped to the two A
classes only (`A_start`, `A_inflow`): one bar for "pass-face all-1 (by definition) = 1.000" and a
second, visually distinct bar for "continuous pre111 maintenance," to make the §7.2 gap (0.729 / 0.548)
immediately visible rather than stated only in prose. `Other_start` and `Other_inflow` must **not** be
drawn as zero-height bars on the "pass-face all-1" axis — a zero bar would misleadingly read as "this
was measured and found to be 0," when in fact the quantity is undefined for non-A classes. Instead,
mark `Other_start`/`Other_inflow` on that axis as **"not A face / not applicable"** (e.g. a hatched
placeholder, an "n/a" label, or an explicit omission with a one-line note below the chart), and show
their continuous-pre111-maintenance bars (both `0.000`, which *is* a measured value) on the second axis
as normal bars. **Caption tag: "Two distinct quantities; not to be conflated. Pass-face all-1 is
undefined, not zero, for non-A classes. Observational summary only."**

**Do not use in this section:** "maintain 111 to pass 100%" or any equivalent collapsing of §7.1 into
§7.2; `maintenance` for the by-definition pass-face condition; `strict`/`continuous` for the
`1111`-present-at-pass column; `because`; `forces`; any overinterpretation of the lower
continuous-maintenance shares as evidence against the pass-face classification.

---

## 8. Limits and outlook

**Scope and sampling.** The analysis universe is a sampled, scanner-defined ensemble of 550
accelerated Collatz trajectories under `original_n_strict`, not an exhaustive enumeration of integers.
All shares, counts, and distances reported here are within-sample quantities tied to that scanner
mode; a different mode (e.g. `odd_core`, `odd_only`) would shift counts, though we do not re-derive
that dependence in this paper.

**Descriptive scope.** Every claim in this paper is a concentration, co-location, separation, or
reconvergence statement about observed descriptors. None is a causal, generative, or mechanistic claim,
and none is a proof or disproof of any statement about the Collatz conjecture. The boundary
intersection map (§6) marks where descriptors co-locate in this scan; it is not a mechanism diagram.

**Low-support tails.** Several cells remain visible in the tables above but are explicitly **not
load-bearing**: `Other_inflow` (3 of 538), the small START-route tails on downstream boundaries (e.g.
7/545 at `32-63 -> 16-31`), and the lost-`111` micro-cases within `Other_start` (8 of 66). These are
candidate structure, not claims.

**Open descriptive questions.** This paper does not explain *why* descriptors are distributed the way
Table 1, 4, and 5 show; *why* low-support tails appear where they do; or whether the same contrasts
would persist under a larger or differently sampled universe. These are left open.

**Relation to the finite-block and delta chapters.** As stated in §1, this paper does not integrate
with, or import claims from, the finite-block (broad actual-vs-iid discrepancy) or delta
(localization/diagnostic) chapters. A later piece of work may connect the three — for instance, asking
whether the `64-95 -> 32-63` intersection-row pattern found here is itself a finer-grained view of the
difference signal the delta chapter localizes to the `64-95` band — but that connection is **not**
attempted here, and no claim in this paper should be read as already making it.

**Figures/tables:** none.

**Do not use in this section:** any upgrade of the limitations above into a stronger claim than
stated; any closing sentence that reads as a Collatz-conjecture conclusion.

---

## 9. Terminology table (for reference; carried from the reconciliation note)

| Canonical term | Definition | Value(s) | Forbidden usage |
| --- | --- | --- | --- |
| `pass-face all-1` (= `all-1 at pass`) | First `64-95 -> 32-63` pass has `transition_k=1`, `pre_k_window_3=1,1,1`. | `A_start` 1.000; `A_inflow` 1.000 (both by definition) | calling this "maintenance" |
| `continuous pre111 maintenance` | After `pre111` first appears, `pre_k_window_3` stays `1,1,1` at every event through the pass. | `A_start` 0.729; `A_inflow` 0.548; `Other_start`/`Other_inflow` 0.000 | reporting this as 1.000 |
| `1111 present at pass` (= `pass-event 1111`) | Whether `1111` is present at the pass event. | `A_start` 0.564; `A_inflow` 0.548 | calling this "strict" or "continuous" maintenance |
| `pre111 ever appears before pass` (source field: `share_first_pre111_present`) | Whether `pre111` is reached **anywhere** in the entry-to-pass window (formation, not pass-event presence). | `A_start` 1.000; `A_inflow` 1.000; `Other_start` 0.121; `Other_inflow` 1.000 | calling this "pre111 present at pass"; reading `Other_inflow`'s 1.000 here as A-face membership |
| `A face` (legacy: "A signature") | First-pass descriptor: `from=64-95`, `to=32-63`, `transition_k=1`, `pre3=1,1,1`, either entry route. | — | using "signature" as a mechanism |
| `A_start` / `A_inflow` | A face with route `START_IN_LAYER` / `INFLOW_FROM_96-127`. | 365 / 104 | "relabelled A_start" for `A_inflow` |
| `Other_start` / `Other_inflow` | Non-A first pass at the same boundary, by route. | 66 / 3 (low support) | "near-A failure" applied to all rows |
| `START_IN_LAYER` | The valuation word **begins** in that `remaining_K` layer. | — | "first occurrence / first visit / first entry" |
| `first pass` | First `64-95 -> 32-63` pass event. | — | conflating with "first entry" |
| `co-location` | Multiple observable axes scoring high on the same boundary row. | `64-95 -> 32-63`: 6 axes, score 12 | "cause," "imposes downstream fate" |
| `reconvergence` | Downstream rows where major classes share the dominant compact face. | shares ≈ 0.987–0.998 | "sorting mechanism" |
| `low-support tail` | Cells below the support threshold; candidate structure only. | e.g. `Other_inflow`, START-route downstream tails | "result" |

---

## 10. Open items before this draft is final

1. Figures 1–6 above are specified by source/content/caption tag but not yet rendered as final
   image files for this manuscript; Figures 2, 4, and 5 reuse or redraw existing source images
   (`updated band ladder summary.png` — note the actual filename uses spaces, not underscores —
   `boundary_intersection_heatmap.png`, `boundary_intersection_ladder.png`, and the two "Band
   Labyrinth" / "Δ-localization → chamber" conceptual figures), and **Figure 2's source images must
   be relabeled** from "A signature" to "A face" / "pass-face all-1" before inclusion (§4). Figures 3
   and 6 are newly specified here and have no existing source image.
2. Confirm whether any actual-vs-iid background material is retained as a scoped paragraph anywhere
   in the paper; this draft contains none beyond the one background sentence in §1.
3. Confirm whether a Rozier–Terracol external-benchmark appendix is wanted; this draft does not include
   one, per the reconciliation note's "appendix-level only" guidance and the instruction to keep this
   paper limited to the paradoxical-sequence material.
4. Numeric audit pass: re-verify every number in this draft (counts, shares, distances) directly
   against the seven evidence files before this moves from draft to final.
