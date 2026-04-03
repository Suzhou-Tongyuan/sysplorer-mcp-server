# ZeroOrderHold
---
&nbsp;

实现零阶保持采样周期

- **库：** Sysblock / Discrete

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/ZeroOrderHold/ZeroOrderHold.png')" style="width: 100px; height: auto;">

## 描述

ZeroOrderHold 模块在您指定的采样周期内保持其输入不变。如果输入为向量，模块会按相同的采样周期保持向量中的所有元素。

可通过**采样时间**参数指定样本之间的时间间隔。设置为 -1 表示模块将继承**采样时间**。


### 总线支持

ZeroOrderHold 模块支持总线。输入可以是虚拟或非虚拟总线信号。没有特定于模块的限制条件。ZeroOrderHold 模块的非虚拟总线输入中的所有信号必须具有相同的采样时间，即使相关总线对象的元素指定了继承的采样时间也是如此。

<!-- 暂无
### 与类似模块的比较

Memory、Unit Delay 和 Zero-Order Hold 模块提供相似的功能，但各自具有不同的能力。此外，每个模块的用途也各不相同。

下表显示每个模块的推荐用途。

| 模块                                                         | 模块的用途                                                   | 引用示例                                                     |
| :----------------------------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| [Unit Delay](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/unitdelay.html) | 使用您指定的离散采样时间实现延迟。该模块接受并输出具有离散采样时间的信号。 | [Engine Timing Model with Closed Loop Control](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/engine-timing-model-with-closed-loop-control.html)（Compression 子系统） |
| [Memory](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/memory.html) | 将信号延迟一个主积分时间步。在理想情况下，该模块接受连续（或在子时间步中固定）的信号并输出在子时间步中固定的信号。 | [Building a Clutch Lock-Up Model](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/building-a-clutch-lock-up-model.html)（Friction Mode Logic/Lockup FSM 子系统）[Capture the Velocity of a Bouncing Ball with the Memory Block](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/capture-velocity-of-bouncing-ball-with-memory.html) |
| [Zero-Order Hold](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/zeroorderhold.html) | 将具有连续采样时间的输入信号转换为具有离散采样时间的输出信号。 | [Developing the Apollo Lunar Module Digital Autopilot](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/developing-the-apollo-lunar-module-digital-autopilot.html)[使用 MATLAB Function 模块的雷达跟踪](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/radar-tracking-using-matlab-function-block.html) |

每个模块有以下功能。

| 功能             | 内存                                                         | 单位延迟 | 零阶保持                                            |
| :--------------- | :----------------------------------------------------------- | :------- | :-------------------------------------------------- |
| 指定初始条件     | 是                                                           | 是       | 否，因为在时间 t = 0 的模块输出必须与输入值相匹配。 |
| 指定采样时间     | 否，因为该模块只能从驱动模块或用于整个模型的求解器继承采样时间。 | 是       | 是                                                  |
| 支持基于帧的信号 | 否                                                           | 是       | 是                                                  |
| 支持状态记录     | 否                                                           | 是       | 否                                                  | -->

## 示例

将一个正弦波的输出进行离散化，双击 ZeroOrderHold 模块将采样时间设置为 0.1 输出的离散信号在每个采样周期内保持一个固定的值，这个值是在采样时刻的正弦波信号值。例如，在 0 - 0.1 秒内，输出保持为正弦波在 0 秒时刻的值；
在 0.1 - 0.2 秒内，输出保持为正弦波在 0.1 秒时刻的值，以此类推。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/ZeroOrderHold.mo">ZeroOrderHold.mo</helpButton>。


<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/ZeroOrderHold/ZeroOrderHold01.png')" style="width: 600px; height: auto;">

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/ZeroOrderHold/ZeroOrderHold02.png')" style="width: 600px; height: auto;">

## 端口

### 输入


<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

输入信号，模块会将其保持一个采样周期。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | Boolean | fixed point | enumerated 

</div>
</div>


### 输出


<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

输出信号，即保持了一个采样周期的输入。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | Boolean | fixed point | enumerated 

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>采样时间（-1 表示继承） — 采样时间命中点之间的离散间隔<div>-1（默认）</div></summary>
</details>
<div class="details-content">

指定采样时间间隔。要继承采样时间，请将此参数设置为 -1。

不要指定连续采样时间 0 或 [0,0]。此模块仅支持离散采样时间。当此参数为 -1 时，继承的采样时间必须是离散时间，不能是连续时间。

</div>
</div>

<!-- ## 模块特性 -->

<!-- 部分功能暂无
| **数据类型**     | `Boolean` \| `bus` \| `double` \| `enumerated` \| `fixed point` \| `integer` \| `single` |
| ---------------- | ------------------------------------------------------------ |
| **直接馈通**     | `是`                                                         |
| **多维信号**     | `否`                                                         |
| **可变大小信号** | `否`                                                         |
| **过零检测**     | `否`                                                         | -->

<!-- ## 扩展功能 -->



<!-- ### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。

生成的代码在特定条件下依赖于 `memcpy` 或 `memset` 函数 (`strong.h`)。



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 Verilog 代码和 VHDL 代码。

HDL Coder™ 提供影响 HDL 实现和综合逻辑的额外配置选项。



**HDL 架构**

此模块具有一个默认 HDL 架构。

**HDL 模块属性**

| **ConstrainedOutputPipeline** | 通过移动设计中现有延迟的方式来放置在输出端的寄存器的数量。分布式流水线处理不会重新分发这些寄存器。默认值为 `0`。有关详细信息，请参阅[ConstrainedOutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#btp8gmp) (HDL Coder)。 |
| ----------------------------- | ------------------------------------------------------------ |
| **InputPipeline**             | 要在生成的代码中插入的输入流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 `0`。有关详细信息，请参阅[InputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-25) (HDL Coder)。 |
| **OutputPipeline**            | 要在生成的代码中插入的输出流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 `0`。有关详细信息，请参阅[OutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-26) (HDL Coder)。 |

**复数数据支持**

此模块支持复信号的代码生成。



### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。 -->

## 版本历史记录

- 在 2024b 之前推出

### 限制信息

描述-与类似模块的比较

## 另请参阅

[UnitDelay](UnitDelay.html)

<!-- [Memory]() |  -->