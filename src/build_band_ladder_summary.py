from __future__ import annotations

import csv
import math
from collections import Counter
from pathlib import Path

import pandas as pd


ROOT = Path(r"C:\Users\yauki\Documents\Codex\2026-06-28\task-first-pass-face-analysis-for")
OUT = ROOT / "outputs"
OLD_OUT = Path(r"C:\Users\yauki\Documents\Codex\2026-06-27\task-analyze-the-12-trajectories-that\outputs")
LOW_SUPPORT_N = 10


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame()
    return pd.read_csv(path)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def fmt_share(num: int, den: int) -> str:
    if den == 0:
        return "NA"
    return f"{num / den:.3f}"


def face_from_row(row: pd.Series) -> str:
    return f"{row['entry_route']} | k={row['transition_k']} | pre3={row['pre_k_window_3']}"


def summarize_compact_counts(df: pd.DataFrame) -> Counter[str]:
    counts: Counter[str] = Counter()
    if df.empty:
        return counts
    for _, row in df.iterrows():
        counts[face_from_row(row)] += int(row["count"])
    return counts


def secondary_faces(counts: Counter[str], limit: int = 4) -> str:
    items = counts.most_common()[1 : limit + 1]
    if not items:
        return ""
    return "; ".join(
        f"{face}: {count}{' LOW_SUPPORT' if count < LOW_SUPPORT_N else ''}" for face, count in items
    )


def clean_label(counts: Counter[str], pass_count: int, full_count: int, absent: bool = False) -> str:
    if absent:
        return "absent"
    if pass_count == 0 or not counts:
        return "absent"
    top_count = counts.most_common(1)[0][1]
    share = top_count / pass_count
    if share >= 0.98 and full_count <= 6:
        return "clean"
    if share >= 0.90:
        return "near-universal with low-support tail"
    return "diffuse"


def role_label(transition: str, counts: Counter[str], pass_count: int, absent: bool = False) -> str:
    if absent:
        return "absent transition"
    if transition == "96-127 -> 64-95":
        return "upstream diffuse feeder"
    if transition == "64-95 -> 32-63":
        return "main sorting face"
    if transition == "4-7 -> 0-1":
        return "terminal direct drop"
    return "merged downstream face"


def row_from_counts(
    transition: str,
    entered: int,
    passed: int,
    counts: Counter[str],
    full_count: int,
    absent: bool = False,
) -> dict[str, object]:
    if counts:
        dom_face, dom_count = counts.most_common(1)[0]
    else:
        dom_face, dom_count = "", 0
    return {
        "band_transition": transition,
        "entered_from_bin_count": entered,
        "first_pass_count": passed,
        "first_pass_share": fmt_share(passed, entered),
        "dominant_compact_face": dom_face,
        "dominant_face_count": dom_count,
        "dominant_face_share": fmt_share(dom_count, passed),
        "secondary_faces": secondary_faces(counts),
        "clean_or_diffuse": clean_label(counts, passed, full_count, absent=absent),
        "role_label": role_label(transition, counts, passed, absent=absent),
    }


def previous_class_counts_64() -> Counter[str]:
    df = read_csv(OLD_OUT / "postpass_step1_first_pass_classes.csv")
    counts = Counter(df["pass_face_class"]) if not df.empty else Counter()
    counts["G0"] = 12
    return counts


def link_share(path: Path, source_col: str, face_col: str, source: str, denominator: int | None = None) -> str:
    df = read_csv(path)
    if df.empty:
        return "0/0 NA"
    sub = df[df[source_col] == source].copy()
    if sub.empty:
        den = denominator if denominator is not None else 0
        return f"0/{den} NA"
    if denominator is None:
        denominator = int(sub["source_total"].iloc[0]) if "source_total" in sub.columns else int(sub["previous_class_total"].iloc[0])
    top = sub.sort_values("count", ascending=False).iloc[0]
    count = int(top["count"])
    face = str(top[face_col])
    flag = " LOW_SUPPORT" if count < LOW_SUPPORT_N or denominator < LOW_SUPPORT_N else ""
    return f"{face}: {count}/{denominator} ({fmt_share(count, denominator)}){flag}"


def class_4_7_outcome(source: str, denominator: int) -> str:
    df = read_csv(OUT / "downstream4_step1_first_pass_table.csv")
    sub = df[df["previous_64_95_face_class"] == source] if not df.empty else pd.DataFrame()
    if sub.empty:
        return f"no rows: 0/{denominator}"
    counts = Counter(sub["first_4_7_transition"])
    parts = []
    for transition, count in counts.most_common():
        flag = " LOW_SUPPORT" if count < LOW_SUPPORT_N or denominator < LOW_SUPPORT_N else ""
        parts.append(f"{transition}: {count}/{denominator} ({fmt_share(count, denominator)}){flag}")
    return "; ".join(parts)


def make_simple_png(summary_rows: list[dict[str, object]]) -> None:
    try:
        import matplotlib.pyplot as plt
    except Exception:
        plt = None

    if plt is None:
        from PIL import Image, ImageDraw, ImageFont

        display_rows = [r for r in summary_rows if r["band_transition"] != "4-7 -> 2-3"]
        width = 1450
        row_h = 135
        height = 165 + row_h * len(display_rows)
        img = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(img)
        try:
            title_font = ImageFont.truetype("arial.ttf", 32)
            label_font = ImageFont.truetype("arial.ttf", 22)
            text_font = ImageFont.truetype("arial.ttf", 25)
            small_font = ImageFont.truetype("arial.ttf", 19)
        except Exception:
            title_font = ImageFont.load_default()
            label_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
            small_font = ImageFont.load_default()

        colors = {
            "feeder": "#d8892f",
            "selection": "#2f6fbd",
            "convergence": "#2f9e73",
            "termination": "#8a5fbf",
        }
        stage_by_role = {
            "upstream diffuse feeder": "feeder",
            "main sorting face": "selection",
            "merged downstream face": "convergence",
            "terminal direct drop": "termination",
        }

        draw.text((46, 32), "Observed first-pass band ladder", fill="#222222", font=title_font)
        draw.text(
            (46, 74),
            "Scanner: original_n_strict. Counts separate first-pass coverage from representative face counts.",
            fill="#555555",
            font=small_font,
        )
        x_dot = 235
        x_text = 295
        x_stage = 45
        x_arrow = 1290
        top = 125

        draw.line((x_arrow, top + 40, x_arrow, top + row_h * (len(display_rows) - 1) + 46), fill="#c7c7c7", width=5)
        draw.polygon(
            [
                (x_arrow - 14, top + row_h * (len(display_rows) - 1) + 46),
                (x_arrow + 14, top + row_h * (len(display_rows) - 1) + 46),
                (x_arrow, top + row_h * (len(display_rows) - 1) + 72),
            ],
            fill="#c7c7c7",
        )
        draw.text((x_arrow - 90, top - 14), "flow", fill="#777777", font=small_font)

        for idx, row in enumerate(display_rows):
            y = top + idx * row_h
            role = str(row["role_label"])
            stage = stage_by_role.get(role, "convergence")
            color = colors.get(stage, "#777777")
            if idx < len(display_rows) - 1:
                draw.line((x_dot, y + 46, x_dot, y + row_h + 12), fill="#d0d0d0", width=5)
            draw.rounded_rectangle((x_stage, y + 18, x_stage + 155, y + 58), radius=12, fill=color)
            draw.text((x_stage + 16, y + 28), stage, fill="white", font=label_font)
            draw.ellipse((x_dot - 20, y + 20, x_dot + 20, y + 60), fill=color)

            transition = str(row["band_transition"])
            entered = int(row["entered_from_bin_count"])
            first_pass = int(row["first_pass_count"])
            dominant_count = int(row["dominant_face_count"])
            face = str(row["dominant_compact_face"] or "no observed pass")

            draw.text((x_text, y + 8), transition, fill="#111111", font=text_font)
            if transition == "64-95 -> 32-63":
                draw.text((x_text, y + 43), "first pass: 538/538", fill="#333333", font=small_font)
                draw.text(
                    (x_text, y + 72),
                    "classes: A_start 365 | A_inflow 104 | Other_start 66 | Other_inflow 3",
                    fill="#333333",
                    font=small_font,
                )
                draw.text(
                    (x_text, y + 101),
                    "representative face: A_start, k=1/pre111 (365/538)",
                    fill="#555555",
                    font=small_font,
                )
            elif transition == "4-7 -> 0-1":
                draw.text((x_text, y + 43), f"terminal direct drop: {first_pass}/{entered}", fill="#333333", font=small_font)
                draw.text((x_text, y + 72), "side outcome: 4-7 stay 5/550 (low support)", fill="#555555", font=small_font)
                draw.text((x_text, y + 101), "target 4-7 -> 2-3 was absent in this scan", fill="#555555", font=small_font)
            else:
                draw.text((x_text, y + 43), f"first pass: {first_pass}/{entered}", fill="#333333", font=small_font)
                draw.text(
                    (x_text, y + 72),
                    f"dominant face: {face} ({dominant_count}/{first_pass})",
                    fill="#333333",
                    font=small_font,
                )
                tail_note = {
                    "96-127 -> 64-95": "tail: diffuse low-support candidate faces",
                    "32-63 -> 16-31": "tail: START route 7/545 (low support)",
                    "16-31 -> 8-15": "tail: START route 1/546 (low support)",
                    "8-15 -> 4-7": "tail: low-support START/k=2 variants, 5/550 total",
                }.get(transition, "")
                if tail_note:
                    draw.text((x_text, y + 101), tail_note, fill="#666666", font=small_font)
        img.save(OUT / "band_ladder_summary.png")
        return

    fig, ax = plt.subplots(figsize=(11, 5.5))
    ax.axis("off")
    y_positions = list(range(len(summary_rows)))[::-1]
    for y, row in zip(y_positions, summary_rows):
        role = row["role_label"]
        if role == "main sorting face":
            color = "#2f6fbd"
        elif role == "merged downstream face":
            color = "#2f9e73"
        elif role == "terminal direct drop":
            color = "#8a5fbf"
        elif role == "absent transition":
            color = "#9a9a9a"
        else:
            color = "#d8892f"
        ax.scatter([0.05], [y], s=260, color=color)
        label = (
            f"{row['band_transition']}  "
            f"{row['dominant_compact_face'] or 'no observed pass'}  "
            f"[{row['dominant_face_count']}/{row['first_pass_count']}]"
        )
        ax.text(0.1, y, label, va="center", fontsize=10)
        if y > 0:
            ax.plot([0.05, 0.05], [y - 0.82, y - 0.18], color="#cccccc", linewidth=2)
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.7, len(summary_rows) - 0.3)
    ax.set_title("Band ladder first-pass summary (observational)", fontsize=14, loc="left")
    fig.tight_layout()
    fig.savefig(OUT / "band_ladder_summary.png", dpi=180)
    plt.close(fig)


def main() -> None:
    OUT.mkdir(exist_ok=True)

    summary_rows: list[dict[str, object]] = []

    up96_step1 = read_csv(OUT / "upstream96_step1_first_pass_table.csv")
    up96_counts = summarize_compact_counts(read_csv(OUT / "upstream96_step2_signature_counts.csv"))
    summary_rows.append(row_from_counts("96-127 -> 64-95", len(up96_step1), int(up96_step1["has_96_127_to_64_95"].sum()), up96_counts, len(read_csv(OUT / "upstream96_step2_signature_counts.csv"))))

    post64 = read_csv(OLD_OUT / "postpass_step1_first_pass_classes.csv")
    c64 = Counter()
    if not post64.empty:
        for cls, count in Counter(post64["pass_face_class"]).items():
            if cls == "A_start":
                c64["START_IN_LAYER | k=1 | pre3=1,1,1"] += count
            elif cls == "A_inflow":
                c64["INFLOW_FROM_96-127 | k=1 | pre3=1,1,1"] += count
            elif cls == "Other_start":
                c64["START_IN_LAYER | non-A compact tail"] += count
            elif cls == "Other_inflow":
                c64["INFLOW_FROM_96-127 | non-A compact tail"] += count
    summary_rows.append(row_from_counts("64-95 -> 32-63", len(post64), len(post64), c64, 4))

    for transition, prefix, has_col in [
        ("32-63 -> 16-31", "downstream32", "has_32_63_to_16_31"),
        ("16-31 -> 8-15", "downstream16", "has_16_31_to_8_15"),
        ("8-15 -> 4-7", "downstream8", "has_8_15_to_4_7"),
    ]:
        step1 = read_csv(OUT / f"{prefix}_step1_first_pass_table.csv")
        sig = read_csv(OUT / f"{prefix}_step2_signature_counts.csv")
        counts = summarize_compact_counts(sig)
        summary_rows.append(row_from_counts(transition, len(step1), int(step1[has_col].sum()), counts, len(sig)))

    step4 = read_csv(OUT / "downstream4_step1_first_pass_table.csv")
    summary_rows.append(row_from_counts("4-7 -> 2-3", len(step4), int(step4["has_4_7_to_2_3"].sum()), Counter(), 0, absent=True))
    entry_counts = Counter(step4["first_4_7_transition"]) if not step4.empty else Counter()
    direct_counts = Counter({"4-7 -> 0-1": entry_counts["4-7 -> 0-1"], "4-7 -> 4-7": entry_counts["4-7 -> 4-7"]})
    summary_rows.append(row_from_counts("4-7 -> 0-1", len(step4), entry_counts["4-7 -> 0-1"], direct_counts, len(direct_counts)))

    write_csv(OUT / "band_ladder_summary.csv", summary_rows)

    class_counts = previous_class_counts_64()
    class_rows: list[dict[str, object]] = []
    for cls in ["A_start", "A_inflow", "Other_start", "Other_inflow", "G0"]:
        denominator = int(class_counts[cls])
        class_rows.append(
            {
                "class": cls,
                "count": denominator,
                "64-95 -> 32-63 class": cls if cls != "G0" else "G0 / no 64-95 entry",
                "32-63 -> 16-31 dominant face share": link_share(
                    OUT / "downstream32_step4_link_from_64_95_face.csv",
                    "previous_64_95_face_class",
                    "downstream32_first_pass_face",
                    cls,
                    denominator=denominator,
                ),
                "16-31 -> 8-15 dominant face share": link_share(
                    OUT / "downstream16_step4_link_from_64_95_class.csv",
                    "previous_64_95_face_class",
                    "downstream16_first_pass_face",
                    cls,
                    denominator=denominator,
                ),
                "8-15 -> 4-7 dominant face share": link_share(
                    OUT / "downstream8_step4_link_from_64_95_class.csv",
                    "previous_64_95_face_class",
                    "downstream8_first_pass_face",
                    cls,
                    denominator=denominator,
                ),
                "4-7 -> 0-1 / 4-7 stay outcome if available": class_4_7_outcome(cls, denominator),
            }
        )
    write_csv(OUT / "band_ladder_class_propagation.csv", class_rows)

    report = [
        "# Band ladder summary",
        "",
        "Dataset and scanner mode: `original_n_strict`. This report integrates existing CSV/report outputs only; it does not rescan trajectories.",
        "",
        "All statements are observational summaries of this finite scan. They are not mechanism claims or proof claims.",
        "",
        "## Main Summary",
        "",
        "| band_transition | entered | first_pass | dominant_compact_face | dominant_share | role |",
        "| --- | ---: | ---: | --- | ---: | --- |",
    ]
    for row in summary_rows:
        report.append(
            f"| `{row['band_transition']}` | {row['entered_from_bin_count']} | {row['first_pass_count']} | "
            f"`{row['dominant_compact_face'] or 'none'}` | {row['dominant_face_share']} | {row['role_label']} |"
        )

    report.extend(
        [
            "",
            "## Answers",
            "",
            "1. The main split is at `64-95 -> 32-63`: this is where the named A_start / A_inflow / Other_start / Other_inflow classes are defined. The upstream `96-127 -> 64-95` surface is more diffuse.",
            "2. The merged downstream faces are `32-63 -> 16-31`, `16-31 -> 8-15`, and the main part of `8-15 -> 4-7`. A_start, A_inflow, and Other_start stay merged across these rows in the observed tables.",
            "3. The k/pre3 face changes by band: `64-95 -> 32-63` is led by k=1/pre111, `32-63 -> 16-31` by k=3/pre113+, `16-31 -> 8-15` by k=4/pre223+, and `8-15 -> 4-7` by k=5/pre113+.",
            "4. The ladder terminates at the first `4-7` entry in this scan: the requested `4-7 -> 2-3` transition is absent, while `545/550` rows go directly `4-7 -> 0-1`.",
            "5. A compact descriptive name would be `observed first-pass band ladder`: a main sorting face at `64-95 -> 32-63`, followed by merged downstream faces and a terminal direct drop.",
            "",
            "## Support Notes",
            "",
            "- Low-support threshold used in source analyses: count < 10.",
            "- G0 remains the small, least stable group: it partly merges downstream but also carries the low-support side outcomes near the bottom of the ladder.",
            "- Empty link tables for `4-7 -> 2-3` reflect an absent target transition, not a failed calculation.",
            "",
            "## Output Files",
            "",
            "- `band_ladder_summary.csv`",
            "- `band_ladder_class_propagation.csv`",
            "- `band_ladder_summary.png`",
        ]
    )
    (OUT / "band_ladder_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    make_simple_png(summary_rows)


if __name__ == "__main__":
    main()
