"""Parse MCP result time_point values and interpolate series when official At-APIs miss a sample."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional, Sequence, Tuple


@dataclass(frozen=True)
class ParsedTimePoint:
    kind: str  # begin | end | numeric | error
    numeric: Optional[float] = None
    error: str = ""


def parse_result_time_point(time_point: Any) -> ParsedTimePoint:
    """Normalize MCP ``time_point`` to begin/end/numeric.

    JSON/MCP often send numbers as strings (``\"1.0\"``). Official GetVarValueAt
    / GetVarsValueAt expect a float or SimulationTime enum, not a numeric string.
    """
    if time_point is None:
        return ParsedTimePoint(kind="end")
    if isinstance(time_point, bool):
        return ParsedTimePoint(
            kind="error",
            error=f"invalid time_point={time_point!r}; use begin/end or a number",
        )
    if isinstance(time_point, (int, float)):
        return ParsedTimePoint(kind="numeric", numeric=float(time_point))
    if isinstance(time_point, str):
        text = time_point.strip()
        if not text:
            return ParsedTimePoint(kind="end")
        low = text.lower()
        if low in ("end", "stop", "final"):
            return ParsedTimePoint(kind="end")
        if low in ("begin", "start", "initial"):
            return ParsedTimePoint(kind="begin")
        try:
            return ParsedTimePoint(kind="numeric", numeric=float(text))
        except ValueError:
            return ParsedTimePoint(
                kind="error",
                error=(
                    f"invalid time_point={time_point!r}; "
                    "use \"begin\", \"end\", or a numeric time (e.g. 1.0 or \"1.0\")"
                ),
            )
    return ParsedTimePoint(
        kind="error",
        error=f"invalid time_point type {type(time_point).__name__}; use begin/end or a number",
    )


def series_to_floats(data: Any) -> List[float]:
    if data is None:
        return []
    tolist = getattr(data, "tolist", None)
    if callable(tolist):
        try:
            data = tolist()
        except Exception:
            pass
    if isinstance(data, (int, float)) and not isinstance(data, bool):
        return [float(data)]
    if not isinstance(data, (list, tuple)):
        return []
    out: List[float] = []
    for item in data:
        if isinstance(item, bool):
            continue
        if isinstance(item, (int, float)):
            out.append(float(item))
            continue
        inner = series_to_floats(item)
        if len(inner) == 1:
            out.append(inner[0])
    return out


def interpolate_series_at_time(times: Sequence[float], values: Sequence[float], t: float) -> Optional[float]:
    """Linear interpolate ``values`` vs ``times`` at ``t``; clamp to endpoints."""
    n = min(len(times), len(values))
    if n == 0:
        return None
    ts = [float(times[i]) for i in range(n)]
    vs = [float(values[i]) for i in range(n)]
    if t <= ts[0]:
        return vs[0]
    if t >= ts[-1]:
        return vs[-1]
    for i in range(1, n):
        if t <= ts[i]:
            t0, t1 = ts[i - 1], ts[i]
            v0, v1 = vs[i - 1], vs[i]
            if t1 == t0:
                return v1
            w = (t - t0) / (t1 - t0)
            return v0 + w * (v1 - v0)
    return vs[-1]


def is_empty_at_value(data: Any) -> bool:
    if data is None:
        return True
    if isinstance(data, (list, tuple)):
        if len(data) == 0:
            return True
        return all(is_empty_at_value(x) for x in data)
    if isinstance(data, str) and not data.strip():
        return True
    return False
