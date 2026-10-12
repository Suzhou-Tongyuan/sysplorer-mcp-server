#!/usr/bin/env bash
# 与 install/build_publish.ps1 对齐：填充 publish/sysplorer_mcp（launcher、服务端、resources、
# MCP_BUILD_INFO.json、README.md（来自 install/linux/README.md）、install_mcp.sh），再打成
# publish/sysplorer_mcp_v{version}.zip。不包含 Windows exe / PyInstaller。
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
REPO_ROOT="$(cd -- "$INSTALL_DIR/.." && pwd)"
META_MODE="release"
RAG_HUGE="modelica_doc_index.json"

usage() {
  printf 'Usage: %s [--internal] [REPO_ROOT]\n' "$(basename "$0")" >&2
  printf '  --internal   internal version (version_base.<git commit count>)\n' >&2
  printf '  default      release (version_base only), same as build_publish.ps1\n' >&2
  exit 1
}

while [ $# -gt 0 ]; do
  case "$1" in
    --internal)
      META_MODE="internal"
      shift
      ;;
    -h|--help)
      usage
      ;;
    -*)
      printf 'Unknown option: %s\n' "$1" >&2
      usage
      ;;
    *)
      if [ -n "${REPO_ROOT_ARG_SET:-}" ]; then
        usage
      fi
      REPO_ROOT="$(cd -- "$1" && pwd)"
      REPO_ROOT_ARG_SET=1
      shift
      ;;
  esac
done

if [ -z "${REPO_ROOT_ARG_SET:-}" ]; then
  REPO_ROOT="$(cd -- "$INSTALL_DIR/.." && pwd)"
fi

PUBLISH_ROOT="$REPO_ROOT/publish/sysplorer_mcp"
LAUNCHER_SRC="$INSTALL_DIR/publish_assets/sysplorer_mcp_main.py"
SERVER_SRC="$REPO_ROOT/sysplorer-mcp-server"
RES_SRC="$REPO_ROOT/resources"
INSTALL_SCRIPT_SRC="$SCRIPT_DIR/install_mcp.sh"
README_SRC="$INSTALL_DIR/linux/README.md"
WRITE_META="$INSTALL_DIR/write_build_meta.py"
PKG_VER_JSON="$INSTALL_DIR/package_version.json"

if [ ! -f "$LAUNCHER_SRC" ]; then
  printf 'Missing launcher source: %s\n' "$LAUNCHER_SRC" >&2
  exit 1
fi
if [ ! -d "$SERVER_SRC" ]; then
  printf 'Missing sysplorer-mcp-server: %s\n' "$SERVER_SRC" >&2
  exit 1
fi
if [ ! -d "$RES_SRC" ]; then
  printf 'Missing resources: %s\n' "$RES_SRC" >&2
  exit 1
fi
if [ ! -f "$INSTALL_SCRIPT_SRC" ]; then
  printf 'Missing install script: %s\n' "$INSTALL_SCRIPT_SRC" >&2
  exit 1
fi
if [ ! -f "$README_SRC" ]; then
  printf 'Missing install/linux/README.md: %s\n' "$README_SRC" >&2
  exit 1
fi
if [ ! -f "$WRITE_META" ]; then
  printf 'Missing write_build_meta.py: %s\n' "$WRITE_META" >&2
  exit 1
fi
if [ ! -f "$PKG_VER_JSON" ]; then
  printf 'Missing package_version.json: %s\n' "$PKG_VER_JSON" >&2
  exit 1
fi

if command -v python3 >/dev/null 2>&1; then
  PYTHON=python3
elif command -v python >/dev/null 2>&1; then
  PYTHON=python
else
  printf 'write_build_meta.py requires python3 or python on PATH\n' >&2
  exit 1
fi

printf 'Repo:    %s\n' "$REPO_ROOT"
printf 'Publish: %s\n' "$PUBLISH_ROOT"
printf 'Mode:    %s\n' "$META_MODE"

rm -rf "$PUBLISH_ROOT"
mkdir -p "$PUBLISH_ROOT"
cp -f "$LAUNCHER_SRC" "$PUBLISH_ROOT/main.py"

SERVER_DST="$PUBLISH_ROOT/sysplorer-mcp-server"
rm -rf "$SERVER_DST"
mkdir -p "$SERVER_DST"

while IFS= read -r -d '' f; do
  rel="${f#"$SERVER_SRC"/}"
  parent="$SERVER_DST/$(dirname "$rel")"
  mkdir -p "$parent"
  cp -a "$f" "$SERVER_DST/$rel"
done < <(
  find "$SERVER_SRC" -type f \
    ! -path '*/__pycache__/*' \
    ! -path '*/tests/*' \
    ! -path '*/.pytest_cache/*' \
    ! -name '*.pyc' \
    ! -name "$RAG_HUGE" \
    -print0
)

RES_DST="$PUBLISH_ROOT/resources"
rm -rf "$RES_DST"
cp -a "$RES_SRC" "$RES_DST"
find "$RES_DST" -type f -name "$RAG_HUGE" -delete 2>/dev/null || true

n_res_src="$(find "$RES_SRC" -type f ! -name "$RAG_HUGE" | wc -l | tr -d ' ')"
n_res_dst="$(find "$RES_DST" -type f ! -name "$RAG_HUGE" | wc -l | tr -d ' ')"
if [ "$n_res_src" != "$n_res_dst" ]; then
  printf 'resources file count mismatch: src=%s dst=%s\n' "$n_res_src" "$n_res_dst" >&2
  exit 1
fi

cp -f "$INSTALL_SCRIPT_SRC" "$PUBLISH_ROOT/install_mcp.sh"
chmod +x "$PUBLISH_ROOT/install_mcp.sh"
INSTALL_MCP_SILENT_SRC="$INSTALL_DIR/install_mcp_silent.py"
if [ ! -f "$INSTALL_MCP_SILENT_SRC" ]; then
  printf 'Missing install_mcp_silent.py: %s\n' "$INSTALL_MCP_SILENT_SRC" >&2
  exit 1
fi
cp -f "$INSTALL_MCP_SILENT_SRC" "$PUBLISH_ROOT/install_mcp_silent.py"

META_DST="$SERVER_DST/_build_meta.py"
BUILD_INFO_PATH="$PUBLISH_ROOT/MCP_BUILD_INFO.json"
BUILD_INFO_JSON="$(
  "$PYTHON" "$WRITE_META" \
    --repo-root "$REPO_ROOT" \
    --mode "$META_MODE" \
    --output "$META_DST" \
    --print-json
)"
export MCP_BUILD_INFO_JSON_PATH="$BUILD_INFO_PATH"
export MCP_BUILD_INFO_JSON="$BUILD_INFO_JSON"
ver_line="$(
  "$PYTHON" - <<'PY'
import json
import os

path = os.environ["MCP_BUILD_INFO_JSON_PATH"]
d = json.loads(os.environ["MCP_BUILD_INFO_JSON"])
out = {
    "version": str(d.get("version", "")),
    "version_display": str(d.get("version_display", d.get("version", ""))),
    "version_base": str(d.get("version_base", "")),
    "version_core": str(d.get("version_core", "")),
    "build_counter": int(d.get("build_counter", 0)),
    "git_commit_count": int(d.get("git_commit_count", 0)),
    "build_kind": str(d.get("build_kind", "")),
    "build_time": str(d.get("build_time", "")),
    "git_revision": str(d.get("git_revision", "")),
}
pathlib_path = __import__("pathlib").Path(path)
pathlib_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(out.get("version", ""))
PY
)"
printf 'Version: %s\n' "$ver_line"
printf 'Wrote %s\n' "$BUILD_INFO_PATH"
unset MCP_BUILD_INFO_JSON_PATH
unset MCP_BUILD_INFO_JSON

for legacy in "$PUBLISH_ROOT/README.txt" "$PUBLISH_ROOT/Readme.md" "$PUBLISH_ROOT/INSTALL_MANUAL.md" "$PUBLISH_ROOT/安装部署手册.md"; do
  if [ -e "$legacy" ]; then
    rm -f "$legacy"
  fi
done
cp -f "$README_SRC" "$PUBLISH_ROOT/README.md"
printf 'Wrote README: %s/README.md\n' "$PUBLISH_ROOT"

PUBLISH_PARENT="$REPO_ROOT/publish"
ARCHIVE_FINAL="$PUBLISH_PARENT/sysplorer_mcp_v${ver_line}.zip"
for old_zip in "$PUBLISH_PARENT"/sysplorer_mcp_v*.zip; do
  if [ -f "$old_zip" ]; then
    printf 'Removing old publish archive: %s\n' "$(basename "$old_zip")"
    rm -f "$old_zip"
  fi
done

TMP_ARCHIVE="$(mktemp "${TMPDIR:-/tmp}/sysplorer_mcp_publish.XXXXXX")"
cleanup_tmp_archive() {
  rm -f "$TMP_ARCHIVE"
}
trap cleanup_tmp_archive EXIT

printf 'Creating zip: %s\n' "$ARCHIVE_FINAL"
export MCP_PUBLISH_ROOT="$PUBLISH_ROOT"
export MCP_TMP_ARCHIVE="$TMP_ARCHIVE"
"$PYTHON" - <<'PY'
import os
import zipfile
from pathlib import Path

src = Path(os.environ["MCP_PUBLISH_ROOT"])
tmp = Path(os.environ["MCP_TMP_ARCHIVE"])
parent = src.parent
with zipfile.ZipFile(tmp, "w", compression=zipfile.ZIP_DEFLATED) as zf:
    for path in sorted(src.rglob("*")):
        if path.is_file():
            zf.write(path, path.relative_to(parent).as_posix())
PY
mv -f "$TMP_ARCHIVE" "$ARCHIVE_FINAL"
trap - EXIT
unset MCP_PUBLISH_ROOT MCP_TMP_ARCHIVE
printf 'Archive: %s\n' "$ARCHIVE_FINAL"
printf 'Done. Output: %s\n' "$PUBLISH_ROOT"
