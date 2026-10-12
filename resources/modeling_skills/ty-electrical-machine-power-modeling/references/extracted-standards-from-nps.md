# Extracted Standards From NPS References

以下规则来自对 `NPSLibrary.mol` 与 `NPS_New` 目录的结构抽样，不代表必须逐字复刻，但应优先遵守。

## 1. Component-As-Package

- 单个组件通常不是散落文件，而是一个独立 package。
- 常见形式:
  - `ComponentName/ComponentName.mo`
  - `ComponentName/package.mo`
  - `ComponentName/package.order`

## 2. Common Subpackages

在 `NPS_New` 中高频出现的子包:

- `Tests`
- `Examples`
- `Basic`
- `Components`
- `Types`
- `Resources`

最低建议保留 `Tests`，其余按复杂度增加。

## 3. Test Organization

- 已存在很多 `Tests` 和 `Examples` 样例。
- 常见命名:
  - `Test_*`
  - `*_SimulinkCase`
  - `*_AgainstSimulink`
  - `VoltageRideThroughCase`
  - `ConditioningRecoveryCase`

这说明“组件开发”与“对标验证”是 package 的一部分，不应外包到别处。

## 4. Solver Baseline In Samples

在未发布组件中大量使用:

- `Interval = 5e-5`
- `IntegratorStep = 5e-5`
- `Algorithm = ImplicitEuler` 或 `InlineImplicitEuler`

这与用户要求的 Sysplorer 对标基线一致。

## 5. Parameter And Interface Exposure

从 `LeadLagFilter`、`PulseGeneratorThyristor6Pulse`、`SecondOrderFilterVariableTuned` 等文件可见:

- 参数常带 `annotation(Dialog(group="..."))`
- 枚举参数常带 `choices(...)`
- 中文注释直接写在参数字符串中
- 接口端口也写注释

因此新组件必须把“用户能调的量”显式暴露出来，而不是藏在内部常量里。

## 6. Simulink Compatibility Naming

在 `NPS_New` 中已出现:

- `NonlinearInductorSimulinkCompat`
- `Test_OnDelay_AgainstSimulink`
- `PulseGeneratorThyristor6Pulse_SimulinkCase`

建议对明确的复现件沿用类似命名，便于识别“这是对标件”。

## 7. Documentation Is Part Of Delivery

很多组件和子包都带 `Documentation(info=...)`。

这意味着:

- 组件说明不是可选项
- 测试模型也应说明测试目的
- 帮助文档应建立在代码内注释完整的前提上

## 8. NPSLibrary.mol Archive Observations

从 `.mol` 压缩内容可见:

- `Examples/basic`
- `Examples/LoadFlow`
- `Examples/Microgrids`
- `Examples/MotorAndControl`
- `Examples/PowerElectronicCircuits`
- `Interfaces`
- `Motors`

结论:

- 参考库重视“按领域分层”和“示例先行”
- 组件建模时应同时准备可运行示例，而不是只交一个元件
