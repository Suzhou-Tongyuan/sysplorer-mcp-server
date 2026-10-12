"""Validate key result variables against simple thresholds.

Expected JSON structure:
{
  "validations": [
    {
      "name": "outletTemperature",
      "value": 315.2,
      "min": 300.0,
      "max": 330.0,
      "unit": "K"
    }
  ]
}

If `passed` is provided, it must be a JSON boolean and takes priority.
Otherwise `value` and any supplied `min` / `max` must be finite numbers.
Exit codes: 0 = PASSED, 1 = FAILED (including invalid input),
2 = NOT_VALIDATED (missing or empty validations). This optional helper does
not decide whether result verification is required by the parent task.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path


def is_finite_number(value: object) -> bool:
    if type(value) not in (int, float):
        return False
    try:
        return math.isfinite(value)
    except OverflowError:
        return False


def evaluate(item: dict) -> tuple[bool, str]:
    name = str(item.get("name", "unnamed"))
    if "passed" in item:
        if type(item["passed"]) is not bool:
            return False, f"{name}: passed must be a JSON boolean"
        passed = item["passed"]
        message = str(item.get("message", "passed" if passed else "validation failed"))
        return passed, f"{name}: {message}"

    value = item.get("value")
    minimum = item.get("min")
    maximum = item.get("max")
    unit = str(item.get("unit", "")).strip()

    if not is_finite_number(value):
        return False, f"{name}: invalid numeric value"
    for key in ("min", "max"):
        if key in item and not is_finite_number(item[key]):
            return False, f"{name}: {key} must be a finite number"
    if "min" in item and "max" in item and minimum > maximum:
        return False, f"{name}: min must not exceed max"
    if "min" in item and value < minimum:
        return False, f"{name}: {value} {unit}".strip() + f" < min {minimum}"
    if "max" in item and value > maximum:
        return False, f"{name}: {value} {unit}".strip() + f" > max {maximum}"
    return True, f"{name}: {value} {unit}".strip()


def validate_results(data: object) -> tuple[str, int, list[str]]:
    if not isinstance(data, dict):
        return "FAILED", 1, ["results must be a JSON object"]
    if "validations" not in data:
        return "NOT_VALIDATED", 2, ["validations is missing; no evidence checked"]
    validations = data["validations"]
    if not isinstance(validations, list):
        return "FAILED", 1, ["validations must be a list"]
    if not validations:
        return "NOT_VALIDATED", 2, ["validations is empty; no evidence checked"]

    results = []
    for index, item in enumerate(validations):
        if not isinstance(item, dict):
            results.append((False, f"validations[{index}] must be an object"))
        else:
            results.append(evaluate(item))
    failed = [message for passed, message in results if not passed]
    if failed:
        return "FAILED", 1, failed
    return "PASSED", 0, [message for _, message in results]


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python verify-key-results.py <results.json>")
        return 1

    result_path = Path(sys.argv[1])
    try:
        data = json.loads(result_path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, ValueError) as exc:
        print("FAILED")
        print(f"Cannot read results: {exc}")
        return 1

    status, exit_code, messages = validate_results(data)
    print(status)
    for message in messages:
        print(message)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
