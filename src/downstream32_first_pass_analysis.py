from __future__ import annotations

import csv
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, median

import pandas as pd


ROOT = Path(r"C:\Users\yauki\Documents\Codex\2026-06-28\task-first-pass-face-analysis-for")
OUT = ROOT / "outputs"
PREV_WORK = Path(r"C:\Users\yauki\Documents\Codex\2026-06-27\task-analyze-the-12-trajectories-that\work")
BASE_WORK = Path(r"C:\Users\yauki\Documents\Codex\2026-06-27\codex-codex-remaining-k-chain-64\work")
CLASSIFICATION = Path(
    r"C:\Users\yauki\Documents\Codex\2026-06-27\integer-side-projection-of-64-95\outputs\rozier_nonhit_classification.csv"
)

sys.path.insert(0, str(PREV_WORK))
sys.path.insert(0, str(BASE_WORK))

from analyze_entry_64_95_boundary import (  # noqa: E402
    event_word_original_n_strict,
    local_windows,
    odd_core,
    path_for_word,
    pattern,
    remaining_k_bin,
)

import paradoxical_sequence_analysis as base  # noqa: E402


FROM_BIN = "32-63"
TO_BIN = "16-31"
PREV_FROM = "64-95"
PREV_TO = "32-63"
PREV_CLASS_ORDER = ["A_start", "A_inflow", "Other_start", "Other_inflow", "no_64_95_pass", "G0"]
LOW_SUPPORT_N = 10
REPORTED_FACE = "INFLOW_FROM_64-95 | k=3 | pre3=1,1,3+"


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def fmt(value: object, digits: int = 3) -> str:
    try:
        x = float(value)
    except (TypeError, ValueError):
        return str(value)
    if math.isnan(x):
        return "NA"
    return f"{x:.{digits}f}"


def safe_mean(values: list[float]) -> float:
    return float(mean(values)) if values else math.nan


def safe_median(values: list[float]) -> float:
    return float(median(values)) if values else math.nan


def seq(events: list[dict[str, object]], key: str) -> str:
    return " | ".join(str(e[key]) for e in events)


def scan_events(n: int) -> tuple[tuple[int, ...], list[dict[str, object]]]:
    word = event_word_original_n_strict(n)
    path = path_for_word(word)
    total = sum(word)
    prefix = 0
    rows: list[dict[str, object]] = []
    for pos, k in enumerate(word):
        before = total - prefix
        after = before - k
        from_bin = remaining_k_bin(before)
        to_bin = remaining_k_bin(after)
        rows.append(
            {
                "position": pos,
                "remaining_K_before": before,
                "remaining_K_after": after,
                "from_bin": from_bin,
                "to_bin": to_bin,
                "transition": f"{from_bin} -> {to_bin}",
                "transition_k": k,
                "transition_k_cat": base.kcat(k),
                "entry_route": base.entry_route(path, pos, from_bin),
                "pre_k_window_3": pattern(word[max(0, pos - 2) : pos + 1]),
                "pre_k_window_5": pattern(word[max(0, pos - 4) : pos + 1]),
                "local_window_4": ";".join(local_windows(word, pos, 4)),
                "local_window_5": ";".join(local_windows(word, pos, 5)),
            }
        )
        prefix += k
    return word, rows


def previous_64_95_class(events: list[dict[str, object]]) -> tuple[str, dict[str, object] | None]:
    layer_events = [e for e in events if e["from_bin"] == PREV_FROM]
    if not layer_events:
        return "G0", None
    pass_event = next((e for e in layer_events if e["to_bin"] == PREV_TO), None)
    if pass_event is None:
        return "no_64_95_pass", None
    route = str(pass_event["entry_route"])
    all1 = int(pass_event["transition_k"]) == 1 and str(pass_event["pre_k_window_3"]) == "1,1,1"
    if route == "START_IN_LAYER":
        return ("A_start" if all1 else "Other_start"), pass_event
    if route == "INFLOW_FROM_96-127":
        return ("A_inflow" if all1 else "Other_inflow"), pass_event
    return "Other_inflow", pass_event


def signature_key(row: dict[str, object]) -> tuple[object, ...]:
    return (
        row["first_pass_entry_route"],
        row["first_pass_transition_k"],
        row["first_pass_pre_k_window_3"],
        row["first_pass_pre_k_window_5"],
        row["first_pass_local_window_4"],
        row["first_pass_local_window_5"],
    )


def compact_face(row: dict[str, object]) -> str:
    return (
        f"{row['first_pass_entry_route']} | k={row['first_pass_transition_k']} | "
        f"pre3={row['first_pass_pre_k_window_3']}"
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
        previous_class, previous_pass = previous_64_95_class(events)
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
            "previous_64_95_face_class": previous_class,
            "previous_64_95_pass_index": "" if previous_pass is None else previous_pass["position"],
            "first_32_63_index": first_entry["position"],
            "first_32_63_entry_route": first_entry["entry_route"],
            "first_32_63_transition": first_entry["transition"],
            "first_32_63_transition_k": first_entry["transition_k"],
            "first_32_63_pre_k_window_3": first_entry["pre_k_window_3"],
            "has_32_63_to_16_31": int(has_pass),
        }

        if first_pass is None:
            row = {
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
            first_pass_rows.append(row)
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
                "previous_64_95_face_class": previous_class,
                "first_pass_face": row["first_pass_face"],
                "first_pass_index": pass_pos,
                "postpass_next6_transitions": seq(next_events, "transition"),
                "postpass_next6_bins": seq(next_events, "from_bin"),
                "postpass_next6_k": seq(next_events, "transition_k"),
                "postpass_next6_pre3": seq(next_events, "pre_k_window_3"),
            }
        )

    pass_rows_only = [r for r in first_pass_rows if r["has_32_63_to_16_31"] == 1]
    face_counts = Counter(signature_key(r) for r in pass_rows_only)
    compact_counts = Counter(compact_face(r) for r in pass_rows_only)

    for row in first_pass_rows:
        if row["has_32_63_to_16_31"] != 1:
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
        prev_counts = Counter(str(r["previous_64_95_face_class"]) for r in sub)
        wait_rows.append(
            {
                "first_pass_face": face,
                "count": count,
                "share_of_first_passes": count / pass_count if pass_count else math.nan,
                "median_wait_events": safe_median(waits),
                "mean_wait_events": safe_mean(waits),
                "min_wait_events": min(waits) if waits else math.nan,
                "max_wait_events": max(waits) if waits else math.nan,
                "previous_A_start": prev_counts["A_start"],
                "previous_A_inflow": prev_counts["A_inflow"],
                "previous_Other_start": prev_counts["Other_start"],
                "previous_Other_inflow": prev_counts["Other_inflow"],
                "previous_no_64_95_pass": prev_counts["no_64_95_pass"],
                "previous_G0": prev_counts["G0"],
                "low_support": int(count < LOW_SUPPORT_N),
            }
        )

    link_counts: dict[str, Counter[str]] = defaultdict(Counter)
    for row in pass_rows_only:
        link_counts[str(row["previous_64_95_face_class"])][str(row["first_pass_face"])] += 1

    link_rows: list[dict[str, object]] = []
    for cls in PREV_CLASS_ORDER:
        class_total = sum(link_counts[cls].values())
        for face, count in link_counts[cls].most_common():
            link_rows.append(
                {
                    "previous_64_95_face_class": cls,
                    "downstream32_first_pass_face": face,
                    "count": count,
                    "previous_class_total": class_total,
                    "within_previous_class_share": count / class_total if class_total else math.nan,
                    "low_support_previous_class": int(class_total < LOW_SUPPORT_N),
                    "low_support_cell": int(count < LOW_SUPPORT_N),
                }
            )

    write_csv(OUT / "downstream32_step1_first_pass_table.csv", first_pass_rows)
    write_csv(OUT / "downstream32_step2_signature_counts.csv", signature_rows)
    write_csv(OUT / "downstream32_step3_wait_feature_table.csv", wait_rows)
    write_csv(OUT / "downstream32_step4_link_from_64_95_face.csv", link_rows)
    write_csv(OUT / "downstream32_step5_postpass_windows.csv", postpass_rows)

    compact_top = compact_counts.most_common(12)
    reported_count = compact_counts[REPORTED_FACE]
    prev_totals = Counter(str(r["previous_64_95_face_class"]) for r in pass_rows_only)

    report = [
        "# Downstream 32-63 -> 16-31 first-pass report",
        "",
        "Dataset and scanner mode: `original_n_strict`, using the same 550-trajectory universe as the 64-95 first-pass analysis.",
        "",
        "All statements below are observational summaries of this finite scan. They are not mechanism claims or proof claims.",
        "",
        "## Counts",
        "",
        f"- Trajectories in universe: `{len(ids)}`.",
        f"- Trajectories entering `32-63`: `{enter_count}`.",
        f"- Trajectories with a first `32-63 -> 16-31` pass: `{pass_count}`.",
        f"- Trajectories entering `32-63` without an observed `32-63 -> 16-31` pass: `{enter_count - pass_count}`.",
        "",
        "## Dominant first-pass faces",
        "",
    ]
    for face, count in compact_top:
        flag = " LOW_SUPPORT" if count < LOW_SUPPORT_N else ""
        reported = " REPORTED_FACE" if face == REPORTED_FACE else ""
        report.append(f"- `{face}`: `{count}` ({fmt(count / pass_count if pass_count else math.nan)}){reported}{flag}")

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
            "## Reported face check",
            "",
            f"- Reported compact face `{REPORTED_FACE}` appears in `{reported_count}/{pass_count}` first passes.",
            f"- Share among all first `32-63 -> 16-31` passes: `{fmt(reported_count / pass_count if pass_count else math.nan)}`.",
        ]
    )
    if reported_count == pass_count:
        report.append("- In this first-pass scan the reported compact face is globally dominant and covers every observed first pass.")
    elif reported_count >= pass_count / 2:
        report.append("- In this first-pass scan the reported compact face is dominant, but not exhaustive.")
    else:
        report.append("- In this first-pass scan the reported compact face is not globally dominant.")

    report.extend(
        [
            "",
            "## Link from previous 64-95 class",
            "",
            "Previous class totals among downstream pass rows:",
        ]
    )
    for cls in PREV_CLASS_ORDER:
        report.append(f"- `{cls}`: `{prev_totals[cls]}`")
    report.extend(
        [
            "",
            "The cross-tab in `downstream32_step4_link_from_64_95_face.csv` flags low-support previous classes and low-support cells. Treat cells below 10 rows as descriptive only.",
            "",
            "## Class-level downstream reading",
            "",
        ]
    )
    for cls in PREV_CLASS_ORDER:
        class_total = sum(link_counts[cls].values())
        if class_total == 0:
            continue
        top_face, top_count = link_counts[cls].most_common(1)[0]
        flag = " LOW_SUPPORT_CLASS" if class_total < LOW_SUPPORT_N else ""
        report.append(f"- `{cls}` top downstream face: `{top_face}` = `{top_count}/{class_total}`{flag}")

    report.extend(
        [
            "",
            "## Clean face versus diffuse surface",
            "",
            f"- Compact-face count: `{len(compact_counts)}`.",
            f"- Full-signature count with local windows: `{len(signature_rows)}`.",
            "- If the compact face is nearly exhaustive while full signatures split by longer local windows, the boundary is clean at route/k/pre3 level but more diffuse at the longer-window level.",
            "",
            "## Support caution",
            "",
            f"- Low-support threshold used here: cells or faces with `count < {LOW_SUPPORT_N}`.",
            "- Low-support cells are kept as observations, not promoted to claims.",
            "",
            "## Output files",
            "",
            "- `downstream32_step1_first_pass_table.csv`",
            "- `downstream32_step2_signature_counts.csv`",
            "- `downstream32_step3_wait_feature_table.csv`",
            "- `downstream32_step4_link_from_64_95_face.csv`",
            "- `downstream32_step5_postpass_windows.csv`",
        ]
    )
    (OUT / "downstream32_firstpass_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
