# DetectFallNegative
---
&nbsp;

检测信号值下降到严格负值的情况，且其前一个值是非负的。

**库：** Sysblock模块库 / LogicAndBitOperation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/DetectFallNegative/DetectFallNegative.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

DetectFallNegative 模块用于判断输入信号是否小于零，且其前一个值大于或等于零。

此模块仅支持离散采样时间。

## 示例

<!-- 暂无
[![Detect Fall to Negative Signal Values](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink/win64/DetectFallNegativeBlockExample_02.png)Detect Fall to Negative Signal ValuesDetect when a signal value decreases to a strictly negative value from a value that was greater than or equal to zero.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/detect-fall-to-negative-signal-values.html) -->

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/DetectFallNegative.mo">DetectFallNegative.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/DetectFallNegative/DetectFallNegative_ex.png')" style=" width: 600px;transform: scale(0.8);">

### 示例说明

- Step 模块：用于提供随时间变化的输入信号。在这个例子中，信号在仿真开始时从 0 跳变到 1；
- DetectDecrease 模块：用于检测输入信号是否递减。如果信号值小于前一个值，则输出 1；
- Scope 模块：用于显示模型的输出。在这个例子中，它显示了递减检测的结果，即输入信号是否递减。

## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>信号值</div></summary>
</details>
<div class="details-content">

输入信号，可以是标量、向量或矩阵。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | fixedPoint | enum

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>0 | 1</div></summary>
</details>
<div class="details-content">

输出信号，当输入信号小于零且其前一个值大于或等于零时为真（等于1）；当输入信号大于或等于零，或者输入信号为负但其前一个值也为负时为假（等于0）。

**数据类型：** boolean

</div>
</div>



## 参数

<div class="details-box">
<details open>
<summary>初始条件 — 前一个输入的初始条件<div>0 （默认） | 标量 | 向量</div></summary>
</details>
<div class="details-content">

设置布尔表达式 U/z < 0 的初始条件。

</div>
</div>


<!-- 暂无
#### 编程使用

| **模块参数：** vinit |
| ---------------------- |
| **类型：** 字符向量    |
| **值：** 标量 \| 向量  |
| **默认值：** '0'     | -->


<!-- 暂无
### Input processing — 指定基于采样或基于帧的处理 “元素作为通道(基于采样)” （默认） | “列作为通道(基于帧)”

指定模块是执行基于采样还是基于帧的处理：

- “列作为通道(基于帧)” — 将输入的每一列视为一个单独的通道（基于帧的处理）。

  **注意**

  基于帧的处理需要 DSP System Toolbox™ 许可证。

  有关详细信息，请参阅 [基于样本和基于帧的概念](https://ww2.mathworks.cn/help/releases/R2022b/dsp/ug/sample-and-frame-based-concepts.html) （DSP System Toolbox）。

- “元素作为通道(基于采样)” — 将输入的每个元素视为一个单独的通道（基于采样的处理）。

可以使用**输入处理**指定模块是执行基于采样的处理还是基于帧的处理。有关这两种处理模式的详细信息，请参阅 [基于样本和基于帧的概念](https://ww2.mathworks.cn/help/releases/R2022b/dsp/ug/sample-and-frame-based-concepts.html) （DSP System Toolbox）。

#### 编程使用

| **模块参数：** InputProcessing                     |
| ---------------------------------------------------- |
| **类型：** 字符向量                                  |
| **值：** 'Columns as channels (frame based)'       |
| **默认值：** 'Elements as channels (sample based)' | -->

<div class="details-box">
<details open>
<summary>输出的数据类型 — 输出的数据类型<div>“boolean” （默认） | “Inherit: auto”</div></summary>
</details>
<div class="details-content">

将输出数据类型设置为 boolean 或 Inherit: auto。

</div>
</div>


<!-- 暂无
#### 编程使用

| **模块参数：** OutDataTypeStr |
| ------------------------------- |
| **类型：** 字符向量             |
| **值：** 'boolean'            |
| **默认值：** 'boolean'        | -->



<!-- 不确定
## 模块特性

| **数据类型**     | Boolean | double | fixed point | integer | single |
| ---------------- | --------- | -------- | ------------- | --------- | -------- |
| **直接馈通**     | yes     |          |               |           |          |
| **多维信号**     | yes     |          |               |           |          |
| **可变大小信号** | yes     |          |               |           |          |
| **零交叉检测**   | no      |          |               |           |          | -->


## 版本历史记录

- 在 2024b 之前推出

### 限制信息

1. 暂不支持对输入指定基于采样或基于帧的处理；  
2. 输入信号暂不支持 int64 和 uint64 的数据类型，输出信号暂不支持 float、double、int8、int16、int32、int64、uint8、uint16、uint32、uint64、fixedPoint、enum 和 bus 的数据类型。

<!--暂无 
## 扩展功能

### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 和 C++ 代码。

在特定条件下，生成的代码依赖于 memcpy 或 memset 函数（string.h）。

### HDL 代码生成 使用 HDL Coder™ 生成用于 FPGA 和 ASIC 设计的 Verilog 和 VHDL 代码。

HDL Coder™ 提供额外的配置选项，这些选项影响 HDL 实现和综合逻辑。

**HDL 架构**

此模块具有一个默认 HDL 架构。

**HDL 块属性**

| **ConstrainedOutputPipeline** | 通过移动设计中现有的延迟来放置在输出端的寄存器数量。分布式流水线处理不会重新分配这些寄存器。默认值为 0。更多详情，请参阅 [ConstrainedOutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#btp8gmp) (HDL Coder)。 |
| ----------------------------- | ------------------------------------------------------------ |
| **InputPipeline**             | 在生成的代码中插入的输入流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 0。更多详情，请参阅 [InputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-25) (HDL Coder)。 |
| **OutputPipeline**            | 在生成的代码中插入的输出流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 0。更多详情，请参阅 [OutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-26) (HDL Coder)。 |

### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。

### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。

## 版本历史

**在 R2006a 之前推出** -->

## 另请参阅

[DetectDecrease](DetectDecrease.html) | [DetectChange](DetectChange.html) | [DetectFallNonpositive](DetectFallNonpositive.html) | [DetectIncrease](DetectIncrease.html) | [DetectRiseNonnegative](DetectRiseNonnegative.html) | [DetectRisePositive](DetectRisePositive.html)