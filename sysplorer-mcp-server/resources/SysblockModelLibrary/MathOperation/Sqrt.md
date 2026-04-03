# Sqrt
---
&nbsp;


计算平方根、带符号的平方根或平方根的倒数


- **库：** Sysblock / MathOperation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/Sqrt/Sqrt.png')" style="width: 100px; height: auto;">

## 描述

Sqrt 模块计算输入信号的平方根、有符号平方根或平方根的倒数。从**函数**下拉列表中选择以下函数之一。

| 函数         | 描述                                     | 数学表达式       | Syslab 等效函数                                             |
| :----------- | :--------------------------------------- | :--------------- | :----------------------------------------------------------- |
| `sqrt`       | 输入信号的平方根                         | `u^0.5`           | [`sqrt`](Sqrt.html) |
| `signedSqrt` | 输入信号绝对值的平方根乘以输入信号的符号 | `sign(u)*|u|^0.5` | —                                                            |
| `rSqrt`      | 输入信号的平方根的倒数                   | `u^-0.5`          | —                                                            |

模块图标将发生变化以匹配函数。

## 示例
计算 4 的平方根，将 Constant 模块的值设置为 4，Sqrt 模块函数选择 sqrt。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperation/Sqrt.mo">Sqrt.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/Sqrt/Sqrt01.png')" style="width: 600px; ">

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/Sqrt/Sqrt02.png')" style="width: 600px; ">


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u—输入信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">


模块的输入信号，用于计算平方根、有符号平方根或平方根的倒数。sqrt 函数接受实数或复数输入，但复数定点信号除外。signedSqrt 和 rSqrt 不接受复数输入。输入信号必须为浮点数。

下表总结了 sqrt、rSqrt 和 signedSqrt 函数的浮点、整数和定点数据类型对复数类型和负值的支持。


<table>
    <thead>
        <tr>
            <th>函数</th>
            <th>数据类型</th>
            <th>复数</th>
            <th>负值</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan="2"><code>sqrt</code></td>
            <td>浮点</td>
            <td>是</td>
            <td>是</td>
        </tr>
        <tr>
            <td>整数和定点</td>
            <td>否</td>
            <td>否</td>
        </tr>
        <tr>
            <td rowspan="2"><code>rSqrt</code></td>
            <td>浮点</td>
            <td>否</td>
            <td>否</td>
        </tr>
        <tr>
            <td>整数和定点</td>
            <td>否</td>
            <td>否</td>
        </tr>
        <tr>
            <td rowspan="2"><code>signedSqrt</code></td>
            <td>浮点</td>
            <td>否</td>
            <td>是</td>
        </tr>
        <tr>
            <td>整数和定点</td>
            <td>否</td>
            <td>否</td>
        </tr>
    </tbody>
</table>

如果输入为负数，请将除 signedSqrt 之外的所有函数的**输出信号**设置为复数。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | fixed point

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

输出信号，是输入信号的平方根、有符号平方根或平方根的倒数。当输入信号的类型为整数或定点时，输出必须为浮点。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | fixed point

</div>
</div>

## 参数


### 主要

<div class="details-box">
<details open>
<summary>函数 — 模块执行的函数<div>sqrt（默认） | signedSqrt | rSqrt</div></summary>
</details>
<div class="details-content">


指定模块计算的数学函数。模块图标将发生变化以匹配您选择的函数。

| 函数         | 模块图标                                                     |
| :----------- | :----------------------------------------------------------- |
| `sqrt`       | <img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/Sqrt/Sqrt.png')" width="100" height="100">|
| `signedSqrt` | <img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/Sqrt/Sqrt03.png')" width="100" height="100">|
| `rSqrt`      | <img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/Sqrt/Sqrt04.png')" width="100" height="100">|

#### 依存关系

当此参数设置为 `signedSqrt` 时，**中间结果数据类型**参数被禁用。

</div>
</div>


<!-- 
#### 编程用法

| **模块参数**：`Operator`                      |
| --------------------------------------------- |
| **类型**：字符向量                            |
| **值**：`'sqrt'` | `'signedSqrt'` | `'rSqrt'` |
| **默认值**：`'sqrt'`                          | -->


<!-- 暂无
### `输出信号类型` — 输出信号类型 “`自动`” （默认） | “`实数`” | “`复`”



指定模块的输出信号类型。

| 函数         | 输入信号类型 | 输出信号类型                            |                                         |           |
| :----------- | :----------- | :-------------------------------------- | --------------------------------------- | --------- |
| 自动         | 实数         | 复数                                    |                                         |           |
| `sqrt`       | `real`       | 对于非负输入为 `real`对于负输入为 `NaN` | 对于非负输入为 `real`对于负输入为 `NaN` | `complex` |
| `complex`    | `complex`    | `error`                                 | `complex`                               |           |
| `signedSqrt` | `real`       | `real`                                  | `real`                                  | `complex` |
| `complex`    | `error`      | `error`                                 | `error`                                 |           |
| `rSqrt`      | `real`       | `real`                                  | `real`                                  | `error`   |
| `complex`    | `error`      | `error`                                 | `error`                                 |           |

#### 编程用法

| **模块参数**：`OutputSignalType`          |
| ----------------------------------------- |
| **类型**：字符向量                        |
| **值**：`'auto'` | `'real'` | `'complex'` |
| **默认值**：`'auto'`                      | -->

<div class="details-box">
<details open>
<summary>采样时间 — -1 以外的采样时间值<div>-1 （默认） | 标量 | 向量</div></summary>
</details>
<div class="details-content">

将采样时间指定为 -1 以外的值。

#### 依存关系

此参数不可见，除非将其显式设置为 `-1` 以外的值。

</div>
</div>



<!-- #### 编程用法

| **模块参数：**`SampleTime`     |
| ------------------------------ |
| **类型：**字符串标量或字符向量 |
| **默认值：**`"-1"`             | -->

<!-- ### 算法 -->

<!-- 暂无

### `方法` — 计算平方根倒数的方法 “`完全`” （默认） | “`Newton-Raphson`”



指定用于计算平方根倒数的方法。此参数仅对 “`rSqrt`” 函数有效。

| 方法               | 支持的数据类型             | 何时使用此方法                                       |
| :----------------- | :------------------------- | :--------------------------------------------------- |
| “`完全`”           | 浮点                       | 您不需要逼近值时。**注意**输入或输出必须为浮点类型。 |
| “`Newton-Raphson`” | 浮点、定点和内置的整数类型 | 您需要快速的近似计算时。                             |

“`完全`”方法提供了与 MATLAB 计算一致的结果。



**注意**

不管模块对话框中显示了哪些选项，`sqrt` 和 `signedSqrt` 的算法始终是“`完全`”。

#### 编程用法

| **模块参数**：`AlgorithmType`          |
| -------------------------------------- |
| **类型**：字符向量                     |
| **值**：`'Exact'` | `'Newton-Raphson'` |
| **默认值**：`'Exact'`                  | -->


<!-- 暂无
### `迭代次数` — Newton Raphson 算法的迭代次数 `3` （默认） | 整数



指定执行 Newton-Raphson 算法的迭代次数。在使用 `rSqrt` 函数且**方法**的值为 “`Newton-Raphson`” 时，此参数有效。



**注意**

如果您输入 0，模块输出则是 Newton-Raphson 算法的初始估计值。

#### 编程用法

| **模块参数**：`Iterations` |
| -------------------------- |
| **类型**：字符向量         |
| **值**：整数               |
| **默认值**：`'3'`          | -->

### 数据类型

单击**显示数据类型助手**按钮以显示**数据类型助手**，帮助您设置数据类型属性。

<div class="details-box">
<details open>
<summary>中间结果数据类型—中间结果的数据类型<div>Inherit: internalRule （默认） | Inherit: backPropagation | Inherit: sameAsInput | double | float | int8 | uint8 | int16 | uint16 | int32 | uint32 | fixdt(1,16,,0)</div></summary>
</details>
<div class="details-content">

指定当您在**常设**窗格上将**函数**设置为 sqrt 或 rSqrt 时中间结果的数据类型。

该类型可以继承、直接指定或表示为数据类型对象。

::: warning 注意    
为了避免溢出，中间数据类型必须大于或等于可以包含输出数据类型平方的数据类型。
::: 

为平方根函数 `sqrt` 显式设置中间数据类型时，请遵循以下规范：

| 输入和输出数据类型                                           | 中间数据类型         |
| :----------------------------------------------------------- | :------------------- |
| 输入或输出为双精度。                                         | 使用双精度。         |
| 输入或输出是单精度，而且有任何非单精度数据类型*不*是双精度。 | 使用单精度或双精度。 |
| 输入和输出是定点。                                           | 使用定点。           |

为平方根倒数函数 `rSqrt` 显式设置中间数据类型时，请遵循以下规范：

| 输入和输出数据类型             | 中间数据类型 |
| :----------------------------- | :----------- |
| 输入是双精度，输出不是单精度。 | 使用双精度。 |
| 输入不是单精度，输出是双精度。 | 使用双精度。 |
| 输入和输出是定点。             | 使用定点。   |



#### 依存关系

当**函数**参数设置为 signedSqrt 时，此参数被禁用。

</div>
</div>



<!-- 
#### 编程用法

| **模块参数**：`IntermediateResultsDataTypeStr`               |
| ------------------------------------------------------------ |
| **类型**：字符向量                                           |
| **值**：`'Inherit: Inherit via internal rule'` | `'Inherit: Inherit from input'` | `'Inherit: Inherit from output'` | `'double'` | `'single'`、`'int8'`、`'uint8'`、`int16`、`'uint16'`、`'int32'`、`'uint32'`、`'int64'`、`'uint64'`、`fixdt(1,16,0)`、`fixdt(1,16,2^0,0)`。`'<data type expression>'` |
| **默认值**：`'Inherit: Inherit via internal rule'`           | -->



<!-- ### 输出 — 输出数据类型 “Inherit: internalRule” （默认） | “Inherit: backPropagation” | “Inherit: sameAsInput” | “double” | “float” | “int8” | “int32” | “uint32” | “fixdt(1, 16, 0)”  -->

<!-- #### 依存关系 -->

<!-- 
当输入是小于单精度的浮点数据类型时，“`Inherit: Inherit via internal rule`” 输出数据类型取决于 [Inherit floating-point output type smaller than single precision](https://ww2.mathworks.cn/help/releases/R2022b/simulink/gui/inherit-floating-point-output-type-smaller-than-single-precision.html) 配置参数的设置。当对数据类型进行编码所需的位数小于对单精度数据类型编码所需的 32 位时，数据类型小于单精度。 -->

<!-- 
#### 编程用法

| **模块参数**：`OutDataTypeStr`                               |
| ------------------------------------------------------------ |
| **类型**：字符向量                                           |
| **值**：`'Inherit: Inherit via internal rule'` | `'Inherit: Inherit via back propagation'` | `'Inherit: Same as first input'` | `'double'` | `'single'` | `'half'` | `'int8'` | `'uint8'` | `int16` | `'uint16'` | `'int32'` | `'uint32'` | `'int64'` | `'uint64'` | `fixdt(1,16,0)` | “`fixdt(1,16,2^0,0)`” | `fixdt(1,16,2^0,0)` | `'<data type expression>'` |
| **默认值**：`'Inherit: Same as first input'`                 | -->


<!-- 暂无
### `最小值` — 范围检查的最小输出值 `[]` （默认） | 标量



将 Simulink® 检查的输出范围的下限值指定为有限的双精度实数标量值。



**注意**

如果您指定总线对象作为此模块的数据类型，请不要为模块上的总线数据设置最小值。因为 Simulink 会忽略此设置。但请为指定作为数据类型的总线对象的总线元素设置最小值。有关总线元素的“最小值”参数的信息，请参阅 [`Simulink.BusElement`](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/simulink.buselement.html)。

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
| **值**：标量           |
| **默认值**：`'[ ]'`    | -->


<!-- 暂无
### `最大值` — 范围检查的最大输出值 `[]` （默认） | 标量



将 Simulink 检查的输出范围的上限值指定为有限的双精度实数标量值。



**注意**

如果您指定总线对象作为此模块的数据类型，请不要为模块的总线数据设置最大值。因为 Simulink 会忽略此设置。但请为指定作为数据类型的总线对象的总线元素设置最大值。有关总线元素的“最大值”参数的信息，请参阅 [`Simulink.BusElement`](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/simulink.buselement.html)。

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
| **值**：标量           |
| **默认值**：`'[ ]'`    | -->


<!-- 暂无
### `整数舍入模式` — 定点运算的舍入模式 “`向下`” （默认） | “`向上`” | “`收敛`” | “`最邻近值`” | “`舍入`” | “`最简`” | “`零`”



指定定点运算的舍入模式。有关详细信息，请参阅[舍入](https://ww2.mathworks.cn/help/releases/R2022b/fixedpoint/ug/rounding.html) (Fixed-Point Designer)。

#### 编程用法

| **模块参数**：`RndMeth`                                      |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值：**`'Ceiling' | 'Convergent' | 'Floor' | 'Nearest' | 'Round' | 'Simplest' | 'Zero'` |
| **默认值：**`'Floor'`                                        | -->


<!-- 暂无
### `锁定输出数据类型设置以防止被定点工具更改` — 防止定点工具覆盖数据类型 `off` （默认） | `on`



选中此选项将锁定此模块的输出数据类型设置，从而防止通过定点工具和定点顾问进行更改。有关详细信息，请参阅[Use Lock Output Data Type Setting](https://ww2.mathworks.cn/help/releases/R2022b/fixedpoint/ug/best-practices-for-using-the-fixed-point-tool-to-propose-data-types-for-your-simulink-model.html#br9an48) (Fixed-Point Designer)。

#### 编程用法

| **模块参数**：`LockScale` |
| ------------------------- |
| **类型**：字符向量        |
| **值**：`'off'` | `'on'`  |
| **默认值**：`'off'`       | -->

<div class="details-box">
<details open>
<summary>对整数溢出进行饱和处理 — 选择发生整数溢出时的行为<div>off（默认） | on</div></summary>
</details>
<div class="details-content">


| 操作             | 执行此操作的原因                                             | 溢出时会发生的情况                                 | 示例                                                         |
| :--------------- | :----------------------------------------------------------- | :------------------------------------------------- | :----------------------------------------------------------- |
| 选中此复选框。   | 您的模型可能有溢出，并且您希望在生成的代码中具有显式饱和保护。 | 将溢出饱和处理为数据类型能够表示的最小值或最大值。 | int8（有符号 8 位整数）数据类型可以表示的最大值为 127。任何大于此最大值的模块运算结果都会导致 8 位整数溢出。如果选中此复选框，模块输出将在达到 127 时饱和。类似地，模块输出将在达到最小输出值 -128 时饱和。 |
| 不选中此复选框。 | 您需要优化所生成代码的效率。您希望避免过度地指定信号超出范围时的处理方式。 | 溢出会绕回到由数据类型表示的适当值。               | int8（有符号 8 位整数）数据类型可以表示的最大值为 127。任何大于此最大值的模块运算结果都会导致 8 位整数溢出。清除该复选框时，软件会将导致溢出的值解释为 int8，这可能产生意外结果。例如，以 int8 表示的模块结果 130（二进制 1000 0010）为 -126。 |



如果选中此复选框，饱和将应用于模块中的每个内部操作，而不仅仅应用于输出或结果。通常，代码生成过程可以检测何时不会发生溢出。在这种情况下，代码生成器不会生成饱和代码。

</div>
</div>



<!-- 
#### 编程用法

| **模块参数**：`DoSatur`  |
| ------------------------ |
| **类型**：字符向量       |
| **值**：`'off'` | `'on'` |
|                          |
| **默认值**：`'off'`      | -->



<!-- ## 模块特性 -->

<!-- 暂无部分特性
| **数据类型**     | `double` | `fixed point` | `half` | `integer` | `single` |
| ---------------- | -------------------------------------------------------- |
| **直接馈通**     | `是`                                                     |
| **多维信号**     | `是`                                                     |
| **可变大小信号** | `是`                                                     |
| **过零检测**     | `否`                                                     | -->

<!-- ## 扩展功能 -->


<!-- 
### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 Verilog 代码和 VHDL 代码。



HDL Coder™ 提供影响 HDL 实现和综合逻辑的额外配置选项。

**Sqrt 函数模式**

对于**函数**设置为 “`sqrt`” 的 Sqrt 模块，代码生成器支持各种架构和数据类型。

“`sqrtfunction`” 架构支持定点类型和浮点类型的代码生成。使用浮点类型时，请将[Floating Point IP Library](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/library.html) (HDL Coder)设置为“`本机浮点`”。您可以指定 HDL 属性 **LatencyStrategy** 和 **CustomLatency**，以便在硬件平台上设计时从一系列频率值中进行选择。

将 HDL 模块属性 **UseMultiplier** 与 **LatencyStrategy** 和 **CustomLatency** 属性结合使用，以指定是使用流水线移位相加算法还是使用乘法算法来计算平方根

**不同模式的本机浮点设置**

对于此架构，您可以在“HDL 模块属性”对话框的**本机浮点**选项卡中指定 **HandleDenormals** 和 **LatencyStrategy** 设置。

| 架构                          | 定点 | 本机浮点 | HandleDenormals | LatencyStrategy |
| :---------------------------- | :--- | :------- | :-------------- | :-------------- |
| “`sqrtfunction`”              | ✓    | ✓        | ✓               | ✓               |
| “`sqrtnewton`”                | ✓    | —        | —               | —               |
| “`sqrtnewtonsinglerate`”      | ✓    | —        | —               | —               |
| “`recipsqrtnewton`”           | ✓    | —        | —               | —               |
| “`recipsqrtnewtonsinglerate`” | ✓    | —        | —               | —               |

**HDL 架构**

此模块具有多周期实现，这会在生成的代码中引入额外的延迟。要查看增加的延迟，请查看生成的模型或验证模型。请参阅[Generated Model and Validation Model](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/generated-model-and-validation-model.html) (HDL Coder)。

| 架构                          | 参数                                            | 额外的延迟周期                                     | 描述                                                         |
| :---------------------------- | :---------------------------------------------- | :------------------------------------------------- | :----------------------------------------------------------- |
| “`SqrtFunction`”（默认值）    | `UseMultiplier``LatencyStrategy``CustomLatency` | 取决于参数选择项、输出字长以及输入和输出小数长度。 | 要指定此架构，请将**函数**设置为 “`sqrt`” 或 “`rSqrt`”。使用流水线移位相加算法或基于乘法的算法计算平方根。“`SqrtFunction`” 架构的最大延迟由输出字长以及定点数据的输入和输出小数长度确定。例如，如输出字长 `17`，最大延迟为 `11`。要查看延迟计算，请在 MATLAB 命令提示符下输入：`HDLMathLib`通过将 **UseMultiplier** 设置为 `off` 并将 **LatencyStrategy** 设置为 `inherit`，改进设计频率并减少资源使用。 |
| “`SqrtNewton`”                | `Iterations`                                    | `Iterations` + 3                                   | 要指定此架构，请将**函数**设置为 “`sqrt`”。使用牛顿迭代法。选择此选项以优化面积。`Iterations` 的默认值为 3。`Iterations` 的推荐值为 2 到 10。如果 `Iterations` 超出推荐范围，HDL Coder 会生成一条消息。 |
| “`SqrtNewtonSingleRate`”      | `Iterations`                                    | (`Iterations` * 4) + 6                             | 要指定此架构，请将**函数**设置为 “`sqrt`”。使用单频率流水线牛顿法。要优化速度或需要单速率实现，请选择此选项。`Iterations` 的默认值为 3。`Iterations` 的推荐值为 2 到 10。如果 `Iterations` 超出推荐范围，代码生成器会生成一条消息。 |
| “`RecipSqrtNewton`”           | `Iterations`                                    | `Iterations` + 2                                   | 要指定此架构，请将**函数**设置为 “`rSqrt`”。使用牛顿迭代法。选择此选项以优化面积。 |
| “`RecipSqrtNewtonSingleRate`” | `Iterations`                                    | (`Iterations` * 4) + 5                             | 要指定此架构，请将**函数**设置为 “`rSqrt`”。使用单频率流水线牛顿法。要优化速度或需要单速率实现，请选择此选项。 |

Newton-Raphson 迭代方法：

*x**i*+1=*x**i*−*f*(*x**i*)*f*′(*x**i*)=*x**i*(1.5−0.5*a**x**i*2)

“`ReciprocalRsqrtBasedNewton`” 和 “`ReciprocalRsqrtBasedNewtonSingleRate`” 一起实现 Newton-Raphson 方法，方式如下：

*f*(*x*)=1*x*2−1

**HDL 模块属性**

| 通用                          |                                                              |
| :---------------------------- | ------------------------------------------------------------ |
| **ConstrainedOutputPipeline** | 通过移动设计中现有延迟的方式来放置在输出端的寄存器的数量。分布式流水线处理不会重新分发这些寄存器。默认值为 `0`。有关详细信息，请参阅[ConstrainedOutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#btp8gmp) (HDL Coder)。 |
| **迭代数**                    | “`SqrtNewton`” 或 “`SqrtNewtonSingleRate`” 实现的迭代次数。  |
| **InputPipeline**             | 要在生成的代码中插入的输入流水线级数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 `0`。有关详细信息，请参阅[InputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-25) (HDL Coder)。 |
| **OutputPipeline**            | 要在生成的代码中插入的输出流水线级数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 `0`。有关详细信息，请参阅[OutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-26) (HDL Coder)。 |
| **UseMultiplier**             | 为 “`SqrtFunction`” 实现选择算法。默认情况下，此属性设置为 `off`，并且此模块使用移位相加算法计算平方根。当该属性设置为 `on` 时，通过使用乘数计算平方根。通过将 **UseMultiplier** 设置为 `off` 并将 **LatencyStrategy** 设置为 `inherit`，提高设计频率并减少资源使用。 |
| **LatencyStrategy**           | 对于定点和浮点类型，指定是将设计中的模块映射到 `MAX`、`MIN`、`CUSTOM` 还是 `ZERO` 延迟。默认值为 “`MAX`”。浮点类型的模块设置会覆盖模型级设置。对于定点类型，模块级设置确定延迟策略。另请参阅[LatencyStrategy](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/hdl-block-properties-native-floating-point.html#mw_a99b0822-f2a6-4f5b-aca9-7f7251a67c7c) (HDL Coder)。通过将 **UseMultiplier** 设置为 `off` 并将 **LatencyStrategy** 设置为 `inherit`，提高设计频率并减少资源使用。 |
| **CustomLatency**             | 当 **LatencyStrategy** 设置为 `CUSTOM` 时，如果您使用定点类型，请使用此属性为定点类型指定介于 `ZERO` 和 `MAX` 之间的自定义延迟值。对于浮点类型，此值成为运算符的自定义延迟。另请参阅[NFPCustomLatency](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/hdl-block-properties-native-floating-point.html#mw_e29db696-7117-431a-a8b8-4471b8d24ea8) (HDL Coder)。 |

| 本机浮点            |                                                              |
| :------------------ | ------------------------------------------------------------ |
| **HandleDenormals** | 指定是否希望 HDL Coder 在设计中插入额外的逻辑来处理非正规数字。非规范数是量级非常小、必须使用包含前导零的尾数才能表示的浮点数。默认值为 “`inherit`”。另请参阅[HandleDenormals](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/hdl-block-properties-native-floating-point.html#mw_34395404-aeac-43da-bb3c-96c4a420c9e1) (HDL Coder)。 |

**限制**

- 输入必须为无符号标量值。
- 输出为定点标量值。
 -->

<!-- 
### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。 -->

## 版本历史记录

- 在 2024b 之前推出

<!-- 
**在 R2010a 中推出** -->

## 另请参阅

[MathFunction](MathFunction.html) | [TrigonometricFunction](TrigonometricFunction.html)