#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/../../.." && pwd)"
OUTPUT_DIR="${1:-$REPO_ROOT/install/dist/linux-x64}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
DIST_ROOT="$REPO_ROOT/install/dist"
DIST_DIR="$OUTPUT_DIR"
SPEC_PATH="$REPO_ROOT/install/linux/pyinstaller/sysplorer_mcp_server.spec"
WORK_PATH="$REPO_ROOT/install/build-linux"
EXE_SOURCE="$DIST_ROOT/sysplorer_mcp_server"
LEGACY_EXE_SOURCE="$DIST_ROOT/mworks_mcp_server"
RESOURCES_SOURCE="$REPO_ROOT/resources"
ARCHIVE_NAME="linux-x64.tar.gz"
ARCHIVE_PATH="$DIST_ROOT/$ARCHIVE_NAME"

printf '== Building Linux MCP distribution ==\n'
printf 'Repo root: %s\n' "$REPO_ROOT"
printf 'Spec path: %s\n' "$SPEC_PATH"
printf 'Output dir: %s\n' "$DIST_DIR"

if [ -e "$DIST_DIR" ] && [ ! -d "$DIST_DIR" ]; then
  printf 'Output path exists but is not a directory: %s\n' "$DIST_DIR" >&2
  exit 1
fi

mkdir -p "$DIST_DIR"
find "$DIST_DIR" -mindepth 1 -exec rm -rf -- {} +
rm -rf "$WORK_PATH/sysplorer_mcp_server" "$WORK_PATH/mworks_mcp_server"
rm -f "$EXE_SOURCE" "$LEGACY_EXE_SOURCE"

# 与 Windows build.ps1 一致：version_base 来自 install/package_version.json，内部版为 0.6.x（x = git 提交数）
"$PYTHON_BIN" "$REPO_ROOT/install/write_build_meta.py" --repo-root "$REPO_ROOT" --mode internal

"$PYTHON_BIN" -m PyInstaller --noconfirm --clean --distpath "$DIST_ROOT" --workpath "$WORK_PATH" "$SPEC_PATH"

if [ ! -f "$EXE_SOURCE" ]; then
  printf 'Expected executable not found: %s\n' "$EXE_SOURCE" >&2
  exit 1
fi

cp "$EXE_SOURCE" "$DIST_DIR/sysplorer_mcp_server"
cp -R "$RESOURCES_SOURCE" "$DIST_DIR/resources"
# 默认不打包超大 BM25 索引（与 Windows build.ps1 / PyInstaller spec 一致）
find "$DIST_DIR/resources" -type f -name 'modelica_doc_index.json' -delete 2>/dev/null || true
cp "$REPO_ROOT/sysplorer-mcp-server/requirements.txt" "$DIST_DIR/requirements.txt"
README_PUBLISH_SRC="$REPO_ROOT/install/linux/README.md"
if [ ! -f "$README_PUBLISH_SRC" ]; then
  printf 'Missing install/linux/README.md: %s\n' "$README_PUBLISH_SRC" >&2
  exit 1
fi
cp "$README_PUBLISH_SRC" "$DIST_DIR/README.md"
cp "$REPO_ROOT/install/common/templates/.mcp.json.example" "$DIST_DIR/.mcp.json.example"
cp "$REPO_ROOT/install/common/templates/claude.desktop.json.example" "$DIST_DIR/claude.desktop.json.example"
cp "$REPO_ROOT/install/common/templates/opencode.json.example" "$DIST_DIR/opencode.json.example"
cp "$REPO_ROOT/install/linux/scripts/install_mcp.sh" "$DIST_DIR/install_mcp.sh"

generated_at="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
cat > "$DIST_DIR/manifest.json" <<EOF
{
  "platform": "linux-x64",
  "support": "limited-native-binary",
  "executable": "sysplorer_mcp_server",
  "installScripts": [
    "install_mcp.sh"
  ],
  "generatedAt": "$generated_at"
}
EOF

chmod +x "$DIST_DIR/sysplorer_mcp_server" "$DIST_DIR/install_mcp.sh"

"$PYTHON_BIN" "$REPO_ROOT/install/write_build_meta.py" --repo-root "$REPO_ROOT" --dump-mcp-json "$DIST_DIR/MCP_BUILD_INFO.json"

rm -f "$ARCHIVE_PATH"
tar -czf "$ARCHIVE_PATH" -C "$DIST_DIR" .

printf 'Linux distribution ready: %s\n' "$DIST_DIR"
printf 'Linux archive ready: %s\n' "$ARCHIVE_PATH"
