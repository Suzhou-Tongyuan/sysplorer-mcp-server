# 需求映射

本文件只负责把常见用户说法映射到任务类型、建议 workflow 和首批 reference。主库选择见 `library-selection.md`。

| 用户说法 | 任务类型 | 建议 workflow | 首批读取 |
|---|---|---|---|
| 用 TA 车辆库搭一个整车模型 | 新建整车模型 | `../workflows/build-from-scenario.md` | `library-selection.md` |
| 在 Sysplorer 里搭底盘、悬架或操稳模型 | 新建动力学模型 | `../workflows/build-from-scenario.md` | `library-selection.md`、`library-cards/TADynamics.md` |
| 做动力性、经济性、续航分析 | 整车性能分析 | `../workflows/build-from-scenario.md` | `library-selection.md`、`library-cards/TAEconomy.md` |
| 做悬架、K&C、操稳、平顺性分析 | 动力学分析 | `../workflows/build-from-scenario.md` | `library-selection.md`、`library-cards/TADynamics.md` |
| 做热管理、热泵空调、水冷回路、电池热管理 | 热管理建模或分析 | `../workflows/build-from-scenario.md` | `library-selection.md`、按主目标读 `library-cards/TAThermalSystem.md` 或 `library-cards/TABattery.md` |
| 做发动机、进排气、增压、供油 | 发动机细化建模 | `../workflows/build-from-scenario.md` | `library-selection.md`、`library-cards/TAEngine.md` |
| 做电芯、模组、电池包或 BMS | 电池细化建模 | `../workflows/build-from-scenario.md` | `library-selection.md`、`library-cards/TABattery.md` |
| 做低压电器、DCDC、车身电器、附件功耗 | 电子电器建模 | `../workflows/build-from-scenario.md` | `library-selection.md`、`library-cards/TAElectronic.md` |
| 修一下这个车辆模型 | 修复已有模型 | `../workflows/repair-existing-model.md` | `error-repair-playbook.md` |
| 先让模型 Check/Translate 通过 | 编译通过类修复任务 | `../workflows/repair-existing-model.md` | `error-repair-playbook.md` |
| 跑一下官方样例或公司样例 | 样例验证 | `../workflows/verify-example.md` | `validation-rules.md`、对应库卡片 |
| 输出整车结果曲线、帮我看结果对不对 | 结果复核 | `../workflows/verify-example.md` | `validation-rules.md` |
| 帮我整理图面、检查布局注解 | 图面整改 | `../workflows/repair-existing-model.md` | `diagram-layout-rules.md` |
| 做整车联合模型 | 多库联合建模 | `../workflows/build-from-scenario.md` | `library-selection.md`、`combination-rules.md` |
| 只想问某个 Sysplorer API 怎么用 | API 查询 | 无 | 不触发本 skill，改走 API / 文档查询流程 |
| 做一个普通 Modelica 模型 | 一般 Modelica 建模 | 无 | 不触发本 skill，改走通用 Modelica 或模型库开发 skill |

## 使用说明

- 当用户说法同时涉及多个方向时，先归入一个主任务类型，再用 `library-selection.md` 选择主库。
- 当任务进入真实建模、改模、调试、图面或结果工作时，再按对应 workflow 读取必要规则文件。
- 不要因为本文件列出多个候选文件就一次性读取全部库卡片或全部规则。
