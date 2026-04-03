# TappedDelay
---
&nbsp;

将标量信号延迟多个采样周期并输出所有延迟版本

- **库：** Sysblock / Discrete

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/TappedDelay/TappedDelay.png')" style="width: 100px; height: auto;">

## 描述

Tapped Delay 模块将输入延迟指定数量的采样周期，并为每个延迟提供一个输出信号。例如，当您为**延迟数**指定 4 且**输出向量排序**为**最早**时，该模块提供四个输出，第一个输出延迟四个采样周期，第二个输出延迟三个采样周期，依此类推。使用此模块可以适时离散化信号，或以不同的速率对信号进行重采样。

该模块接受一个标量输入，并生成包含每个增量延迟的数据的输出向量。使用**输出向量排序**参数指定输出向量中的延迟信号顺序：

- **最早**输出向量以最早的延迟版本开始，以最新的延迟版本结束的顺序。
- **最近**输出向量以最新的延迟版本开始，以最早的延迟版本结束的顺序。

通过**初始条件**参数指定第一个采样周期的输出向量。谨慎选择此参数可以减少不需要的输出行为。

通过**采样时间**参数指定采样之间的时间间隔。通过**延迟数**参数指定延迟数量。值 -1 指示模块通过反向传播来继承延迟数量。每个延迟相当于 [UnitDelay](UnitDelay.html) 模块表示的 z-1 离散时间运算符。

## 示例

假设我们有一个简单的音频处理系统，希望通过添加延迟来模拟回声效果。
拖放一个 Sine Wave 模块来模拟简单的音频信号。双击该模块，设置幅度为 1，频率为 100Hz 这里只是为了模拟音频频率，采样时间为 0.001s 模拟音频采样率。输入的音频信号经过延迟模块后，
延迟后的信号和原始信号混合，产生带有回声的音频输出。tappedDelay 模块采样时间设置为 0.001，周期设置为 10。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/TappedDelay.mo">TappedDelay.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/TappedDelay/TappedDelay01.png')" style="width: 600px; height: auto;">

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/TappedDelay/TappedDelay02.png')" style="width: 600px; height: auto;">


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量</div></summary>
</details>
<div class="details-content">
要延迟的输入信号。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | Boolean | fixed point

</div>
</div>



### 输出

<div class="details-box">
<details open>
<summary>y — 输入信号的延迟版本<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

延迟的输入信号的所有版本。使用**输出向量排序**参数指定输出向量中延迟信号的顺序。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | Boolean | fixed point

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>初始条件 — 初始输出<div>0（默认）| 标量</div></summary>
</details>
<div class="details-content">

指定仿真的初始输出。**初始条件**参数通过舍入到最邻近整数及饱和处理从双精度脱机转换为输入数据类型。

</div>
</div>

<!-- 
#### 编程用法

| **模块参数**：`初始条件` |
| --------------------- |
| **类型：**字符向量    |
| **值：**标量          |
| **默认值：**`'0'`   | -->


<div class="details-box">
<details open>
<summary>采样时间 — 采样之间的时间间隔<div>-1（默认）| 标量 | 向量</div></summary>
</details>
<div class="details-content">

指定采样时间间隔。要继承采样时间，请将此参数设置为 -1。

</div>
</div>

<!-- 
#### 编程用法

| **模块参数**：`采样时间` |
| ------------------------ |
| **类型：**字符向量       |
| **值：**标量 \| 向量     |
| **默认值：**`'-1'`       | -->


<div class="details-box">
<details open>
<summary>延迟数 — 离散时间运算符的数量<div>4（默认）| 正标量 | -1（表示继承）</div></summary>
</details>
<div class="details-content">

将离散时间运算符的数量指定为正标量，或指定 -1 表示继承。

</div>
</div>

<!-- 
#### 编程用法

| **模块参数**：`延迟数`      |
| ------------------------------ |
| **类型：**字符向量             |
| **值：**正标量 \| `-1`（继承） |
| **默认值：**`'4'`              | -->


<div class="details-box">
<details open>
<summary>输出向量排序 — 输出的顺序<div>最早（默认）| 最近</div></summary>
</details>
<div class="details-content">

指定先输出最早的延迟版本还是最新的延迟版本。

</div>
</div>

<!-- 
#### 编程用法

| **模块参数**：`输出向量排序`    |
| ----------------------------- |
| **类型：**字符向量            |
| **值**：`'Oldest' | 'Newest'` |
| **默认值：**`'Oldest'`        | -->



<div class="details-box">
<details open>
<summary>将当前输入包含在输出向量中 — 将当前输入包含在输出向量中<div>off （默认） | on</div></summary>
</details>
<div class="details-content">

选中此复选框可将当前输入包括在输出向量中。

</div>
</div>

<!-- 
#### 编程用法

| **模块参数**：`将当前输入包含在输出向量中` |
| ------------------------------ |
| **类型：**字符向量             |
| **值：**`'off' | 'on'`         |
| **默认值：**`'off'`            | -->

<!-- 
## 模型示例
![定点 S-Function：乘积与和](https://ww2.mathworks.cn/help/releases/R2022b/fixedpoint/ug/fxpdemo_sfun_user_prodsum_02_zh_CN.png)

### 定点 S-Function：乘积与和

此模型说明如何使用自定义的 C 语言 S-Function 来计算定点的“乘积与和”运算。要查看 S-Function 的源代码，请使用右键点击上下文菜单选择“模块参数”。当对话框出现时，按“编辑”按钮。

![Internet Low Bitrate Codec (iLBC) for VoIP](https://ww2.mathworks.cn/help/releases/R2022b/examples/dsp/win64/InternetLowBitrateCodecILBCForVoIPExample_02.png)

### Internet Low Bitrate Codec (iLBC) for VoIP

Implements the Internet Low Bitrate Codec (iLBC) and illustrates its use. iLBC is designed for encoding and decoding speech for transmission via VoIP (Voice Over Internet Protocol). -->

<!-- ## 模块特性 -->

<!-- 
| **数据类型**     | `Boolean` \| `double` \| `fixed point` \| `integer` \| `single` |
| ---------------- | ----------------------------------------------------------- |
| **直接馈通**     | `否`                                                        |
| **多维信号**     | `否`                                                        |
| **可变大小信号** | `否`                                                        |
| **过零检测**     | `否`                                                        | -->

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
| **ResetType**                 | 隐藏重置逻辑生成。默认值为“`默认`”，它生成重置逻辑。另请参阅[ResetType](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-27) (HDL Coder)。 |

**复数数据支持**

此模块支持复信号的代码生成。
 -->

<!-- 
### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。

### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。 -->

<!-- ## 版本历史记录

### 限制信息
暂无 -->

## 版本历史记录

- 在 2024b 之前推出

## 另请参阅

[Delay](Delay.html) | [UnitDelay](UnitDelay.html) 
