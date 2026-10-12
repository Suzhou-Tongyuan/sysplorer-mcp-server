#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def read_csv(path: Path) -> tuple[list[str], list[dict[str, float]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"No header found in {path}")
        rows: list[dict[str, float]] = []
        for row in reader:
            rows.append({k: float(v) for k, v in row.items() if k and v is not None and v != ""})
    return reader.fieldnames, rows


def interpolate(rows: list[dict[str, float]], time_col: str, value_col: str, t: float) -> float:
    if not rows:
        raise ValueError("Reference CSV has no rows")
    if t <= rows[0][time_col]:
        return rows[0][value_col]
    if t >= rows[-1][time_col]:
        return rows[-1][value_col]
    left = rows[0]
    right = rows[-1]
    for idx in range(1, len(rows)):
        if rows[idx][time_col] >= t:
            left = rows[idx - 1]
            right = rows[idx]
            break
    t0 = left[time_col]
    t1 = right[time_col]
    y0 = left[value_col]
    y1 = right[value_col]
    if t1 == t0:
        return y1
    ratio = (t - t0) / (t1 - t0)
    return y0 + ratio * (y1 - y0)


def compare(
    reference_rows: list[dict[str, float]],
    candidate_rows: list[dict[str, float]],
    time_col: str,
    value_cols: list[str],
    rtol: float,
    atol: float,
) -> dict:
    summary = {"columns": {}, "pass": True}
    for value_col in value_cols:
        max_rel = 0.0
        max_abs = 0.0
        mean_rel = 0.0
        worst_time = 0.0
        for row in candidate_rows:
            t = row[time_col]
            candidate_value = row[value_col]
            reference_value = interpolate(reference_rows, time_col, value_col, t)
            abs_err = abs(candidate_value - reference_value)
            denom = max(abs(reference_value), atol)
            rel_err = abs_err / denom
            mean_rel += rel_err
            if rel_err > max_rel:
                max_rel = rel_err
                max_abs = abs_err
                worst_time = t
        if candidate_rows:
            mean_rel /= len(candidate_rows)
        passed = max_rel <= rtol
        summary["columns"][value_col] = {
            "max_relative_error": max_rel,
            "mean_relative_error": mean_rel,
            "max_absolute_error": max_abs,
            "worst_time": worst_time,
            "pass": passed,
        }
        if not passed:
            summary["pass"] = False
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare time-series CSV files by interpolating the reference onto the candidate time base.")
    parser.add_argument("reference", help="Reference CSV path.")
    parser.add_argument("candidate", help="Candidate CSV path.")
    parser.add_argument("--time-col", default="time", help="Time column name.")
    parser.add_argument("--columns", nargs="+", required=True, help="Value columns to compare.")
    parser.add_argument("--rtol", type=float, default=0.01, help="Maximum allowed relative error.")
    parser.add_argument("--atol", type=float, default=1e-9, help="Absolute floor for relative error denominator.")
    args = parser.parse_args()

    reference_fields, reference_rows = read_csv(Path(args.reference).resolve())
    candidate_fields, candidate_rows = read_csv(Path(args.candidate).resolve())

    needed = [args.time_col, *args.columns]
    for name in needed:
        if name not in reference_fields:
            raise SystemExit(f"Reference CSV missing column: {name}")
        if name not in candidate_fields:
            raise SystemExit(f"Candidate CSV missing column: {name}")

    result = compare(
        reference_rows=reference_rows,
        candidate_rows=candidate_rows,
        time_col=args.time_col,
        value_cols=args.columns,
        rtol=args.rtol,
        atol=args.atol,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
