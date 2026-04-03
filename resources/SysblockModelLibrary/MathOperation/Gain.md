# Gain
---
&nbsp;

将输入乘以常量

- **库：** Sysblock / MathOperation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/Gain/Gain.png')" style="width: 100px; height: auto;">

## 描述

Gain 模块将输入乘以一个常量值（增益），输入和增益可以是标量、向量或矩阵。

在**增益**参数中指定增益的值，**乘法**参数用于指定按元素还是矩阵乘法。对于矩阵乘法，此参数还用于指示被乘数的阶。

通过舍入到最接近的值和饱和操作将增益从双精度型离线转换为模块封装中指定的数据类型，然后将输入和增益相乘，结果通过指定的舍入和溢出模式转换为输出数据类型。


## 示例

将一个正弦波增益 2 倍，选择一个 SineWave 模块将其输出连接 Gain 模块的输入，将 Gain 的值设置为 2。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperation/Gain.mo">Gain.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/Gain/Gain01.png')" style="width: 600px; ">

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/Gain/Gain02.png')" style="width: 600px; ">


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

Gain 模块接受实数或复数值标量、向量或矩阵输入。Gain 模块支持定点数据类型。如果 Gain 模块的输入为实数，增益为复数，则输出为复数。

**数据类型：**  float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | Boolean | fixed point

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>y — 输入乘以增益<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

Gain 模块的输出是输入乘以常量增益值，当 Gain 模块的输入为实数且增益为复数时，输出为复数。

**数据类型：**  float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | Boolean | fixed point

</div>
</div>

## 参数


### 常设

<div class="details-box">
<details open>
<summary>增益 — 要与输入相乘的值<div>1（默认） | 标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

指定要与输入相乘的值。增益可以是实数或标量、向量或矩阵。

</div>
</div>


<!-- #### 编程用法

| **模块参数**：`Gain`                                         |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值：**`'1' | real- or complex-valued scalar, vector, or matrix` |
| **默认值：**`'1'`                                            | -->


<div class="details-box">
<details open>
<summary>乘法 — 指定乘法模式<div>按元素(K.*u)（默认） | 矩阵(K*u) | 矩阵(u*K) | 矩阵(K*u) (u 向量)</div></summary>
</details>
<div class="details-content">

指定下列乘法模式之一：

- **按元素 (K.\*u)** - 输入的每个元素乘以增益的每个元素。如有必要，该模块会执行扩展，以使输入和增益具有相同的维度。

- **矩阵 (K*u)** - 输入和增益按矩阵乘法方式相乘，其中输入为第二个操作数。

- **矩阵 (u*K)** - 输入和增益按矩阵乘法方式相乘，其中输入为第一个操作数。

- **矩阵 (K*u) (u 向量)** - 输入和增益按矩阵乘法方式相乘，其中输入为第二个操作数。除了确定维度的方式，此模式与 **Matrix(K*u)** 相同。

  假设 K 是一个 m-by-n 矩阵。**Matrix(K*u)(u vector)** 将输入设置为长度为 n 的向量，将输出设置为长度为 m 的向量。相比之下，Matrix(K*u) 则是使用传播来确定输入和输出的维度。对于 m-by-n 增益矩阵，输入可以传播到 n-by-q 矩阵，并且输出变为 m-by-q 矩阵。

</div>
</div>



<!-- 
#### 编程用法

| **参数：**`Multiplication`                                   |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值：**`'Element-wise(K.*u)' | 'Matrix(K*u)' | 'Matrix(u*K)' | 'Matrix(K*u) (u vector)'` |
| **默认值：**`'Element-wise(K.*u)'`                           | -->


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
| **默认值**：`'[ ]'`    | -->

<div class="details-box">
<details open>
<summary>输出数据类型 — 指定输出数据类型<div>Inherit: internalRule（默认） | Inherit: sameAsInput | Inherit: inheritFromGain | double | Inherit: Same as input | double | float | int8 | uint8 | int16 | uint16 | int32 | fixdt(1,16,0) | fixdt(1,16,2^0,0) | fixdt(1,16,1.0,0,0.0)</div></summary>
</details>
<div class="details-content">

为输出选择数据类型。该类型可以继承、直接指定或表示为数据类型对象。

::: tip 提示
要获得更高效的生成代码，请取消选择**对整数溢出进行饱和处理**参数。
此规则从不产生溢出。
:::


</div>
</div>


<!-- 
当您选择继承的选项时，模块的行为如下所示：

- “`Inherit: Inherit via internal rule`” - Simulink 在考虑嵌入式目标硬件的属性的同时，会选择相应的数据类型来平衡数值准确性、性能和生成的代码大小。如果更改了嵌入式目标的设置，则依内部规则选择的数据类型可能会发生变化。例如，如果该模块将 `int8` 类型的输入乘以 `int16` 的增益，并且将 “`ASIC/FPGA`” 指定为目标硬件类型，则输出数据类型为 `sfix24`。如果指定“`未指定(假定通用 32 位)`”（即通用 32 位微处理器）为目标硬件，则输出数据类型为 `int32`。如果目标微处理器不能提供适应输出范围的字长，Simulink 软件将在诊断查看器中显示错误。

- “`Inherit: Keep MSB`” - Simulink 选择一种能够保持运算的完整范围的数据类型，然后将输出精度降低到适合嵌入式目标硬件的大小。 -->


<!-- 
- “`Inherit: Match scaling`” - Simulink 选择一种数据类型，其定标与输入类型的定标相匹配。如果该类型的完整范围不适合嵌入式目标硬件，则该范围会缩小，从而生成适合嵌入式目标硬件的类型。此规则可能产生溢出。

有时软件不能同时满足优化代码效率和保证数值准确性这两个需求。如果这些内部规则不能满足您对数值准确性或性能的特定需求，请使用下列选项之一：

- 显式指定输出数据类型。
- 使用简单的选项 “`Inherit: Same as input`”。
- 显式指定默认数据类型（例如 `fixdt(1,32,16)`），然后使用定点工具为您的模型提供数据类型建议。有关详细信息，请参阅 [`fxptdlg`](https://ww2.mathworks.cn/help/releases/R2022b/fixedpoint/ref/fxptdlg.html) (Fixed-Point Designer)。
- 要指定您自己的继承规则，请使用 “`Inherit: Inherit via back propagation`”，然后使用 [Data Type Propagation](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/datatypepropagation.html) 模块。有关如何使用此模块的示例说明，请参阅 Signal Attributes 模块库中的 Data Type Propagation Examples 模块。 -->



<!-- 
#### 编程用法

| **模块参数**：`OutDataTypeStr`                               |
| ------------------------------------------------------------ |
| **类型**：字符向量                                           |
| **值**：`'Inherit: Inherit via internal rule'` | `'Inherit: Keep MSB'` | `'Inherit: Match scaling'` | `'Inherit: Same as input'` | `'Inherit: Inherit via back propagation'` | `'single'` | `'half'` | `'int8'` | `'uint8'` | `'int16'` | `'uint16'` | `'int32'` | `'uint32'` | `'int64'` | `'uint64'` | `'fixdt(1,16)'` | `'fixdt(1,16,0)'` | `'fixdt(1,16,2^0,0)'` | `'<data type expression>'` |
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

模块参数始终舍入到最接近的可表示值。要控制模块参数的舍入方法，请在封装字段中使用 MATLAB® 舍入函数输入表达式。

#### 编程用法

| **模块参数**：`RndMeth`                                      |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值：**`'Ceiling' | 'Convergent' | 'Floor' | 'Nearest' | 'Round' | 'Simplest' | 'Zero'` |
| **默认值：**`'Floor'`                                        |
 -->

<!-- 暂无
### `对整数溢出进行饱和处理` — 溢出操作的方法 `off` （默认） | `on`



指定对溢出是进行饱和处理还是绕回处理。

| 操作                     | 原理说明                                                     | 对溢出的影响                                       | 示例                                                         |
| :----------------------- | :----------------------------------------------------------- | :------------------------------------------------- | :----------------------------------------------------------- |
| 选中此复选框 (`on`)。    | 您的模型可能有溢出，并且您希望在生成的代码中具有显式饱和保护。 | 将溢出饱和处理为数据类型能够表示的最小值或最大值。 | `int8`（有符号 8 位整数）数据类型可以表示的最大值为 127。任何大于此最大值的模块运算结果都会导致 8 位整数溢出。如果选中此复选框，模块输出将在达到 127 时饱和。类似地，模块输出将在达到最小输出值 -128 时饱和。 |
| 不选中此复选框 (`off`)。 | 您需要优化所生成代码的效率。您希望避免过度地指定信号超出范围时的处理方式。有关详细信息，请参阅[信号范围错误故障排除](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/signal-ranges.html#brdiku9)。 | 溢出会绕回到由数据类型表示的适当值。               | `int8`（有符号 8 位整数）数据类型可以表示的最大值为 127。任何大于此最大值的模块运算结果都会导致 8 位整数溢出。清除该复选框时，软件会将导致溢出的值解释为 `int8`，这可能产生意外结果。例如，以 `int8` 表示的模块结果 130（二进制 1000 0010）为 -126。 |



如果选中此复选框，饱和将应用于模块中的每个内部操作，而不仅仅应用于输出或结果。通常，代码生成过程可以检测何时不会发生溢出。在这种情况下，代码生成器不会生成饱和代码。

#### 编程用法

| **模块参数**：`SaturateOnIntegerOverflow` |
| ----------------------------------------- |
| **类型：**字符向量                        |
| **值：**`'off' | 'on'`                    |
| **默认值：**`'off'`                       | -->

<!-- ### 参数属性 -->

<!-- 暂无

### `参数最小值` — 指定增益的最小值 `[]` （默认） | 标量



指定增益的最小值。默认值为 `[]`（未指定）。Simulink 使用此值来执行：

- 参数范围检查（请参阅[指定模块参数的最小值和最大值](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/checking-parameter-values.html)）
- 定点数据类型的自动定标



#### 编程用法

| **模块参数**：`ParamMin` |
| ------------------------ |
| **类型**：字符向量       |
| **值**：标量             |
| **默认值**：`'[ ]'`      |
 -->

<!-- 暂无
### `参数最大值` — 指定增益的最大值 `[]` （默认） | 标量



指定增益的最大值。默认值为 `[]`（未指定）。Simulink 使用此值来执行：

- 参数范围检查（请参阅[指定模块参数的最小值和最大值](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/checking-parameter-values.html)）
- 定点数据类型的自动定标

#### 编程用法

| **模块参数**：`ParamMax` |
| ------------------------ |
| **类型**：字符向量       |
| **值**：标量             |
| **默认值**：`'[ ]'`      | -->


<!--暂无
### `参数数据类型` — 指定 Gain 参数的数据类型 `Inherit: internalRule` （默认） | `Inherit: sameAsInput` | `Inherit: inheritFromGain` | “`double`” | “`float`” | “`half`” | “`int8`” | “`uint8`” | “`int16`” | “`uint16`” | “`int32`” | “`uint32`” | “`fixdt(1,16,0)`” | “`fixdt(1,16,2^0,0)`” | “`fixdt(1,16,1.0,0,0.0)`” | “`<data type expression>`”



指定**增益**参数的数据类型。

#### 当参数数据类型设置为“`通过内部规则继承`”时调节增益参数值

将**参数数据类型**设置为“`继承:通过内部规则继承`”允许 Gain 模块基于内部启发式方法选择数据类型，该算法查看当前增益值，并提供全精度数据类型来表示当前增益值。

 
当您更新图时，Simulink 会推断出一种适用于增益值 `3` 的高精度且无范围损失的数据类型。例如，使用这种启发式方法，如果指定的增益值是 `3`，则 Gain 模块推断出 `sfix32_En29` 的所选数据类型。因此，这种推断出的数据类型无法保留大于 `4` 的值。在仿真期间，如果将增益值调节为 `6`，则所选数据类型中会发生溢出，并且该行为是非预期行为。 -->


<!-- 
#### 编程用法

| **模块参数**：` ParamDataTypeStr`                            |
| ------------------------------------------------------------ |
| **类型**：字符向量                                           |
| **值**：`'Inherit: Inherit via internal rule` | `'Inherit: Same as input'` | `'Inherit: Inherit via back propagation'` | `'single'` | `'half'` | `'int8'` | `'uint8'` | `'int16'` | `'uint16'`, `'int32'` | `'uint32'` | `'int64'` | `'uint64'` | `'fixdt(1,16)'` | `'fixdt(1,16,0)'` | `'fixdt(1,16,2^0,0)'` | `'<data type expression>'` |
| **默认值**：`'Inherit: Inherit via internal rule'`           | -->


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



### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。 -->

## 版本历史记录

- 在 2024b 之前推出

### 限制信息

不支持部分
1. 参数-信号属性-输出最小值 — 范围检查的最小输出值
2. 参数-信号属性-输出最大值 — 范围检查的最大输出值
3. 参数-信号属性-锁定输出数据类型设置以防止被定点工具更改 — 防止定点工具覆盖输出数据类型
4. 参数-信号属性-整数舍入模式 — 定点运算的舍入模式
5. 参数-信号属性-对整数溢出进行饱和处理 — 溢出操作的方法
6. 参数-参数属性-参数最小值 — 指定增益的最小值
7. 参数-参数属性-参数最大值 — 指定增益的最大值
8. 参数-参数属性-参数数据类型 — 指定 Gain 参数的数据类型



## 另请参阅

[Product](Product.html)

