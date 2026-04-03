# RoundingFunction
---
&nbsp;


对信号应用舍入函数

- **库：** Sysblock / MathOperation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/RoundingFunction/RoundingFunction.png')" style="width: 100px; height: auto;">


## 描述

RoundingFunction 模块对输入信号的每个元素进行舍入以产生输出信号。

您可以从**函数**参数列表中选择舍入类型。所选函数的名称显示在模块上。


::: tip 提示
当您需要向量或矩阵输出时，请使用 RoundingFunction 模块。
:::

## 示例

对 3.1415 进行舍入操作，将 Constant 模块的值设置成 3.1415，RoundingFunction 模块函数选择 floor。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperation/RoundingFunction.mo">RoundingFunction.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/RoundingFunction/RoundingFunction01.png')" style="width: 600px; ">

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/RoundingFunction/RoundingFunction02.png')" style="width: 600px; ">

## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

要应用舍入函数的输入信号。

**数据类型：** float | double

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

对输入信号应用舍入函数后的输出信号，输出信号与输入信号具有相同的维度和数据类型，输出信号的每个元素是对输入信号的对应元素应用所选舍入函数后的结果。

**数据类型：** float | double

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>函数 — 舍入函数<div>向下 （默认） | 上半框括号 | 舍入 | fix</div></summary>
</details>
<div class="details-content">

选择应用于输入信号的舍入函数。

| 函数名&#xA;   | 中文名&#xA;  | 功能说明&#xA;           | 示例：输入 +2.7&#xA; | 示例：输入 -2.7&#xA; |
| ---------- | --------- | ------------------- | --------------- | --------------- |
| floor&#xA; | 向下取整&#xA; | 取不大于输入值的最大整数&#xA;   | 2&#xA;          | -3&#xA;         |
| ceil&#xA;  | 向上取整&#xA; | 取不小于输入值的最小整数&#xA;   | 3&#xA;          | -2&#xA;         |
| round&#xA; | 四舍五入&#xA; | 四舍五入到最接近的整数&#xA;    | 3&#xA;          | -3&#xA;         |
| fix&#xA;   | 截断取整&#xA; | 向零方向取整（去除小数部分）&#xA; | 2&#xA;          | -2&#xA;         |

</div>
</div>





<!-- 
#### 编程用法

| **模块参数**：`Operator`                           |
| -------------------------------------------------- |
| **类型**：字符向量                                 |
| **值**：`'floor'` | `'ceil'` | `'round'` | `'fix'` |
| **默认值**：`'floor'`                              | -->


<!-- 暂无
### 采样时间 — -1 以外的采样时间值 -1 （默认） | 标量 | 向量

将采样时间指定为 `-1` 以外的值。

#### 依存关系

此参数不可见，除非将其显式设置为 `-1` 以外的值。


#### 编程用法

| **模块参数：**`SampleTime`     |
| ------------------------------ |
| **类型：**字符串标量或字符向量 |
| **默认值：**`"-1"`             | -->

<!-- ## 模块特性 -->

<!--部分特性暂无 
| **数据类型**     | `double` | `single` |
| ---------------- | ------------------- |
| **直接馈通**     | `是`                |
| **多维信号**     | `否`                |
| **可变大小信号** | `是`                |
| **过零检测**     | `否`                | -->

<!-- ## 扩展功能 -->
<!-- 


### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 Verilog 代码和 VHDL 代码。



HDL Coder™ 提供影响 HDL 实现和综合逻辑的额外配置选项。

**HDL 代码生成要求**

模块的 HDL 代码生成要求您使用单精度数据类型作为模块的输入，并启用本机浮点模式。在“配置参数”对话框的 **HDL 代码生成** > **浮点**窗格上，对于**库**，选择“`本机浮点`”。要了解有关使用本机浮点模式的详细信息，请参阅[Getting Started with HDL Coder Native Floating-Point Support](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/native-floating-point-support.html) (HDL Coder) 和[Generate Target-Independent HDL Code with Native Floating-Point](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/generate-target-independent-hdl-code-with-native-floating-point-libraries.html) (HDL Coder)。

**HDL 架构**

此模块具有一个默认 HDL 架构。

**HDL 模块属性**

| 通用                          |                                                              |
| :---------------------------- | ------------------------------------------------------------ |
| **ConstrainedOutputPipeline** | 通过移动设计中现有延迟的方式来放置在输出端的寄存器的数量。分布式流水线处理不会重新分发这些寄存器。默认值为 `0`。有关详细信息，请参阅[ConstrainedOutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#btp8gmp) (HDL Coder)。 |
| **InputPipeline**             | 要在生成的代码中插入的输入流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 `0`。有关详细信息，请参阅[InputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-25) (HDL Coder)。 |
| **OutputPipeline**            | 要在生成的代码中插入的输出流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 `0`。有关详细信息，请参阅[OutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-26) (HDL Coder)。 |

| 本机浮点             |                                                              |
| :------------------- | ------------------------------------------------------------ |
| **LatencyStrategy**  | 指定对于浮点运算符是否将设计中的模块映射到 `inherit`、`Max`、`Min`、`Zero` 或 `Custom`。默认值为 “`inherit`”。另请参阅[LatencyStrategy](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/hdl-block-properties-native-floating-point.html#mw_a99b0822-f2a6-4f5b-aca9-7f7251a67c7c) (HDL Coder)。 |
| **NFPCustomLatency** | 要指定值，请将 **LatencyStrategy** 设置为 `Custom`。HDL Coder 会增加延迟，其值等于您为 **NFPCustomLatency** 设置指定的值。另请参阅[NFPCustomLatency](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/hdl-block-properties-native-floating-point.html#mw_e29db696-7117-431a-a8b8-4471b8d24ea8) (HDL Coder)。 |

**复数数据支持**

此模块支持复信号的代码生成。



### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。 -->

## 版本历史记录

- 在 2024b 之前推出

### 限制信息

参数-采样时间 — -1 以外的采样时间值 -1