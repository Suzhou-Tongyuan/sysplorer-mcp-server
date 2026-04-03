# DeMux
---
提取并输出虚拟向量信号的元素

**库：** Sysblock模块库 / SignalRouting

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/DeMux/DeMux.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

DeMux 模块提取输入向量信号的分量，再将它们输出为单独的信号。输出信号端口从上到下排列。

## 示例

<!-- [![提取向量元素并在输出上均匀分布](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/unspecifieddemuxblockexample_01_zh_CN.png)提取向量元素并在输出上均匀分布此示例说明如何使用 Demux 模块将输入信号均匀分布在所需数量的输出上。](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/extract-vector-elements-and-distribute-evenly-across-outputs.html)

[![Extract Vector Elements Using the Demux Block](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink/win64/SpecifiedDemuxBlockExample_01.png)Extract Vector Elements Using the Demux BlockWhen using the Demux block to extract and output elements from a vector input, you can use -1 in a vector expression to indicate that the block dynamically sizes the corresponding port.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/extract-vector-elements-using-demux-block.html)

[![Feedback System](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink/win64/FeedbackSystemExample_01.png)Feedback SystemDemonstrates a state-space system that has matrix signals:](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/feedback-system.html) -->

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/DeMux.mo">DeMux.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/DeMux/DeMux_ex.png')" style="width: 600px; transform: scale(0.8);">

### 示例说明

- Constant 模块：提供固定的向量值作为输入信号，用于模拟实际输入向量值；
- DeMux 模块：将输入向量信号分解成多个单独的信号。在这个示例中，我们将一个三元素向量分解成三个单独的信号；
- Scope 模块：用于显示模型的输出结果，即分解后的各个信号。

## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 接受要从中提取和输出信号的非总线向量信号<div>Scalar | Array1D | ColumnVector2D | RowVector2D</div></summary>
</details>
<div class="details-content">

DeMux 模块从中选择标量信号或更小向量的向量输入信号。

**数据类型：** float | double | int8 | int16 | int32| uint8 | uint16 | uint32 | boolean | fixedPoint | enum

</div>
</div>




### 输出


<div class="details-box">
<details open>
<summary>y1 — 输出从输入向量信号中提取的信号<div>Scalar | Array1D | ColumnVector2D | RowVector2D</div></summary>
</details>
<div class="details-content">

输出从输入向量中提取的信号。输出信号端口从上到下排列。
<!-- 有关各种模块方向的端口顺序的说明，请参阅[旋转或翻转后的端口位置](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/changing-a-blocks-appearance.html#f13-83952)。 -->

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | fixedPoint | enum 

</div>
</div>




<div class="details-box">
<details open>
<summary>y2 — 输出从输入向量信号中提取的信号<div>Scalar | Array1D | ColumnVector2D | RowVector2D</div></summary>
</details>
<div class="details-content">

输出从输入向量中提取的信号。输出信号端口从上到下排列。
<!-- 有关各种模块方向的端口顺序的说明，请参阅[旋转或翻转后的端口位置](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/changing-a-blocks-appearance.html#f13-83952)。 -->

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | fixedPoint | enum 

</div>
</div>




## 参数

<div class="details-box">
<details open>
<summary>输出数目 — 输出信号的数量<div>2 （默认） | 标量 </div></summary>
</details>
<div class="details-content">

输出信号的数量。该值需为正整数标量，且必须与输入信号的长度相匹配。


</div>
</div>



<!-- 有关示例，请参阅[提取向量元素并在输出上均匀分布](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/extract-vector-elements-and-distribute-evenly-across-outputs.html) 和[Extract Vector Elements Using the Demux Block](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/extract-vector-elements-using-demux-block.html)。 -->

<!-- #### 编程用法

| **模块参数：**Outputs    |
| -------------------------- |
| **类型：**标量或向量       |
| **值：**字符向量           |
| **默认值：**{'2'} 或向量 | -->



<!-- ### 显示选项 — 显示的模块图标 “bar” （默认） | “无”



默认情况下，模块图标是一个填充了模块前景颜色的实心条形。要将图标显示为一个包含模块类型名称的框，请选择“无”。

#### 编程用法

| **模块参数**：Display option |
| ------------------------------ |
| **类型：**字符向量             |
| **值：**'bar' | 'none'     |
| **默认值：**'bar'            | -->



<!-- ## 模块特性

| **数据类型**     | Boolean | double | enumerated | fixed point | half | integer | single |
| ---------------- | ------------------------------------------------------------ |
| **直接馈通**     | 是                                                         |
| **多维信号**     | 否                                                         |
| **可变大小信号** | 否                                                         |
| **过零检测**     | 否                                                         | -->

## 版本历史记录

- 在 2024b 之前推出

### 限制信息

1. 暂不支持显示选项的功能；  
2. 输入和输出端口暂不支持 half、int64、uint64 和 image 的数据类型；
3. 输出端口仅支持正整数标量输出。


<!-- ## 扩展功能



### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。

实际数据类型或功能支持取决于模块实现。



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 Verilog 代码和 VHDL 代码。



HDL Coder™ 提供影响 HDL 实现和综合逻辑的额外配置选项。

**HDL 架构**

此模块具有一个默认 HDL 架构。

**HDL 模块属性**

| **ConstrainedOutputPipeline** | 通过移动设计中现有延迟的方式来放置在输出端的寄存器的数量。分布式流水线处理不会重新分发这些寄存器。默认值为 0。有关详细信息，请参阅[ConstrainedOutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#btp8gmp) (HDL Coder)。 |
| ----------------------------- | ------------------------------------------------------------ |
| **InputPipeline**             | 要在生成的代码中插入的输入流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 0。有关详细信息，请参阅[InputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-25) (HDL Coder)。 |
| **OutputPipeline**            | 要在生成的代码中插入的输出流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 0。有关详细信息，请参阅[OutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-26) (HDL Coder)。 |

**复数数据支持**

此模块支持复信号的代码生成。



### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。

实际数据类型或功能支持取决于模块实现。

## 版本历史记录

**在 R2006a 之前推出** -->

## 另请参阅

[Selector](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SignalRouting/Selector.html)

<!-- 

[Mux](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/mux.html) | [Bus Creator](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/buscreator.html) | [Bus to Vector](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/bustovector.html)

### 主题

- [虚拟和非虚拟信号](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/signal-types.html#bq4ic6w-1)
- [合成接口规范](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/composite-signal-techniques.html)
- [Simplify Subsystem and Model Interfaces with Bus Element Ports](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/simplify-subsystem-bus-interfaces.html) -->