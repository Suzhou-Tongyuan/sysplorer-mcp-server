# UnaryMinus
---
&nbsp;

对输入求反

- **库：** Sysblock / MathOperation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/UnaryMinus/UnaryMinus.png')" style="width: 100px; height: auto;">

## 描述

UnaryMinus 模块对输入进行求反。

## 示例

对于一个信号源为 5 的求反输出。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperation/UnaryMinus.mo">UnaryMinus.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/UnaryMinus/UnaryMinus01.png')" style="width: 600px; ">

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/UnaryMinus/UnaryMinus02.png')" style="width: 600px; ">


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 要求反的信号<div>标量 | 向量 | 矩阵 | N 维数组</div></summary>
</details>
<div class="details-content">

输入信号，指定为标量、向量、矩阵或 N 维数组。

**数据类型：** float | double | int8 | int16 | int32 | fixed point

</div>
</div>

<div class="details-box">
<details open>
<summary>u — 要求反的信号<div>标量 | 向量 | 矩阵 | N 维数组</div></summary>
</details>
<div class="details-content">

输入信号，指定为标量、向量、矩阵或 N 维数组。

**数据类型：** float | double | int8 | int16 | int32 | fixed point

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 输入信号的求反<div>标量 | 向量 | 矩阵 | N 维数组</div></summary>
</details>
<div class="details-content">

输入信号的求反。输出具有与输入相同的数据类型和维度。

**数据类型：**  float | double | int8 | int16 | int32 | fixed point

</div>
</div>



## 参数

<div class="details-box">
<details open>
<summary>对整数溢出进行饱和处理 — 溢出操作的方法<div>off（默认） | on</div></summary>
</details>
<div class="details-content">


选中可实现整数溢出饱和。否则，溢出将绕回。

如果选中此复选框，饱和将应用于模块中的每个内部操作，而不仅仅应用于输出或结果。一般情况下，代码生成进程可以检测到何时不可能发生溢出。在这种情况下，代码生成器不会生成饱和代码。

对于有符号整数数据类型，最负值的一元减法无法用该数据类型表示。在这种情况下，由**对整数溢出进行饱和处理**复选框控制模块的行为：

| 参数设置                           | 模块行为                             | 示例                                                         |
| :--------------------------------- | :----------------------------------- | :----------------------------------------------------------- |
| **对整数溢出进行饱和处理** = `on`  | 值饱和处理为该整数数据类型的最大正值 | 对于 8 位有符号整数，-128 对应为 127。对于 16 位有符号整数，-32768 对应为 32767。对于 32 位有符号整数，-2147483648 对应为 2147483647。 |
| **对整数溢出进行饱和处理** = `off` | 值绕回到该整数数据类型的最小负值     | 对于 8 位有符号整数，-128 依然是 -128。对于 16 位有符号整数，-32768 依然是 -32768。对于 32 位有符号整数，-2147483648 依然是 -2147483648。 |

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
<summary>采样时间 — -1 以外的采样时间值<div>-1（默认） | 标量 | 向量</div></summary>
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
<!-- 部分特性暂无
| **数据类型**                                                 | `double` | `fixed pointa` | `integera` | `float` |
| ------------------------------------------------------------ | ---------------------------------------------------------- |
| **直接馈通**                                                 | `是`                                                       |
| **多维信号**                                                 | `是`                                                       |
| **可变大小信号**                                             | `否`                                                       |
| **过零检测**                                                 | `否`                                                       | -->

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



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。

此模块仅支持有符号定点数据类型。 -->

## 版本历史记录

- 在 2024b 之前推出

<!-- ### 限制信息 -->

<!-- 暂无

## 另请参阅


### 主题 -->

