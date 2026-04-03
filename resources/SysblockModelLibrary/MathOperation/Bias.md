# Bias
---
&nbsp;

为输入添加偏差


- **库：** Sysblock / MathOperation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/Bias/Bias.png')" style="width: 100px; height: auto;">

## 描述

Bias 模块根据以下公式为输入信号添加偏差或偏移量：

Y = U + bias

其中 U 是模块输入，Y 是输出。

## 示例

将一个正弦波添加 +3 偏差。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperation/Bias.mo">Bias.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/Bias/Bias01.png')" style="width: 600px; ">

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/Bias/Bias02.png')" style="width: 600px; ">


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

输入信号，向该输入信号添加偏差以创建输出信号。

**数据类型:**  float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | fixed point

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

输出信号是将偏差添加到输入信号而产生的。

**数据类型:** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | fixed point

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>偏置 — 要添加到输入信号的偏移量<div>0 (默认) | 标量 | 向量</div></summary>
</details>
<div class="details-content">

指定要添加到输入信号的偏移量的值。

</div>
</div>

<!-- 
#### 编程用法

| **模块参数**：`Bias` |
| -------------------- |
| **类型：**字符向量   |
| **值：**有限实数     |
| **默认值：**`'0'`  | -->


<!-- 暂无
### **对整数溢出进行饱和处理** — 溢出操作的方法 `off` (默认) | `on`



指定对溢出是进行饱和处理还是绕回处理。

- `on` - 将溢出饱和处理为数据类型能够表示的最小值或最大值。
- `off` - 溢出将绕回到数据类型可以表示的合适值。

例如，有符号 8 位整数 `int8` 可以表示的最大值是 127。任何大于此最大值的模块运算结果都会导致 8 位整数溢出。

- 选择此参数后，模块输出将在达到 127 时饱和。类似地，模块输出将在达到最小输出值 -128 时饱和。
- 清除此参数后，软件会将导致溢出的值解释为 `int8`，这可能产生意外结果。例如，以 `int8` 表示的模块结果 130（二进制 1000 0010）为 -126。



#### 提示

- 如果您的模型存在可能的溢出，而您希望在生成的代码中进行显式饱和保护，请考虑选中此参数。
- 如果您希望优化生成的代码的效率，请考虑清除此参数。清除此参数还可以帮助您避免过度地指定信号超出范围时模块的处理方式。有关详细信息，请参阅[信号范围错误故障排除](https://ww2.mathworks.cn/help/simulink/ug/signal-ranges.html#brdiku9)。
- 如果选中此参数，饱和将应用于模块中的每个内部操作，而不仅仅应用于输出或结果。
- 一般情况下，代码生成进程可以检测到何时不可能发生溢出。在这种情况下，代码生成器不会生成饱和代码。

#### 编程用法

要以编程方式设置模块参数值，请使用 [`set_param`](https://ww2.mathworks.cn/help/simulink/slref/set_param.html) 函数。

| **参数:** | `SaturateOnIntegerOverflow` |
| --------- | --------------------------- |
| **值:**   | `'off'` (默认) | `'on'`     | -->

<!-- ## 模块特性 -->
<!-- 部分特性暂无
| **数据类型**     | `double` \| `fixed point` \| `half` \| `integer` \| `single` |
| ---------------- | -------------------------------------------------------- |
| **直接馈通**     | `是`                                                     |
| **多维信号**     | `否`                                                     |
| **可变大小信号** | `是`                                                     |
| **过零检测**     | `否`                                                     | -->


<!-- ## 扩展功能 -->

<!-- 

### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 VHDL、Verilog 和 SystemVerilog 代码。



HDL Coder™ 提供影响 HDL 实现和综合逻辑的额外配置选项。

**HDL 架构**

此模块具有一个默认 HDL 架构。

**HDL 模块属性**

| **ConstrainedOutputPipeline** | 通过移动设计中现有延迟的方式来放置在输出端的寄存器的数量。分布式流水线不会重新分发这些寄存器。默认值为 `0`。有关详细信息，请参阅[ConstrainedOutputPipeline](https://ww2.mathworks.cn/help/hdlcoder/ug/block-implementation-parameters.html#btp8gmp) (HDL Coder)。 |
| ----------------------------- | ------------------------------------------------------------ |
| **InputPipeline**             | 要在生成的代码中插入的输入流水线阶段数。分布式流水线和受限输出流水线可以移动这些寄存器。默认值为 `0`。有关详细信息，请参阅[InputPipeline](https://ww2.mathworks.cn/help/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-25) (HDL Coder)。 |
| **OutputPipeline**            | 要在生成的代码中插入的输出流水线阶段数。分布式流水线和受限输出流水线可以移动这些寄存器。默认值为 `0`。有关详细信息，请参阅[OutputPipeline](https://ww2.mathworks.cn/help/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-26) (HDL Coder)。 |



### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。 -->

## 版本历史记录

- 在 2024b 之前推出

### 限制信息

参数-对整数溢出进行饱和处理 — 溢出操作的方法

## 另请参阅
[Gain](Gain.html)