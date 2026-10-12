#!/usr/bin/env python3
"""Audit a TA Modelica source file before Sysplorer check/simulation."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


TA_LIBS = {
    "TAEconomy",
    "TADynamics",
    "TAThermalSystem",
    "TAEngine",
    "TABattery",
    "TAElectronic",
}

# Complete examples/templates are reference material, not valid parents for a new
# deliverable model. Keep both Example and Examples because TA libraries differ.
DEFAULT_FORBIDDEN_EXTENDS_PREFIXES = tuple(
    f"{lib}.{section}"
    for lib in sorted(TA_LIBS)
    for section in ("Example", "Examples", "VehicleArchitectures")
)

OFFICIAL_SOURCE_PATH_MARKERS = (
    ("Docs", "VehLib", "Samples"),
    ("Library", "TAEconomy"),
    ("Library", "TADynamics"),
    ("Library", "TAThermalSystem"),
    ("Library", "TAEngine"),
    ("Library", "TABattery"),
    ("Library", "TAElectronic"),
    ("mw_mol", "TAEconomy"),
    ("mw_mol", "TADynamics"),
    ("mw_mol", "TAThermalSystem"),
    ("mw_mol", "TAEngine"),
    ("mw_mol", "TABattery"),
    ("mw_mol", "TAElectronic"),
)


def strip_comments(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def modelica_tokens(text: str) -> list[tuple[str, str, int]]:
    """Tokenize audit evidence; comments are skipped and strings stay opaque."""
    tokens: list[tuple[str, str, int]] = []
    index = 0
    while index < len(text):
        char = text[index]
        if char.isspace() or char == "\ufeff":
            index += 1
        elif text.startswith("//", index):
            end = text.find("\n", index + 2)
            index = len(text) if end < 0 else end
        elif text.startswith("/*", index):
            end = text.find("*/", index + 2)
            if end < 0:
                raise ValueError("unterminated Modelica block comment")
            index = end + 2
        elif char in "\"'":
            start, quote = index, char
            index += 1
            value: list[str] = []
            while index < len(text) and text[index] != quote:
                if text[index] == "\\":
                    index += 1
                    if index == len(text):
                        raise ValueError("unterminated Modelica escape")
                value.append(text[index])
                index += 1
            if index == len(text):
                raise ValueError("unterminated Modelica string or quoted identifier")
            kind = "string" if quote == '"' else "quoted_identifier"
            tokens.append((kind, "".join(value), start))
            index += 1
        elif char.isalpha() or char == "_":
            start = index
            index += 1
            while index < len(text) and (text[index].isalnum() or text[index] == "_"):
                index += 1
            tokens.append(("identifier", text[start:index], start))
        else:
            tokens.append(("symbol", char, index))
            index += 1
    return tokens


def closing_paren(tokens: list[tuple[str, str, int]], start: int) -> int:
    depth = 0
    for index in range(start, len(tokens)):
        if tokens[index][:2] == ("symbol", "("):
            depth += 1
        elif tokens[index][:2] == ("symbol", ")"):
            depth -= 1
            if depth == 0:
                return index
    raise ValueError("unbalanced Modelica annotation parentheses")


def line_number(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Preflight audit for TA Modelica deliverable source."
    )
    parser.add_argument("modelica_file", type=Path, help="Path to the deliverable .mo file")
    parser.add_argument(
        "--dependency-root",
        type=Path,
        help=(
            "Explicitly authorized top-level package directory; read enclosing "
            "package.mo files only inside this root. Without it, read only the model file."
        ),
    )
    parser.add_argument(
        "--allowed-library",
        action="append",
        default=[],
        choices=sorted(TA_LIBS),
        help="TA library allowed by the build contract; repeat as needed",
    )
    parser.add_argument(
        "--forbid-extends-prefix",
        action="append",
        default=[],
        help="Additional fully qualified extends prefix to reject",
    )
    parser.add_argument(
        "--allow-official-source-path",
        action="store_true",
        help="Allow auditing a file located under installed official library/example paths",
    )
    parser.add_argument(
        "--min-connects",
        type=int,
        default=1,
        help="Minimum number of explicit connect(...) statements expected",
    )
    parser.add_argument(
        "--require-component",
        action="append",
        default=[],
        help="Regex that must appear in source for a required top-level component",
    )
    return parser.parse_args()


def find_uses_dependencies(code: str) -> list[tuple[str, str | None]]:
    """Read direct uses(...) entries in annotations, not examples in strings."""
    tokens = modelica_tokens(code)
    entries: list[tuple[str, str | None]] = []
    identifiers = {"identifier", "quoted_identifier"}
    for index, token in enumerate(tokens[:-1]):
        if token[:2] != ("identifier", "annotation") or tokens[index + 1][:2] != ("symbol", "("):
            continue
        end = closing_paren(tokens, index + 1)
        cursor = index + 2
        while cursor < end:
            if (
                tokens[cursor][:2] == ("identifier", "uses")
                and tokens[cursor - 1][:2] in {("symbol", "("), ("symbol", ",")}
                and cursor + 1 < end
                and tokens[cursor + 1][:2] == ("symbol", "(")
            ):
                uses_end = closing_paren(tokens, cursor + 1)
                entry = cursor + 2
                while entry < uses_end:
                    if (
                        tokens[entry][0] in identifiers
                        and entry + 1 < uses_end
                        and tokens[entry + 1][:2] == ("symbol", "(")
                    ):
                        entry_end = closing_paren(tokens, entry + 1)
                        versions: list[str] = []
                        parameter = entry + 2
                        while parameter < entry_end:
                            if (
                                tokens[parameter][:2] == ("identifier", "version")
                                and parameter + 2 < entry_end
                                and tokens[parameter + 1][:2] == ("symbol", "=")
                                and tokens[parameter + 2][0] == "string"
                            ):
                                versions.append(tokens[parameter + 2][1])
                                parameter += 3
                            elif tokens[parameter][:2] == ("symbol", "("):
                                parameter = closing_paren(tokens, parameter) + 1
                            else:
                                parameter += 1
                        entries.extend((tokens[entry][1], version) for version in (versions or [None]))
                        entry = entry_end + 1
                    else:
                        entry += 1
                cursor = uses_end + 1
            elif tokens[cursor][:2] == ("symbol", "("):
                cursor = closing_paren(tokens, cursor) + 1
            else:
                cursor += 1
    return entries


def extends_matches_prefix(class_name: str, prefix: str) -> bool:
    normalized = prefix.rstrip(".")
    return class_name == normalized or class_name.startswith(normalized + ".")


def find_forbidden_extends(code: str, prefixes: tuple[str, ...]) -> list[tuple[int, str, str]]:
    findings: list[tuple[int, str, str]] = []
    tokens = modelica_tokens(code)
    identifiers = {"identifier", "quoted_identifier"}
    for index, token in enumerate(tokens):
        if token[:2] != ("identifier", "extends"):
            continue
        cursor = index + 1
        if cursor < len(tokens) and tokens[cursor][:2] == ("symbol", "."):
            cursor += 1
        parts: list[str] = []
        while cursor < len(tokens) and tokens[cursor][0] in identifiers:
            part = tokens[cursor][1]
            # A quoted identifier containing dots is one name, not a qualified path.
            if not re.fullmatch(r"[A-Za-z_]\w*", part):
                part = "'" + part.replace("\\", "\\\\").replace("'", "\\'") + "'"
            parts.append(part)
            cursor += 1
            if cursor >= len(tokens) or tokens[cursor][:2] != ("symbol", "."):
                break
            cursor += 1
        class_name = ".".join(parts)
        for prefix in prefixes:
            if extends_matches_prefix(class_name, prefix):
                findings.append((line_number(code, token[2]), class_name, prefix.rstrip(".")))
                break
    return findings


def path_contains_sequence(path: Path, sequence: tuple[str, ...]) -> bool:
    parts = tuple(part.lower() for part in path.parts)
    needle = tuple(item.lower() for item in sequence)
    if len(needle) > len(parts):
        return False
    return any(parts[index : index + len(needle)] == needle for index in range(len(parts) - len(needle) + 1))


def official_source_marker(path: Path) -> tuple[str, ...] | None:
    resolved = path.resolve()
    for marker in OFFICIAL_SOURCE_PATH_MARKERS:
        if path_contains_sequence(resolved, marker):
            return marker
    return None


def read_text_utf8(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def require_within(path: Path, root: Path) -> None:
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"dependency path is outside authorized root {root}: {path}") from exc


def read_audit_sources(
    path: Path, dependency_root: Path | None
) -> list[tuple[Path, str]]:
    """Read no implicit parents: enclosing package context requires an explicit root."""
    model_path = path.resolve(strict=True)
    root = None
    if dependency_root is not None:
        root = dependency_root.resolve(strict=True)
        if not root.is_dir():
            raise ValueError(f"dependency root is not a directory: {root}")
        require_within(model_path, root)
    sources = [(model_path, read_text_utf8(model_path))]
    if root is None:
        return sources

    directory = model_path.parent
    seen = {model_path}
    while True:
        package_path = (directory / "package.mo").resolve()
        # Check resolved symlink/junction destinations before reading their content.
        require_within(package_path, root)
        if not package_path.is_file():
            raise ValueError(f"missing package.mo inside dependency root: {directory}")
        if package_path not in seen:
            sources.append((package_path, read_text_utf8(package_path)))
            seen.add(package_path)
        if directory == root:
            break
        directory = directory.parent
    return sources


def main() -> int:
    args = parse_args()
    path = args.modelica_file
    if not path.exists():
        print(f"ERROR: file not found: {path}")
        return 2
    if path.suffix.lower() != ".mo":
        print(f"ERROR: expected a .mo file: {path}")
        return 2

    prefixes = DEFAULT_FORBIDDEN_EXTENDS_PREFIXES + tuple(args.forbid_extends_prefix)
    try:
        sources = read_audit_sources(path, args.dependency_root)
        raw = sources[0][1]
        dependencies = [
            (source, library, version)
            for source, text in sources
            for library, version in find_uses_dependencies(text)
        ]
        forbidden_extends = find_forbidden_extends(raw, prefixes)
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"ERROR: unable to audit source/dependency context: {exc}")
        return 2
    code = strip_comments(raw)
    errors: list[str] = []
    warnings: list[str] = []

    marker = official_source_marker(path)
    if marker and not args.allow_official_source_path:
        errors.append(
            "source path appears to be an installed official/example library path: "
            + "\\".join(marker)
            + "; audit deliverable user-owned .mo files, or pass --allow-official-source-path only for example verification"
        )

    modelica_dependencies = [
        (source, version) for source, library, version in dependencies if library == "Modelica"
    ]
    if not modelica_dependencies:
        errors.append(
            'missing uses(Modelica(version = "4.0.0.TY.1")) in authorized source context; '
            "for a packaged model, pass --dependency-root only for an already authorized package root"
        )
    for source, version in modelica_dependencies:
        if version != "4.0.0.TY.1":
            errors.append(
                f"Modelica dependency in {source} is {version!r}; required version is '4.0.0.TY.1'"
            )

    for lineno, class_name, matched_prefix in forbidden_extends:
        errors.append(
            f"line {lineno}: forbidden direct extends of {class_name} "
            f"(matches complete example/template prefix {matched_prefix})"
        )

    connect_count = len(re.findall(r"\bconnect\s*\(", code))
    if connect_count < args.min_connects:
        errors.append(
            f"only {connect_count} explicit connect(...) statements; expected at least {args.min_connects}"
        )

    for pattern in args.require_component:
        if not re.search(pattern, code):
            errors.append(f"required component pattern not found: {pattern}")

    used_ta_libs = {library for _, library, _ in dependencies if library in TA_LIBS}
    allowed = set(args.allowed_library)
    if allowed:
        unexpected = sorted(used_ta_libs - allowed)
        if unexpected:
            errors.append(
                "TA libraries outside build contract: " + ", ".join(unexpected)
            )
    elif used_ta_libs == TA_LIBS:
        warnings.append("all six TA libraries appear in uses(...); confirm the build contract needs them")

    print(f"Audit file: {path}")
    print("Dependency sources: " + ", ".join(str(source) for source, _ in sources))
    print(f"Modelica connects: {connect_count}")
    print("TA libraries in uses(...): " + (", ".join(sorted(used_ta_libs)) or "none"))

    if warnings:
        print("\nWarnings:")
        for item in warnings:
            print(f"- {item}")

    if errors:
        print("\nErrors:")
        for item in errors:
            print(f"- {item}")
        return 1

    print("\nAudit passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())