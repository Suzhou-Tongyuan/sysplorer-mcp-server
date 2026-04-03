# RepeatingSequence
---
生成任意形状的周期信号

**库：** Sysblock模块库 / Sources

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/RepeatingSequence/RepeatingSequence.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

RepeatingSequence 模块可以输出波形由**时间值**和**输出值**参数指定的周期性标量信号。**时间值**参数指定输出时间向量。**输出值**参数指定输出时间对应的信号幅值向量。这两个参数结合使用指定输出波形的重复间隔（信号周期）的各测量点确定的采样。

默认情况下，这两个参数都是 [0 2]。这些默认设置指定了从仿真开始每 2 秒重复一次，最大幅值为 2 的锯齿波形。

## 示例

<!-- [![Specify a Waveform with the Repeating Sequence Block](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink/win64/SpecifyAWaveformWithTheRepeatingSequenceBlockExample_02.png)Specify a Waveform with the Repeating Sequence BlockHow you specify a waveform with the Repeating Sequence block.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/specify-waveform-with-repeating-sequence.html)

[![容错燃油控制系统建模](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/modelingafaulttolerantfuelcontrolsystemexample_02_zh_CN.png)容错燃油控制系统建模此示例说明如何结合使用 Stateflow® 和 Simulink® 来高效地进行混合系统建模。这种类型的建模对于具有基于离散事件的多种可能运行模式的系统特别有用。传统的信号流在 Simulink 中处理，而控制配置的更改在 Stateflow 中实现。下面所述的模型表示汽油引擎的燃油控制系统。该系统具有很强的稳健性，因为它可以检测到单个传感器的故障，并且可以动态重新配置控制系统以实现不间断运行。](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/modeling-a-fault-tolerant-fuel-control-system.html)

[![Two Cylinder Model with Load Constraints](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink_general/win64/sldemo_hydrodExample_01.png)Two Cylinder Model with Load ConstraintsModel a rigid rod supporting a large mass interconnecting two hydraulic actuators. The model eliminates the springs as it applies the piston forces directly to the load. These forces balance the gravitational force and result in both linear and rotational displacement.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/two-cylinder-model-with-load-constraints.html)

[![Simulating Systems with Variable Transport Delay Phenomena](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink_general/win64/sldemo_VariableTransportDelayExample_04.png)Simulating Systems with Variable Transport Delay PhenomenaTwo cases where you can use Simulink® to model variable transport delay phenomena.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/simulating-systems-with-variable-transport-delay-phenomena.html) -->

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/RepeatingSequence.mo">RepeatingSequence.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/RepeatingSequence/RepeatingSequence_ex.png')" style="width: 300px; height: auto; transform: scale(0.8);">

### 示例说明

- RepeatingSequence 模块：用于生成一个任意形状的周期信号。可以指定时间值和输出值；
- Scope 模块：用于显示模型的输出结果，即 RepeatingSequence 模块生成的周期性重复序列信号。

## 端口

### 输出

<div class="details-box">
<details open>
<summary>y — 周期性输出信号<div>标量</div></summary>
</details>
<div class="details-content">

输出由**时间值**和**输出值**参数指定的信号以创建周期性标量信号。

**数据类型：** double

</div>
</div>


## 参数


<div class="details-box">
<details open>
<summary>时间值 — 输出时间的向量<div>[0 2] （默认） | 向量</div></summary>
</details>
<div class="details-content">

严格单调递增时间值的向量。生成的波形的周期是此参数的最后一个值和第一个值之差。

</div>
</div>




<!-- #### 编程用法

| **模块参数**：rep_seq_t |
| ------------------------- |
| **类型**：字符向量        |
| **值**：向量              |
| **默认值**：[0 2]       | -->


<div class="details-box">
<details open>
<summary>输出值 — 输出值的向量<div>[0 2] （默认） | 向量</div></summary>
</details>
<div class="details-content">

输出值的向量，用于指定输出波形。每个元素对应于**时间值**参数中的时间值。

</div>
</div>




<!-- #### 编程用法

| **模块参数**：rep_seq_y |
| ------------------------- |
| **类型**：字符向量        |
| **值**：向量              |
| **默认值**：[0 2]       | -->



<!-- ## 模块特性

| **数据类型**     | double |
| ---------------- | -------- |
| **直接馈通**     | 否     |
| **多维信号**     | 否     |
| **可变大小信号** | 否     |
| **过零检测**     | 否     | -->

## 算法

此模块将输入周期设置为第一个和最后一个**时间值**参数值之差。任意时间 t 的输出就是 t = t-n\*period 时的输出，其中 n 是整数。该序列在 t = n\*period 时重复。此模块使用线性插值来计算在您指定的输出时间之间的波形值。

## 版本历史记录

- 在 2024b 之前推出

<!-- ## 版本历史记录

### 限制信息 -->



<!-- ## 扩展功能



### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。

不建议用于生产代码。

考虑使用 Repeating Sequence Stair 或 Repeating Sequence Interpolated 模块进行代码生成。

## 版本历史记录

**在 R2006a 之前推出** -->

<!-- ## 另请参阅

[Repeating Sequence Stair](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/repeatingsequencestair.html) | [Repeating Sequence Interpolated](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/repeatingsequenceinterpolated.html) -->