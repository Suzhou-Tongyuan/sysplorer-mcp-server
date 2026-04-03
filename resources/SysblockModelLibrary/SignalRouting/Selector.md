# Selector
---
从向量、矩阵或多维信号中选择输入元素

**库：** Sysblock模块库 / SignalRouting

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/Selector/Selector.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

Selector 模块根据指定的索引提取输入向量、矩阵或多维信号的所选元素。提取的信号可以按不同于输入信号的方式进行组合。

基于您为**输入维数**参数输入的值，将显示一个索引设置表。表中的每一行对应于**输入维数**中的一个输入维度。对于每个维度，您可以定义要使用的信号元素。可将向量信号指定为一维信号，将矩阵信号指定为二维信号。

例如，假设一个 6 维信号具有从 1 开始的索引模式。Selector 模块对话框中的表将发生变化，使每个维度都有一个对应的行。如果如下表所示定义维度，则输出为 Y = U(1:end,2:6,[1,3,5],Idx4:Idx4+7,Idx5,Idx6(1):Idx6(2))，其中 Idx4、Idx5 和 Idx6 是维度 4、5 和 6 的索引端口。

| 行   | 索引选项                 | 索引      | 输出大小 |
| :--- | :----------------------- | :-------- | :------- |
| 1    | “全选”                 |/           |/          |
| 2    | “起始索引(对话框)”     | 2       | 5      |
| 3    | “索引向量(对话框)”     | [1,3,5] |/          |
| 4    | “起始索引(端口)”       |/           | 8      |
| 5    | “索引向量(端口)”       |/           |/          |
| 6    | “起始和结束索引(端口)” |/           |/          |

<!-- 有关定义和使用总线数组的详细信息，请参阅[使用总线数组组合非虚拟总线](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/combining-buses-into-an-array-of-buses.html)。 -->

<!-- ## 限制

- **索引**参数在仿真期间不可调。如果维度的**索引选项**设置为“索引向量(对话框)” 或“起始索引(对话框)”，并且您在模块对话框中为对应的**索引**指定了符号值，包括 [Simulink.Parameter](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/simulink.parameter.html) 对象，则仿真开始时的瞬时值将在整个仿真中使用，并且该参数将在生成代码中作为内联值出现。请参阅[使用模块参数值进行调优和试验](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/using-tunable-parameters.html)。您可以使用索引端口动态调整选择索引。 -->

## 示例

<!-- [![Selector 模块的索引选项](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/indexoptionswiththeselectorblockexample_01_zh_CN.png)Selector 模块的索引选项此示例显示两个 Selector 模块，它们具有相同类型的输入信号，但有两种不同**索引选项**设置。](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/index-options-with-selector-block.html)

[![可变大小信号基本操作](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/variablesizesignalbasicoperationsexample_01_zh_CN.png)可变大小信号基本操作此示例说明可变大小信号是如何生成的。它还说明了可对这些信号应用的一些操作。此示例旨在介绍与可变大小信号相关联的基本操作。](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/variable-size-signal-basic-operations.html)

[![Multimode Variable-Size Signal](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink_features/win64/MultimodeVariableSizeSignalExample_01.png)Multimode Variable-Size SignalHow to use different operation modes to correspond to different signal sizes.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/multimode-variable-size-signal.html)

[![Model Arrays of Buses](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink_features/win64/ModelingArraysOfBusesExample_01.png)Model Arrays of BusesUse arrays of buses to represent structured data compactly.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/modeling-arrays-of-buses.html) -->

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/Selector.mo">Selector.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/Selector/Selector_ex.png')" style="width: 600px; transform: scale(0.8);">


### 示例说明

- Constant 模块：提供固定的向量值作为输入信号，用于模拟实际输入向量值；
- Selector 模块：根据指定的索引从向量、矩阵或多维信号中选择输入元素。在这个示例中，我们使用 Selector 模块选择向量中的特定元素；
- Scope 模块：用于显示模型的输出结果，即从输入向量中选择的特定元素。



## 端口

### 输入


<div class="details-box">
<details open>
<summary>x — 输入信号<div>标量 | 向量 | 矩阵 | 多维</div></summary>
</details>
<div class="details-content">

输入信号，亦即输出信号的元素来源。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | enum

</div>
</div>




<!-- ### IndxN — 第 N 个索引信号 标量 | 向量 | 矩阵



外部端口，用于指定对应输出元素的选择的索引。

#### 依存关系

要启用外部索引端口，请在**索引选项**表的对应行中，将**索引选项**设置为“索引向量(端口)”、“起始索引(端口)” 或“起始和结束索引(端口)”。

**数据类型：** single | double | int8 | int16 | int32 | uint8 | uint16 | uint32 -->

### 输出


<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 向量 | 矩阵 | 多维</div></summary>
</details>
<div class="details-content">

根据选定或重新排序的输入信号元素生成的输出信号。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | enum

</div>
</div>




## 参数


<div class="details-box">
<details open>
<summary>输入维数 — 输入信号的维数<div>正整数常量</div></summary>
</details>
<div class="details-content">

指定输入信号的维度数。

</div>
</div>



<!-- #### 编程用法

| **模块参数**：NumberOfDimensions |
| ---------------------------------- |
| **类型：**字符向量                 |
| **值：**integer                  |
| **默认值：**'1'                  | -->


<div class="details-box">
<details open>
<summary>索引模式 — 索引模式<div>“从 1 开始” （默认） | “从 0 开始”</div></summary>
</details>
<div class="details-content">

指定索引模式。如果选择 从 1 开始，则索引 1 指定输入向量的第一个元素。如果选择 从 0 开始，则索引 0 指定输入向量的第一个元素。

</div>
</div>




<!-- #### 编程用法

| **模块参数**：IndexMode            |
| ------------------------------------ |
| **类型：**字符向量                   |
| **值**：'One-based' | 'Zero-based' |
| **默认值：**'One-based'            | -->


<div class="details-box">
<details open>
<summary>索引选项 — 元素的索引方法<div>“索引向量(对话框)” （默认） | “全选” | “索引向量(端口)” | “起始索引(对话框)” | “起始索引(端口)” | “起始和结束索引(端口)”</div></summary>
</details>
<div class="details-content">

按维度定义信号元素的索引方式。从列表中，选择：

- “全选”

  不需要进一步配置。所有元素都被选中。

- “索引向量(对话框)”

  启用**索引**列。输入元素索引向量。当输入信号大小可变时，请不要选择此选项。

- “索引向量(端口)”

  不需要进一步配置。

- “起始索引(对话框)”

  启用**索引**和**输出大小**列。在**索引**列中输入要选择的元素范围的起始索引，在**输出大小**列中输入要选择的元素数。当输入信号大小可变时，请不要选择此选项。

- “起始索引(端口)”

  启用**输出大小**列。在**输出大小**列中输入要选择的元素数。

- “起始和结束索引(端口)”

  不需要进一步配置。

  使用此选项将生成可变大小的输出信号。当您更新时，输出维度设置为与输入信号的维度相同。在执行过程中，将根据提供给索引的信号来更新输出维度。

  记录输出信号数据时，未选择的信号用 NaN 值填充。

可以根据需要显示**索引**和**输出大小**列。
**索引**和**输出大小**支持引用工作区变量。

</div>
</div>




<!-- #### 编程用法

| **模块参数**：IndexOptionArray                             |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值**：'Select all' | 'Index vector (dialog)' | 'Index option (port)' | 'Starting index (dialog)' | 'Starting index (port)' | Starting and ending indices (port) |
| **默认值：**'Index vector (dialog)'                        | -->


<div class="details-box">
<details open>
<summary>索引 — 元素的索引<div>1 （默认） | 整数</div></summary>
</details>
<div class="details-content">

如果**索引选项**设置为“索引向量(对话框)”，则输入所需的每个元素的索引。

如果**索引选项**设置为“起始索引(对话框)”，则输入要选择的元素范围的起始索引。

</div>
</div>




<!-- #### 编程用法

| **模块参数**：IndexParamArray |
| ------------------------------- |
| **类型：**字符向量              |
| **值：**元胞数组                |
| **默认值：**'{ }'             | -->



<div class="details-box">
<details open>
<summary>输出大小 — 模块输出信号的宽度<div>1 （默认） | 整数</div></summary>
</details>
<div class="details-content">

指定模块输出信号的宽度。

</div>
</div>




<!-- #### 编程用法

| **模块参数**：OutputSizeArray |
| ------------------------------- |
| **类型：**字符向量              |
| **值：**元胞数组                |
| **默认值：**'{ }'             | -->


<div class="details-box">
<details open>
<summary>输入端口大小 — 输入信号的宽度<div>1 （默认） | 整数</div></summary>
</details>
<div class="details-content">

指定一维信号的模块输入信号的宽度。输入 -1 将从驱动模块继承。

</div>
</div>




<!-- #### 编程用法

| **模块参数**：InputPortWidth |
| ------------------------------ |
| **类型：**字符向量             |
| **值：**integer              |
| **默认值：**'3'              | -->



<!-- ### 采样时间 — -1 以外的采样时间值 -1 （默认） | 标量 | 向量



将采样时间指定为 -1 以外的值。有关详细信息，请参阅[指定采样时间](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/how-to-specify-the-sample-time.html)。

#### 依存关系

此参数不可见，除非将其显式设置为 -1 以外的值。要了解详细信息，请参阅[不建议设置采样时间的模块](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/sampletimehiding.html)。

#### 编程用法

| **模块参数：**SampleTime     |
| ------------------------------ |
| **类型：**字符串标量或字符向量 |
| **默认值：**"-1"             | -->



<!-- ### 在加速仿真中检查超范围索引 — 在加速和快速加速仿真模式下检查超范围索引值的选项 off （默认） | on



选中此复选框可让 Simulink® 在加速或快速加速模式下进行仿真时检查是否有任何索引值超出输入信号的相关维度的有效索引范围。如果索引超出范围，Simulink 将停止仿真并显示错误消息。



**注意**

如果不选中此复选框，超出范围的索引值可能导致在加速或快速加速模式下仿真期间出现未定义的行为。



无论是否选中此复选框，在普通模式仿真期间 Simulink 都会执行此检查。

#### 编程用法

| **参数：**RuntimeRangeChecks |
| ------------------------------ |
| **类型：**字符向量             |
| **值**：'Off' | 'On'       |
| **默认值**：'Off'            | -->



<!-- ## 模块特性

| **数据类型**     | Boolean | double | enumerated | fixed point | half | integer | single |
| ---------------- | ------------------------------------------------------------ |
| **直接馈通**     | 否                                                         |
| **多维信号**     | 是                                                         |
| **可变大小信号** | 是                                                         |
| **过零检测**     | 否
                                                         | -->


## 版本历史记录

- 在 2024b 之前推出

### 限制信息

1. 暂不支持自定义采样时间；  
2. 暂不支持在加速仿真中检查超范围索引的复选框；  
3. 暂不支持第 N 个索引信号的输入端口；  
4. 输入和输出信号暂不支持 half、int64、uint64、fixedPoint、bus 和 image 的数据类型。

<!-- ## 扩展功能



### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 Verilog 代码和 VHDL 代码。



HDL Coder™ 提供影响 HDL 实现和综合逻辑的额外配置选项。

**HDL 架构**

此模块具有一个默认 HDL 架构。

**HDL 模块属性**

| 通用                          |                                                              |
| :---------------------------- | ------------------------------------------------------------ |
| **ConstrainedOutputPipeline** | 通过移动设计中现有延迟的方式来放置在输出端的寄存器的数量。分布式流水线处理不会重新分发这些寄存器。默认值为 0。有关详细信息，请参阅[ConstrainedOutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#btp8gmp) (HDL Coder)。 |
| **InputPipeline**             | 要在生成的代码中插入的输入流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 0。有关详细信息，请参阅[InputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-25) (HDL Coder)。 |
| **OutputPipeline**            | 要在生成的代码中插入的输出流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 0。有关详细信息，请参阅[OutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-26) (HDL Coder)。 |

| 本机浮点            |                                                              |
| :------------------ | ------------------------------------------------------------ |
| **LatencyStrategy** | 指定对于浮点运算符是否将设计中的模块映射到 inherit、Max、Min 或 Zero。默认值为 “inherit”。另请参阅[LatencyStrategy](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/hdl-block-properties-native-floating-point.html#mw_a99b0822-f2a6-4f5b-aca9-7f7251a67c7c) (HDL Coder)。 |

**复数数据支持**

此模块支持复信号的代码生成。



### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。

## 版本历史记录

**在 R2006a 之前推出** -->

## 另请参阅

<!-- [Assignment](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/assignment.html) |  -->
[Switch](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SignalRouting/Switch.html) | [BusSelector](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SignalRouting/BusSelector.html)