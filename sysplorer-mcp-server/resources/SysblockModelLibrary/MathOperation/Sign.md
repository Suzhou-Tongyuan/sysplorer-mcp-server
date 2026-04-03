# Sign
---
&nbsp;

指示输入的符号

- **库：** Sysblock / MathOperation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/Sign/Sign.png')" style="width: 100px; height: auto;">


## 描述

### 实数输入的模块行为

对于实数输入，Sign 模块将输出输入的符号：

| 输入   | 输出 |
| :----- | :--- |
| 大于零 | 1    |
| 等于零 | 0    |
| 小于零 | -1   |



## 示例

对一个向量进行输入的符号指示。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperation/Sign.mo">Sign.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/Sign/Sign01.png')" style="width: 600px; ">



## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

输入信号，其符号将决定输出。

模块仅支持浮点数据类型（即 double 和 single）的复输入信号。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | Boolean | fixed point


</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

输出信号，它是输入信号的符号。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | Boolean

</div>
</div>


<!-- ## 参数 -->


<!-- 暂无
### `启用过零检测` — 启用过零检测 `on` （默认） | `off`



选择此项以启用过零检测。有关详细信息，请参阅[过零检测](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/zero-crossing-detection.html)。

#### 编程用法

| **模块参数**：`ZeroCross`    |
| ---------------------------- |
| **类型**：字符向量 \| 字符串 |
| **值**：`'off'` | `'on'`     |
| **默认值**：`'on'`           | -->


<!-- 
### 采样时间 — -1 以外的采样时间值 -1 （默认） | 标量 | 向量

将采样时间指定为 `-1` 以外的值。

#### 依存关系

此参数不可见，除非将其显式设置为 `-1` 以外的值。


#### 编程用法

| **模块参数：**`SampleTime`     |
| ------------------------------ |
| **类型：**字符串标量或字符向量 |
| **默认值：**`"-1"`             |  -->



<!-- ## 模块特性 -->

<!-- 部分特性暂无
| **数据类型**     | `Boolean` | `double` | `fixed point` | `integer` | `single` |
| ---------------- | ----------------------------------------------------------- |
| **直接馈通**     | `是`                                                        |
| **多维信号**     | `否`                                                        |
| **可变大小信号** | `否`                                                        |
| **过零检测**     | `是`                                                        | -->

<!-- ## 扩展功能 -->


<!-- 
### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 Verilog 代码和 VHDL 代码。

HDL Coder™ 提供影响 HDL 实现和综合逻辑的额外配置选项。



**HDL 架构**

此模块具有一个默认 HDL 架构。

**HDL 模块属性**

| **ConstrainedOutputPipeline** | 通过移动设计中现有延迟的方式来放置在输出端的寄存器的数量。分布式流水线处理不会重新分发这些寄存器。默认值为 `0`。有关详细信息，请参阅[ConstrainedOutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#btp8gmp) (HDL Coder)。 |
| ----------------------------- | ------------------------------------------------------------ |
| **InputPipeline**             | 要在生成的代码中插入的输入流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 `0`。有关详细信息，请参阅[InputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-25) (HDL Coder)。 |
| **OutputPipeline**            | 要在生成的代码中插入的输出流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 `0`。有关详细信息，请参阅[OutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-26) (HDL Coder)。 |

**复数数据支持**

此模块支持复信号的代码生成。



### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。 -->

## 版本历史记录

- 在 2024b 之前推出

### 限制信息
暂不支持

参数-采样时间 — -1 以外的采样时间值 -1

## 另请参阅

[Abs](Abs.html)