# IntervalTestDynamic
---
&nbsp;

确定信号是否在指定的区间内

**库：** Sysblock模块库 / LogicAndBitOperation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/IntervalTestDynamic/IntervalTestDynamic.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

IntervalTestDynamic 模块用于判断输入信号是否位于外部信号 **up** 和 **lo** 指定的区间内。如果输入信号位于这两个值之间，模块输出真（1）；如果输入信号在这些值之外，则输出假（0）。通过使用“区间闭左”和“区间闭右”复选框，可以控制模块如何处理等于信号 **lo** 或信号 **up** 的输入值。

## 示例

<!-- 暂无
[![检测动态指定区间内的信号值](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink/win64/DetectValuesInDynamicallySpecifiedIntervalExample_02.png)检测动态指定区间内的信号值](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/detect-signal-values-within-dynamically-specified-interval.html)  -->

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/IntervalTestDynamic.mo">IntervalTestDynamic.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/IntervalTestDynamic/IntervalTestDynamic_ex.png')" style="width: 600px;transform: scale(0.8);">

### 示例说明

- SineWave 模块：提供动态变化的区间上下界和输入信号；
- IntervalTestDynamic 模块：动态检测输入信号是否在由外部信号定义的区间内。如果输入信号在上界和下界之间，输出 1（真）；如果不在这个区间内，输出 0（假）；
- Scope 模块：用于显示模型的输出结果，即信号是否在动态指定的区间内。


## 端口

### 输入

<div class="details-box">
<details open>
<summary>up — 区间上限<div>标量 | 向量 | 矩阵 | N 维数组</div></summary>
</details>
<div class="details-content">

区间的上限，可以是标量、向量、矩阵或N维数组。

**限制：** 当输入信号为枚举类型时，**up** 和 **lo** 信号必须为同一类型的枚举。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | fixedPoint | enum

</div>
</div>



<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 向量 | 矩阵 | N维数组</div></summary>
</details>
<div class="details-content">

输入信号，可以是标量、向量、矩阵或N维数组。

**限制：** 当输入信号为枚举类型时，**up** 和 **lo** 信号必须为同一类型的枚举。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | fixedPoint | enum

</div>
</div>


<div class="details-box">
<details open>
<summary>lo — 区间下限<div>标量 | 向量 | 矩阵 | N维数组</div></summary>
</details>
<div class="details-content">

区间的下限，可以是标量、向量、矩阵或N维数组。

**限制：** 当输入信号为枚举类型时，**up** 和 **lo** 信号必须为同一类型的枚举。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | fixedPoint | enum

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>0 | 1</div></summary>
</details>
<div class="details-content">

输出信号指示输入值是否落在指定的区间内。您可以将**输出数据类型**指定为 boolean 或 Inherit: auto。

**数据类型：** boolean

</div>
</div>




## 参数

<div class="details-box">
<details open>
<summary>右半闭区间 — 包含上限值<div>on （默认） | off</div></summary>
</details>
<div class="details-content">

当您选中此复选框时，与 **up** 输入端口相连的信号值将被包含在块输出真（1）的区间内。

</div>
</div>


<!-- 暂无
#### 编程使用

| **模块参数：** IntervalClosedRight |
| ------------------------------ |
| **类型：** 字符向量             |
| **值：** 'on' | 'off'         |
| **默认值：** 'on'               | -->

<div class="details-box">
<details open>
<summary>左半闭区间 — 包含下限值<div>on （默认） | off</div></summary>
</details>
<div class="details-content">

当您选中此复选框时，与 **lo** 输入端口相连的信号值将被包含在块输出真（1）的区间内。

</div>
</div>

<!-- 暂无
#### 编程使用

| **模块参数：** IntervalClosedLeft |
| ------------------------- |
| **类型：** 字符向量          |
| **值：** 'on' | 'off'     |
| **默认值：** 'on'          | -->


<div class="details-box">
<details open>
<summary>输出数据类型 — 输出数据类型<div>boolean （默认） | Inherit: auto</div></summary>
</details>
<div class="details-content">

指定输出数据类型为 boolean 或 Inherit: auto。

</div>
</div>


<!-- 暂无
#### 编程使用

| **模块参数：** OutDataTypeStr |
| -------------------------- |
| **类型：** 字符向量        |
| **值：** 'boolean' | 'uint8' |
| **默认值：** 'boolean'      | -->


<!-- 不确定
## 模块特性

| **数据类型**               | Boolean | double | enumerated | fixed point | integer | float |
| ------------------------- | ----------------------------------------------------------- |
| **直接馈通**               | yes                                                       |
| **多维信号**               | yes                                                       |
| **可变大小信号**            | no                                                        |
| **零交叉检测**             | no                                                        | -->


## 版本历史记录

- 在 2024b 之前推出

### 限制信息

区间上限暂不支持 int64 和 uint64 的数据类型，输入信号暂不支持 int64 和 uint64 的数据类型，区间下限暂不支持 int64 和 uint64 的数据类型，输出信号暂不支持 uint8 的数据类型。

<!-- 暂无
## 扩展功能

### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 和 C++ 代码。

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

[IntervalTest](IntervalTest.html)

