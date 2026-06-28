from __future__ import annotations

import csv
import math
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, median

import pandas as pd

from downstream8_first_pass_analysis import (
    CLASSIFICATION,
    LOW_SUPPORT_N,
    OUT,
    PREV16_FACE_ORDER,
    PREV32_FACE_ORDER,
    PREV64_CLASS_ORDER,
    compact_event_face,
    compact_face,
    fmt,
    link_rows_from_counts,
    odd_core,
    previous_64_95_class,
    previous_face,
    scan_events,
    seq,
)


FROM_BIN = "4-7"
TO_BIN = "2-3"
PREV32_FROM = "32-63"
PREV32_TO = "16-31"
PREV16_FROM = "16-31"
PREV16_TO = "8-15"
PREV8_FROM = "8-15"
PREV8_TO = "4-7"
PREV8_FACE_ORDER = [
    "INFLOW_FROM_16-31 | k=5 | pre3=1,1,3+",
    "START_IN_LAYER | k=2 | pre3=1,1,2",
    "START_IN_LAYER | k=2 | pre3=3+,1,2",
    "INFLOW_FROM_16-31 | k=2 | pre3=3+,1,2",
    "NO_8_15_PASS",
]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def safe_mean(values: list[float]) -> float:
    return float(mean(values)) if values else math.nan


def safe_median(values: list[float]) -> float:
    return float(median(values)) if values else math.nan


def signature_key(row: dict[str, object]) -> tuple[object, ...]:
    return (
        row["first_pass_entry_route"],
        row["first_pass_transition_k"],
        row["first_pass_pre_k_window_3"],
        row["first_pass_pre_k_window_5"],
        row["first_pass_local_window_4"],
        row["first_pass_local_window_5"],
    )


def main() -> None:
    OUT.mkdir(exist_ok=True)
    classified = pd.read_csv(CLASSIFICATION)
    universe = classified[classified["mode"] == "original_n_strict"].copy()
    ids = sorted(int(x) for x in universe["n_original"].unique())
    if len(ids) != 550:
        raise RuntimeError(f"expected 550 original_n_strict trajectories, got {len(ids)}")

    first_pass_rows: list[dict[str, object]] = []
    postpass_rows: list[dict[str, object]] = []
    enter_count = 0
    pass_count = 0

    for n in ids:
        word, events = scan_events(n)
        previous64_class, previous64_pass = previous_64_95_class(events)
        previous32_face, previous32_pass = previous_face(events, PREV32_FROM, PREV32_TO, "NO_32_63_PASS")
        previous16_face, previous16_pass = previous_face(events, PREV16_FROM, PREV16_TO, "NO_16_31_PASS")
        previous8_face, previous8_pass = previous_face(events, PREV8_FROM, PREV8_TO, "NO_8_15_PASS")
        layer_events = [e for e in events if e["from_bin"] == FROM_BIN]
        if not layer_events:
            continue
        enter_count += 1
        first_entry = layer_events[0]
        first_pass = next((e for e in layer_events if e["to_bin"] == TO_BIN), None)
        has_pass = first_pass is not None
        if has_pass:
            pass_count += 1

        common: dict[str, object] = {
            "trajectory_id": n,
            "n": n,
            "odd_core": odd_core(n),
            "log2_n": math.log2(n),
            "word_length": len(word),
            "total_K": sum(word),
            "previous_64_95_face_class": previous64_class,
            "previous_64_95_pass_index": "" if previous64_pass is None else previous64_pass["position"],
            "previous_32_63_face": previous32_face,
            "previous_32_63_pass_index": "" if previous32_pass is None else previous32_pass["position"],
            "previous_16_31_face": previous16_face,
            "previous_16_31_pass_index": "" if previous16_pass is None else previous16_pass["position"],
            "previous_8_15_face": previous8_face,
            "previous_8_15_pass_index": "" if previous8_pass is None else previous8_pass["position"],
            "first_4_7_index": first_entry["position"],
            "first_4_7_entry_route": first_entry["entry_route"],
            "first_4_7_transition": first_entry["transition"],
            "first_4_7_transition_k": first_entry["transition_k"],
            "first_4_7_pre_k_window_3": first_entry["pre_k_window_3"],
            "has_4_7_to_2_3": int(has_pass),
        }

        if first_pass is None:
            first_pass_rows.append(
                {
                    **common,
                    "first_pass_index": "",
                    "first_pass_wait_events": "",
                    "first_pass_entry_route": "",
                    "first_pass_transition_k": "",
                    "first_pass_pre_k_window_3": "",
                    "first_pass_pre_k_window_5": "",
                    "first_pass_local_window_4": "",
                    "first_pass_local_window_5": "",
                    "first_pass_face": "NO_PASS",
                    "low_support_face": "",
                }
            )
            continue

        pass_pos = int(first_pass["position"])
        row = {
            **common,
            "first_pass_index": pass_pos,
            "first_pass_wait_events": pass_pos - int(first_entry["position"]),
            "first_pass_entry_route": first_pass["entry_route"],
            "first_pass_transition_k": first_pass["transition_k"],
            "first_pass_pre_k_window_3": first_pass["pre_k_window_3"],
            "first_pass_pre_k_window_5": first_pass["pre_k_window_5"],
            "first_pass_local_window_4": first_pass["local_window_4"],
            "first_pass_local_window_5": first_pass["local_window_5"],
            "first_pass_face": "",
            "low_support_face": "",
        }
        row["first_pass_face"] = compact_face(row)
        first_pass_rows.append(row)

        next_events = events[pass_pos : pass_pos + 7]
        postpass_rows.append(
            {
                "trajectory_id": n,
                "n": n,
                "odd_core": odd_core(n),
                "previous_64_95_face_class": previous64_class,
                "previous_32_63_face": previous32_face,
                "previous_16_31_face": previous16_face,
                "previous_8_15_face": previous8_face,
                "first_pass_face": row["first_pass_face"],
                "first_pass_index": pass_pos,
                "postpass_next6_transitions": seq(next_events, "transition"),
                "postpass_next6_bins": seq(next_events, "from_bin"),
                "postpass_next6_k": seq(next_events, "transition_k"),
                "postpass_next6_pre3": seq(next_events, "pre_k_window_3"),
            }
        )

    pass_rows_only = [r for r in first_pass_rows if r["has_4_7_to_2_3"] == 1]
    face_counts = Counter(signature_key(r) for r in pass_rows_only)
    compact_counts = Counter(compact_face(r) for r in pass_rows_only)

    for row in first_pass_rows:
        if row["has_4_7_to_2_3"] != 1:
            continue
        row["low_support_face"] = int(compact_counts[str(row["first_pass_face"])] < LOW_SUPPORT_N)

    signature_rows: list[dict[str, object]] = []
    for key, count in face_counts.most_common():
        route, k, pre3, pre5, local4, local5 = key
        signature_rows.append(
            {
                "entry_route": route,
                "transition_k": k,
                "pre_k_window_3": pre3,
                "pre_k_window_5": pre5,
                "local_window_4": local4,
                "local_window_5": local5,
                "count": count,
                "share_of_first_passes": count / pass_count if pass_count else math.nan,
                "low_support": int(count < LOW_SUPPORT_N),
            }
        )

    wait_rows: list[dict[str, object]] = []
    for face, count in compact_counts.most_common():
        sub = [r for r in pass_rows_only if r["first_pass_face"] == face]
        waits = [float(r["first_pass_wait_events"]) for r in sub]
        prev64_counts = Counter(str(r["previous_64_95_face_class"]) for r in sub)
        prev32_counts = Counter(str(r["previous_32_63_face"]) for r in sub)
        prev16_counts = Counter(str(r["previous_16_31_face"]) for r in sub)
        prev8_counts = Counter(str(r["previous_8_15_face"]) for r in sub)
        wait_rows.append(
            {
                "first_pass_face": face,
                "count": count,
                "share_of_first_passes": count / pass_count if pass_count else math.nan,
                "median_wait_events": safe_median(waits),
                "mean_wait_events": safe_mean(waits),
                "min_wait_events": min(waits) if waits else math.nan,
                "max_wait_events": max(waits) if waits else math.nan,
                "previous_A_start": prev64_counts["A_start"],
                "previous_A_inflow": prev64_counts["A_inflow"],
                "previous_Other_start": prev64_counts["Other_start"],
                "previous_Other_inflow": prev64_counts["Other_inflow"],
                "previous_G0": prev64_counts["G0"],
                "previous32_no_pass": prev32_counts["NO_32_63_PASS"],
                "previous16_no_pass": prev16_counts["NO_16_31_PASS"],
                "previous8_no_pass": prev8_counts["NO_8_15_PASS"],
                "low_support": int(count < LOW_SUPPORT_N),
            }
        )

    link64_counts: dict[str, Counter[str]] = defaultdict(Counter)
    link32_counts: dict[str, Counter[str]] = defaultdict(Counter)
    link16_counts: dict[str, Counter[str]] = defaultdict(Counter)
    link8_counts: dict[str, Counter[str]] = defaultdict(Counter)
    for row in pass_rows_only:
        link64_counts[str(row["previous_64_95_face_class"])][str(row["first_pass_face"])] += 1
        link32_counts[str(row["previous_32_63_face"])][str(row["first_pass_face"])] += 1
        link16_counts[str(row["previous_16_31_face"])][str(row["first_pass_face"])] += 1
        link8_counts[str(row["previous_8_15_face"])][str(row["first_pass_face"])] += 1

    write_csv(OUT / "downstream4_step1_first_pass_table.csv", first_pass_rows)
    write_csv(OUT / "downstream4_step2_signature_counts.csv", signature_rows)
    write_csv(OUT / "downstream4_step3_wait_feature_table.csv", wait_rows)
    write_csv(
        OUT / "downstream4_step4_link_from_64_95_class.csv",
        link_rows_from_counts(
            link64_counts,
            PREV64_CLASS_ORDER,
            "previous_64_95_face_class",
            "downstream4_first_pass_face",
        ),
    )
    write_csv(
        OUT / "downstream4_step5_link_from_32_63_face.csv",
        link_rows_from_counts(
            link32_counts,
            PREV32_FACE_ORDER,
            "previous_32_63_face",
            "downstream4_first_pass_face",
        ),
    )
    write_csv(
        OUT / "downstream4_step6_link_from_16_31_face.csv",
        link_rows_from_counts(
            link16_counts,
            PREV16_FACE_ORDER,
            "previous_16_31_face",
            "downstream4_first_pass_face",
        ),
    )
    write_csv(
        OUT / "downstream4_step7_link_from_8_15_face.csv",
        link_rows_from_counts(
            link8_counts,
            PREV8_FACE_ORDER,
            "previous_8_15_face",
            "downstream4_first_pass_face",
        ),
    )
    write_csv(OUT / "downstream4_step8_postpass_windows.csv", postpass_rows)

    prev64_totals = Counter(str(r["previous_64_95_face_class"]) for r in pass_rows_only)
    prev8_totals = Counter(str(r["previous_8_15_face"]) for r in pass_rows_only)
    entry_transition_counts = Counter(str(r["first_4_7_transition"]) for r in first_pass_rows)
    entry_k_counts = Counter(str(r["first_4_7_transition_k"]) for r in first_pass_rows)
    compact_top = compact_counts.most_common(12)
    dominant_face, dominant_count = compact_top[0] if compact_top else ("", 0)

    report = [
        "# Downstream 4-7 -> 2-3 first-pass report",
        "",
        "Dataset and scanner mode: `original_n_strict`, using the same 550-trajectory universe as the previous first-pass analyses.",
        "",
        "All statements below are observational summaries of this finite scan. They are not mechanism claims or proof claims.",
        "",
        "## Counts",
        "",
        f"- Trajectories in universe: `{len(ids)}`.",
        f"- Trajectories entering `4-7`: `{enter_count}`.",
        f"- Trajectories with a first `4-7 -> 2-3` pass: `{pass_count}`.",
        f"- Trajectories entering `4-7` without an observed `4-7 -> 2-3` pass: `{enter_count - pass_count}`.",
        "",
        "## Dominant first-pass faces",
        "",
    ]
    if pass_count == 0:
        report.append("- No `4-7 -> 2-3` pass was observed, so no first-pass face is defined for this target.")
    else:
        for face, count in compact_top:
            flag = " LOW_SUPPORT" if count < LOW_SUPPORT_N else ""
            report.append(f"- `{face}`: `{count}` ({fmt(count / pass_count if pass_count else math.nan)}){flag}")

    report.extend(
        [
            "",
            "Top full signatures, including the requested longer windows:",
            "",
            "| entry_route | transition_k | pre3 | pre5 | count | share | low_support |",
            "| --- | ---: | --- | --- | ---: | ---: | ---: |",
        ]
    )
    for row in signature_rows[:12]:
        report.append(
            f"| `{row['entry_route']}` | `{row['transition_k']}` | `{row['pre_k_window_3']}` | "
            f"`{row['pre_k_window_5']}` | {row['count']} | {fmt(row['share_of_first_passes'])} | {row['low_support']} |"
        )

    report.extend(
        [
            "",
            "## Boundary shape",
            "",
            f"- Dominant compact face: `{dominant_face}` with `{dominant_count}/{pass_count}` rows.",
            f"- Compact-face count: `{len(compact_counts)}`.",
            f"- Full-signature count with local windows: `{len(signature_rows)}`.",
        ]
    )
    if pass_count == 0:
        report.append("- The requested boundary is not observed in this scan; this is a zero-pass result rather than a clean/diffuse face result.")
    elif dominant_count == pass_count:
        report.append("- At the compact-face level, this boundary is exhaustive in this scan.")
    elif dominant_count >= pass_count / 2:
        report.append("- At the compact-face level, this boundary is dominant but not exhaustive in this scan.")
    else:
        report.append("- At the compact-face level, this boundary is split rather than dominated by one face.")

    report.extend(
        [
            "",
            "## First 4-7 entry check",
            "",
            "Because the target pass is absent, the first `4-7` entry transition is informative:",
        ]
    )
    for transition, count in entry_transition_counts.most_common():
        report.append(f"- `{transition}`: `{count}/{enter_count}`")
    report.append("")
    report.append("First `4-7` entry transition_k counts:")
    for k, count in entry_k_counts.most_common():
        report.append(f"- `k={k}`: `{count}/{enter_count}`")

    report.extend(
        [
            "",
            "## Link from previous 64-95 class",
            "",
            "Previous 64-95 class totals among downstream pass rows:",
        ]
    )
    for cls in PREV64_CLASS_ORDER:
        report.append(f"- `{cls}`: `{prev64_totals[cls]}`")
    report.append("")
    for cls in PREV64_CLASS_ORDER:
        total = sum(link64_counts[cls].values())
        if total == 0:
            continue
        top_face, top_count = link64_counts[cls].most_common(1)[0]
        flag = " LOW_SUPPORT_SOURCE" if total < LOW_SUPPORT_N else ""
        report.append(f"- `{cls}` top downstream face: `{top_face}` = `{top_count}/{total}`{flag}")

    report.extend(
        [
            "",
            "## Link from previous 8-15 face",
            "",
            "Previous 8-15 face totals among downstream pass rows:",
        ]
    )
    for face in PREV8_FACE_ORDER:
        report.append(f"- `{face}`: `{prev8_totals[face]}`")
    report.append("")
    for face in PREV8_FACE_ORDER:
        total = sum(link8_counts[face].values())
        if total == 0:
            continue
        top_face, top_count = link8_counts[face].most_common(1)[0]
        flag = " LOW_SUPPORT_SOURCE" if total < LOW_SUPPORT_N else ""
        report.append(f"- Previous `{face}` top downstream face: `{top_face}` = `{top_count}/{total}`{flag}")

    report.extend(
        [
            "",
            "## Support caution",
            "",
            f"- Low-support threshold used here: cells or faces with `count < {LOW_SUPPORT_N}`.",
            "- Low-support cells are kept as observations, not promoted to claims.",
            "",
            "## Output files",
            "",
            "- `downstream4_step1_first_pass_table.csv`",
            "- `downstream4_step2_signature_counts.csv`",
            "- `downstream4_step3_wait_feature_table.csv`",
            "- `downstream4_step4_link_from_64_95_class.csv`",
            "- `downstream4_step5_link_from_32_63_face.csv`",
            "- `downstream4_step6_link_from_16_31_face.csv`",
            "- `downstream4_step7_link_from_8_15_face.csv`",
            "- `downstream4_step8_postpass_windows.csv`",
        ]
    )
    (OUT / "downstream4_firstpass_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
