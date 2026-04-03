# Backlash
---
&nbsp;


对间隙系统行为进行建模


- **库：** Sysblock / Discontinuities

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/DiscontinuitiesPng/backlash/backlash.png')" style="width: 100px; height: auto;">


## 描述

Backlash 模块实现这样一个系统，其中输入信号的改变使得输出信号产生相同的改变量，输入改变方向时除外。当输入信号方向改变时，输入信号的初始变化不会影响输出。系统的侧隙称为死区。死区位于输出信号的中心。下图显示了初始状态，默认死区宽度为 1，初始输出为 0。
 

间隙系统有三种模式。

| 模式       | 输入               | 输出                           |
| :--------- | :----------------- | :----------------------------- |
| 不啮合     | 在死区内。         | 保持不变。                     |
| 正方向啮合 | 在死区外并且增加。 | 等于输入减去死区宽度的一半。 |
| 负方向啮合 | 在死区外并且减少。 | 等于输入加上死区宽度的一半。 |

**初始输出**参数值定义死区的初始中心。

下表显示初始条件为各种情况时的输出值：**死区宽度** = `2` 和**初始输出** = `5`。

| 输出值   | 条件           |
| :------- | :------------- |
| 5        | 4 <= 输入 <= 6 |
| 输入 + 1 | 输入 < 4       |
| 输入 - 1 | 输入 > 6       |

例如，您可以使用 Backlash 模块对两个齿轮的啮合进行建模。输入和输出是两个轴（一端带有齿轮），输入轴驱动输出轴。轮齿之间的额外空间产生间隙。此间隙的宽度就是**死区宽度**参数。如果系统最初不啮合，则**初始输出**参数定义输出。

下列各图显示当初始输入处于死区范围内和系统在不啮合模式下开始时的操作。


当输入增加并到达死区边缘时，它与输出啮合。输出保持在上一个值。


在输入与输出啮合后，输出以与输入相同的量变化。


如果输入反转方向，则不再与输出啮合。输出保持不变，直到输入到达死区边缘并重新啮合。

## 示例

使用 sineWave 模块输出一个正弦波，将 Backlash 模块的死区设置为 1。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discontinuities/backlash.mo">Backlash.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/DiscontinuitiesPng/backlash/backlash02.png')" style="width: 600px; height: auto;">


<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/DiscontinuitiesPng/backlash/backlash01.png')" style="width: 600px; height: auto;">


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

Backlash 算法的输入信号。此信号的值要么在死区中，要么在正方向或负方向上与输出啮合。

**数据类型：** double | float | int8 | int16 | int32 | uint8 | uint16 | uint32

</div>
</div>

### 输出


<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

Backlash 算法应用于输入信号后的输出信号。当输入处于死区中时，输出保持不变。如果输入与输出啮合，则输出将与输入等量变化。

**数据类型：** double | float | int8 | int16 | int32 | uint8 | uint16 | uint32

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>死区宽度 — 指定死区的宽度<div>1 （默认） | 标量 | 向量</div></summary>
</details>
<div class="details-content">

指定以输出值为中心的死区的大小。当输入信号在死区内时，输入的更改不会引起输出的更改。当输入信号在死区外时，输出将与输入等量变化。

</div>
</div>

<!-- 
#### 编程用法

| **模块参数**：`BacklashWidth` |
| ----------------------------- |
| **类型**：字符向量            |
| **值**：实数标量或向量        |
| **默认值**：`'1'`             | -->



<div class="details-box">
<details open>
<summary>初始输出 — 指定初始输出值 <div>0 （默认） | 标量 | 向量</div></summary>
</details>
<div class="details-content">

指定死区的初始中心。如果初始输入值在死区中，则输出值等于**初始输出**。如果初始输入值在死区外，则输出值为**初始输出**加上或减去死区宽度的一半。

</div>
</div>


<!--
#### 编程用法
| **模块参数**：`InitialOutput` |
| ----------------------------- |
| **类型**：字符向量            |
| **值**：实数标量或向量        |
| **默认值**：`'0'`             | -->


<!-- 暂无

### `输入处理` — 指定基于采样或基于帧的处理 “`元素作为通道(基于采样)`” （默认） | “`列作为通道(基于帧)`”



指定模块是执行基于采样还是基于帧的处理：

- “`列作为通道(基于帧)`” - 将输入信号的每一列视为一个单独的通道（基于帧的处理）。

  

  **注意**

  基于帧的处理需要具有 DSP System Toolbox™ 许可证。

  有关详细信息，请参阅[Sample- and Frame-Based Concepts](https://ww2.mathworks.cn/help/releases/R2022b/dsp/ug/sample-and-frame-based-concepts.html) (DSP System Toolbox)。

- “`元素作为通道(基于采样)`” - 将输入信号的每个元素视为一个单独的通道（基于采样的处理）。

可以使用**输入处理**指定模块是执行基于采样的处理还是基于帧的处理。有关这两种处理模式的详细信息，请参阅[Sample- and Frame-Based Concepts](https://ww2.mathworks.cn/help/releases/R2022b/dsp/ug/sample-and-frame-based-concepts.html) (DSP System Toolbox)。

#### 编程用法

| **模块参数**：`InputProcessing`                              |
| ------------------------------------------------------------ |
| **类型**：字符向量                                           |
| **值**：`'Columns as channels (frame based)'` | `'Elements as channels (sample based)'` |
| **默认值**：`'Elements as channels (sample based)'`          |

 -->

<!-- 暂无
### `启用过零检测` — 启用过零检测 `on` （默认） | `off`



选择此项以启用过零检测。有关详细信息，请参阅[过零检测](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/zero-crossing-detection.html)。

此模块仅在使用变步长求解器的仿真中支持过零检测。当使用定步长求解器进行仿真时，软件不会检测或定位此模块的过零点。

#### 编程用法

| **模块参数**：`ZeroCross`    |
| ---------------------------- |
| **类型**：字符向量 \| 字符串 |
| **值**：`'off'` | `'on'`     |
| **默认值**：`'on'`           | -->




<!-- ## 模块特性 -->

<!-- 部分功能未实现
| **数据类型**     | `double` \| `integer` \| `float` |
| ---------------- | ------------------------------- |
| **直接馈通**     | `是`                            |
| **多维信号**     | `否`                            |
| **可变大小信号** | `否`                            |
| **过零检测**     | `是`                            | -->


<!-- ## 拓展功能 -->

<!-- 

### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。

生成的代码在某些条件下依赖于 `memcpy` 或 `memset` 函数 (`string.h`)。



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 Verilog 代码和 VHDL 代码。



HDL Coder™ 提供影响 HDL 实现和综合逻辑的额外配置选项。

**HDL 架构**

此模块具有一个默认 HDL 架构。

**HDL 模块属性**

| **ConstrainedOutputPipeline** | 通过移动设计中现有延迟的方式来放置在输出端的寄存器的数量。分布式流水线处理不会重新分发这些寄存器。默认值为 `0`。有关详细信息，请参阅[ConstrainedOutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#btp8gmp) (HDL Coder)。 |
| ----------------------------- | ------------------------------------------------------------ |
| **InputPipeline**             | 要在生成的代码中插入的输入流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 `0`。有关详细信息，请参阅[InputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-25) (HDL Coder)。 |
| **OutputPipeline**            | 要在生成的代码中插入的输出流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 `0`。有关详细信息，请参阅[OutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-26) (HDL Coder)。 |

**限制**

**死区宽度**和**初始输出**参数仅支持标量值。 -->


## 版本历史记录

- 在 2024b 之前推出

未实现部分
1. 参数-输入处理 — 指定基于采样或基于帧的处理
2. 参数-启用过零检测
 
## 另请参阅

[DeadZone](DeadZone.html)
