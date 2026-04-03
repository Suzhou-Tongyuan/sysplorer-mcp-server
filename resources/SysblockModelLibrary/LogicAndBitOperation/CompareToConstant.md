# CompareToConstant
---
&nbsp;

确定信号与指定常量的比较方式

**库：** Sysblock模块库 / LogicAndBitOperation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/CompareToConstant/CompareToConstant.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

CompareToConstant 模块用于将输入信号与常量进行比较。在**常量值**参数中指定常量。使用**运算符**参数指定输入与常量值的比较方式。

## 示例

<!-- 暂无
[![Illustration of Law of Large Numbers](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink_features/win64/IllustrationOfLawOfLargeNumbersExample_01.png)Illustration of Law of Large NumbersUse MATLAB System blocks to illustrate the law of large numbers.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/illustration-of-law-of-large-numbers.html) -->

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/CompareToConstant.mo">CompareToConstant.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/CompareToConstant/CompareToConstant_ex.png')" style="width: 600px; transform: scale(0.8);">

### 示例说明

- Step 模块：用于提供随时间变化的输入信号。在这个例子中，信号从 0 开始，在仿真开始时立即跳变到 1；
- CompareToConstant 模块：用于将输入信号与一个预设的常量值进行比较。在这个例子中，常量值设置为 0.5；
- Scope 模块：用于显示模型的输出。在这个例子中，它显示了比较操作的结果，即输入信号是否大于常量值 0.5。

## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量</div></summary>
</details>
<div class="details-content">

输入信号，指定为标量，与零进行比较。该模块首先将其**常量值**参数转换为输入数据类型，然后执行指定的运算。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | fixedPoint | enum

</div>
</div>


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

- == - 确定输入是否等于指定的常量；
- ~= - 确定输入是否不等于指定的常量；
- < - 确定输入是否小于指定的常量；
- <= - 确定输入是否小于或等于指定的常量；
- \> - 确定输入是否大于指定的常量；
- \>= - 确定输入是否大于或等于指定的常量。

</div>
</div>


<!-- 暂无
#### 编程用法

| **模块参数**：relop                                 |
| ----------------------------------------------------- |
| **类型**：字符向量                                    |
| **值**：'==' | '~='| '<' |'<='| '>='| '>' |
| **默认值**：'<='                                    | -->


<div class="details-box">
<details open>
<summary>常量值 — 要与之比较的常量<div>常量</div></summary>
</details>
<div class="details-content">

指定与输入进行比较的常量值。

</div>
</div>



<!-- 暂无
#### 编程用法

| **模块参数**：const                    |
| ---------------------------------------- |
| **类型**：字符向量                       |
| **值：**标量 \| 向量 \| 矩阵 \| N 维数组 |
| **默认值**：'3.0'                      | -->


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
| **值**：'boolean' | 'uint8' |
| **默认值**：'boolean'         | -->


<!-- 暂无
### 启用过零检测 — 选择此项以启用过零检测 'on' （默认） | 'off'


选择此项以启用过零检测。有关详细信息，请参阅 中的[过零检测]()。

#### 编程用法

| **模块参数**：ZeroCross |
| ------------------------- |
| **类型**：字符向量        |
| **值**：'off' | 'on'  |
| **默认值**：'on'        | -->


<!-- 不确定
## 模块特性

| **数据类型**     | Boolean \| double \| enumerated \| fixed point \| half \| integer \| single |
| ---------------- | ------------------------------------------------------------ |
| **直接馈通**     | 是                                                         |
| **多维信号**     | 是                                                         |
| **可变大小信号** | 是                                                         |
| **过零检测**     | 是                                                         | -->

## 版本历史记录

- 在 2024b 之前推出

### 限制信息    

1. 暂不支持启用过零检测；  
2. 输入端口暂不支持 half、int64、uint64 和 bus 的数据类型，输出端口暂不支持 uint8 的数据类型。

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

**复数数据支持**

此模块支持复信号的代码生成。


### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。


### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。

## 版本历史记录

**在 R2006a 之前推出** -->


## 另请参阅

[CompareToZero](CompareToZero.html) | [LogicalOperator](LogicalOperator.html)
 <!-- | [Combinatorial Logic]() -->