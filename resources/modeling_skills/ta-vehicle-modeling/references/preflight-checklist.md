# TA 新建模型预检清单

新建 TA 整车或子系统模型时，先读本文件，再读场景 workflow 和必要 reference。若本文件与较长 reference 有冲突，按本文件的阻断项先停下处理。

## 写模型前

1. 形成建模契约：主目标、车型架构、工况、落地等级、主库/辅助库、参考示例或参考类、顶层组件、暴露接口/总线；仅结果验收在范围时填写预期结果变量，否则记 `not_required`。
2. 只选一个 TA 主库；辅助库必须由建模契约说明，不得无差别加载 TA 六库。
3. 官方示例、整车架构和子系统模板只能作为参考模式；新交付模型不得直接复制或 `extends` 完整官方示例、完整整车架构或完整子系统模板。
4. 交付模型必须显式包含关键组件实例和 `connect(...)`，不能把用户要求可见的拓扑藏在继承来的完整模板里。
5. 建模困难、内部信号接线找不到、修复失败或时间压力不是绕过第 3、4 条的理由；遇阻时先缩小范围、拆分子系统、手工补齐可见拓扑，或报告阻塞点。

## 写源码时

1. Modelica 物理模型必须写 `.mo` 文本，并声明 `uses(Modelica(version = "4.0.0.TY.1"))`：独立模型在本文件声明，包内模型沿用顶层 `package.mo` 的依赖；不为通过审计而在每个子模型重复添加注解。
2. 参数默认不改；任何非默认参数都必须能回到用户需求、库接口闭合、初始化或合理性验证。
3. 允许的 `extends` 仅限小粒度接口、connector、record、replaceable partial 基类，或不隐藏拓扑的用户自有抽象。
4. 顶层关键实例和连接应带可复核的 `Placement` / `Line` annotation，后续仍按父级 Gate 6 做图面验收。

## 仿真前

1. 先运行源码审计脚本，例如：

   ```bash
   python scripts/audit_modelica_source.py path/to/model.mo --allowed-library TAEconomy --allowed-library TADynamics
   python scripts/audit_modelica_source.py path/to/VehicleLib/Tests/DriveTest.mo --dependency-root path/to/VehicleLib --allowed-library TAEconomy
   ```

   包内模型的 `--dependency-root` 必须是本次已经获准读取的顶层包目录；只读取模型及其到该根之间的 `package.mo`，不递归扫描、不自动访问根外父目录，解析后越界的符号链接/目录联接会被拒绝。未提供该参数时只检查当前文件；根未获授权或依赖不完整时报告阻塞，不扩大读取范围或伪造依赖。固定版本、禁继承及默认连接数规则不变；审计输出依赖证据文件，任一可见 Modelica 版本冲突均需处理。

2. 审计未通过时，不进入 `check_model`、翻译或仿真；先重构源码或补齐建模契约。
3. 明确仿真时长和工具参数映射：用户要求 20s/60s/CLTC 等时，必须确认模型实验设置或仿真工具的 stop time / StopTime / stopTime 已设置为目标时长或目标工况结束时间。
4. 不要把结果读取/校验时刻误当仿真终止时间。若工具同时有 stop-time 参数和 `target_time` / probe time 参数，前者控制仿真时长，后者只用于结果采样或校验。
5. 如果当前工具 schema 没有暴露 stop-time 参数，先用模型实验设置、仿真配置或官方帮助确认设置路径；不能确认时，在交付中明确“仿真终止时间未能由工具确认”，不得声称已按目标时长完成。
6. 审计和适用的仿真时长预检通过后回到父级七门闸，执行到本次请求终态。图形注解语法/结构错误由检查阻断；纯视觉缺陷不阻塞检查/翻译/仿真，完整图形交付前完成适用 Gate 6。结果核验未要求时记 `not_required`。
7. 最终回复中必须声明官方/样例使用状态：仅参考、直接复用已有样例或未使用。
