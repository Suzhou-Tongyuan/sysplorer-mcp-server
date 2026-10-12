# Sysblock Block Reference

This file is authoritative for block availability and editable parameter keys. Read `runtime-contracts.md` for localized/version-sensitive enum values and disposable-probe rules; do not infer API values from UI labels or mask-document labels.

Use this reference to choose SysplorerEmbeddedCoder blocks, check allowed/prohibited modules, map natural-language needs to components, and set verified parameters. "Allowed" means the block is usable in the current environment; it does not mean every parameter is editable.

## Contents

- Use Rules
- Library Families
- Common Component Mapping
- Allowed Blocks
- Prohibited Blocks
- Conditional Blocks
- Batch Parameter APIs

## Use Rules

- Prefer allowed blocks for the minimum runnable closed loop.
- Follow any listed editable-parameter restrictions and preconditions.
- Do not use prohibited blocks even if the class exists.
- Use conditional blocks only when necessary and when the listed limits are acceptable.
- Treat blocks not listed here as conditional by default.
- Topology edits still use modeling APIs such as `AddComponent`, `RemoveComponent`, and `ConnectPort`; parameter APIs do not replace topology editing.
- When a concrete parameter name is not listed here, search `references/sysblock-parameters.json` by full block class name.

## Library Families

The SysplorerEmbeddedCoder library is organized by block family:

| Family | Typical use |
|---|---|
| `Continuous` | Continuous dynamics such as integrators, transfer functions, state space, PID, and delays. |
| `Discrete` | Discrete-time delay, memory, discrete integrator, discrete transfer function, and zero-order hold blocks. |
| `Discontinuities` | Saturation, dead zone, relay, rate limiter, quantizer, and related nonlinear blocks. |
| `LogicAndBitOperation` | Relational, logical, bitwise, edge-detect, interval, and combinational-logic blocks. |
| `LookupTable` | One-dimensional, two-dimensional, and N-dimensional lookup tables. |
| `MathOperation` | Gain, sum, product, trigonometric, type conversion, reshape, and matrix/math functions. |
| `ModelVerification` | Assertion-style model checks. |
| `Port` | Inport and Outport boundary blocks. |
| `SignalRouting` | Bus, mux, demux, switch, goto/from, and vector routing blocks. |
| `SignalAttributes` | Rate and signal attribute conversion blocks. |
| `Sources` | Constants, steps, clocks, random sources, pulses, files, and workspace inputs. |
| `Sinks` | Signal logging and display sinks. |
| `SubSystems` | Subsystem, enable, trigger, iterator, if/switch-case, and function-call related blocks. |
| `StateMachine` | StateMachine Chart and related chart elements. |
| `Utilities` | Scopes, displays, files/workspace I/O, counters, byte/CAN helpers, and termination utilities. |

## Common Component Mapping

Sources:

| Need | Component | Main parameters |
|---|---|---|
| Step | `SysplorerEmbeddedCoder.Sources.Step` | `Time`, `Before`, `After` |
| Sine wave | `SysplorerEmbeddedCoder.Sources.SineWave` | `Amplitude`, `Frequency`, `Phase` |
| Ramp | `SysplorerEmbeddedCoder.Sources.Ramp` | `Slope`, `Start` |
| Pulse | `SysplorerEmbeddedCoder.Sources.PulseGenerator` | `Amplitude`, `Period_*`, `Width_*`, `Phase_*` |
| Constant | `SysplorerEmbeddedCoder.Sources.Constant` | `Value` |
| Random number | `SysplorerEmbeddedCoder.Sources.RandomNumber` | minimum/maximum settings |
| Clock | `SysplorerEmbeddedCoder.Sources.Clock` | none |

Math and logic:

| Need | Component | Main parameters |
|---|---|---|
| Gain | `SysplorerEmbeddedCoder.MathOperation.Gain` | `Gain` |
| Sum | `SysplorerEmbeddedCoder.MathOperation.Sum` | `Inputs`, for example `++-` |
| Product | `SysplorerEmbeddedCoder.MathOperation.Product` | `Inputs` |
| Abs | `SysplorerEmbeddedCoder.MathOperation.Abs` | none |
| Sqrt | `SysplorerEmbeddedCoder.MathOperation.Sqrt` | `Function` |
| Sign | `SysplorerEmbeddedCoder.MathOperation.Sign` | none |
| Relational comparison | `SysplorerEmbeddedCoder.LogicAndBitOperation.RelationalOperator` | `Operator` |
| Logical operation | `SysplorerEmbeddedCoder.LogicAndBitOperation.LogicalOperator` | `Operator`, `NumInputPorts` |
| Combinational logic | `SysplorerEmbeddedCoder.LogicAndBitOperation.CombinatorialLogic` | `TruthTable` |

Continuous/discrete:

| Need | Component | Main parameters |
|---|---|---|
| Integrator | `SysplorerEmbeddedCoder.Continuous.Integrator` | initial/limit settings |
| Derivative | `SysplorerEmbeddedCoder.Continuous.Derivative` | coefficient settings |
| Transfer function | `SysplorerEmbeddedCoder.Continuous.TransferFcn` | `Numerator`, `Denominator` |
| State space | `SysplorerEmbeddedCoder.Continuous.StateSpace` | `A`, `B`, `C`, `D`, `X0` |
| PID | `SysplorerEmbeddedCoder.Continuous.PIDController` or `DiscretePIDController` | controller gains and methods |
| Unit delay | `SysplorerEmbeddedCoder.Discrete.UnitDelay` | `InitialCondition`, `SampleTime` |
| Discrete transfer function | `SysplorerEmbeddedCoder.Discrete.DiscreteTransferFcn` | numerator/denominator/source settings |
| Zero-order hold | `SysplorerEmbeddedCoder.Discrete.ZeroOrderHold` | `SampleTime` |

Ports and observation:

| Need | Component |
|---|---|
| Model input | `SysplorerEmbeddedCoder.Port.Inport` |
| Model output | `SysplorerEmbeddedCoder.Port.Outport` |
| Scope | `SysplorerEmbeddedCoder.Utilities.Scope` |
| Display | `SysplorerEmbeddedCoder.Utilities.Display` |
| Workspace output | `SysplorerEmbeddedCoder.Utilities.ToWorkspace` |

Common control patterns:

- PI controller: `Step` setpoint -> `Sum("+-")` error -> parallel `Kp` gain and `Ki` gain plus `Integrator` -> `Sum("++")` PI output -> plant -> feedback.
- Motor speed control: setpoint -> `Sum("+-")` -> PI controller -> motor plant `K/(T*s + 1)` -> feedback. Typical starting values: `K=10 rpm/V`, `T=0.5 s`.
- Discrete PID: error -> `Kp`, `Ki` through discrete integrator, `Kd` through derivative/difference -> `Sum("++")`.

Recommended names:

| Role | Names |
|---|---|
| Reference | `setpoint`, `reference`, `ref` |
| Error | `error`, `err`, `error_sum` |
| Proportional gain | `Kp`, `Kp_gain` |
| Integral gain | `Ki`, `Ki_gain` |
| Derivative gain | `Kd`, `Kd_gain` |
| Controller | `controller`, `pid_ctrl` |
| Plant | `plant`, `system`, `motor` |
| Scope | `scope`, `monitor` |

Common simulation defaults: `StopTime=5.0`, `Interval=0.01`, `Solver=Euler`, `StartTime=0.0`. Common controller starting values: P `Kp=1.0`; PI `Kp=1.0`, `Ki=1.0`; PID `Kp=1.0`, `Ki=1.0`, `Kd=0.1`.

## Allowed Blocks

### Continuous

- `SysplorerEmbeddedCoder.Continuous.Derivative`
- `SysplorerEmbeddedCoder.Continuous.FirstOrderHold`
- `SysplorerEmbeddedCoder.Continuous.Integrator`
- `SysplorerEmbeddedCoder.Continuous.IntegratorLimited`
  - Editable: `ExternalResetType`, `InitCondSourceType`, `InitCond`, `LimitOutput`, `UpperSaturationLimit`, `LowerSaturationLimit`, `WrapState`, `UpperStateLimit`, `LowerStateLimit`, `ShowSaturationPort`, `ShowStatePort`, `IgnoreLimit`, `ZeroCross`.
  - Do not edit: `AbsoluteTolerance`.
  - Preconditions: set `LimitOutput=true` before `UpperSaturationLimit` and `LowerSaturationLimit`.
- `SysplorerEmbeddedCoder.Continuous.PIDController`
- `SysplorerEmbeddedCoder.Continuous.SecondOrderIntegrator`
- `SysplorerEmbeddedCoder.Continuous.SecondOrderIntegratorLimited`
  - Preconditions: set `XLimit=true` before `XUpperLimit` and `XLowerLimit`; set `DXDTLimit=true` before `DXDTUpperLimit` and `DXDTLowerLimit`.
- `SysplorerEmbeddedCoder.Continuous.StateSpace`
- `SysplorerEmbeddedCoder.Continuous.TransferFcn`
- `SysplorerEmbeddedCoder.Continuous.TransportDelay`
- `SysplorerEmbeddedCoder.Continuous.VariableTimeDelay`
- `SysplorerEmbeddedCoder.Continuous.VariableTransportDelay`
- `SysplorerEmbeddedCoder.Continuous.ZeroPole`

### Discontinuities

- `SysplorerEmbeddedCoder.Discontinuities.Backlash`
- `SysplorerEmbeddedCoder.Discontinuities.CoulombAndViscousFriction`
- `SysplorerEmbeddedCoder.Discontinuities.DeadZone`
  - Editable: `LowerValue`, `UpperValue`, `LinearizeAsGain`.
  - Do not edit: `ZeroCross`.
- `SysplorerEmbeddedCoder.Discontinuities.DeadZoneDynamic`
- `SysplorerEmbeddedCoder.Discontinuities.HitCrossing`
- `SysplorerEmbeddedCoder.Discontinuities.Quantizer`
- `SysplorerEmbeddedCoder.Discontinuities.RateLimiter`
- `SysplorerEmbeddedCoder.Discontinuities.RateLimiterDynamic`
- `SysplorerEmbeddedCoder.Discontinuities.Relay`
  - Editable: `OnSwitchValue`, `OffSwitchValue`, `OnOutputValue`, `OffOutputValue`, `ZeroCross`, `OutDataTypeStr`.
  - Do not edit: `OutMin`, `OutMax`.
- `SysplorerEmbeddedCoder.Discontinuities.Saturation`
  - Editable: `UpperLimit`, `LowerLimit`, `LinearizeAsGain`, `ZeroCross`, `OutDataTypeStr`.
  - Do not edit: `OutMin`, `OutMax`.
- `SysplorerEmbeddedCoder.Discontinuities.SaturationDynamic`
- `SysplorerEmbeddedCoder.Discontinuities.WrapToZero`

### Discrete

- `SysplorerEmbeddedCoder.Discrete.Delay`
  - Editable: `DelayLengthSource`, `InitialConditionSource`, `DelayLength`, `InitialCondition`, `ShowEnablePort`, `ExternalReset`, `SampleTime`.
  - Do not edit: `DelayLengthUpperLimit`.
- `SysplorerEmbeddedCoder.Discrete.Difference`
- `SysplorerEmbeddedCoder.Discrete.DiscreteDerivative`
- `SysplorerEmbeddedCoder.Discrete.DiscretePIDController`
- `SysplorerEmbeddedCoder.Discrete.DiscreteStateSpace`
- `SysplorerEmbeddedCoder.Discrete.DiscreteTimeIntegrator`
  - Editable: `IntegratorMethod`, `GainValue`, `ExternalReset`, `InitialConditionSource`, `InitialCondition`, `SampleTime`, `LimitOutput`, `ShowSaturationPort`, `ShowStatePort`, `IgnoreLimit`, `OutDataTypeStr`, `UpperSaturationLimit`, `LowerSaturationLimit`.
  - Do not edit: `OutMin`, `OutMax`.
  - Preconditions: set `LimitOutput=true` before `UpperSaturationLimit` and `LowerSaturationLimit`.
- `SysplorerEmbeddedCoder.Discrete.DiscreteTransferFcn`
  - Editable: `NumeratorSourceEdit`, `DenominatorSourceEdit`, `initStateSourceEdit`, `numeratorEdit`, `denominatorEdit`, `initStateEdit`, `ExternalReset`, `a0EqualsOne`, `SampleTime`, `OutDataTypeStr`.
  - Do not edit: `OutMin`, `OutMax`.
- `SysplorerEmbeddedCoder.Discrete.Memory`
- `SysplorerEmbeddedCoder.Discrete.TappedDelay`
- `SysplorerEmbeddedCoder.Discrete.TransferFcnFirstOrder`
- `SysplorerEmbeddedCoder.Discrete.TransferFcnLeadorLeg`
- `SysplorerEmbeddedCoder.Discrete.TransferFcnRealZero`
- `SysplorerEmbeddedCoder.Discrete.UnitDelay`
- `SysplorerEmbeddedCoder.Discrete.ZeroOrderHold`

### FlipFlops

- `SysplorerEmbeddedCoder.FlipFlops.DFlipFlop`
- `SysplorerEmbeddedCoder.FlipFlops.J_KFlipFlop`
- `SysplorerEmbeddedCoder.FlipFlops.S_RFlipFlop`

### LogicAndBitOperation

- `SysplorerEmbeddedCoder.LogicAndBitOperation.BitClear`
- `SysplorerEmbeddedCoder.LogicAndBitOperation.BitSet`
- `SysplorerEmbeddedCoder.LogicAndBitOperation.BitSlice`
- `SysplorerEmbeddedCoder.LogicAndBitOperation.BitToIntegerConverter`
- `SysplorerEmbeddedCoder.LogicAndBitOperation.BitwiseOperator`
  - Editable: `LogicOperator`, `UseBitMask`, `BitMask`, `NumInputPorts`.
  - Preconditions: set `UseBitMask=false` before `NumInputPorts`.
- `SysplorerEmbeddedCoder.LogicAndBitOperation.CombinatorialLogic`
- `SysplorerEmbeddedCoder.LogicAndBitOperation.CompareToConstant`
  - Editable: `Operator`, `ConstValue`, `OutDataTypeStr`.
  - Do not edit: `ZeroCross`.
- `SysplorerEmbeddedCoder.LogicAndBitOperation.CompareToZero`
  - Documented vs actual parameter: `relop -> Operator`.
- `SysplorerEmbeddedCoder.LogicAndBitOperation.DetectChange`
  - Documented vs actual parameter: `vinit -> InitialCondition`.
- `SysplorerEmbeddedCoder.LogicAndBitOperation.DetectDecrease`
  - Documented vs actual parameter: `vinit -> InitialCondition`.
- `SysplorerEmbeddedCoder.LogicAndBitOperation.DetectFallNegative`
  - Documented vs actual parameter: `vinit -> InitialCondition`.
- `SysplorerEmbeddedCoder.LogicAndBitOperation.DetectFallNonpositive`
  - Documented vs actual parameter: `vinit -> InitialCondition`.
- `SysplorerEmbeddedCoder.LogicAndBitOperation.DetectIncrease`
  - Documented vs actual parameter: `vinit -> InitialCondition`.
- `SysplorerEmbeddedCoder.LogicAndBitOperation.DetectRiseNonnegative`
  - Documented vs actual parameter: `vinit -> InitialCondition`.
- `SysplorerEmbeddedCoder.LogicAndBitOperation.DetectRisePositive`
  - Documented vs actual parameter: `vinit -> InitialCondition`.
- `SysplorerEmbeddedCoder.LogicAndBitOperation.ExtractBits`
- `SysplorerEmbeddedCoder.LogicAndBitOperation.FloatExtractBits`
- `SysplorerEmbeddedCoder.LogicAndBitOperation.IntegerToBitConverter`
- `SysplorerEmbeddedCoder.LogicAndBitOperation.IntervalTest`
  - Documented vs actual parameters: `uplimit -> UpperLimit`, `lowlimit -> LowerLimit`.
- `SysplorerEmbeddedCoder.LogicAndBitOperation.IntervalTestDynamic`
- `SysplorerEmbeddedCoder.LogicAndBitOperation.LogicalOperator`
  - Documented vs actual parameter: `Inputs -> NumInputPorts`.
- `SysplorerEmbeddedCoder.LogicAndBitOperation.RelationalOperator`
- `SysplorerEmbeddedCoder.LogicAndBitOperation.ShiftArithmetic`

### LookupTable

- `SysplorerEmbeddedCoder.LookupTable.LookupTable1D`
  - Batch parameters: verified `GetModelParamValues` / `SetModelParamValues` can write back `Table` and `BreakpointsForDimension1` as a group.
  - Editable: `Table`, `BreakpointsForDimension1`, `InterpMethod`, `ExtrapMethod`, `IndexSearchMethod`, `OutDataTypeStr`.
  - Verified insertion, write/readback, check, and simulation.
  - Known localized API enum values include `\u5747\u4e00`, `\u7ebf\u6027\u70b9-\u659c\u7387` for `InterpMethod`; `\u88c1\u526a`, `\u7ebf\u6027` for `ExtrapMethod`; `\u4e8c\u5206\u641c\u7d22` for `IndexSearchMethod`.
  - Table and breakpoint lengths must match the current dimension. Single-field dimension shortening may be rejected.
- `SysplorerEmbeddedCoder.LookupTable.LookupTable2D`
  - Batch parameters: verified `GetModelParamValues` / `SetModelParamValues` can write back `Table`, `BreakpointsForDimension1`, `BreakpointsForDimension2`, and interpolation method as a group.
  - Editable: `Table`, `BreakpointsForDimension1`, `BreakpointsForDimension2`, `InterpMethod`, `OutDataType`.
  - Verified insertion, write/readback, check, and simulation.
  - Known localized `InterpMethod` values include `\u5747\u4e00`, `\u6700\u90bb\u8fd1`. `ExtrapMethod` is currently not editable.
  - Table matrix shape must match both breakpoint dimensions. Shape changes may be rejected.
- `SysplorerEmbeddedCoder.LookupTable.LookupTableDynamic`
- `SysplorerEmbeddedCoder.LookupTable.LookupTableND`
  - Batch parameters: verified `GetModelParamValues` / `SetModelParamValues` can write back `N`, `Table`, `Axis1/2/3`, `InterpolationMethod`, and `ExtrapolationMethod` as a group.
  - Editable: `N`, `Table`, `Axis1`, `Axis2`, `Axis3`, `InterpolationMethod`, `ExtrapolationMethod`, `IndexSearchMethod`, `YType`.
  - Verified insertion, write/readback, check, and simulation.
  - Known localized values include `\u5747\u4e00`, `\u7ebf\u6027\u70b9-\u659c\u7387` for `InterpolationMethod`; `\u88c1\u526a` for `ExtrapolationMethod`; `\u4e8c\u5206\u641c\u7d22` for `IndexSearchMethod`.
  - After setting `N`, `Table` shape must match the axis lengths.

### MathOperation

- `SysplorerEmbeddedCoder.MathOperation.Abs`
- `SysplorerEmbeddedCoder.MathOperation.Bias`
- `SysplorerEmbeddedCoder.MathOperation.ComplexToMagnitudeAngle`
- `SysplorerEmbeddedCoder.MathOperation.ComplexToRealImag`
- `SysplorerEmbeddedCoder.MathOperation.dBGain`
- `SysplorerEmbeddedCoder.MathOperation.FindNonzeroElements`
- `SysplorerEmbeddedCoder.MathOperation.Gain`
- `SysplorerEmbeddedCoder.MathOperation.IsTriangular`
- `SysplorerEmbeddedCoder.MathOperation.MathFunction`
  - Editable: `Operator`.
  - Do not edit: `AlgorithmType`, `SignedPower`, `Iterations`.
- `SysplorerEmbeddedCoder.MathOperation.MagnitudeAngleToComplex`
- `SysplorerEmbeddedCoder.MathOperation.Matrix.AdjointOf3x3Matrix`
- `SysplorerEmbeddedCoder.MathOperation.Matrix.Create3x3Matrix`
- `SysplorerEmbeddedCoder.MathOperation.Matrix.CreateDiagonalMatrix`
- `SysplorerEmbeddedCoder.MathOperation.Matrix.CrossProduct`
- `SysplorerEmbeddedCoder.MathOperation.Matrix.Det3x3`
- `SysplorerEmbeddedCoder.MathOperation.Matrix.DotProduct`
- `SysplorerEmbeddedCoder.MathOperation.Matrix.ExtractDiagonal`
- `SysplorerEmbeddedCoder.MathOperation.Matrix.IdentityMatrix`
  - Editable: `Inherit`, `OutputDimensions`, `OutDataTypeStr`.
  - Do not edit: `SampleTime`.
- `SysplorerEmbeddedCoder.MathOperation.Matrix.Invert3x3Matrix`
- `SysplorerEmbeddedCoder.MathOperation.Matrix.MatrixSquare`
- `SysplorerEmbeddedCoder.MathOperation.Matrix.PermuteMatrix`
- `SysplorerEmbeddedCoder.MathOperation.Matrix.SubMatrix`
- `SysplorerEmbeddedCoder.MathOperation.Maxmin`
- `SysplorerEmbeddedCoder.MathOperation.MinMaxRunningResettable`
- `SysplorerEmbeddedCoder.MathOperation.Polynomial`
- `SysplorerEmbeddedCoder.MathOperation.Product`
- `SysplorerEmbeddedCoder.MathOperation.Quaternion.QuaternionConjugate`
- `SysplorerEmbeddedCoder.MathOperation.Quaternion.QuaternionInterpolation`
  - Documented vs actual parameter: `method -> Method`.
- `SysplorerEmbeddedCoder.MathOperation.Quaternion.QuaternionDivision`
- `SysplorerEmbeddedCoder.MathOperation.Quaternion.QuaternionInverse`
- `SysplorerEmbeddedCoder.MathOperation.Quaternion.QuaternionModulus`
- `SysplorerEmbeddedCoder.MathOperation.Quaternion.QuaternionMultiplication`
- `SysplorerEmbeddedCoder.MathOperation.Quaternion.QuaternionNorm`
- `SysplorerEmbeddedCoder.MathOperation.Quaternion.QuaternionNormalize`
- `SysplorerEmbeddedCoder.MathOperation.Quaternion.QuaternionRotation`
- `SysplorerEmbeddedCoder.MathOperation.RealImagToComplex`
- `SysplorerEmbeddedCoder.MathOperation.ReciprocalSqrt`
  - Editable: `Function`, `OutDataTypeStr`, `SaturateOnIntegerOverflow`.
  - Do not edit: `OutMin`, `OutMax`, `RoundType`.
- `SysplorerEmbeddedCoder.MathOperation.Reshape`
  - Editable: `OutputDimensionality`, `OutputDimensions`.
  - Preconditions: set `OutputDimensionality=\u81ea\u5b9a\u4e49` before `OutputDimensions`.
- `SysplorerEmbeddedCoder.MathOperation.RMS`
- `SysplorerEmbeddedCoder.MathOperation.RoundingFunction`
- `SysplorerEmbeddedCoder.MathOperation.Sign`
- `SysplorerEmbeddedCoder.MathOperation.SignedSqrt`
  - Editable: `Function`, `OutDataTypeStr`, `SaturateOnIntegerOverflow`.
  - Do not edit: `OutMin`, `OutMax`, `RoundType`.
- `SysplorerEmbeddedCoder.MathOperation.SineWaveFunction`
  - Editable: `SineType`, `TimeSource`, `Amplitude`, `Bias`, `Frequency`, `Phase`, `Samples`, `Offset`.
  - Do not edit: `SampleTime`.
  - Preconditions: set `SineType=\u57fa\u4e8e\u91c7\u6837` before `Samples` and `Offset`.
- `SysplorerEmbeddedCoder.MathOperation.Sqrt`
  - Editable: `Function`, `OutDataTypeStr`, `SaturateOnIntegerOverflow`.
  - Do not edit: `OutMin`, `OutMax`, `RoundType`.
- `SysplorerEmbeddedCoder.MathOperation.Squeeze`
- `SysplorerEmbeddedCoder.MathOperation.Sum`
  - Editable: `Inputs`, `OutDataTypeStr`, `SaturateOnIntegerOverflow`.
  - Do not edit: `OutMin`, `OutMax`.
- `SysplorerEmbeddedCoder.MathOperation.TrigonometricFunction`
- `SysplorerEmbeddedCoder.MathOperation.TypeConversion`
  - Editable: `OutDataTypeStr`, `IsSaturate`.
  - Do not edit: `OutMin`, `OutMax`.
- `SysplorerEmbeddedCoder.MathOperation.UnaryMinus`
  - Editable: none.
  - Do not edit: `SaturateOnIntegerOverflow`, `SampleTime`.
- `SysplorerEmbeddedCoder.MathOperation.WeightedSampleTimeMath`

### ModelVerification

- `SysplorerEmbeddedCoder.ModelVerification.Assertion`

### Port

- `SysplorerEmbeddedCoder.Port.Inport`
  - Editable: `OutDataTypeStr`, `Dimension`, `SampleTime`.
  - Do not edit: `OutMin`, `OutMax`, `InputPartition`, `PartitionDimension`, `PartitionWidth`, `PartitionOffset`.
- `SysplorerEmbeddedCoder.Port.Outport`
  - In Sysplorer 2026b, `GetComponentPorts(..., 0)` may return `[]`; this is valid for this boundary block.
  - Connect an incoming signal to the component name, for example `ConnectPort(model, "chart.mode", "mode_out")`, not `mode_out.u`.
  - Default parameters include `Dimension=-1` and `OutDataTypeStr=Inherit: auto`; direct real, `int32`, and `boolean` sources are accepted under inherited typing.

### SignalAttributes

- `SysplorerEmbeddedCoder.SignalAttributes.DownSample`
- `SysplorerEmbeddedCoder.SignalAttributes.RateTransition`
- `SysplorerEmbeddedCoder.SignalAttributes.WeightedSampleTime`
- `SysplorerEmbeddedCoder.SignalAttributes.Width`

### SignalRouting

- `SysplorerEmbeddedCoder.SignalRouting.BusToVector`
- `SysplorerEmbeddedCoder.SignalRouting.DataStoreMemory`
- `SysplorerEmbeddedCoder.SignalRouting.DataStoreRead`
- `SysplorerEmbeddedCoder.SignalRouting.DataStoreWrite`
- `SysplorerEmbeddedCoder.SignalRouting.DeMux`
- `SysplorerEmbeddedCoder.SignalRouting.GotoTagVisibility`
- `SysplorerEmbeddedCoder.SignalRouting.ManualSwitch`
- `SysplorerEmbeddedCoder.SignalRouting.MultiportSwitch`
  - Editable: `DataPortOrder`, `Inputs`, `DataPortIndices`, `DataPortForDefault`, `OutDataTypeStr`, `AllowDiffInputSizes`.
  - Preconditions: set `DataPortOrder=\u6307\u5b9a\u7d22\u5f15` before `DataPortIndices`.
- `SysplorerEmbeddedCoder.SignalRouting.Mux`
- `SysplorerEmbeddedCoder.SignalRouting.Switch`
- `SysplorerEmbeddedCoder.SignalRouting.VectorConcatenate`

### StateMachine

- `SysplorerEmbeddedCoder.StateMachine.Chart`
  - Current Sysblock supports StateMachine modeling. Create Charts with `AddComponent("SysplorerEmbeddedCoder.StateMachine.Chart", model, name, x, y, w, h)`.
  - Create and edit internal states, transitions, data, events, and junctions through StateMachine element APIs. Do not directly edit `.mo` text.

### Sinks

- `SysplorerEmbeddedCoder.Sinks.AveragingPowerSpectralDensity`
- `SysplorerEmbeddedCoder.Sinks.PowerSpectralDensity`

### Sources

- `SysplorerEmbeddedCoder.Sources.BandLimitedWhiteNoise`
- `SysplorerEmbeddedCoder.Sources.BernoulliBinaryGenerator`
- `SysplorerEmbeddedCoder.Sources.ChirpSignal`
- `SysplorerEmbeddedCoder.Sources.Clock`
- `SysplorerEmbeddedCoder.Sources.Constant`
- `SysplorerEmbeddedCoder.Sources.CounterFreeRunning`
- `SysplorerEmbeddedCoder.Sources.CounterLimited`
- `SysplorerEmbeddedCoder.Sources.DigitalClock`
- `SysplorerEmbeddedCoder.Sources.DiscretePulseGenerator`
  - Preconditions: set `PulseType=\u57fa\u4e8e\u65f6\u95f4` before `Period_time`, `Width_time`, and `Phase_time`.
- `SysplorerEmbeddedCoder.Sources.FromFile`
- `SysplorerEmbeddedCoder.Sources.FromWorkspace`
- `SysplorerEmbeddedCoder.Sources.Ground`
- `SysplorerEmbeddedCoder.Sources.PoissonIntegerGenerator`
- `SysplorerEmbeddedCoder.Sources.PulseGenerator`
  - Editable: `PulseType`, `TimeSource`, `Amplitude`, `Period_time`, `Width_time`, `Phase_time`, `Period_Sample`, `Width_sample`, `Phase_sample`, `Sample_Time`.
  - Preconditions: set `PulseType=\u57fa\u4e8e\u91c7\u6837` before `Period_Sample`, `Width_sample`, `Phase_sample`, and `Sample_Time`.
- `SysplorerEmbeddedCoder.Sources.RandomIntegerGenerator`
- `SysplorerEmbeddedCoder.Sources.RandomNumber`
- `SysplorerEmbeddedCoder.Sources.Ramp`
  - Documented vs actual parameters: `slope -> Slope`, `start -> Start`.
- `SysplorerEmbeddedCoder.Sources.RepeatingSequence`
  - Documented vs actual parameters: `rep_seq_t -> TimeEdit`, `rep_seq_y -> ValueEdit`.
- `SysplorerEmbeddedCoder.Sources.RepeatingSequenceInterpolated`
- `SysplorerEmbeddedCoder.Sources.RepeatingSequenceStair`
- `SysplorerEmbeddedCoder.Sources.SineWave`
  - Editable: `SineType`, `TimeSource`, `Amplitude`, `Bias`, `Frequency`, `Phase`, `SampleTime`, `Samples`, `Offset`.
  - Preconditions: set `SineType=\u57fa\u4e8e\u91c7\u6837` before `Samples` and `Offset`.
  - Note: `SetModelParamValue` return value is unreliable; confirm by readback.
- `SysplorerEmbeddedCoder.Sources.Step`
- `SysplorerEmbeddedCoder.Sources.UniformRandomNumber`

### SubSystems

- `SysplorerEmbeddedCoder.SubSystems.ActionPort`
  - Use only in a subsystem context, not as an ordinary root-model block.
- `SysplorerEmbeddedCoder.SubSystems.ForIterator`
- `SysplorerEmbeddedCoder.SubSystems.If`
  - Documented vs actual parameters: `NumInputs -> InputNum`, `ElseIfExpressions -> ElseifExpression`, `ShowElse -> ShowElsePort`.
- `SysplorerEmbeddedCoder.SubSystems.SampleAndHold`
- `SysplorerEmbeddedCoder.SubSystems.SwitchCase`
  - Documented vs actual parameter: `CaseConditions -> CaseCondition`.
- `SysplorerEmbeddedCoder.SubSystems.WhileIterator`
  - Use only in a subsystem context, not as an ordinary root-model block.

### Utilities

- `SysplorerEmbeddedCoder.Utilities.BytePack`
- `SysplorerEmbeddedCoder.Utilities.ByteUnpack`
- `SysplorerEmbeddedCoder.Utilities.Counter`
- `SysplorerEmbeddedCoder.Utilities.Display`
  - Editable: none.
  - Do not edit: `Format`.
- `SysplorerEmbeddedCoder.Utilities.ExternalInport`
- `SysplorerEmbeddedCoder.Utilities.ExternalOutport`
- `SysplorerEmbeddedCoder.Utilities.Fcn`
- `SysplorerEmbeddedCoder.Utilities.Merge`
- `SysplorerEmbeddedCoder.Utilities.Scope`
- `SysplorerEmbeddedCoder.Utilities.StopSimulation`
- `SysplorerEmbeddedCoder.Utilities.Terminator`
- `SysplorerEmbeddedCoder.Utilities.ToFile`
- `SysplorerEmbeddedCoder.Utilities.ToWorkspace`

## Prohibited Blocks

### SignalRouting

- `SysplorerEmbeddedCoder.SignalRouting.From`
  - Do not edit: `GotoTag`.
- `SysplorerEmbeddedCoder.SignalRouting.Goto`
  - Do not edit: `GotoTag`, `TagVisibility`.

### Sources And StateMachine

- `SysplorerEmbeddedCoder.Sources.SignalBuilder`
  - Current Sysblock MCP cannot set this block correctly.
- `SysplorerEmbeddedCoder.StateMachine.GraphFunction`
  - Current Sysblock StateMachine does not support graph functions.
- `SysplorerEmbeddedCoder.StateMachine.HistoryJunction`
  - Current Sysblock StateMachine does not support history junctions.
- `SysplorerEmbeddedCoder.StateMachine.SysblockState`
  - Current Sysblock StateMachine does not support SysblockState.
- `SysplorerEmbeddedCoder.StateMachine.TruthTable`
  - Current Sysblock StateMachine does not support truth tables.

### Utilities

- `SysplorerEmbeddedCoder.Utilities.CANFDPack`
- `SysplorerEmbeddedCoder.Utilities.CANFDUnpack`
- `SysplorerEmbeddedCoder.Utilities.CANPack`
- `SysplorerEmbeddedCoder.Utilities.CANUnpack`
- `SysplorerEmbeddedCoder.Utilities.CFunction`
- `SysplorerEmbeddedCoder.Utilities.CCaller`
  - Current Sysblock MCP can parse some function prototypes but cannot complete external `.c` source registration and simulation closure. Do not use as a modeling block.
- `SysplorerEmbeddedCoder.Utilities.JuliaFunction`
- `SysplorerEmbeddedCoder.Utilities.JuliaObject`

The other prohibited utility blocks are unavailable because the current Sysblock MCP cannot set their function correctly.

## Conditional Blocks

Use these only when necessary and after accepting the listed limits.

### SignalRouting

- `SysplorerEmbeddedCoder.SignalRouting.BusCreator`
  - Batch parameters: full read, field read, and port readback are verified. `SetModelParamValues` blocks even when writing only `ShowSignalNames`; do not use batch write for now.
  - Current insertion and port readback work. `InputsNum` through `SetModelParamValue` may block; validate separately before changing input count.
- `SysplorerEmbeddedCoder.SignalRouting.BusSelector`
  - Batch parameters: insertion and port readback are verified. Full `GetModelParamValues` blocks in the minimum test scenario; field read returns empty with no bus or a simple `BusCreator` context, so do not use it as parameter-configuration evidence.
  - Signal-selection configuration must be validated in the real bus context.
- `SysplorerEmbeddedCoder.SignalRouting.Selector`
  - Do not edit: `IndexMode`, `InputPortWidth`, `NumberOfDimensions`, `IndexOptions`, `Indices`, `OutputSizes`.

### SubSystems

- `SysplorerEmbeddedCoder.SubSystems.Enable`
  - Do not edit: `StatesWhenEnabling`.
- `SysplorerEmbeddedCoder.SubSystems.ForEach`
  - Do not edit: `SpecifiedNumIters`.
- `SysplorerEmbeddedCoder.SubSystems.FunctionCallGenerator`
  - Documented vs actual parameters: `sample_time -> SampleTime`, `numberOfIterations -> NumberOfIterations`.
  - Do not edit: `DisallowWideOutput`.
  - Preconditions: set `ShowEnablePort=false` before `SampleTime`.
- `SysplorerEmbeddedCoder.SubSystems.SubSystem`
  - Batch parameters: full read, field read, batch write, and field readback are verified.
  - `ShowPortLabels` uses enum values such as `PortName`, `PortNumber`, `SignalName`; do not write booleans.
  - `TreatAsAtomicUnit` and `SystemSampleTime` may be written back with the full object.
  - After writing back `TreatAsAtomicUnit=true`, `FunctionPackType`, `FunctionName`, and `FunctionFile` are editable.
  - `FunctionPackType` values: `auto`, `inline`, `nonreusable`, `reusable`.
- `SysplorerEmbeddedCoder.SubSystems.Trigger`
  - Do not edit: `TriggerType`.

### StateMachine

- `SysplorerEmbeddedCoder.StateMachine.DefaultTransition`
  - Not an ordinary Sysblock block. Do not add directly with `AddComponent`; create through StateMachine element APIs.
- `SysplorerEmbeddedCoder.StateMachine.Junction`
  - Not an ordinary Sysblock block. Create through StateMachine element APIs only when junction semantics are required, not for cosmetic layout.
- `SysplorerEmbeddedCoder.StateMachine.State`
  - Not an ordinary Sysblock block. Do not add directly with `AddComponent`; create through StateMachine element APIs.

## Batch Parameter APIs

Use `GetModelParamValues(model, block[, fields])` and `SetModelParamValues(model, block, params)` for blocks with linked fields.

Rules:

- Read the full parameter object first, copy it, modify fields, write it back, and then read fields back to confirm.
- When `fields` is provided, the return value is a `dict`. Except for disabled `CCaller`, verified full reads are also treated as `dict`.
- Do not judge structural or context-dependent parameters as usable only because an API returns success. Combine with port readback, `CheckModel`, or a real-context validation.
- `SetModelParamValues` is not a topology-edit API. Adding/removing blocks, wiring, and port-count changes must still use modeling APIs and obey this block reference.

Recommended pattern:

```python
cfg = ModelingPy.GetModelParamValues(model, block)
cfg["Table"] = "{0, 10, 20, 30, 40}"
cfg["BreakpointsForDimension1"] = "{0, 1, 2, 3, 4}"
ok = ModelingPy.SetModelParamValues(model, block, cfg)
after = ModelingPy.GetModelParamValues(model, block, ["Table", "BreakpointsForDimension1"])
```
