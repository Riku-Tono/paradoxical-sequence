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


BOUNDARIES = [
    ("B_up", "96-127", "64-95"),
    ("B_sort", "64-95", "32-63"),
    ("B_down1", "32-63", "16-31"),
    ("B_down2", "16-31", "8-15"),
    ("B_down3", "8-15", "4-7"),
    ("B_terminal", "4-7", "0-1"),
]
BOUNDARY_LABELS = {b[0]: f"{b[1]} -> {b[2]}" for b in BOUNDARIES}
MAJOR_CLASSES = ["A_start", "A_inflow", "Other_start"]
CLASS_ORDER = ["A_start", "A_inflow", "Other_start", "Other_inflow", "G0"]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def fmt(x: object, digits: int = 3) -> str:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return str(x)
    if math.isnan(v):
        return "NA"
    return f"{v:.{digits}f}"


def compact_dist(counter: Counter[str], limit: int = 10) -> str:
    total = sum(counter.values())
    return "; ".join(f"{k}: {v} ({v / total:.3f})" for k, v in counter.most_common(limit)) if total else ""


def entropy(counter: Counter[str]) -> float:
    total = sum(counter.values())
    if not total:
        return math.nan
    return -sum((v / total) * math.log2(v / total) for v in counter.values() if v)


def safe_mean(values: list[float]) -> float:
    return float(mean(values)) if values else math.nan


def safe_median(values: list[float]) -> float:
    return float(median(values)) if values else math.nan


def l1(a: Counter[str], b: Counter[str]) -> float:
    ta = sum(a.values())
    tb = sum(b.values())
    keys = set(a) | set(b)
    if not ta and not tb:
        return 0.0
    return sum(abs((a[k] / ta if ta else 0.0) - (b[k] / tb if tb else 0.0)) for k in keys)


def normalize_feature_value(value: object) -> str:
    if value is None:
        return "NA"
    if isinstance(value, float) and math.isnan(value):
        return "NA"
    return str(value)


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
                "transition_k": k,
                "entry_route": base.entry_route(path, pos, from_bin),
                "pre_k_window_1": pattern(word[pos : pos + 1]),
                "pre_k_window_2": pattern(word[max(0, pos - 1) : pos + 1]),
                "pre_k_window_3": pattern(word[max(0, pos - 2) : pos + 1]),
                "pre_k_window_4": pattern(word[max(0, pos - 3) : pos + 1]),
                "pre_k_window_5": pattern(word[max(0, pos - 4) : pos + 1]),
                "local_window_3": ";".join(local_windows(word, pos, 3)),
                "local_window_4": ";".join(local_windows(word, pos, 4)),
                "local_window_5": ";".join(local_windows(word, pos, 5)),
            }
        )
        prefix += k
    return word, rows


def compact_face(row: dict[str, object]) -> str:
    return f"{row['entry_route']} | k={row['transition_k']} | pre3={row['pre_k_window_3']}"


def full_face(row: dict[str, object]) -> str:
    return (
        f"{row['entry_route']} | k={row['transition_k']} | "
        f"pre5={row['pre_k_window_5']} | local4={row['local_window_4']}"
    )


def class_64_95(events: list[dict[str, object]]) -> str:
    first_64 = next((e for e in events if e["from_bin"] == "64-95"), None)
    if first_64 is None:
        return "G0"
    pass_event = next((e for e in events if e["from_bin"] == "64-95" and e["to_bin"] == "32-63"), None)
    if pass_event is None:
        return "G0"
    is_a = int(pass_event["transition_k"]) == 1 and pass_event["pre_k_window_3"] == "1,1,1"
    route = str(pass_event["entry_route"])
    if route == "START_IN_LAYER":
        return "A_start" if is_a else "Other_start"
    if route == "INFLOW_FROM_96-127":
        return "A_inflow" if is_a else "Other_inflow"
    return "Other_inflow"


def first_boundary_event(events: list[dict[str, object]], from_bin: str, to_bin: str) -> tuple[dict[str, object] | None, int | None]:
    entry_pos = next((int(e["position"]) for e in events if e["from_bin"] == from_bin), None)
    if entry_pos is None:
        return None, None
    event = next((e for e in events if e["from_bin"] == from_bin and e["to_bin"] == to_bin), None)
    return event, entry_pos


def k1_metrics(word: tuple[int, ...], entry_pos: int, pass_pos: int) -> dict[str, object]:
    seq = list(word[entry_pos : pass_pos + 1])
    cur_run = 0
    for k in reversed(seq):
        if k == 1:
            cur_run += 1
        else:
            break
    longest = 0
    run = 0
    for k in seq:
        if k == 1:
            run += 1
            longest = max(longest, run)
        else:
            run = 0
    return {
        "current_k1_run": cur_run,
        "longest_k1_run_since_entry": longest,
        "share_k1_since_entry": seq.count(1) / len(seq) if seq else math.nan,
    }


def pre111_metrics(events: list[dict[str, object]], entry_pos: int, pass_pos: int) -> dict[str, object]:
    segment = [e for e in events if entry_pos <= int(e["position"]) <= pass_pos]
    first = next((int(e["position"]) for e in segment if e["pre_k_window_3"] == "1,1,1"), None)
    if first is None:
        return {
            "has_pre111_since_entry": 0,
            "first_pre111_index_since_entry": "",
            "distance_first_pre111_to_pass": "",
            "maintains_pre111_to_pass": 0,
        }
    tail = [e for e in segment if int(e["position"]) >= first]
    return {
        "has_pre111_since_entry": 1,
        "first_pre111_index_since_entry": first - entry_pos,
        "distance_first_pre111_to_pass": pass_pos - first,
        "maintains_pre111_to_pass": int(all(e["pre_k_window_3"] == "1,1,1" for e in tail)),
    }


def boundary_face_map(events: list[dict[str, object]]) -> dict[str, str]:
    out: dict[str, str] = {}
    for boundary_id, from_bin, to_bin in BOUNDARIES:
        event, _entry = first_boundary_event(events, from_bin, to_bin)
        out[boundary_id] = compact_face(event) if event is not None else "NO_EVENT"
    return out


def make_event_rows(ids: list[int]) -> tuple[list[dict[str, object]], dict[int, tuple[int, ...]], dict[int, list[dict[str, object]]]]:
    rows: list[dict[str, object]] = []
    words: dict[int, tuple[int, ...]] = {}
    events_by_id: dict[int, list[dict[str, object]]] = {}
    for n in ids:
        word, events = scan_events(n)
        words[n] = word
        events_by_id[n] = events
        faces = boundary_face_map(events)
        cls = class_64_95(events)
        for idx, (boundary_id, from_bin, to_bin) in enumerate(BOUNDARIES):
            event, entry_pos = first_boundary_event(events, from_bin, to_bin)
            if event is None or entry_pos is None:
                continue
            pass_pos = int(event["position"])
            metrics = {}
            metrics.update(k1_metrics(word, entry_pos, pass_pos))
            metrics.update(pre111_metrics(events, entry_pos, pass_pos))
            row = {
                "boundary_id": boundary_id,
                "boundary_label": f"{from_bin} -> {to_bin}",
                "trajectory_id": n,
                "n": n,
                "odd_core": odd_core(n),
                "log2_n": math.log2(n),
                "word_length": len(word),
                "total_K": sum(word),
                "from_bin": from_bin,
                "to_bin": to_bin,
                "event_index_global": pass_pos,
                "event_index_from_first_relevant_entry": pass_pos - entry_pos,
                "wait_from_entry": pass_pos - entry_pos,
                "entry_route": event["entry_route"],
                "transition_k": event["transition_k"],
                "pre_k_window_1": event["pre_k_window_1"],
                "pre_k_window_2": event["pre_k_window_2"],
                "pre_k_window_3": event["pre_k_window_3"],
                "pre_k_window_4": event["pre_k_window_4"],
                "pre_k_window_5": event["pre_k_window_5"],
                "local_window_3": event["local_window_3"],
                "local_window_4": event["local_window_4"],
                "local_window_5": event["local_window_5"],
                "contains_1111_local4": int("1,1,1,1" in str(event["local_window_4"]).split(";")),
                "contains_11111_local5": int("1,1,1,1,1" in str(event["local_window_5"]).split(";")),
                "previous_boundary_face": faces[BOUNDARIES[idx - 1][0]] if idx > 0 else "NA",
                "next_boundary_face": faces[BOUNDARIES[idx + 1][0]] if idx + 1 < len(BOUNDARIES) else "NA",
                "64_95_class": cls,
                "compact_face": compact_face(event),
                "full_face": full_face(event),
            }
            row.update(metrics)
            rows.append(row)
    return rows, words, events_by_id


def boundary_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for boundary_id, _from_bin, _to_bin in BOUNDARIES:
        sub = [r for r in rows if r["boundary_id"] == boundary_id]
        compact = Counter(str(r["compact_face"]) for r in sub)
        full = Counter(str(r["full_face"]) for r in sub)
        k_counter = Counter(str(r["transition_k"]) for r in sub)
        pre3 = Counter(str(r["pre_k_window_3"]) for r in sub)
        route = Counter(str(r["entry_route"]) for r in sub)
        dom_c, dom_c_count = compact.most_common(1)[0] if compact else ("", 0)
        dom_f, dom_f_count = full.most_common(1)[0] if full else ("", 0)
        waits = [float(r["wait_from_entry"]) for r in sub]
        ks = [float(r["transition_k"]) for r in sub]
        out.append(
            {
                "boundary_id": boundary_id,
                "boundary_label": BOUNDARY_LABELS[boundary_id],
                "count": len(sub),
                "distinct_odd_core_count": len({r["odd_core"] for r in sub}),
                "dominant_compact_face": dom_c,
                "dominant_compact_face_count": dom_c_count,
                "dominant_compact_face_share": dom_c_count / len(sub) if sub else math.nan,
                "number_of_compact_faces": len(compact),
                "compact_face_entropy": entropy(compact),
                "top_10_compact_faces": compact_dist(compact),
                "dominant_full_face": dom_f,
                "dominant_full_face_count": dom_f_count,
                "dominant_full_face_share": dom_f_count / len(sub) if sub else math.nan,
                "number_of_full_faces": len(full),
                "full_face_entropy": entropy(full),
                "top_10_full_faces": compact_dist(full),
                "median_wait_from_entry": safe_median(waits),
                "mean_wait_from_entry": safe_mean(waits),
                "median_transition_k": safe_median(ks),
                "mean_transition_k": safe_mean(ks),
                "transition_k_distribution": compact_dist(k_counter, 20),
                "pre3_distribution": compact_dist(pre3, 20),
                "entry_route_distribution": compact_dist(route, 20),
                "share_k1": sum(1 for r in sub if int(r["transition_k"]) == 1) / len(sub) if sub else math.nan,
                "share_k2": sum(1 for r in sub if int(r["transition_k"]) == 2) / len(sub) if sub else math.nan,
                "share_k3plus": sum(1 for r in sub if int(r["transition_k"]) >= 3) / len(sub) if sub else math.nan,
                "share_pre111": sum(1 for r in sub if r["pre_k_window_3"] == "1,1,1") / len(sub) if sub else math.nan,
                "share_pre113plus": sum(1 for r in sub if r["pre_k_window_3"] == "1,1,3+") / len(sub) if sub else math.nan,
                "share_pre223plus": sum(1 for r in sub if r["pre_k_window_3"] == "2,2,3+") / len(sub) if sub else math.nan,
                "share_has_pre111_since_entry": sum(int(r["has_pre111_since_entry"]) for r in sub) / len(sub) if sub else math.nan,
                "share_maintains_pre111_to_pass": sum(int(r["maintains_pre111_to_pass"]) for r in sub) / len(sub) if sub else math.nan,
            }
        )
    return out


def neighbor_contrasts(rows: list[dict[str, object]], summaries: list[dict[str, object]]) -> list[dict[str, object]]:
    by_summary = {r["boundary_id"]: r for r in summaries}
    out: list[dict[str, object]] = []
    for (a, _af, _at), (b, _bf, _bt) in zip(BOUNDARIES, BOUNDARIES[1:]):
        ar = [r for r in rows if r["boundary_id"] == a]
        br = [r for r in rows if r["boundary_id"] == b]
        out.append(
            {
                "pair": f"{a} vs {b}",
                "left_boundary": a,
                "right_boundary": b,
                "dominant_share_difference": float(by_summary[b]["dominant_compact_face_share"]) - float(by_summary[a]["dominant_compact_face_share"]),
                "compact_face_entropy_difference": float(by_summary[b]["compact_face_entropy"]) - float(by_summary[a]["compact_face_entropy"]),
                "full_face_entropy_difference": float(by_summary[b]["full_face_entropy"]) - float(by_summary[a]["full_face_entropy"]),
                "transition_k_distribution_distance": l1(Counter(str(r["transition_k"]) for r in ar), Counter(str(r["transition_k"]) for r in br)),
                "pre3_distribution_distance": l1(Counter(str(r["pre_k_window_3"]) for r in ar), Counter(str(r["pre_k_window_3"]) for r in br)),
                "entry_route_distribution_distance": l1(Counter(str(r["entry_route"]) for r in ar), Counter(str(r["entry_route"]) for r in br)),
                "share_pre111_difference": float(by_summary[b]["share_pre111"]) - float(by_summary[a]["share_pre111"]),
                "share_maintains_pre111_difference": float(by_summary[b]["share_maintains_pre111_to_pass"]) - float(by_summary[a]["share_maintains_pre111_to_pass"]),
                "share_k1_difference": float(by_summary[b]["share_k1"]) - float(by_summary[a]["share_k1"]),
            }
        )
    return out


def purity_and_mi(sub: list[dict[str, object]], feature: str) -> tuple[int, float, float, float, str]:
    groups: dict[str, Counter[str]] = defaultdict(Counter)
    label_counts = Counter(str(r["64_95_class"]) for r in sub)
    for r in sub:
        groups[normalize_feature_value(r.get(feature))][str(r["64_95_class"])] += 1
    total = len(sub)
    if not total:
        return 0, math.nan, math.nan, math.nan, ""
    largest_group_share = max(sum(c.values()) for c in groups.values()) / total if groups else math.nan
    purity = sum(max(c.values()) for c in groups.values()) / total if groups else math.nan
    mi = 0.0
    for value, c in groups.items():
        group_total = sum(c.values())
        for label, n in c.items():
            if n:
                mi += (n / total) * math.log2((n * total) / (group_total * label_counts[label]))
    top = []
    for value, c in sorted(groups.items(), key=lambda item: -sum(item[1].values()))[:8]:
        top.append(f"{value} -> {dict(c)}")
    return len(groups), largest_group_share, purity, mi, "; ".join(top)


def sorting_power(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    features = [
        "entry_route",
        "transition_k",
        "pre_k_window_3",
        "pre_k_window_5",
        "local_window_4",
        "compact_face",
        "full_face",
        "has_pre111_since_entry",
        "maintains_pre111_to_pass",
        "longest_k1_bucket",
    ]
    enriched = []
    for r in rows:
        rr = dict(r)
        longest = int(rr["longest_k1_run_since_entry"])
        rr["longest_k1_bucket"] = "0" if longest == 0 else ("1-2" if longest <= 2 else ("3-4" if longest <= 4 else "5+"))
        enriched.append(rr)
    out: list[dict[str, object]] = []
    for boundary_id, _from_bin, _to_bin in BOUNDARIES:
        sub = [r for r in enriched if r["boundary_id"] == boundary_id]
        for feature in features:
            ng, largest, purity, mi, top = purity_and_mi(sub, feature)
            out.append(
                {
                    "boundary_id": boundary_id,
                    "feature_name": feature,
                    "number_of_groups": ng,
                    "largest_group_share": largest,
                    "purity_for_64_95_class": purity,
                    "mutual_information_like_score": mi,
                    "top_feature_value_class_distribution": top,
                }
            )
    return out


def class_profiles(rows: list[dict[str, object]]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    profiles: list[dict[str, object]] = []
    distances: list[dict[str, object]] = []
    for boundary_id, _from_bin, _to_bin in BOUNDARIES:
        for cls in MAJOR_CLASSES:
            sub = [r for r in rows if r["boundary_id"] == boundary_id and r["64_95_class"] == cls]
            compact = Counter(str(r["compact_face"]) for r in sub)
            dom, dom_count = compact.most_common(1)[0] if compact else ("", 0)
            profiles.append(
                {
                    "64_95_class": cls,
                    "boundary_id": boundary_id,
                    "count": len(sub),
                    "dominant_compact_face": dom,
                    "dominant_compact_face_share": dom_count / len(sub) if sub else math.nan,
                    "transition_k_distribution": compact_dist(Counter(str(r["transition_k"]) for r in sub), 20),
                    "pre3_distribution": compact_dist(Counter(str(r["pre_k_window_3"]) for r in sub), 20),
                    "entry_route_distribution": compact_dist(Counter(str(r["entry_route"]) for r in sub), 20),
                    "wait_from_entry_median": safe_median([float(r["wait_from_entry"]) for r in sub]),
                    "has_pre111_since_entry_share": sum(int(r["has_pre111_since_entry"]) for r in sub) / len(sub) if sub else math.nan,
                    "maintains_pre111_to_pass_share": sum(int(r["maintains_pre111_to_pass"]) for r in sub) / len(sub) if sub else math.nan,
                }
            )
        for left, right in [("A_start", "A_inflow"), ("A_start", "Other_start"), ("A_inflow", "Other_start")]:
            lrows = [r for r in rows if r["boundary_id"] == boundary_id and r["64_95_class"] == left]
            rrows = [r for r in rows if r["boundary_id"] == boundary_id and r["64_95_class"] == right]
            distances.append(
                {
                    "boundary_id": boundary_id,
                    "class_pair": f"{left} vs {right}",
                    "compact_face_l1": l1(Counter(str(r["compact_face"]) for r in lrows), Counter(str(r["compact_face"]) for r in rrows)),
                    "transition_k_l1": l1(Counter(str(r["transition_k"]) for r in lrows), Counter(str(r["transition_k"]) for r in rrows)),
                    "pre3_l1": l1(Counter(str(r["pre_k_window_3"]) for r in lrows), Counter(str(r["pre_k_window_3"]) for r in rrows)),
                    "entry_route_l1": l1(Counter(str(r["entry_route"]) for r in lrows), Counter(str(r["entry_route"]) for r in rrows)),
                }
            )
    return profiles, distances


def forensic_tables(ids: list[int], words: dict[int, tuple[int, ...]], events_by_id: dict[int, list[dict[str, object]]]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    rows: list[dict[str, object]] = []
    for n in ids:
        events = events_by_id[n]
        word = words[n]
        cls = class_64_95(events)
        if cls == "G0":
            continue
        event, entry_pos = first_boundary_event(events, "64-95", "32-63")
        if event is None or entry_pos is None:
            continue
        pass_pos = int(event["position"])
        segment = [e for e in events if entry_pos <= int(e["position"]) <= pass_pos]
        first_pre = next((int(e["position"]) for e in segment if e["pre_k_window_3"] == "1,1,1"), None)
        last_pre = next((int(e["position"]) for e in reversed(segment) if e["pre_k_window_3"] == "1,1,1"), None)
        break_event = ""
        break_type = ""
        if first_pre is not None:
            for e in segment:
                if int(e["position"]) > first_pre and e["pre_k_window_3"] != "1,1,1":
                    break_event = int(e["position"]) - entry_pos
                    break_type = str(e["pre_k_window_3"])
                    break
        metrics = pre111_metrics(events, entry_pos, pass_pos)
        rows.append(
            {
                "trajectory_id": n,
                "64_95_class": cls,
                "wait": pass_pos - entry_pos,
                "k_sequence": ",".join(str(k) for k in word[entry_pos : pass_pos + 1]),
                "pre3_sequence": " | ".join(str(e["pre_k_window_3"]) for e in segment),
                "local4_sequence": " | ".join(str(e["local_window_4"]) for e in segment),
                "first_pre111_event": "" if first_pre is None else first_pre - entry_pos,
                "last_pre111_event": "" if last_pre is None else last_pre - entry_pos,
                "maintains_pre111_to_pass": metrics["maintains_pre111_to_pass"],
                "break_event_if_any": break_event,
                "break_type_if_any": break_type,
                "pass_face": compact_face(event),
            }
        )
    summary: list[dict[str, object]] = []
    for cls in ["A_start", "A_inflow", "Other_start", "Other_inflow"]:
        sub = [r for r in rows if r["64_95_class"] == cls]
        summary.append(
            {
                "64_95_class": cls,
                "count": len(sub),
                "median_wait": safe_median([float(r["wait"]) for r in sub]),
                "mean_wait": safe_mean([float(r["wait"]) for r in sub]),
                "share_first_pre111_present": sum(1 for r in sub if r["first_pre111_event"] != "") / len(sub) if sub else math.nan,
                "share_maintains_pre111_to_pass": sum(int(r["maintains_pre111_to_pass"]) for r in sub) / len(sub) if sub else math.nan,
                "break_type_counts": compact_dist(Counter(str(r["break_type_if_any"]) for r in sub if r["break_type_if_any"]), 20),
                "pass_face_counts": compact_dist(Counter(str(r["pass_face"]) for r in sub), 20),
            }
        )
    return rows, summary


def build_report(
    summaries: list[dict[str, object]],
    contrasts: list[dict[str, object]],
    power: list[dict[str, object]],
    profiles: list[dict[str, object]],
    distances: list[dict[str, object]],
    forensic_summary: list[dict[str, object]],
) -> str:
    by = {r["boundary_id"]: r for r in summaries}
    most_diffuse = max(summaries, key=lambda r: float(r["compact_face_entropy"]))
    strongest = max(summaries, key=lambda r: float(r["dominant_compact_face_share"]))
    sort_power = [r for r in power if r["boundary_id"] == "B_sort"]
    best_sort_feature = max(sort_power, key=lambda r: float(r["mutual_information_like_score"]))
    downstream_pairs = [r for r in contrasts if r["pair"] in {"B_down1 vs B_down2", "B_down2 vs B_down3", "B_down3 vs B_terminal"}]
    sort_pairs = [r for r in contrasts if r["pair"] in {"B_up vs B_sort", "B_sort vs B_down1"}]
    sort_distance = safe_mean(
        [
            float(r["transition_k_distribution_distance"]) + float(r["pre3_distribution_distance"]) + float(r["entry_route_distribution_distance"])
            for r in sort_pairs
        ]
    )
    downstream_distance = safe_mean(
        [
            float(r["transition_k_distribution_distance"]) + float(r["pre3_distribution_distance"]) + float(r["entry_route_distribution_distance"])
            for r in downstream_pairs
        ]
    )
    class_sep_by_boundary = defaultdict(float)
    for r in distances:
        class_sep_by_boundary[str(r["boundary_id"])] += (
            float(r["compact_face_l1"]) + float(r["transition_k_l1"]) + float(r["pre3_l1"]) + float(r["entry_route_l1"])
        )
    max_sep_boundary = max(class_sep_by_boundary, key=class_sep_by_boundary.get)
    fsum = {r["64_95_class"]: r for r in forensic_summary}

    contrast_answer = (
        "By the raw neighboring-distribution L1 distances, no: downstream boundaries also show large label changes because "
        "`transition_k`, `pre3`, and `entry_route` are boundary-specific labels. The clearer `B_sort` contrast is not larger raw "
        "neighbor distance; it is the combination of moderate face diversity with high 64-95 class separation."
        if sort_distance <= downstream_distance
        else "By the raw neighboring-distribution L1 distances, yes: the two contrasts around `B_sort` are larger on average than the downstream-neighbor contrasts."
    )

    lines = [
        "# Boundary differential report",
        "",
        "Dataset/scanner mode: `original_n_strict`. This report compares observed first-pass descriptors across neighboring remaining_K boundaries. It is descriptive only and does not upgrade the tables into causal or proof-level claims.",
        "",
        "## Direct answers",
        "",
        f"1. Most diffuse boundary: `{most_diffuse['boundary_label']}` by compact-face entropy (`{fmt(most_diffuse['compact_face_entropy'])}`) and `{most_diffuse['number_of_compact_faces']}` compact faces.",
        f"2. Cleanest merged boundary: `{strongest['boundary_label']}` by dominant compact-face share (`{fmt(strongest['dominant_compact_face_share'])}`).",
        "3. `64-95 -> 32-63` stands out observationally because it combines a route split (`START_IN_LAYER` vs `INFLOW_FROM_96-127`) with a local-context split (`pre111` A face vs non-A tails). Its dominant share is not as clean as downstream merged faces, but its class separation is concentrated at the face definition itself.",
        f"4. The standout signal is a combination. In the sorting-power screen, the strongest `B_sort` feature is `{best_sort_feature['feature_name']}` with MI-like score `{fmt(best_sort_feature['mutual_information_like_score'])}` and purity `{fmt(best_sort_feature['purity_for_64_95_class'])}`.",
        f"5. Major classes diverge most at `{max_sep_boundary}` in the class-distance table and then largely reconverge in downstream compact faces, especially where dominant downstream shares approach 1.",
        "6. Upstream `96-127 -> 64-95` does not uniquely identify the later `A_inflow` class. It supplies the route label used later, but the later `64-95 -> 32-63` face still carries the observed A/non-A separation.",
        "7. What remains unexplained: why these descriptors are distributed this way, why low-support tails appear where they do, and whether the same contrasts persist under larger or differently sampled universes.",
        "8. What should not be claimed: avoid causal language, proof-level language, or statements that the boundary imposes downstream fate. The tables only show observed concentration, separation, and reconvergence in this scan.",
        "",
        "## Neighbor contrast reading",
        "",
        f"The summed descriptive distance around `B_sort` is `{fmt(sort_distance)}` versus downstream-neighbor average `{fmt(downstream_distance)}`. {contrast_answer}",
        "",
        "## 64-95 forensic reading",
        "",
    ]
    for cls in ["A_start", "A_inflow", "Other_start", "Other_inflow"]:
        row = fsum.get(cls)
        if row:
            lines.append(
                f"- `{cls}`: count `{row['count']}`, median wait `{fmt(row['median_wait'])}`, pre111 present share `{fmt(row['share_first_pre111_present'])}`, maintains-pre111 share `{fmt(row['share_maintains_pre111_to_pass'])}`."
            )
    lines.extend(
        [
            "",
            "Within `B_sort`, A_start and A_inflow are exactly the rows where the all-1 local context is present at pass (`k=1`, `pre3=1,1,1`) and the route differs. Other_start and Other_inflow are the observed complement at the same boundary. This is an association in the first-pass descriptor table, not a mechanism statement.",
            "",
            "## Compact boundary table",
            "",
            "| Boundary | role | dominant face | diversity | class separation | reading |",
            "| --- | --- | --- | ---: | ---: | --- |",
        ]
    )
    roles = {
        "B_up": "feeder",
        "B_sort": "sorting face",
        "B_down1": "merged downstream",
        "B_down2": "merged downstream",
        "B_down3": "merged downstream",
        "B_terminal": "terminal drop",
    }
    readings = {
        "B_up": "diffuse upstream surface; route evidence is weak as a standalone separator",
        "B_sort": "route plus pre111/local-context split is concentrated here",
        "B_down1": "mostly merged into a common downstream face",
        "B_down2": "near-clean downstream continuation",
        "B_down3": "near-clean downstream continuation with small START tails",
        "B_terminal": "direct terminal drop for most rows",
    }
    for boundary_id, _from_bin, _to_bin in BOUNDARIES:
        row = by[boundary_id]
        lines.append(
            f"| `{row['boundary_label']}` | {roles[boundary_id]} | `{row['dominant_compact_face']}` | "
            f"{fmt(row['compact_face_entropy'])} | {fmt(class_sep_by_boundary[boundary_id])} | {readings[boundary_id]} |"
        )
    lines.extend(
        [
            "",
            "## Output files",
            "",
            "- `boundary_diff_step1_unified_events.csv`",
            "- `boundary_diff_step2_boundary_feature_summary.csv`",
            "- `boundary_diff_step3_neighbor_contrasts.csv`",
            "- `boundary_diff_step4_sorting_power.csv`",
            "- `boundary_diff_step5_class_trajectory_profiles.csv`",
            "- `boundary_diff_step5_class_distance_by_boundary.csv`",
            "- `boundary_diff_step6_64_95_forensic_timeline.csv`",
            "- `boundary_diff_step6_64_95_forensic_summary.csv`",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    OUT.mkdir(exist_ok=True)
    classified = pd.read_csv(CLASSIFICATION)
    universe = classified[classified["mode"] == "original_n_strict"].copy()
    ids = sorted(int(x) for x in universe["n_original"].unique())
    if len(ids) != 550:
        raise RuntimeError(f"expected 550 original_n_strict trajectories, got {len(ids)}")

    event_rows, words, events_by_id = make_event_rows(ids)
    summaries = boundary_summary(event_rows)
    contrasts = neighbor_contrasts(event_rows, summaries)
    power = sorting_power(event_rows)
    profiles, distances = class_profiles(event_rows)
    forensic_rows, forensic_summary = forensic_tables(ids, words, events_by_id)

    write_csv(OUT / "boundary_diff_step1_unified_events.csv", event_rows)
    write_csv(OUT / "boundary_diff_step2_boundary_feature_summary.csv", summaries)
    write_csv(OUT / "boundary_diff_step3_neighbor_contrasts.csv", contrasts)
    write_csv(OUT / "boundary_diff_step4_sorting_power.csv", power)
    write_csv(OUT / "boundary_diff_step5_class_trajectory_profiles.csv", profiles)
    write_csv(OUT / "boundary_diff_step5_class_distance_by_boundary.csv", distances)
    write_csv(OUT / "boundary_diff_step6_64_95_forensic_timeline.csv", forensic_rows)
    write_csv(OUT / "boundary_diff_step6_64_95_forensic_summary.csv", forensic_summary)
    (OUT / "boundary_differential_report.md").write_text(
        build_report(summaries, contrasts, power, profiles, distances, forensic_summary),
        encoding="utf-8",
    )
    print(OUT / "boundary_differential_report.md")


if __name__ == "__main__":
    main()
