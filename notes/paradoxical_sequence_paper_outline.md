# Paradoxical-Sequence Paper — Detailed Outline

**Status:** outline only. This is a build plan for a standalone paradoxical-sequence /
first-pass-boundary paper. It is **not** the finished body text. Each section below states the claims
to include, the tables/figures to use, and the words to avoid.

**Scope rules carried from the reconciliation note:**

- Body covers **only** paradoxical-sequence / first-pass-boundary material.
- finite-block and delta work appear as prior research in a **single background paragraph** (§1), with
  one forward-reference in the conclusion. They are **not** integrated.
- Scanner mode for all numbers: `original_n_strict`. Universe: 550 trajectories.
- **`pass-face all-1`** and **`continuous pre111 maintenance`** are kept strictly separate.
- **`START_IN_LAYER`** keeps its strict definition (the word *begins* in the layer).
- `64-95 -> 32-63` is positioned by **co-location of observable axes**, never by maximal neighbor
  distance.
- Stance throughout: **observational only; not a mechanism; not a proof.**

---

## 1. Proposed title

**Primary:**
> First-Pass Faces and an Observational Boundary-Intersection Map of the `64-95 -> 32-63` Layer

**Alternatives:**
> An Observational Boundary Map Around the `64-95 -> 32-63` First-Pass Face
>
> Where Observable Axes Co-Locate: A Descriptive First-Pass Boundary Scan in Accelerated Collatz Trajectories

---

## 2. Abstract draft (≈180 words)

> We report a finite, descriptive scan of first-pass events across dyadic `remaining_K` boundaries in
> accelerated Collatz trajectories, under the `original_n_strict` scanner over a 550-trajectory
> universe. The analysis is observational: it maps where descriptors co-locate, not why they do.
> Boundaries organize into an observed band ladder running from a diffuse upstream feeder
> (`96-127 -> 64-95`) through a single intersection row (`64-95 -> 32-63`) into merged downstream
> faces and a terminal drop. The intersection row is distinctive not because it shows the largest
> neighbor distance — its summed descriptive distance is in fact below the downstream-neighbor average
> — but because several observable axes co-locate there: an entry-route split, a local all-1 context
> split, and concentrated class separation. We separate two conditions that earlier drafts conflated:
> pass-face all-1, which holds by definition for the A classes, and continuous pre111 maintenance,
> which is strictly lower (0.729 and 0.548). Downstream boundaries reconverge into compact common
> faces. We claim no mechanism, no causal role, and no proof about Collatz.

*Word-count and number checks are listed in §7.*

---

## 3. Section-by-section outline

### §1 — Introduction and stance

**Claims to include**
- The object is a finite, descriptive scan of first-pass events across `remaining_K` boundaries; the
  question is *where* observable descriptors co-locate, not *why*.
- Headline observation, stated up front: `64-95 -> 32-63` is where route, local all-1 pass-face
  context, and class separation co-locate; downstream boundaries reconverge.
- **Single background paragraph** on prior work: the finite-block analysis is the broad
  actual-vs-iid discrepancy layer and the delta analysis is the localization/diagnostic layer; the
  present paper is the boundary / first-pass-face layer and does not integrate them here.
- Explicit stance sentence: observational language only (we observe, we find, is concentrated in, is
  carried by, co-locates with); no causal, mechanistic, or proof claims.

**Tables/figures:** none (prose only).

**Do not use:** `because`, `mechanism`, `proof`, `causes`, `forces`, `imposes downstream fate`,
`sorts` (as a verb the boundary performs). Do not frame the iid/actual difference signal as the thesis
of *this* paper.

---

### §2 — Definitions and scanner mode

**Claims to include (definitions, in order, before any result)**
- Scanner mode `original_n_strict`; universe = 550 trajectories.
- `remaining_K` coordinate and dyadic bins; `pass` vs `stay`; `transition_k`; `pre_k_window_3`
  (`pre111` = `1,1,1`); `entry_route`.
- **`START_IN_LAYER` (strict):** the valuation word *begins* in that `remaining_K` layer. Plain-language
  gloss allowed: "the word begins in the `64-95` layer." The alternative route is
  `INFLOW_FROM_96-127`.
- `first pass` = first `64-95 -> 32-63` pass event; **`first pass` ≠ `first entry`**.
- `compact face` vs `full face`.
- **`pass-face all-1`** (= all-1 at pass): the first pass has `k=1` and `pre3=1,1,1`. True by
  definition for the A classes.
- **`continuous pre111 maintenance`**: after `pre111` first appears, `pre3` stays `1,1,1` at every
  subsequent event through the pass. A strictly different and lower quantity.
- **`1111 present at pass` (pass-event 1111):** whether `1111` is present at the pass; a pass-presence
  judgment, not a maintenance measure.

**Tables/figures:** optional Table D1 (definitions glossary) keyed to the §6 terminology table.

**Do not use:** `first visit` / `first occurrence` / `first entry` as synonyms for `START_IN_LAYER`;
`maintenance` for the by-definition pass-face condition; `strict / continuous maintenance` for the
`1111`-present-at-pass column.

---

### §3 — Observed band ladder

**Claims to include**
- The ladder: diffuse feeder `96-127 -> 64-95` → intersection row `64-95 -> 32-63` → merged downstream
  faces (`32-63 -> 16-31`, `16-31 -> 8-15`, `8-15 -> 4-7`) → terminal drop `4-7 -> 0-1`.
- Dominant compact face and dominant share per boundary (feeder share ≈ 0.178; intersection-row share
  0.678; downstream shares 0.987 / 0.998 / 0.991; terminal 0.991).
- The ladder separates first-pass coverage from representative face counts; labels are observational
  (`feeder`, `intersection row`, `reconvergence/merged`, `terminal drop`).

**Tables/figures:** **Figure 1** = `updated_band_ladder_summary.png` (observed first-pass band ladder
with coverage counts); **Table 1** = compact boundary table from `boundary_differential_report.md`
(boundary | role | dominant face | diversity | class separation | reading).

**Do not use:** `selection`/`sorting` as a claimed action; `mechanism`; `imposes`; any wording that
the ladder is a causal pathway.

---

### §4 — The `64-95 -> 32-63` first-pass face and its classes

**Claims to include**
- Four-class partition of `G1 = 538`: `A_start 365`, `A_inflow 104`, `Other_start 66`,
  `Other_inflow 3`; plus `G0 = 12` never entering `64-95`. Checks: 365+104+66+3 = 538; 538+12 = 550.
- A is a within-layer first-pass face: it coincides with the first pass, never with first entry
  (first entry is almost always a `64-95 -> 64-95` stay).
- `A_start` and `A_inflow` share the same local pass face (`k=1`, `pre3=1,1,1`) and differ only by
  entry route; both are **pass-face all-1 = 1.000 by definition**.
- `Other_start`/`Other_inflow` are the observed non-A complement at the same boundary.
- After the pass, `A_start` and `A_inflow` share a common coarse downstream corridor (top next-3/next-5
  are `32-63 -> 32-63` stays; next boundary face `INFLOW_FROM_64-95 | k=3 | pre3=1,1,3+`).
- Note that the formation table (§7) tabulates only three classes; the 3 `Other_inflow` rows are
  excluded **by scope** (low support), not by discrepancy.

**Tables/figures:** **Table 2** = first-pass face classes (`class | count | first-pass face`).

**Do not use:** `signature` as a mechanism; `near-A failure` for all of `Other_*`; `maintenance` here
(that belongs in §7); any "A forces the downstream corridor" phrasing.

---

### §5 — Boundary differential comparison

**Claims to include**
- The intersection row is **not** singled out by maximal neighbor distance. Quantitatively, the summed
  descriptive distance around `B_sort` is `4.676`, *below* the downstream-neighbor average `5.996`;
  downstream boundaries also show large label changes because `transition_k`, `pre3`, and
  `entry_route` are boundary-specific labels.
- What singles the row out is the **combination** of moderate face diversity with high `64-95` class
  separation. Class-distance is `15.212` at `B_sort` vs `8.000` upstream and `0.000` downstream.
- Sorting-power screen (descriptive association only): the strongest `B_sort` feature is `full_face`,
  MI-like score `1.251`, purity `1.000` — i.e. the full face label aligns with class, an association
  in the first-pass descriptor table, not a mechanism.
- Most diffuse boundary = `96-127 -> 64-95` (compact-face entropy `4.069`, 24 compact faces);
  cleanest merged boundary = `16-31 -> 8-15` (dominant share `0.998`).
- Upstream `96-127 -> 64-95` supplies the route label used later but does **not** uniquely identify the
  later `A_inflow` class; the A/non-A separation is carried at the `64-95 -> 32-63` face itself.

**Required sentences (verbatim):**
> `64-95 -> 32-63` is not identified here as special by maximal neighbor distance alone.
>
> Its distinctive role is the co-location of route split, local all-1/pass-face context, and class
> separation.

**Tables/figures:** **Table 3** = neighbor-contrast summary (`B_sort` 4.676 vs downstream avg 5.996);
**Table 4** = sorting-power screen (`full_face` MI-like 1.251, purity 1.000). Optionally reuse Table 1.

**Do not use:** `maximal neighbor distance` as the reason; `mechanism`; `because`; `proof`; `MI` stated
as causal information transfer (call it "MI-like association score").

---

### §6 — Boundary intersection map

**Claims to include**
- The intersection map is the cleanest summary: `64-95 -> 32-63` has active-axis count `6` and total
  score `12`, the only row scoring across route, k, pre3, all-1 context, class separation, and face
  diversity together.
- Downstream rows score mainly on reconvergence; upstream `96-127 -> 64-95` is diffuse (high face
  diversity) but weak as a standalone A separator (score `3 / 8`).
- State the scoring thresholds (distribution axes 0/1/2 rule; class separation 2 for the `64-95`
  sorting row or distance ≥ 8; reconvergence 2 for downstream merged faces near 0.99 dominant share;
  face diversity 2 for entropy ≥ 2 or ≥ 20 compact faces).

**Required sentence (verbatim):**
> This is an observational intersection map, not a mechanism diagram.

**Tables/figures:** **Figure 2** = `boundary_intersection_heatmap.png` (axis grid, row highlighted);
**Figure 3** = `boundary_intersection_ladder.png` (ladder with active-axis badges); **Table 5** =
`boundary_intersection_axis_scores.csv` reduced to the displayed columns
(`boundary | role | active axes | dominant face | reading`).

**Do not use:** `causal evidence`; `certainty-level evidence`; `imposed downstream fate`; reading the
map as anything beyond co-location of observed descriptors in this scan.

---

### §7 — All-1 formation, pass-face all-1, and continuous maintenance

**Claims to include (the C1 resolution, stated explicitly)**
- **Pass-face all-1 = 1.000 by definition** for `A_start` and `A_inflow` (the first pass *is* `k=1`,
  `pre3=1,1,1`). `pre111`-present-at-pass share is `1.000` for both A classes.
- **Continuous pre111 maintenance is strictly lower:** `A_start` `0.729`, `A_inflow` `0.548`;
  `Other_start` and `Other_inflow` `0.000`. This is a stricter temporal condition, not a contradiction
  of the 1.000 pass-face share.
- Break statistics: for `A_start` the interrupting break is `1,1,2` ×59 (0.596) and `1,1,3+` ×40
  (0.404); for `A_inflow`, `1,1,2` ×29 (0.617) and `1,1,3+` ×18 (0.383).
- Formation reading: median distance from first `111` to pass is `1` event for both A classes, so
  "all-1 at pass" ≈ "111 formed just before the pass."
- **`1111 present at pass` (pass-event 1111):** `A_start` `0.564`, `A_inflow` `0.548`. This column is a
  pass-presence judgment, **not** continuous maintenance, and must be labelled as such.
- Separator reading: among `START_IN_LAYER` rows, `Other_start` mostly never forms `111` (present-share
  `0.121`) — the separator lives at the pass, in the local all-1 context.
- Do not overinterpret the lower continuous-maintenance shares.

**Tables/figures:** **Table 6** = forensic class summary
(`class | count | pre111 present | continuous pre111 maintenance | pass-event 1111 | dominant pass
face`) from `boundary_diff_step6_64_95_forensic_summary.csv` + `all1_formation_class_summary.csv`.

**Do not use:** `maintain 111 to pass 100%`; `maintenance` for the 1.000 pass-face condition;
`strict / continuous maintenance` for the `1111`-present column; `because`; `forces`.

---

### §8 — Limits and stance

**Claims to include**
- Finite, sampled, scanner-defined scan; definitions are operational and `original_n_strict`-dependent.
- Low-support tails (`Other_inflow = 3`, START-route downstream tails, lost-`111` micro-cases) remain
  visible but are not load-bearing.
- No causal, generative, or mechanistic claim; no proof about Collatz; the intersection map is not a
  mechanism diagram.
- Open descriptive questions: why descriptors distribute this way, why low-support tails appear where
  they do, and whether the contrasts persist under larger or differently sampled universes.
- One-sentence forward reference: this layer can later be related to the finite-block and delta layers
  only after its own definitions are stable (no integration here).

**Tables/figures:** none.

**Do not use:** any upgrade of the tables into causal/proof-level statements.

---

## 4. Figure / table plan (consolidated)

| ID | Type | Source artifact | Section | Purpose |
| --- | --- | --- | --- | --- |
| Figure 1 | figure | `updated_band_ladder_summary.png` | §3 | Observed band ladder with first-pass coverage counts |
| Figure 2 | figure | `boundary_intersection_heatmap.png` | §6 | Axis grid; `64-95 -> 32-63` highlighted |
| Figure 3 | figure | `boundary_intersection_ladder.png` | §6 | Ladder with active-axis badges |
| Table 1 | table | `boundary_differential_report.md` (compact boundary table) | §3 (reuse §5) | Per-boundary role / dominant face / diversity / class separation |
| Table 2 | table | Paper-3 first-pass classes / forensic CSV | §4 | Four-class partition with counts |
| Table 3 | table | `boundary_differential_report.md` (neighbor contrast) | §5 | `B_sort` 4.676 vs downstream avg 5.996 |
| Table 4 | table | `boundary_differential_report.md` (sorting power) | §5 | `full_face` MI-like 1.251, purity 1.000 |
| Table 5 | table | `boundary_intersection_axis_scores.csv` | §6 | Axis scores per boundary (display columns) |
| Table 6 | table | `boundary_diff_step6_64_95_forensic_summary.csv` + `all1_formation_class_summary.csv` | §7 | Forensic class summary incl. pass-face all-1, continuous maintenance, pass-event 1111 |

**Figure caption rule:** every caption ends with an observational tag ("Observational summary only" /
"Descriptive scan; not a mechanism diagram").

---

## 5. Claims to keep / claims to avoid

**Keep (with cautious wording)**
1. `64-95 -> 32-63` has a distinctive observational role.
2. That role is the **co-location** of observable axes (route, k, pre3, all-1/pass-face context, class
   separation, face diversity), not maximal neighbor distance.
3. A face = first-pass face defined by route + `k=1` + `pre3=1,1,1`; A coincides with first pass, never
   first entry.
4. `A_start`/`A_inflow` differ only by route and share a common coarse downstream corridor.
5. Downstream boundaries reconverge into compact common faces; upstream is a diffuse feeder.
6. The separator of `A_start` from same-route `Other_start` lives at the pass, in the all-1 context.
7. Pass-face all-1 = 1.000 by definition; continuous pre111 maintenance is lower (0.729 / 0.548).
8. Low-support tails remain visible but not load-bearing.
9. Rozier–Terracol overlay (if retained) is an external benchmark only, appendix-level.

**Avoid (remove or rewrite)**
- the result proves anything about Collatz;
- the boundary causes/sorts, or the all-1 face forces downstream fate;
- `START_IN_LAYER` = first visit / first entry;
- `A_start`/`A_inflow` maintain `pre111` continuously at 100%;
- `64-95 -> 32-63` is special because of largest neighbor distance;
- the boundary is a mechanism / the map is a mechanism diagram;
- the `1111`-present-at-pass column is "strict/continuous maintenance";
- the iid/actual difference signal as the paper's thesis.

Replacement vocabulary: `observed`, `descriptive`, `first-pass descriptor`, `co-location`,
`separation`, `reconvergence`, `low-support tail`, `association (not mechanism)`, `not a proof claim`.

---

## 6. Terminology table

| Canonical term | Definition (operational, scanner-dependent) | Value(s) | Deprecated / forbidden |
| --- | --- | --- | --- |
| `pass-face all-1` (= `all-1 at pass`) | First `64-95 -> 32-63` pass has `transition_k = 1` and `pre_k_window_3 = 1,1,1`. | `A_start` 365/365 = 1.000; `A_inflow` 104/104 = 1.000 | "maintenance" for this condition |
| `continuous pre111 maintenance` | After `pre111` first appears, `pre_k_window_3` stays `1,1,1` at every subsequent event through the pass. | `A_start` 0.729; `A_inflow` 0.548; `Other_start` 0.000; `Other_inflow` 0.000 | reporting this as 1.000 |
| `1111 present at pass` (= `pass-event 1111`) | Whether `1111` is present at the pass event (pass-presence judgment, the `share_maintaining_1111_until_pass` column). | `A_start` 0.564; `A_inflow` 0.548 | "strict / continuous maintenance" for this column |
| `A face` (legacy: "A signature") | First-pass descriptor: `from=64-95`, `to=32-63`, route ∈ {`START_IN_LAYER`, `INFLOW_FROM_96-127`}, `k=1`, `pre3=1,1,1`. | — | "A signature" as a mechanism |
| `A_start` / `A_inflow` | A face with route `START_IN_LAYER` / `INFLOW_FROM_96-127`. | 365 / 104 | "relabelled A_start" |
| `Other_start` / `Other_inflow` | Non-A first pass at the same boundary, by route. | 66 / 3 (low support) | "near-A failure" (for all); load-bearing tail claims |
| `G0` / `G1` | Never enters `64-95` / enters and all eventually pass. | 12 / 538 | "near-A failures" for G0 |
| `START_IN_LAYER` | The valuation word **begins** in that `remaining_K` layer. | — | "first occurrence / first visit / first entry" |
| `face` | Observed descriptor at the first pass event. | — | mechanism / permanent trajectory class |
| `first pass` | First `64-95 -> 32-63` pass event. | — | conflating with "first entry" |
| `co-location` | Several observable axes scoring high on the same boundary row. | `B_sort`: 6 axes / score 12 | "cause" / "imposes downstream fate" |
| `reconvergence` | Downstream rows where major classes share one dominant compact face. | shares ≈ 0.987–0.998 | "sorting mechanism" |
| `low-support tail` | Cells below the support threshold; candidate structure only. | e.g. `Other_inflow`, START tails | "result" |

---

## 7. Unresolved checks before the final draft

1. **Abstract word count and numbers.** Confirm the abstract lands at 150–200 words after edits and
   that every number in it (0.729, 0.548, 4.676, 5.996, 550, counts) matches the source files.
2. **`Other_inflow` scope note.** Confirm the formation table (`all1_formation_class_summary.csv`,
   3-class) excludes `Other_inflow = 3` by scope, and place the one-sentence note in §4 and §7.
3. **`pass-event 1111` labeling.** Verify §7 and the terminology table never call the
   `share_maintaining_1111_until_pass` column (0.564 / 0.548) continuous/strict maintenance.
4. **Sorting-power provenance.** Confirm the `full_face` MI-like score `1.251` and purity `1.000`
   come from `boundary_diff_step4_sorting_power.csv`, and present them as association, not mechanism.
5. **Neighbor-distance provenance.** Confirm the `4.676` vs `5.996` figures (and the
   `B_sort` class-distance `15.212`) trace to `boundary_diff_step3_neighbor_contrasts.csv` /
   `step5_class_distance_by_boundary.csv`.
6. **iid retention decision.** Decide whether any actual−iid background survives as a scoped
   subsection or is dropped; the new authoritative files do not use it.
7. **Rozier–Terracol appendix.** Decide whether to include the external-benchmark overlay; if so, keep
   it appendix-level with the "different notion of paradoxical" caveat and one consistent phrasing.
8. **"Sorting" label hygiene.** Decide on one row label (`intersection row` preferred; `sorting face`
   only as a descriptive name) and ensure no sentence implies the boundary performs sorting.
