# RelationalOperator
---
&nbsp;

对输入执行指定的关系运算

**库：** Sysblock模块库 / LogicAndBitOperation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/RelationalOperator/RelationalOperator.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

RelationalOperator 模块对输入执行指定的关系运算。为**关系运算符**参数选择的值确定模块是接受一个还是两个输入信号。

### 双输入模式

默认情况下，RelationalOperator 模块使用您指定的**关系运算符**参数比较两个输入。第一个输入对应于上面的输入端口，第二个输入对应于下面的输入端口。
<!-- 暂无
（有关各种模块方向的端口顺序的描述，请参阅[旋转或翻转后的端口位置](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/changing-a-blocks-appearance.html#f13-83952)。） -->

您可以在双输入模式中指定以下运算之一：

| 运算 | 描述                                          |
| :--- | :-------------------------------------------- |
| == | 如果第一个输入等于第二个输入，则为 TRUE       |
| ~= | 如果第一个输入不等于第二个输入，则为 TRUE     |
| <  | 如果第一个输入小于第二个输入，则为 TRUE       |
| <= | 如果第一个输入小于或等于第二个输入，则为 TRUE |
| >= | 如果第一个输入大于或等于第二个输入，则为 TRUE |
| >  | 如果第一个输入大于第二个输入，则为 TRUE       |

您可以将输入指定为标量、数组或者标量与数组的组合。

| 对于...            | 输出为...                                                    |
| :----------------- | :----------------------------------------------------------- |
| 标量输入           | 标量                                                         |
| 数组输入           | 具有相同维度的数组，其中每个元素是对输入数组逐元素比较的结果 |
| 混合标量和数组输入 | 数组，其中每个元素是将标量与对应的数组元素进行比较的结果     |

对于正数范围较小的输入，将使用舍入到最邻近整数和饱和方法，脱机转换为另一个输入的数据类型。此转换发生在比较之前。

您可以使用**输出数据类型**参数指定输出的数据类型。如果为 true，则输出为 1；如果为 false，则输出为 0。

::: tip 提示 
选择准确表示零的输出数据类型。满足此条件的数据类型包括有符号整数和无符号整数，以及所有浮点数据类型。
:::



### 单输入模式

当您为**关系运算符**选择下列运算之一时，模块将切换到单输入模式。

| 运算       | 描述                        |
| :--------- | :-------------------------- |
| isInf    | 如果输入为 Inf，则为 TRUE |
| isNaN    | 如果输入为 NaN，则为 TRUE |
| isFin | 如果输入为有限值，则为 TRUE |

对于非浮点输入，模块将生成以下输出。

<table border="1">
    <tr>
        <th>数据类型</th>
        <th>运算</th>
        <th>模块输出</th>
    </tr>
    <tr>
        <td rowspan="3">定点<br>布尔<br>内置整数</td>
        <td>isInf</td>
        <td>false</td>
    </tr>
    <tr>
        <td>isNaN</td>
        <td>false</td>
    </tr>
    <tr>
        <td>isFinite</td>
        <td>true</td>
    </tr>
</table>

### 数据类型传播的规则

当您的模块有一个或多个输入端口未指定数据类型时，将按以下规则进行数据类型传播。

<table border="1">
    <tr>
        <th>当模块位于...</th>
        <th>而且...</th>
        <th>模块使用...</th>
    </tr>
    <tr>
        <td rowspan="2">双输入模式</td>
        <td>两个输入端口均未指定数据类型</td>
        <td>double 作为两个输入的默认数据类型</td>
    </tr>
    <tr>
        <td>一个输入端口未指定数据类型</td>
        <td>指定了数据类型的输入端口的数据类型作为另一个端口的默认数据类型</td>
    </tr>
    <tr>
        <td>单输入模式</td>
        <td>输入端口未指定数据类型</td>
        <td>double 作为输入的默认数据类型</td>
    </tr>
</table>


## 示例
<!-- 暂无
[![容错燃油控制系统建模](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/modelingafaulttolerantfuelcontrolsystemexample_02_zh_CN.png)容错燃油控制系统建模此示例说明如何结合使用 Stateflow® 和 Simulink® 来高效地进行混合系统建模。这种类型的建模对于具有基于离散事件的多种可能运行模式的系统特别有用。传统的信号流在 Simulink 中处理，而控制配置的更改在 Stateflow 中实现。下面所述的模型表示汽油引擎的燃油控制系统。该系统具有很强的稳健性，因为它可以检测到单个传感器的故障，并且可以动态重新配置控制系统以实现不间断运行。](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/modeling-a-fault-tolerant-fuel-control-system.html) -->

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/RelationalOperator.mo">RelationalOperator.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/RelationalOperator/RelationalOperator_ex.png')" style="width: 600px;transform: scale(0.8);">

### 示例说明

- Step 模块：提供两个不同的步进信号作为比较的输入；
- RelationalOperator 模块：根据设置的比较操作（例如小于 < ），比较两个输入信号，并输出布尔结果；
- Scope 模块：用于显示模型的输出结果，即比较操作的布尔值。

## 端口

### 输入


<div class="details-box">
<details open>
<summary>u1 — 第一个输入信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

第一个输入信号，指定为标量、向量或矩阵。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | fixedPoint | enum  

</div>
</div>





<div class="details-box">
<details open>
<summary>u2 — 第二个输入信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">


第二个输入信号，指定为标量、向量或矩阵。

**依存关系：**要启用此端口，请将**关系运算符**设置为 “==”、“~=”、“<”、“<=”、“>=” 或 “>”。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | fixedPoint | enum  

</div>
</div>




### 输出


<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

输出信号，由 0 和 1 组成，具有与输入相同的维度。使用**输出数据类型**参数控制输出数据类型。

**数据类型：** boolean | fixedPoint 

</div>
</div>



## 参数

### 主要


<div class="details-box">
<details open>
<summary>关系运算符 — 关系运算符<div>“<=” （默认） | “~=” | “==” | “<” | “>=” | “>” | “isInf” | “isNaN” | “isFin”</div></summary>
</details>
<div class="details-content">

指定比较两个输入的运算，或确定一个输入的信号类型。

- “==” - 如果第一个输入等于第二个输入，则为 TRUE；
- “~=” - 如果第一个输入不等于第二个输入，则为 TRUE；
- “<” - 如果第一个输入小于第二个输入，则为 TRUE；
- “<=” - 如果第一个输入小于或等于第二个输入，则为 TRUE；
- “>=” - 如果第一个输入大于或等于第二个输入，则为 TRUE；
- “>” - 如果第一个输入大于第二个输入，则为 TRUE；
- “isInf” - 如果输入为 Inf，则为 TRUE；
- “isNaN” - 如果输入为 NaN，则为 TRUE；
- “isFin” - 如果输入为有限值，则为 TRUE。

</div>
</div>




<!-- 暂无
#### 编程用法

| **模块参数**：Operator                                     |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值：**'==' | '~=' | '<' | '<=' | '>=' | '>' | 'isInf' | 'isNaN' | 'isFin' |
| **默认值：**'<='                                           | -->


<!-- 暂无
### 启用过零检测 — 启用过零检测 on （默认） | off



选择此项以启用过零检测。有关详细信息，请参阅[过零检测](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/zero-crossing-detection.html)。

#### 编程用法

| **参数：**ZeroCross      |
| -------------------------- |
| **类型：**字符向量、字符串 |
| **值：** 'on' | 'off'  |
| **默认值：**'on'         | -->


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
### 要求所有输入具有相同的数据类型 — 要求所有输入都有相同的数据类型 off （默认） | on



若要求所有模块输入具有相同的数据类型，请选中此复选框。清除此复选框后，输入可以具有不同数据类型。

#### 依存关系

将**关系运算符**设置为 “isInf”、“isNaN” 或 “isFin” 时，此复选框不可用，因为在这些模式下，模块只有一个输入端口。

#### 编程用法

| **模块参数**：InputSameDT |
| --------------------------- |
| **类型：**字符向量          |
| **值：**'off' | 'on       |
| **默认值：**'off'         | -->



 <!-- 暂无
  | “<data type expression>” -->
<div class="details-box">
<details open>
<summary>输出数据类型 — 输出数据类型<div>“boolean” （默认） | “Inherit: Logical（请参阅配置参数：优化）” | “fixdt(1,16,0)” | “fixdt(1,16,2^0,0)” | “fixdt(1,16,1.0,0,0.0)”</div></summary>
</details>
<div class="details-content">

指定输出数据类型。各选项的意义如下：

- “boolean” - 模块输出的数据类型为 boolean；

- “Inherit: Logical（请参阅配置参数：优化)” - 模块使用**将逻辑信号实现为布尔数据**配置参数指定输出数据类型；
<!-- 暂无
（请参阅[将逻辑信号实现为布尔数据(而不是双精度数据)](https://ww2.mathworks.cn/help/releases/R2022b/simulink/gui/implement-logic-signals-as-boolean-data-vs-double.html)）。 -->

  

  ::: warning 注意 
  此选项支持在 boolean 选项可用之前创建的模型。对于新模型，请使用其他选项之一，首选 boolean。
  :::


- “fixdt(1,16)” - 模块输出具有指定的定点数据类型 fixdt(1,16)；
- “fixdt(1,16,2^0,0)” - 模块输出具有指定的定点数据类型 fixdt(1,16,2^0,0)；
- “fixdt(1,16,1.0,0,0.0)” - 模块输出具有指定的定点数据类型 fixdt(1,16,1.0,0,0.0)。


  

::: tip 提示 
单击**显示数据类型帮助**按钮 <img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/RelationalOperator/RelationalOperator_button.png')" style="width: 8%; height: auto; vertical-align:middle; display:inline; margin:0;"> 以显示**数据类型帮助**，帮助您设置数据类型属性。  

<!-- 有关详细信息，请参阅[使用数据类型助手指定数据类型]()。 -->

:::

</div>
</div>




  


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


<!-- 暂无
### 整数舍入模式 — 定点运算的舍入模式 “最简” （默认） | “收敛” | “向下” | “最邻近值” | “舍入” | “向上” | “零”



指定定点运算的舍入模式。您可以选择：

- “向上”

  朝正无穷方向舍入正数和负数。等同于 MATLAB® ceil 函数。

- “收敛”

  将数值舍入到最邻近的可表示值。如果出现结值，则舍入到最邻近的偶数整数。等同于 Fixed-Point Designer™ convergent 函数。

- “向下”

  朝负无穷方向舍入正数和负数。等同于 MATLAB floor 函数。

- “最邻近值”

  将数值舍入到最邻近的可表示值。如果出现结值，则朝正无穷方向舍入。等同于 Fixed-Point Designer nearest 函数。

- “舍入”

  将数值舍入到最邻近的可表示值。如果出现结值，则将正数朝正无穷方向舍入，将负数朝负无穷方向舍入。等同于 Fixed-Point Designer round 函数。

- “最简”

  在向负无穷大方向舍入和向零舍入之间选择，以生成尽可能有效的舍入代码。

- “零”

  将数值向零舍入。等同于 MATLAB fix 函数。

有关详细信息，请参阅[舍入](https://ww2.mathworks.cn/help/releases/R2022b/fixedpoint/ug/rounding.html) (Fixed-Point Designer)。

#### 编程用法

| **模块参数**：RndMeth                                      |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值：**'Ceiling' | 'Convergent' | 'Floor' | 'Nearest' | 'Round' | 'Simplest' | 'Zero' |
| **默认值：**'Simplest'                                     | -->


<!-- 不确定
## 模块特性

| **数据类型**     | Boolean | double | enumerated | fixed point | half | integer | single |
| ---------------- | ------------------------------------------------------------ |
| **直接馈通**     | 是                                                         |
| **多维信号**     | 是                                                         |
| **可变大小信号** | 是                                                         |
| **过零检测**     | 是                                                         | -->


## 版本历史记录

- 在 2024b 之前推出

### 限制信息

1. 暂不支持启动过零检测；  
2. 暂不支持自定义采样时间；  
3. 暂不支持要求所有输入和输出具有相同的数据类型；  
4. 暂不支持 data type expression 输出数据类型；   
5. 输入信号暂不支持 int64、uint64 和 half 的数据类型，输出信号暂不支持 half、float、double、int8、int16、int32、int64、uint8、uint16、uint32、uint64 和 enum 的数据类型。

<!-- 暂无
## 扩展功能



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

| 本机浮点             |                                                              |
| :------------------- | ------------------------------------------------------------ |
| **LatencyStrategy**  | 指定对于浮点运算符是否将设计中的模块映射到 inherit、Max、Min、Zero 或 Custom。默认值为 “inherit”。另请参阅[LatencyStrategy](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/hdl-block-properties-native-floating-point.html#mw_a99b0822-f2a6-4f5b-aca9-7f7251a67c7c) (HDL Coder)。 |
| **NFPCustomLatency** | 要指定值，请将 **LatencyStrategy** 设置为 Custom。HDL Coder 会增加延迟，其值等于您为 **NFPCustomLatency** 设置指定的值。另请参阅[NFPCustomLatency](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/hdl-block-properties-native-floating-point.html#mw_e29db696-7117-431a-a8b8-4471b8d24ea8) (HDL Coder)。 |

**复数数据支持**

代码生成支持 ~= 和 == 运算符。



### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。

## 版本历史记录

**在 R2006a 之前推出** -->

## 另请参阅

[LogicalOperator](LogicalOperator.html)