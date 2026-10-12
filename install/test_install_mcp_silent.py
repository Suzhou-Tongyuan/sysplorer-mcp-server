"""Tests for install_mcp_silent (unit + install_mcp integration + subprocess main)."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

INSTALL_DIR = Path(__file__).resolve().parent
if str(INSTALL_DIR) not in sys.path:
    sys.path.insert(0, str(INSTALL_DIR))

import install_mcp_silent as ims  # noqa: E402


def _touch(path: Path, text: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _fake_mworks_layout(root: Path, *, use_sysplorer_mcp_subpath: bool = False) -> None:
    """Minimal Sysplorer-style tree so get_sysplorer_python_path / resolve_main_py succeed."""
    if sys.platform == "win32":
        py = root / "External" / "python64" / "python.exe"
    else:
        py = root / "external" / "python64" / "bin" / "python3"
    _touch(py, "")
    if use_sysplorer_mcp_subpath:
        _touch(root / "Tools" / "sysplorer_mcp" / "main.py", "# stub main")
    else:
        _touch(root / "Tools" / "sysplorer_mcp_server" / "main.py", "# stub main")


def _fake_home_configs(home: Path) -> None:
    _touch(home / ".claude.json", "{}\n")
    _touch(home / ".config" / "opencode" / "opencode.json", "{}\n")
    codex = home / ".codex"
    codex.mkdir(parents=True, exist_ok=True)
    _touch(codex / "config.toml", "")
    mogick = home / ".mworks" / "mogick" / "Sysplorer"
    mogick.mkdir(parents=True, exist_ok=True)
    _touch(mogick / "mcp.json", "{}\n")


class TestNormalizeAndPlatform(unittest.TestCase):
    def test_normalize_strips_quotes_and_resolves(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            td = os.path.abspath(td)
            self.assertEqual(ims.normalize_install_dir(f'"{td}"'), td)

    def test_normalize_missing_dir_raises(self) -> None:
        with self.assertRaises(RuntimeError) as ctx:
            ims.normalize_install_dir(os.path.join(tempfile.gettempdir(), "nonexistent_mw_XYZ_12345"))
        self.assertIn("not found", str(ctx.exception))

    def test_normalize_none_raises(self) -> None:
        with self.assertRaises(RuntimeError):
            ims.normalize_install_dir(None)  # type: ignore[arg-type]

    def test_resolve_platform_default(self) -> None:
        self.assertEqual(ims.resolve_platform_label(None), "Sysplorer 2026b")
        self.assertEqual(ims.resolve_platform_label(""), "Sysplorer 2026b")
        self.assertEqual(ims.resolve_platform_label("   "), "Sysplorer 2026b")

    def test_resolve_platform_custom(self) -> None:
        self.assertEqual(ims.resolve_platform_label(" MyLabel "), "MyLabel")


class TestPathsAndArgs(unittest.TestCase):
    def setUp(self) -> None:
        self._td = tempfile.mkdtemp()
        self._root = Path(self._td)

    def tearDown(self) -> None:
        shutil.rmtree(self._td, ignore_errors=True)

    def test_get_sysplorer_python_prefers_external_case_nt(self) -> None:
        _fake_mworks_layout(self._root)
        p = ims.get_sysplorer_python_path(str(self._root))
        self.assertTrue(os.path.isfile(p))

    def test_resolve_main_prefers_sysplorer_mcp_server(self) -> None:
        _fake_mworks_layout(self._root, use_sysplorer_mcp_subpath=False)
        m = ims.resolve_main_py(str(self._root))
        self.assertTrue(m.endswith("main.py"))
        self.assertIn("sysplorer_mcp_server", m.replace("\\", "/"))

    def test_resolve_main_sysplorer_mcp_when_server_missing(self) -> None:
        _fake_mworks_layout(self._root, use_sysplorer_mcp_subpath=True)
        m = ims.resolve_main_py(str(self._root))
        self.assertIn("sysplorer_mcp", m.replace("\\", "/"))

    def test_build_server_args_order(self) -> None:
        args = ims.build_server_args("/x/main.py", "D:\\MW", "Plat")
        self.assertEqual(
            args,
            ["/x/main.py", "--mworks-install-dir", "D:\\MW", "--sysplorer-platform-label", "Plat"],
        )


class TestTomlHelpers(unittest.TestCase):
    def test_remove_mcp_servers_toml_block(self) -> None:
        body = """
other = 1
[mcp_servers.sysplorer_mcp]
command = "old"
[mcp_servers.sysplorer_mcp.env]
X = "y"
[unrelated]
k = "v"
""".strip()
        out = ims.remove_mcp_servers_toml_block(body, "sysplorer_mcp")
        self.assertNotIn("sysplorer_mcp", out)
        self.assertIn("unrelated", out)

    def test_strip_known_mcp_server_toml_blocks_removes_duplicate_sysplorer(self) -> None:
        body = """
[other]
k = 1

[mcp_servers.sysplorer]
command = "old1"
args = []

[mcp_servers.sysplorer]
command = "old2"
args = []
""".strip()
        out = ims.strip_known_mcp_server_toml_blocks(body)
        self.assertNotIn("sysplorer", out)
        self.assertIn("[other]", out)

    def test_write_codex_sysplorer_toml_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = os.path.join(td, "config.toml")
            ims.write_codex_sysplorer_toml(path, "python.exe", ["/x/main.py", "--label", "P"])
            ims.write_codex_sysplorer_toml(path, "python.exe", ["/x/main.py", "--label", "P"])
            text = Path(path).read_text(encoding="utf-8")
        self.assertEqual(text.count("[mcp_servers.sysplorer]"), 1)
        self.assertIn("P", text)


class TestInstallMcpIntegration(unittest.TestCase):
    def setUp(self) -> None:
        self._td = tempfile.mkdtemp()
        self._mw = Path(self._td) / "fake_mworks"
        self._home = Path(self._td) / "fake_home"
        self._mw.mkdir(parents=True)
        self._home.mkdir(parents=True)
        _fake_mworks_layout(self._mw)
        _fake_home_configs(self._home)
        self._prev_no_sync = os.environ.get("NO_SYNC_OPENCODE_SKILLS")
        os.environ["NO_SYNC_OPENCODE_SKILLS"] = "1"
        # Quiet stdout from install_mcp_silent log_ok / log_warn
        self._patcher_log_ok = patch.object(ims, "log_ok", lambda _m: None)
        self._patcher_log_warn = patch.object(ims, "log_warn", lambda _m: None)
        self._patcher_log_ok.start()
        self._patcher_log_warn.start()

    def tearDown(self) -> None:
        self._patcher_log_ok.stop()
        self._patcher_log_warn.stop()
        shutil.rmtree(self._td, ignore_errors=True)
        if self._prev_no_sync is None:
            os.environ.pop("NO_SYNC_OPENCODE_SKILLS", None)
        else:
            os.environ["NO_SYNC_OPENCODE_SKILLS"] = self._prev_no_sync

    def test_install_mcp_writes_claude_and_opencode_and_codex(self) -> None:
        with patch.object(ims, "get_home_dir", return_value=str(self._home)):
            updated, errors = ims.install_mcp(str(self._mw), "TestPlatform")

        self.assertEqual(errors, [])
        self.assertEqual(set(updated), {"Claude", "OpenCode", "Codex", "Mogick"})

        claude_path = self._home / ".claude.json"
        data = json.loads(claude_path.read_text(encoding="utf-8"))
        entry = data["mcpServers"]["sysplorer"]
        self.assertIn("command", entry)
        self.assertEqual(entry["args"][-1], "TestPlatform")

        oc_path = self._home / ".config" / "opencode" / "opencode.json"
        oc = json.loads(oc_path.read_text(encoding="utf-8"))
        self.assertEqual(oc["mcp"]["sysplorer"]["type"], "local")
        self.assertIn("--sysplorer-platform-label", oc["mcp"]["sysplorer"]["command"])
        if sys.platform.startswith("linux"):
            env = oc["mcp"]["sysplorer"].get("environment") or {}
            self.assertEqual(
                env.get("LD_LIBRARY_PATH"),
                str(self._mw / "bin64") + ":$LD_LIBRARY_PATH",
            )
        else:
            self.assertNotIn("environment", oc["mcp"]["sysplorer"])

        codex_path = self._home / ".codex" / "config.toml"
        toml_txt = codex_path.read_text(encoding="utf-8")
        self.assertIn("[mcp_servers.sysplorer]", toml_txt)
        self.assertIn("TestPlatform", toml_txt)

        mogick_path = self._home / ".mworks" / "mogick" / "Sysplorer" / "mcp.json"
        mogick = json.loads(mogick_path.read_text(encoding="utf-8"))
        mx = mogick["servers"]["sysplorer"]
        self.assertTrue(mx.get("enabled"))
        self.assertEqual(mx["type"], "local")
        self.assertIn("TestPlatform", mx["command"])

    def test_install_mcp_pops_legacy_mworks_mcp(self) -> None:
        legacy = {"mcpServers": {"mworks_mcp": {"command": "x"}, "keep": {}}}
        (self._home / ".claude.json").write_text(json.dumps(legacy), encoding="utf-8")
        with patch.object(ims, "get_home_dir", return_value=str(self._home)):
            ims.install_mcp(str(self._mw), "P")
        data = json.loads((self._home / ".claude.json").read_text(encoding="utf-8"))
        self.assertNotIn("mworks_mcp", data["mcpServers"])
        self.assertIn("sysplorer", data["mcpServers"])

    def test_install_mcp_pops_legacy_sysplorer_mcp(self) -> None:
        legacy = {"mcpServers": {"sysplorer_mcp": {"command": "x"}, "keep": {}}}
        (self._home / ".claude.json").write_text(json.dumps(legacy), encoding="utf-8")
        with patch.object(ims, "get_home_dir", return_value=str(self._home)):
            ims.install_mcp(str(self._mw), "P")
        data = json.loads((self._home / ".claude.json").read_text(encoding="utf-8"))
        self.assertNotIn("sysplorer_mcp", data["mcpServers"])
        self.assertIn("sysplorer", data["mcpServers"])
        self.assertIn("keep", data["mcpServers"])


class TestMainSubprocess(unittest.TestCase):
    """Runs install_mcp_silent.py as a script (same as user invocation)."""

    def setUp(self) -> None:
        self._td = tempfile.mkdtemp()
        self._mw = Path(self._td) / "mw"
        self._home = Path(self._td) / "home"
        self._mw.mkdir(parents=True)
        self._home.mkdir(parents=True)
        _fake_mworks_layout(self._mw)
        _fake_home_configs(self._home)

    def tearDown(self) -> None:
        shutil.rmtree(self._td, ignore_errors=True)

    def _run_script(self, extra_env: dict | None = None) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["USERPROFILE"] = str(self._home)
        env["HOME"] = str(self._home)
        env["NO_SYNC_OPENCODE_SKILLS"] = "1"
        if extra_env:
            env.update(extra_env)
        script = INSTALL_DIR / "install_mcp_silent.py"
        return subprocess.run(
            [sys.executable, str(script), str(self._mw), "SubPlatTest", "--no-sync-opencode-skills"],
            cwd=str(INSTALL_DIR),
            env=env,
            capture_output=True,
            text=True,
            timeout=120,
        )

    def test_main_subprocess_exit_zero(self) -> None:
        cp = self._run_script()
        self.assertEqual(cp.returncode, 0, msg=cp.stderr + cp.stdout)
        data = json.loads((self._home / ".claude.json").read_text(encoding="utf-8"))
        self.assertEqual(data["mcpServers"]["sysplorer"]["args"][-1], "SubPlatTest")

    def test_main_subprocess_bad_usage_exit_nonzero(self) -> None:
        env = os.environ.copy()
        env["USERPROFILE"] = str(self._home)
        env["HOME"] = str(self._home)
        cp = subprocess.run(
            [sys.executable, str(INSTALL_DIR / "install_mcp_silent.py")],
            cwd=str(INSTALL_DIR),
            env=env,
            capture_output=True,
            text=True,
            timeout=60,
        )
        self.assertEqual(cp.returncode, 1)
        self.assertIn("Usage", cp.stdout)

    def test_main_subprocess_missing_install_dir_exit_nonzero(self) -> None:
        env = os.environ.copy()
        env["USERPROFILE"] = str(self._home)
        env["HOME"] = str(self._home)
        bad_path = os.path.join(self._td, "no_such_mworks_dir_XYZ")
        cp = subprocess.run(
            [sys.executable, str(INSTALL_DIR / "install_mcp_silent.py"), bad_path],
            cwd=str(INSTALL_DIR),
            env=env,
            capture_output=True,
            text=True,
            timeout=60,
        )
        self.assertEqual(cp.returncode, 1)
        self.assertIn("ERROR", cp.stderr)


class TestSyncOpencodeSkillsSubcommand(unittest.TestCase):
    """``install_mcp_silent.py --sync-opencode-skills`` (merged former sync_opencode_skills.py)."""

    def test_subprocess_sync_skills_dry_run(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            bundle = Path(td)
            (bundle / "resources" / "modeling_skills").mkdir(parents=True)
            cp = subprocess.run(
                [
                    sys.executable,
                    str(INSTALL_DIR / "install_mcp_silent.py"),
                    "--sync-opencode-skills",
                    "--dry-run",
                    "--bundle-root",
                    str(bundle),
                ],
                cwd=str(INSTALL_DIR),
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertEqual(cp.returncode, 0, msg=cp.stderr + cp.stdout)
            self.assertIn("source:", cp.stdout)


class TestEnsureDictField(unittest.TestCase):
    def test_replaces_non_dict_mcp_servers(self) -> None:
        with patch.object(ims, "log_warn", lambda _m: None):
            data: dict = {"mcpServers": "broken"}
            d = ims.ensure_dict_field(data, "mcpServers", "cfg.json")
        self.assertIsInstance(d, dict)
        self.assertEqual(data["mcpServers"], d)

    def test_creates_missing_nested(self) -> None:
        data: dict = {}
        d = ims.ensure_dict_field(data, "mcp", "x.json")
        self.assertEqual(data["mcp"], d)


class TestLoadJsonEdgeCases(unittest.TestCase):
    def test_load_json_missing_returns_empty_dict(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            p = os.path.join(td, "nope.json")
            self.assertEqual(ims.load_json(p), {})

    def test_load_json_valid_utf8(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "a.json"
            p.write_text('{"x": 1}', encoding="utf-8")
            self.assertEqual(ims.load_json(str(p)), {"x": 1})


if __name__ == "__main__":
    unittest.main()
