"""Unit tests for OpenCode skills sync (whitelist delete, foreign dir preservation)."""
from __future__ import annotations

import shutil
import sys
import unittest
from pathlib import Path

INSTALL_DIR = Path(__file__).resolve().parent
if str(INSTALL_DIR) not in sys.path:
    sys.path.insert(0, str(INSTALL_DIR))

import install_mcp_silent as s  # noqa: E402


class TestSyncOpenCodeSkills(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = Path(__file__).resolve().parent / "_test_sync_skills_tmp"
        if self._tmp.exists():
            shutil.rmtree(self._tmp)
        self._tmp.mkdir(parents=True)

    def tearDown(self) -> None:
        if self._tmp.exists():
            shutil.rmtree(self._tmp, ignore_errors=True)

    def _make_skill(self, root: Path, name: str) -> None:
        d = root / name
        d.mkdir(parents=True)
        (d / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: test\nmetadata:\n  version: 0.0.1\n---\n",
            encoding="utf-8",
        )

    def test_managed_list_only_skill_md_dirs(self) -> None:
        src = self._tmp / "modeling_skills"
        src.mkdir()
        self._make_skill(src, "ty-aaa")
        (src / "not-a-skill").mkdir()
        (src / "not-a-skill" / "readme.txt").write_text("x", encoding="utf-8")
        (src / "Skills汇总.md").write_text("# x", encoding="utf-8")
        names = s.list_managed_skill_names(src)
        self.assertEqual(names, ["ty-aaa"])

    def test_foreign_directory_not_deleted(self) -> None:
        src = self._tmp / "src_skills"
        dst = self._tmp / "opencode" / "skills"
        src.mkdir(parents=True)
        self._make_skill(src, "ty-managed-one")
        self._make_skill(src, "ty-managed-two")
        dst.mkdir(parents=True)
        foreign = dst / "user-custom-skill"
        foreign.mkdir()
        (foreign / "SKILL.md").write_text(
            "---\nname: user-custom-skill\ndescription: x\n---\n", encoding="utf-8"
        )

        out = s.sync_opencode_skills(
            bundle_root=self._tmp,
            source_dir=src,
            dest_root=dst,
            write_sidecar=False,
            log=lambda _m: None,
        )
        self.assertTrue(out["ok"], msg=out)
        self.assertTrue(foreign.is_dir())
        self.assertTrue((foreign / "SKILL.md").is_file())
        self.assertTrue((dst / "ty-managed-one" / "SKILL.md").is_file())
        self.assertTrue((dst / "ty-managed-two" / "SKILL.md").is_file())

    def test_refuse_delete_outside_dest(self) -> None:
        src = self._tmp / "src2"
        dst = self._tmp / "dst2"
        src.mkdir(parents=True)
        dst.mkdir(parents=True)
        self._make_skill(src, "evil")
        self.assertFalse(s._opencode_skills_is_strict_child(dst.resolve(), dst.resolve()))

    def test_source_missing_skips_ok_no_errors(self) -> None:
        missing = self._tmp / "no_such_modeling_skills"
        dst = self._tmp / "dest_skip"
        out = s.sync_opencode_skills(
            bundle_root=self._tmp,
            source_dir=missing,
            dest_root=dst,
            write_sidecar=False,
            log=lambda _m: None,
        )
        self.assertTrue(out["ok"], msg=out)
        self.assertTrue(out.get("skipped"))
        self.assertEqual(out.get("skip_reason"), "source_missing")
        self.assertFalse(out.get("errors"))
        self.assertFalse(dst.exists())

    def test_source_empty_dir_skips_ok(self) -> None:
        src = self._tmp / "empty_skills"
        src.mkdir()
        dst = self._tmp / "dest_empty"
        out = s.sync_opencode_skills(
            bundle_root=self._tmp,
            source_dir=src,
            dest_root=dst,
            write_sidecar=False,
            log=lambda _m: None,
        )
        self.assertTrue(out["ok"], msg=out)
        self.assertTrue(out.get("skipped"))
        self.assertEqual(out.get("skip_reason"), "no_managed_skills")
        self.assertFalse(out.get("errors"))

    def test_retired_old_skill_name_removed_from_dest(self) -> None:
        """If dest still has pre-rename skill dir, it is removed so only current bundle names remain."""
        src = self._tmp / "src_retired"
        dst = self._tmp / "dest_retired"
        src.mkdir(parents=True)
        dst.mkdir(parents=True)
        self._make_skill(src, "ty-sysplorer-modeling-rules")
        (src / "ty-sysplorer-modeling-rules" / "SKILL.md").write_text(
            "---\nname: ty-sysplorer-modeling-rules\n---\nNEW\n", encoding="utf-8"
        )
        old_router = dst / "ty-sysplorer-modeling-router"
        old_router.mkdir()
        (old_router / "SKILL.md").write_text("---\nname: old\n---\n", encoding="utf-8")

        out = s.sync_opencode_skills(
            bundle_root=self._tmp,
            source_dir=src,
            dest_root=dst,
            write_sidecar=False,
            log=lambda _m: None,
        )
        self.assertTrue(out["ok"], msg=out)
        self.assertFalse((dst / "ty-sysplorer-modeling-router").exists(), msg="stale pre-rename skill dir must be gone")
        self.assertIn(str(old_router.resolve()), out.get("legacy_removed") or [])
        text = (dst / "ty-sysplorer-modeling-rules" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("NEW", text)

    def test_lite_pack_retires_cad_and_mds_skills(self) -> None:
        src = self._tmp / "src_lite"
        dst = self._tmp / "dest_lite"
        src.mkdir(parents=True)
        dst.mkdir(parents=True)
        self._make_skill(src, "ty-sysplorer-modeling-rules")
        for leftover in ("ty-cadtool-modeling", "sysplorer-mds-docs"):
            old = dst / leftover
            old.mkdir()
            (old / "SKILL.md").write_text("---\nname: leftover\n---\n", encoding="utf-8")
        (self._tmp / "MCP_BUILD_INFO.json").write_text(
            '{"pack_variant": "modelica_lite", "version": "0.0-test"}',
            encoding="utf-8",
        )
        out = s.sync_opencode_skills(
            bundle_root=self._tmp,
            source_dir=src,
            dest_root=dst,
            write_sidecar=False,
            log=lambda _m: None,
        )
        self.assertTrue(out["ok"], msg=out)
        self.assertFalse((dst / "ty-cadtool-modeling").exists())
        self.assertFalse((dst / "sysplorer-mds-docs").exists())
        self.assertTrue((dst / "ty-sysplorer-modeling-rules" / "SKILL.md").is_file())

    def test_same_name_dest_removed_then_copied(self) -> None:
        """Managed name under dest is deleted only for that folder, then replaced from source."""
        src = self._tmp / "src_replace"
        dst = self._tmp / "dest_replace"
        src.mkdir(parents=True)
        dst.mkdir(parents=True)
        self._make_skill(src, "skill-a")
        (src / "skill-a" / "SKILL.md").write_text("---\nname: skill-a\n---\nNEW", encoding="utf-8")
        old = dst / "skill-a"
        old.mkdir()
        (old / "SKILL.md").write_text("---\nname: skill-a\n---\nOLD", encoding="utf-8")
        (old / "stale.txt").write_text("gone", encoding="utf-8")

        out = s.sync_opencode_skills(
            bundle_root=self._tmp,
            source_dir=src,
            dest_root=dst,
            write_sidecar=False,
            log=lambda _m: None,
        )
        self.assertTrue(out["ok"], msg=out)
        self.assertFalse(out.get("skipped"))
        self.assertIn(str(old.resolve()), out.get("removed") or [])
        text = (dst / "skill-a" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("NEW", text)
        self.assertNotIn("OLD", text)
        self.assertFalse((dst / "skill-a" / "stale.txt").exists())

    def test_modelex_default_dest_root(self) -> None:
        expected = (Path.home() / ".modelex" / "skills").resolve()
        self.assertEqual(s.modelex_skills_default_dest_root(), expected)

    def test_sync_agent_skills_writes_both_destinations(self) -> None:
        src = self._tmp / "src_both"
        opencode_dst = self._tmp / "opencode" / "skills"
        modelex_dst = self._tmp / "modelex" / "skills"
        src.mkdir(parents=True)
        self._make_skill(src, "ty-both")

        out = s.sync_agent_skills(
            bundle_root=self._tmp,
            source_dir=src,
            dest_roots=[
                ("OpenCode", opencode_dst),
                ("Modelex", modelex_dst),
            ],
            write_sidecar=False,
            log=lambda _m: None,
        )
        self.assertTrue(out["ok"], msg=out)
        self.assertTrue((opencode_dst / "ty-both" / "SKILL.md").is_file())
        self.assertTrue((modelex_dst / "ty-both" / "SKILL.md").is_file())
        self.assertEqual(len(out.get("destinations") or []), 2)

    def test_skipped_no_sidecar_file(self) -> None:
        missing = self._tmp / "missing_for_sidecar"
        dst = self._tmp / "dest_sidecar"
        out = s.sync_opencode_skills(
            bundle_root=self._tmp,
            source_dir=missing,
            dest_root=dst,
            write_sidecar=True,
            log=lambda _m: None,
        )
        self.assertTrue(out.get("skipped"))
        sidecar = dst / ".sysplorer_mcp_skills_source_version"
        self.assertFalse(sidecar.exists())


if __name__ == "__main__":
    unittest.main()
