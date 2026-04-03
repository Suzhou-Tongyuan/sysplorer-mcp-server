#!/usr/bin/env bash
# 与 install_mcp.ps1 对齐：
# - 仅支持源码包：main.py + sysplorer-mcp-server/ + resources/
# - 使用 Python 启动 main.py，并写入 Claude / OpenCode / Codex 配置
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

usage() {
  printf 'Usage: %s [-d MWORKS_DIR] [-p PLATFORM_LABEL]\n' "$(basename "$0")" >&2
  printf '  Env: MWORKS_INSTALL_DIR, SYSPLORER_PLATFORM_LABEL, PYTHON_BIN (override)\n' >&2
  exit 1
}

MWORKS_INSTALL_DIR_INPUT="${MWORKS_INSTALL_DIR:-}"
SYSPLORER_PLATFORM_LABEL_INPUT="${SYSPLORER_PLATFORM_LABEL:-}"

while [ $# -gt 0 ]; do
  case "$1" in
    -d|--mworks-install-dir)
      MWORKS_INSTALL_DIR_INPUT="${2:-}"
      shift 2 || usage
      ;;
    -p|--sysplorer-platform-label)
      SYSPLORER_PLATFORM_LABEL_INPUT="${2:-}"
      shift 2 || usage
      ;;
    -h|--help)
      usage
      ;;
    *)
      printf 'Unknown argument: %s\n' "$1" >&2
      usage
      ;;
  esac
done

resolve_sysplorer_python() {
  local root="$1"
  local c
  for c in \
    "$root/external/python64/bin/python3" \
    "$root/external/python64/bin/python"
  do
    if [ -x "$c" ]; then
      printf '%s\n' "$c"
      return 0
    fi
  done
  return 1
}

resolve_json_python() {
  local c
  for c in python3 python python2; do
    if command -v "$c" >/dev/null 2>&1; then
      command -v "$c"
      return 0
    fi
  done
  return 1
}

print_build_info() {
  local p="$SCRIPT_DIR/MCP_BUILD_INFO.json"
  local json_python=""
  if [ ! -f "$p" ]; then
    printf 'MCP_BUILD_INFO.json not found; version/build time unknown.\n\n' >&2
    return 0
  fi
  json_python="$(resolve_json_python || true)"
  if [ -z "$json_python" ]; then
    return 0
  fi
  MCP_INFO_JSON="$p" "$json_python" - <<'PY' || true
from __future__ import print_function
import io
import json
import os

p = os.environ.get("MCP_INFO_JSON", "")
try:
    with io.open(p, "r", encoding="utf-8-sig") as f:
        d = json.load(f)
except IOError:
    raise SystemExit(0)
_vd = d.get("version_display") or d.get("version") or ""
print("-----------------------------------------------")
print(" Package version:       {0}".format(_vd))
print(" Build time:            {0}".format(d.get("build_time", "")))
gr = d.get("git_revision")
if gr and gr != "unknown":
    print(" Git revision:          {0}".format(gr))
print("-----------------------------------------------")
print("")
PY
}

pip_check_mcp() {
  local py="$1"
  printf '\nChecking whether pip list contains package mcp (Sysplorer Python)...\n'
  if ! "$py" -m pip list >/dev/null 2>&1; then
    printf 'Could not run pip list; please confirm mcp is installed.\n' >&2
    return 0
  fi
  if "$py" -m pip list 2>/dev/null | awk '{print $1}' | grep -qx 'mcp'; then
    printf '[OK] pip list shows mcp.\n'
  else
    printf 'mcp not found in pip list for this interpreter.\n' >&2
    printf 'Install with:\n  "%s" -m pip install mcp\n' "$py" >&2
  fi
}

write_all_client_configs() {
  local mworks="$1"
  local label="$2"
  local py="$3"
  local main_py="$4"
  local claude="$HOME/.claude.json"
  local opencode_dir="$HOME/.config/opencode"
  local opencode="$opencode_dir/opencode.json"
  local codex="$HOME/.codex/config.toml"

  export MCP_MWORKS_DIR="$mworks"
  export MCP_PLATFORM_LABEL="$label"
  export MCP_PYTHON="$py"
  export MCP_MAIN_PY="$main_py"
  export MCP_CLAUDE="$claude"
  export MCP_OPENCODE="$opencode"
  export MCP_CODEX="$codex"

  local json_python=""
  json_python="$(resolve_json_python || true)"
  if [ -z "$json_python" ]; then
    printf 'Error: python/python2/python3 is required to merge JSON/TOML client configs.\n' >&2
    exit 1
  fi

  mkdir -p "$opencode_dir" "$HOME/.codex"

  "$json_python" - <<'PY'
from __future__ import print_function
import io
import json
import os
import re

try:
    JSONDecodeError = json.JSONDecodeError
except AttributeError:
    JSONDecodeError = ValueError


def load_json(path):
    if os.path.exists(path):
        try:
            with io.open(path, "r", encoding="utf-8-sig") as f:
                content = f.read() or u"{}"
            return json.loads(content)
        except JSONDecodeError as exc:
            raise SystemExit("Invalid JSON in {0}: {1}".format(path, exc))
    return {}


def remove_mcp_servers_block(text, server_key):
    header = "[mcp_servers.{0}]".format(server_key)
    lines = re.split(r"\r\n|\n|\r", text)
    out = []
    i = 0
    while i < len(lines):
        if lines[i].strip() == header:
            i += 1
            while i < len(lines) and not re.match(r"^\s*\[", lines[i]):
                i += 1
            continue
        out.append(lines[i])
        i += 1
    return "\n".join(out)


def escape_toml_single(s):
    return s.replace("'", "''")


def write_text(path, content):
    parent = os.path.dirname(path)
    if parent and not os.path.exists(parent):
        os.makedirs(parent)
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


def write_codex_toml(path, command, args):
    parent = os.path.dirname(path)
    if parent and not os.path.exists(parent):
        os.makedirs(parent)
    if os.path.exists(path):
        with io.open(path, "r", encoding="utf-8-sig") as f:
            body = f.read()
    else:
        body = u""
    body = remove_mcp_servers_block(body, "sysplorer_mcp")
    body = remove_mcp_servers_block(body, "mworks_mcp")
    lines = [
        "[mcp_servers.sysplorer_mcp]",
        "command = '{0}'".format(escape_toml_single(command)),
        "args = [",
    ]
    for a in args:
        lines.append("    '{0}',".format(escape_toml_single(a)))
    lines.append("]")
    block = "\n".join(lines) + "\n"
    body = body.rstrip()
    if body:
        body = body + "\n\n" + block
    else:
        body = block
    write_text(path, body.rstrip() + "\n")


mworks = os.environ["MCP_MWORKS_DIR"]
label = os.environ["MCP_PLATFORM_LABEL"]
py = os.environ["MCP_PYTHON"]
main = os.environ["MCP_MAIN_PY"]
claude_p = os.environ["MCP_CLAUDE"]
opencode_p = os.environ["MCP_OPENCODE"]
codex_p = os.environ["MCP_CODEX"]
main_res = os.path.abspath(main)

claude_data = load_json(claude_p)
ms = claude_data.setdefault("mcpServers", {})
ms.pop("mworks_mcp", None)
ms["sysplorer_mcp"] = {
    "command": py,
    "args": [
        main_res,
        "--mworks-install-dir",
        mworks,
        "--sysplorer-platform-label",
        label,
    ],
}
write_text(claude_p, json.dumps(claude_data, indent=2, ensure_ascii=False) + "\n")

opencode_data = load_json(opencode_p)
mcp = opencode_data.setdefault("mcp", {})
mcp.pop("mworks_mcp", None)
mcp["sysplorer_mcp"] = {
    "type": "local",
    "command": [
        py,
        main_res,
        "--mworks-install-dir",
        mworks,
        "--sysplorer-platform-label",
        label,
    ],
}
write_text(opencode_p, json.dumps(opencode_data, indent=2, ensure_ascii=False) + "\n")

write_codex_toml(
    codex_p,
    py,
    [
        main_res,
        "--mworks-install-dir",
        mworks,
        "--sysplorer-platform-label",
        label,
    ],
)
PY
}

backup_if_exists() {
  local f="$1"
  if [ -f "$f" ]; then
    local stamp
    stamp="$(date +%Y%m%d-%H%M%S%3N 2>/dev/null || date +%Y%m%d-%H%M%S)"
    cp -p "$f" "${f}.bak.${stamp}"
    printf 'Backed up: %s -> %s.bak.%s\n' "$f" "$f" "$stamp"
  fi
}

MAIN_PY="$SCRIPT_DIR/main.py"
PKG_DIR="$SCRIPT_DIR/sysplorer-mcp-server"
RES_DIR="$SCRIPT_DIR/resources"

if [ ! -f "$MAIN_PY" ] || [ ! -d "$PKG_DIR" ] || [ ! -d "$RES_DIR" ]; then
  printf 'Error: source bundle files not found next to this script.\n' >&2
  printf 'Expected:\n' >&2
  printf '  - %s\n' "$MAIN_PY" >&2
  printf '  - %s\n' "$PKG_DIR" >&2
  printf '  - %s\n' "$RES_DIR" >&2
  exit 1
fi

print_build_info

printf '=== MWorks MCP (Python + main.py) ===\n'
printf 'Bundle root: %s\n\n' "$SCRIPT_DIR"
DEFAULT_MWORKS="/usr/local/MWORKS/Sysplorer-2026a"
DEFAULT_LABEL="Sysplorer 2026a"

if [ -z "$MWORKS_INSTALL_DIR_INPUT" ]; then
  read -r -p "Enter Sysplorer installation path (default: $DEFAULT_MWORKS): " MWORKS_INSTALL_DIR_INPUT
fi
mworks_dir="${MWORKS_INSTALL_DIR_INPUT:-$DEFAULT_MWORKS}"

if [ -z "$SYSPLORER_PLATFORM_LABEL_INPUT" ]; then
  read -r -p "Enter Sysplorer platform label (default: $DEFAULT_LABEL): " SYSPLORER_PLATFORM_LABEL_INPUT
fi
platform_label="${SYSPLORER_PLATFORM_LABEL_INPUT:-$DEFAULT_LABEL}"

if [ ! -d "$mworks_dir" ]; then
  printf 'Warning: path does not exist: %s\n' "$mworks_dir" >&2
  read -r -p "Continue? (y/N): " cont
  case "$cont" in
    y|Y) ;;
    *) exit 0 ;;
  esac
fi

python_exe=""
if [ -n "${PYTHON_BIN:-}" ]; then
  if [ -x "$PYTHON_BIN" ]; then
    python_exe="$PYTHON_BIN"
  elif command -v "$PYTHON_BIN" >/dev/null 2>&1; then
    python_exe="$(command -v "$PYTHON_BIN")"
  fi
fi
if [ -z "$python_exe" ]; then
  python_exe="$(resolve_sysplorer_python "$mworks_dir" || true)"
fi
if [ -z "$python_exe" ]; then
  read -r -p "Enter Python interpreter path for MCP (Sysplorer or compatible): " python_exe
fi
if [ -z "$python_exe" ] || [ ! -x "$python_exe" ]; then
  printf 'Error: Python interpreter not executable: %s\n' "${python_exe:-<empty>}" >&2
  exit 1
fi

main_py_full="$(readlink -f "$MAIN_PY" 2>/dev/null || realpath "$MAIN_PY" 2>/dev/null || echo "$MAIN_PY")"
printf '\nUsing:\n  Sysplorer: %s\n  Python:    %s\n  main.py:   %s\n  Label:     %s\n\n' \
  "$mworks_dir" "$python_exe" "$main_py_full" "$platform_label"

printf 'Backing up existing configuration files (if any)...\n'
backup_if_exists "$HOME/.claude.json"
backup_if_exists "$HOME/.config/opencode/opencode.json"
backup_if_exists "$HOME/.codex/config.toml"
printf '\n'

write_all_client_configs "$mworks_dir" "$platform_label" "$python_exe" "$main_py_full"
printf 'Claude configuration updated: %s\n' "$HOME/.claude.json"
printf 'OpenCode configuration updated: %s\n' "$HOME/.config/opencode/opencode.json"
printf 'Codex configuration updated: %s\n' "$HOME/.codex/config.toml"

pip_check_mcp "$python_exe"

printf '\nConfiguration completed. Restart Claude Code / OpenCode / Codex CLI to load MCP.\n'
printf 'To uninstall, remove sysplorer_mcp from the corresponding config files.\n'
