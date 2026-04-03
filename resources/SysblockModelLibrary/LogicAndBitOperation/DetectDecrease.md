# DetectDecrease
---
&nbsp;

检测信号值的减小

**库：** Sysblock模块库 / LogicAndBitOperation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/DetectDecrease/DetectDecrease.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

DetectDecrease 模块确定输入信号是否严格小于上一个值。

此模块仅支持离散采样时间。

## 示例

<!-- 暂无
[![Detect Decreasing Signal Values](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink/win64/DetectDecreasingSignalValuesBlockExample_02.png)Detect Decreasing Signal ValuesDetermine if an input signal is strictly less than its previous value using the Detect Decrease block.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/detect-decreasing-signal-values.html) -->

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/DetectDecrease.mo">DetectDecrease.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/DetectDecrease/DetectDecrease_ex.png')" style="width: 600px; transform: scale(0.8);">

### 示例说明

- Step 模块：用于提供随时间变化的输入信号。在这个例子中，信号在仿真开始时从 0 跳变到 1；
- DetectDecrease 模块：用于检测输入信号是否递减。如果信号值小于前一个值，则输出 1；
- Scope 模块：用于显示模型的输出。在这个例子中，它显示了递减检测的结果，即输入信号是否递减。

## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

输入信号，指定为标量、向量或矩阵。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | fixedPoint | enum

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>0 | 1</div></summary>
</details>
<div class="details-content">

输出信号，当输入信号小于上一个值时，为 true（等于 1）；当输入信号大于或等于上一个值时，为 false（等于 0）。

**数据类型：**  boolean 

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>初始条件 — 上一个的初始条件<div>0 （默认） | 标量 | 向量</div></summary>
</details>
<div class="details-content">

为上一个输入 U/z 设置初始条件。 

</div>
</div>


<!-- 暂无
#### 编程用法

| **模块参数**：vinit |
| --------------------- |
| **类型：**字符向量    |
| **值：**标量 \| 向量  |
| **默认值：**'0'     | -->


<!-- 暂无
### 输入处理 — 指定基于采样或基于帧的处理 “元素作为通道(基于采样)” （默认） | “列作为通道(基于帧)”



指定模块是执行基于采样还是基于帧的处理：

- “列作为通道(基于帧)” - 将输入信号的每一列视为一个单独的通道（基于帧的处理）。

  

  **注意**

  基于帧的处理需要具有 DSP System Toolbox™ 许可证。

  有关详细信息，请参阅[Sample- and Frame-Based Concepts](https://ww2.mathworks.cn/help/releases/R2022b/dsp/ug/sample-and-frame-based-concepts.html) (DSP System Toolbox)。

- “元素作为通道(基于采样)” - 将输入信号的每个元素视为一个单独的通道（基于采样的处理）。

可以使用**输入处理**指定模块是执行基于采样的处理还是基于帧的处理。有关这两种处理模式的详细信息，请参阅[Sample- and Frame-Based Concepts](https://ww2.mathworks.cn/help/releases/R2022b/dsp/ug/sample-and-frame-based-concepts.html) (DSP System Toolbox)。

#### 编程用法

| **模块参数**：InputProcessing                              |
| ------------------------------------------------------------ |
| **类型**：字符向量                                           |
| **值**：'Columns as channels (frame based)' | 'Elements as channels (sample based)' |
| **默认值**：'Elements as channels (sample based)'          | -->


<div class="details-box">
<details open>
<summary>输出数据类型 — 输出的数据类型<div>“boolean” （默认） | “Inherit: auto”</div></summary>
</details>
<div class="details-content">

将输出数据类型设置为 boolean 或 Inherit: auto。

</div>
</div>




<!-- 暂无
#### 编程用法

| **模块参数**：OutDataTypeStr  |
| ------------------------------- |
| **类型**：字符向量              |
| **值**：'boolean' | 'uint8' |
| **默认值**：'boolean'         | -->




<!-- 不确定
## 模块特性

| **数据类型**     | Boolean | double | enumerated | fixed point | integer | single |
| ---------------- | ------------------------------------------------------------ |
| **直接馈通**     | 是                                                         |
| **多维信号**     | 是                                                         |
| **可变大小信号** | 是                                                         |
| **过零检测**     | 否                                                         | -->

## 版本历史记录

- 在 2024b 之前推出

### 限制信息

1. 暂不支持对输入指定基于采样或基于帧的处理；  
2. 输入信号暂不支持 int64 和 uint64 的数据类型，输出信号暂不支持 float、double、int8、int16、int32、int64、uint8、uint16、uint32、uint64、fixedPoint、enum 和 bus 的数据类型。

<!-- 暂无
## 扩展功能


### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。

生成的代码在特定条件下依赖于 memcpy 或 memset 函数 (string.h)。


### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 Verilog 代码和 VHDL 代码。



HDL Coder™ 提供影响 HDL 实现和综合逻辑的额外配置选项。

**HDL 架构**

此模块具有一个默认 HDL 架构。

**HDL 模块属性**

| **ConstrainedOutputPipeline** | 通过移动设计中现有延迟的方式来放置在输出端的寄存器的数量。分布式流水线处理不会重新分发这些寄存器。默认值为 0。有关详细信息，请参阅[ConstrainedOutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#btp8gmp) (HDL Coder)。 |
| ----------------------------- | ------------------------------------------------------------ |
| **InputPipeline**             | 要在生成的代码中插入的输入流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 0。有关详细信息，请参阅[InputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-25) (HDL Coder)。 |
| **OutputPipeline**            | 要在生成的代码中插入的输出流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 0。有关详细信息，请参阅[OutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-26) (HDL Coder)。 |



### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。

## 版本历史记录

**在 R2006a 之前推出** -->

## 另请参阅

[DetectChange](DetectChange.html) | [DetectFallNegative](DetectFallNegative.html) | [DetectFallNonpositive](DetectFallNonpositive.html) | [DetectIncrease](DetectIncrease.html) | [DetectRiseNonnegative](DetectRiseNonnegative.html) | [DetectRisePositive](DetectRisePositive.html)