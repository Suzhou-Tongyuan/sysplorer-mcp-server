# CompareToZero
---
&nbsp;

确定信号与零的比较方式

**库：** Sysblock模块库 / LogicAndBitOperation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/CompareToZero/CompareToZero.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

CompareToZero 模块将输入信号与零进行比较。使用**运算符**参数指定输入与零的比较方式。

如果比较结果为 false，输出为 0；如果比较结果为 true，输出为 1。

## 示例

<!-- 暂无
[![可变大小信号基本操作](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/variablesizesignalbasicoperationsexample_01_zh_CN.png)可变大小信号基本操作此示例说明可变大小信号是如何生成的。它还说明了可对这些信号应用的一些操作。此示例旨在介绍与可变大小信号相关联的基本操作。](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/variable-size-signal-basic-operations.html)

[![View Sequential Logic Through State Transition Matrix](https://ww2.mathworks.cn/help/releases/R2022b/examples/stateflow/win64/sf_debouncer_stm.png)View Sequential Logic Through State Transition MatrixUse the State Transition Matrix view for a state transition table in Stateflow®. Instead of drawing states and transitions graphically in a Stateflow chart, use state transition tables to express the modal logic in tabular format. State transition tables are supported only as blocks in a Simulink® model. For more information, see Stateflow 中的状态转移表 (Stateflow).](https://ww2.mathworks.cn/help/releases/R2022b/stateflow/ug/state-transition-matrix-view-for-state-transition-tables.html) -->

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/CompareToZero.mo">CompareToZero.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/CompareToZero/CompareToZero_ex.png')" style="width: 600px;transform: scale(0.8);">

### 示例说明

- SineWave 模块：用于产生一个正弦波信号，该信号周期性地穿过零点；
- CompareToZero 模块：用于检测输入信号何时穿过零点。当输入信号的值从正变负或从负变正时，即与零进行比较，如果输入信号等于零，则输出 1（真）；
- Scope 模块：用于显示模型的输出。在这个例子中，它显示了零点检测的结果，即正弦波信号何时穿过零点。

## 端口

### 输入


<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量</div></summary>
</details>
<div class="details-content">

输入信号，指定为标量，与零进行比较。如果输入数据类型不能表示零，将发生参数溢出。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | fixedPoint

</div>
</div>



<!-- 暂无
要检测此溢出，请转到“配置参数”对话框的**诊断 > 数据有效性**窗格，并将**参数 > 检测上溢**设置为“警告”或“错误”。

在这种情况下，模块将输入信号与输入数据类型的*接地值*进行比较。例如，如果输入信号的类型为 fixdt(0,8,2^0,10)，由于偏差为 10，输入数据类型可以表示从 10 到 265 的无符号 8 位整数。接地值为 10，而不是 0。 -->



### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>0 | 1</div></summary>
</details>
<div class="details-content">

如果比较结果为 false，输出为 0；如果比较结果为 true，输出为 1。

**数据类型：** boolean

</div>
</div>



## 参数


<div class="details-box">
<details open>
<summary>运算符 — 逻辑运算符<div><= （默认） | == | ~= | < | >= | ></div></summary>
</details>
<div class="details-content">

此参数可以具有以下值：

- == - 确定输入是否等于零；
- ~= - 确定输入是否不等于零；
- < - 确定输入是否小于零；
- <= - 确定输入是否小于或等于零；
- /> - 确定输入是否大于零；
- />= - 确定输入是否大于或等于零。


</div>
</div>


<!-- 暂无
#### 编程用法

| **模块参数**：relop                                 |
| ----------------------------------------------------- |
| **类型**：字符向量                                    |
| **值**：'==' \| '~='\| '<' \|'<='\| '>='\| '>' |
| **默认值**：'<='                                    | -->




<div class="details-box">
<details open>
<summary>输出数据类型 — 输出的数据类型<div>“boolean” （默认） | “Inherit: auto”</div></summary>
</details>
<div class="details-content">

指定输出的数据类型，boolean 或 Inherit: auto。

</div>
</div>





<!-- 暂无
#### 编程用法

| **模块参数**：OutDataTypeStr  |
| ------------------------------- |
| **类型**：字符向量              |
| **值**：'boolean' \| 'uint8' |
| **默认值**：'boolean'         | -->


<!-- 暂无
### 启用过零检测 — 选择此项以启用过零检测 on （默认） | off



选择此项以启用过零检测。有关详细信息，请参阅 中的[过零检测](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/zero-crossing-detection.html)。

#### 编程用法

| **模块参数**：ZeroCross |
| ------------------------- |
| **类型**：字符向量        |
| **值**：'off' \| 'on'  |
| **默认值**：'on'        | -->


<!-- 不确定
## 模块特性

| **数据类型**     | Boolean \| double \| fixed point \| half \| integer \| single |
| ---------------- | ------------------------------------------------------------ |
| **直接馈通**     | 是                                                         |
| **多维信号**     | 是                                                         |
| **可变大小信号** | 是                                                         |
| **过零检测**     | 是                                                         | -->

## 版本历史记录

- 在 2024b 之前推出

### 限制信息

1. 暂不支持启用过零检测；  
2. 输入信号暂不支持half、int64 和 uint64 的数据类型，输出信号暂不支持 uint8 的数据类型。

<!--暂无 

## 扩展功能



### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。



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

## 版本历史记录

**在 R2006a 之前推出** -->

## 另请参阅

[CompareToConstant](CompareToConstant.html) | [LogicalOperator](LogicalOperator.html) | [BitwiseOperator](BitwiseOperator.html)
 <!-- | [String Compare]() -->