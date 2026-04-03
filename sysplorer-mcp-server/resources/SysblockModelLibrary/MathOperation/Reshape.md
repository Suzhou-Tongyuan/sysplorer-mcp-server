# Reshape
---
&nbsp;

更改信号的维度


- **库：** Sysblock / MathOperation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/Reshape/Reshape.png')" style="width: 100px; height: auto;">

## 描述

Reshape 模块可以使用**输出维度**参数，将输入信号的维度更改为您指定的维度。例如，您可以使用该模块将 N 元素向量更改为 1×N 或 N×1 矩阵信号。

## 示例
将一个维度为 6 的信号更改为 2×3。Reshape 模块输出维度设置为自定义[2,3]。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperation/Reshape.mo">Reshape.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/Reshape/Reshape01.png')" style="width: 600px; ">


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

输入信号，其维度根据**输出维度**参数而更改。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | Boolean | fixed point 

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

使用**输出维度**参数中指定的维度创建的输出信号。

**数据类型：**  float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | Boolean | fixed point 

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>输出维度 — 输出信号的维度<div>一维数组（默认） | 列向量(二维) | 行向量(二维) | 自定义 | 从引用输入端口派生</div></summary>
</details>
<div class="details-content">

指定输出信号的维度。

| 输出维度           | 描述                                                         |
| :----------------- | :----------------------------------------------------------- |
| 一维数组           | 将多维数组转换为向量（1 维数组）数组信号。输出向量包含输入矩阵的第一列，后接第二列，以此类推。（此选项会保留向量输入不变。） |
| 列向量             | 将向量、矩阵或多维输入信号转换为列矩阵，即一个 M×1 矩阵，其中 M 是输入信号中的元素数。对于矩阵，转换是按列优先顺序进行的。对于多维数组，转换从第一个维度开始进行。 |
| 行向量             | 将向量、矩阵或多维输入信号转换为行矩阵，即一个 1×N 矩阵，其中 N 是输入信号中的元素数。对于矩阵，转换是按列优先顺序进行的。对于多维数组，转换从第一个维度开始进行。 |
| 自定义             | 将输入信号转换为输出信号，其维度可使用**输出维度**参数来指定。 |
| 从引用输入端口派生 | 在模块中创建另一个输入端口 **Ref**。输出信号的维度派生自 Ref 输入端口的输入信号的维度。选择此选项将禁用**输出维度**参数。如果选择此参数，**U** 和 **Ref** 这两个输入端口的输入信号必须具有相同的采样模式（基于采样或基于帧）。 |

</div>
</div>





<!-- 
#### 编程用法

| **模块参数**：`OutputDimensionality`                         |
| ------------------------------------------------------------ |
| **类型**：字符向量                                           |
| **值**：`'1-D array'` | `'Column vector (2-D)'` | `'Row vector (2-D)'` | `'Customize'` | `'Derive from reference input port'` |
| **默认值**：`'1-D array'`                                    | -->



<div id="输出维度—输出信号的自定义维度" class="jump-target"></div>
<div class="details-box">
<details open>
<summary>输出维度 — 输出信号的自定义维度<div>[1,1]（默认） | [integer] | [integer,integer]</div></summary>
</details>
<div class="details-content">

指定输出信号的维度。该值可以是一元素或多元素向量。值为 `[N]` 将输出大小为 `N` 的向量。值为 `[M N]` 将输出 `M`×`N` 矩阵。输入信号中的元素数必须与**输出维度**参数指定的元素数相匹配。对于多维数组，转换从第一个维度开始进行。

#### 依存关系

要启用此参数，请将**输出维度**设置为**自定义**。

</div>
</div>


<!-- 
#### 编程用法

| **模块参数**：`OutputDimensions` |
| -------------------------------- |
| **类型**：字符向量               |
| **值**：`'[integer,intger]'` \|  |
| **默认值**：`'[1,1]'`            | -->

<!-- ## 模块特性 -->

<!--部分特性暂无 
| **数据类型**     | `Boolean` | `bus` | `double` | `enumerated` | `fixed point` | `integer` | `single` |
| ---------------- | ------------------------------------------------------------ |
| **直接馈通**     | `是`                                                         |
| **多维信号**     | `是`                                                         |
| **可变大小信号** | `是`                                                         |
| **过零检测**     | `否`                                                         | -->

<!-- ## 扩展功能 -->


<!-- 
### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 Verilog 代码和 VHDL 代码。



HDL Coder™ 提供影响 HDL 实现和综合逻辑的额外配置选项。

**HDL 架构**

此模块具有一个默认 HDL 架构。

**HDL 模块属性**

| **ConstrainedOutputPipeline** | 通过移动设计中现有延迟的方式来放置在输出端的寄存器的数量。分布式流水线处理不会重新分发这些寄存器。默认值为 `0`。有关详细信息，请参阅[ConstrainedOutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#btp8gmp) (HDL Coder)。 |
| ----------------------------- | ------------------------------------------------------------ |
| **InputPipeline**             | 要在生成的代码中插入的输入流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 `0`。有关详细信息，请参阅[InputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-25) (HDL Coder)。 |
| **OutputPipeline**            | 要在生成的代码中插入的输出流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 `0`。有关详细信息，请参阅[OutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-26) (HDL Coder)。 |

**复数数据支持**

此模块支持复信号的代码生成。

**FOR-GENERATE 循环支持**

对于此模块，HDL Coder 在您将目标语言设置为 VHDL® 时使用 `FOR-GENERATE` 循环生成代码。

当目标语言为 Verilog® 时，会生成循环展开的代码。有关详细信息，请参阅[Unroll For-Generate Loops in VHDL Code](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/rtl-style.html#buiuh3k-196) (HDL Coder)。



### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。 -->

## 版本历史记录
 
- 在 2024b 之前推出

<!-- 
### 限制信息
暂无

## 另请参阅


### 主题  -->

