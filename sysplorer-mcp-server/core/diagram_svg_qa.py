"""Heuristic checks on Sysplorer-exported diagram SVG for layout / error QA."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, List


def _is_red_like_stroke(value: str) -> bool:
    s = value.lower().replace(" ", "")
    if s in ("red", "#red"):
        return True
    if "#ff0000" in s or s in ("#f00", "rgb(255,0,0)", "rgba(255,0,0,1)"):
        return True
    m = re.search(r"rgb\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)", s)
    if m:
        r, g, b = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if r >= 200 and g <= 80 and b <= 80:
            return True
    return False


def scan_diagram_svg(path: str | Path) -> Dict[str, Any]:
    """Parse exported SVG text for stroke/fill colors; flag probable error red (heuristic).

    Sysplorer error overlays often use red strokes; domain wires may also be red (e.g. Analog),
    so treat counts as hints, not definitive pass/fail.
    """
    p = Path(path)
    out: Dict[str, Any] = {"ok": False, "path": str(p.resolve())}
    if p.suffix.lower() != ".svg":
        out["error"] = "not_an_svg_file"
        return out
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        out["error"] = str(exc)
        return out

    strokes: List[str] = []
    for pat in (
        r'stroke\s*=\s*["\']([^"\']+)["\']',
        r"stroke:\s*([^;\"'<]+)",
    ):
        for m in re.finditer(pat, text, flags=re.IGNORECASE):
            strokes.append(m.group(1).strip())

    fills: List[str] = []
    for pat in (
        r'fill\s*=\s*["\']([^"\']+)["\']',
        r"fill:\s*([^;\"'<]+)",
    ):
        for m in re.finditer(pat, text, flags=re.IGNORECASE):
            fills.append(m.group(1).strip())

    red_strokes = [s for s in strokes if _is_red_like_stroke(s)]
    red_fills = [s for s in fills if _is_red_like_stroke(s)]

    out["ok"] = True
    out["svg_size_bytes"] = len(text.encode("utf-8"))
    out["stroke_color_samples"] = strokes[:50]
    out["fill_color_samples"] = fills[:30]
    out["probable_error_red_stroke_hits"] = len(red_strokes)
    out["probable_error_red_stroke_values"] = list(dict.fromkeys(red_strokes))[:15]
    out["probable_error_red_fill_hits"] = len(red_fills)
    out["hint"] = (
        "红色描边可能含错误连线，也可能为电气域正常蓝色以外的配色；请结合模型与图面语义判断。"
    )
    return out
