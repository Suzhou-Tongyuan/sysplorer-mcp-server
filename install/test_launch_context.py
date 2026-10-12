"""Unit tests for Sysplorer desktop-like launch env sanitization."""
from __future__ import annotations

import os
import sys
import unittest
from contextlib import nullcontext
from pathlib import Path
from unittest.mock import patch

PKG_DIR = Path(__file__).resolve().parent.parent / "sysplorer-mcp-server"
if str(PKG_DIR) not in sys.path:
    sys.path.insert(0, str(PKG_DIR))

from launch_context import (  # noqa: E402
    sanitize_sysplorer_child_env,
    start_sysplorer_in_desktop_context,
    strip_agent_utf8_env_from_process,
)


class LaunchContextEnvTests(unittest.TestCase):
    def test_sanitize_removes_opencode_desktop_utf8_knobs_on_windows(self) -> None:
        raw = {
            "PATH": "C:\\Windows",
            "CHCP": "65001",
            "LANG": "en_US.UTF-8",
            "LC_ALL": "en_US.UTF-8",
            "LC_CTYPE": "en_US.UTF-8",
            "PYTHONUTF8": "1",
            "PYTHONWUTF8": "1",
            "PYTHONIOENCODING": "utf-8",
            "COMSPEC": "C:\\Windows\\system32\\cmd.exe",
        }
        out = sanitize_sysplorer_child_env(raw, for_windows=True)
        self.assertEqual(out["PATH"], raw["PATH"])
        self.assertEqual(out["COMSPEC"], raw["COMSPEC"])
        for key in (
            "CHCP",
            "LANG",
            "LC_ALL",
            "LC_CTYPE",
            "PYTHONUTF8",
            "PYTHONWUTF8",
            "PYTHONIOENCODING",
        ):
            self.assertNotIn(key, out)

    def test_sanitize_unchanged_on_non_windows(self) -> None:
        raw = {"PYTHONUTF8": "1", "LANG": "en_US.UTF-8"}
        out = sanitize_sysplorer_child_env(raw, for_windows=False)
        self.assertEqual(out, raw)

    @patch("launch_context.platform.system", return_value="Windows")
    def test_strip_agent_utf8_env_from_process(self, _platform: unittest.mock.MagicMock) -> None:
        saved = dict(os.environ)
        try:
            os.environ["CHCP"] = "65001"
            os.environ["PYTHONUTF8"] = "1"
            os.environ["LANG"] = "en_US.UTF-8"
            strip_agent_utf8_env_from_process()
            self.assertNotIn("CHCP", os.environ)
            self.assertNotIn("PYTHONUTF8", os.environ)
            self.assertNotIn("LANG", os.environ)
            self.assertNotIn("LC_ALL", os.environ)
        finally:
            os.environ.clear()
            os.environ.update(saved)

    def test_start_sysplorer_wrapper_uses_native_and_desktop_context(self) -> None:
        calls: list[tuple[tuple[object, ...], dict[str, object]]] = []

        def fake_start(*args, **kwargs):
            calls.append((args, kwargs))

        with (
            patch("launch_context.desktop_like_sysplorer_launch_context", return_value=nullcontext()) as desktop_ctx,
            patch(
                "core.subprocess_encoding.windows_strip_utf8_mode_env_while_calling_native",
                return_value=nullcontext(),
            ) as native_ctx,
        ):
            start_sysplorer_in_desktop_context(fake_start, r"C:\MWORKS\Bin64\mworks.exe", start_mode="-q")

        native_ctx.assert_called_once_with()
        desktop_ctx.assert_called_once_with()
        self.assertEqual(calls, [(("-q",), {"processPath": r"C:\MWORKS\Bin64\mworks.exe"})])


if __name__ == "__main__":
    unittest.main()
