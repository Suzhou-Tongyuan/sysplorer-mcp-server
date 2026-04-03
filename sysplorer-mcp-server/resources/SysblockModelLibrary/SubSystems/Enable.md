# Enable

将使能端口添加到子系统或模型


- **库：** Sysblock / Subsystems


<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SubSystems/enable/enable.png')" style="width: 150px; height: auto; transform: scale(1);">


## 描述

Enable 模块允许外部信号控制子系统或模型的执行。要启用此功能，可在 Subsystem 模块中添加该模块，或在 Model 模块所引用模型的根级别添加该模块。

如果在模型的根级别使用使能端口：

- 对于多速率模型，请将求解器设置为单任务。
- 对于具有定步长的模型，模型中有至少一个模块必须以指定的定步长速率运行。

## 示例

示例，使用一个 sineWave 模块输出正弦波，然后使用一个 SubSystem 模块，里面放入 Enable 模块，连接输入，SubSystem 模块只输出大于 0 的部分。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SubSystems/Enable1.mo">Enable.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SubSystems/enable/enable01.png')" style="width:600px">

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SubSystems/enable/enable02.png')" style="width:600px">

## 端口

### 输出

<div class="details-box">
<details open>
<summary>Enable signal — 子系统或模型的外部使能信号<div>标量</div></summary>
</details>
<div class="details-content">

使能信号从外部连接到 Enabled Subsystem 模块的外部，并传递到子系统的内部。当您选择**显示输出端口**参数时，使能信号端口将添加到 Enable 模块。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | Boolean | fixed point | expression

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>启用时的状态 — 选择当禁用的子系统或模型被激活时要采用的模块状态<div>保持（默认）| 重置</div></summary>
</details>
<div class="details-content">

对于处于禁用状态的 Subsystem 模块或 Model 模块，选择在激活这些模块时其所含模块的状态变化情况。

- **保持**

  按其先前值保持模块状态。

- **重置**

  将模块状态重置为其初始条件（如果未定义，则为零）。

</div>
</div>


<!-- 
#### 编程用法

| **模块参数：**`StatesWhenEnabling` |
| ---------------------------------- |
| **类型：**字符向量                 |
| **值**：`'held'` | `'reset'`       |
| **默认值：**`'held'`               | -->


<!-- 暂无
### 传播可变大小信号的大小 — 选择何时传播可变大小信号 “仅在启用时” （默认） | “执行期间”





选择何时传播可变大小信号。

- “`仅在启用时`”

  当重新启用包含 Enable 端口模块的 Subsystem 模块或 Model 模块时，传播可变大小的信号。如果您选择此选项，采样时间必须为周期性采样时间。

- “`执行期间`”

  在每个时间步传播可变大小的信号。

#### 编程用法

| **模块参数：**`PropagateVarSize`                      |
| ----------------------------------------------------- |
| **类型：**字符向量                                    |
| **值**：`'Only when enabling'` | `'During execution'` |
| **默认值：**`'Only when enabling'`                    | -->


<!-- 暂无
### 显示输出端口 — 控制使能信号的输出端口的显示 off （默认） | on





输出端口将 Enabled Subsystem 模块或激活的 Model 模块的外接使能信号传递到内部。

- ![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/off_check_box.gif) off

  在 Enable 端口模块上删除输出端口。

- ![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/on_check_box.gif) on

  在 Enable 端口模块上显示输出端口。选择此选项将允许子系统或模型处理使能信号。

#### 编程用法

| **模块参数：**`ShowOutputPort` |
| ------------------------------ |
| **类型：**字符向量             |
| **值：**`'off'` | `'on'`       |
| **默认值：**`'off'`            | -->


<!-- 暂无
### 启用过零检测 — 控制过零检测 on （默认） | off





控制模型的过零检测。

- ![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/on_check_box.gif) on

  检测过零点。

- ![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/off_check_box.gif) off

  不检测过零点。

#### 编程用法

| **模块参数：**`ZeroCross` |
| ------------------------- |
| **类型：**字符向量        |
| **值：** `'on'` | `'off'` |
| **默认值：**`'on'`        | -->


<!-- 暂无
### 端口维度 — 指定使能信号的维度 1 （默认） | [n] | [m n]





指定从外部连接到 Model 模块并传递到模块内部的使能信号的维度。

- `1`

  标量信号。

- `[n]`

  宽度为 `n` 的向量信号。

- `[m n]`

  具有 `m` 行和 `n` 列的矩阵信号。

#### 编程用法

| **模块参数：**`PortDimensions`      |
| ----------------------------------- |
| **类型：**字符向量                  |
| **值**：`'1'` | `'[n]'` | `'[m n]'` |
| **默认值：**`'1'`                   | -->


<!-- 暂无
### 采样时间 — 指定时间间隔 -1 （默认） | Ts | [Ts, To]





指定模块方法执行之间的时间间隔。请参阅[指定采样时间](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/how-to-specify-the-sample-time.html)。

- `-1`

  从模型继承采样时间。

- `Ts`

  标量，其中 Ts 是时间间隔。

- `[Ts, To]`

  向量，其中 Ts 是时间间隔，To 是初始时间偏移量。

#### 编程用法

| **模块参数：**`SampleTime`            |
| ------------------------------------- |
| **类型：**字符向量                    |
| **值**：`'-1'` | `'Ts'`| `'[Ts, To]'` |
| **默认值：**`'-1'`                    | -->


<!-- 暂无
### 最小值 — 指定使能信号的最小输出值 [] （默认） | 实数标量





指定从外部连接到 Model 模块并传递到模块内部的使能信号的最小值。

Simulink® 使用此值来执行：

- 仿真范围检查。请参阅[指定信号范围](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/signal-ranges.html)。
- 定点数据类型的自动定标。
- 所生成代码的优化。此优化可删除算法代码，并影响某些仿真模式（如 SIL 或外部模式）的结果。请参阅[Optimize using the specified minimum and maximum values](https://ww2.mathworks.cn/help/releases/R2022b/ecoder/ref/optimizeusingthespecifiedminimumandmaximumvalues.html) (Embedded Coder)。



- `[]`

  不指定最小值。

- 实数标量

  实数双精度标量值。

#### 编程用法

| **模块参数：**`OutMin`             |
| ---------------------------------- |
| **类型：**字符向量                 |
| **值**：`'[]'` | `'<real scalar>'` |
| **默认值：**`'[]'`                 | -->


<!-- 暂无
### 最大值 — 指定使能信号的最大输出值 [] （默认） | 实数标量





指定从外部连接到 Model 模块并传递到模块内部的使能信号的最大值。

Simulink 使用此值来执行：

- 仿真范围检查。请参阅[指定信号范围](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/signal-ranges.html)。
- 定点数据类型的自动定标。
- 所生成代码的优化。此优化可删除算法代码，并影响某些仿真模式（如 SIL 或外部模式）的结果。请参阅[Optimize using the specified minimum and maximum values](https://ww2.mathworks.cn/help/releases/R2022b/ecoder/ref/optimizeusingthespecifiedminimumandmaximumvalues.html) (Embedded Coder)。



- `[]`

  不指定最大值。

- 实数标量

  实数双精度标量值。

#### 编程用法

| **模块参数：**`OutMax`             |
| ---------------------------------- |
| **类型：**字符向量                 |
| **值**：`'[]'` | `'<real scalar>'` |
| **默认值：**`'[]'`                 | -->


<!-- 暂无
### 数据类型 — 指定使能信号的输出数据类型 “`double`” （默认） | “`single`” | “`int8`” | “`uint8`” | “`int16`” | “`uint16`” | “`int32`” | “`uint32`” | “`int64`” | “`uint64`” | “`boolean`” | “`fixdt(1,16)`” | “`fixdt(1,16,0)`” | “`fixdt(1,16,2^,0)`” | “`<data type expression>`”





指定从外部连接到 Model 模块并传递到模块内部的使能信号的数据类型。

- “`double`”

  双精度浮点。

- “`single`”

  单精度浮点。

- “`int8`”

  有符号 8 位整数。

- “`uint8`”

  无符号 8 位整数。

- “`int16`”

  有符号 16 位整数。

- “`uint16`”

  无符号 16 位整数。

- “`int32`”

  有符号 32 位整数。

- “`uint32`”

  无符号 32 位整数。

- “`int64`”

  有符号 64 位整数。

- “`uint64`”

  无符号 64 位整数。

- “`boolean`”

  值为 `true` 或 `false` 的布尔值。

- “`fixdt(1,16)`”

  未定义二进制小数点位置的有符号 16 位定点数。

- “`fixdt(1,16,0)`”

  二进制小数点位置设置为零的有符号 16 位定点数。

- “`fixdt(1,16,2^,0)`”

  斜率设置为 `2^0` 且偏置设置为 `0` 的有符号 16 位定点数。

- “`<data type expression>`”

  数据类型对象，例如 `Simulink.NumericType`。您不能以数据类型表达式的形式输入 [`Simulink.Bus`](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/simulink.bus.html) 对象的名称。

#### 编程用法

| **模块参数：**`OutDataTypeStr`                               |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值**：`'double'` | `'single'` | `'int8'` | `'uint8'` | `'int16'` | `'uint16'` | `'int32'` | `'uint32'` | `'int64'` | `'uint64'` | `'boolean'` | `'<fixdt(1,16)'` | `'fixdt(1,16,0)'` | `'fixdt(1,16,2^0,0)'` | `'<data type expression>'` |
| **默认值：**`'double'`                                       | -->

<!-- 暂无
### 模式 — 选择数据类型类别 “内置” （默认） | “定点” | “表达式”





选择数据类型类别并显示下拉列表以帮助您定义数据类型。

- “`内置`”

  显示数据类型和“数据类型覆盖”的下拉列表。

- “`定点`”

  显示“符号性”、“定标”和“数据类型覆盖”的下拉列表。

- “`表达式`”

  显示用于输入表达式的文本框。

#### 依存关系

要启用此参数，请选择“显示数据类型助手”按钮。

#### 编程用法 

没有等效的命令行参数。-->


<!-- 暂无
### 数据插值 — 指定缺失的工作区数据的值 on （默认） | off

指定从工作区加载数据时缺失的工作区数据的值。

- ![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/on_check_box.gif) on

  在不存在对应工作区数据的时间步上对输出进行线性插值。

- ![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/off_check_box.gif) off

  不在时间步处进行输出插值。取存在数据的最近时间步上的输出作为当前输出。

#### 编程用法

| **模块参数：**`Interpolate` |
| --------------------------- |
| **类型：**字符向量          |
| **值：** `'on'` | `'off'`   |
| **默认值：**`'on'`          | -->


<!-- 
## 模型示例

[![Enabled Subsystems](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink_features/win64/EnabledSubsystemsExample_01.png)Enabled SubsystemsWhat happens when a sine wave is fed into an enabled subsystem. After running the simulation, the scope shows three plots.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/enabled-subsystems.html)

[![Advanced Enabled Subsystems](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink_features/win64/AdvancedEnabledSubsystemsExample_03.png)Advanced Enabled SubsystemsWhat happens when a sine wave is fed into an enabled subsystem. The four subsystems in the model contain integrators, either discrete or continuous as described by the subsystem name. After running the simulation, the two scopes show the results for the discrete enabled subsystems (top scope) and continuous enabled subsystems (bottom scope).](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/advanced-enabled-subsystems.html)

[![Illustration of Law of Large Numbers](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink_features/win64/IllustrationOfLawOfLargeNumbersExample_01.png)Illustration of Law of Large NumbersUse MATLAB System blocks to illustrate the law of large numbers.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/illustration-of-law-of-large-numbers.html)

[![Counters Using Conditionally Executed Subsystems](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink_general/win64/sldemo_countersExample_02.png)Counters Using Conditionally Executed SubsystemsThe contrast between enabled subsystems and triggered subsystems for the same control signal, through the use of counter circuits. After running the simulation, the scope shows three plots.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/counters-using-conditionally-executed-subsystems.html)

[![Merging Signals](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink_features/win64/MergingSignalsExample_01.png)Merging SignalsUse conditionally executed subsystems and the Merge block to combine two inputs into a single output.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/merging-signals.html)

[![Building a Clutch Lock-Up Model](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink_automotive/win64/BuildingAClutchLockUpModelExample_07.png)Building a Clutch Lock-Up ModelUse Simulink® to model and simulate a rotating clutch system. Although modeling a clutch system is difficult because of topological changes in the system dynamics during lockup, this example shows how Simulink's enabled subsystems easily handle such problems. We illustrate how to employ important Simulink modeling concepts in the creation of the clutch simulation. Designers can apply these concepts to many models with strong discontinuities and constraints that may change dynamically.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/building-a-clutch-lock-up-model.html) -->


<!-- 暂无
## 模块特性

| **数据类型**     | `Boolean` | `double` | `fixed point` | `integer` | `single` |
| ---------------- | ----------------------------------------------------------- |
| **直接馈通**     | `否`                                                        |
| **多维信号**     | `是`                                                        |
| **可变大小信号** | `否`                                                        |
| **过零检测**     | `是`                                                        | -->

<!-- ## 扩展功能 -->

<!-- 
### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 Verilog 代码和 VHDL 代码。



HDL Coder™ 提供影响 HDL 实现和综合逻辑的额外配置选项。

**HDL 架构**

此模块具有一个默认 HDL 架构。

**HDL 模块属性**

| **ConstrainedOutputPipeline** | 通过移动设计中现有延迟的方式来放置在输出端的寄存器的数量。分布式流水线处理不会重新分发这些寄存器。默认值为 `0`。有关详细信息，请参阅[ConstrainedOutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#btp8gmp) (HDL Coder)。 |
| ----------------------------- | ------------------------------------------------------------ |
| **InputPipeline**             | 要在生成的代码中插入的输入流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 `0`。有关详细信息，请参阅[InputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-25) (HDL Coder)。 |
| **OutputPipeline**            | 要在生成的代码中插入的输出流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 `0`。有关详细信息，请参阅[OutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-26) (HDL Coder)。 |



### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。 -->

## 版本历史记录

- 在 2024b 之前推出

### 限制信息
不支持部分
1. 参数-传播可变大小信号的大小 — 选择何时传播可变大小信号
2. 参数-显示输出端口 — 控制使能信号的输出端口的显示
3. 参数-启用过零检测 — 控制过零检测
4. 参数-端口维度 — 指定使能信号的维度
5. 参数-采样时间 — 指定时间间隔
6. 参数-最小 — 指定使能信号的最小输出值
7. 参数-最大 — 指定使能信号的最大输出值
8. 参数-数据类型 — 指定使能信号的输出数据类型
9. 参数-模式 — 选择数据类型类别
10. 参数-数据插值 — 指定缺失的工作区数据的值

## 另请参阅

[Subsystem](Subsystem.html) 


<!-- - [条件执行子系统概述](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/about-conditional-subsystems.html)
- [使用使能子系统](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/enabled-subsystems.html)
- [使用使能触发子系统](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/triggered-and-enabled-subsystems.html) -->