# 本文件须保持 Python 3.7 语法兼容，勿使用 3.8 及以上版本特性。
"""Configure Sysplorer MCP for Claude / OpenCode / Codex (target: Python 3.7+).

Avoids PEP 585 (``list[str]``) and PEP 604 (``X | None``). ``tomllib`` is optional
(stdlib 3.11+); without it, TOML write validation is skipped.
"""
import argparse
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, List, Optional

try:
    import tomllib
except ImportError:
    tomllib = None

MCP_CLIENT_KEY = "sysplorer"
LEGACY_MCP_CLIENT_KEYS = ("sysplorer_mcp", "mworks_mcp")


def _pop_legacy_mcp_keys(container):
    for key in LEGACY_MCP_CLIENT_KEYS:
        container.pop(key, None)


def make_timestamped_path(path, suffix):
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S%f")
    if suffix == "bak":
        return f"{path}.bak.{stamp}"
    return f"{path}.{suffix}.{stamp}"


def log_ok(message):
    print(f"[OK] {message}")


def log_warn(message):
    print(f"[WARN] {message}")


def backup_file_if_exists(path, suffix="bak"):
    if not os.path.exists(path):
        return None
    backup_path = make_timestamped_path(path, suffix)
    try:
        shutil.copy2(path, backup_path)
    except OSError as exc:
        log_warn(f"failed to back up {path}: {exc}")
        return None
    log_ok(f"backed up: {path} -> {backup_path}")
    return backup_path


def backup_invalid_file(path, reason, suffix):
    backup_path = backup_file_if_exists(path, suffix=suffix)
    kind = suffix.replace("invalid-", "").replace("-", " ")
    log_warn(f"invalid {kind} in {path}: {reason}")
    if backup_path:
        log_warn(f"using empty config; invalid file copy: {backup_path}")
    else:
        log_warn("using empty config without backup because backup failed")
    return backup_path


def read_bytes_file(path):
    with open(path, "rb") as f:
        return f.read()


def decode_text_candidates(raw):
    if not raw:
        return []

    bom_candidates = (
        ("utf-8-sig", b"\xef\xbb\xbf"),
        ("utf-32", b"\xff\xfe\x00\x00"),
        ("utf-32", b"\x00\x00\xfe\xff"),
        ("utf-16", b"\xff\xfe"),
        ("utf-16", b"\xfe\xff"),
    )
    decoded = []
    seen = set()
    for encoding, bom in bom_candidates:
        if raw.startswith(bom):
            try:
                text = raw.decode(encoding)
                if "\x00" not in text:
                    key = (encoding, text)
                    if key not in seen:
                        seen.add(key)
                        decoded.append(key)
            except UnicodeError:
                break

    encodings = (
        "utf-8",
        "utf-8-sig",
        "utf-16-le",
        "utf-16-be",
        "utf-16",
        "utf-32-le",
        "utf-32-be",
        "utf-32",
        "gb18030",
        "gbk",
        "cp936",
        "big5",
    )
    last_error = None
    for encoding in encodings:
        try:
            text = raw.decode(encoding)
            if "\x00" in text:
                continue
            key = (encoding, text)
            if key not in seen:
                seen.add(key)
                decoded.append(key)
        except UnicodeError as exc:
            last_error = exc
    if decoded:
        return decoded
    raise RuntimeError(f"unable to decode text bytes: {last_error}")


def write_text_atomic(path, text, encoding="utf-8", newline=None):
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    temp_path = make_timestamped_path(path, "tmp")
    try:
        with open(temp_path, "w", encoding=encoding, newline=newline) as f:
            f.write(text)
        os.replace(temp_path, path)
    finally:
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except OSError:
                pass


def write_json_atomic(path, data):
    text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    write_text_atomic(path, text, encoding="utf-8", newline="\n")


def is_table_header(line):
    stripped = line.strip()
    return stripped.startswith("[") and stripped.endswith("]")


def get_table_name(line):
    stripped = line.strip()
    if not is_table_header(stripped):
        return None
    return stripped.strip("[]").strip()


def is_target_mcp_table(line, server_key):
    name = get_table_name(line)
    if not name:
        return False
    prefix = f"mcp_servers.{server_key}"
    return name == prefix or name.startswith(prefix + ".")


def remove_mcp_servers_toml_block(text, server_key):
    lines = text.splitlines()
    out = []
    skipping = False
    for line in lines:
        if is_table_header(line):
            if is_target_mcp_table(line, server_key):
                skipping = True
                continue
            if skipping:
                skipping = False
        if not skipping:
            out.append(line)
    return "\n".join(out)


def strip_known_mcp_server_toml_blocks(text):
    """Remove current and legacy MCP server table blocks before rewriting Codex config."""
    for key in (MCP_CLIENT_KEY, *LEGACY_MCP_CLIENT_KEYS):
        text = remove_mcp_servers_toml_block(text, key)
    return text


def load_json(path):
    if not os.path.exists(path):
        return {}
    raw = read_bytes_file(path)
    if not raw:
        return {}
    try:
        decoded_candidates = decode_text_candidates(raw)
    except Exception as exc:
        raise RuntimeError(f"Invalid JSON in {path}: {exc}")
    last_json_error = None
    for _, decoded_text in decoded_candidates:
        content = decoded_text.strip()
        if not content:
            return {}
        try:
            data = json.loads(content)
        except json.JSONDecodeError as exc:
            last_json_error = exc
            continue
        if not isinstance(data, dict):
            raise RuntimeError(
                f"Invalid JSON in {path}: top-level JSON value must be an object, got {type(data).__name__}"
            )
        return data
    raise RuntimeError(f"Invalid JSON in {path}: {last_json_error or 'unable to parse JSON with supported encodings'}")


def load_toml_text(path):
    if not os.path.exists(path):
        return ""
    raw = read_bytes_file(path)
    if not raw:
        return ""
    decoded_candidates = decode_text_candidates(raw)
    if not decoded_candidates:
        return ""
    if tomllib is None:
        return decoded_candidates[0][1]
    last_toml_error = None
    for _, content in decoded_candidates:
        if not content.strip():
            return ""
        try:
            tomllib.loads(content)
            return content
        except Exception as exc:
            last_toml_error = exc
            continue
    backup_invalid_file(path, last_toml_error or "unable to parse TOML with supported encodings", "invalid-toml")
    return ""


def ensure_dict_field(container, key, owner_path):
    value = container.get(key)
    if value is None:
        container[key] = {}
        return container[key]
    if isinstance(value, dict):
        return value
    log_warn(f"{owner_path}: field {key!r} is {type(value).__name__}; replacing it with an object")
    container[key] = {}
    return container[key]


def write_codex_sysplorer_toml(config_path, command, mcp_args):
    body = load_toml_text(config_path)
    body = strip_known_mcp_server_toml_blocks(body)

    lines = [
        f"[mcp_servers.{MCP_CLIENT_KEY}]",
        f"command = {json.dumps(command, ensure_ascii=False)}",
        "args = [",
    ]
    for arg in mcp_args:
        lines.append(f"    {json.dumps(arg, ensure_ascii=False)},")
    lines.append("]")

    block = "\n".join(lines)
    body = body.rstrip()
    body = f"{body}\n\n{block}\n" if body else f"{block}\n"

    if tomllib is not None:
        tomllib.loads(body)
    backup_file_if_exists(config_path)
    write_text_atomic(config_path, body, encoding="utf-8", newline="\n")


def get_bundle_root():
    return os.path.dirname(os.path.abspath(__file__))


def get_home_dir():
    candidates = [
        os.environ.get("HOME"),
        os.environ.get("USERPROFILE"),
        os.path.expanduser("~"),
    ]
    for candidate in candidates:
        if candidate and candidate.strip() and candidate.strip() != "~":
            return os.path.abspath(os.path.expandvars(candidate))
    raise RuntimeError("Unable to resolve user home directory")


def mogick_config_path(home_dir):
    return os.path.join(home_dir, ".mworks", "mogick", "Sysplorer", "mcp.json")


def normalize_install_dir(mworks_install_dir):
    if mworks_install_dir is None:
        raise RuntimeError("MWorks install directory is required")
    text = str(mworks_install_dir).strip().strip('"')
    if not text:
        raise RuntimeError("MWorks install directory is empty")
    path = os.path.abspath(os.path.expandvars(os.path.expanduser(text)))
    if not os.path.isdir(path):
        raise RuntimeError(f"MWorks install directory not found: {path}")
    return path


def resolve_platform_label(platform_label):
    text = "" if platform_label is None else str(platform_label).strip()
    return text or "Sysplorer 2026b"


def get_sysplorer_python_path(mworks_install_dir):
    if os.name == "nt":
        candidates = [
            os.path.join(mworks_install_dir, "External", "python64", "python.exe"),
            os.path.join(mworks_install_dir, "external", "python64", "python.exe"),
        ]
    else:
        candidates = [
            os.path.join(mworks_install_dir, "external", "python64", "bin", "python3"),
            os.path.join(mworks_install_dir, "External", "python64", "bin", "python3"),
        ]
    for candidate in candidates:
        if os.path.exists(candidate):
            return os.path.abspath(candidate)
    raise RuntimeError("Sysplorer bundled Python not found:\n" + "\n".join(candidates))


def resolve_main_py(mworks_install_dir):
    candidates = [
        os.path.join(mworks_install_dir, "Tools", "sysplorer_mcp_server", "main.py"),
        os.path.join(mworks_install_dir, "Tools", "sysplorer_mcp", "main.py"),
    ]
    bundle_root = get_bundle_root()
    bundle_main = os.path.join(bundle_root, "main.py")
    if os.path.exists(bundle_main):
        try:
            if os.path.commonpath([os.path.abspath(bundle_root), os.path.abspath(mworks_install_dir)]) == os.path.abspath(mworks_install_dir):
                candidates.append(bundle_main)
        except ValueError:
            pass
    for candidate in candidates:
        if os.path.exists(candidate):
            return os.path.abspath(candidate)
    raise RuntimeError("Sysplorer MCP main.py not found:\n" + "\n".join(candidates))


def build_server_args(main_py, mworks_install_dir, platform_label):
    return [
        main_py,
        "--mworks-install-dir",
        mworks_install_dir,
        "--sysplorer-platform-label",
        platform_label,
    ]


def _build_local_mcp_command_block(python_exe, args, mworks_install_dir, *, include_enabled=False):
    block = {
        "type": "local",
        "command": [python_exe] + list(args),
        "timeout": 1000000,
    }
    if include_enabled:
        block["enabled"] = True
    if sys.platform.startswith("linux"):
        block["environment"] = {
            "LD_LIBRARY_PATH": os.path.join(mworks_install_dir, "bin64") + ":$LD_LIBRARY_PATH",
        }
    return block


def update_claude_config(config_path, data, python_exe, args):
    mcp_servers = ensure_dict_field(data, "mcpServers", config_path)
    _pop_legacy_mcp_keys(mcp_servers)
    mcp_servers[MCP_CLIENT_KEY] = {
        "command": python_exe,
        "args": args,
    }
    backup_file_if_exists(config_path)
    write_json_atomic(config_path, data)
    log_ok(f"Claude configuration updated: {config_path}")


def update_opencode_config(config_path, data, python_exe, args, mworks_install_dir):
    mcp = ensure_dict_field(data, "mcp", config_path)
    _pop_legacy_mcp_keys(mcp)
    mcp[MCP_CLIENT_KEY] = _build_local_mcp_command_block(
        python_exe, args, mworks_install_dir, include_enabled=False
    )
    backup_file_if_exists(config_path)
    write_json_atomic(config_path, data)
    log_ok(f"OpenCode configuration updated: {config_path}")


def update_mogick_config(config_path, data, python_exe, args, mworks_install_dir):
    servers = ensure_dict_field(data, "servers", config_path)
    _pop_legacy_mcp_keys(servers)
    servers[MCP_CLIENT_KEY] = _build_local_mcp_command_block(
        python_exe, args, mworks_install_dir, include_enabled=True
    )
    backup_file_if_exists(config_path)
    write_json_atomic(config_path, data)
    log_ok(f"Mogick configuration updated: {config_path}")


def update_codex_config(config_path, python_exe, args):
    write_codex_sysplorer_toml(config_path, python_exe, args)
    log_ok(f"Codex configuration updated: {config_path}")


# --- Agent skills sync (bundled modeling_skills → OpenCode / Mogick global skills dirs) ---

LogFn = Callable[[str], None]


def _sync_skills_log_default(msg: str) -> None:
    print(msg, flush=True)


def opencode_skills_resolve_bundle_root(start: Optional[Path] = None) -> Path:
    """Directory that contains ``resources/modeling_skills`` (repo root, publish bundle, …)."""
    here = Path(start).resolve() if start is not None else Path(__file__).resolve().parent
    for p in [here, *here.parents]:
        marker = p / "resources" / "modeling_skills"
        if marker.is_dir():
            return p.resolve()
    return here.resolve()


def opencode_skills_default_source(bundle_root: Optional[Path] = None) -> Path:
    root = bundle_root or opencode_skills_resolve_bundle_root()
    return (root / "resources" / "modeling_skills").resolve()


def opencode_skills_default_dest_root() -> Path:
    return (Path.home() / ".config" / "opencode" / "skills").resolve()


def mogick_skills_default_dest_root() -> Path:
    return (Path.home() / ".mworks" / "mogick" / "Sysplorer" / "skills").resolve()


def agent_skills_default_dest_roots() -> List[tuple]:
    return [
        ("OpenCode", opencode_skills_default_dest_root()),
        ("Mogick", mogick_skills_default_dest_root()),
    ]


# Bundled skills renamed or removed: still rmtree under dest on sync so old copies do not linger
# (new installs only have current `resources/modeling_skills/<name>/`).
OPENCODE_SKILLS_RETIRED_DIR_NAMES: tuple = (
    "ty-sysplorer-modeling-router",  # renamed to ty-sysplorer-modeling-rules
)
# modelica-lite exe pack does not ship these Sysplorer-only skills; clear leftovers on sync.
MODELICA_LITE_RETIRED_SKILL_DIR_NAMES: tuple = (
    "ty-cadtool-modeling",
    "sysplorer-mds-docs",
)


def _read_mcp_build_info(bundle_root: Optional[Path]) -> dict:
    if bundle_root is None:
        return {}
    info = bundle_root / "MCP_BUILD_INFO.json"
    if not info.is_file():
        return {}
    try:
        data = json.loads(info.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def _read_mcp_build_version(bundle_root: Optional[Path]) -> str:
    data = _read_mcp_build_info(bundle_root)
    return str(data.get("version_display") or data.get("version") or "unknown")


def retired_skill_dir_names(bundle_root: Optional[Path] = None) -> tuple:
    names = list(OPENCODE_SKILLS_RETIRED_DIR_NAMES)
    variant = str(_read_mcp_build_info(bundle_root).get("pack_variant") or "").strip().lower().replace("-", "_")
    if variant in ("modelica_lite", "mols"):
        names.extend(MODELICA_LITE_RETIRED_SKILL_DIR_NAMES)
    return tuple(names)


def list_managed_skill_names(source_dir: Path) -> List[str]:
    """Names of immediate subdirectories that contain ``SKILL.md`` (bundle whitelist)."""
    if not source_dir.is_dir():
        return []
    names: List[str] = []
    for child in sorted(source_dir.iterdir()):
        if not child.is_dir():
            continue
        if not (child / "SKILL.md").is_file():
            continue
        name = child.name
        if name in (".", "..") or os.sep in name or "/" in name or "\\" in name:
            continue
        names.append(name)
    return names


def _opencode_skills_is_strict_child(path: Path, parent: Path) -> bool:
    try:
        path_res = path.resolve()
        parent_res = parent.resolve()
    except OSError:
        return False
    try:
        path_res.relative_to(parent_res)
    except ValueError:
        return False
    return path_res != parent_res


def _opencode_skills_safe_rmtree_skill_dir(target: Path, skills_root: Path, log: LogFn) -> bool:
    if not target.exists():
        return True
    if not _opencode_skills_is_strict_child(target, skills_root):
        log(f"[WARN] refuse to remove path outside skills root: {target}")
        return False
    if not target.is_dir():
        log(f"[WARN] skip non-directory: {target}")
        return False
    shutil.rmtree(target)
    return True


def sync_opencode_skills(
    *,
    bundle_root: Optional[Path] = None,
    source_dir: Optional[Path] = None,
    dest_root: Optional[Path] = None,
    dest_label: str = "OpenCode",
    log: LogFn = _sync_skills_log_default,
    write_sidecar: bool = True,
) -> dict:
    """Per skill name: remove ``dest_root/<name>`` if present, then copy from source.

    Only immediate subdirectories of ``source_dir`` that contain ``SKILL.md`` are synced.
    The entire ``dest_root`` is never removed—only matching child directories.
    If ``source_dir`` is missing or not a directory, returns ok with ``skipped`` (no error).
    **Retired** directory names (see ``retired_skill_dir_names``) are removed from
    ``dest_root`` when present, so renames in the bundle do not leave stale skill trees.
    """
    bundle = (bundle_root or opencode_skills_resolve_bundle_root()).resolve()
    src = (source_dir or opencode_skills_default_source(bundle)).resolve()
    dst_parent = (dest_root or opencode_skills_default_dest_root()).resolve()
    label = dest_label or "OpenCode"
    result: dict = {
        "ok": True,
        "skipped": False,
        "skip_reason": None,
        "bundle_root": str(bundle),
        "source": str(src),
        "dest_root": str(dst_parent),
        "dest_label": label,
        "managed": [],
        "removed": [],
        "copied": [],
        "skipped_remove": [],
        "errors": [],
        "legacy_removed": [],
    }

    if not src.exists():
        result["skipped"] = True
        result["skip_reason"] = "source_missing"
        log(f"[OK] {label} skills sync skipped (source not found): {src}")
        return result

    if not src.is_dir():
        result["skipped"] = True
        result["skip_reason"] = "source_not_directory"
        log(f"[OK] {label} skills sync skipped (source is not a directory): {src}")
        return result

    managed = list_managed_skill_names(src)
    result["managed"] = list(managed)
    if not managed:
        result["skipped"] = True
        result["skip_reason"] = "no_managed_skills"
        log(f"[OK] {label} skills sync skipped (no SKILL.md subdirs under): {src}")
        return result

    dst_parent.mkdir(parents=True, exist_ok=True)
    try:
        dst_parent_res = dst_parent.resolve()
    except OSError as exc:
        result["ok"] = False
        result["errors"].append(f"bad dest_root: {exc}")
        return result

    for legacy in retired_skill_dir_names(bundle):
        if legacy in managed:
            continue
        leg_target = (dst_parent / legacy).resolve()
        if not leg_target.exists():
            continue
        if not _opencode_skills_is_strict_child(leg_target, dst_parent_res):
            msg = f"refuse remove retired (path escape): {leg_target}"
            result["errors"].append(msg)
            result["skipped_remove"].append(str(leg_target))
            log(f"[WARN] {msg}")
            continue
        if _opencode_skills_safe_rmtree_skill_dir(leg_target, dst_parent_res, log):
            path_str = str(leg_target)
            result["legacy_removed"].append(path_str)
            result["removed"].append(path_str)
            log(f"[OK] removed (retired skill name): {leg_target}")
        else:
            result["skipped_remove"].append(str(leg_target))

    for name in managed:
        target = (dst_parent / name).resolve()
        if target.exists():
            if not _opencode_skills_is_strict_child(target, dst_parent_res):
                msg = f"refuse remove (path escape): {target}"
                result["errors"].append(msg)
                result["skipped_remove"].append(str(target))
                log(f"[WARN] {msg}")
                continue
            if _opencode_skills_safe_rmtree_skill_dir(target, dst_parent_res, log):
                result["removed"].append(str(target))
                log(f"[OK] removed: {target}")
            else:
                result["skipped_remove"].append(str(target))

    for name in managed:
        from_dir = src / name
        to_dir = dst_parent / name
        if not from_dir.is_dir():
            result["errors"].append(f"missing source skill: {from_dir}")
            result["ok"] = False
            continue
        shutil.copytree(from_dir, to_dir)
        result["copied"].append(str(to_dir))
        log(f"[OK] copied: {name} -> {to_dir}")

    if write_sidecar and result["ok"] and not result.get("skipped"):
        sidecar = dst_parent / ".sysplorer_mcp_skills_source_version"
        stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        ver = _read_mcp_build_version(bundle)
        text = f"version={ver}\nutc={stamp}\nbundle_root={bundle}\n"
        try:
            write_text_atomic(str(sidecar), text, encoding="utf-8", newline="\n")
            result["sidecar"] = str(sidecar)
        except OSError as exc:
            result["errors"].append(f"sidecar write failed: {exc}")

    if result["errors"]:
        result["ok"] = False

    return result


def sync_agent_skills(
    *,
    bundle_root: Optional[Path] = None,
    source_dir: Optional[Path] = None,
    dest_roots: Optional[List[tuple]] = None,
    log: LogFn = _sync_skills_log_default,
    write_sidecar: bool = True,
) -> dict:
    """Sync bundled skills to all configured agent destinations (OpenCode + Mogick by default)."""
    destinations = dest_roots or agent_skills_default_dest_roots()
    combined: dict = {
        "ok": True,
        "skipped": False,
        "destinations": [],
        "errors": [],
    }
    any_synced = False
    for label, dest in destinations:
        out = sync_opencode_skills(
            bundle_root=bundle_root,
            source_dir=source_dir,
            dest_root=dest,
            dest_label=label,
            log=log,
            write_sidecar=write_sidecar,
        )
        combined["destinations"].append(out)
        if out.get("errors"):
            combined["errors"].extend(out["errors"])
        if not out.get("skipped"):
            any_synced = True
    if combined["errors"]:
        combined["ok"] = False
    if not any_synced and combined["destinations"]:
        combined["skipped"] = all(d.get("skipped") for d in combined["destinations"])
    return combined


def _sync_opencode_skills_cli_main(cli_argv: Optional[List[str]]) -> int:
    """CLI for ``python install_mcp_silent.py --sync-opencode-skills ...`` (replaces old sync_opencode_skills.py)."""
    p = argparse.ArgumentParser(
        description="Sync bundled resources/modeling_skills into OpenCode and Mogick global skills directories.",
    )
    p.add_argument(
        "--bundle-root",
        type=Path,
        default=None,
        help="MCP bundle root (directory with resources/); default: auto",
    )
    p.add_argument(
        "--source",
        type=Path,
        default=None,
        help="Override modeling_skills source directory",
    )
    p.add_argument(
        "--dest",
        type=Path,
        default=None,
        help="Override skills root for a single destination (~/.config/opencode/skills by default when alone)",
    )
    p.add_argument(
        "--dest-mogick",
        type=Path,
        default=None,
        help="Override Mogick skills root (~/.mworks/mogick/Sysplorer/skills); only used when --dest is not set",
    )
    p.add_argument(
        "--opencode-only",
        action="store_true",
        help="Sync only to OpenCode (skip Mogick)",
    )
    p.add_argument(
        "--mogick-only",
        action="store_true",
        help="Sync only to Mogick (skip OpenCode)",
    )
    p.add_argument("--dry-run", action="store_true", help="List managed names only; no delete/copy")
    args = p.parse_args(cli_argv)

    bundle = (args.bundle_root or opencode_skills_resolve_bundle_root()).resolve()
    src = (args.source or opencode_skills_default_source(bundle)).resolve()
    managed = list_managed_skill_names(src) if src.is_dir() else []
    if args.dry_run:
        print("managed skill dirs:", ", ".join(managed) or "<none>")
        print("retired dirs removed on sync if present under dest:", ", ".join(retired_skill_dir_names(bundle)) or "<none>")
        print("source:", src)
        if args.dest is not None:
            print("dest:", args.dest.resolve())
        elif args.mogick_only:
            print("dest:", (args.dest_mogick or mogick_skills_default_dest_root()).resolve())
        elif args.opencode_only:
            print("dest:", opencode_skills_default_dest_root().resolve())
        else:
            for label, dest in agent_skills_default_dest_roots():
                override = args.dest_mogick if label == "Mogick" and args.dest_mogick else None
                print(f"dest ({label}):", (override or dest).resolve())
        return 0

    if args.dest is not None:
        out = sync_opencode_skills(bundle_root=bundle, source_dir=args.source, dest_root=args.dest)
        if out.get("skipped"):
            return 0
        return 0 if out.get("ok") and not out.get("errors") else 1

    dest_roots: List[tuple] = []
    if args.mogick_only:
        dest_roots.append(("Mogick", (args.dest_mogick or mogick_skills_default_dest_root()).resolve()))
    elif args.opencode_only:
        dest_roots.append(("OpenCode", opencode_skills_default_dest_root()))
    else:
        dest_roots = agent_skills_default_dest_roots()
        if args.dest_mogick is not None:
            dest_roots = [
                (label, args.dest_mogick.resolve() if label == "Mogick" else dest)
                for label, dest in dest_roots
            ]

    out = sync_agent_skills(
        bundle_root=bundle,
        source_dir=args.source,
        dest_roots=dest_roots,
    )
    if out.get("skipped"):
        return 0
    return 0 if out.get("ok") and not out.get("errors") else 1


def _maybe_sync_opencode_skills(mworks_install_dir: str) -> None:
    if os.environ.get("NO_SYNC_OPENCODE_SKILLS", "").strip().lower() in ("1", "true", "yes"):
        log_warn("skipping agent skills sync (NO_SYNC_OPENCODE_SKILLS is set)")
        return
    mcp_bundle = Path(mworks_install_dir) / "Tools" / "sysplorer_mcp"
    skills_source = mcp_bundle / "resources" / "modeling_skills"
    try:
        out = sync_agent_skills(
            bundle_root=mcp_bundle.resolve(),
            source_dir=skills_source.resolve(),
            log=_sync_skills_log_default,
        )
    except Exception as exc:
        log_warn(f"agent skills sync failed: {exc}")
        return
    if out.get("skipped"):
        return
    for item in out.get("destinations") or ():
        if item.get("skipped"):
            continue
        label = item.get("dest_label") or "Agent"
        if item.get("ok"):
            log_ok(f"{label} global skills synced: {item.get('dest_root')}")
        else:
            log_warn(
                f"{label} skills sync finished with issues: "
                + "; ".join(item.get("errors") or ())
            )


def install_mcp(mworks_install_dir, platform_label):
    mworks_install_dir = normalize_install_dir(mworks_install_dir)
    platform_label = resolve_platform_label(platform_label)
    python_exe = get_sysplorer_python_path(mworks_install_dir)
    main_py = resolve_main_py(mworks_install_dir)
    args = build_server_args(main_py, mworks_install_dir, platform_label)

    home_dir = get_home_dir()
    claude_config_path = os.path.join(home_dir, ".claude.json")
    opencode_config_path = os.path.join(home_dir, ".config", "opencode", "opencode.json")
    codex_config_path = os.path.join(home_dir, ".codex", "config.toml")
    mogick_path = mogick_config_path(home_dir)

    # Preflight: JSON must be valid before any write happens.
    claude_config_data = load_json(claude_config_path)
    opencode_config_data = load_json(opencode_config_path)
    mogick_config_data = load_json(mogick_path)

    errors = []
    updated = []

    for client_name, updater, config_path in (
        ("Claude", update_claude_config, claude_config_path),
        ("OpenCode", update_opencode_config, opencode_config_path),
        ("Codex", update_codex_config, codex_config_path),
        ("Mogick", update_mogick_config, mogick_path),
    ):
        try:
            if client_name == "Claude":
                updater(config_path, claude_config_data, python_exe, args)
            elif client_name in ("OpenCode", "Mogick"):
                data = opencode_config_data if client_name == "OpenCode" else mogick_config_data
                updater(config_path, data, python_exe, args, mworks_install_dir)
            else:
                updater(config_path, python_exe, args)
            updated.append(client_name)
        except Exception as exc:
            errors.append(f"{client_name}: {exc}")
            log_warn(f"{client_name} configuration update failed: {exc}")

    if not updated:
        raise RuntimeError("Failed to update any client configuration:\n" + "\n".join(errors))
    if errors:
        log_warn("partial success; updated clients: " + ", ".join(updated))
        for item in errors:
            log_warn(item)
    _maybe_sync_opencode_skills(mworks_install_dir)
    return updated, errors


def main(*args):
    args_list = list(args)
    if len(args_list) >= 2 and args_list[1] == "--sync-opencode-skills":
        return _sync_opencode_skills_cli_main(args_list[2:])
    argv = [a for a in args if a != "--no-sync-opencode-skills"]
    no_sync = len(argv) != len(args)
    if len(argv) < 2 or len(argv) > 3:
        print(
            "Usage: python install_mcp_silent.py <mworks_install_dir> [platform_label] "
            "[--no-sync-opencode-skills]\n"
            "   or: python install_mcp_silent.py --sync-opencode-skills [--bundle-root DIR] [--source PATH] "
            "[--dest PATH] [--dry-run]"
        )
        return 1
    try:
        if no_sync:
            os.environ["NO_SYNC_OPENCODE_SKILLS"] = "1"
        mworks_install_dir = argv[1]
        platform_label = argv[2] if len(argv) == 3 else "Sysplorer 2026b"
        updated, errors = install_mcp(mworks_install_dir, platform_label)
        log_ok("silent MCP installation completed.")
        if errors:
            log_warn("completed with warnings")
        else:
            log_ok("updated clients: " + ", ".join(updated))
        return 0
    except Exception as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(*sys.argv))
