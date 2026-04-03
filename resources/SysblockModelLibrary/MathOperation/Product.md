# Product
---
&nbsp;

标量和非标量的乘除运算或者矩阵的乘法和逆运算

- **库：** Sysblock / MathOperation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/Product/Product.png')" style="width: 100px; height: auto;">

## 描述

Product 模块输出两个输入（两个标量、一个标量和一个非标量，或者具有相同维度的两个非标量）的相乘结果。指定此行为的默认参数值包括：

- **乘法：** 按元素 (.*)
- **输入的数目**：2

Product 模块可以执行标量或矩阵乘法运算，具体取决于**乘法**参数的值。此模块接受一个或多个输入，具体取决于**输入的数目**参数。**输入的数目**参数还指定要对每个输入执行的运算。

Product 模块可以输入标量、向量和矩阵的任意组合，对于这些输入，执行的运算必须具有数学定义的结果。该模块对输入执行指定的运算，然后输出结果。

Product 模块有两种模式：**按元素模式**，按元素处理非标量输入元素；**矩阵模式**，以矩阵方式处理非标量输入。

### 按元素模式

当**乘法**设置为按元素 (.*) 时，Product 模块即处于**按元素模式**，在这种模式下，模块将对任何非标量输入的单个数值元素执行运算。

**输入的数目**参数的值控制存在多少个输入，以及是乘以还是除以每个输入以得到输出。当模块具有多个输入时，任何非标量输入都必须具有相同的维度，而模块将输出具有这些维度的非标量。为了计算输出，模块首先将任何标量输入展开为与非标量输入具有相同维度的非标量。

### 矩阵模式

当**乘法**参数的值为矩阵 (*) 时，Product 模块即处于**矩阵模式**，在这种模式下，模块按矩阵处理非标量输入。

**输入的数目**参数的值既控制存在多少个输入，也控制是乘以还是除以每个输入矩阵以得到输出。**输入的数目**的语法与按元素模式相同。这两个模式的不同之处在于发生的乘法和除法的类型。

### 模块输入和模式之间的交互

Product 模块输入与其**乘法**模式之间的交互如下：

- 1 或 \ 或 /

- 大于 1 的整数值

- 不带引号的含有两个或更多 \ 和 / 字符的字符串

<!-- ### 仿真与代码生成之间的预期差异

对于复数浮点输入的按元素运算，仿真和代码生成结果在接近溢出情况下可能会有所差异。尽管在**配置参数**对话框的**代码生成** > **接口**窗格上选中了**复数**且取消选中了**非有限数**，代码生成器也不会为中间溢出生成特殊情况代码。此方法可以提高嵌入式运算在不含极值的一般情况下的效率。如果输入可能包含极值，必须显式处理这些情况。

如果 `NaN` 和 `inf` 值在数学上没有意义，则生成的代码可能不会为这些值生成与仿真相同的模式。例如，如果仿真输出包含 `NaN`，生成的代码的输出也会包含 `NaN`，但不一定在相同的位置。 -->

## 示例

对两个常量值进行相乘。将两个 Constant 模块设置为 2 分别连接到 Product 模块的两个输入端。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperation/Product.mo">Product.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/Product/Product01.png')" style="width: 600px; ">

## 端口

### 输入

<div class="details-box">
<details open>
<summary>u1 — 要进行乘法或除法运算的第一个输入<div>标量 | 向量 | 矩阵 | N 维数组</div></summary>
</details>
<div class="details-content">

要进行乘法或除法运算的第一个输入，作为标量、向量、矩阵或 N 维数组提供。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | fixed point

</div>
</div>


<div class="details-box">
<details open>
<summary>u2 — 要进行乘法或除法运算的第 N 个输入<div>标量 | 向量 | 矩阵 | N 维数组</div></summary>
</details>
<div class="details-content">

要进行乘法或除法运算的第 N 个输入，作为标量、向量、矩阵或 N 维数组提供。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | fixed point

</div>
</div>

<div class="details-box">
<details open>
<summary>X — 要相乘的输入信号<div>标量 | 向量 | 矩阵 | N 维数组</div></summary>
</details>
<div class="details-content">

要与其他输入相乘的输入信号。

#### 依存关系

要启用一个或多个 **X** 端口，请为**输入的数目**参数指定一个或多个 * 字符，并将**乘法**参数设置为**按元素 (.*)**。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | fixed point

</div>
</div>

<div class="details-box">
<details open>
<summary>÷ — 要进行除法或逆运算的输入信号<div>标量 | 向量 | 矩阵 | N 维数组</div></summary>
</details>
<div class="details-content">

要进行除法或逆运算的输入信号。

#### 依存关系

要启用一个或多个 **÷** 端口，请为**输入的数目**参数指定一个或多个 / 字符，并将**乘法**参数设置为**按元素 (.*)**。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | fixed point

</div>
</div>

<div class="details-box">
<details open>
<summary>* — 要相乘的输入信号<div>标量 | 向量 | 矩阵 | N 维数组</div></summary>
</details>
<div class="details-content">

要与其他输入相乘的输入信号。

#### 依存关系

要启用一个或多个 * 端口，请为**输入数目**参数指定一个或多个 * 字符，并将**乘法**参数设置为**矩阵 (*)**。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | fixed point

</div>
</div>

<div class="details-box">
<details open>
<summary>Inv — 要进行除法或逆运算的输入信号<div>标量 | 向量 | 矩阵 | N 维数组</div></summary>
</details>
<div class="details-content">

要进行除法或逆运算的输入信号。

#### 依存关系

要启用一个或多个 **Inv** 端口，请为**输入数目**参数指定一个或多个 / 字符，并将**乘法**参数设置为**矩阵 (*)**。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | fixed point

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 通过对输入进行乘法、除法或逆运算来计算得出输出<div>标量 | 向量 | 矩阵 | N 维数组</div></summary>
</details>
<div class="details-content">

通过对输入进行乘法、除法或逆运算来计算得出输出。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | fixed point

</div>
</div>


## 参数


### 主要

<div class="details-box">
<details open>
<summary>输入的数目 — 控制输入的数量和运算的类型<div>**（默认） | 标量 | 对每个输入端口应用 * 或 /</div></summary>
</details>
<div class="details-content">

控制模块的两个属性：

- 模块上的输入端口数
- 是乘以还是除以每个输入来得到输出

</div>
</div>

<!-- 
如果您指定：

- **1 或 \* 或 /**

  模块有一个输入端口。在按元素模式下，模块按照 [Product of Elements](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/productofelements.html) 模块说明处理输入。在矩阵模式下，如果参数值为 `1` 或 `*`，则模块将输出输入值。如果值为 `/`，则输入必须为方阵（包括作为简并情况的标量），模块将输出逆矩阵。有关详细信息，请参阅[按元素模式](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/product.html#brofebg)和[矩阵模式](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/product.html#brofoay-1)。

- **大于 1 的整数值**

  模块的输入的数量由整数值指定。输入依**乘法**参数指定的按元素模式或矩阵模式相乘。有关详细信息，请参阅[按元素模式](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/product.html#brofebg)和[矩阵模式](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/product.html#brofoay-1)。

- **不带引号的含有两个或更多 `\*` 和 `/` 字符的字符串**

  模块的输入的数量由字符向量长度指定。乘以与 `*` 字符相对应的每个输入来得到输出。除以与 `/` 字符相对应的每个输入来得到输出。依**乘法**参数指定的按元素模式或矩阵模式进行运算。有关详细信息，请参阅[按元素模式](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/product.html#brofebg)和[矩阵模式](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/product.html#brofoay-1)。 -->

<!-- 
#### 编程用法

| **模块参数**：`Inputs`                    |
| ----------------------------------------- |
| **类型：**字符向量                        |
| **值：**`'2' | '**' | '*/' | '*/*' | ...` |
| **默认值：**`'2'`                         | -->


<div class="details-box">
<details open>
<summary>乘法 — 按元素 (.* ) 或矩阵 (* )<div>乘法 按元素(.* )（默认） | 矩阵(*)</div></summary>
</details>
<div class="details-content">

指定模块是执行**按元素 (.*)** 还是**矩阵 (*)** 乘法。

</div>
</div>


<!-- 
#### 编程用法

| **模块参数**：`Multiplication`             |
| ------------------------------------------ |
| **类型：**字符向量                         |
| **值：**`'Element-wise(.*)' | 'Matrix(*)'` |
| **默认值：**`'Element-wise(.*)'`           |
 -->

<!-- 暂无
### `乘法运算维度` — 所有维度或指定维度 “`所有维度`” （默认） | “`指定的维度`”



指定要乘以的维度是“`所有维度`”还是“`指定的维度`”。当选择“`指定的维度`”时，您可以将**维度**指定为 `1` 或 `2`。

#### 依存关系

要启用此参数，请将**输入的数目**设置为 `*` 并将**乘法**设置为“`按元素(.*)`”。

#### 编程用法

| **模块参数**：`CollapseMode`                       |
| -------------------------------------------------- |
| **类型：**字符向量                                 |
| **值：**`'All dimensions' | 'Specified dimension'` |
| **默认值：**`'All dimensions'`                     | -->


<!-- 暂无
### `维度` — 要进行乘法运算的维度 `1` （默认） | `2` | `...` | `N`



要进行乘法运算的维度需指定为小于或等于输入信号的维度数量的整数。

#### 依存关系

要启用此参数，请进行如下设置：

- 将**输入的数目**设置为 `*`
- 将**乘法**设置为“`按元素(.*)`”
- 将**乘法运算维度**设置为“`指定的维度`”



#### 编程用法

| **模块参数**：`CollapseDim` |
| --------------------------- |
| **类型：**字符向量          |
| **值：**`'1' | '2' | ...`   |
| **默认值：**`'1'`           | -->


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

### 信号属性

<!-- 暂无

### `要求所有输入具有相同的数据类型` — 要求所有输入具有相同的数据类型 `off` （默认） | `on`



指定输入信号是否必须全部具有相同的数据类型。如果启用此参数，则在输入信号类型不同时，仿真过程中会发生错误。

#### 编程用法

| **模块参数**：`InputSameDT` |
| --------------------------- |
| **类型：**字符向量          |
| **值：**`'off' | 'on'`      |
| **默认值：**`'off'`         | -->

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


<div class="details-box">
<details open>
<summary>输出数据类型 — 指定输出数据类型<div>Inherit: internalRule（默认） | Inherit: keepMSB | Inherit: matchScaling | Inherit: backPropagation | Inherit: sameAsFirstInput | double | float | int8 | uint8 | int16 | uint16 | int32 | uint32 | fixdt(1,16,0) | fixdt(1,16,2^0,0) | fixdt(1,16,1.0,0,0.0) </div></summary>
</details>
<div class="details-content">

为输出选择数据类型。该类型可以继承、直接指定或表示为数据类型对象。

</div>
</div>

<!-- 
#### 编程用法

| **模块参数**：`OutDataTypeStr`                               |
| ------------------------------------------------------------ |
| **类型**：字符向量                                           |
| **值**：`'Inherit: Inherit via internal rule` | `'Inherit: Keep MSB'`| `'Inherit: Match scaling'`| `'Inherit: Same as first input'` | `'Inherit: Inherit via back propagation'` | `'double'` | `'single'` | `'half'` | `'int8'` | `'uint8'` | `'int16'` | `'uint16'` | `'int32'` | `'uint32'` | `'uint64'`|`'int64'`|`'fixdt(1,16)'` | `'fixdt(1,16,0)'` | `'fixdt(1,16,2^0,0)'` | `'<data type expression>'` |
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



选择定点运算的舍入模式。您可以选择：

- “`向上`”

  朝正无穷方向舍入正数和负数。等同于 MATLAB `ceil` 函数。

- “`收敛`”

  将数值舍入到最接近的可表示值。如果出现结值，则舍入到最接近的偶数整数。等同于 Fixed-Point Designer™ `convergent` 函数。

- “`向下`”

  朝负无穷方向舍入正数和负数。等同于 MATLAB `floor` 函数。

- “`最邻近值`”

  将数值舍入到最接近的可表示值。如果出现结值，则朝正无穷方向舍入。等同于 Fixed-Point Designer `nearest` 函数。

- “`舍入`”

  将数值舍入到最接近的可表示值。如果出现结值，则将正数朝正无穷方向舍入，将负数朝负无穷方向舍入。等同于 Fixed-Point Designer `round` 函数。

- “`最简`”

  在向负无穷大方向舍入和向零舍入之间选择，以生成尽可能有效的舍入代码。

- “`零`”

  将数值向零舍入。等同于 MATLAB `fix` 函数。

有关详细信息，请参阅[舍入](https://ww2.mathworks.cn/help/releases/R2022b/fixedpoint/ug/rounding.html) (Fixed-Point Designer)。

模块参数始终舍入到最接近的可表示值。要控制模块参数的舍入方法，请在封装字段中使用 MATLAB 舍入函数输入表达式。

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
| 不选中此复选框 (off)。 | 您需要优化所生成代码的效率。您希望避免过度地指定信号超出范围时的处理方式。 | 溢出会绕回到由数据类型表示的适当值。               | int8（有符号 8 位整数）数据类型可以表示的最大值为 127。任何大于此最大值的模块运算结果都会导致 8 位整数溢出。清除该复选框时，软件会将导致溢出的值解释为 int8，这可能产生意外结果。例如，以 int8 表示的模块结果 130（二进制 1000 0010）为 -126。 |



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
<!-- 部分功能暂无
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

默认的“`线性`”实现为 N 个输入生成包含 N 个运算（乘法器）的运算链。

| **架构**         | **参数**            | **描述**                                                     |
| ---------------- | ------------------- | ------------------------------------------------------------ |
| “`线性`”“`默认`” | 无                  | 在生成的代码中生成乘积运算符 `*`。                           |
| “`ShiftAdd`”     | **LatencyStrategy** | 通过使用多个移位相加运算对定点类型执行乘积运算。该模块具有流水线实现，这会在生成的代码中引入额外的延迟。“`ShiftAdd`” 架构可映射到 ASIC 应用中的高效电路。这种架构在没有 DSP 单元的 FPGA 目标板上的应用中非常有用。不同字长的 `MAX` 延迟使用以下公式进行计算：`ceil(log2(min(in1WL,in2WL)))`。`in1WL` 是第一个输入字长，`in2WL` 是第二个输入字长。例如，如果两个输入的字长均为 4，则 `MAX` 延迟为 2。 |

**HDL 模块属性**

如果在矩阵乘法模式下使用该模块，可以指定 **DotProductStrategy**。此设置决定您是要通过使用加法器和乘法器树来实现矩阵乘法，还是使用 Multiply-Accumulate 模块实现。默认值为 `Fully Parallel`。



**注意**

使用 `Native Floating Point` 模式时，**DotProductStrategy** 必须设置为 `Fully Parallel`。

有关详细信息，请参阅 [DotProductStrategy](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#mw_5ce3de4a-ff91-420d-bea4-96e2fd32f914) (HDL Coder)。

另请参阅[Design Considerations for Matrices and Vectors](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/convert-between-2d-and-1d-signals.html) (HDL Coder)。

| 通用                          |                                                              |
| :---------------------------- | ------------------------------------------------------------ |
| **ConstrainedOutputPipeline** | 通过移动设计中现有延迟的方式来放置在输出端的寄存器的数量。分布式流水线处理不会重新分发这些寄存器。默认值为 `0`。有关详细信息，请参阅[ConstrainedOutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#btp8gmp) (HDL Coder)。 |
| **DSPStyle**                  | 乘法器映射的综合属性。默认值为“`无`”。另请参阅[DSPStyle](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bubc5wb-1) (HDL Coder)。 |
| **InputPipeline**             | 要在生成的代码中插入的输入流水线级数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 `0`。有关详细信息，请参阅[InputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-25) (HDL Coder)。 |
| **OutputPipeline**            | 要在生成的代码中插入的输出流水线级数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 `0`。有关详细信息，请参阅[OutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-26) (HDL Coder)。 |
| **LatencyStrategy**           | 要启用此属性，请将 HDL 架构设置为 “`ShiftAdd`”。对于定点和浮点类型，指定是将设计中的模块映射到 `MAX`、`CUSTOM` 还是 `ZERO` 延迟。默认值为 “`MAX`”。另请参阅[LatencyStrategy](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/hdl-block-properties-native-floating-point.html#mw_a99b0822-f2a6-4f5b-aca9-7f7251a67c7c) (HDL Coder)。 |
| **CustomLatency**             | 要启用此属性，请将 HDL 架构设置为 “`ShiftAdd`”。当 **LatencyStrategy** 设置为 `CUSTOM` 时，使用此属性为定点类型指定介于 `ZERO` 和 `MAX` 之间的自定义延迟值。另请参阅[LatencyStrategy](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/hdl-block-properties-native-floating-point.html#mw_a99b0822-f2a6-4f5b-aca9-7f7251a67c7c) (HDL Coder)。 |

| 本机浮点                     |                                                              |
| :--------------------------- | ------------------------------------------------------------ |
| **HandleDenormals**          | 指定是否希望 HDL Coder 在设计中插入额外的逻辑来处理非正规数字。非规范数是量级非常小、必须使用包含前导零的尾数才能表示的浮点数。默认值为 “`inherit`”。另请参阅[HandleDenormals](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/hdl-block-properties-native-floating-point.html#mw_34395404-aeac-43da-bb3c-96c4a420c9e1) (HDL Coder)。 |
| **LatencyStrategy**          | 指定对于浮点运算符是否将设计中的模块映射到 `inherit`、`Max`、`Min`、`Zero` 或 `Custom`。默认值为 “`inherit`”。另请参阅[LatencyStrategy](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/hdl-block-properties-native-floating-point.html#mw_a99b0822-f2a6-4f5b-aca9-7f7251a67c7c) (HDL Coder)。 |
| **NFPCustomLatency**         | 要指定值，请将 **LatencyStrategy** 设置为 `Custom`。HDL Coder 会增加延迟，其值等于您为 **NFPCustomLatency** 设置指定的值。另请参阅[NFPCustomLatency](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/hdl-block-properties-native-floating-point.html#mw_e29db696-7117-431a-a8b8-4471b8d24ea8) (HDL Coder)。 |
| **MantissaMultiplyStrategy** | 指定在代码生成期间如何实现尾数乘法运算。通过使用不同设置，您可以控制目标 FPGA 设备上 DSP 的使用。默认值为 “`inherit`”。另请参阅[MantissaMultiplyStrategy](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/hdl-block-properties-native-floating-point.html#mw_425f11cb-a3a5-45aa-a3aa-df5a7c765b5f) (HDL Coder)。 |

**复数数据支持**

默认（线性）实现支持复数数据。

不支持复数除法。关于在除法模式或倒数模式下 Product 模块的模块实现，请参阅 Divide 模块参考页上的 [HDL 代码生成](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/divide.html#f6-2156461_hdl)。

**限制**

- 当您在矩阵乘法模式下使用模块时，HDL 代码生成不支持模块端口上有两个以上的输入。
- **输入的数目**模块参数值为 “`/*`” 的 Product 模块执行除法，其中第二个输入除以第一个输入。此模式的限制与适用于 Divide 模块的限制相同。请参阅[HDL 代码生成](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/divide.html#f6-2156461_hdl)。
- Product 模块不支持 “`ShiftAdd`” 架构中的共享优化。要在 Product 模块上应用共享优化，请考虑使用“`线性`”架构。要查看子系统的共享优化结果，请生成**流式传输并共享报告**。



### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。 -->

## 版本历史记录

- 在 2024b 之前推出

### 限制信息
不支持部分
1. 参数-主要-乘法运算维度 — 所有维度或指定维度
2. 参数-主要-维度 — 要进行乘法运算的维度
3. 参数-主要-采样时间 — -1 以外的采样时间值
4. 参数-信号属性-要求所有输入具有相同的数据类型 — 要求所有输入具有相同的数据类型
5. 参数-信号属性-输出最小值 — 范围检查的最小输出值
6. 参数-信号属性-输出最大值 — 范围检查的最大输出值
7. 参数-信号属性-锁定输出数据类型设置以防止被定点工具更改 — 防止定点工具覆盖输出数据类型
8. 参数-信号属性-整数舍入模式 — 定点运算的舍入模式


## 另请参阅
[DotProduct](DotProduct.html) 

