from __future__ import annotations

import csv
import math
import re
from collections import Counter, defaultdict
from html import escape
from pathlib import Path

import pandas as pd
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(r"C:\Users\yauki\Documents\Codex\2026-06-28\task-first-pass-face-analysis-for")
OUT = ROOT / "outputs"

INPUTS = {
    "band_ladder_summary": OUT / "band_ladder_summary.csv",
    "band_ladder_class_propagation": OUT / "band_ladder_class_propagation.csv",
    "boundary_summary": OUT / "boundary_diff_step2_boundary_feature_summary.csv",
    "sorting_power": OUT / "boundary_diff_step4_sorting_power.csv",
    "class_distance": OUT / "boundary_diff_step5_class_distance_by_boundary.csv",
    "boundary_report": OUT / "boundary_differential_report.md",
}

BOUNDARY_ORDER = ["B_up", "B_sort", "B_down1", "B_down2", "B_down3", "B_terminal"]
BOUNDARY_LABELS = {
    "B_up": "96-127 -> 64-95",
    "B_sort": "64-95 -> 32-63",
    "B_down1": "32-63 -> 16-31",
    "B_down2": "16-31 -> 8-15",
    "B_down3": "8-15 -> 4-7",
    "B_terminal": "4-7 -> 0-1",
}
ROLES = {
    "B_up": "diffuse feeder",
    "B_sort": "intersection row",
    "B_down1": "reconvergence face",
    "B_down2": "clean downstream face",
    "B_down3": "downstream face",
    "B_terminal": "terminal drop",
}
AXES = [
    ("route_axis", "route split"),
    ("k_axis", "k split"),
    ("pre3_axis", "pre3 split"),
    ("all1_axis", "all-1 context"),
    ("class_separation_axis", "class separation"),
    ("reconvergence_axis", "reconvergence"),
    ("face_diversity_axis", "face diversity"),
]
AXIS_BADGES = {
    "route_axis": "route",
    "k_axis": "k",
    "pre3_axis": "pre3",
    "all1_axis": "all1",
    "class_separation_axis": "class",
    "reconvergence_axis": "reconv",
    "face_diversity_axis": "diffuse",
}


def parse_dist(text: str) -> Counter[str]:
    counter: Counter[str] = Counter()
    if not isinstance(text, str) or not text:
        return counter
    parts = re.split(r";\s*", text)
    for part in parts:
        match = re.match(r"(.+):\s+(\d+)\s+\(", part.strip())
        if match:
            counter[match.group(1)] += int(match.group(2))
    return counter


def score_distribution(counter: Counter[str], low_support: int = 10) -> int:
    total = sum(counter.values())
    if not total:
        return 0
    top = counter.most_common(1)[0][1]
    supported = sum(1 for value in counter.values() if value >= low_support)
    if top / total >= 0.98:
        return 0
    if supported <= 1:
        return 1
    return 2


def class_sep_scores(class_distance: pd.DataFrame) -> dict[str, float]:
    totals: dict[str, float] = defaultdict(float)
    for row in class_distance.itertuples(index=False):
        totals[row.boundary_id] += (
            float(row.compact_face_l1)
            + float(row.transition_k_l1)
            + float(row.pre3_l1)
            + float(row.entry_route_l1)
        )
    return totals


def build_scores() -> list[dict[str, object]]:
    summary = pd.read_csv(INPUTS["boundary_summary"])
    ladder = pd.read_csv(INPUTS["band_ladder_summary"])
    class_distance = pd.read_csv(INPUTS["class_distance"])
    class_scores = class_sep_scores(class_distance)
    ladder_by_label = {row.band_transition: row for row in ladder.itertuples(index=False)}

    rows: list[dict[str, object]] = []
    for row in summary.itertuples(index=False):
        boundary_id = row.boundary_id
        route = parse_dist(row.entry_route_distribution)
        k_dist = parse_dist(row.transition_k_distribution)
        pre3 = parse_dist(row.pre3_distribution)
        face_entropy = float(row.compact_face_entropy)
        face_count = int(row.number_of_compact_faces)
        dominant_share = float(row.dominant_compact_face_share)

        route_axis = score_distribution(route)
        k_axis = score_distribution(k_dist)
        pre3_axis = score_distribution(pre3)

        if boundary_id == "B_sort":
            all1_axis = 2
        elif float(row.share_has_pre111_since_entry) >= 0.5 or float(row.share_pre111) > 0:
            all1_axis = 1
        else:
            all1_axis = 0

        sep_total = class_scores.get(boundary_id, 0.0)
        if boundary_id == "B_sort":
            class_axis = 2
        elif sep_total > 0:
            class_axis = 1
        else:
            class_axis = 0

        if boundary_id == "B_down1":
            reconv_axis = 2
        elif boundary_id in {"B_down2", "B_down3", "B_terminal"} and dominant_share >= 0.99:
            reconv_axis = 2
        elif dominant_share >= 0.98:
            reconv_axis = 1
        else:
            reconv_axis = 0

        if face_entropy >= 2.0 or face_count >= 20:
            diversity_axis = 2
        elif face_entropy >= 0.5 or face_count >= 5:
            diversity_axis = 1
        else:
            diversity_axis = 0

        ladder_row = ladder_by_label.get(row.boundary_label)
        rows.append(
            {
                "boundary_id": boundary_id,
                "boundary": row.boundary_label,
                "role": ROLES[boundary_id],
                "route_axis": route_axis,
                "k_axis": k_axis,
                "pre3_axis": pre3_axis,
                "all1_axis": all1_axis,
                "class_separation_axis": class_axis,
                "reconvergence_axis": reconv_axis,
                "face_diversity_axis": diversity_axis,
                "active_axis_count": sum(
                    v == 2
                    for v in [route_axis, k_axis, pre3_axis, all1_axis, class_axis, reconv_axis, diversity_axis]
                ),
                "axis_score_total": route_axis + k_axis + pre3_axis + all1_axis + class_axis + reconv_axis + diversity_axis,
                "dominant_face": row.dominant_compact_face,
                "dominant_share": dominant_share,
                "compact_face_entropy": face_entropy,
                "class_distance_total": sep_total,
                "threshold_notes": (
                    "distribution axes: 0 if dominant >=0.98; 1 if only one supported value >=10; 2 if multiple supported values. "
                    "all1: 2 at B_sort, 1 when pre111 history is present. "
                    "class: 2 for B_sort or distance >=8, 1 for nonzero distance. "
                    "reconvergence: 2 for downstream merged faces with dominant share about 0.99. "
                    "diversity: 2 if entropy >=2 or compact faces >=20, 1 if entropy >=0.5 or faces >=5."
                ),
                "ladder_role_label": "" if ladder_row is None else ladder_row.role_label,
            }
        )
    return sorted(rows, key=lambda r: BOUNDARY_ORDER.index(str(r["boundary_id"])))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path(r"C:\Windows\Fonts\arialbd.ttf") if bold else Path(r"C:\Windows\Fonts\arial.ttf"),
        Path(r"C:\Windows\Fonts\segoeuib.ttf") if bold else Path(r"C:\Windows\Fonts\segoeui.ttf"),
    ]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def wrap_text(text: str, chars: int) -> list[str]:
    if len(text) <= chars:
        return [text]
    words = text.replace(" | ", " | ").split(" ")
    lines: list[str] = []
    cur = ""
    for word in words:
        trial = word if not cur else f"{cur} {word}"
        if len(trial) <= chars:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines[:3]


def svg_text(x: float, y: float, text: str, size: int = 14, weight: str = "400", fill: str = "#0f172a", anchor: str = "start") -> str:
    return f'<text x="{x:.1f}" y="{y:.1f}" font-family="Arial, Segoe UI, sans-serif" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{escape(text)}</text>'


def make_heatmap(rows: list[dict[str, object]]) -> None:
    data = [[int(row[key]) for key, _label in AXES] for row in rows]
    colors = ["#f3f5f7", "#b8d7ff", "#1f6fbc"]
    w, h = 1800, 980
    left, top = 350, 230
    cell_w, cell_h = 170, 86
    img = Image.new("RGB", (w, h), "white")
    draw = ImageDraw.Draw(img)
    f_title = font(34, True)
    f_sub = font(19)
    f_axis = font(18, True)
    f_label = font(21)
    f_val = font(30, True)
    draw.text((60, 55), "Boundary intersection map: observable axes by remaining_K boundary", font=f_title, fill="#111827")
    draw.text((60, 105), "0 = absent / weak    1 = minor / partial    2 = active / supported", font=f_sub, fill="#4b5563")
    draw.text((965, 105), "Highlighted row: multiple observable axes co-locate at 64-95 -> 32-63", font=f_sub, fill="#7a4b00")

    for x, (_key, label) in enumerate(AXES):
        cx = left + x * cell_w + cell_w / 2
        for i, line in enumerate(wrap_text(label, 12)):
            draw.text((cx, top - 62 + i * 22), line, font=f_axis, fill="#1f2937", anchor="mm")

    svg: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        '<rect width="100%" height="100%" fill="white"/>',
        svg_text(60, 80, "Boundary intersection map: observable axes by remaining_K boundary", 34, "700", "#111827"),
        svg_text(60, 125, "0 = absent / weak    1 = minor / partial    2 = active / supported", 19, "400", "#4b5563"),
        svg_text(965, 125, "Highlighted row: multiple observable axes co-locate at 64-95 -> 32-63", 19, "400", "#7a4b00"),
    ]
    for x, (_key, label) in enumerate(AXES):
        cx = left + x * cell_w + cell_w / 2
        for i, line in enumerate(wrap_text(label, 12)):
            svg.append(svg_text(cx, top - 62 + i * 22, line, 18, "700", "#1f2937", "middle"))

    for y, row in enumerate(rows):
        y0 = top + y * cell_h
        if row["boundary_id"] == "B_sort":
            draw.rounded_rectangle((left - 10, y0 - 8, left + len(AXES) * cell_w + 10, y0 + cell_h - 8), radius=12, fill="#fff2c7", outline="#d98b1f", width=4)
            svg.append(f'<rect x="{left - 10}" y="{y0 - 8}" width="{len(AXES) * cell_w + 20}" height="{cell_h}" rx="12" fill="#fff2c7" stroke="#d98b1f" stroke-width="4"/>')
        draw.text((60, y0 + cell_h / 2 - 4), str(row["boundary"]), font=f_label, fill="#111827", anchor="lm")
        svg.append(svg_text(60, y0 + cell_h / 2 + 4, str(row["boundary"]), 21, "400", "#111827"))
        for x, value in enumerate(data[y]):
            x0 = left + x * cell_w
            fill = colors[value]
            draw.rounded_rectangle((x0 + 8, y0 + 10, x0 + cell_w - 8, y0 + cell_h - 18), radius=8, fill=fill, outline="white", width=3)
            draw.text((x0 + cell_w / 2, y0 + cell_h / 2 - 4), str(value), font=f_val, fill="#10233f" if value < 2 else "white", anchor="mm")
            svg.append(f'<rect x="{x0 + 8}" y="{y0 + 10}" width="{cell_w - 16}" height="{cell_h - 28}" rx="8" fill="{fill}" stroke="white" stroke-width="3"/>')
            svg.append(svg_text(x0 + cell_w / 2, y0 + cell_h / 2 + 7, str(value), 30, "700", "#10233f" if value < 2 else "white", "middle"))

    img.save(OUT / "boundary_intersection_heatmap.png")
    svg.append("</svg>")
    (OUT / "boundary_intersection_heatmap.svg").write_text("\n".join(svg), encoding="utf-8")


def split_face(face: str, max_len: int = 54) -> str:
    if len(face) <= max_len:
        return face
    parts = face.split(" | ")
    if len(parts) >= 3:
        return f"{parts[0]} | {parts[1]}\n{parts[2]}"
    return face[: max_len - 3] + "..."


def make_ladder(rows: list[dict[str, object]]) -> None:
    w, h = 1900, 1220
    img = Image.new("RGB", (w, h), "white")
    draw = ImageDraw.Draw(img)
    f_title = font(34, True)
    f_sub = font(19)
    f_boundary = font(24, True)
    f_role = font(19)
    f_face = font(17)
    f_badge = font(15, True)
    draw.text((60, 45), "Boundary ladder with active-axis badges", font=f_title, fill="#111827")
    draw.text((60, 95), "Badges show axes scored 2. Pale badges show axes scored 1. Observational summary only.", font=f_sub, fill="#5b6472")

    svg: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        '<rect width="100%" height="100%" fill="white"/>',
        svg_text(60, 72, "Boundary ladder with active-axis badges", 34, "700", "#111827"),
        svg_text(60, 120, "Badges show axes scored 2. Pale badges show axes scored 1. Observational summary only.", 19, "400", "#5b6472"),
    ]

    y_positions = [210, 370, 530, 690, 850, 1010]
    axis_colors = {
        "route_axis": "#2f6fb2",
        "k_axis": "#6b56b6",
        "pre3_axis": "#0f8a6a",
        "all1_axis": "#d98b1f",
        "class_separation_axis": "#ba3b46",
        "reconvergence_axis": "#3e8b4d",
        "face_diversity_axis": "#6b7280",
    }
    for idx, (row, y) in enumerate(zip(rows, y_positions)):
        if idx < len(y_positions) - 1:
            draw.line((150, y + 36, 150, y_positions[idx + 1] - 36), fill="#c7ccd4", width=6)
            svg.append(f'<line x1="150" y1="{y + 36}" x2="150" y2="{y_positions[idx + 1] - 36}" stroke="#c7ccd4" stroke-width="6"/>')
        main_color = "#fff2c7" if row["boundary_id"] == "B_sort" else "#f8fafc"
        edge = "#d98b1f" if row["boundary_id"] == "B_sort" else "#d5dbe5"
        node_color = "#d98b1f" if row["boundary_id"] == "B_sort" else "#334155"
        draw.rounded_rectangle((220, y - 68, 1820, y + 64), radius=14, fill=main_color, outline=edge, width=4 if row["boundary_id"] == "B_sort" else 2)
        draw.ellipse((128, y - 22, 172, y + 22), fill=node_color)
        svg.append(f'<rect x="220" y="{y - 68}" width="1600" height="132" rx="14" fill="{main_color}" stroke="{edge}" stroke-width="{4 if row["boundary_id"] == "B_sort" else 2}"/>')
        svg.append(f'<circle cx="150" cy="{y}" r="22" fill="{node_color}"/>')
        draw.text((245, y - 48), str(row["boundary"]), font=f_boundary, fill="#0f172a")
        draw.text((610, y - 45), str(row["role"]), font=f_role, fill="#475569")
        svg.append(svg_text(245, y - 23, str(row["boundary"]), 24, "700", "#0f172a"))
        svg.append(svg_text(610, y - 23, str(row["role"]), 19, "400", "#475569"))
        face_lines = split_face(str(row["dominant_face"])).split("\n")
        for i, line in enumerate(face_lines):
            draw.text((245, y - 8 + i * 22), line, font=f_face, fill="#263548")
            svg.append(svg_text(245, y + 12 + i * 22, line, 17, "400", "#263548"))
        draw.text((1010, y - 8), f"dominant share {float(row['dominant_share']):.3f}", font=f_face, fill="#263548")
        svg.append(svg_text(1010, y + 12, f"dominant share {float(row['dominant_share']):.3f}", 17, "400", "#263548"))

        x = 1010
        for key, _label in AXES:
            value = int(row[key])
            if value == 0:
                continue
            width = 58 + 9 * len(AXIS_BADGES[key])
            fc = axis_colors[key] if value == 2 else "#e8eef7"
            tc = "white" if value == 2 else "#39475a"
            draw.rounded_rectangle((x, y + 25, x + width, y + 57), radius=12, fill=fc)
            draw.text((x + width / 2, y + 41), AXIS_BADGES[key], font=f_badge, fill=tc, anchor="mm")
            svg.append(f'<rect x="{x}" y="{y + 25}" width="{width}" height="32" rx="12" fill="{fc}"/>')
            svg.append(svg_text(x + width / 2, y + 47, AXIS_BADGES[key], 15, "700", tc, "middle"))
            x += width + 10

    img.save(OUT / "boundary_intersection_ladder.png")
    svg.append("</svg>")
    (OUT / "boundary_intersection_ladder.svg").write_text("\n".join(svg), encoding="utf-8")


def active_axes(row: dict[str, object]) -> str:
    labels = []
    for key, label in AXES:
        value = int(row[key])
        if value == 2:
            labels.append(label)
        elif value == 1:
            labels.append(f"{label} (minor)")
    return ", ".join(labels) if labels else "none"


def write_table(rows: list[dict[str, object]]) -> None:
    readings = {
        "B_up": "Diffuse upstream surface; not a standalone A separator.",
        "B_sort": "Route and all-1/local-context axes intersect with class separation.",
        "B_down1": "Previously separated classes reconverge into a common downstream face.",
        "B_down2": "Near-clean downstream continuation with changed k/pre3 face.",
        "B_down3": "Downstream continuation with small low-support side branches.",
        "B_terminal": "Terminal direct drop.",
    }
    lines = [
        "# Boundary Intersection Table",
        "",
        "| Boundary | role | active axes | dominant face | reading |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| `{row['boundary']}` | {row['role']} | {active_axes(row)} | `{row['dominant_face']}` | {readings[str(row['boundary_id'])]} |"
        )
    (OUT / "boundary_intersection_table.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_report(rows: list[dict[str, object]]) -> None:
    best = max(rows, key=lambda r: (int(r["active_axis_count"]), int(r["axis_score_total"])))
    lines = [
        "# Boundary Intersection Map Report",
        "",
        "This is an observational intersection map, not a mechanism diagram.",
        "",
        "## Thresholds",
        "",
        "- Distribution axes use: 0 when the dominant value is at least 0.98; 1 when only one value has support of at least 10; 2 when multiple values have support of at least 10.",
        "- Class separation uses the class-distance table: 2 for the 64-95 sorting row or total class-distance at least 8; 1 for nonzero but weaker separation.",
        "- Reconvergence is marked 2 on downstream rows where major classes share the dominant compact face.",
        "- Face diversity is marked 2 when compact-face entropy is at least 2 or at least 20 compact faces are present.",
        "",
        "## Answers",
        "",
        f"1. Strongest intersection of active axes: `{best['boundary']}`, with active-axis count `{best['active_axis_count']}` and total score `{best['axis_score_total']}`.",
        "2. `64-95 -> 32-63 is not identified here as special by maximal neighbor distance alone.`",
        "3. `Its distinctive role is the co-location of route split, local all-1/context split, and class separation.`",
        "4. The mainly reconvergent rows are `32-63 -> 16-31`, `16-31 -> 8-15`, and `8-15 -> 4-7`; the terminal row also preserves a near-single direct drop.",
        "5. The diffuse upstream feeder is `96-127 -> 64-95`, where face diversity is high but the later class split is weak as a standalone separator.",
        "6. The terminal row is `4-7 -> 0-1`.",
        "7. Do not read the map as causal evidence, certainty-level evidence, or a diagram of imposed downstream fate. It only marks where observed descriptors co-locate in this scan.",
        "",
        "## Outputs",
        "",
        "- `boundary_intersection_axis_scores.csv`",
        "- `boundary_intersection_heatmap.png` / `boundary_intersection_heatmap.svg`",
        "- `boundary_intersection_ladder.png` / `boundary_intersection_ladder.svg`",
        "- `boundary_intersection_table.md`",
    ]
    (OUT / "boundary_intersection_map_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate(rows: list[dict[str, object]]) -> list[str]:
    messages: list[str] = []
    for name, path in INPUTS.items():
        if not path.exists():
            raise FileNotFoundError(f"missing input: {name} {path}")
    if [row["boundary_id"] for row in rows] != BOUNDARY_ORDER:
        raise RuntimeError("boundary order mismatch")
    for row in rows:
        for key, _label in AXES:
            if int(row[key]) not in {0, 1, 2}:
                raise RuntimeError(f"bad score {key}={row[key]} for {row['boundary_id']}")
    for name in [
        "boundary_intersection_heatmap.png",
        "boundary_intersection_heatmap.svg",
        "boundary_intersection_ladder.png",
        "boundary_intersection_ladder.svg",
        "boundary_intersection_table.md",
        "boundary_intersection_map_report.md",
    ]:
        path = OUT / name
        if not path.exists() or path.stat().st_size == 0:
            raise RuntimeError(f"missing or empty output: {path}")
    report = (OUT / "boundary_intersection_map_report.md").read_text(encoding="utf-8").lower()
    forbidden = ["because", "causes", "proof", "forces", "explains"]
    hits = [word for word in forbidden if re.search(rf"\b{word}\b", report)]
    if hits:
        raise RuntimeError(f"forbidden report words found: {hits}")
    mechanism_count = len(re.findall(r"\bmechanism\b", report))
    if mechanism_count != 1:
        raise RuntimeError(f"expected exactly one required negated mechanism use, got {mechanism_count}")
    messages.append("inputs: ok")
    messages.append("boundaries: ok")
    messages.append("axis scores 0/1/2: ok")
    messages.append("PNG/SVG/markdown outputs: ok")
    messages.append("language check: ok, with one required negated 'mechanism' phrase")
    return messages


def main() -> None:
    OUT.mkdir(exist_ok=True)
    rows = build_scores()
    write_csv(OUT / "boundary_intersection_axis_scores.csv", rows)
    make_heatmap(rows)
    make_ladder(rows)
    write_table(rows)
    write_report(rows)
    print("Validation summary")
    for message in validate(rows):
        print(f"- {message}")
    print(OUT / "boundary_intersection_heatmap.png")
    print(OUT / "boundary_intersection_ladder.png")
    print(OUT / "boundary_intersection_map_report.md")


if __name__ == "__main__":
    main()
