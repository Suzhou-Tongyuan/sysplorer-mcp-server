# UnitDelay
---
&nbsp;

将信号延迟一个采样周期


- **库:** Sysblock / Discrete

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/UnitDelay/UnitDelay.png')" style="width: 100px; height: auto;">

## 描述

UnitDelay 模块将其输入保持并延迟一个采样周期。当放置于迭代子系统中时，该模块将其输入保持并延迟一个迭代。此模块相当于 z-1 离散时间运算符。此模块接受一个输入并生成一个输出。每个信号可以是标量，也可以是向量。如果输入为向量，模块会按相同的采样周期保持和延迟向量中的所有元素。

可通过**初始条件**参数指定第一个采样周期的模块输出。仔细选择此参数可以最大程度地减少不需要的输出行为。可通过**采样时间**参数指定样本之间的时间间隔。设置为 -1 表示模块将继承**采样时间**。

<!-- 暂无
### 与类似模块的比较

Memory、Unit Delay 和 Zero-Order Hold 模块提供相似的功能，但各自具有不同的能力。此外，每个模块的用途也各不相同。

下表显示每个模块的推荐用途。

| 模块                                                         | 模块的用途                                                   | 引用示例                                                     |
| :----------------------------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| [Unit Delay](https://ww2.mathworks.cn/help/simulink/slref/unitdelay.html) | 使用您指定的离散采样时间实现延迟。该模块接受并输出具有离散采样时间的信号。 | [Engine Timing Model with Closed Loop Control](https://ww2.mathworks.cn/help/simulink/slref/engine-timing-model-with-closed-loop-control.html)（Compression 子系统） |
| [Memory](https://ww2.mathworks.cn/help/simulink/slref/memory.html) | 将信号延迟一个主积分时间步。在理想情况下，该模块接受连续（或在子时间步中固定）的信号并输出在子时间步中固定的信号。 | [Building a Clutch Lock-Up Model](https://ww2.mathworks.cn/help/simulink/slref/building-a-clutch-lock-up-model.html)（Friction Mode Logic/Lockup FSM 子系统）[Capture the Velocity of a Bouncing Ball with the Memory Block](https://ww2.mathworks.cn/help/simulink/slref/capture-velocity-of-bouncing-ball-with-memory.html) |
| [Zero-Order Hold](https://ww2.mathworks.cn/help/simulink/slref/zeroorderhold.html) | 将具有连续采样时间的输入信号转换为具有离散采样时间的输出信号。 | [Developing the Apollo Lunar Module Digital Autopilot](https://ww2.mathworks.cn/help/simulink/slref/developing-the-apollo-lunar-module-digital-autopilot.html)[使用 MATLAB Function 模块的雷达跟踪](https://ww2.mathworks.cn/help/simulink/slref/radar-tracking-using-matlab-function-block.html) |

每个模块有以下功能。

| 功能             | 内存                                                         | 单位延迟 | 零阶保持                                            |
| :--------------- | :----------------------------------------------------------- | :------- | :-------------------------------------------------- |
| 指定初始条件     | 是                                                           | 是       | 否，因为在时间 t = 0 的模块输出必须与输入值相匹配。 |
| 指定采样时间     | 否，因为该模块只能从驱动模块或用于整个模型的求解器继承采样时间。 | 是       | 是                                                  |
| 支持基于帧的信号 | 否                                                           | 是       | 是                                                  |
| 支持状态记录     | 否                                                           | 是       | 否                                                  | -->

<!-- 暂无
### 字符串支持

仅当 Unit Delay 模块配置为**初始条件**参数采用默认值 (0) 时，该模块才接受和输出字符串数据类型。 -->

## 示例

添加一个 constant 模块作为信号源，将信号源延迟一个单位输出。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/UnitDelay.mo">UnitDelay.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/UnitDelay/UnitDelay01.png')" style="width: 600px; height: auto;">

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/UnitDelay/UnitDelay02.png')" style="width: 600px; height: auto;">


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

输入信号，它被模块延迟了一个采样周期。

**数据类型:**  float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | Boolean | fixed point | bus

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

输出信号，即延迟了一个采样周期的输入信号。

**数据类型:** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | Boolean | fixed point | bus 

</div>
</div>

## 参数

### 常设

<div class="details-box">
<details open>
<summary>初始条件 — 第一个采样周期输出<div>0 (默认) | 标量 | 向量</div></summary>
</details>
<div class="details-content">

指定第一个采样周期的仿真输出，否则，此周期内 Unit Delay 模块的输出为未定义。

</div>
</div>

<!-- 
#### 编程用法

| **模块参数**：`InitialCondition` |
| -------------------------------- |
| **类型**：字符向量               |
| **值**：标量 \| 向量             |
| **默认值**：`'0'`                |
-->

<!-- 暂无
### **输入处理** — 指定基于采样或基于帧的处理 **元素作为通道(基于采样)** (默认) | **列作为通道(基于帧)**



指定模块是执行基于采样还是基于帧的处理：

- **列作为通道(基于帧)** - 将输入信号的每一列视为一个单独的通道（基于帧的处理）。

  

  **注意**

  基于帧的处理需要具有 DSP System Toolbox™ 许可证。

  有关详细信息，请参阅[Sample- and Frame-Based Concepts](https://ww2.mathworks.cn/help/dsp/ug/sample-and-frame-based-concepts.html) (DSP System Toolbox)。

- **元素作为通道(基于采样)** - 将输入信号的每个元素视为一个单独的通道（基于采样的处理）。

可以使用**输入处理**指定模块是执行基于采样的处理还是基于帧的处理。有关这两种处理模式的详细信息，请参阅[Sample- and Frame-Based Concepts](https://ww2.mathworks.cn/help/dsp/ug/sample-and-frame-based-concepts.html) (DSP System Toolbox)。

#### 编程用法

| **模块参数**：`InputProcessing`                              |
| ------------------------------------------------------------ |
| **类型**：字符向量                                           |
| **值**：`'Columns as channels (frame based)'` | `'Elements as channels (sample based)'` |
| **默认值**：`'Elements as channels (sample based)'`          | -->


<div class="details-box">
<details open>
<summary>采样时间（-1 表示继承） — 采样时间命中点之间的离散间隔<div>-1（默认） | 1×2 向量</div></summary>
</details>
<div class="details-content">

输入采样时间命中点之间的离散间隔，或者指定 -1 以继承采样时间。

</div>
</div>

<!-- 
#### 编程用法

| **模块参数**：`SampleTime`   |
| ---------------------------- |
| **类型**：字符向量           |
| **值**：实数标量 \| 1×2 向量 |
| **默认值**：`'-1'`           | -->

<!-- 
### 状态属性 -->

<!-- 暂无

### **状态名称** — 模块状态的唯一名称 `''` (默认) | 字母数字字符串



使用此参数为模块状态指定唯一名称。默认值为 `' '`。如果此字段为空，则表示未指定任何名称。使用此参数时，请记住以下注意事项：

- 有效的标识符以字母或下划线字符开始，后跟字母数字或下划线字符。
- 状态名称仅适用于所选模块。

当您点击**应用**时，此参数将启用**状态名称必须解析为 Simulink 信号对象**。

有关详细信息，请参阅[C Data Code Interface Configuration for Model Interface Elements](https://ww2.mathworks.cn/help/rtw/ug/c-data-code-interface-configuration-for-model-interface-elements.html) (Simulink Coder)。

#### 编程用法

| **模块参数**：`StateName` |
| ------------------------- |
| **类型：**字符向量        |
| **值：**唯一名称          |
| **默认值：**`''`          | -->


<!-- 暂无
### **状态名称必须解析为 Simulink 信号对象** — 要求状态名称解析为信号对象的选项 `off` (默认) | `on`



指定是否需要将状态名称解析为信号对象。如果选中此选项，则在指定的状态名称与信号对象的名称不匹配时，软件会在运行时生成错误。

选择此参数将禁用**代码生成存储类**参数。

#### 依存关系

当您为**状态名称**参数指定值并将**信号解析**模型配置参数设置为**无**以外的值时启用。

#### 编程用法

| **模块参数**：`StateMustResolveToSignalObject` |
| ---------------------------------------------- |
| **类型**：字符向量                             |
| **值**：`'off'` | `'on'`                       |
| **默认值**：`'off'`                            | -->

<!-- ## 模块特性 -->

<!-- 部分属性暂无
| **数据类型**  | `Boolean` \| `bus` \| `double` \| `fixed point` \| `integer` \| `float` \|
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| **直接馈通**                                                 | `否a`                                                        |
| **多维信号**                                                 | `是`                                                         |
| **可变大小信号**                                             | `是`                                                         |
| **过零检测**                                                 | `否`                                                         |
| [a](https://ww2.mathworks.cn/help/simulink/slref/unitdelay.html?s_tid=doc_ta#d126e269651) 此模块的直接馈通特性取决于模块参数值。 |                                                              | -->

<!-- ## 扩展功能 -->


<!-- 暂无
### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。

生成的代码在特定条件下依赖于 `memcpy` 或 `memset` 函数 (`strong.h`)。



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 VHDL、Verilog 和 SystemVerilog 代码。

HDL Coder™ 提供影响 HDL 实现和综合逻辑的额外配置选项。



**HDL 架构**

此模块具有一个默认 HDL 架构。

**HDL 模块属性**

| **AllowDelayDistribution** | 允许在分布式流水线和延迟吸收优化期间分布或吸收延迟。默认值为 **inherit**。有关详细信息，请参阅[AllowDelayDistribution](https://ww2.mathworks.cn/help/hdlcoder/ug/block-implementation-parameters.html#mw_41060a9f-e2a7-4403-9582-35948532beed) (HDL Coder)。 |
| -------------------------- | ------------------------------------------------------------ |
| **InputPipeline**          | 要在生成的代码中插入的输入流水线阶段数。分布式流水线和受限输出流水线可以移动这些寄存器。默认值为 `0`。有关详细信息，请参阅[InputPipeline](https://ww2.mathworks.cn/help/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-25) (HDL Coder)。 |
| **OutputPipeline**         | 要在生成的代码中插入的输出流水线阶段数。分布式流水线和受限输出流水线可以移动这些寄存器。默认值为 `0`。有关详细信息，请参阅[OutputPipeline](https://ww2.mathworks.cn/help/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-26) (HDL Coder)。 |
| **ResetType**              | 隐藏重置逻辑生成。默认值为**默认**，它生成重置逻辑。另请参阅[ResetType](https://ww2.mathworks.cn/help/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-27) (HDL Coder)。 |

**复数数据支持**

此模块支持复信号的代码生成。



### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。 -->

## 版本历史记录

- 在 2024b 之前推出

### 限制信息
不支持部分
1. 描述-与类似模块的比较
2. 描述-字符串支持
3. 参数-常设-输入处理 — 指定基于采样或基于帧的处理
4. 参数-常设-状态名称 — 模块状态的唯一名称



## 另请参阅

[Delay](Delay.html)
