#!/usr/bin/env bash
# 与仓库根目录 install_sysplorer_mcp_tools.ps1 / install/dist/install_mcp.ps1 对齐：
# - 源码包：main.py + sysplorer-mcp-server/ + resources/（由 build_publish.sh 产出）→ 使用 Sysplorer 自带 Python 启动 main.py
# - 二进制包：sysplorer_mcp_server（PyInstaller 等）→ command 为可执行文件路径
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
    "$root/External/python64/python" \
    "$root/External/python64/python3" \
    "$root/bin/python3" \
    "$root/bin/python"
  do
    if [ -x "$c" ]; then
      printf '%s\n' "$c"
      return 0
    fi
  done
  return 1
}

resolve_default_binary_launcher() {
  if [ -e "$SCRIPT_DIR/sysplorer_mcp_server" ]; then
    printf '%s\n' "$SCRIPT_DIR/sysplorer_mcp_server"
    return 0
  fi
  printf '%s\n' "$SCRIPT_DIR/../../dist/linux-x64/sysplorer_mcp_server"
}

print_build_info() {
  local p="$SCRIPT_DIR/MCP_BUILD_INFO.json"
  if [ ! -f "$p" ]; then
    printf 'MCP_BUILD_INFO.json not found; version/build time unknown.\n\n' >&2
    return 0
  fi
  if ! command -v python3 >/dev/null 2>&1; then
    return 0
  fi
  MCP_INFO_JSON="$p" python3 - <<'PY' || true
import json, os
p = os.environ.get("MCP_INFO_JSON", "")
try:
    d = json.load(open(p, encoding="utf-8"))
except OSError:
    raise SystemExit(0)
_vd = d.get("version_display") or d.get("version") or ""
print("-----------------------------------------------")
print(" Package version:       ", _vd)
print(" Build time:            ", d.get("build_time", ""))
gr = d.get("git_revision")
if gr and gr != "unknown":
    print(" Git revision:          ", gr)
print("-----------------------------------------------")
print()
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
  local mode="$1"
  local mworks="$2"
  local label="$3"
  local claude="$HOME/.claude.json"
  local opencode_dir="$HOME/.config/opencode"
  local opencode="$opencode_dir/opencode.json"
  local codex="$HOME/.codex/config.toml"

  export MCP_INSTALL_MODE="$mode"
  export MCP_MWORKS_DIR="$mworks"
  export MCP_PLATFORM_LABEL="$label"
  export MCP_CLAUDE="$claude"
  export MCP_OPENCODE="$opencode"
  export MCP_CODEX="$codex"

  if [ "$mode" = "source" ]; then
    export MCP_PYTHON="$4"
    export MCP_MAIN_PY="$5"
  else
    export MCP_LAUNCHER="$4"
  fi

  mkdir -p "$opencode_dir" "$HOME/.codex"

  python3 - <<'PY'
import json
import os
import pathlib
import re


def load_json(path: pathlib.Path) -> dict:
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8") or "{}")
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Invalid JSON in {path}: {exc}")
    return {}


def remove_mcp_servers_block(text: str, server_key: str) -> str:
    header = f"[mcp_servers.{server_key}]"
    lines = re.split(r"\r\n|\n|\r", text)
    out: list[str] = []
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


def escape_toml_single(s: str) -> str:
    return s.replace("'", "''")


def write_codex_toml(path: pathlib.Path, command: str, args: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    body = path.read_text(encoding="utf-8") if path.exists() else ""
    body = remove_mcp_servers_block(body, "sysplorer_mcp")
    body = remove_mcp_servers_block(body, "mworks_mcp")
    lines = [
        "[mcp_servers.sysplorer_mcp]",
        f"command = '{escape_toml_single(command)}'",
        "args = [",
    ]
    for a in args:
        lines.append(f"    '{escape_toml_single(a)}',")
    lines.append("]")
    block = "\n".join(lines) + "\n"
    body = body.rstrip()
    if body:
        body = body + "\n\n" + block
    else:
        body = block
    path.write_text(body.rstrip() + "\n", encoding="utf-8")


mode = os.environ["MCP_INSTALL_MODE"]
mworks = os.environ["MCP_MWORKS_DIR"]
label = os.environ["MCP_PLATFORM_LABEL"]
claude_p = pathlib.Path(os.environ["MCP_CLAUDE"])
opencode_p = pathlib.Path(os.environ["MCP_OPENCODE"])
codex_p = pathlib.Path(os.environ["MCP_CODEX"])

if mode == "source":
    py = os.environ["MCP_PYTHON"]
    main = os.environ["MCP_MAIN_PY"]
    main_res = str(pathlib.Path(main).resolve())
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
    claude_p.write_text(json.dumps(claude_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

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
    opencode_p.write_text(json.dumps(opencode_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

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
else:
    launcher = os.environ["MCP_LAUNCHER"]
    launcher_res = str(pathlib.Path(launcher).resolve())
    claude_data = load_json(claude_p)
    ms = claude_data.setdefault("mcpServers", {})
    ms.pop("mworks_mcp", None)
    ms["sysplorer_mcp"] = {
        "command": launcher_res,
        "args": [
            "--mworks-install-dir",
            mworks,
            "--sysplorer-platform-label",
            label,
        ],
    }
    claude_p.write_text(json.dumps(claude_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    opencode_data = load_json(opencode_p)
    mcp = opencode_data.setdefault("mcp", {})
    mcp.pop("mworks_mcp", None)
    mcp["sysplorer_mcp"] = {
        "type": "local",
        "command": [
            launcher_res,
            "--mworks-install-dir",
            mworks,
            "--sysplorer-platform-label",
            label,
        ],
    }
    opencode_p.write_text(json.dumps(opencode_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    write_codex_toml(
        codex_p,
        launcher_res,
        [
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

# --- 模式：源码包 vs 二进制 ---
MAIN_PY="$SCRIPT_DIR/main.py"
PKG_DIR="$SCRIPT_DIR/sysplorer-mcp-server"
RES_DIR="$SCRIPT_DIR/resources"
BINARY_LAUNCHER="$SCRIPT_DIR/sysplorer_mcp_server"

if [ -f "$MAIN_PY" ] && [ -d "$PKG_DIR" ] && [ -d "$RES_DIR" ]; then
  INSTALL_MODE="source"
elif [ -e "$BINARY_LAUNCHER" ]; then
  INSTALL_MODE="binary"
else
  printf 'Error: unsupported layout next to this script.\n' >&2
  printf 'Expected either:\n' >&2
  printf '  - Source bundle: main.py, sysplorer-mcp-server/, resources/ (run install/linux/scripts/build_publish.sh)\n' >&2
  printf '  - Binary bundle: sysplorer_mcp_server executable\n' >&2
  printf 'Bundle root: %s\n' "$SCRIPT_DIR" >&2
  exit 1
fi

print_build_info

if [ "$INSTALL_MODE" = "source" ]; then
  printf '=== MWorks MCP (Sysplorer Python) — source bundle ===\n'
  printf 'Bundle root: %s\n\n' "$SCRIPT_DIR"
  DEFAULT_MWORKS="/opt/MWORKS/Sysplorer-2026a"
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

  if ! command -v python3 >/dev/null 2>&1; then
    printf 'Error: python3 is required to merge JSON/TOML client configs.\n' >&2
    exit 1
  fi

  write_all_client_configs "source" "$mworks_dir" "$platform_label" "$python_exe" "$main_py_full"
  printf 'Claude configuration updated: %s\n' "$HOME/.claude.json"
  printf 'OpenCode configuration updated: %s\n' "$HOME/.config/opencode/opencode.json"
  printf 'Codex configuration updated: %s\n' "$HOME/.codex/config.toml"

  pip_check_mcp "$python_exe"
else
  printf '=== MWorks MCP — binary launcher ===\n'
  printf 'Note: Sysplorer-backed runtime features remain mostly Windows-oriented.\n\n'

  DEFAULT_LAUNCHER="$(resolve_default_binary_launcher)"
  DEFAULT_MWORKS="${MWORKS_INSTALL_DIR:-/opt/MWORKS/Sysplorer-2026a}"
  DEFAULT_LABEL="${SYSPLORER_PLATFORM_LABEL:-Sysplorer 2026a}"

  read -r -p "Enter Linux launcher path (default: $DEFAULT_LAUNCHER): " launcher_path
  launcher_path="${launcher_path:-$DEFAULT_LAUNCHER}"

  if [ -z "$MWORKS_INSTALL_DIR_INPUT" ]; then
    read -r -p "Enter MWorks install dir value to record (default: $DEFAULT_MWORKS): " MWORKS_INSTALL_DIR_INPUT
  fi
  mworks_dir="${MWORKS_INSTALL_DIR_INPUT:-$DEFAULT_MWORKS}"

  if [ -z "$SYSPLORER_PLATFORM_LABEL_INPUT" ]; then
    read -r -p "Enter Sysplorer platform label (default: $DEFAULT_LABEL): " SYSPLORER_PLATFORM_LABEL_INPUT
  fi
  platform_label="${SYSPLORER_PLATFORM_LABEL_INPUT:-$DEFAULT_LABEL}"

  if [ ! -e "$launcher_path" ]; then
    printf 'Launcher not found: %s\n' "$launcher_path" >&2
    exit 1
  fi

  if ! command -v python3 >/dev/null 2>&1; then
    printf 'Error: python3 is required to merge JSON/TOML client configs.\n' >&2
    exit 1
  fi

  printf 'Backing up existing configuration files (if any)...\n'
  backup_if_exists "$HOME/.claude.json"
  backup_if_exists "$HOME/.config/opencode/opencode.json"
  backup_if_exists "$HOME/.codex/config.toml"
  printf '\n'

  write_all_client_configs "binary" "$mworks_dir" "$platform_label" "$launcher_path"
  printf 'Claude configuration updated: %s\n' "$HOME/.claude.json"
  printf 'OpenCode configuration updated: %s\n' "$HOME/.config/opencode/opencode.json"
  printf 'Codex configuration updated: %s\n' "$HOME/.codex/config.toml"
fi

printf '\nConfiguration completed. Restart Claude Code / OpenCode / Codex CLI to load MCP.\n'
printf 'To uninstall, remove sysplorer_mcp from the corresponding config files.\n'
