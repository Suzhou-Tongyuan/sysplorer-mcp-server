# DotProduct
---
&nbsp;

生成两个向量的点积

- **库：** Sysblock / MathOperation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/DotProduct/DotProduct.png')" style="width: 100px; height: auto;">

## 描述

DotProduct 模块生成输入向量的点积。标量输出 `y` 等于 Sysblock 运算。

```
y = sum(conj(u1) .* u2 ) 
```

其中 `u1` 和 `u2` 表示输入向量。输入可以是向量、列向量（单列矩阵）或标量。如果两个输入都是向量或者都是列向量，它们的长度必须相同。如果 `u1` 和 `u2` 都是列向量，模块将输出 Sysblock 表达式 `u1'*u2` 的等效项。

<!-- 
输入向量的元素可以是实数值或复数值信号。输出的信号类型（复信号或实信号）取决于输入的信号类型。

| 输入 1 | 输入 2 | 输出   |
| :----- | :----- | :----- |
| 实信号 | 实数   | 实数   |
| 实数   | 复数   | 复数   |
| 复信号 | 实信号 | 复数   |
| 复数   | 复数   | 复信号 | -->

## 示例

生成两个向量的点积。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperation/DotProduct.mo">DotProduct.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/DotProduct/DotProduct01.png')" style="width: 600px; ">

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/DotProduct/DotProduct02.png')" style="width: 600px; ">

## 端口

### 输入


<div class="details-box">
<details open>
<summary>u1 — 第一个操作数输入信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

表示点积计算的第一个操作数的信号。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | fixed point

</div>
</div>

<div class="details-box">
<details open>
<summary>u2 — 第二个操作数输入信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

代表点积计算的第二个操作数的信号。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | fixed point

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>y — 点积输出信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

由两个输入信号的点积计算得到的输出信号。

**数据类型：** flaot | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | fixed point

</div>
</div>


## 参数


<!-- 暂无

### `要求所有输入具有相同的数据类型` — 要求所有输入具有相同的数据类型 `on` （默认） | `off`



清除此复选框可使各个输入具有不同数据类型。

#### 编程用法

| **模块参数**：`InputSameDT` |
| --------------------------- |
| **类型**：字符向量          |
| **值**：`'on'` | `'off'`    |
| **默认值**：`'on'`          | -->


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

<div class="details-box">
<details open>
<summary>输出数据类型 — 指定输出数据类型<div>Inherit: internalRule（默认） | Inherit: backPropagation | Inherit: sameAsFirstInput | double | float | int8 | uint8 | int16 | uint16 | int32 | uint32 | fixdt(1,16,0) | fixdt(1,16,2^0,0) | fixdt(1,16,1.0,0,0.0)</div></summary>
</details><div class="details-content">

为输出选择数据类型。该类型可以继承、直接指定或表示为数据类型对象。

当您选择继承的选项时，模块的行为如下所示：

- **Inherit: internalRule** - 在考虑嵌入式目标硬件的属性的同时，会选择相应的数据类型来平衡数值准确性、性能和生成的代码大小。如果更改了嵌入式目标的设置，则依内部规则选择的数据类型可能会发生变化。例如，如果该模块将 int8 类型的输入乘以 int16 的增益，并且将 ASIC/FPGA 指定为目标硬件类型，则输出数据类型为 sfix24。如果指定未指定(假定通用 32 位)（即通用 32 位微处理器）为目标硬件，则输出数据类型为 int32。


- **Inherit: backPropagation** - 使用驱动模块的数据类型。

- **Inherit: sameAsFirstInput** - 使用第一个输入信号的数据类型。


</div>
</div>




<!-- 
#### 编程用法

| **模块参数**：`OutDataTypeStr`                               |
| ------------------------------------------------------------ |
| **类型**：字符向量                                           |
| **值**：`'Inherit: Inherit via internal rule` | `'Inherit: Same as first input'` | `'Inherit: Inherit via back propagation'` | `'double'` | `'single'` | `'half'` | `'int8'` | `'uint8'` | `'int16'` | `'uint16'` | `'int32'` | `'uint32'` | `'int64'` | `'uint64'` | `'fixdt(1,16)'` | `'fixdt(1,16,0)'` | `'fixdt(1,16,2^0,0)'` | `'<data type expression>'` |
| **默认值**：`'Inherit: Inherit via internal rule'`           | -->


<!-- 暂无
### `锁定输出数据类型设置以防止被定点工具更改` — 防止定点工具覆盖数据类型 `off` （默认） | `on`



选中此选项将锁定此模块的输出数据类型设置，从而防止通过定点工具和定点顾问进行更改。有关详细信息，请参阅[Use Lock Output Data Type Setting](https://ww2.mathworks.cn/help/releases/R2022b/fixedpoint/ug/best-practices-for-using-the-fixed-point-tool-to-propose-data-types-for-your-simulink-model.html#br9an48) (Fixed-Point Designer)。

#### 编程用法

| **模块参数**：`LockScale` |
| ------------------------- |
| **类型**：字符向量        |
| **值**：`'off'` | `'on'`  |
| **默认值**：`'off'`       |
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
| **默认值：**`'Floor'`                                        | -->


<!-- 暂无
### `对整数溢出进行饱和处理` — 溢出操作的方法 `off` （默认） | `on`



指定对溢出是进行饱和处理还是绕回处理。

- `off` - 溢出将绕回到数据类型可以表示的合适值。

  例如，数字 130 不适合一个有符号的 8 位整数，因此绕回 -126。

- `on` - 将溢出饱和处理为数据类型能够表示的最小值或最大值。

  例如，一个有符号的 8 位整数的溢出可以饱和处理为 -128 或 127。



**提示**

- 如果您的模型存在可能的溢出，而您希望在生成的代码中进行显式饱和保护，请考虑选中此复选框。

- 如果您希望优化生成的代码的效率，请考虑清除此复选框。

  清除此复选框还可以帮助您避免过度地指定信号超出范围时的处理方式。有关详细信息，请参阅[信号范围错误故障排除](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/signal-ranges.html#brdiku9)。

- 如果选中此复选框，饱和将应用于模块中的每个内部操作，而不仅仅应用于输出或结果。

- 一般情况下，代码生成进程可以检测到何时不可能发生溢出。在这种情况下，代码生成器不会生成饱和代码。

#### 编程用法

| **模块参数**：`SaturateOnIntegerOverflow` |
| ----------------------------------------- |
| **类型：**字符向量                        |
| **值：**`'off' | 'on'`                    |
| **默认值：**`'off'`                       | -->



<!-- ## 模块特性 -->
<!-- 部分功能暂无
| **数据类型**     | `Boolean` \| `double` \| `fixed point` \| `integer` \| `float` |
| ---------------- | ------------------------------------------------------------ |
| **直接馈通**     | `是`                                                         |
| **多维信号**     | `是`                                                         |
| **可变大小信号** | `否`                                                         |
| **过零检测**     | `否`                                                         | -->

<!-- ## 扩展功能 -->


<!-- 
### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 Verilog 代码和 VHDL 代码。



HDL Coder™ 提供影响 HDL 实现和综合逻辑的额外配置选项。

**HDL 架构**

| 架构               | 描述                               |
| :----------------- | :--------------------------------- |
| “`线性`”（默认值） | 生成线性加法器链来计算乘积之和。   |
| “`树`”             | 生成加法器树形结构来计算乘积之和。 |

**HDL 模块属性**

| 通用                          |                                                              |
| :---------------------------- | ------------------------------------------------------------ |
| **InputPipeline**             | 要在生成的代码中插入的输入流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 `0`。有关详细信息，请参阅[InputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-25) (HDL Coder)。 |
| **OutputPipeline**            | 要在生成的代码中插入的输出流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 `0`。有关详细信息，请参阅[OutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-26) (HDL Coder)。 |
| **ConstrainedOutputPipeline** | 通过移动设计中现有延迟的方式来放置在输出端的寄存器的数量。分布式流水线处理不会重新分发这些寄存器。默认值为 `0`。有关详细信息，请参阅[ConstrainedOutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#btp8gmp) (HDL Coder)。 |

| 本机浮点                     |                                                              |
| :--------------------------- | ------------------------------------------------------------ |
| **HandleDenormals**          | 指定是否希望 HDL Coder 在设计中插入额外的逻辑来处理非正规数字。非规范数是量级非常小、必须使用包含前导零的尾数才能表示的浮点数。默认值为 “`inherit`”。另请参阅[HandleDenormals](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/hdl-block-properties-native-floating-point.html#mw_34395404-aeac-43da-bb3c-96c4a420c9e1) (HDL Coder)。 |
| **LatencyStrategy**          | 指定对于浮点运算符是否将设计中的模块映射到 `inherit`、`Max`、`Min` 或 `Zero`。默认值为 “`inherit`”。另请参阅[LatencyStrategy](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/hdl-block-properties-native-floating-point.html#mw_a99b0822-f2a6-4f5b-aca9-7f7251a67c7c) (HDL Coder)。 |
| **MantissaMultiplyStrategy** | 指定在代码生成期间如何实现尾数乘法运算。通过使用不同设置，您可以控制目标 FPGA 设备上 DSP 的使用。默认值为 “`inherit`”。另请参阅[MantissaMultiplyStrategy](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/hdl-block-properties-native-floating-point.html#mw_425f11cb-a3a5-45aa-a3aa-df5a7c765b5f) (HDL Coder)。 |



### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。 -->

## 版本历史记录

- 在 2024b 之前推出

### 限制信息
不支持部分
1. 参数-要求所有输入具有相同的数据类型 — 要求所有输入具有相同的数据类型
2. 参数-输出最小值 — 范围检查的最小输出值
3. 参数-输出最大值 — 范围检查的最大输出值
4. 参数-锁定输出数据类型设置以防止被定点工具更改 — 防止定点工具覆盖数据类型
5. 参数-整数舍入模式 — 定点运算的舍入模式
6. 参数-对整数溢出进行饱和处理 — 溢出操作的方法

## 另请参阅
[Product](Product.html)