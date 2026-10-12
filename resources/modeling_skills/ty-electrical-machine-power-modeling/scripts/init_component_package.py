#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


PACKAGE_MO_TEMPLATE = """within __WITHIN__;
package __NAME__
  annotation(Documentation(info="<html><p>__NAME__ package.</p></html>"));
end __NAME__;
"""

SUBPACKAGE_MO_TEMPLATE = """within __WITHIN__;
package __NAME__
  annotation(Documentation(info="<html><p>__NAME__ subpackage.</p></html>"));
end __NAME__;
"""

COMPONENT_TEMPLATE = """within __WITHIN__;
model __NAME__
  "TODO: 补充组件中文说明"

  parameter Real sampleTime(unit="s") = 5e-5
    "采样时间 sampleTime，单位 s"
    annotation(Dialog(group="离散设置"));

  Modelica.Blocks.Interfaces.RealInput u
    "输入信号，按实际物理意义修改"
    annotation(Placement(transformation(extent={{-120,-20},{-80,20}})));
  Modelica.Blocks.Interfaces.RealOutput y
    "输出信号，按实际物理意义修改"
    annotation(Placement(transformation(extent={{80,-10},{120,10}})));

equation
  y = u;

  annotation(
    Documentation(info="<html><p>TODO: 补充原理、参数、接口说明。</p></html>"),
    Icon(coordinateSystem(extent={{-100,-100},{100,100}})),
    Diagram(coordinateSystem(extent={{-100,-100},{100,100}})));
end __NAME__;
"""

TEST_TEMPLATE = """within __WITHIN__;
model __NAME__
  annotation(experiment(StartTime=0, StopTime=0.1, Interval=5e-5, Algorithm=ImplicitEuler),
    Documentation(info="<html><p>TODO: 补充测试目的与对标来源。</p></html>"));
end __NAME__;
"""


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def fill_template(template: str, within: str, name: str) -> str:
    return template.replace("__WITHIN__", within).replace("__NAME__", name)


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize a component package skeleton.")
    parser.add_argument("root", help="Root directory where the component package will be created.")
    parser.add_argument("name", help="Component package name.")
    parser.add_argument(
        "--within",
        default=None,
        help="Explicit parent package path, for example NPS_New.SkillValidationCases. Defaults to the root directory name.",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    name = args.name
    within_root = args.within or root.name
    package_dir = root / name
    package_dir.mkdir(parents=True, exist_ok=True)

    write_file(
        package_dir / "package.mo",
        fill_template(PACKAGE_MO_TEMPLATE, within=within_root, name=name),
    )
    write_file(package_dir / "package.order", f"{name}\nTests\nExamples\nResources\n")
    write_file(
        package_dir / f"{name}.mo",
        fill_template(COMPONENT_TEMPLATE, within=f"{within_root}.{name}", name=name),
    )

    for subpackage in ("Tests", "Examples", "Resources"):
        sub_dir = package_dir / subpackage
        sub_dir.mkdir(exist_ok=True)
        write_file(
            sub_dir / "package.mo",
            fill_template(
                SUBPACKAGE_MO_TEMPLATE,
                within=f"{within_root}.{name}",
                name=subpackage,
            ),
        )
        write_file(sub_dir / "package.order", "")

    tests_dir = package_dir / "Tests"
    write_file(
        tests_dir / "Case1.mo",
        fill_template(
            TEST_TEMPLATE,
            within=f"{within_root}.{name}.Tests",
            name="Case1",
        ),
    )
    write_file(
        tests_dir / "Case2.mo",
        fill_template(
            TEST_TEMPLATE,
            within=f"{within_root}.{name}.Tests",
            name="Case2",
        ),
    )
    write_file(tests_dir / "package.order", "Case1\nCase2\n")

    print(f"Created component package at: {package_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
