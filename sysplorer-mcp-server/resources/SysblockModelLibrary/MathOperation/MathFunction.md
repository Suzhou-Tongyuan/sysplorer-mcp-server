# MathFunction
---
&nbsp;

执行数学函数


- **库：** Sysblock / MathOperation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/MathFunction/MathFunction.png')" style="width: 100px; height: auto;">

## 描述

MathFunction 模块执行许多常见的数学函数。

可以从 MathFunction 模块中的**函数**参数列表中选择以下函数之一。

| 函数                                    | 描述                   | 数学表达式                                                   | Syslab 等效函数                                             |
| :-------------------------------------- | :--------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| `exp`                                   | 指数                   | `eu`                                                         | [`exp`] |
| `log`                                   | 自然对数               | `ln u`                                                       | [`log`]|
| `10^u`                                  | 以 10 为底的幂         | `10u`                                                        | `10.^u` [`power`] |
| `log10`                                 | 常用（以 10 为底）对数 | `log u`                                                      | [`log10`] |
| `square`                                | 2 次幂                 | `u2`                                                         | `u.^2` [`power`] |
| `pow`                                   | 幂                     | `sign(u)*|u|v`（默认值，仅适用于偶数阶根）或 `uv`            | [`power`]
| 使用精确法的 `reciprocal`               | 倒数                   | `1/u`                                                        | `1./u` [`rdivide`] |
| 使用 Newton-Raphson 方法的 `reciprocal` | 倒数                   | Newton-Raphson 倒数算法方法 | 无                                                           |
| `rem`                                   | 除后的余数             | —                                                            | [`rem`] |
| `mod`                                   | 除后的模数             | —                                                            | [`mod`] |
| `transpose`                             | 转置                   | `uT`                                                         | `u.'`  |


<!--暂无
 | `hermitian`                             | 复共轭转置             | `uH`                                                         | `u'` （请参见[数组与矩阵运算](https://ww2.mathworks.cn/help/releases/R2022b/matlab/matlab_prog/array-vs-matrix-operations.html)） | 
`hypot`                                 | 平方和的平方根         | `(u2+v2)0.5`                                                 | [`hypot`](https://ww2.mathworks.cn/help/releases/R2022b/matlab/ref/hypot.html) | |
| `conj`                                  | 复共轭                 | `ū`                                                          | [`conj`](https://ww2.mathworks.cn/help/releases/R2022b/matlab/ref/conj.html) || `magnitude^2`                           | 复数模量               | `|u|2`                                                       | `real(u).^2 + imag(u).^2` （请参见 [`real`](https://ww2.mathworks.cn/help/releases/R2022b/matlab/ref/real.html)、[`imag`](https://ww2.mathworks.cn/help/releases/R2022b/matlab/ref/imag.html) 和 [`power`](https://ww2.mathworks.cn/help/releases/R2022b/matlab/ref/power.html)） |-->


::: tip 提示
要执行平方根计算，请使用 [Sqrt](Sqrt.html) 模块。
:::

模块输出是对一个或多个输入执行函数运算的结果。这些函数支持以下类型的运算。

| 函数                                    | 标量运算             | 按元素的向量和矩阵运算                                       | 向量和矩阵运算 |
| :-------------------------------------- | :------------------- | :----------------------------------------------------------- | :------------- |
| `exp`                                   | 是                   | 是                                                           | 不适用         |
| `log`                                   | 是                   | 是                                                           | 不适用         |
| `10^u`                                  | 是                   | 是                                                           | 不适用         |
| `log10`                                 | 是                   | 是                                                           | 不适用         |
| `square`                                | 是                   | 是                                                           | 不适用         |
| `pow`                                   | 是                   | 是                                                           | 不适用         |
| 使用精确法的 `reciprocal`               | 是                   | 是                                                           | 不适用         |
| 使用 Newton-Raphson 方法的 `reciprocal` | 是                   | 是                                                           | 不适用         |
| `rem`                                   | 是，对两个输入均执行 | 是，对两个输入均执行（大小相同的两个向量或两个矩阵、一个标量和一个向量，或者一个标量和一个矩阵） | 不适用         |
| `mod`                                   | 是，对两个输入均执行 | 是，对两个输入均执行（大小相同的两个向量或两个矩阵、一个标量和一个向量，或者一个标量和一个矩阵） | 不适用         |
| `transpose`                             | 是                   | —                                                            | 是             |

函数名称和适当的输入端口数出现在模块上。

<!--暂无
 | `conj`                                  | 是                   | 是                                                           | 不适用         | 
 | `magnitude^2`                           | 是                   | 是                                                           | 不适用         |
 | `hypot`                                 | 是，对两个输入均执行 | 是，对两个输入均执行（大小相同的两个向量或两个矩阵、一个标量和一个向量，或者一个标量和一个矩阵） | —              |
 | `hermitian`                             | 是                   | —                                                            | 是             |
-->

::: tip 提示
当需要向量或矩阵输出时，使用 Math Function 模块。
:::

<!-- ### Newton-Raphson 倒数算法方法

具有 Newton-Raphson 算法方法的 `reciprocal` 函数通过使用 Newton-Raphson 逼近方法来计算倒数。该函数使用递归逼近来求实数值函数根的更佳逼近。

实数 *a* 的倒数定义为函数的零值：



*f*(*x*)=1*x*−*a*



Sysblock 选择 0<*x*0<2*a* 范围内的一个初始估计值，因为这是函数的收敛域。

要连续计算函数的根，请指定**迭代次数**参数。该过程按如下方式重复执行：



*x**i*+1=*x**i*−*f*(*x**i*)*f*′(*x**i*)=*x**i*+(*x**i*−*a**x**i*2)=*x**i*.(2−*a**x**i*)



*f*′(*x*) 是函数 *f*(*x*) 的导数。 -->

### 数据类型支持

下表列出了该模块的每个函数可以支持的输入数据类型。

| 函数                                                         | 单精度 | 双精度 | 半精度* | 布尔 | 内置整数 | 定点 |
| :----------------------------------------------------------- | :----- | :----- | :------ | :--- | :------- | :--- |
| `exp`                                                        | 是     | 是     | 是      | —    | —        | —    |
| `log`                                                        | 是     | 是     | 是      | —    | —        | —    |
| `10^u`                                                       | 是     | 是     | 是      | —    | —        | —    |
| `log10`                                                      | 是     | 是     | 是      | —    | —        | —    |
| `square`                                                     | 是     | 是     | 是      | —    | 是       | 是   |
| `pow`                                                        | 是     | 是     | 是      | —    | —        | —    |
| `reciprocal`                                    | 是     | 是     | 是      | —    | 是       | 是   |
| 使用 Newton-Raphson 方法的 `reciprocal` | 是     | 是     | —       | —    | 是       | 是   |
| `rem`                                                        | 是     | 是     | 是      | —    | 是       | —    |
| `mod`                                                        | 是     | 是     | 是      | —    | 是       | —    |
| `transpose`                                                  | 是     | 是     | 是      | 是   | 是       | 是   |


<!-- 暂无
| `magnitude^2`                                                | 是     | 是     | 是      | —    | 是       | 是   |
| `conj`                                                       | 是     | 是     | 是      | —    | 是       | 是   |
| `hypot`                                                      | 是     | 是     | 是      | —    | —        | —    |
| `hermitian`                                                  | 是     | 是     | 是      | —    | 是       | 是   | -->



## 示例

计算一个以 10 为底，100 的对数。
使用一个 Constant 模块设值为 100，MathFunction 模块的函数选择 log10。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperation/MathFunction.mo">MathFunction.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/MathFunction/MathFunction01.png')" style="width: 600px; ">

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/MathFunction/MathFunction02.png')" style="width: 600px; ">


<!-- ### 可变大小信号基本操作

此示例说明可变大小信号是如何生成的。它还说明了可对这些信号应用的一些操作。此示例旨在介绍与可变大小信号相关联的基本操作。 -->

## 端口


### 输入

<div class="details-box">
<details open>
<summary>u1 — 输入信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

输入信号，指定为标量、向量或矩阵。受支持的模式同时接受实数和复数输入，但 reciprocal 除外，它不接受复数定点输入。

#### 依存关系

此模块的数据类型支持取决于您选择的**函数**和输入的大小。

**数据类型：**  float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | Boolean | fixed point

</div>
</div>


<div class="details-box">
<details open>
<summary>u2 — 输入信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

输入信号，指定为标量、向量或矩阵。受支持的模式同时接受实数和复数输入，但 reciprocal 除外，它不接受复数定点输入。

#### 依存关系

要启用此端口，请将**函数**设置为 **rem** 或 **mod**。

此模块的数据类型支持取决于您选择的**函数**和输入的大小。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | Boolean | fixed point

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 对一个或多个输入执行函数运算的结果<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

输出信号，指定为标量、向量或矩阵。模块输出的维度取决于您选择的**函数**和输入的大小。模块输出是实数还是复数取决于您的**输出信号类型**选项。

</div>
</div>

<div class="details-box">
<details open>
<summary>使用 Newton-Raphson 方法的 reciprocal<div></div></summary>
</details>
<div class="details-content">

使用 Newton-Raphson 方法的 reciprocal 的输出数据类型取决于输入数据类型：

| 输入数据类型                                  | 输出数据类型                                                |
| :-------------------------------------------- | :---------------------------------------------------------- |
| 单精度                                        | 单精度                                                      |
| 双精度                                        | 双精度                                                      |
| 内置整数                                      | 内置整数                                                    |
| 内置定点                                      | 内置定点                                                    |
| `fi` (value, 0, word_length, fraction_length) | `fi` (value, 0, word_length, word_length–fraction_length–1) |
| `fi` (value, 1, word_length, fraction_length) | `fi` (value, 1, word_length, word_length–fraction_length–2) |

**数据类型：**  float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | Boolean | fixed point


</div>
</div>


## 参数


### 主要

<div class="details-box">
<details open>
<summary>函数 — 数学函数<div>exp （默认） | log | 10^u | log10 | square | pow | reciprocal | rem | mod | transpose </div></summary>
</details>
<div class="details-content">

#### 依存关系

将**函数**设置为 **pow** 会启用**有符号幂**参数。

</div>
</div>


<!-- 
#### 编程用法

| **模块参数**：`Operator`                                     |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值：**`'exp' | 'log' | '10^u' | 'log10' | 'square' | 'pow' | 'reciprocal' | 'rem' | 'mod' | 'transpose'|
| **默认值：**`'exp'`                                          | -->


<div class="details-box">
<details open>
<summary>算法方法 — reciprocal 函数的算法方法<div>完全 （默认） | Newton-Raphson</div></summary>
</details>
<div class="details-content">

reciprocal 函数的算法方法，指定为**完全**或 **Newton-Raphson**。要使用 **Newton-Raphson** 逼近方法计算倒数，请选择 **Newton-Raphson**。否则，请选择**完全**。

#### 依存关系

将**函数**设置为**倒数**会启用此参数。

</div>
</div>

<!-- #### 编程用法

| **模块参数**：`AlgorithmType`        |
| ------------------------------------ |
| **类型：**字符向量                   |
| **值：**`'Exact' | 'Newton-Raphson'` |
| **默认值**：`'Exact'`                | -->


<div class="details-box">
<details open>
<summary>有符号幂 — 幂的符号性<div>on （默认） | off</div></summary>
</details>
<div class="details-content">

在计算幂时考虑输入信号的符号，指定为 on 或 off。此参数仅适用于偶数阶根，如 u1/2、u1/4 等。

- **on** - 通过将输入信号绝对值乘以输入信号的符号来计算幂。
- **off** - 计算实际输入值的幂。如果第一个输入为负值，第二个输入为偶数阶根，则返回 `nan`。

#### 依存关系

将**函数**设置为 **pow** 会启用此参数。


</div>
</div>



<!-- #### 编程用法

| **模块参数**：`SignedPower` |
| --------------------------- |
| **类型：**字符向量          |
| **值：**`'on' | 'off' |`    |
| **默认值：**`'on'`          | -->


<!-- 暂无
### `输出信号类型` — 输出信号的复/实性 “`自动`” （默认） | “`实数`” | “`复`”



将 Math Function 模块的输出信号类型指定为 `auto`、`real` 或 `complex`。

| 函数                                                         | 输入信号类型    | 输出信号类型    |               |                    |
| :----------------------------------------------------------- | :-------------- | :-------------- | ------------- | ------------------ |
| 自动                                                         | 实数            | 复数            |               |                    |
| `exp`, `log`, `10u`, `log10`, `square`, `pow`, `reciprocal`, `conjugate`, `transpose`, `hermitian` | `real``complex` | `real``complex` | `real``error` | `complex``complex` |
| `magnitude squared`                                          | `real``complex` | `real``real`    | `real``real`  | `complex``complex` |
| `hypot`, `rem`, `mod`                                        | `real``complex` | `real``error`   | `real``error` | `complex``error`   |

#### 编程用法

| **模块参数**：`OutputSignalType`      |
| ------------------------------------- |
| **类型：**字符向量                    |
| **值：**`'auto' | 'real' | 'complex'` |
| **默认值：**`'auto'`                  | -->



<div class="details-box">
<details open>
<summary>迭代次数 — Newton-Raphson 迭代次数<div> 3 （默认） | 标量</div></summary>
</details>
<div class="details-content">

Newton-Raphson 迭代次数，指定为标量。

#### 依存关系

要启用此参数，请进行如下设置：

- **函数**设置为**倒数**。
- **算法方法**设置为 **Newton-Raphson**。

</div>
</div>


<!-- 
#### 编程用法

| **模块参数**：`Iterations` |
| -------------------------- |
| **类型：**字符向量         |
| **值：**`'3' | scalar`     |
| **默认值：**`'3'`          | -->


<!-- 
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
| **默认值**：`'[ ]'`    | -->


<!-- 暂无
### `输出数据类型` — 指定输出数据类型 `Inherit: Same as first input` （默认） | `Inherit: Inherit via internal rule` | `Inherit: Inherit via back propagation` | “`double`” | “`single`” | “`half`” | “`int8`” | “`uint8`” | “`int16`” | “`uint16`” | “`int32`” | “`uint32`” | “`int64`” | “`uint64`” | “`fixdt(1,16)`” | “`fixdt(1,16,0)`” | “`fixdt(1,16,2^0,0)`” | “`<data type expression>`”



指定输出数据类型。可以将其设置为：

- 继承数据类型的规则，例如 “`Inherit: Inherit via back propagation`”
- 内置数据类型的名称，例如 `single`
- 数据类型对象的名称，例如 `Simulink.NumericType` 对象
- 计算结果为数据类型的表达式，例如 `fixdt(1,16,0)`

单击**显示数据类型助手**按钮 ![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/show_data_type_asst_button.png) 以显示**数据类型助手**，帮助您设置数据类型属性。有关详细信息，请参阅[使用数据类型助手指定数据类型](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/specify-data-types-using-data-type-assistant.html)。

#### 依存关系

- 要启用此参数，请将**函数**设置为 “`magnitude^2`”、“`方波`”或“`倒数`”。
- 对于 “`magnitude^2`” 和 “`square`”，当输入是小于单精度的浮点数据类型时，“`Inherit: Inherit via internal rule`” 输出数据类型取决于 [Inherit floating-point output type smaller than single precision](https://ww2.mathworks.cn/help/releases/R2022b/simulink/gui/inherit-floating-point-output-type-smaller-than-single-precision.html) 配置参数的设置。当编码数据类型所需的位数小于编码单精度数据类型所需的 32 位时，数据类型小于单精度。例如，`half` 和 `int16` 小于单精度。

#### 编程用法

| **模块参数**：`OutDataTypeStr`                               |
| ------------------------------------------------------------ |
| **类型**：字符向量                                           |
| **值**：`'Inherit: Inherit via internal rule` | `'Inherit: Same as first input'` | `'Inherit: Inherit via back propagation'` | `'double'` | `'single'` | `'half'` | `'int8'` | `'uint8'` | `'int16'` | `'uint16'` | `'int32'` | `'uint32'` | `'int64'` | `'uint64'` | `'fixdt(1,16)'` | `'fixdt(1,16,0)'` | `'fixdt(1,16,2^0,0)'` | `'<data type expression>'` |
| **默认值**：`'Inherit: Same as first input'`                 | -->


<!-- 暂无
### `锁定输出数据类型设置以防止被定点工具更改` — 防止定点工具覆盖数据类型 `off` （默认） | `on`



选择此参数可防止定点工具覆盖您在模块上指定的**输出**数据类型。有关详细信息，请参阅[Use Lock Output Data Type Setting](https://ww2.mathworks.cn/help/releases/R2022b/fixedpoint/ug/best-practices-for-using-the-fixed-point-tool-to-propose-data-types-for-your-simulink-model.html#br9an48) (Fixed-Point Designer)。

#### 依存关系

要启用此参数，请将**函数**设置为 “`magnitude^2`”、“`方波`”或“`倒数`”。

#### 编程用法

| **模块参数**：`LockScale` |
| ------------------------- |
| **类型：**字符向量        |
| **值：**`'off' | 'on'`    |
| **默认值：**`'off'`       | -->


<!-- 暂无
### `整数舍入模式` — 定点运算的舍入模式 “`向下`” （默认） | “`向上`” | “`收敛`” | “`最邻近值`” | “`舍入`” | “`最简`” | “`零`”



定点运算的舍入模式。有关详细信息，请参阅[舍入](https://ww2.mathworks.cn/help/releases/R2022b/fixedpoint/ug/rounding.html) (Fixed-Point Designer)。

模块参数始终舍入到最接近的可表示值。要控制模块参数的舍入方法，请在封装字段中使用 MATLAB 舍入函数输入表达式。

#### 依存关系

要启用此参数，请将**函数**设置为 “`magnitude^2`”、“`方波`”或“`倒数`”。

#### 编程用法

| **模块参数**：`RndMeth`                                      |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值：**`'Ceiling' | 'Convergent' | 'Floor' | 'Nearest' | 'Round' | 'Simplest' | 'Zero'` |
| **默认值：**`'Floor'`                                        | -->

<!-- 暂无

### `对整数溢出进行饱和处理` — 选择发生整数溢出时的行为 `on` （默认） | 布尔





| 操作                                     | 原理说明                                                     | 溢出                                               | 示例                                                         |
| :--------------------------------------- | :----------------------------------------------------------- | :------------------------------------------------- | :----------------------------------------------------------- |
| 选中**对整数溢出进行饱和处理**复选框。   | 您的模型可能有溢出，并且您希望在生成的代码中具有显式饱和保护。 | 将溢出饱和处理为数据类型能够表示的最小值或最大值。 | `int8`（有符号 8 位整数）数据类型可以表示的最大值为 127。任何大于此最大值的模块运算结果都会导致 8 位整数溢出。如果选中此复选框，模块输出将在达到 127 时饱和。类似地，模块输出将在达到最小输出值 -128 时饱和。 |
| 不选中**对整数溢出进行饱和处理**复选框。 | 您需要优化所生成代码的效率。您希望避免过度地指定信号超出范围时的处理方式。有关详细信息，请参阅[信号范围错误故障排除](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/signal-ranges.html#brdiku9)。 | 溢出会绕回到由数据类型表示的适当值。               | `int8`（有符号 8 位整数）数据类型可以表示的最大值为 127。任何大于此最大值的模块运算结果都会导致 8 位整数溢出。清除该复选框时，软件会将导致溢出的值解释为 `int8`，这可能产生意外结果。例如，以 `int8` 表示的模块结果 130（二进制 1000 0010）为 -126。 |



如果选中此复选框，饱和将应用于模块中的每个内部操作，而不仅仅应用于输出或结果。代码生成过程可以检测何时不会发生溢出。在这种情况下，代码生成器不会生成饱和代码。

#### 依存关系

要启用此参数，请将**函数**设置为 “`magnitude^2`”、“`方波`”、“`conj`”、“`倒数`”或 “`hermitian`”。

#### 编程用法

| **模块参数**：`SaturateOnIntegerOverflow` |
| ----------------------------------------- |
| **类型**：字符向量                        |
| **值**：`'off'` | `'on'`                  |
|                                           |
| **默认值**：`'on'`                        | -->


<!-- ## 模块特性 -->

<!-- 部分属性暂无
| **数据类型**     | `Boolean` \| `double` \| `fixed point` \| `half` \| `integer` \| `single` |
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

| 函数        | 架构                 | 描述                                                         |
| :---------- | :------------------- | :----------------------------------------------------------- |
| `conj`      | “`ComplexConjugate`” | 计算复共轭。                                                 |
| `hermitian` | “`hermitian`”        | 计算 hermitian。                                             |
| `transpose` | “`转置`”             | 计算数组转置。请参阅 Simulink 文档中的[Math Function](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/mathfunction.html)。 |

**倒数架构**

您可以通过使用 `reciprocal` 函数的“`数学`”架构在本机浮点模式下为单精度浮点数据类型生成 HDL 代码。Math Function 模块中的 `reciprocal` 函数也支持表中列出的架构。

| 架构                                 | 参数         | 额外的延迟周期                                               | 描述                                                         |
| :----------------------------------- | :----------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| 倒数                                 | 无           | 0                                                            | 通过使用 HDL 除法 (`/`) 运算符实现除法，以 `1/N` 的形式计算倒数。 |
| ReciprocalRsqrtBasedNewton           | `Iterations` | 有符号输入：`Iterations` + 5无符号输入：`Iterations` + 3     | 使用牛顿迭代法。选择此选项以优化面积。`Iterations` 的默认值为 3。`Iterations` 的推荐值为 2 到 10。如果 `Iterations` 超出推荐范围，HDL Coder 会生成一条消息。 |
| ReciprocalRsqrtBasedNewtonSingleRate | `Iterations` | 有符号输入：(`Iterations` * 4) + 8无符号输入：(`Iterations` * 4) + 6 | 使用单频率流水线牛顿法。要优化速度或需要单速率实现，请选择此选项。`Iterations` 的默认值为 3。`Iterations` 的推荐值为 2 到 10。如果 `Iterations` 超出推荐范围，代码生成器会生成一条消息。 |
| “`ShiftAdd`”                         | UsePipelines | 有符号输入：（输入字长 + 4）无符号输入：（输入字长 + 4）     | 通过使用非还原除法算法对定点输入执行倒数运算，该算法执行多次移位相加运算来计算倒数。与 Newton-Raphson 逼近方法相比，这种架构提高了精度。当您使用这种架构时，为了在目标 FPGA 设备上实现更高的最大时钟频率，请将 **UsePipelines** HDL 模块属性保留为 `on`。使用定点数据类型时，必须满足以下标准才能生成 HDL 代码：输入字长 (`WL`) 必须小于或等于 63。`[WL input + Abs(FL Sum)]` 必须小于或等于 63。其中，` FL Sum` 由下式给出：`FL sum = FL input + FL output` |

当算法方法设置为“精确”时，您可以在此模块的 HDL 模块属性中选择这些选项。

此模块具有多周期实现，这会在生成的代码中引入额外的延迟。要查看增加的延迟，请查看生成的模型或验证模型。请参阅[Generated Model and Validation Model](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/generated-model-and-validation-model.html) (HDL Coder)。

对于 `reciprocal` 函数，HDL 代码生成还支持 Newton-Raphson 算法方法。选择**算法方法**为 “`Newton-Raphson`”，以将这些架构用于 Math Function 模块中的 `reciprocal` 函数。

| 架构                           | 额外的延迟周期         | 描述                                                         |
| :----------------------------- | :--------------------- | :----------------------------------------------------------- |
| “`ReciprocalNewton`”（默认值） | `Iterations` + 1       | 使用牛顿迭代法的多速率实现。选择此选项可优化设计区域。`Iterations` 的默认值为 3。`Iterations` 的推荐值为 2 到 10。如果 `Iterations` 的值超出建议的范围，HDL Coder 将显示一条消息。 |
| “`ReciprocalNewtonSingleRate`” | (`Iterations` * 2) + 1 | 使用单频率流水线牛顿法。要为您的设计优化速度或需要单速率实现，请选择此选项。`Iterations` 的默认值为 3。`Iterations` 的建议值介于 2 到 10 之间。如果 `Iterations` 值超出建议的范围，HDL Coder 将显示一条消息。 |



**HDL 模块属性**

| 通用                          |                                                              |
| :---------------------------- | ------------------------------------------------------------ |
| **ConstrainedOutputPipeline** | 通过移动设计中现有延迟的方式来放置在输出端的寄存器的数量。分布式流水线处理不会重新分发这些寄存器。默认值为 `0`。有关详细信息，请参阅[ConstrainedOutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#btp8gmp) (HDL Coder)。 |
| **InputPipeline**             | 要在生成的代码中插入的输入流水线级数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 `0`。有关详细信息，请参阅[InputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-25) (HDL Coder)。 |
| **OutputPipeline**            | 要在生成的代码中插入的输出流水线级数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 `0`。有关详细信息，请参阅[OutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-26) (HDL Coder)。 |

| 本机浮点             |                                                              |
| :------------------- | ------------------------------------------------------------ |
| **CheckResetToZero** | 将此属性用于 Math Function 模块的 `mod` 和 `rem` 函数。如果两个数 `a` 和 `b` 的商 `a/b` 接近整数，则此设置将 `a` 视为 `b` 的整数倍且 `rem(a,b)` = 0。该结果在数值上是精确的，并且与仿真结果相匹配。计算该结果会使用额外的资源，并会增加目标 FPGA 设备上的占用面积。有关详细信息，请参阅 [CheckResetToZero](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/hdl-block-properties-native-floating-point.html#mw_f60d6f02-d387-4b02-b23c-db65ea3d5549) (HDL Coder)。 |
| **HandleDenormals**  | 指定是否希望 HDL Coder 在设计中插入额外的逻辑来处理非正规数字。非规范数是量级非常小、必须使用包含前导零的尾数才能表示的浮点数。默认值为 “`inherit`”。另请参阅[HandleDenormals](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/hdl-block-properties-native-floating-point.html#mw_34395404-aeac-43da-bb3c-96c4a420c9e1) (HDL Coder)。 |
| **LatencyStrategy**  | 指定对于浮点运算符是否将设计中的模块映射到 `inherit`、`Max`、`Min`、`Zero` 或 `Custom`。默认值为 “`inherit`”。另请参阅[LatencyStrategy](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/hdl-block-properties-native-floating-point.html#mw_a99b0822-f2a6-4f5b-aca9-7f7251a67c7c) (HDL Coder)。 |
| **NFPCustomLatency** | 要指定值，请将 **LatencyStrategy** 设置为 `Custom`。HDL Coder 会增加延迟，其值等于您为 **NFPCustomLatency** 设置指定的值。另请参阅[NFPCustomLatency](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/hdl-block-properties-native-floating-point.html#mw_e29db696-7117-431a-a8b8-4471b8d24ea8) (HDL Coder)。 |
| **MaxIterations**    | 将此属性用于 Math Function 模块的 `mod` 和 `rem` 函数。如果您的两个数 `a` 和 `b` 是非常大的整数，您可以增大 **MaxIterations** 以匹配仿真结果。计算该结果会使用额外的资源，并会增加目标 FPGA 设备上的占用面积。有关详细信息，请参阅 [MaxIterations](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/hdl-block-properties-native-floating-point.html#mw_9b23285a-5a3b-4f00-96bb-2f4a73a3e889) (HDL Coder)。 |

**支持本机浮点的数据类型和函数**

在 Math Function 模块中，下列函数支持本机浮点。

| 数学函数      | 支持的浮点数据类型 | 复数数据支持 |      |      |
| :------------ | :----------------- | :----------- | ---- | ---- |
| 半精度        | 单精度             | 双精度       |      |      |
| `exp`         | 否                 | 是           | 否   | 否   |
| `log`         | 否                 | 是           | 是   | 否   |
| `10^u`        | 否                 | 是           | 否   | 否   |
| `log10`       | 否                 | 是           | 否   | 否   |
| `magnitude^2` | 否                 | 是           | 是   | 是   |
| `square`      | 否                 | 是           | 否   | 是   |
| `pow`         | 否                 | 是           | 否   | 否   |
| `conj`        | 否                 | 是           | 否   | 是   |
| `reciprocal`  | 是                 | 是           | 是   | 否   |
| `hypot`       | 否                 | 是           | 否   | 否   |
| `rem`         | 否                 | 是           | 否   | 否   |
| `mod`         | 否                 | 是           | 否   | 否   |
| `transpose`   | 是                 | 是           | 是   | 是   |
| `hermitian`   | 否                 | 是           | 否   | 是   |



**限制**

当您使用“`倒数`”实现时：

- 输入必须为标量，并且必须具有整数或定点（有符号或无符号）数据类型。
- 输出必须为标量，并且具有整数或定点（有符号或无符号）数据类型。
- 仅支持“`零`”舍入模式。
- 必须对模块选择**对整数溢出进行饱和处理**选项。



### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。

Math Function 模块只支持某些配置中的定点转换。有关详细信息，请参阅 [Block Support Table](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/blocksupporttable.html)。 -->

## 版本历史记录

- 在 2024b 之前推出

### 限制信息

1. 参数-常设-输出信号类型 — 输出信号的复/实性
2. 参数-常设-迭代次数 — Newton-Raphson 迭代次数
3. 参数-常设-采样时间 — -1 以外的采样时间值
4. 参数-常设-信号属性-输出最小值 — 范围检查的最小输出值

5. 参数-常设-信号属性-输出最大值 — 范围检查的最大输出值

6. 参数-常设-信号属性-锁定输出数据类型设置以防止被定点工具更改 — 防止定点工具覆盖数据类型
7. 参数-常设-信号属性-整数舍入模式 — 定点运算的舍入模式
8. 参数-常设-信号属性-整数舍入模式-对整数溢出进行饱和处理 — 选择发生整数溢出时的行为



## 另请参阅

[Sqrt](Sqrt.html) | [TrigonometricFunction](TrigonometricFunction.html)
