#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import asdict, dataclass
from pathlib import Path


FLOAT_TYPES = {"MwbDouble", "MwbFloat", "double", "float"}
BOOL_TYPES = {"MwbBool", "bool", "_Bool"}
SV_REAL_DEFAULT = "0.0"
SV_INT_DEFAULT = "0"


@dataclass
class Signal:
    name: str
    base_type: str
    length: int = 1

    @property
    def is_array(self) -> bool:
        return self.length > 1


@dataclass
class Testpoint:
    trace_id: str
    function_suffix: str
    c_expr: str
    base_type: str
    length: int = 1
    selected_via: str = "list"

    @property
    def is_array(self) -> bool:
        return self.length > 1

    @property
    def sv_var_name(self) -> str:
        return f"tp_{self.function_suffix}"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def sanitize_prefix(api_prefix: str) -> str:
    if not re.fullmatch(r"[A-Za-z_]\w*", api_prefix):
        raise ValueError(f"invalid api prefix: {api_prefix!r}")
    return api_prefix


def detect_model_stem(codegen_dir: Path, requested: str | None) -> str:
    if requested:
        return requested
    candidates: list[str] = []
    ignored = {"dpi", "mwb_main", "mwb_runtime", "mwb_types", "julia_blocks_private"}
    for source_path in sorted(codegen_dir.glob("*.c")):
        stem = source_path.stem
        if stem in ignored or stem.endswith("_data") or stem.endswith("_private"):
            continue
        if (codegen_dir / f"{stem}.h").exists() and (codegen_dir / f"{stem}_private.h").exists():
            candidates.append(stem)
    if len(candidates) != 1:
        raise ValueError(f"unable to infer model stem from {codegen_dir}; candidates={candidates}")
    return candidates[0]


def parse_main_header(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for struct_name, global_name in re.findall(r"extern struct\s+(\w+)\s+(\w+)\s*;", text):
        if struct_name.endswith("ExtU"):
            result["input_struct"] = struct_name
            result["input_global"] = global_name
        elif struct_name.endswith("ExtY"):
            result["output_struct"] = struct_name
            result["output_global"] = global_name
        elif struct_name.endswith("B"):
            result["block_struct"] = struct_name
            result["block_global"] = global_name
        elif struct_name.endswith("Dw"):
            result["state_struct"] = struct_name
            result["state_global"] = global_name
    md_match = re.search(r"extern\s+(\w+)\s*\*\s*const\s+(\w+)\s*;", text)
    if md_match:
        result["md_type"] = md_match.group(1)
        result["md_global"] = md_match.group(2)
    functions = re.findall(r"void\s+(\w+)\s*\(\s*void\s*\)\s*;", text)
    for name in functions:
        if name.lower() == "step":
            result["step_func"] = name
        elif name.lower() == "init":
            result["init_func"] = name
        elif "term" in name.lower():
            result["term_func"] = name
    required = ["input_struct", "input_global", "output_struct", "output_global", "md_global", "init_func", "step_func"]
    missing = [name for name in required if name not in result]
    if missing:
        raise ValueError(f"missing required symbols in main header: {missing}")
    return result


def extract_struct_fields(text: str, struct_name: str) -> list[Signal]:
    match = re.search(rf"struct\s+{re.escape(struct_name)}\s*\{{(.*?)\}};", text, re.S)
    if not match:
        raise ValueError(f"unable to find struct {struct_name}")
    fields: list[Signal] = []
    for base_type, name, _, length in re.findall(
        r"^\s*([A-Za-z_]\w*)\s+([A-Za-z_]\w*)(\[(\d+)\])?\s*;",
        match.group(1),
        re.M,
    ):
        fields.append(Signal(name=name, base_type=base_type, length=int(length or 1)))
    return fields


def parse_step_size(source_text: str, md_global: str) -> str | None:
    match = re.search(rf"{re.escape(md_global)}->m_stepSize\s*=\s*([^;]+);", source_text)
    return match.group(1).strip() if match else None


def detect_julia(codegen_dir: Path) -> bool:
    return (codegen_dir / "julia_blocks_codegen").exists() or (codegen_dir / "julia_blocks_private.c").exists()


def build_signal_lookup(symbols: dict[str, str], inputs: list[Signal], outputs: list[Signal], blocks: list[Signal], states: list[Signal]) -> dict[str, Signal]:
    lookup: dict[str, Signal] = {}
    for global_key, signal_list in (
        ("input_global", inputs),
        ("output_global", outputs),
        ("block_global", blocks),
        ("state_global", states),
    ):
        global_name = symbols.get(global_key)
        if not global_name:
            continue
        for sig in signal_list:
            lookup[f"{global_name}.{sig.name}"] = sig
    return lookup


def sanitize_trace_suffix(trace_id: str) -> str:
    suffix = re.sub(r"[^0-9A-Za-z_]+", "_", trace_id.strip().lstrip("-"))
    suffix = re.sub(r"_+", "_", suffix).strip("_")
    if not suffix:
        suffix = "tp"
    if suffix[0].isdigit():
        suffix = f"tp_{suffix}"
    return suffix


def trace_field_id(trace_id: str) -> str:
    return trace_id.strip().lstrip("-")


def normalize_tokens(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9]+", text.lower())


def normalize_text(text: str) -> str:
    return " ".join(normalize_tokens(text))


def split_query_phrases(query: str) -> list[str]:
    normalized = query.replace("，", ",").replace("；", ";").replace("\n", ",")
    normalized = normalized.replace("以及", ",").replace("及", ",").replace("和", ",")
    parts = re.split(r"\s*(?:,|;|\band\b|\bor\b|\bplus\b)\s*", normalized, flags=re.I)
    return [part.strip() for part in parts if part.strip()]


def extract_position_text(lines: list[str], position: dict[str, int]) -> str:
    begin_row = position["begin row"] - 1
    begin_col = position["begin column"] - 1
    end_row = position["end row"] - 1
    end_col = position["end column"] - 1
    if begin_row == end_row:
        return lines[begin_row][begin_col:end_col]
    chunks = [lines[begin_row][begin_col:]]
    for row in range(begin_row + 1, end_row):
        chunks.append(lines[row])
    chunks.append(lines[end_row][:end_col])
    return "\n".join(chunks)


def iter_trace_entities(entity: dict[str, object]) -> list[dict[str, object]]:
    items: list[dict[str, object]] = [entity]
    for child in entity.get("entities", []):
        items.extend(iter_trace_entities(child))
    return items


def choose_supported_expression(snippets: list[str], signal_lookup: dict[str, Signal]) -> tuple[str, Signal] | None:
    for snippet in snippets:
        expr = "".join(snippet.split())
        signal = signal_lookup.get(expr)
        if signal is not None:
            return expr, signal
    return None


def collect_testpoint_candidates(codegen_dir: Path, symbols: dict[str, str], inputs: list[Signal], outputs: list[Signal], blocks: list[Signal], states: list[Signal]) -> list[Testpoint]:
    motrace_path = codegen_dir / "motrace.json"
    if not motrace_path.exists():
        return []

    signal_lookup = build_signal_lookup(symbols, inputs, outputs, blocks, states)
    field_names = {sig.name for sig in inputs + outputs + blocks + states}
    motrace = json.loads(read_text(motrace_path))
    line_cache: dict[str, list[str]] = {}
    candidates: list[Testpoint] = []
    seen_suffixes: set[str] = set()

    for entity in iter_trace_entities(motrace):
        trace_id = str(entity.get("id") or "").strip()
        if not trace_id:
            continue
        stripped_id = trace_field_id(trace_id)
        if trace_id.startswith("-") and stripped_id not in field_names:
            continue

        snippets: list[str] = []
        for code in entity.get("codes", []):
            source_name = code.get("file")
            if not source_name:
                continue
            if source_name not in line_cache:
                source_path = codegen_dir / source_name
                if not source_path.exists():
                    continue
                line_cache[source_name] = read_text(source_path).splitlines()
            lines = line_cache[source_name]
            for position in code.get("positions", []):
                snippets.append(extract_position_text(lines, position).strip())

        supported = choose_supported_expression(snippets, signal_lookup)
        if supported is None:
            continue
        c_expr, signal = supported
        if signal.is_array:
            continue

        function_suffix = sanitize_trace_suffix(stripped_id)
        if function_suffix in seen_suffixes:
            continue
        seen_suffixes.add(function_suffix)
        candidates.append(
            Testpoint(
                trace_id=stripped_id,
                function_suffix=function_suffix,
                c_expr=c_expr,
                base_type=signal.base_type,
                length=signal.length,
            )
        )
    return candidates


def resolve_requested_testpoints(requested_ids: list[str], natural_language: str | None, candidates: list[Testpoint]) -> tuple[list[Testpoint], list[str], list[str]]:
    selected: list[Testpoint] = []
    warnings: list[str] = []
    unresolved: list[str] = []
    by_exact: dict[str, Testpoint] = {}
    for candidate in candidates:
        by_exact[candidate.trace_id] = candidate
        by_exact[candidate.trace_id.lstrip("-")] = candidate

    for requested in requested_ids:
        key = requested.strip()
        candidate = by_exact.get(key) or by_exact.get(key.lstrip("-"))
        if candidate is None:
            unresolved.append(key)
            continue
        selected.append(Testpoint(**{**asdict(candidate), "selected_via": "list"}))

    if natural_language:
        for phrase in split_query_phrases(natural_language):
            phrase_norm = normalize_text(phrase)
            phrase_tokens = set(normalize_tokens(phrase))
            if not phrase_norm and not phrase_tokens:
                continue
            best_candidate: Testpoint | None = None
            best_score = 0
            for candidate in candidates:
                candidate_norm = normalize_text(candidate.trace_id)
                candidate_tokens = set(normalize_tokens(candidate.trace_id))
                score = 0
                if candidate_norm and candidate_norm in phrase_norm:
                    score += 100
                overlap = len(phrase_tokens & candidate_tokens)
                score += overlap * 10
                if phrase_tokens and phrase_tokens <= candidate_tokens:
                    score += 25
                if score > best_score:
                    best_candidate = candidate
                    best_score = score
            if best_candidate is None or best_score <= 0:
                unresolved.append(phrase)
                continue
            selected.append(Testpoint(**{**asdict(best_candidate), "selected_via": "nl"}))

    deduped: list[Testpoint] = []
    seen_suffixes: set[str] = set()
    for candidate in selected:
        if candidate.function_suffix in seen_suffixes:
            continue
        seen_suffixes.add(candidate.function_suffix)
        deduped.append(candidate)

    if natural_language and deduped:
        warnings.append("Natural-language testpoint matching is heuristic and currently works best when the prompt uses motrace ids or close token variants.")
    return deduped, unresolved, warnings


def dedupe_keep_order(items: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for item in items:
        if item and item not in seen:
            result.append(item)
            seen.add(item)
    return result


def model_csv_bases(model_stem: str) -> list[str]:
    bases = [model_stem]
    stem_parts = [part for part in re.split(r"[_.]", model_stem) if part]
    if stem_parts:
        bases.append(stem_parts[0])
    bases.append("model")
    return dedupe_keep_order(bases)


def relative_posix_path(base_dir: Path, target_path: Path) -> str | None:
    try:
        return Path(os.path.relpath(target_path, start=base_dir)).as_posix()
    except ValueError:
        return None


def discover_nearby_csv_files(codegen_dir: Path, suffix: str) -> list[tuple[str, Path]]:
    discovered: list[tuple[str, Path]] = []
    current = codegen_dir
    for _ in range(4):
        if current.exists():
            for csv_path in sorted(current.glob(f"*{suffix}")):
                base_name = csv_path.name.removesuffix(suffix)
                discovered.append((base_name, csv_path.resolve()))
        parent = current.parent
        if parent == current:
            break
        current = parent
    return discovered


def discover_csv_candidates(search_dir: Path, render_dir: Path, model_stem: str, suffix: str, preferred_bases: list[str] | None = None) -> list[str]:
    preferred_bases = preferred_bases or []
    bases = model_csv_bases(model_stem)
    discovered = discover_nearby_csv_files(search_dir, suffix)

    candidates: list[str] = []

    for base in preferred_bases:
        for discovered_base, csv_path in discovered:
            if discovered_base == base:
                relative_path = relative_posix_path(render_dir, csv_path)
                if relative_path:
                    candidates.append(relative_path)

    for prefix in ("", "../", "../../", "../../../"):
        for base in dedupe_keep_order(preferred_bases + bases):
            candidates.append(f"{prefix}{base}{suffix}")

    for _, csv_path in discovered:
        relative_path = relative_posix_path(render_dir, csv_path)
        if relative_path:
            candidates.append(relative_path)

    return dedupe_keep_order(candidates)


def sv_type(base_type: str) -> str:
    if base_type in FLOAT_TYPES:
        return "real"
    if base_type in BOOL_TYPES:
        return "bit"
    return "int"


def scalar_default(sig: Signal) -> str:
    return SV_REAL_DEFAULT if sv_type(sig.base_type) == "real" else SV_INT_DEFAULT


def c_input_param(sig: Signal) -> str:
    if sig.is_array:
        return f"{sig.base_type}* {sig.name}"
    return f"{sig.base_type} {sig.name}"


def c_output_param(sig: Signal) -> str:
    return f"{sig.base_type}* {sig.name}"


def sv_port(direction: str, sig: Signal) -> str:
    if sig.is_array:
        return f"    {direction} {sv_type(sig.base_type)} {sig.name}[{sig.length - 1}:0]"
    return f"    {direction} {sv_type(sig.base_type)} {sig.name}"


def sv_decl(sig: Signal) -> str:
    if sig.is_array:
        return f"{sv_type(sig.base_type)} {sig.name}[{sig.length - 1}:0];"
    return f"{sv_type(sig.base_type)} {sig.name};"


def comma_block(lines: list[str]) -> str:
    if not lines:
        return "void"
    return ",\n".join(lines)


def join_args(signals: list[Signal], indent: str = "        ") -> str:
    return f",\n{indent}".join(sig.name for sig in signals)


def sv_call(function_name: str, signals: list[Signal], indent: str) -> str:
    if not signals:
        return f"{function_name}()"
    return f"{function_name}(\n{indent}{join_args(signals, indent)})"


def render_testpoint_h_decls(api_prefix: str, testpoints: list[Testpoint]) -> str:
    if not testpoints:
        return ""
    return "\n".join(
        f"DPI_LINK_DECL DPI_DLLESPEC int {api_prefix}_DPI_GetTestpoint_{tp.function_suffix}({tp.base_type}* value);"
        for tp in testpoints
    )


def render_dpi_h(model_stem: str, api_prefix: str, inputs: list[Signal], outputs: list[Signal], testpoints: list[Testpoint]) -> str:
    guard = f"INCLUDED_{api_prefix.upper()}_DPI"
    testpoint_block = render_testpoint_h_decls(api_prefix, testpoints)
    if testpoint_block:
        testpoint_block = f"\n{testpoint_block}\n"
    return f"""/* Auto-generated by sysplorer-svdpi */
#ifndef {guard}
#define {guard}

#ifdef __cplusplus
#define DPI_LINK_DECL extern "C"
#else
#define DPI_LINK_DECL
#endif

#include "svdpi.h"
#include "mwb_types.h"

DPI_LINK_DECL DPI_DLLESPEC int {api_prefix}_DPI_Init(void);
DPI_LINK_DECL DPI_DLLESPEC int {api_prefix}_DPI_Reset(void);
DPI_LINK_DECL DPI_DLLESPEC int {api_prefix}_DPI_Step(void);
DPI_LINK_DECL DPI_DLLESPEC int {api_prefix}_DPI_Terminate(void);

DPI_LINK_DECL DPI_DLLESPEC int {api_prefix}_DPI_GetOutputs(
{comma_block([f"    {c_output_param(sig)}" for sig in outputs])});

DPI_LINK_DECL DPI_DLLESPEC int {api_prefix}_DPI_SetInputs(
{comma_block([f"    {c_input_param(sig)}" for sig in inputs])});
{testpoint_block}

#endif
"""


def render_testpoint_c_impl(api_prefix: str, testpoints: list[Testpoint]) -> str:
    if not testpoints:
        return ""
    blocks: list[str] = []
    for tp in testpoints:
        blocks.append(
            f"""DPI_DLLESPEC int {api_prefix}_DPI_GetTestpoint_{tp.function_suffix}({tp.base_type}* value)
{{
    if (!g_initialized) {{ return {api_prefix}_DPI_ERROR_NOT_INIT; }}
    if (!value) {{ return {api_prefix}_DPI_ERROR_NULL_PTR; }}
    *value = {tp.c_expr};
    return {api_prefix}_DPI_SUCCESS;
}}"""
        )
    return "\n\n" + "\n\n".join(blocks)


def render_dpi_c(model_stem: str, api_prefix: str, symbols: dict[str, str], inputs: list[Signal], outputs: list[Signal], testpoints: list[Testpoint]) -> str:
    output_checks = "\n".join(f"    if (!{sig.name}) {{ return {api_prefix}_DPI_ERROR_NULL_PTR; }}" for sig in outputs)
    input_checks = "\n".join(f"    if (!{sig.name}) {{ return {api_prefix}_DPI_ERROR_NULL_PTR; }}" for sig in inputs if sig.is_array)
    output_assignments = "\n".join(
        f"    *{sig.name} = {symbols['output_global']}.{sig.name};" if not sig.is_array else
        f"    for (i = 0; i < {sig.length}; ++i) {{ {sig.name}[i] = {symbols['output_global']}.{sig.name}[i]; }}"
        for sig in outputs
    )
    input_assignments = "\n".join(
        f"    {symbols['input_global']}.{sig.name} = {sig.name};" if not sig.is_array else
        f"    for (i = 0; i < {sig.length}; ++i) {{ {symbols['input_global']}.{sig.name}[i] = {sig.name}[i]; }}"
        for sig in inputs
    )
    output_loop = "    int i;\n" if any(sig.is_array for sig in outputs) else ""
    input_loop = "    int i;\n" if any(sig.is_array for sig in inputs) else ""
    term_stmt = f"    {symbols['term_func']}();\n" if "term_func" in symbols else ""
    testpoint_impl = render_testpoint_c_impl(api_prefix, testpoints)
    return f"""/* Auto-generated by sysplorer-svdpi */
#include "dpi.h"
#include "{model_stem}.h"
#include "{model_stem}_private.h"

#define {api_prefix}_DPI_SUCCESS 0
#define {api_prefix}_DPI_ERROR_NOT_INIT -1
#define {api_prefix}_DPI_ERROR_NULL_PTR -2
#define {api_prefix}_DPI_ERROR_EXECUTION -3

static int g_initialized = 0;

DPI_DLLESPEC int {api_prefix}_DPI_Init(void)
{{
    if (g_initialized) {{ return {api_prefix}_DPI_ERROR_EXECUTION; }}
    {symbols['init_func']}();
    g_initialized = 1;
    return {api_prefix}_DPI_SUCCESS;
}}

DPI_DLLESPEC int {api_prefix}_DPI_Reset(void)
{{
    if (!g_initialized) {{ return {api_prefix}_DPI_ERROR_NOT_INIT; }}
{term_stmt}    {symbols['init_func']}();
    return {api_prefix}_DPI_SUCCESS;
}}

DPI_DLLESPEC int {api_prefix}_DPI_Step(void)
{{
    if (!g_initialized) {{ return {api_prefix}_DPI_ERROR_NOT_INIT; }}
    {symbols['step_func']}();
    return {api_prefix}_DPI_SUCCESS;
}}

DPI_DLLESPEC int {api_prefix}_DPI_Terminate(void)
{{
    if (!g_initialized) {{ return {api_prefix}_DPI_ERROR_NOT_INIT; }}
{term_stmt}    g_initialized = 0;
    return {api_prefix}_DPI_SUCCESS;
}}

DPI_DLLESPEC int {api_prefix}_DPI_GetOutputs(
{comma_block([f"    {c_output_param(sig)}" for sig in outputs])})
{{
    if (!g_initialized) {{ return {api_prefix}_DPI_ERROR_NOT_INIT; }}
{output_loop}{output_checks}
{output_assignments}
    return {api_prefix}_DPI_SUCCESS;
}}

DPI_DLLESPEC int {api_prefix}_DPI_SetInputs(
{comma_block([f"    {c_input_param(sig)}" for sig in inputs])})
{{
    if (!g_initialized) {{ return {api_prefix}_DPI_ERROR_NOT_INIT; }}
{input_loop}{input_checks}
{input_assignments}
    return {api_prefix}_DPI_SUCCESS;
}}
{testpoint_impl}
"""


def render_testpoint_pkg_imports(api_prefix: str, testpoints: list[Testpoint]) -> str:
    if not testpoints:
        return ""
    return "\n".join(
        f'import "DPI-C" function int {api_prefix}_DPI_GetTestpoint_{tp.function_suffix}(output {sv_type(tp.base_type)} value);'
        for tp in testpoints
    )


def render_dpi_pkg(api_prefix: str, inputs: list[Signal], outputs: list[Signal], testpoints: list[Testpoint]) -> str:
    testpoint_imports = render_testpoint_pkg_imports(api_prefix, testpoints)
    if testpoint_imports:
        testpoint_imports = f"{testpoint_imports}\n"
    return f"""/* Auto-generated by sysplorer-svdpi */
`timescale 1ns / 1ns

package {api_prefix}_dpi_pkg;

localparam int {api_prefix}_DPI_SUCCESS = 0;
localparam int {api_prefix}_DPI_ERROR_NOT_INIT = -1;
localparam int {api_prefix}_DPI_ERROR_NULL_PTR = -2;
localparam int {api_prefix}_DPI_ERROR_EXECUTION = -3;

import "DPI-C" function int {api_prefix}_DPI_Init();
import "DPI-C" function int {api_prefix}_DPI_Reset();
import "DPI-C" function int {api_prefix}_DPI_Step();
import "DPI-C" function int {api_prefix}_DPI_Terminate();
import "DPI-C" function int {api_prefix}_DPI_GetOutputs(
{comma_block([sv_port("output", sig) for sig in outputs])});
import "DPI-C" function int {api_prefix}_DPI_SetInputs(
{comma_block([sv_port("input", sig) for sig in inputs])});
{testpoint_imports}

endpackage : {api_prefix}_dpi_pkg
"""


def scalar_refs(signals: list[Signal], prefix: str = "") -> list[str]:
    refs: list[str] = []
    for sig in signals:
        if sig.is_array:
            refs.extend(f"{prefix}{sig.name}[{i}]" for i in range(sig.length))
        else:
            refs.append(f"{prefix}{sig.name}")
    return refs


def render_open_candidates(handle_name: str, candidates: list[str], indent: str = "        ") -> str:
    if not candidates:
        return f"{indent}{handle_name} = 0;"
    lines = [f'{indent}{handle_name} = $fopen("{candidates[0]}", "r");']
    for candidate in candidates[1:]:
        lines.append(f"{indent}if ({handle_name} == 0) begin")
        lines.append(f'{indent}    {handle_name} = $fopen("{candidate}", "r");')
        lines.append(f"{indent}end")
    return "\n".join(lines)


def render_testpoint_sv_decls(testpoints: list[Testpoint]) -> str:
    return "\n".join(f"{sv_type(tp.base_type)} {tp.sv_var_name};" for tp in testpoints)


def render_testpoint_calls(api_prefix: str, testpoints: list[Testpoint], indent: str) -> str:
    if not testpoints:
        return ""
    lines: list[str] = []
    for tp in testpoints:
        lines.append(f"{indent}dpi_result = {api_prefix}_DPI_GetTestpoint_{tp.function_suffix}({tp.sv_var_name});")
        lines.append(f"{indent}if (dpi_result != {api_prefix}_DPI_SUCCESS) begin")
        lines.append(f'{indent}    $display("GetTestpoint {tp.trace_id} failed: %0d", dpi_result);')
        lines.append(f"{indent}    $fatal(1);")
        lines.append(f"{indent}end")
    return "\n".join(lines)


def render_smoke_initial_block(api_prefix: str, inputs: list[Signal], outputs: list[Signal], testpoints: list[Testpoint], smoke_steps: int, csv_mode: bool, model_stem: str, input_candidates: list[str]) -> str:
    input_zero = "\n".join(
        f"            {sig.name} = {scalar_default(sig)};"
        if not sig.is_array else
        f"            for (int i = 0; i < {sig.length}; i++) begin {sig.name}[i] = {scalar_default(sig)}; end"
        for sig in inputs
    )
    testpoint_calls = render_testpoint_calls(api_prefix, testpoints, "                ")
    read_fmt = ",".join(["%f"] + ["%f" if sv_type(sig.base_type) == "real" else "%d" for sig in inputs]) + "\\n"
    read_args = ",\n                ".join(["sample_time"] + [sig.name for sig in inputs])
    output_sample = "0.0" if not outputs else (f"{outputs[0].name}[0]" if outputs[0].is_array else outputs[0].name)
    if csv_mode:
        return f"""    int fd_in;
    int dpi_result;
    int r;
    string line;
    real sample_time;
    initial begin
{render_open_candidates("fd_in", input_candidates)}
        if ({api_prefix}_DPI_Init() != {api_prefix}_DPI_SUCCESS) $fatal(1, "Init failed");
        if (fd_in != 0) begin
            while (!$feof(fd_in)) begin
                r = $fscanf(fd_in, "{read_fmt}",
                {read_args});
                if (r < {len(inputs) + 1}) begin
                    void'($fgets(line, fd_in));
                    continue;
                end
                if ({sv_call(f"{api_prefix}_DPI_SetInputs", inputs, "                    ")} != {api_prefix}_DPI_SUCCESS) $fatal(1, "SetInputs failed");
                if ({api_prefix}_DPI_Step() != {api_prefix}_DPI_SUCCESS) $fatal(1, "Step failed");
                if ({sv_call(f"{api_prefix}_DPI_GetOutputs", outputs, "                    ")} != {api_prefix}_DPI_SUCCESS) $fatal(1, "GetOutputs failed");
{testpoint_calls}
                $display("sample=%f first_output=%f", sample_time, {output_sample});
            end
            $fclose(fd_in);
        end else begin
{input_zero}
            repeat ({smoke_steps}) begin
                if ({sv_call(f"{api_prefix}_DPI_SetInputs", inputs, "                    ")} != {api_prefix}_DPI_SUCCESS) $fatal(1, "SetInputs failed");
                if ({api_prefix}_DPI_Step() != {api_prefix}_DPI_SUCCESS) $fatal(1, "Step failed");
                if ({sv_call(f"{api_prefix}_DPI_GetOutputs", outputs, "                    ")} != {api_prefix}_DPI_SUCCESS) $fatal(1, "GetOutputs failed");
{testpoint_calls}
                $display("step first_output=%f", {output_sample});
            end
        end
        void'({api_prefix}_DPI_Terminate());
        $finish;
    end"""
    return f"""    initial begin
        int dpi_result;
        if ({api_prefix}_DPI_Init() != {api_prefix}_DPI_SUCCESS) $fatal(1, "Init failed");
{input_zero}
        repeat ({smoke_steps}) begin
            if ({sv_call(f"{api_prefix}_DPI_SetInputs", inputs, "                ")} != {api_prefix}_DPI_SUCCESS) $fatal(1, "SetInputs failed");
            if ({api_prefix}_DPI_Step() != {api_prefix}_DPI_SUCCESS) $fatal(1, "Step failed");
            if ({sv_call(f"{api_prefix}_DPI_GetOutputs", outputs, "                ")} != {api_prefix}_DPI_SUCCESS) $fatal(1, "GetOutputs failed");
{testpoint_calls}
            $display("step first_output=%f", {output_sample});
        end
        void'({api_prefix}_DPI_Terminate());
        $finish;
    end"""


def render_smoke_module(module_name: str, api_prefix: str, model_stem: str, inputs: list[Signal], outputs: list[Signal], testpoints: list[Testpoint], smoke_steps: int, csv_mode: bool, input_candidates: list[str]) -> str:
    signal_decls = "\n".join(f"{sv_decl(sig)}" for sig in outputs + inputs)
    testpoint_decls = render_testpoint_sv_decls(testpoints)
    decls = "\n".join(part for part in [signal_decls, testpoint_decls] if part)
    initial_block = render_smoke_initial_block(api_prefix, inputs, outputs, testpoints, smoke_steps, csv_mode, model_stem, input_candidates)
    return f"""/* Auto-generated by sysplorer-svdpi */
`timescale 1ns / 1ns
import {api_prefix}_dpi_pkg::*;

module {module_name};

{decls}
{initial_block}

endmodule
"""


def render_smoke_fallback_body(api_prefix: str, inputs: list[Signal], outputs: list[Signal], testpoints: list[Testpoint], smoke_steps: int) -> str:
    input_zero = "\n".join(
        f"            {sig.name} = {scalar_default(sig)};"
        if not sig.is_array else
        f"            for (int i = 0; i < {sig.length}; i++) begin {sig.name}[i] = {scalar_default(sig)}; end"
        for sig in inputs
    )
    testpoint_calls = render_testpoint_calls(api_prefix, testpoints, "                ")
    output_sample = "0.0" if not outputs else (f"{outputs[0].name}[0]" if outputs[0].is_array else outputs[0].name)
    return f"""{input_zero}
            repeat ({smoke_steps}) begin
                dpi_result = {sv_call(f"{api_prefix}_DPI_SetInputs", inputs, "                    ")};
                if (dpi_result != {api_prefix}_DPI_SUCCESS) begin
                    $display("SetInputs failed: %0d", dpi_result);
                    $fatal(1);
                end
                dpi_result = {api_prefix}_DPI_Step();
                if (dpi_result != {api_prefix}_DPI_SUCCESS) begin
                    $display("Step failed: %0d", dpi_result);
                    $fatal(1);
                end
                dpi_result = {sv_call(f"{api_prefix}_DPI_GetOutputs", outputs, "                    ")};
                if (dpi_result != {api_prefix}_DPI_SUCCESS) begin
                    $display("GetOutputs failed: %0d", dpi_result);
                    $fatal(1);
                end
{testpoint_calls}
                total_samples++;
                $display("step first_output=%f", {output_sample});
            end"""


def render_summary_line(sig: Signal, display_fn: str, handle: str | None = None) -> list[str]:
    prefix = f"{display_fn}({handle}, " if handle is not None else f"{display_fn}("
    if sig.is_array:
        fmt = ", ".join(["%0d"] * sig.length)
        refs = ", ".join(f"{sig.name}_mis[{i}]" for i in range(sig.length))
        return [
            f'            {prefix}"{sig.name} mismatches: [{fmt}]",',
            f"                {refs});",
        ]
    return [f'            {prefix}"{sig.name} mismatches: %0d", {sig.name}_mis);']


def render_compare_tb_module(
    api_prefix: str,
    model_stem: str,
    inputs: list[Signal],
    outputs: list[Signal],
    testpoints: list[Testpoint],
    smoke_steps: int,
    csv_mode: bool,
    input_candidates: list[str],
    expected_candidates: list[str],
) -> str:
    if not csv_mode:
        return render_smoke_module("model_tb", api_prefix, model_stem, inputs, outputs, testpoints, smoke_steps, False, input_candidates)

    signal_decls = "\n".join(f"{sv_decl(sig)}" for sig in outputs + inputs)
    testpoint_decls = render_testpoint_sv_decls(testpoints)
    decls = "\n".join(part for part in [signal_decls, testpoint_decls] if part)
    expected_decls = "\n".join(
        f"real exp_{sig.name}[{sig.length - 1}:0];" if sig.is_array else f"real exp_{sig.name};"
        for sig in outputs
    )
    mismatch_decls = "\n".join(
        f"int {sig.name}_mis[{sig.length - 1}:0];" if sig.is_array else f"int {sig.name}_mis;"
        for sig in outputs
    )
    input_fmt = ",".join(["%f"] + ["%f" if sv_type(sig.base_type) == "real" else "%d" for sig in inputs]) + "\\n"
    input_args = ",\n                ".join(["t"] + scalar_refs(inputs))
    expected_refs = scalar_refs(outputs, "exp_")
    expected_fmt = ",".join(["%f"] + ["%f"] * len(expected_refs)) + "\\n"
    expected_args = ",\n                    ".join(["t_exp"] + expected_refs)

    init_mismatch_lines: list[str] = []
    compare_lines: list[str] = []
    summary_file_lines: list[str] = []
    summary_console_lines: list[str] = []
    for sig in outputs:
        if sig.is_array:
            init_mismatch_lines.append(f"        for (int i = 0; i < {sig.length}; i++) begin")
            init_mismatch_lines.append(f"            {sig.name}_mis[i] = 0;")
            init_mismatch_lines.append("        end")
            compare_lines.append(f"                for (int i = 0; i < {sig.length}; i++) begin")
            compare_lines.append(f"                    if (abs_real({sig.name}[i] - exp_{sig.name}[i]) > tol) begin")
            compare_lines.append(f"                        {sig.name}_mis[i]++;")
            compare_lines.append("                        sample_mismatch = 1;")
            compare_lines.append("                    end")
            compare_lines.append("                end")
        else:
            init_mismatch_lines.append(f"        {sig.name}_mis = 0;")
            compare_lines.append(f"                if (abs_real({sig.name} - exp_{sig.name}) > tol) begin")
            compare_lines.append(f"                    {sig.name}_mis++;")
            compare_lines.append("                    sample_mismatch = 1;")
            compare_lines.append("                end")
        summary_file_lines.extend(render_summary_line(sig, "$fdisplay", "fd_sum"))
        summary_console_lines.extend(render_summary_line(sig, "$display"))

    output_sample = "0.0" if not outputs else (f"{outputs[0].name}[0]" if outputs[0].is_array else outputs[0].name)
    summary_file = "\n".join(summary_file_lines)
    summary_console = "\n".join(summary_console_lines)
    compare_body = "\n".join(compare_lines)
    init_mismatch = "\n".join(init_mismatch_lines)
    testpoint_calls = render_testpoint_calls(api_prefix, testpoints, "                ")

    return f"""/* Auto-generated by sysplorer-svdpi */
`timescale 1ns / 1ns
import {api_prefix}_dpi_pkg::*;

module model_tb;

{decls}
{expected_decls}
    int dpi_result;
    int fd_in;
    int fd_exp;
    int fd_sum;
    int r;
    int r_exp;
    real t;
    real t_exp;
    string line;
    bit has_expected;
    int mismatches;
    int printed;
    int total_samples;
    real tol;
{mismatch_decls}

    task automatic write_summary;
        begin
            fd_sum = $fopen("tb_compare_summary.txt", "w");
            if (fd_sum == 0) begin
                $display("Failed to open summary file: tb_compare_summary.txt");
                return;
            end
            $fdisplay(fd_sum, "Samples: %0d", total_samples);
            if (has_expected) begin
                if (mismatches == 0) begin
                    $fdisplay(fd_sum, "TEST RESULT: PASS");
                end else begin
                    $fdisplay(fd_sum, "TEST RESULT: FAIL");
                end
                $fdisplay(fd_sum, "mismatched samples: %0d (tol=%e)", mismatches, tol);
{summary_file}
            end else begin
                $fdisplay(fd_sum, "TEST RESULT: NO_EXPECTED_OUTPUT");
            end
            $fclose(fd_sum);
        end
    endtask

    function automatic real abs_real(input real v);
        if (v < 0.0) abs_real = -v;
        else abs_real = v;
    endfunction

    initial begin
        $display("{model_stem}TB (CSV) Start!");
        has_expected = 0;
        mismatches = 0;
        printed = 0;
        total_samples = 0;
        tol = 1e-6;
{init_mismatch}

        dpi_result = {api_prefix}_DPI_Init();
        if (dpi_result != {api_prefix}_DPI_SUCCESS) begin
            $display("Init failed: %0d", dpi_result);
            $fatal(1);
        end

{render_open_candidates("fd_in", input_candidates)}
{render_open_candidates("fd_exp", expected_candidates)}
        if (fd_exp != 0) begin
            has_expected = 1;
            void'($fgets(line, fd_exp));
            $display("Expected output compare enabled.");
        end else begin
            $display("Expected output CSV not found. Running input-only mode.");
        end

        if (fd_in != 0) begin
            while (!$feof(fd_in)) begin
                r = $fscanf(fd_in, "{input_fmt}",
                {input_args});
                if (r < {len(scalar_refs(inputs)) + 1}) begin
                    void'($fgets(line, fd_in));
                    continue;
                end

                if (has_expected) begin
                    r_exp = $fscanf(fd_exp,
                    "{expected_fmt}",
                    {expected_args});
                    if (r_exp != {len(expected_refs) + 1}) begin
                        if ($feof(fd_exp)) begin
                            $display("Expected output CSV ended early at t=%f", t);
                        end else begin
                            $display("Failed to parse expected output CSV at t=%f", t);
                        end
                        $fatal(1);
                    end
                    if (abs_real(t - t_exp) > tol) begin
                        $display("Time mismatch: input t=%f output t=%f", t, t_exp);
                        $fatal(1);
                    end
                end

                dpi_result = {sv_call(f"{api_prefix}_DPI_SetInputs", inputs, "                    ")};
                if (dpi_result != {api_prefix}_DPI_SUCCESS) begin
                    $display("SetInputs failed: %0d", dpi_result);
                    $fatal(1);
                end

                dpi_result = {api_prefix}_DPI_Step();
                if (dpi_result != {api_prefix}_DPI_SUCCESS) begin
                    $display("Step failed: %0d", dpi_result);
                    $fatal(1);
                end

                dpi_result = {sv_call(f"{api_prefix}_DPI_GetOutputs", outputs, "                    ")};
                if (dpi_result != {api_prefix}_DPI_SUCCESS) begin
                    $display("GetOutputs failed: %0d", dpi_result);
                    $fatal(1);
                end
{testpoint_calls}

                total_samples++;

                if (has_expected) begin
                    bit sample_mismatch;
                    sample_mismatch = 0;
{compare_body}
                    if (sample_mismatch) begin
                        mismatches++;
                        if (printed < 10) begin
                            $display("Mismatch detected at t=%f first_output=%f", t, {output_sample});
                            printed++;
                        end
                    end
                end else begin
                    $display("sample=%f first_output=%f", t, {output_sample});
                end
            end
            $fclose(fd_in);
        end else begin
            $display("Input CSV not found. Falling back to smoke mode.");
            if (fd_exp != 0) begin
                $fclose(fd_exp);
                fd_exp = 0;
            end
            has_expected = 0;
{render_smoke_fallback_body(api_prefix, inputs, outputs, testpoints, smoke_steps)}
        end

        if (fd_exp != 0) begin
            $fclose(fd_exp);
        end
        dpi_result = {api_prefix}_DPI_Terminate();
        if (dpi_result != {api_prefix}_DPI_SUCCESS) begin
            $display("Terminate failed: %0d", dpi_result);
            $fatal(1);
        end

        if (has_expected) begin
            if (mismatches == 0) begin
                $display("{model_stem}TB (CSV) Completed. TEST RESULT: PASS");
            end else begin
                $display("{model_stem}TB (CSV) Completed. TEST RESULT: FAIL");
            end
            $display("Samples: %0d", total_samples);
            $display("mismatched samples: %0d (tol=%e)", mismatches, tol);
{summary_console}
        end else begin
            $display("{model_stem}TB (CSV) Completed. TEST RESULT: NO_EXPECTED_OUTPUT");
        end
        write_summary();
        $finish;
    end

endmodule
"""


def render_simulate_do(model_stem: str, has_julia: bool) -> str:
    julia_hint = "# Julia artifacts are handled automatically when julia_blocks.lib exists." if has_julia else "# No Julia artifacts detected."
    return f"""# Auto-generated by sysplorer-svdpi
# Batch compile and run helper for ModelSim/Questa.

if {{[info exists env(TB_TOP)]}} {{
    set tb_top $env(TB_TOP)
}} else {{
    set tb_top "model_tb"
}}

if {{[info exists env(WAVE_WLF)] && $env(WAVE_WLF) ne ""}} {{
    set wave_wlf $env(WAVE_WLF)
}} else {{
    set wave_wlf "waves.wlf"
}}

if {{[info exists env(WAVE_SCOPE)] && $env(WAVE_SCOPE) ne ""}} {{
    set wave_scope $env(WAVE_SCOPE)
}} else {{
    set wave_scope "/$tb_top/*"
}}

if {{[info exists env(WAVE_VCD)] && $env(WAVE_VCD) ne ""}} {{
    set wave_vcd $env(WAVE_VCD)
}} else {{
    set wave_vcd ""
}}

set worklib "work"
if {{![file isdirectory $worklib]}} {{
    vlib $worklib
}}

set sv_files [list]
foreach f {{dpi_pkg.sv dpi.sv tb.sv}} {{
    if {{[file exists $f]}} {{
        lappend sv_files $f
    }}
}}

set c_files [list]
foreach f {{dpi.c julia_blocks_private.c}} {{
    if {{[file exists $f]}} {{
        lappend c_files $f
    }}
}}
foreach f [glob -nocomplain *.c] {{
    if {{$f ni {{dpi.c julia_blocks_private.c mwb_main.c}}}} {{
        lappend c_files $f
    }}
}}
foreach f [glob -nocomplain extern_inc/*.c] {{
    lappend c_files $f
}}
foreach f [list "mwb_infnan.c" "../mwb_infnan.c" "../../mwb_infnan.c" "../../../mwb_infnan.c"] {{
    if {{[file exists $f]}} {{
        lappend c_files $f
        break
    }}
}}

set cc_inc_flags "-I. -I.. -I../.. -I../../.. -Iextern_inc"
puts "Compiling SV files: $sv_files"
puts "Compiling C files : $c_files"
eval [concat [list vlog -nolock -work $worklib -sv -mfcu -ccflags $cc_inc_flags] $sv_files $c_files]

set vsim_cmd [list vsim -c -voptargs=+acc]
set julia_bin "[pwd]/julia_blocks_codegen/bin"
set julia_lib "$julia_bin/julia_blocks.lib"
{julia_hint}
if {{[file exists $julia_lib]}} {{
    set env(PATH) "$julia_bin;$env(PATH)"
    lappend vsim_cmd -ldflags "-L$julia_bin -l:julia_blocks.lib"
}}
lappend vsim_cmd -wlf $wave_wlf
lappend vsim_cmd "$worklib.$tb_top"
eval $vsim_cmd
if {{[catch {{eval [list log -r $wave_scope]}} wave_log_err]}} {{
    puts "Wave logging on $wave_scope failed: $wave_log_err"
    puts "Falling back to log -r /*"
    log -r /*
}}
if {{$wave_vcd ne ""}} {{
    vcd file $wave_vcd
    if {{[catch {{eval [list vcd add -r $wave_scope]}} wave_vcd_err]}} {{
        puts "VCD add on $wave_scope failed: $wave_vcd_err"
        puts "Falling back to vcd add -r /*"
        vcd add -r /*
    }}
}}
run -all
if {{$wave_vcd ne ""}} {{
    vcd flush
}}
quit -f
"""


def render_wave_do() -> str:
    return """# Auto-generated by sysplorer-svdpi
# GUI helper for ModelSim/Questa wave window.

if {[info exists tb_top]} {
    set wave_scope "/$tb_top/*"
} elseif {[info exists env(TB_TOP)]} {
    set wave_scope "/$env(TB_TOP)/*"
} else {
    set wave_scope "/model_tb/*"
}

view wave
quietly WaveActivateNextPane {} 0
add wave -r $wave_scope
configure wave -namecolwidth 240
configure wave -valuecolwidth 120
configure wave -justifyvalue left
configure wave -signalnamewidth 1
configure wave -timelineunits ns
"""


def write_file(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"{path} already exists; pass --force to overwrite")
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def build_metadata(
    codegen_dir: Path,
    output_dir: Path,
    model_stem: str,
    api_prefix: str,
    inputs: list[Signal],
    outputs: list[Signal],
    available_testpoints: list[Testpoint],
    selected_testpoints: list[Testpoint],
    step_size: str | None,
    has_julia: bool,
    csv_mode: bool,
    generated_files: list[str],
    extra_warnings: list[str],
    unresolved_testpoints: list[str],
) -> dict[str, object]:
    warnings: list[str] = []
    if not csv_mode:
        warnings.append("tb.sv fell back to smoke mode because root inputs include arrays or no scalar CSV shape was inferred.")
    if not selected_testpoints:
        warnings.append("No testpoint accessors were generated.")
    if has_julia:
        warnings.append("Julia artifacts were detected, but this MVP only passes them through and does not build Julia dependencies.")
    warnings.extend(extra_warnings)
    if unresolved_testpoints:
        warnings.append(f"Unresolved testpoint requests: {unresolved_testpoints}")
    return {
        "codegen_dir": str(codegen_dir),
        "output_dir": str(output_dir),
        "model_stem": model_stem,
        "api_prefix": api_prefix,
        "step_size": step_size,
        "has_julia": has_julia,
        "supports_csv_tb": csv_mode,
        "inputs": [asdict(sig) for sig in inputs],
        "outputs": [asdict(sig) for sig in outputs],
        "available_testpoints": [asdict(tp) for tp in available_testpoints],
        "selected_testpoints": [asdict(tp) for tp in selected_testpoints],
        "unresolved_testpoints": unresolved_testpoints,
        "generated_files": generated_files,
        "warnings": warnings,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Render minimal SV-DPI wrapper files from a Sysplorer codegen directory.")
    parser.add_argument("--codegen-dir", required=True)
    parser.add_argument("--output-dir", help="optional output folder; defaults to --codegen-dir")
    parser.add_argument("--model-stem")
    parser.add_argument("--api-prefix", default="model")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--skip-simulate-do", action="store_true")
    parser.add_argument("--smoke-steps", type=int, default=10)
    parser.add_argument("--testpoint", action="append", default=[], help="exact testpoint id from motrace.json; repeatable")
    parser.add_argument("--testpoint-nl", help="heuristic natural-language selection over motrace candidate ids")
    parser.add_argument("--list-testpoints", action="store_true", help="print parsed motrace candidates and exit")
    args = parser.parse_args()

    codegen_dir = Path(args.codegen_dir).resolve()
    output_dir = Path(args.output_dir).resolve() if args.output_dir else codegen_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    api_prefix = sanitize_prefix(args.api_prefix)
    model_stem = detect_model_stem(codegen_dir, args.model_stem)

    header_text = read_text(codegen_dir / f"{model_stem}.h")
    private_text = read_text(codegen_dir / f"{model_stem}_private.h")
    source_text = read_text(codegen_dir / f"{model_stem}.c")

    symbols = parse_main_header(header_text)
    inputs = extract_struct_fields(private_text, symbols["input_struct"])
    outputs = extract_struct_fields(private_text, symbols["output_struct"])
    blocks = extract_struct_fields(private_text, symbols["block_struct"]) if "block_struct" in symbols else []
    states = extract_struct_fields(private_text, symbols["state_struct"]) if "state_struct" in symbols else []
    step_size = parse_step_size(source_text, symbols["md_global"])
    has_julia = detect_julia(codegen_dir)
    available_testpoints = collect_testpoint_candidates(codegen_dir, symbols, inputs, outputs, blocks, states)
    if args.list_testpoints:
        print(json.dumps([asdict(tp) for tp in available_testpoints], ensure_ascii=False, indent=2))
        return
    selected_testpoints, unresolved_testpoints, testpoint_warnings = resolve_requested_testpoints(args.testpoint, args.testpoint_nl, available_testpoints)
    if args.testpoint and any(item not in {tp.trace_id for tp in selected_testpoints} for item in [req.strip().lstrip("-") for req in args.testpoint]):
        if unresolved_testpoints:
            raise ValueError(f"unresolved testpoint requests: {unresolved_testpoints}")
    if (args.testpoint or args.testpoint_nl) and not selected_testpoints:
        raise ValueError("no testpoints were resolved from the provided requests")
    csv_mode = bool(inputs) and all(not sig.is_array for sig in inputs)
    nearby_input_files = discover_nearby_csv_files(codegen_dir, "_input.csv")
    nearby_output_files = discover_nearby_csv_files(codegen_dir, "_output.csv")
    common_csv_bases = dedupe_keep_order([base for base, _ in nearby_output_files if any(input_base == base for input_base, _ in nearby_input_files)])
    input_candidates = discover_csv_candidates(codegen_dir, output_dir, model_stem, "_input.csv", common_csv_bases)
    expected_candidates = discover_csv_candidates(codegen_dir, output_dir, model_stem, "_output.csv", common_csv_bases)

    generated_files = ["dpi.h", "dpi.c", "dpi_pkg.sv", "dpi.sv", "tb.sv", "_svdpi_metadata.json"]
    if not args.skip_simulate_do:
        generated_files.extend(["simulate.do", "wave.do"])

    write_file(output_dir / "dpi.h", render_dpi_h(model_stem, api_prefix, inputs, outputs, selected_testpoints), args.force)
    write_file(output_dir / "dpi.c", render_dpi_c(model_stem, api_prefix, symbols, inputs, outputs, selected_testpoints), args.force)
    write_file(output_dir / "dpi_pkg.sv", render_dpi_pkg(api_prefix, inputs, outputs, selected_testpoints), args.force)
    write_file(output_dir / "dpi.sv", render_smoke_module(f"{api_prefix}_dpi", api_prefix, model_stem, inputs, outputs, selected_testpoints, args.smoke_steps, False, input_candidates), args.force)
    write_file(output_dir / "tb.sv", render_compare_tb_module(api_prefix, model_stem, inputs, outputs, selected_testpoints, args.smoke_steps, csv_mode, input_candidates, expected_candidates), args.force)
    if not args.skip_simulate_do:
        write_file(output_dir / "simulate.do", render_simulate_do(model_stem, has_julia), args.force)
        write_file(output_dir / "wave.do", render_wave_do(), args.force)

    metadata = build_metadata(
        codegen_dir=codegen_dir,
        output_dir=output_dir,
        model_stem=model_stem,
        api_prefix=api_prefix,
        inputs=inputs,
        outputs=outputs,
        available_testpoints=available_testpoints,
        selected_testpoints=selected_testpoints,
        step_size=step_size,
        has_julia=has_julia,
        csv_mode=csv_mode,
        generated_files=generated_files,
        extra_warnings=testpoint_warnings,
        unresolved_testpoints=unresolved_testpoints,
    )
    write_file(output_dir / "_svdpi_metadata.json", json.dumps(metadata, ensure_ascii=False, indent=2), args.force)
    print(json.dumps(metadata, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
