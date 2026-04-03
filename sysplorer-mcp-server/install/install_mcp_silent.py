import json
import os
import shutil
import sys
from datetime import datetime


def backup_config_file_if_exists(path):
    if not os.path.exists(path):
        return
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S%f")
    backup_path = f"{path}.bak.{stamp}"
    shutil.copy2(path, backup_path)
    print(f"[OK] backed up: {path} -> {backup_path}")


def remove_mcp_servers_toml_block(text, server_key):
    header = f"[mcp_servers.{server_key}]"
    lines = text.splitlines()
    out = []
    i = 0
    while i < len(lines):
        if lines[i].strip() == header:
            i += 1
            while i < len(lines) and not lines[i].lstrip().startswith("["):
                i += 1
            continue
        out.append(lines[i])
        i += 1
    return "\n".join(out)


def write_codex_sysplorer_mcp_toml(config_path, command, mcp_args):
    config_dir = os.path.dirname(config_path)
    if config_dir and not os.path.exists(config_dir):
        os.makedirs(config_dir, exist_ok=True)

    body = ""
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            body = f.read()

    body = remove_mcp_servers_toml_block(body, "sysplorer_mcp")
    body = remove_mcp_servers_toml_block(body, "mworks_mcp")

    lines = [
        "[mcp_servers.sysplorer_mcp]",
        f"command = {json.dumps(command, ensure_ascii=False)}",
        "args = [",
    ]
    for arg in mcp_args:
        lines.append(f"    {json.dumps(arg, ensure_ascii=False)},")
    lines.append("]")

    block = "\n".join(lines)
    body = body.rstrip()
    body = f"{body}\n\n{block}\n" if body else f"{block}\n"

    with open(config_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(body)


def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        content = f.read().strip()
    return json.loads(content) if content else {}


def get_bundle_root():
    return os.path.dirname(os.path.abspath(__file__))


def ensure_bundle(bundle_root):
    main_py = os.path.join(bundle_root, "main.py")
    pkg_dir = os.path.join(bundle_root, "sysplorer-mcp-server")
    res_dir = os.path.join(bundle_root, "resources")
    missing = [path for path in (main_py, pkg_dir, res_dir) if not os.path.exists(path)]
    if missing:
        raise RuntimeError("Missing required bundle files:\n" + "\n".join(missing))
    return os.path.abspath(main_py)


def get_sysplorer_python_path(mworks_install_dir):
    if os.name == "nt":
        return os.path.join(mworks_install_dir, "External", "python64", "python.exe")
    return os.path.join(mworks_install_dir, "external", "python64", "bin", "python3")


def install_mcp(mworks_install_dir, platform_label):
    main_py = os.path.join(mworks_install_dir, "Tools", "sysplorer_mcp_server", "main.py")
    if not os.path.exists(main_py):
        raise RuntimeError(f"Sysplorer MCP main.py not found: {main_py}")

    python_exe = get_sysplorer_python_path(mworks_install_dir)
    if not os.path.exists(python_exe):
        raise RuntimeError(f"Sysplorer bundled Python not found: {python_exe}")

    home_dir = os.path.expanduser("~")
    claude_config_path = os.path.join(home_dir, ".claude.json")
    opencode_config_path = os.path.join(home_dir, ".config", "opencode", "opencode.json")
    codex_config_path = os.path.join(home_dir, ".codex", "config.toml")

    os.makedirs(os.path.dirname(opencode_config_path), exist_ok=True)

    for path in (claude_config_path, opencode_config_path, codex_config_path):
        backup_config_file_if_exists(path)

    claude_config = load_json(claude_config_path)
    mcp_servers = claude_config.setdefault("mcpServers", {})
    mcp_servers.pop("mworks_mcp", None)
    mcp_servers["sysplorer_mcp"] = {
        "command": python_exe,
        "args": [
            main_py,
            "--mworks-install-dir",
            mworks_install_dir,
            "--sysplorer-platform-label",
            platform_label,
        ],
    }
    with open(claude_config_path, "w", encoding="utf-8") as f:
        json.dump(claude_config, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"[OK] Claude configuration updated: {claude_config_path}")

    opencode_config = load_json(opencode_config_path)
    mcp = opencode_config.setdefault("mcp", {})
    mcp.pop("mworks_mcp", None)
    mcp["sysplorer_mcp"] = {
        "type": "local",
        "command": [
            python_exe,
            main_py,
            "--mworks-install-dir",
            mworks_install_dir,
            "--sysplorer-platform-label",
            platform_label,
        ],
    }
    with open(opencode_config_path, "w", encoding="utf-8") as f:
        json.dump(opencode_config, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"[OK] OpenCode configuration updated: {opencode_config_path}")

    write_codex_sysplorer_mcp_toml(
        codex_config_path,
        python_exe,
        [
            main_py,
            "--mworks-install-dir",
            mworks_install_dir,
            "--sysplorer-platform-label",
            platform_label,
        ],
    )
    print(f"[OK] Codex configuration updated: {codex_config_path}")


def main(*args):
    # Accept install path and optional platform label.
    if len(args) < 2 or len(args) > 3:
        print("Usage: python install_mcp_silent.py <mworks_install_dir> [platform_label]")
        return 1

    mworks_install_dir = args[1]
    platform_label = args[2] if len(args) == 3 else "Sysplorer 2026a"
    install_mcp(mworks_install_dir, platform_label)
    print("[OK] silent MCP installation completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(*sys.argv))
