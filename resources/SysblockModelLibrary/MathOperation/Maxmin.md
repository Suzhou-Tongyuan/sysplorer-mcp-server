# Maxmin
---
&nbsp;

输出最小或最大输入值


- **库：** Sysblock / MathOperation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/Maxmin/Maxmin.png')" style="width: 100px; height: auto;">

## 描述

Maxmin 模块输出输入的最小或最大元素。您可以通过设置**函数**参数来选择模块是否输出最小值或最大值。

Maxmin 模块将忽略类型为 `NaN` 的任何输入值，除非每个输入值为 `NaN`。当所有输入值均为 `NaN` 时，输出为 `NaN`，要么是标量，要么是每个输出向量元素的值。

## 示例
输出两个值中的最大值。将两个 Constant 模块的值分别设置为 1 和 10，将 Maxmin 模块的函数设置为 max，输入端口为 2。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperation/Maxmin.mo">Maxmin.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/Maxmin/Maxmin01.png')" style="width: 600px; ">

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/Maxmin/Maxmin02.png')" style="width: 600px; ">


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u1 — 输入信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

提供输入信号，模块根据该输入信号输出最大值或最小值。

- 如果模块只有一个输入端口，则输入必须为标量或向量。模块将输出等于输入向量的最小或最大元素的标量。
- 如果模块有多个输入端口，则所有非标量输入都必须具有相同的维度。模块会扩展任何标量输入，使其与非标量输入具有相同的维度。模块将输出与输入具有相同维度的信号。每个输出元素等于对应输入元素的最小值或最大值。

#### 依存关系

要支持矩阵输入，您必须将**输入端口数目**参数设置为大于 1 的整数。所有的非标量输入信号必须具有相同的维度。

**数据类型：**  float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | Boolean | fixed point


</div>
</div>

<div class="details-box">
<details open>
<summary>u2 — 第 N 个输入信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

提供输入信号，模块根据该输入信号输出最大值或最小值。

如果模块有多个输入端口，则所有非标量输入都必须具有相同的维度。模块会扩展任何标量输入，使其与非标量输入具有相同的维度。模块将输出与输入具有相同维度的信号。每个输出元素等于对应输入元素的最小值或最大值。

#### 依存关系

要提供多个输入信号，请将**输入端口数目**设置为大于 1 的整数。

**数据类型：**  float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | Boolean | fixed point

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>y — 输入的最小值或最大值<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

当模块有一个输入时，输出是标量值，该标量等于输入元素的最小值或最大值。当模块有多个输入时，输出是与输入具有相同维度的信号。每个输出元素等于对应输入元素的最小值或最大值。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | Boolean | fixed point

</div>
</div>

## 参数


### 主要

<div class="details-box">
<details open>
<summary>函数 — 指定最小值或最大值<div>max（默认） | min</div></summary>
</details>
<div class="details-content">

指定对输入应用 min 函数还是 max 函数。

</div>
</div>

<!-- 
#### 编程用法

| **模块参数**：`Function` |
| ------------------------ |
| **类型：**字符向量       |
| **值：**`'min' | 'max'`  |
| **默认值：**`'min'`      | -->

<div class="details-box">
<details open>
<summary>输入端口个数 — 指定输入端口个数<div>2 （默认） | positive integer</div></summary>
</details>
<div class="details-content">

指定模块的输入数目。

</div>
</div>


<!-- #### 编程用法

| **模块参数**：`Inputs`     |
| -------------------------- |
| **类型：**字符向量         |
| **值：**`positive integer` |
| **默认值：**`'1'`          | -->


<!-- 暂无
### `启用过零检测` — 启用过零检测 `on` （默认） | `off`



选择此项以启用过零检测。有关详细信息，请参阅[过零检测](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/zero-crossing-detection.html)。

#### 编程用法

| **模块参数**：`ZeroCross`    |
| ---------------------------- |
| **类型**：字符向量 \| 字符串 |
| **值**：`'off'` | `'on'`     |
| **默认值**：`'on'`           | -->

<!-- 暂无

### `采样时间` — `-1` 以外的采样时间值 `-1` （默认） | 标量 | 向量



将采样时间指定为 `-1` 以外的值。有关详细信息，请参阅[指定采样时间](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/how-to-specify-the-sample-time.html)。

#### 依存关系

此参数不可见，除非将其显式设置为 `-1` 以外的值。要了解详细信息，请参阅[不建议设置采样时间的模块](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/sampletimehiding.html)。

#### 编程用法

| **模块参数：**`SampleTime`     |
| ------------------------------ |
| **类型：**字符串标量或字符向量 |
| **默认值：**`"-1"`             | -->

<!-- ### 信号属性 -->


<!-- 暂无
### `要求所有输入具有相同的数据类型` — 输入必须具有相同的数据类型 `off` （默认） | `on`



选中此复选框将要求所有输入具有相同的数据类型。

#### 编程用法

| **模块参数**：`InputSameDT` |
| --------------------------- |
| **类型：**字符向量          |
| **值：**`'off' | 'on'`      |
| **默认值：**`'off'`         |
 -->

<!-- 暂无
### `输出最小值` — 范围检查的最小输出值 `[]` （默认） | 标量



Simulink® 检查的输出范围的下限值。

Simulink 使用最小值执行下列操作：

- 某些模块的参数范围检查（请参阅[指定模块参数的最小值和最大值](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/checking-parameter-values.html)）。
- 仿真范围检查（请参阅[指定信号范围](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/signal-ranges.html)和[启用仿真范围检查](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/signal-ranges.html#brdikvq)）。
- 定点数据类型的自动定标。
- 从模型生成的代码的优化。此优化可删除算法代码，并影响某些仿真模式（如 SIL 或外部模式）的结果。有关详细信息，请参阅[Optimize using the specified minimum and maximum values](https://ww2.mathworks.cn/help/releases/R2022b/ecoder/ref/optimizeusingthespecifiedminimumandmaximumvalues.html) (Embedded Coder)。





**注意**

**输出最小值**不会饱和或剪切实际输出信号。请改用 [Saturation](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/saturation.html) 模块。



#### 编程用法

| **模块参数**：`OutMin` |
| ---------------------- |
| **类型**：字符向量     |
| **值**：`'[ ]'`\| 标量 |
| **默认值**：`'[ ]'`    | -->


<!-- 暂无
### `输出最大值` — 范围检查的最大输出值 `[]` （默认） | 标量



Simulink 检查的输出范围的上限值。

Simulink 使用最大值执行下列操作：

- 某些模块的参数范围检查（请参阅[指定模块参数的最小值和最大值](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/checking-parameter-values.html)）。
- 仿真范围检查（请参阅[指定信号范围](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/signal-ranges.html)和[启用仿真范围检查](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/signal-ranges.html#brdikvq)）。
- 定点数据类型的自动定标。
- 从模型生成的代码的优化。此优化可删除算法代码，并影响某些仿真模式（如 SIL 或外部模式）的结果。有关详细信息，请参阅[Optimize using the specified minimum and maximum values](https://ww2.mathworks.cn/help/releases/R2022b/ecoder/ref/optimizeusingthespecifiedminimumandmaximumvalues.html) (Embedded Coder)。





**注意**

**输出最大值**不会饱和或剪切实际输出信号。请改用 [Saturation](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/saturation.html) 模块。



#### 编程用法

| **模块参数**：`OutMax` |
| ---------------------- |
| **类型**：字符向量     |
| **值**：`'[ ]'`\| 标量 |
| **默认值**：`'[ ]'`    |
 -->

<div class="details-box">
<details open>
<summary>输出数据类型 — 指定输出数据类型<div>Inherit: internalRule（默认） | Inherit: backPropagation | Inherit: sameAsFirstInput | double | float | int8 | uint8 | int16 | uint16 | int32 | uint32 | fixdt(1,16,0) | fixdt(1,16,2^0,0) | fixdt(1,16,1.0,0,0.0)</div></summary>
</details>
<div class="details-content">

为输出选择数据类型。该类型可以继承、直接指定或表示为数据类型对象。

</div>
</div>


<!-- 

单机**显示数据类型助手**按钮 ![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/show_data_type_asst_button.png) 以显示**数据类型助手**，帮助您设置数据类型属性。有关详细信息，请参阅[使用数据类型助手指定数据类型](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/specify-data-types-using-data-type-assistant.html)。 -->

<!-- 
#### 依存关系

当输入是小于单精度的浮点数据类型时，“`Inherit: Inherit via internal rule`” 输出数据类型取决于 [Inherit floating-point output type smaller than single precision](https://ww2.mathworks.cn/help/releases/R2022b/simulink/gui/inherit-floating-point-output-type-smaller-than-single-precision.html) 配置参数的设置。当对数据类型进行编码所需的位数小于对单精度数据类型编码所需的 32 位时，数据类型小于单精度。例如，`half` 和 `int16` 小于单精度。 -->

<!-- 
#### 编程用法

| **模块参数**：`OutDataTypeStr`                               |
| ------------------------------------------------------------ |
| **类型**：字符向量                                           |
| **值**：`'Inherit: Inherit via internal rule'` | `'Inherit: Inherit via back propagation'` | `'Inherit: Same as first input'` | `'single'` | “`'half'`” | `'int8'` | `'uint8'` | `'int16'` | `'uint16'` | `'int32'` | `'uint32'` | `'int64'` | `'uint64'` | `'fixdt(1,16,0)'` | `'fixdt(1,16,2^0,0)'` | `'<data type expression>'` |
| **默认值**：`'Inherit: Inherit via internal rule'`           | -->

<!-- 暂无

### `锁定输出数据类型设置以防止被定点工具更改` — 防止定点工具覆盖输出数据类型 `off` （默认） | `on`



选择此参数可防止定点工具覆盖您在模块上指定的**输出**数据类型。有关详细信息，请参阅[Use Lock Output Data Type Setting](https://ww2.mathworks.cn/help/releases/R2022b/fixedpoint/ug/best-practices-for-using-the-fixed-point-tool-to-propose-data-types-for-your-simulink-model.html#br9an48) (Fixed-Point Designer)。

#### 编程用法

| **模块参数**：`LockScale` |
| ------------------------- |
| **类型：**字符向量        |
| **值：**`'off' | 'on'`    |
| **默认值：**`'off'`       |

 -->
<!-- 暂无
### `整数舍入模式` — 定点运算的舍入模式 “`向下`” （默认） | “`向上`” | “`收敛`” | “`最邻近值`” | “`舍入`” | “`最简`” | “`零`”



指定定点运算的舍入模式。有关详细信息，请参阅[舍入](https://ww2.mathworks.cn/help/releases/R2022b/fixedpoint/ug/rounding.html) (Fixed-Point Designer)。

模块参数始终舍入到最邻近的可表示值。要控制模块参数的舍入方法，请在封装字段中使用 MATLAB® 舍入函数输入表达式。

#### 编程用法

| **模块参数**：`RndMeth`                                      |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值：**`'Ceiling' | 'Convergent' | 'Floor' | 'Nearest' | 'Round' | 'Simplest' | 'Zero'` |
| **默认值：**`'Floor'`                                        |
 -->


<div class="details-box">
<details open>
<summary>对整数溢出进行饱和处理 — 溢出操作的方法<div>off （默认） | on</div></summary>
</details>
<div class="details-content">


指定对溢出是进行饱和处理还是绕回处理。

| 操作                     | 原理说明                                                     | 对溢出的影响                                       | 示例                                                         |
| :----------------------- | :----------------------------------------------------------- | :------------------------------------------------- | :----------------------------------------------------------- |
| 选中此复选框 (`on`)。    | 您的模型可能有溢出，并且您希望在生成的代码中具有显式饱和保护。 | 将溢出饱和处理为数据类型能够表示的最小值或最大值。 | `int8`（有符号 8 位整数）数据类型可以表示的最大值为 127。任何大于此最大值的模块运算结果都会导致 8 位整数溢出。如果选中此复选框，模块输出将在达到 127 时饱和。类似地，模块输出将在达到最小输出值 -128 时饱和。 |
| 不选中此复选框 (`off`)。 | 您需要优化所生成代码的效率。您希望避免过度地指定信号超出范围时的处理方式。有关详细信息。 | 溢出会绕回到由数据类型表示的适当值。               | `int8`（有符号 8 位整数）数据类型可以表示的最大值为 127。任何大于此最大值的模块运算结果都会导致 8 位整数溢出。清除该复选框时，软件会将导致溢出的值解释为 `int8`，这可能产生意外结果。例如，以 `int8` 表示的模块结果 130（二进制 1000 0010）为 -126。 |



如果选中此复选框，饱和将应用于模块中的每个内部操作，而不仅仅应用于输出或结果。通常，代码生成过程可以检测何时不会发生溢出。在这种情况下，代码生成器不会生成饱和代码。

</div>
</div>



<!-- 
#### 编程用法

| **模块参数**：`SaturateOnIntegerOverflow` |
| ----------------------------------------- |
| **类型：**字符向量                        |
| **值：**`'off' | 'on'`                    |
| **默认值：**`'off'`                       | -->


<!-- ## 模块特性 -->

<!--部分功能暂无 
| **数据类型**     | `Boolean` \| `double` \| `fixed point` \| `half` \| `integer` \| `single` |
| ---------------- | ------------------------------------------------------------ |
| **直接馈通**     | `是`                                                         |
| **多维信号**     | `是`                                                         |
| **可变大小信号** | `是`                                                         |
| **过零检测**     | `是`                                                         | -->

<!-- ## 扩展功能 -->

<!-- 

### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 Verilog 代码和 VHDL 代码。



HDL Coder™ 提供影响 HDL 实现和综合逻辑的额外配置选项。

**HDL 架构**

此模块具有多周期实现，这会在生成的代码中引入额外的延迟。要查看增加的延迟，请查看生成的模型或验证模型。请参阅[Generated Model and Validation Model](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/generated-model-and-validation-model.html) (HDL Coder)。



| 架构            | 额外的延迟周期                    | 描述                                                         |
| :-------------- | :-------------------------------- | :----------------------------------------------------------- |
| “`默认`” “`树`” | 0                                 | 生成树状结构的比较器。                                       |
| “`层叠`”        | 1，当模块具有单个向量输入端口时。 | 此实现针对延迟 * 面积进行优化，速度为中等。请参阅[Cascade Architecture Best Practices](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/blocks-with-multiple-implementations.html#btug1eg-1) (HDL Coder)。“`级联`”架构将在以后的版本中删除。 |

**HDL 模块属性**

| 通用                          |                                                              |
| :---------------------------- | ------------------------------------------------------------ |
| **ConstrainedOutputPipeline** | 通过移动设计中现有延迟的方式来放置在输出端的寄存器的数量。分布式流水线处理不会重新分发这些寄存器。默认值为 `0`。有关详细信息，请参阅[ConstrainedOutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#btp8gmp) (HDL Coder)。 |
| **InputPipeline**             | 要在生成的代码中插入的输入流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 `0`。有关详细信息，请参阅[InputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-25) (HDL Coder)。 |
| **OutputPipeline**            | 要在生成的代码中插入的输出流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 `0`。有关详细信息，请参阅[OutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-26) (HDL Coder)。 |
| **InstantiateStages**         | 为每个级联级生成 VHDL® `entity` 或 Verilog® `module`。默认值为 “`off`”。另请参阅[InstantiateStages](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bunj2k5-1) (HDL Coder)。 |
| **SerialPartition**           | 将级联-串行实现的分区指定为由每个分区长度组成的向量。默认设置使用最小级数。另请参阅[SerialPartition](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bunj60i-1) (HDL Coder)。 |



**注意**

要为 MinMax 模块启用 **LatencyStrategy** 设置，您必须将“`树`”指定为 **HDL 架构**。

| 本机浮点            |                                                              |
| :------------------ | ------------------------------------------------------------ |
| **LatencyStrategy** | 指定对于浮点运算符是否将设计中的模块映射到 `inherit`、`Max`、`Min` 或 `Zero`。默认值为 “`inherit`”。另请参阅[LatencyStrategy](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/hdl-block-properties-native-floating-point.html#mw_a99b0822-f2a6-4f5b-aca9-7f7251a67c7c) (HDL Coder)。 |



### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。 -->

## 版本历史记录

- 在 2024b 之前推出

### 限制信息
不支持部分
1. 参数-常设-启用过零检测 — 启用过零检测
2. 参数-常设-采样时间 — -1 以外的采样时间值
3. 参数-信号属性-要求所有输入具有相同的数据类型 — 输入必须具有相同的数据类型
4. 参数-信号属性-输出最小值 — 范围检查的最小输出值
5. 参数-信号属性-输出最大值 — 范围检查的最大输出值
6. 参数-信号属性-锁定输出数据类型设置以防止被定点工具更改 — 防止定点工具覆盖输出数据类型
7. 参数-信号属性-整数舍入模式 — 定点运算的舍入模式

<!-- ## 另请参阅 -->
<!-- 
[MinMax Running Resettable](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/minmaxrunningresettable.html) -->