# PulseGenerator
---
按固定间隔生成方波脉冲

**库：** Sysblock模块库 / Sources

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/PulseGenerator/PulseGenerator.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

PulseGenerator 模块按固定间隔生成方波脉冲。此模块的波形参数**振幅**、**脉冲宽度**、**周期**和**相位延迟**确定了输出波形的形状。

<!-- 下图说明了每个参数对波形的影响。

![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/pulse_generator_parameter_effects.png) -->

PulseGenerator 模块可以生成任何实数数据类型的标量、向量或矩阵信号。要生成标量信号，请使用标量指定波形参数。要生成向量或矩阵信号，请分别使用向量或矩阵指定波形参数。波形参数的每个元素会影响输出信号的对应元素。例如，幅值向量参数的第一个元素确定输出脉冲向量的第一个元素的幅值。进行标量扩展后，所有波形参数必须具有相同的维度。输出的数据类型与**振幅**参数的数据类型相同。

可以在基于时间或基于采样的模式下生成模块输出，具体情况由**脉冲类型**参数确定。

### 基于时间的模式

在基于时间的模式下，Sysblock 仅在输出实际发生变化时才计算模块输出。采用此方法，在仿真时间周期内为求取模块输出而进行的计算量较少。通过将**脉冲类型**参数设置为“基于时间”可以激活此模式。

此模块不支持产生常量输出信号的基于时间的配置。如果参数**脉冲宽度**和**周期**满足下列任一条件，Sysblock 将返回错误：

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/PulseGenerator/PulseGenerator01.png')" style="width: 200px; height: auto; transform: scale(1);">

根据脉冲波形特征，模块输出发生变化的时间间隔可能不同。由于这个原因，基于时间的 PulseGenerator 模块具有可变的采样时间。

<!-- 此类模块的采样时间颜色是褐色的（有关详细信息，请参阅[查看采样时间信息](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/how-to-view-sample-time-information.html)）。 -->

<!-- Sysblock 不能使用定步长求解器来计算基于时间的脉冲发生器的输出。如果您为包含基于时间的脉冲发生器的模型指定定步长求解器，Sysblock 将计算基于时间的脉冲发生器的固定采样时间。然后基于时间的脉冲发生器会以基于采样的模式进行仿真。

如果使用定步长求解器，而**脉冲类型**为基于时间，请选择步长，使周期、相位延迟和脉冲宽度（以秒为单位）等于求解器步长的整数倍。例如，假定周期为 4 秒，脉冲宽度为 750px（即 3 秒），相位延迟为 1 秒。在这种情况下，计算出的采样时间为 1 秒。因此，请选择定步长 1 或者能够将 1 整除的数字（例如 0.25）。要确保此设置，请在“配置参数”对话框的**求解器**窗格中选择 auto。 -->

### 基于采样的模式

在基于采样的模式下，模块按照您指定的固定时间间隔来计算其输出。通过将**脉冲类型**参数设置为“基于采样”可以激活此模式。

基于时间的模式和基于采样的模式之间有一个重要区别，前者的模块输出基于仿真时间，后者的模块输出只取决于仿真开始时间，与已用仿真时间无关。

在基于采样的模式下，此模块支持重置语义。例如，如果 PulseGenerator 模块在一个可重置子系统中，如果子系统触发了重置触发器，模块输出将重置为其初始条件。

## 示例

<!-- [![在仿真期间调节脉冲发生器上的相位延迟](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/tunephasedelayonpulsegeneratorduringsimulationexample_01_zh_CN.png)在仿真期间调节脉冲发生器上的相位延迟此示例说明如何修改模型以便在仿真期间更改 Pulse Generation 模块的相位延迟。](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/tuen-phase-delay-on-pulse-generator-during-simulation.html)

[![Difference Between Time- and Sample-Based Pulse Generation](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink/win64/DifferenceBetweenTimeAndSampleBasedPulseGenerationExample_02.png)Difference Between Time- and Sample-Based Pulse GenerationThe difference in behavior of the Pulse Generator block in time-based and sample-based modes.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/distance-between-time-and-sample-based-pulse-generation.html)

[![自动气候控制系统仿真](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/simulatingautomaticclimatecontrolsystemsexample_01_zh_CN.png)自动气候控制系统仿真此示例说明如何使用 Simulink® 和 Stateflow® 对汽车中自动气候控制系统进行仿真。](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/simulating-automatic-climate-control-systems.html)

[![使用时序逻辑的 Bang-Bang 控制](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/sldemo_boilerexample_01_zh_CN.png)使用时序逻辑的 Bang-Bang 控制此示例说明如何使用 Stateflow® 为锅炉的 Bang-Bang 温度控制系统建模。在 Simulink® 中对锅炉动态特性进行建模。](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/bang-bang-control-using-temporal-logic.html) -->

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/PulseGenerator.mo">PulseGenerator.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/PulseGenerator/PulseGenerator_ex.png')" style="width: 300px; height: auto; transform: scale(0.8);">

### 示例说明

- PulseGenerator 模块：按固定间隔生成方波脉冲。此模块的波形参数振幅、脉冲宽度、周期和相位延迟确定了输出波形的形状。可以生成任何实数数据类型的标量、向量或矩阵信号；
- Scope 模块：用于显示模型的输出结果，即 PulseGenerator 模块生成的方波脉冲信号。


## 端口

### 输出


<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

根据参数指定生成的方波脉冲信号。

**数据类型：** float | int8 | int16 | int32 | uint8 | uint16 | uint32 | fixedPoint

</div>
</div>



## 参数


<div class="details-box">
<details open>
<summary>脉冲类型 — 计算方法<div>“基于时间” （默认） | “基于采样”</div></summary>
</details>
<div class="details-content">

计算方法，基于时间或基于采样生成此模块生成的方波类型。根据您选择的是基于时间还是基于采样，对话框中将出现某些参数。

</div>
</div>


<!-- #### 编程用法

| **模块参数**：PulseType                 |
| ----------------------------------------- |
| **类型**：字符向量                        |
| **值**：'Time based' | 'Sample based' |
| **默认值**：'Time based'                | -->


<div class="details-box">
<details open>
<summary>时间(t) — 时间变量的来源<div>“使用仿真时间” （默认） | “使用外部信号”</div></summary>
</details>
<div class="details-content">

指定是使用仿真时间还是外部信号作为输出脉冲时间变量值的来源。如果指定外部源，模块将显示一个输入端口用来连接该外部源。输出脉冲有所不同，如下所示：

- “使用仿真时间”：模块生成时间变量等于仿真时间的输出脉冲；
- “使用外部信号”：模块生成时间变量等于来自输入端口的值（可能不同于仿真时间）的输出脉冲。

</div>
</div>




<!-- #### 编程用法

| **模块参数**：TimeSource                                |
| --------------------------------------------------------- |
| **类型**：字符向量                                        |
| **值**：'Use simulation time' | 'Use external signal' |
| **默认值**：'Use simulation time'                       | -->


<div class="details-box">
<details open>
<summary>振幅 — 信号幅值<div>1 （默认） | scalar</div></summary>
</details>
<div class="details-content">

指定信号幅值。

</div>
</div>




<!-- #### 编程用法

| **模块参数**：Amplitude |
| ------------------------- |
| **类型**：字符向量        |
| **值**：标量              |
| **默认值**：'1'         | -->

<div class="details-box">
<details open>
<summary>周期(秒) — 脉冲周期<div>10 （默认） | scalar</div></summary>
</details>
<div class="details-content">

如果脉冲类型为基于时间，则以秒为单位指定脉冲周期。如果脉冲类型为基于采样，则以采样时间的数量指定脉冲周期。

</div>
</div>


<!-- #### 编程用法

| **模块参数**：Period |
| ---------------------- |
| **类型**：字符向量     |
| **值**：标量           |
| **默认值**：'10'     | -->


<div class="details-box">
<details open>
<summary>脉冲宽度 — 占空比<div>50 （默认） | scalar in the range [0,100]</div></summary>
</details>
<div class="details-content">

占空比，如果脉冲类型是基于时间，则指定为脉冲周期内有信号时的占比；如果基于采样，则是指定为有信号的采样次数。

</div>
</div>




<!-- #### 编程用法

| **模块参数**：PulseWidth |
| -------------------------- |
| **类型**：字符向量         |
| **值**：标量               |
| **默认值**：'5'          | -->

<div class="details-box">
<details open>
<summary>相位延迟(秒) — 脉冲前延迟量<div>0 （默认） | scalar</div></summary>
</details>
<div class="details-content">

脉冲前延迟量，如果脉冲类型为基于时间，则以秒为单位指定生成脉冲之前的延迟时间；如果基于采样，则指定为生成脉冲之前的采样次数。

</div>
</div>




<!-- #### 编程用法

| **模块参数**：PhaseDelay |
| -------------------------- |
| **类型**：字符向量         |
| **值**：标量               |
| **默认值**：'0'          | -->



<!-- ### 采样时间 — 采样时间的长度 0 （默认） | scalar | 向量



此模块的采样时间的长度（以秒为单位）。仅当模块的脉冲类型为基于采样时，才会显示此参数。请参阅 [指定采样时间](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/how-to-specify-the-sample-time.html)。

#### 编程用法

| **模块参数**：SampleTime |
| -------------------------- |
| **类型**：字符向量         |
| **值**：标量               |
| **默认值**：'0'          | -->



<!-- ### 将向量参数解释为一维向量 — 将向量视为一维 on （默认） | off



如果**振幅**、**周期**、**脉冲宽度**或**相位延迟**参数的计算结果为包含 N 个元素的行向量或列向量，则选中此复选框将输出长度为 N 的向量。

- 如果任一值参数的计算结果为包含 N 个元素的行或列向量，则选中此复选框时，模块将输出长度为 N 的向量。例如，模块将输出 1-by-N 维或 N-by-1 维矩阵。
- 如果任一值参数的计算结果为包含 N 个元素的行或列向量，则清除此复选框时，模块不输出长度为 N 的向量。

有关如何使用此参数的详细信息，请参阅[确定源模块的输出维度](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/determining-output-signal-dimensions.html#bsud_ek-4)。

#### 编程用法

| **模块参数**：VectorParams1D |
| ------------------------------ |
| **类型：**字符向量             |
| **值：**'on' | 'off'         |
| **默认值：**'on'             | -->



<!-- ## 模块特性

| **数据类型**     | Boolean | double | fixed point | integer | single |
| ---------------- | ----------------------------------------------------------- |
| **直接馈通**     | 是                                                        |
| **多维信号**     | 否                                                        |
| **可变大小信号** | 否                                                        |
| **过零检测**     | 否                                                        | -->


## 版本历史记录

- 在 2024b 之前推出

### 限制信息

1. 暂不支持自定义采样时间；  
2. 暂不支持将向量参数解释为一维向量的复选框；  
3. 输出信号暂不支持 double、int64 和 uint64 的数据类型。

<!-- ## 扩展功能



### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。

不能在触发子系统层次结构中使用。

当配置为基于采样运行时，这些模块不引用绝对时间。在基于时间的运行中，它们依赖于绝对时间。



### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。

## 版本历史记录

**在 R2006a 之前推出** -->

<!-- ## 另请参阅

[Signal Generator](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/signalgenerator.html) | [Waveform Generator](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/waveformgenerator.html) -->