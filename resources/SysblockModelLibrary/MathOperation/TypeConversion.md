# TypeConversion
---
&nbsp;

将输入信号转换为指定的数据类型

- **库：** Sysblock / MathOperation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/TypeConversion/TypeConversion.png')" style="width: 100px; height: auto;">


## 描述

TypeConversion 模块可将任何数据类型的输入信号转换为您指定的数据类型。


::: warning 注意

要通过指定模块参数来控制输出数据类型，或者要从下游模块继承数据类型，请使用 TypeConversion 模块。

:::

### 转换定点信号

在定点数据类型之间转换时，可以通过**输入和输出具有相等的**参数来控制模块的行为。在以下情况下，此参数不会更改模块的行为：

- 输入和输出没有定点数据类型。
- 输入或输出使用具有平凡定标的定点数据类型。

要通过保留输入信号的真实值，将信号从一种数据类型转换为另一种数据类型，请选择默认值**真实值（RWV）**。模块会解释由输入和输出的定标施加的限制，并尝试生成具有相等真实值的输出。

要通过对存储的整数值执行定标重新解释来更改输入信号的真实值，请选择**存储的整数（SI）**。在转换过程中，模块将尝试在指定的数据类型范围内保留为信号存储的整数值。最佳做法是使用相同的字长和符号指定输入和输出数据类型。这样做可确保模块仅更改信号的定标。为输入和输出指定不同的符号或字长可能会产生意外的结果，例如范围丢失或意外的符号扩展。

如果选择**存储的整数（SI）**，则模块不会对浮点输入信号执行较低级别的位重新解释。例如，如果输入为 `single` 且值为 `5`，则内存中存储该输入的位将通过下列命令以十六进制方式给出。

```
num2hex(single(5))
```

```dataframe
40a00000
```

但是，Type Conversion 模块不会将存储的整数值视为 `40a00000`，而是视为真实值 `5`。转换后，输出的存储的整数值为 `5`。


### 转换枚举信号

使用 TypeConversion 模块按如下所示转换枚举信号：

1. 将枚举类型的信号转换为任意数值类型的信号。

    TypeConversion 模块的所有枚举值输入的基础整数都必须在该数值类型的范围内。否则，仿真过程中将发生错误。

2. 将任意整数类型的信号转换为枚举类型的信号。

    TypeConversion 模块的值输入必须与枚举值的基础值匹配。否则，仿真过程中将发生错误。

您可以启用**对整数溢出进行饱和处理**参数，这样当模块的值输入与枚举值的基础值不匹配时。


在下列情况下，您不能使用 TypeConversion 模块：

- 将非整数数值信号转换为枚举信号。
- 将复信号转换为枚举信号，而不管复信号的实部和虚部的数据类型如何。


## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperation/TypeConversion.mo">TypeConversion.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/TypeConversion/TypeConversion01.png')" style="width: 600px; ">


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 向量 | 矩阵 | N 维数组</div></summary>
</details>
<div class="details-content">

输入信号，指定为标量、向量、矩阵或 N 维数组。输入可以是任何实数或复数值信号。如果输入为实数，则输出也是实数。如果输入为复数，则输出也是复数。该模块将输入信号转换为您指定的**输出数据类型**。

在转换定点数据类型时，使用**输入和输出具有相等的**参数确定是基于信号的真实值（RWV） 还是存储的整数（SI） 值进行转换。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | Boolean | fixed point | enumerated

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 向量 | 矩阵 | N 维数组</div></summary>
</details>
<div class="details-content">

输出信号，转换为您指定的数据类型，具有与输入信号相同的维度。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | Boolean | fixed point | enumerated

</div>
</div>



## 参数

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

<div class="details-box">
<details open>
<summary>输出数据类型 — 输出数据类型<div>Inherit: backPropagation (默认) | double | float | int8 | uint8 | int16 | uint16 | int32 | uint32 | boolean | fixdt(1,16,0)</div></summary>
</details>
<div class="details-content">

为输出选择数据类型。该类型可以继承、直接指定或表示为数据类型对象。

</div>
</div>


<!-- #### 编程用法

| **模块参数**：`输出数据类型`                               |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值**：`'Inherit: Inherit via back propagation'` | `'double'` | `'float'` | `'int8'` | `'uint8'` | `'int16'` | `'uint16'` | `'int32'` | `'uint32'` | `'fixdt(1,16,0)'` | `'Enum: <class name>'` | `'<data type expression>'` |
| **默认值：**`'Inherit: Inherit via back propagation'`  | -->

<!-- 暂无
### `锁定输出数据类型设置以防止被定点工具更改` — 防止定点工具覆盖输出数据类型 `off` （默认） | `on`



选择此参数可防止定点工具覆盖您在模块上指定的**输出**数据类型。有关详细信息，请参阅[Use Lock Output Data Type Setting](https://ww2.mathworks.cn/help/releases/R2022b/fixedpoint/ug/best-practices-for-using-the-fixed-point-tool-to-propose-data-types-for-your-simulink-model.html#br9an48) (Fixed-Point Designer)。

#### 编程用法

| **模块参数**：`LockScale` |
| ------------------------- |
| **类型：**字符向量        |
| **值：**`'off' | 'on'`    |
| **默认值：**`'off'`       |



### `输入和输出具有相等的` — 转换定点数据类型的约束 “`真实值(RWV)`” （默认） | “`存储的整数(SI)`”



在定点数据表示的上下文中，指定哪种类型的输入和输出必须相等。

- “`真实值(RWV)`” - 指定希望输入的“`真实值(RWV)`” 等于输出的“`真实值(RWV)`”。
- “`存储的整数(SI)`” - 指定希望输入的“`存储的整数(SI)`” 值等于输出的“`存储的整数(SI)`” 值。

#### 编程用法

| **模块参数**：`ConvertRealWorld`                           |
| ---------------------------------------------------------- |
| **类型：**字符向量                                         |
| **值：**`'Real World Value (RWV)' | 'Stored Integer (SI)'` |
| **默认值**：`'Real World Value (RWV)'`                     | -->



<!-- 暂无
### `整数舍入模式` — 指定定点运算的舍入模式 “`向下`” （默认） | “`向上`” | “`收敛`” | “`最邻近值`” | “`舍入`” | “`最简`” | “`零`”



选择下列舍入模式之一。

- “`向上`”

将正值和负值朝正无穷方向舍入。等同于 MATLAB® `ceil` 函数。

- “`收敛`”

将数值舍入到最邻近的可表示值。如果出现结值，则舍入到最邻近的偶数整数。等同于 Fixed-Point Designer™ `convergent` 函数。

- “`向下`”

将正值和负值朝负无穷方向舍入。等同于 MATLAB `floor` 函数。

- “`最邻近值`”

将数值舍入到最邻近的可表示值。如果出现结值，则朝正无穷方向舍入。等同于 Fixed-Point Designer `nearest` 函数。

- “`舍入`”

将数值舍入到最邻近的可表示值。如果出现结值，则将正数朝正无穷方向舍入，将负数朝负无穷方向舍入。等同于 Fixed-Point Designer `round` 函数。

- “`最简`”

自动选择是向负无穷大方向舍入还是向零舍入，以生成尽可能有效的舍入代码。

- “`零`”

将数值向零舍入。等同于 MATLAB `fix` 函数。



#### 编程用法

| **模块参数**：`RndMeth`                                      |
| ------------------------------------------------------------ |
| **类型**：字符向量                                           |
| **值**：`'Ceiling'` | `'Convergent'` | `'Floor'` | `'Nearest'` | `'Round'` | `'Simplest'` | `'Zero'` |
| **默认值**：`'Floor'`                                        |

#### 另请参阅

有关详细信息，请参阅[舍入](https://ww2.mathworks.cn/help/releases/R2022b/fixedpoint/ug/rounding.html) (Fixed-Point Designer)。 -->

<div class="details-box">
<details open>
<summary>对整数溢出进行饱和处理 — 溢出操作的方法<div>off （默认） | on</div></summary>
</details>
<div class="details-content">

指定对溢出是进行饱和处理还是绕回处理。

- off - 溢出将绕回到数据类型可以表示的合适值。

例如，数字 130 不适合一个有符号的 8 位整数，因此绕回 -126。

- on - 将溢出饱和处理为数据类型能够表示的最小值或最大值。

例如，一个有符号的 8 位整数的溢出可以饱和处理为 -128 或 127。


</div>
</div>








<!-- 
#### 编程用法

| **模块参数**：`SaturateOnIntegerOverflow` |
| ----------------------------------------- |
| **类型：**字符向量                        |
| **值：**`'off' | 'on'`                    |
| **默认值：**`'off'`                       | -->

<div class="details-box">
<details open>
<summary>采样时间 — -1 以外的采样时间值<div>-1 （默认） | 标量 | 向量</div></summary>
</details>
<div class="details-content">

将采样时间指定为 -1 以外的值。

#### 依存关系

此参数不可见，除非将其显式设置为 -1 以外的值。

</div>
</div>


<!-- 
#### 编程用法

| **模块参数：**`SampleTime`     |
| ------------------------------ |
| **类型：**字符串标量或字符向量 |
| **默认值：**`"-1"`             | -->


<!-- ## 模块特性 -->

<!-- 
| **数据类型**     | `Boolean` | `double` | `enumerated` | `fixed point` | `half` | `integer` | `single` |
| ---------------- | ------------------------------------------------------------ |
| **直接馈通**     | `是`                                                         |
| **多维信号**     | `是`                                                         |
| **可变大小信号** | `是`                                                         |
| **过零检测**     | `否`                                                         | -->

<!-- ## 扩展功能 -->


<!-- 
### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 Verilog 代码和 VHDL 代码。



### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。 -->

## 版本历史记录

- 在 2024b 之前推出

### 限制信息

不支持部分
1. 参数-输出最小值 — 范围检查的最小输出值
2. 参数-输出最大值 — 范围检查的最大输出值
3. 参数-锁定输出数据类型设置以防止被定点工具更改 — 用于防止定点工具覆盖输出数据类型的选项
4. 参数-输入和输出具有相等的 — 转换定点数据类型的约束
5. 参数-整数舍入模式 — 指定定点运算的舍入模式
6. 参数-数据类型覆盖 — 为此信号指定数据类型覆盖模式


<!-- ## 另请参阅

### 主题 -->


