# LogicalOperator
---
&nbsp;

对输入执行指定的逻辑运算

**库：** Sysblock模块库 / LogicAndBitOperation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/LogicalOperator/LogicalOperator.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

LogicalOperator 模块对其输入执行指定的逻辑运算。输入值为非零值时为 true (1)，为零时则为 false (0)。

使用**运算符**参数列表选择连接输入的布尔运算。
<!--暂无
 如果您选择“矩形”作为**图标形状**属性，所选运算符的名称将显示在模块图标上。如果您选择“不同”作为**图标形状**属性，则 -->
所选运算符的名称不会显示在模块图标上。下表显示了支持的运算：

| 运算 | 描述                                  |
| :--- | :------------------------------------ |
| 与  | 如果所有输入均为 TRUE，则为 TRUE      |
| 或   | 如果至少有一个输入为 TRUE，则为 TRUE  |
| 与非 | 如果至少有一个输入为 FALSE，则为 TRUE |
| 或非  | 如果所有输入均不为 TRUE，则为 TRUE    |
| 异或  | 如果有奇数个输入为 TRUE，则为 TRUE    |
| 同或 | 如果有偶数个输入为 TRUE，则为 TRUE    |
| 非  | 如果输入为 FALSE，则为 TRUE           |

<!-- 暂无
如果选择“不同”作为**图标形状**，则模块的外观会指示其功能。Simulink® 软件将按照 IEEE® 逻辑函数的图形符号标准，显示所选运算符的独特形状。

![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/logical_operator_shapes.png) -->

要指定输入端口的数量，请使用**输入端口数目**参数。使用**输出数据类型**参数指定输出类型。如果为 TRUE，则输出值为 1，如果为 FALSE，则输出值为 0。

::: warning 注意 
输出数据类型应该准确表示零。满足此条件的数据类型包括有符号整数和无符号整数，以及所有浮点数据类型。
:::

输出大小取决于输入向量大小和所选运算符：

- 如果模块有多个输入，则任何非标量输入都必须具有相同的维度。例如，如果有任何输入是 2×2 数组，则所有其他非标量输入也必须是 2×2 数组。

  标量输入将扩展为与非标量输入具有相同的维度。

  如果模块有多个输入，则输出与输入具有相同的维度（标量扩展后），并且每个输出元素都是将指定逻辑运算应用于相应输入元素的结果。例如，如果指定运算为 AND，输入为 2×2 数组，则输出为 2×2 数组，其左上角的元素是将 与 应用于输入的左上角元素的结果，以此类推；

- 对于单个向量输入，模块会将运算（除 非 运算符外）应用于向量的所有元素。输出始终为标量；

- 非 运算符仅接受一个输入，该输入可以是标量也可以是向量。如果输入为向量，则输出为相同大小的向量，其中包含输入向量元素的逻辑补码。

当配置为多输入 异或 门时，此模块将按照 IEEE 逻辑元素标准的规定执行加法双模运算。


## 示例

<!-- 暂无
[![容错燃油控制系统建模](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/modelingafaulttolerantfuelcontrolsystemexample_02_zh_CN.png)容错燃油控制系统建模此示例说明如何结合使用 Stateflow® 和 Simulink® 来高效地进行混合系统建模。这种类型的建模对于具有基于离散事件的多种可能运行模式的系统特别有用。传统的信号流在 Simulink 中处理，而控制配置的更改在 Stateflow 中实现。下面所述的模型表示汽油引擎的燃油控制系统。该系统具有很强的稳健性，因为它可以检测到单个传感器的故障，并且可以动态重新配置控制系统以实现不间断运行。](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/modeling-a-fault-tolerant-fuel-control-system.html)

[![带紧急刹车的摩擦模型](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/sldemo_hardstopexample_02_zh_CN.png)带紧急刹车的摩擦模型此示例介绍了一种在 Simulink® 中对摩擦建模的方式。模型中的两个积分器用于计算系统的速度和位置，然后将计算结果用于在 Friction Model 中计算摩擦力。](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/friction-model-with-hard-stops.html)

[![Building a Clutch Lock-Up Model](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink_automotive/win64/BuildingAClutchLockUpModelExample_07.png)Building a Clutch Lock-Up ModelUse Simulink® to model and simulate a rotating clutch system. Although modeling a clutch system is difficult because of topological changes in the system dynamics during lockup, this example shows how Simulink's enabled subsystems easily handle such problems. We illustrate how to employ important Simulink modeling concepts in the creation of the clutch simulation. Designers can apply these concepts to many models with strong discontinuities and constraints that may change dynamically.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/building-a-clutch-lock-up-model.html) -->

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/LogicalOperator.mo">LogicalOperator.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/LogicalOperator/LogicalOperator_ex.png')" style="width: 600px;transform: scale(0.8);">

### 示例说明

- Constant 模块：提供固定的布尔值输入信号。在这个例子中，一个为 true，另一个为 false；
- LogicalOperator 模块：执行逻辑运算。根据配置的运算符（如‘与’、‘或’等），该模块将对输入信号进行逻辑运算；
- Scope 模块：用于显示模型的输出结果，即逻辑运算的结果。

## 端口

### 输入

<div class="details-box">
<details open>
<summary>u1 — 第一个输入信号 <div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

第一个输入信号，指定为标量、向量或矩阵。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | fixedPoint

</div>
</div>




<div class="details-box">
<details open>
<summary>u2 — 第二个输入信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

第二个输入信号，指定为标量、向量或矩阵。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | fixedPoint

</div>
</div>





<div class="details-box">
<details open>
<summary>uN — 第 N 个输入信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

第 N 个输入信号，指定为标量、向量或矩阵。

**依存关系：** 要启用其他输入端口，请使用**输入端口数目**参数。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | fixedPoint

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

输出信号，由 0 和 1 组成，具有与输入相同的维度。您可以使用
<!-- 暂无
**要求所有输入和输出具有相同的数据类型**和 -->
**输出数据类型**参数控制输出数据类型。

**数据类型：** boolean | fixedPoint

</div>
</div>





## 参数

### 主要

<div class="details-box">
<details open>
<summary>运算符 — 逻辑运算符<div>“与” （默认） | “或” | “与非” | “或非” | “异或” | “同或” | “非”</div></summary>
</details>
<div class="details-content">

选择要应用于模块输入的逻辑运算符。

- “与” - 如果所有输入都为 TRUE，则为 TRUE；
- “或” - 如果至少有一个输入为 TRUE，则为 TRUE；
- “与非” - 如果至少有一个输入为 FALSE，则为 TRUE；
- “或非” - 如果所有输入均不为 TRUE，则为 TRUE；
- “异或” - 如果有奇数个输入为 TRUE，则为 TRUE；
- “同或” - 如果有偶数个输入为 TRUE，则为 TRUE；
- “非” - 如果输入为 FALSE，则为 TRUE。

</div>
</div>


<!-- 暂无
#### 编程用法

| **模块参数**：Operator                                     |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值：**'与' | '或' | '与非' | '或非' | '异或' | '同或' | '非' |
| **默认值：**'与'                                          | -->


<div class="details-box">
<details open>
<summary>输入端口数目 — 输入的数目<div>2 （默认） | 正整数</div></summary>
</details>
<div class="details-content">

将模块输入的个数指定为正整数。

**依存关系：** 将**运算符**设置为 “非” 时，此参数不可用。

</div>
</div>



<!-- 暂无
#### 编程用法

| **模块参数**：Inputs |
| ---------------------- |
| **类型：**字符向量     |
| **值：**正整数         |
| **默认值：**'2'      | -->




<!-- 暂无
### 图标形状 — 图标形状 “矩形” （默认） | “不同”



指定模块图标的形状。

- “矩形” - 生成显示所选运算符名称的矩形模块。
- “不同” - 按照 IEEE 标准针对所选运算符使用图形符号。

#### 编程用法

| **模块参数**：IconShape               |
| --------------------------------------- |
| **类型：**字符向量                      |
| **值**：'rectangular' | 'distinctive' |
| **默认值：**'rectangular'             | -->


<!-- 暂无
### 采样时间 — -1 以外的采样时间值 -1 （默认） | 标量 | 向量



将采样时间指定为 -1 以外的值。有关详细信息，请参阅[指定采样时间](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/how-to-specify-the-sample-time.html)。

#### 依存关系

此参数不可见，除非将其显式设置为 -1 以外的值。要了解详细信息，请参阅[不建议设置采样时间的模块](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/sampletimehiding.html)。

#### 编程用法

| **模块参数：**SampleTime     |
| ------------------------------ |
| **类型：**字符串标量或字符向量 |
| **默认值：**"-1"             | -->

### 数据类型


<!-- 暂无
### 要求所有输入和输出具有相同的数据类型 — 要求所有端口具有相同的数据类型 off （默认） | on



若要求所有模块输入和输出具有相同的数据类型，请选中此复选框。清除此复选框后，输入和输出可以具有不同数据类型。

#### 编程用法

| **模块参数**：AllPortsSameDT |
| ------------------------------ |
| **类型：**字符向量             |
| **值：**'off' | 'on          |
| **默认值：**'off'            | -->


<div class="details-box">
<details open>
<summary>输出数据类型 — 输出数据类型<div>“boolean” （默认） | “Inherit: Logical（请参阅配置参数：优化）” | “fixdt(1,16,0)” | “fixdt(1,16,2^0,0)” | “fixdt(1,16,1.0,0,0.0)”</div></summary>
</details>
<div class="details-content">

指定输出数据类型。各选项的意义如下：

- “boolean” - 模块输出的数据类型为 boolean；

- “Inherit: Logical（请参阅配置参数：优化）” - 模块使用**将逻辑信号实现为布尔数据**配置参数指定输出数据类型；
<!-- 暂无
（请参阅[将逻辑信号实现为布尔数据(而不是双精度数据)](https://ww2.mathworks.cn/help/releases/R2022b/simulink/gui/implement-logic-signals-as-boolean-data-vs-double.html)）。 -->

  

  ::: warning 注意 
  此选项支持在 boolean 选项可用之前创建的模型。对于新模型，请使用其他选项之一，首选 boolean。
  :::


- “fixdt(1,16)” - 模块输出具有指定的定点数据类型 fixdt(1,16)；
- “fixdt(1,16,2^0,0)” - 模块输出具有指定的定点数据类型 fixdt(1,16,2^0,0)；
- “fixdt(1,16,1.0,0,0.0)” - 模块输出具有指定的定点数据类型 fixdt(1,16,1.0,0,0.0)。


  

::: tip 提示 
单击**显示数据类型帮助**按钮 <img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/LogicalOperator/LogicalOperator_button.png')" style="width: 80px; height: auto; vertical-align:middle; display:inline; margin:0;"> 以显示**数据类型帮助**，帮助您设置数据类型属性。 

  <!-- 有关详细信息，请参阅[使用数据类型助手指定数据类型]()。 -->

  :::

</div>
</div>

 <!-- 暂无
  | “<data type expression>” -->





  


<!-- 暂无
- “<data type expression>” - 模块输出具有您指定为数据类型表达式的数据类型，例如 Simulink.NumericType。

  

  **提示**

  要输入内置数据类型（double、single、int8、uint8、int16、uint16、int32 或 uint32），请将表达式用单引号引起来。例如，输入 'double' 而不是 double。 -->

<!-- 暂无
#### 编程用法

| **模块参数**：OutDataTypeStr                               |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值：**'Inherit: Logical (see Configuration Parameters: Optimization)' | 'boolean' | 'fixdt(1,16)' | '<data type expression>' |
| **默认值：**'boolean'                                      | -->

<!-- 不确定
## 模块特性

| **数据类型**     | Boolean | double | fixed point | float | integer | single |
| ---------------- | ------------------------------------------------------------ |
| **直接馈通**     | 是                                                         |
| **多维信号**     | 是                                                         |
| **可变大小信号** | 是                                                         |
| **过零检测**     | 否                                                         | -->

## 版本历史记录

- 在 2024b 之前推出

### 限制信息

1. 暂不支持不同的图标形状；  
2. 暂不支持自定义采样时间；  
3. 暂不支持要求所有输入和输出具有相同的数据类型；  
4. 暂不支持 data type expression 输出数据类型；   
5. 输入信号暂不支持 int64、uint64 和 enum 的数据类型，输出信号暂不支持 uint8 的数据类型。

<!-- 暂无
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



### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。

## 版本历史记录

**在 R2006a 之前推出** -->

## 另请参阅

[RelationalOperator](RelationalOperator.html) 
<!-- | [Combinatorial Logic]() | [将逻辑信号实现为布尔数据(而不是双精度数据)]() -->