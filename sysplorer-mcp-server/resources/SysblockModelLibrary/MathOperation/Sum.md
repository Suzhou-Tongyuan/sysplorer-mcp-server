# Sum
---
&nbsp;

输入信号的加减运算

- **库：** Sysblock / MathOperation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/Sum/Sum.png')" style="width: 100px; height: auto;">


## 描述

<!-- Sum 模块对输入信号执行加减运算。Add、Subtract、Sum of Elements 和 Sum 模块是相同的模块。此模块可对标量、向量或矩阵输入执行加减运算。它还可以缩减信号的元素并执行求和。 -->

您可以使用**符号列表**参数以及加号 (`+`)、减号 (`-`) 和分隔符 (`|`) 指定模块的运算。

- `+` 和 `-` 字符的个数等于输入的个数。例如，`+-+` 需要三个输入。模块从第一个（顶部）输入信号中减去第二个（中间）输入信号，然后加上第三个（底部）输入信号。
- 分隔符在模块图标上的端口之间产生额外空间。
- 如果仅执行加法，则可以使用一个与输入个数相等的数值。
- 如果只有一个输入端口，则单个 `+` 或 `-` 会在所有维度上或在指定的维度中加上或减去元素。

Sum 模块首先将输入数据类型转换为其累加器数据类型，然后执行指定的运算。最后，模块使用指定的舍入和溢出模式，将计算结果转换为输出数据类型。

<!-- ### 模块输出的计算

Sum 模块的输出计算取决于模块输入的个数和输入端口的符号：

| 如果 Sum 模块有...                       | 而且...                                                      | 输出计算公式为...                       | 其中...                        |
| :--------------------------------------- | :----------------------------------------------------------- | :-------------------------------------- | :----------------------------- |
| 一个输入端口                             | 输入端口符号为 + 号                                          | y = e[0] + e[1] + e[2] ... + e[m]       | `e[i]` 是输入 u 的第 i 个元素  |
| 输入端口符号为 – 号                      | y = 0.0 – e[0] – e[1] – e[2] ... – e[m]                      |                                         |                                |
| 两个或更多输入端口                       | 所有输入端口符号均为 – 号                                    | y = 0.0 – u[0] – u[1] – u[2] ... – u[n] | `u[i]` 是第 i 个输入端口的输入 |
| 第 k 个输入端口是第一个符号为 + 号的端口 | y = u[k] – u[0] – u[1] – u[2] – u[k–1] (+/–) u[k+1] ... (+/–) u[n] |                                         |                                | -->

## 示例

对两个常量值进行相加， 将两个 Constant 模块设置为 1，Sum 模块符号列表选择 ++。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperation/Sum.mo">Sum.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/Sum/Sum01.png')" style="width: 600px; ">

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/Sum/Sum02.png')" style="width: 600px; ">


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 第一个输入操作数信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

用于加法或减法运算的输入信号。如果只有一个输入信号，则对所有维度或指定维度中的元素执行加法或减法。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | Boolean | fixed point

</div>
</div>

<!-- 输入可以具有不同的数据类型，除非您选中了**要求所有输入具有相同的数据类型**参数。 -->

<div class="details-box">
<details open>
<summary>u_n — 第 n 个输入操作数信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

运算的第 n 个输入信号，输入的个数与符号列表参数中的符号个数相匹配。模块按照列出的顺序将运算应用于输入。您还可以使用一个与输入端口个数相等的数值作为符号列表参数。模块创建输入端口并将加法应用于所有输入。例如，如果为符号列表参数赋值 5，则模块创建 5 个输入端口并将它们相加以产生输出。

所有的非标量输入信号必须具有相同的维度。标量输入将扩展为与其他输入具有相同的维度。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | Boolean | fixed point

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

加法和 / 或减法运算产生的输出信号，输出信号具有与输入信号相同的维度。

**数据类型：**  float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | Boolean | fixed point

</div>
</div>


## 参数


### 主要


<!-- 暂无
### `图标形状` — 模块图标形状 **矩形** （默认） | **舍入**



将模块的图标形状指定为矩形或圆形。

对于矩形模块，第一个输入端口是顶部端口。对于一个圆形 Sum 模块，第一个输入端口最靠近 12 点钟位置，按逆时针方向围绕模块。类似地，其他输入端口也按逆时针方向围绕模块。

#### 编程用法

| **模块参数**：`IconShape`           |
| ----------------------------------- |
| **类型**：字符向量                  |
| **值**：`'rectangular'` | `'round'` |
|                                     |
| **默认值**：`'round'`               |
 -->

<div class="details-box">
<details open>
<summary>符号列表 — 对输入执行的运算<div>++ （默认） | + | - | | | integer</div></summary>
</details>
<div class="details-content">

输入对输入信号执行的加法和减法运算。为每个运算创建一个输入端口。分隔符 (`|`) 在模块图标上的输入端口之间产生额外空间。加法是默认运算。如果您只想将输入信号相加，请键入输入端口的个数。各项运算按所列顺序执行。

只输入一个元素时，模块将启用**求和维度**参数。对于单个向量输入，`+` 或 `-` 会在所有维度上或在指定的维度中加上或减去元素。

::: tip 提示
您可以通过在**符号列表**参数中的符号之间插入分隔符 (`|`) 来控制输入端口在模块上的位置。
:::

</div>
</div>

<!-- 
#### 编程用法

| **模块参数**：`Inputs`               |
| ------------------------------------ |
| **类型**：字符向量                   |
| **值**：`'+'` | `'-'` | `\|` \| 整数 |
|                                      |
| **默认值**：`'++'`                   | -->


<div class="details-box">
<details open>
<summary>求和维度 — 对单个向量输入执行的运算的维度<div>所有维度（默认） | 指定的维度</div></summary>
</details>
<div class="details-content">

选择模块执行求和运算所用的维度。

选择**指定的维度**，则会出现另一个参数**维度**。选择对向量输入求和所用的特定维度。

#### 依存关系

当**符号列表**参数中仅列出一个符号时启用。

</div>
</div>


<!-- 
#### 编程用法

| **模块参数**：`CollapseMode`                         |
| ---------------------------------------------------- |
| **类型**：字符向量                                   |
| **值**：`'All dimensions'` | `'Specified dimension'` |
|                                                      |
| **默认值**：`'All dimensions'`                       | -->


<div class="details-box">
<details open>
<summary>维度 — 对向量输入求和所用的维数<div>1 （默认） | integer</div></summary>
</details>
<div class="details-content">

当为**求和维度**参数选择**指定的维度**时，请指定执行运算所用的维度。

假设您有一个 2×3 矩阵 U。
  
如果指定的维度大于输入的维度，则会显示错误消息。

#### 依存关系

为**求和维度**参数选择**指定的维度**时启用。

</div>
</div>


<!-- 
#### 编程用法

| **模块参数**：`CollapseDim` |
| --------------------------- |
| **类型**：字符向量          |
| **值**：`integer`           |
|                             |
| **默认值**：`'1'`           | -->


### 信号属性

<div class="details-box">
<details open>
<summary>要求所有输入具有相同的数据类型<div>off（默认） | on</div></summary>
</details>
<div class="details-content">

指定输入信号是否必须全部具有相同的数据类型。如果启用此参数，则在输入信号类型不同时，仿真过程中会发生错误。

</div>
</div>

<!-- 
#### 编程用法

| **模块参数**：`InputSameDT` |
| --------------------------- |
| **类型：**字符向量          |
| **值：**`'off' | 'on'`      |
| **默认值：**`'off'`         |  -->


<!-- 暂无
### `累加器数据类型` — 累加器的数据类型 “`Inherit: Inherit via internal rule`” （默认） | “`Inherit: Same as first input`” | “`double`” | “`single`” | “`half`” | “`int8`” | “`uint8`” | “`int16`” | “`uint16`” | “`int32`” | “`uint32`” | “`int64`” | “`uint64`” | “`fixdt(1,16)`” | “`fixdt(1,16,0)`” | “`fixdt(1,16,2^0,0)`” | “`<data type expression>`”



选择累加器的数据类型。该类型可以继承、直接指定或表示为数据类型对象，如 `Simulink.NumericType`。如果您选择 “`Inherit: Inherit via internal rule`”，Simulink 在考虑嵌入式目标硬件的属性的同时，会选择相应的数据类型来平衡数值准确性、性能和生成的代码大小。

#### 编程用法

| **模块参数**：` AccumDataTypeStr`                            |
| ------------------------------------------------------------ |
| **类型**：字符向量                                           |
| **值**：`'Inherit: Inherit via internal rule` | `'Inherit: Same as first input'` | `'double'``'single'` | `'half'` | `'int8'` | `'uint8'` | `'int16'` | `'uint16'`、`'int32'` | `'uint32'` | `'int64'` | `'uint64'` | `'fixdt(1,16)'` | `'fixdt(1,16,0)'` | `'fixdt(1,16,2^0,0)'` | `'<data type expression>'` |
| **默认值**：`'Inherit: Inherit via internal rule'`           | -->


<!-- 暂无
### `输出最小值` — 范围检查的最小输出值 `[]` （默认） | 标量



Simulink 检查的输出范围的下限值。

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
| **默认值**：`'[ ]'`    |
 -->

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
| **默认值**：`'[ ]'`    | -->

<!-- ### 输出数据类型 — 指定输出数据类型 “Inherit: internalRule” （默认） | “Inherit: keepMSB” | “Inherit: keepLSB” | “Inherit: backPropagation” | “Inherit: sameAsFirstInput” | “double” | “float” | “int8” | “uint8” | “int16” | “uint16” | “`int32`” | “uint32” | “fixdt(1,16,0)” | “fixdt(1,16,2^0,0)” | “fixdt(1,16,1.0,0,0.0)”  -->


<!-- 
当您选择继承的选项时，模块的行为如下所示：

- “`Inherit: Inherit via internal rule`” - Simulink 在考虑嵌入式目标硬件的属性的同时，会选择相应的数据类型来平衡数值准确性、性能和生成的代码大小。

  

  **注意**

  累加器内部规则的优点是数值更准确，而代价可能是生成的代码效率低下。要获取相同的输出精度，请将输出数据类型设置为 “`Inherit: Inherit same as accumulator`”。 -->


<!--   

  **注意**

  当输入是小于单精度的浮点数据类型时，“`Inherit: Inherit via internal rule`” 输出数据类型取决于 [Inherit floating-point output type smaller than single precision](https://ww2.mathworks.cn/help/releases/R2022b/simulink/gui/inherit-floating-point-output-type-smaller-than-single-precision.html) 配置参数的设置。当对数据类型进行编码所需的位数小于对单精度数据类型编码所需的 32 位时，数据类型小于单精度。例如，`half` 和 `int16` 小于单精度。

- “`Inherit: Keep MSB`” - Simulink 选择一种能够保持运算的完整范围的数据类型，然后将输出精度降低到适合嵌入式目标硬件的大小。

  

  **提示**

  要获得更高效的生成代码，请将**累加器数据类型**设置为 “`Inherit: Inherit via internal rule`”，并取消选择**对整数溢出进行饱和处理**参数。

  此规则从不产生溢出。

- “`Inherit: Keep LSB`” - Simulink 选择一种保持运算精度的数据类型，但如果完整类型不适合嵌入式目标硬件，则会缩小范围。

  

  **提示**

  要获得更高效的生成代码，请将**累加器数据类型**设置为 “`Inherit: Inherit via internal rule`”，并取消选择**对整数溢出进行饱和处理**参数。

  此规则可能产生溢出。

  如果更改了嵌入式目标的设置，则依这些内部规则选择的数据类型可能会发生变化。有时软件不能同时满足优化代码效率和保证数值准确性这两个需求。如果这些规则不能满足您对数值准确性或性能的特定需求，请使用下列选项之一：

  - 显式指定输出数据类型。
  - 使用简单的选项 “`Inherit: Same as first input`”。
  - 显式指定默认数据类型（例如 `fixdt(1,32,16)`），然后使用定点工具为您的模型提供数据类型建议。有关详细信息，请参阅 [`fxptdlg`](https://ww2.mathworks.cn/help/releases/R2022b/fixedpoint/ref/fxptdlg.html) (Fixed-Point Designer)。
  - 要指定您自己的继承规则，请使用 “`Inherit: Inherit via back propagation`”，然后使用 [Data Type Propagation](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/datatypepropagation.html) 模块。有关如何使用此模块的示例说明，请参阅 Signal Attributes 模块库中的 Data Type Propagation Examples 模块。

  

- “`Inherit: Inherit via back propagation`” - 使用驱动模块的数据类型。

- “`Inherit: Same as first input`” - 使用第一个输入信号的数据类型。

- “`Inherit: Inherit same as accumulator`” - 使用累加器的数据类型。 -->


<!-- 

#### 编程用法

| **模块参数**：`OutDataTypeStr`                               |
| ------------------------------------------------------------ |
| **类型**：字符向量                                           |
| **值**：`'Inherit: Inherit via internal rule`|`'Inherit: Keep MSB'`|`'Inherit: Keep LSB'` | `'Inherit: Inherit via back propagation'``'Inherit: Same as first input'` | `'Inherit: Same as accumulator'` | `'double'` | `'single'` | `'half'` | `'int8'` | `'uint8'` | `'int16'` | `'uint16'`, `'int32'` | `'uint32'` | `'int64'`| `'uint64'`|`'fixdt(1,16)'` | `'fixdt(1,16,0)'` | `'fixdt(1,16,2^0,0)'` | `'<data type expression>'` |
| **默认值**：`'Inherit: Inherit via internal rule'`           | -->


<!-- 暂无
### `锁定数据类型设置以防止被定点工具更改` — 防止定点工具覆盖数据类型 `off` （默认） | `on`



选择此选项可锁定数据类型设置，防止使用定点工具和定点顾问进行更改。有关详细信息，请参阅[Lock the Output Data Type Setting](https://ww2.mathworks.cn/help/releases/R2022b/fixedpoint/ug/configuring-blocks-with-fixed-point-output.html#f25236) (Fixed-Point Designer)。

#### 编程用法

| **模块参数：**`LockScale` |
| ------------------------- |
| **值：**`'off' | 'on'`    |
| **默认值：**`'off'`       |

 -->
<!-- 暂无
### `整数舍入模式` — 定点运算的舍入模式 “`向下`” （默认） | “`向上`” | “`收敛`” | “`最邻近值`” | “`舍入`” | “`最简`” | “`零`”



指定定点运算的舍入模式。有关详细信息，请参阅[舍入](https://ww2.mathworks.cn/help/releases/R2022b/fixedpoint/ug/rounding.html) (Fixed-Point Designer)。

模块参数始终舍入到最邻近的可表示值。要控制模块参数的舍入方法，请在封装字段中使用 MATLAB 舍入函数输入表达式。

#### 编程用法

| **模块参数**：`RndMeth`                                      |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值：**`'Ceiling' | 'Convergent' | 'Floor' | 'Nearest' | 'Round' | 'Simplest' | 'Zero'` |
| **默认值：**`'Floor'`                                        |
 -->


<div class="details-box">
<details open>
<summary>对整数溢出进行饱和处理 — 溢出操作的方法<div>off（默认） | on</div></summary>
</details>
<div class="details-content">

指定对溢出是进行饱和处理还是绕回处理。

| 操作                     | 原理说明                                                     | 对溢出的影响                                       | 示例                                                         |
| :----------------------- | :----------------------------------------------------------- | :------------------------------------------------- | :----------------------------------------------------------- |
| 选中此复选框 (on)。    | 您的模型可能有溢出，并且您希望在生成的代码中具有显式饱和保护。 | 将溢出饱和处理为数据类型能够表示的最小值或最大值。 | int8（有符号 8 位整数）数据类型可以表示的最大值为 127。任何大于此最大值的模块运算结果都会导致 8 位整数溢出。如果选中此复选框，模块输出将在达到 127 时饱和。类似地，模块输出将在达到最小输出值 -128 时饱和。 |
| 不选中此复选框 (off)。 | 您需要优化所生成代码的效率。您希望避免过度地指定信号超出范围时的处理方式。| 溢出会绕回到由数据类型表示的适当值。               | int8（有符号 8 位整数）数据类型可以表示的最大值为 127。任何大于此最大值的模块运算结果都会导致 8 位整数溢出。清除该复选框时，软件会将导致溢出的值解释为 int8，这可能产生意外结果。例如，以 int8 表示的模块结果 130（二进制 1000 0010）为 -126。 |

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

<!-- 部分暂无
| **数据类型**     | `Boolean` | `double` | `fixed point` | `half` | `integer` | `single` |
| ---------------- | ------------------------------------------------------------ |
| **直接馈通**     | `是`                                                         |
| **多维信号**     | `是`                                                         |
| **可变大小信号** | `是`                                                         |
| **过零检测**     | `否`                                                         | -->

<!-- 
### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 Verilog 代码和 VHDL 代码。



HDL Coder™ 提供影响 HDL 实现和综合逻辑的额外配置选项。

**Sum、Add 和 Subtract 模块的 HDL 架构**

默认的“`线性`”架构为 N 个输入生成包含 N 个运算（加法器）的运算链。

**Sum of Elements 模块的 HDL 架构**

对于 Sum of Elements 模块，HDL Coder 支持对单个向量输入具有多个元素的 Sum of Elements 模块使用“`树`”和“`层叠`”架构。

此模块具有多周期实现，这会在生成的代码中引入额外的延迟。要查看增加的延迟，请查看生成的模型或验证模型。请参阅[Generated Model and Validation Model](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/generated-model-and-validation-model.html) (HDL Coder)。

| 架构     | 额外的延迟周期                    | 描述                                                         |
| :------- | :-------------------------------- | :----------------------------------------------------------- |
| “`线性`” | 0                                 | 生成线性加法器链来计算乘积之和。对于具有不同位宽的多个输入，“`Linear`” 架构会对加法器进行多级实现并用流水线串联各级，以优化资源利用率。每级的输出是根据该级的输入宽度来计算的。 |
| “`树`”   | 0                                 | 生成加法器树形结构来计算乘积之和。                           |
| “`层叠`” | 1，当模块具有单个向量输入端口时。 | 此实现优化延迟 * 面积，并且比“`树`”实现更快。它计算部分乘积并级联乘法器。“`级联`”架构将在以后的版本中删除。请参阅[Cascade Architecture Best Practices](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/blocks-with-multiple-implementations.html#btug1eg-1) (HDL Coder)。 |

**HDL 模块属性**



**注意**

要使用“HDL 模块属性”对话框的**本机浮点**选项卡中的 **LatencyStrategy** 设置，请指定“`线性`”或“`树`”作为 HDL 架构。

| 通用                          |                                                              |
| :---------------------------- | ------------------------------------------------------------ |
| **ConstrainedOutputPipeline** | 通过移动设计中现有延迟的方式来放置在输出端的寄存器的数量。分布式流水线处理不会重新分发这些寄存器。默认值为 `0`。有关详细信息，请参阅[ConstrainedOutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#btp8gmp) (HDL Coder)。 |
| **InputPipeline**             | 要在生成的代码中插入的输入流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 `0`。有关详细信息，请参阅[InputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-25) (HDL Coder)。 |
| **OutputPipeline**            | 要在生成的代码中插入的输出流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 `0`。有关详细信息，请参阅[OutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-26) (HDL Coder)。 |



**注意**

Sum of Elements 模块不支持本机浮点模式下双精度数据类型的 HDL 代码生成。

| 本机浮点             |                                                              |
| :------------------- | ------------------------------------------------------------ |
| **LatencyStrategy**  | 指定对于浮点运算符是否将设计中的模块映射到 `inherit`、`Max`、`Min`、`Zero` 或 `Custom`。默认值为 “`inherit`”。另请参阅[LatencyStrategy](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/hdl-block-properties-native-floating-point.html#mw_a99b0822-f2a6-4f5b-aca9-7f7251a67c7c) (HDL Coder)。 |
| **NFPCustomLatency** | 要指定值，请将 **LatencyStrategy** 设置为 `Custom`。HDL Coder 会增加延迟，其值等于您为 **NFPCustomLatency** 设置指定的值。另请参阅[NFPCustomLatency](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/hdl-block-properties-native-floating-point.html#mw_e29db696-7117-431a-a8b8-4471b8d24ea8) (HDL Coder)。 |

**复数数据支持**

默认的“`线性`”实现支持复数数据。

“`树`”实现支持**符号列表**模块参数为 `+` 的复数数据。借助本机浮点支持，“`树`”实现支持**符号列表**为 `+` 和 `-` 的复数数据。

**限制和注意事项**

要为混合使用标量和向量输入的多输入 Sum 模块生成 HDL 代码，您必须在 Sum 模块的前两个输入之一上指定向量输入。



### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。 -->

## 版本历史记录

- 在 2024b 之前推出

<!-- 
**在 R2006a 之前推出** -->

### 限制信息
不支持部分
1. 参数-常设-图标形状 — 模块图标形状
2. 参数-常设-求和维度 — 对单个向量输入执行的运算的维度
3. 参数-常设-维度 — 对向量输入求和所用的维数
4. 参数-常设-采样时间 — -1 以外的采样时间值
5. 参数-信号属性-要求所有输入具有相同的数据类型 — 要求所有输入具有相同的数据类型
6. 输出最小值 — 范围检查的最小输出值
7. 输出最大值 — 范围检查的最大输出值
8. 锁定数据类型设置以防止被定点工具更改 — 防止定点工具覆盖数据类型

## 另请参阅

[Gain](Gain.html) | [Bias](Bias.html)

<!-- ### 主题 -->
