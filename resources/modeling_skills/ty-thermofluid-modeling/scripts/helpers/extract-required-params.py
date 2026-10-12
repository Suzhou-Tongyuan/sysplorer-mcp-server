"""Extract first-pass required inputs from scenario templates.

Supports:
1. JSON templates with a `required_parameters` array.
2. Markdown templates by extracting bullet items under selected headings.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKDOWN_SECTIONS = {"Recommended Inputs", "推荐输入", "Required Elements", "必配要素", "Default Validation Variables", "默认验证量"}


def extract_from_json(template_path: Path) -> list[str]:
    data = json.loads(template_path.read_text(encoding="utf-8"))
    items = data.get("required_parameters", [])
    return [str(item).strip() for item in items if str(item).strip()]


def extract_from_markdown(template_path: Path) -> list[str]:
    items: list[str] = []
    current_section = ""

    for raw_line in template_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue

        heading_match = re.match(r"^#{1,6}\s+(.*)$", line)
        if heading_match:
            current_section = heading_match.group(1).strip()
            continue

        if current_section not in MARKDOWN_SECTIONS:
            continue

        bullet_match = re.match(r"^[-*]\s+(.*)$", line)
        if bullet_match:
            items.append(f"{current_section}: {bullet_match.group(1).strip()}")

    return items


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python extract-required-params.py <scenario-template>")
        return 1

    template_path = Path(sys.argv[1])
    if not template_path.exists():
        print(f"Template not found: {template_path}")
        return 1

    suffix = template_path.suffix.lower()
    if suffix == ".json":
        items = extract_from_json(template_path)
    elif suffix == ".md":
        items = extract_from_markdown(template_path)
    else:
        print("Unsupported file type. Use .json or .md.")
        return 1

    for item in items:
        print(item)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
