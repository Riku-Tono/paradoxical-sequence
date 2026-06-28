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


FROM_BIN = "96-127"
TO_BIN = "64-95"
DOWNSTREAM_FROM = "64-95"
DOWNSTREAM_TO = "32-63"
CLASS_ORDER = ["A_start", "A_inflow", "Other_start", "Other_inflow", "no_64_95_pass"]
LOW_SUPPORT_N = 10


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


def downstream_face_class(event: dict[str, object] | None) -> str:
    if event is None:
        return "no_64_95_pass"
    route = str(event["entry_route"])
    all1 = int(event["transition_k"]) == 1 and str(event["pre_k_window_3"]) == "1,1,1"
    if route == "START_IN_LAYER":
        return "A_start" if all1 else "Other_start"
    if route == "INFLOW_FROM_96-127":
        return "A_inflow" if all1 else "Other_inflow"
    return "Other_inflow"


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


def first_after(events: list[dict[str, object]], start: int, predicate) -> dict[str, object] | None:
    for event in events[start + 1 :]:
        if predicate(event):
            return event
    return None


def main() -> None:
    OUT.mkdir(exist_ok=True)
    classified = pd.read_csv(CLASSIFICATION)
    universe = classified[classified["mode"] == "original_n_strict"].copy()
    ids = sorted(int(x) for x in universe["n_original"].unique())
    if len(ids) != 550:
        raise RuntimeError(f"expected 550 original_n_strict trajectories, got {len(ids)}")

    first_pass_rows: list[dict[str, object]] = []
    downstream_rows: list[dict[str, object]] = []
    link_source_rows: list[dict[str, object]] = []

    enter_count = 0
    pass_count = 0

    for n in ids:
        word, events = scan_events(n)
        layer_events = [e for e in events if e["from_bin"] == FROM_BIN]
        if not layer_events:
            continue
        enter_count += 1
        first_entry = layer_events[0]
        first_pass = next((e for e in layer_events if e["to_bin"] == TO_BIN), None)
        has_pass = first_pass is not None
        if has_pass:
            pass_count += 1

        downstream_pass = next(
            (e for e in events if e["from_bin"] == DOWNSTREAM_FROM and e["to_bin"] == DOWNSTREAM_TO),
            None,
        )
        downstream_class = downstream_face_class(downstream_pass)
        common: dict[str, object] = {
            "trajectory_id": n,
            "n": n,
            "odd_core": odd_core(n),
            "log2_n": math.log2(n),
            "word_length": len(word),
            "total_K": sum(word),
            "first_96_127_index": first_entry["position"],
            "first_96_127_entry_route": first_entry["entry_route"],
            "first_96_127_transition": first_entry["transition"],
            "first_96_127_transition_k": first_entry["transition_k"],
            "first_96_127_pre_k_window_3": first_entry["pre_k_window_3"],
            "has_96_127_to_64_95": int(has_pass),
            "downstream_64_95_face_class": downstream_class,
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

        post64 = first_after(
            events,
            pass_pos,
            lambda e: e["from_bin"] == DOWNSTREAM_FROM and e["to_bin"] == DOWNSTREAM_TO,
        )
        next_events = events[pass_pos : pass_pos + 7]
        downstream_rows.append(
            {
                "trajectory_id": n,
                "n": n,
                "odd_core": odd_core(n),
                "upstream_first_pass_face": row["first_pass_face"],
                "upstream_entry_route": row["first_pass_entry_route"],
                "upstream_transition_k": row["first_pass_transition_k"],
                "upstream_pre_k_window_3": row["first_pass_pre_k_window_3"],
                "upstream_pre_k_window_5": row["first_pass_pre_k_window_5"],
                "downstream_64_95_face_class": downstream_class,
                "downstream_64_95_pass_index": "" if downstream_pass is None else downstream_pass["position"],
                "wait_from_96_64_pass_to_64_32_pass": "" if post64 is None else int(post64["position"]) - pass_pos,
                "post_96_64_next6_transitions": seq(next_events, "transition"),
                "post_96_64_next6_k": seq(next_events, "transition_k"),
                "post_96_64_next6_pre3": seq(next_events, "pre_k_window_3"),
            }
        )
        link_source_rows.append(row)

    pass_rows_only = [r for r in first_pass_rows if r["has_96_127_to_64_95"] == 1]
    face_counts = Counter(signature_key(r) for r in pass_rows_only)
    compact_counts = Counter(compact_face(r) for r in pass_rows_only)

    for row in first_pass_rows:
        if row["has_96_127_to_64_95"] != 1:
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
        downstream_counts = Counter(str(r["downstream_64_95_face_class"]) for r in sub)
        wait_rows.append(
            {
                "upstream_first_pass_face": face,
                "count": count,
                "share_of_first_passes": count / pass_count if pass_count else math.nan,
                "median_wait_events": safe_median(waits),
                "mean_wait_events": safe_mean(waits),
                "min_wait_events": min(waits) if waits else math.nan,
                "max_wait_events": max(waits) if waits else math.nan,
                "downstream_A_start": downstream_counts["A_start"],
                "downstream_A_inflow": downstream_counts["A_inflow"],
                "downstream_Other_start": downstream_counts["Other_start"],
                "downstream_Other_inflow": downstream_counts["Other_inflow"],
                "downstream_no_64_95_pass": downstream_counts["no_64_95_pass"],
                "low_support": int(count < LOW_SUPPORT_N),
            }
        )

    link_rows: list[dict[str, object]] = []
    face_to_class_counts: dict[str, Counter[str]] = defaultdict(Counter)
    for row in link_source_rows:
        face_to_class_counts[str(row["first_pass_face"])][str(row["downstream_64_95_face_class"])] += 1
    for face, class_counts in sorted(
        face_to_class_counts.items(),
        key=lambda item: (-sum(item[1].values()), item[0]),
    ):
        total = sum(class_counts.values())
        for cls in CLASS_ORDER:
            count = class_counts[cls]
            link_rows.append(
                {
                    "upstream_first_pass_face": face,
                    "downstream_64_95_face_class": cls,
                    "count": count,
                    "face_total": total,
                    "within_face_share": count / total if total else math.nan,
                    "low_support_face": int(total < LOW_SUPPORT_N),
                    "low_support_cell": int(count < LOW_SUPPORT_N),
                }
            )

    write_csv(OUT / "upstream96_step1_first_pass_table.csv", first_pass_rows)
    write_csv(OUT / "upstream96_step2_signature_counts.csv", signature_rows)
    write_csv(OUT / "upstream96_step3_wait_feature_table.csv", wait_rows)
    write_csv(OUT / "upstream96_step4_downstream_to_64_95.csv", downstream_rows)
    write_csv(OUT / "upstream96_step5_link_to_64_95_face.csv", link_rows)

    top_compact = compact_counts.most_common(10)
    top_full = signature_rows[:10]
    class_counts = Counter(str(r["downstream_64_95_face_class"]) for r in pass_rows_only)

    all1_count = sum(
        1
        for r in pass_rows_only
        if int(r["first_pass_transition_k"]) == 1 and str(r["first_pass_pre_k_window_3"]) == "1,1,1"
    )
    start_count = sum(1 for r in pass_rows_only if str(r["first_pass_entry_route"]) == "START_IN_LAYER")
    start_all1_count = sum(
        1
        for r in pass_rows_only
        if str(r["first_pass_entry_route"]) == "START_IN_LAYER"
        and int(r["first_pass_transition_k"]) == 1
        and str(r["first_pass_pre_k_window_3"]) == "1,1,1"
    )

    report = [
        "# Upstream 96-127 -> 64-95 first-pass report",
        "",
        "Dataset and scanner mode: `original_n_strict`, using the same 550-trajectory universe as the 64-95 first-pass analysis.",
        "",
        "All statements below are observational summaries of this finite scan. They are not mechanism claims or proof claims.",
        "",
        "## Counts",
        "",
        f"- Trajectories in universe: `{len(ids)}`.",
        f"- Trajectories entering `96-127`: `{enter_count}`.",
        f"- Trajectories with a first `96-127 -> 64-95` pass: `{pass_count}`.",
        f"- Trajectories entering `96-127` without an observed `96-127 -> 64-95` pass: `{enter_count - pass_count}`.",
        "",
        "## Dominant first-pass faces",
        "",
    ]
    for face, count in top_compact:
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
    for row in top_full:
        report.append(
            f"| `{row['entry_route']}` | `{row['transition_k']}` | `{row['pre_k_window_3']}` | "
            f"`{row['pre_k_window_5']}` | {row['count']} | {fmt(row['share_of_first_passes'])} | {row['low_support']} |"
        )

    report.extend(
        [
            "",
            "## A_start analogue check",
            "",
            f"- `START_IN_LAYER` upstream first passes: `{start_count}/{pass_count}`.",
            f"- `START_IN_LAYER & transition_k=1 & pre_k_window_3=1,1,1`: `{start_all1_count}/{pass_count}`.",
            f"- Any-route `transition_k=1 & pre_k_window_3=1,1,1`: `{all1_count}/{pass_count}`.",
        ]
    )
    if start_all1_count >= LOW_SUPPORT_N:
        report.append("- A same-shape all-1 start face is present above the low-support cutoff, but it should still be read as an upstream candidate face, not as a mechanism.")
    else:
        report.append("- A clean all-1 `START_IN_LAYER` analogue is not supported above the low-support cutoff in this pass-level table.")

    report.extend(
        [
            "",
            "## Link to later 64-95 -> 32-63 class",
            "",
            "Downstream first `64-95 -> 32-63` classes among upstream pass rows:",
        ]
    )
    for cls in CLASS_ORDER:
        count = class_counts[cls]
        report.append(f"- `{cls}`: `{count}` ({fmt(count / pass_count if pass_count else math.nan)})")

    report.extend(
        [
            "",
            "The cross-tab in `upstream96_step5_link_to_64_95_face.csv` flags both low-support upstream faces and low-support cells. Treat cells below 10 rows as descriptive only.",
            "",
            "## Comparison with the 64-95 all-1 face",
            "",
            f"- The upstream `96-127 -> 64-95` first pass has `{all1_count}/{pass_count}` all-1 rows under `transition_k=1 & pre_k_window_3=1,1,1`.",
            "- The leading upstream faces should be read from the count table rather than projected from the 64-95 A_start definition.",
            "- If the leading rows are not dominated by `k=1/pre111`, this upstream boundary has a different first-pass surface from the 64-95 all-1 face in this scan.",
            "",
            "## Support caution",
            "",
            f"- Low-support threshold used here: cells or faces with `count < {LOW_SUPPORT_N}`.",
            "- The upstream boundary is less suitable as a load-bearing claim when interpretation depends on a single low-count face or a low-count downstream class cell.",
            "- The generated files keep the longer local windows so candidate faces can be inspected without upgrading them into claims.",
            "",
            "## Output files",
            "",
            "- `upstream96_step1_first_pass_table.csv`",
            "- `upstream96_step2_signature_counts.csv`",
            "- `upstream96_step3_wait_feature_table.csv`",
            "- `upstream96_step4_downstream_to_64_95.csv`",
            "- `upstream96_step5_link_to_64_95_face.csv`",
        ]
    )
    (OUT / "upstream96_firstpass_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
