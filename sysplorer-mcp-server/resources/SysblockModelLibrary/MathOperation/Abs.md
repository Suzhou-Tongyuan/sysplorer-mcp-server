# Abs
---
&nbsp;

输出输入信号的绝对值

- **库:** Sysblock / MathOperation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/Abs/Abs.png')" style="width: 100px; height: auto;">

## 描述

Abs 模块输出输入信号的绝对值。

对于有符号整数数据类型，最小负值的绝对值无法用该数据类型表示。在这种情况下，由**对整数溢出进行饱和处理**复选框控制模块的行为。

| 如果您...      | 模块将...                          | 而且...                                                      |
| :------------- | :--------------------------------- | :----------------------------------------------------------- |
| 选中此复选框   | 饱和处理为该整数数据类型的最大正值 | 对于 8 位有符号整数，-128 对应为 127。对于 16 位有符号整数，-32768 对应为 32767。对于 32 位有符号整数，-2147483648 对应为 2147483647。 |
| 不选中此复选框 | 绕回到该整数数据类型的最小负值     | 对于 8 位有符号整数，-128 依然是 -128。对于 16 位有符号整数，-32768 依然是 -32768。对于 32 位有符号整数，-2147483648 依然是 -2147483648。 |

Abs 模块支持过零检测。但是，当您在对话框中选择**启用过零检测**时，该模块不会在定点工具中报告仿真最小值或最大值。如果您要使用定点工具来分析模型，请先对模型中的所有 Abs 模块禁用过零检测。

## 示例

对于一个正弦波的绝对值信号的输出。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperation/Abs.mo">Abs.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/Abs/Abs01.png')" style="width: 600px; ">
<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/Abs/Abs02.png')" style="width: 600px; ">


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

绝对值模块的输入信号。

**数据类型:** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | fixed point

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 绝对值输出信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

输入信号的绝对值。

**数据类型:** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | fixed point

</div>
</div>

## 参数

### 常设


<!-- 暂无
### **启用过零检测** — 启用过零检测 `on` (默认) | `off`

选择此项以启用过零检测。有关详细信息，请参阅[过零检测](https://ww2.mathworks.cn/help/simulink/ug/zero-crossing-detection.html)。

#### 编程用法

| **模块参数**：`ZeroCross`    |
| ---------------------------- |
| **类型**：字符向量 \| 字符串 |
| **值**：`'off'` | `'on'`     |
| **默认值**：`'on'`           | -->


<!-- 暂无
### **采样时间(-1 表示继承)** — 采样之间的时间间隔 `-1` (默认) | 标量 | 向量



指定采样时间间隔。要继承采样时间，请将此参数设置为 `-1`。有关详细信息，请参阅[指定采样时间](https://ww2.mathworks.cn/help/simulink/ug/how-to-specify-the-sample-time.html)。

#### 依存关系

仅当您将此参数设置为 `-1` 以外的值时才可见。要了解详细信息，请参阅[不建议设置采样时间的模块](https://ww2.mathworks.cn/help/simulink/ug/sampletimehiding.html)。

#### 编程用法

要以编程方式设置模块参数值，请使用 [`set_param`](https://ww2.mathworks.cn/help/simulink/slref/set_param.html) 函数。

| **参数:** | `SampleTime`                                |
| --------- | ------------------------------------------- |
| **值:**   | `"-1"` (默认) \| scalar or vector in quotes | -->

### 信号属性

<!-- 暂无
### **输出最小值** — 范围检查的最小输出值 `[]` (默认) | 标量



软件检查的输出范围的下限值。

软件使用最小值执行下列操作：

- 某些模块的参数范围检查（请参阅[指定模块参数的最小值和最大值](https://ww2.mathworks.cn/help/simulink/ug/checking-parameter-values.html)）。
- 仿真范围检查（请参阅[指定信号范围](https://ww2.mathworks.cn/help/simulink/ug/signal-ranges.html)和[启用仿真范围检查](https://ww2.mathworks.cn/help/simulink/ug/signal-ranges.html#brdikvq)）。
- 定点数据类型的自动定标。
- 从模型生成的代码的优化。此优化可删除算法代码，并影响某些仿真模式（如 SIL 或外部模式）的结果。有关详细信息，请参阅[Optimize using the specified minimum and maximum values](https://ww2.mathworks.cn/help/ecoder/ref/optimizeusingthespecifiedminimumandmaximumvalues.html) (Embedded Coder)。



#### 提示

**输出最小值**不会对实际输出信号进行饱和处理或截断。请改用 [Saturation](https://ww2.mathworks.cn/help/simulink/slref/saturation.html) 模块。

#### 编程用法

要以编程方式设置模块参数值，请使用 [`set_param`](https://ww2.mathworks.cn/help/simulink/slref/set_param.html) 函数。

| **参数:** | `OutMin`                          |
| --------- | --------------------------------- |
| **值:**   | `'[]'` (默认) \| scalar in quotes | -->


<!-- 暂无
### **输出最大值** — 范围检查的最大输出值 `[]` (默认) | 标量



软件检查的输出范围的上限值。

软件使用最大值执行下列操作：

- 某些模块的参数范围检查（请参阅[指定模块参数的最小值和最大值](https://ww2.mathworks.cn/help/simulink/ug/checking-parameter-values.html)）。
- 仿真范围检查（请参阅[指定信号范围](https://ww2.mathworks.cn/help/simulink/ug/signal-ranges.html)和[启用仿真范围检查](https://ww2.mathworks.cn/help/simulink/ug/signal-ranges.html#brdikvq)）。
- 定点数据类型的自动定标。
- 从模型生成的代码的优化。此优化可删除算法代码，并影响某些仿真模式（如 SIL 或外部模式）的结果。有关详细信息，请参阅[Optimize using the specified minimum and maximum values](https://ww2.mathworks.cn/help/ecoder/ref/optimizeusingthespecifiedminimumandmaximumvalues.html) (Embedded Coder)。



#### 提示

**输出最大值**不会对实际输出信号进行饱和处理或截断。请改用 [Saturation](https://ww2.mathworks.cn/help/simulink/slref/saturation.html) 模块。

#### 编程用法

要以编程方式设置模块参数值，请使用 [`set_param`](https://ww2.mathworks.cn/help/simulink/slref/set_param.html) 函数。

| **参数:** | `OutMax`                          |
| --------- | --------------------------------- |
| **值:**   | `'[]'` (默认) \| scalar in quotes | -->

<div class="details-box">
<details open>
<summary>输出数据类型 — 指定输出数据类型<div>Inherit: sameAsInput (默认) | Inherit: internalRule | Inherit: backPropagation | double | float | int8 | int32 | uint32 | fixdt(1,16,0) | fixdt(1,16,2^0,0) | fixdt(1,16,1.0,0,0.0)</div></summary>
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
| **值**：`'Inherit: Same as input'` | `'Inherit: Inherit via internal rule'` | `'Inherit: Inherit via back propagation'` | `'double'` | `'single'` | `'half'` | `'int8'` | `'uint8'` | `int16` | `'uint16'` | `'int32'` | `'uint32'` | `'int64'` | `'uint64'` | `fixdt(1,16,0)` | **fixdt(1,16,2^0,0)** | `fixdt(1,16,2^0,0)` | `'<data type expression>'` |
| **默认值**：`'Inherit: Same as input'`                       | -->


<!-- 暂无
### **锁定输出数据类型设置以防止被定点工具更改** — 用于防止定点工具覆盖输出数据类型的选项 `off` (默认) | `on`



选择此参数可防止定点工具覆盖您在模块上指定的**输出**数据类型。有关详细信息，请参阅[Use Lock Output Data Type Setting](https://ww2.mathworks.cn/help/fixedpoint/ug/best-practices-for-using-the-fixed-point-tool-to-propose-data-types-for-your-simulink-model.html#br9an48) (Fixed-Point Designer)。

#### 编程用法

要以编程方式设置模块参数值，请使用 [`set_param`](https://ww2.mathworks.cn/help/simulink/slref/set_param.html) 函数。

| **参数:** | `LockScale`             |
| --------- | ----------------------- |
| **值:**   | `'off'` (默认) | `'on'` | -->


<!-- 暂无
### **整数舍入模式** — 定点运算的舍入模式 **向下** (默认) | **向上** | **收敛** | **最邻近值** | **舍入** | **最简** | **零**



指定定点运算的舍入模式。有关详细信息，请参阅[舍入](https://ww2.mathworks.cn/help/fixedpoint/ug/rounding.html) (Fixed-Point Designer)。

模块参数始终舍入到最邻近的可表示值。要控制模块参数的舍入方法，请在封装字段中使用 MATLAB® 舍入函数输入表达式。

#### 编程用法

要以编程方式设置模块参数值，请使用 [`set_param`](https://ww2.mathworks.cn/help/simulink/slref/set_param.html) 函数。

| **参数:** | `RndMeth`                                                    |
| --------- | ------------------------------------------------------------ |
| **值:**   | `'Floor'` (默认) | `'Ceiling'` | `'Convergent'` | `'Nearest'` | `'Round'` | `'Simplest'` | `'Zero'` | -->

<div id="对整数溢出进行饱和处理—选择发生整数溢出时的行为" class="jump-target"></div>
<div class="details-box">
<details open>
<summary>对整数溢出进行饱和处理 — 选择发生整数溢出时的行为<div>off (默认) | on</div></summary>
</details>
<div class="details-content">

如果选中此复选框，饱和将应用于模块中的每个内部操作，而不仅仅应用于输出或结果。一般情况下，代码生成进程可以检测到何时不可能发生溢出。在这种情况下，代码生成器不会生成饱和代码。

| 操作             | 执行此操作的原因                                             | 发生的情况                                 | 示例                                                     |
| :--------------- | :----------------------------------------------------------- | :----------------------------------------- | :------------------------------------------------------- |
| 选中此复选框。   | 您的模型可能有溢出，并且您希望在生成的代码中具有显式饱和保护。 | 溢出将饱和处理为数据类型可以表示的最大值。 | 数字 130 不适合一个有符号 8 位整数，因此饱和处理为 127。 |
| 不选中此复选框。 | 您需要优化所生成代码的效率。                                 | 溢出会绕回到由数据类型表示的适当值。       | 数字 130 不适合一个有符号 8 位整数，因此绕回 -126。      |

</div>
</div>





<!-- 
#### 编程用法

| **模块参数**：`SaturateOnIntegerOverflow` |
| ----------------------------------------- |
| **类型**：字符向量                        |
| **值**：`'off'` | `'on'`                  |
| **默认值**：`'off'`                       | -->

<!-- ## 模块特性 -->

<!-- 部分功能暂无
| **数据类型**     | `double` \| `fixed point` \| `half` \| `integer` \| `float` |
| ---------------- | -------------------------------------------------------- |
| **直接馈通**     | `是`                                                     |
| **多维信号**     | `是`                                                     |
| **可变大小信号** | `是`                                                     |
| **过零检测**     | `是`                                                     | -->

<!-- ## 详细信息 -->
<!-- 

### 模型覆盖率

如果您有 Simulink® Coverage™ 许可证，则 Abs 模块会接收决策覆盖率和关系边界覆盖率。决策覆盖率基于：

- 模块的输入是否小于零
- 输入信号的数据类型



当模块的输入小于零时，决策覆盖率测量：

- 模块输入小于零的时间步数，这表示 true 决策
- 模块输入不小于零的时间步数，这表示 false 决策



如果您在“配置参数”对话框的**覆盖率**窗格中选择**对整数溢出进行饱和处理**参数，则 Abs 模块会接收对整数溢出进行饱和处理覆盖率。有关详细信息，请参阅[整数溢出覆盖率](https://ww2.mathworks.cn/help/slcoverage/ug/types-of-model-coverage.html#bs9e8_v-1) (Simulink Coverage)。

如果 Abs 模块的输入数据类型是无符号整数，则 Simulink Coverage 不会报告该模块的决策覆盖率。Simulink 设置模块输出等于模块输入，而不进行决策。

由于 Abs 将输入与零进行比较，因此如果您选择**关系边界**覆盖率度量，则 Abs 模块会接收关系边界覆盖率。有关详细信息，请参阅[关系边界覆盖率](https://ww2.mathworks.cn/help/slcoverage/ug/types-of-model-coverage.html#buei_i5) (Simulink Coverage)。 -->

<!-- ## 扩展功能 -->


<!-- 
### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 VHDL、Verilog 和 SystemVerilog 代码。



HDL Coder™ 提供影响 HDL 实现和综合逻辑的额外配置选项。

**HDL 架构**

此模块具有一个默认 HDL 架构。

**HDL 模块属性**

| 通用                          |                                                              |
| :---------------------------- | ------------------------------------------------------------ |
| **ConstrainedOutputPipeline** | 通过移动设计中现有延迟的方式来放置在输出端的寄存器的数量。分布式流水线不会重新分发这些寄存器。默认值为 `0`。有关详细信息，请参阅[ConstrainedOutputPipeline](https://ww2.mathworks.cn/help/hdlcoder/ug/block-implementation-parameters.html#btp8gmp) (HDL Coder)。 |
| **InputPipeline**             | 要在生成的代码中插入的输入流水线阶段数。分布式流水线和受限输出流水线可以移动这些寄存器。默认值为 `0`。有关详细信息，请参阅[InputPipeline](https://ww2.mathworks.cn/help/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-25) (HDL Coder)。 |
| **OutputPipeline**            | 要在生成的代码中插入的输出流水线阶段数。分布式流水线和受限输出流水线可以移动这些寄存器。默认值为 `0`。有关详细信息，请参阅[OutputPipeline](https://ww2.mathworks.cn/help/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-26) (HDL Coder)。 |

| 原生浮点            |                                                              |
| :------------------ | ------------------------------------------------------------ |
| **LatencyStrategy** | 指定对于浮点运算符是否将设计中的模块映射到 `inherit`、`Max`、`Min` 或 `Zero`。默认值为 **inherit**。另请参阅[LatencyStrategy](https://ww2.mathworks.cn/help/hdlcoder/ug/hdl-block-properties-native-floating-point.html#mw_a99b0822-f2a6-4f5b-aca9-7f7251a67c7c) (HDL Coder)。 |

**复数数据支持**

此模块支持在 `Native Floating Point` 模式下浮点类型的复信号的代码生成。

不支持使用定点类型的复信号的模块的代码生成。要计算复数的模，请改用 [Complex to Magnitude-Angle](https://ww2.mathworks.cn/help/dsphdl/ref/complextomagnitudeangle.html) (DSP HDL Toolbox) 模块。



### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。 -->

## 版本历史记录

- 在 2024b 之前推出


### 限制信息

1. 参数-常设-启用过零检测 — 启用过零检测
2. 参数-常设-采样时间 — -1 以外的采样时间值
3. 参数-信号属性-输出最小值 — 范围检查的最小输出值
4. 参数-信号属性-输出最大值 — 范围检查的最大输出值
5. 参数-信号属性-锁定输出数据类型设置以防止被定点工具更改 — 防止定点工具覆盖输出数据类型
6. 参数-信号属性-整数舍入模式 — 定点运算的舍入模式


## 另请参阅

[Sign](Sign.html) | [Sum](Sum.html)