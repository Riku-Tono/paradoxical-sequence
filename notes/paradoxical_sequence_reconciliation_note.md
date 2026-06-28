# Paradoxical-Sequence Reconciliation Note

**Purpose.** Reconcile only the paradoxical-sequence / first-pass-boundary material, including the
latest boundary-differential and boundary-intersection results, so that the chapter is internally
consistent before any final rewrite. This is a planning note, **not** the chapter itself: it audits
definition conflicts, fixes terminology, lists claims to keep / rewrite / remove, and proposes a
section outline.

**Hard scope rule.** Do **not** merge this with the finite-block or delta chapters in this pass. The
older `Δ-localization` companion and the actual-vs-iid finite-block discrepancy work are referenced
here only where they explain a conflict; they are not integrated. A bridge stub is reserved for later
(see §11).

**Scanner mode for all reconciled numbers:** `original_n_strict`. Universe: 550 trajectories.

---

## 1. Source inventory and provenance status

The sources fall into three tiers. Tier weight matters because the old drafts and the new result
files disagree on framing, and the new files win.

### 1a. Old drafts — *audit only, do not preserve wholesale*

| File | What it is | How to treat it |
| --- | --- | --- |
| `band_signatures1.html` | "Paper 2 — Band signatures" (actual−iid difference paper; introduces the **A signature**, mass-deficit/conditional-excess framing, Rozier–Terracol Appendix A) | Historical source. Audit definitions; do not carry its iid-first framing into the new backbone unscoped. |
| `band_signature_first_pass_paper2.html` | "Paper 3 — First-pass signature" (introduces `A_start` / `A_inflow` / `Other_start`, the 538/12 partition, the formation-vs-maintenance reading) | Closest in structure to the new chapter, **but** contains the central `maintenance` wording conflict (§2, C1). Audit, do not preserve its maintenance claim verbatim. |
| `band_signature_first_pass_paper3.html` | Variant/comparison copy of the first-pass paper | Optional comparison only. |

### 1b. New result files — *current authoritative summaries*

- `boundary_intersection_map_report.md`
- `boundary_intersection_table.md`
- `boundary_intersection_axis_scores.csv`
- `boundary_diff_step6_64_95_forensic_summary.csv`  ← decisive for the maintenance fix
- `all1_formation_report.md` and `all1_formation_class_summary.csv`
- (boundary differential report — referenced by the plan; reconciled here from the intersection/forensic outputs)

### 1c. Figures — *use only after definitions are stable*

- `boundary_intersection_heatmap.png` (observable-axis grid; `64-95 -> 32-63` highlighted)
- `boundary_intersection_ladder.png` (ladder with active-axis badges)
- `updated_band_ladder_summary.png` (observed first-pass band ladder with coverage counts)

---

## 2. Definition-conflict audit

Seven conflicts. C1 and C2 are load-bearing; the rest are clean-ups.

### C1 — `maintenance` is overloaded (THE central conflict)

The same dataset reports **two different numbers** for "maintains 111 to the pass," computed under two
different definitions, and the old drafts collapse them into one claim.

- **Loose version (present at pass).** `all1_formation_class_summary.csv` →
  `share_maintaining_111_until_pass = 1.000` for both `A_start` and `A_inflow`. The
  `all1_formation_report.md` repeats this as "maintain-111-to-pass share `1.000`." Old draft Paper 3
  §7 states it in prose: *"all maintain it to the pass."*
- **Strict version (continuous).** `boundary_diff_step6_64_95_forensic_summary.csv` →
  `share_maintains_pre111_to_pass = 0.729` (`A_start`) and `0.548` (`A_inflow`).

Both numbers are correct under their own definition. The loose one is true **by construction**: an A
row is defined to have `k=1` and `pre3=1,1,1` *at the pass*, so it is all-1 at the pass with
probability 1. The strict one asks the harder temporal question — does `pre3` stay `1,1,1` at *every*
event from the first appearance of `pre111` through the pass — and there the share drops to
`0.729 / 0.548`.

**Resolution (non-negotiable):**

- Reserve the word **`maintenance`** for the strict continuous condition only.
- Use **`pass-face all-1`** / **`all-1 at pass`** for the `1.000`-by-definition condition.
- Forbid any sentence of the form "A_start and A_inflow maintain 111 to the pass 100%."

This is compatible: A rows are all-1 *at* the pass by definition; they do not all hold `pre111`
*continuously* from its first appearance. The break statistics confirm the gap is real, not noise —
for `A_start` the interrupting break is `1,1,2` in 59 cases (0.596) and `1,1,3+` in 40 (0.404); for
`A_inflow`, `1,1,2` ×29 (0.617) and `1,1,3+` ×18 (0.383).

### C2 — framing: actual−iid difference apparatus vs descriptive intersection map

The old drafts are built end-to-end on the **actual−iid** contrast: `mass delta`, `conditional
delta`, `pass share`, and "paradoxical configuration" defined as `mass delta < 0 AND conditional
delta > 0`. The **new authoritative results carry none of that machinery.** The boundary-intersection
and forensic outputs are purely **descriptive** — observed first-pass coverage, observed compact
faces, observed axis co-location — with no surrogate ensemble.

**Resolution:** the new chapter's backbone is the **observational intersection map**, not the
difference-signal decomposition. The iid contrast may survive as a clearly-scoped background
subsection or appendix *if* the author wants it, but it must not be the primary thesis and must not
leak mechanism/causal language. Use the plan's required sentence verbatim:

> This is an observational intersection map, not a mechanism diagram.

### C3 — `A signature` (occurrence-level) vs `A face` (first-pass descriptor)

Old drafts call the joint condition the **"A signature"** and treat it as an occurrence-level test
(Paper 2 §4.7). The new framing treats `face` as a **first-pass descriptor** — the observed
descriptor at the first pass event, not a mechanism and not a permanent class of the whole trajectory.

**Resolution:** prefer **`A face`**, **`A_start`**, **`A_inflow`**, **`pass-face`**. "A signature" may
appear once, parenthetically, as the legacy name. Do not let "signature" imply a generative cause.

### C4 — trajectory-level A vs first-pass A

Paper 2's Appendix A states the A overlap is a *"trajectory-level event"* and that under a
"first-`64-95`-occurrence-only" definition the overlap is `0`. Read carelessly this contradicts the
first-pass framing. Paper 3 §4 resolves it: A never appears at the first *entry* event (that is almost
always a `64-95 -> 64-95` stay), but among all 365 trajectories that satisfy A, it coincides with the
first `64-95 -> 32-63` **pass** in every case (`first_A_index = first_pass_index`).

**Resolution:** state explicitly that **first pass ≠ first entry**. A is a *within-layer first-pass*
face. Drop or rewrite any phrasing that calls A merely a "trajectory-level event," which invites the
first-entry misreading.

### C5 — `START_IN_LAYER` strictness (already compliant — lock it)

Both old drafts already define `START_IN_LAYER` strictly: *"the word begins inside that
`remaining_K` layer … it does not mean the first occurrence / first arrival."* The plan requires the
same strict reading.

**Resolution:** no change needed, but **lock it** — forbid any future rewrite that turns it into
"first occurrence / first visit / first entry." Approved plain-language gloss: *"the word begins in
the `64-95` layer."*

### C6 — selection rationale for the `64-95 -> 32-63` row

Old Paper 2 justifies focusing on this row via the iid quantities (negative `mass delta`, positive
`conditional delta`, adequate support; and it correctly notes the conditional excess is numerically
*largest* at `96-127 -> 64-95` but low-support). The new boundary-differential / intersection result
re-bases the justification on **co-location of observable axes**, not any single extremum.

**Resolution:** adopt the descriptive rationale. Required sentences:

> `64-95 -> 32-63` is not identified here as special by maximal neighbor distance alone.
>
> Its distinctive role is the co-location of route split, local all-1/pass-face context, and class
> separation.

Axis evidence: `boundary_intersection_axis_scores.csv` gives `64-95 -> 32-63` (`B_sort`) an
`active_axis_count = 6` and `axis_score_total = 12` — the only row scoring on route, k, pre3, all-1
context, class separation, and face diversity together. The upstream feeder `96-127 -> 64-95`
(`B_up`) scores `3 / 8` (diffuse, weak as a standalone A separator); all downstream rows score `1` or
`2`, driven almost entirely by reconvergence.

### C7 — `Other_inflow` count hygiene

`Other_inflow = 3` appears in Paper 3 Table 3, in `boundary_diff_step6_64_95_forensic_summary.csv`,
and in the band-ladder figure. It is **absent** from `all1_formation_report.md`'s "Verified counts"
list and from `all1_formation_class_summary.csv` (3 rows only). The formation report's verified
counts therefore sum to `365 + 104 + 66 = 535`, with the 3 `Other_inflow` rows implicit in `G1 = 538`.

**Resolution:** carry the four-class partition (`A_start 365 / A_inflow 104 / Other_start 66 /
Other_inflow 3 = 538`) consistently in the chapter, and add one sentence noting that the formation
analysis tabulates only the three larger classes (the 3 `Other_inflow` rows are low-support).

---

## 3. Revised terminology table

| Canonical term | Definition (operational, scanner-dependent) | Value(s) in this dataset | Deprecated / forbidden |
| --- | --- | --- | --- |
| `pass-face all-1` (= `all-1 at pass`) | First `64-95 -> 32-63` pass has `transition_k = 1` and `pre_k_window_3 = 1,1,1`. | `A_start` 365/365 = 1.000; `A_inflow` 104/104 = 1.000 | "maintenance" for this condition |
| `continuous pre111 maintenance` | After `pre111` first appears in the entry-to-pass window, `pre_k_window_3` stays `1,1,1` at every subsequent event through the pass. | `A_start` 0.729; `A_inflow` 0.548; `Other_start` 0.000; `Other_inflow` 0.000 | reporting this as 1.000 |
| `1111 present at pass` (= `pass-event 1111`) | Whether `pre_k_window_4`/run is `1111` at the pass event (pass-presence judgment, the `share_maintaining_1111_until_pass` column). | `A_start` 0.564; `A_inflow` 0.548 | "strict / continuous maintenance" for this column |
| `A face` (legacy: "A signature") | First-pass descriptor: `from=64-95`, `to=32-63`, route ∈ {`START_IN_LAYER`, `INFLOW_FROM_96-127`}, `k=1`, `pre3=1,1,1`. | — | "A signature" used as a mechanism |
| `A_start` | A face with `entry_route = START_IN_LAYER`. | 365 | — |
| `A_inflow` | A face with `entry_route = INFLOW_FROM_96-127`. | 104 | "relabelled A_start" |
| `Other_start` | `START_IN_LAYER` first pass that is not `A_start`. | 66 | "near-A failure" (for all of them) |
| `Other_inflow` | `INFLOW_FROM_96-127` first pass that is not `A_inflow`. | 3 (low support) | load-bearing claims |
| `G0` | Never enters `64-95`. | 12 | "near-A failures" |
| `G1` | Enters `64-95`; all eventually pass to `32-63`. | 538 | — |
| `START_IN_LAYER` | The valuation word **begins** in that `remaining_K` layer. | — | "first occurrence / first visit / first entry" |
| `face` | Observed descriptor at the first pass event. | — | mechanism / permanent trajectory class |
| `first pass` | First `64-95 -> 32-63` pass event. | — | conflating with "first entry" |
| `co-location` | Several observable axes scoring high on the same boundary row. | `B_sort`: 6 axes / score 12 | "cause" / "imposes downstream fate" |
| `reconvergence` | Downstream rows where major classes share one dominant compact face. | shares ≈ 0.987–0.998 | "sorting mechanism" |
| `low-support tail` | Cells below the support threshold; candidate structure only. | e.g. `Other_inflow`, START tails 1–7/≈545 | "result" |

---

## 4. Counts — single source of truth

Use these exact numbers. They agree across Paper 3, the forensic CSV, and the ladder figure. The
formation table is the one deliberate exception: `all1_formation_class_summary.csv` is a **three-class
table** (`A_start`, `A_inflow`, `Other_start` only) and **excludes the low-support `Other_inflow = 3`
by design / by scope**, so its rows sum to `535` rather than `538`. This is an intended scope choice,
not a count discrepancy.

```
Total universe ........................ 550
  G0  never enters 64-95 .............. 12
  G1  enters 64-95 (all eventually pass) 538
        A_start  (START_IN_LAYER) ..... 365
        A_inflow (INFLOW_FROM_96-127) .. 104
        Other_start (START, not A) ..... 66
        Other_inflow (INFLOW, not A) .... 3
        check: 365+104+66+3 = 538 ✓ ; 538+12 = 550 ✓
```

Supporting forensic numbers (`original_n_strict`):

| Class | count | first pre111 present | continuous maintenance | dominant pass face |
| --- | --- | --- | --- | --- |
| `A_start` | 365 | 1.000 | **0.729** | `START_IN_LAYER \| k=1 \| pre3=1,1,1` (1.000) |
| `A_inflow` | 104 | 1.000 | **0.548** | `INFLOW_FROM_96-127 \| k=1 \| pre3=1,1,1` (1.000) |
| `Other_start` | 66 | 0.121 | 0.000 | heterogeneous; leading `k=1 \| pre3=3+,1,1` (0.424) |
| `Other_inflow` | 3 | 1.000 | 0.000 | low support |

Formation detail (from `all1_formation_class_summary.csv`): median distance from first `111` to pass
is `1` event for both A classes (so "all-1 at pass" ≈ "111 formed just before the pass"); `1111` is
reached by 0.655 (`A_start`) / 0.712 (`A_inflow`) and is **present at the pass** (pass-event `1111`)
for 0.564 (`A_start`) / 0.548 (`A_inflow`). Note: `share_maintaining_1111_until_pass` is a
**pass-presence** judgment (is `1111` present at the pass), **not** a continuous-maintenance measure,
and must not be labelled as such.

---

## 5. Claims to KEEP (with cautious wording)

1. The `64-95 -> 32-63` first-pass boundary has a distinctive **observational** role.
2. Its role is the **co-location** of several observable axes (route split, k, pre3, all-1/pass-face
   context, class separation, face diversity), **not** maximal neighbor distance alone.
3. The A face is a **first-pass face** defined by route + `k=1` + `pre3=1,1,1`.
4. A is a **within-layer first-pass** face: it coincides with the first pass, never with first entry.
5. `A_start` and `A_inflow` share the same local pass face and differ only by entry route; after the
   pass they share a common coarse downstream corridor (top next-3/next-5 are `32-63 -> 32-63` stays;
   next boundary face `INFLOW_FROM_64-95 | k=3 | pre3=1,1,3+`).
6. Downstream boundaries are mostly **merged / clean continuation faces** (dominant shares
   ≈ 0.987–0.998); the terminal row is a near-single direct drop.
7. The upstream `96-127 -> 64-95` boundary is **diffuse and feeder-like** (high face diversity, weak
   as a standalone A separator).
8. The separator of `A_start` from same-route `Other_start` lives **at the pass**, in the local
   all-1 context: `Other_start` mostly never forms `111` (58/66) with a small lose-it subset (8/66).
9. Low-support tails (`Other_inflow = 3`, START-route downstream tails, the 8 lost-`111` cases)
   remain visible but **not load-bearing**.
10. The Rozier–Terracol Appendix A overlay is an **external benchmark only** (different notion of
    "paradoxical") and stays in an appendix, not the main spine.

## 6. Claims to REWRITE

| Old wording (drafts / formation report) | Rewrite to |
| --- | --- |
| "A_start and A_inflow maintain 111 to the pass 100%" / "maintain-111-to-pass share 1.000" | "A_start and A_inflow are all-1 at the pass by definition. Under the stricter continuous-maintenance definition, the shares are lower: 0.729 (A_start) and 0.548 (A_inflow)." |
| "the A signature" (as the primary object) | "the A face" / "A_start" / "A_inflow"; mention "A signature" once as the legacy name. |
| Paper 2 framing of the row's importance via `mass delta`/`conditional delta` extrema | "co-location of route split, local all-1/pass-face context, and class separation." |
| "trajectory-level event" / "A overlap is 0 at first occurrence" (without context) | "A coincides with the first pass, not first entry; first pass ≠ first entry." |
| The mass-deficit / conditional-excess "paradoxical configuration" as the chapter thesis | Reframe as descriptive background only (scoped subsection/appendix), not the spine. |
| Any "the distinction is … its maintenance" sentence that uses the loose 1.000 maintenance | Keep the *formation-vs-maintenance* insight, but state it with the strict shares (0.729 / 0.548) and the break statistics. |

## 7. Claims to REMOVE

Remove any sentence that says or implies:

- the result **proves** anything about Collatz;
- the boundary **causes** sorting, or the all-1 face **forces** downstream fate;
- `START_IN_LAYER` means first observed visit / first entry to the layer;
- `A_start` / `A_inflow` maintain `pre111` continuously at 100%;
- `64-95 -> 32-63` is special because it has the **largest neighbor distance**;
- the boundary is a **mechanism** or the intersection map is a mechanism diagram;
- the iid surrogate establishes a generative cause.

Replacement vocabulary: `observed`, `descriptive`, `first-pass descriptor`, `co-location`,
`separation`, `reconvergence`, `low-support tail`, `not a mechanism claim`, `not a proof claim`.

---

## 8. Proposed chapter outline

Working title: **"First-Pass Faces in the `64-95 -> 32-63` Boundary"**
(alt: "An Observational Boundary Map Around the `64-95 -> 32-63` First-Pass Face").

Abstract thesis: a finite, descriptive scan of first-pass events across `remaining_K` boundaries;
`64-95 -> 32-63` is where route, local all-1 pass-face context, and class separation co-locate;
downstream boundaries reconverge into compact common faces; no mechanism claimed.

| § | Section | Content | Feeds from |
| --- | --- | --- | --- |
| 1 | Definitions & scanner mode | `original_n_strict`; 550 universe; `remaining_K` bins; pass/stay; first pass; entry route; `START_IN_LAYER` (strict); compact vs full face; **`pass-face all-1`** and **`continuous pre111 maintenance`** defined separately. Must precede all results. | §3 here; Paper 2 §4 (audited) |
| 2 | Band ladder | Feeder → intersection/sorting row → merged downstream faces → terminal drop, all observational. | ladder figure; intersection table |
| 3 | The `64-95 -> 32-63` first-pass face | Define `A_start` / `A_inflow` / `Other_start` / `Other_inflow` / `G0`; carry the §4 counts; state pass-face all-1 = 1.000 by definition. | §4 here; forensic CSV |
| 4 | Boundary differential comparison | Diffuse upstream feeder; row is singled out by axis co-location, not raw neighbor distance. | boundary-differential result; C6 sentences |
| 5 | Boundary intersection map | Heatmap + badge ladder + axis-score table; show co-location at `B_sort`, downstream reconvergence, upstream diffuseness. "Observational intersection map, not a mechanism diagram." | `boundary_intersection_*`; axis_scores.csv |
| 6 | All-1 formation & continuous maintenance | Resolve C1 explicitly: 1.000 pass-face all-1 vs 0.729/0.548 continuous; break statistics; do not overinterpret the lower shares. | `all1_formation_*`; forensic CSV |
| 7 | Limits | Finite scan; descriptive only; low-support tails; no causal/mechanism/proof claim; operational scanner-dependent definitions. | §7 here |
| 8 | Bridge stub to finite-block & delta | One short paragraph only; do **not** integrate. | §11 here |

---

## 9. Open consistency items to verify before final write

1. **`Other_inflow` in the formation tables.** Confirm whether the 3 rows were excluded by design or
   merged; reflect the chosen explanation in §3 and §6 (currently flagged as low-support).
2. **`maintain-1111` / `share_maintaining_1111_until_pass` figures.** `all1_formation_report.md`
   cites `A_start` = 0.564; the class summary gives 0.564 (`A_start`) / 0.548 (`A_inflow`). These are
   **"1111 present at pass" (pass-event `1111`)** judgments — whether `1111` is present at the pass —
   **not** strict / continuous maintenance. Label them accordingly and keep them clearly distinct
   from the `continuous pre111 maintenance` numbers (0.729 / 0.548) in the forensic CSV.
3. **iid material retention decision.** Decide explicitly whether any actual−iid content survives as
   a scoped background subsection or is dropped entirely. The new authoritative files do not use it.
4. **Rozier–Terracol appendix.** The two drafts give slightly different overlay phrasings; pick one,
   keep it appendix-level, and retain the "different notion of paradoxical" caveat.

---

## 10. Mandatory conclusions (must appear, verbatim where marked)

- `64-95 -> 32-63` is not identified here as special by maximal neighbor distance alone.
- Its distinctive role is the co-location of route split, local all-1/pass-face context, and class
  separation.
- This is an observational intersection map, not a mechanism diagram.
- `A_start` and `A_inflow` are all-1 at the pass by definition; under continuous maintenance the
  shares are 0.729 and 0.548.

## 11. Non-integration rule for later

When this chapter is eventually connected to the older two:

1. finite-block stays the broad actual-vs-iid discrepancy layer;
2. delta stays the localization / diagnostic layer;
3. paradoxical-sequence stays the boundary / first-pass-face layer.

Do not import finite-block or delta claims into this chapter unless the term is explicitly redefined
in the definitions section. The bridge (§8 stub) is the only contact point in this pass.
