# DeadZone
---
&nbsp;

输入位于死区内时输出零。超出死区时，按起始值或结束值对输入信号进行偏移

- **库：** Sysblock / Discontinuities

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/DiscontinuitiesPng/deadZone/deadZone.png')" style="width: 100px; height: auto;">


## 描述

Dead Zone 模块在指定的区域内生成零值输出，此区域称为死区。您可以通过**死区起点**和**死区终点**参数指定死区的下限 (`LL`) 和上限 (`UL`)。模块输出取决于输入 (`U`) 以及上限和下限的值。

| 输入                   | 输出       |
| :--------------------- | :--------- |
| `U >= LL` 和 `U <= UL` | 零         |
| `U > UL`               | `U` – `UL` |
| `U < LL`               | `U` – `LL` |


## 示例

DeadZone 模块设置死区下限 -0.5，上限 0.5。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discontinuities/DeadZone.mo">DeadZone.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/DiscontinuitiesPng/deadZone/deadZone01.png')" style="width: 600px; height: auto;">

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/DiscontinuitiesPng/deadZone/deadZone02.png')" style="width: 600px; height: auto;">


## 端口


### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

死区算法的输入信号。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | fixed point

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

死区算法应用于输入信号后的输出信号。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | fixed point

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>死区起点 — 指定死区的下界<div>-0.5 （默认） | 标量 | 向量</div></summary>
</details>
<div class="details-content">



指定死区下限。为**死区起点**设置小于或等于**死区终点**的值。当输入值小于**死区起点**时，模块会将输出值向下移动**死区起点**值。

</div>
</div>


<!-- 
#### 编程用法

| **模块参数**：`LowerValue`                     |
| ---------------------------------------------- |
| **类型**：字符向量                             |
| **值**：小于或等于 `UpperValue` 的标量或向量。 |
| **默认值**：`'-0.5'`                           | -->

<div class="details-box">
<details open>
<summary>死区终点 — 指定死区的上限<div>0.5 （默认） | 标量 | 向量</div></summary>
</details>
<div class="details-content">

指定死区上限。为**死区终点**设置大于或等于**死区起点**的值。当输入值大于**死区终点**时，模块会将输出值向下移动**死区终点**值。

</div>
</div>

<!-- 
#### 编程用法

| **模块参数**：`UpperValue`                     |
| ---------------------------------------------- |
| **类型**：字符向量                             |
| **值**：大于或等于 `LowerValue` 的标量或向量。 |
| **默认值**：`'0.5'`                            | -->


<!-- 暂无
### `对整数溢出进行饱和处理` — 选择发生整数溢出时的行为 “`off`” （默认） | “`on`”





| 操作             | 执行此操作的原因                                             | 溢出时会发生的情况                                 | 示例                                                         |
| :--------------- | :----------------------------------------------------------- | :------------------------------------------------- | :----------------------------------------------------------- |
| 选中此复选框。   | 您的模型可能有溢出，并且您希望在生成的代码中具有显式饱和保护。 | 将溢出饱和处理为数据类型能够表示的最小值或最大值。 | `int8`（有符号 8 位整数）数据类型可以表示的最大值为 127。任何大于此最大值的模块运算结果都会导致 8 位整数溢出。如果选中此复选框，模块输出将在达到 127 时饱和。类似地，模块输出将在达到最小输出值 -128 时饱和。 |
| 不选中此复选框。 | 您需要优化所生成代码的效率。您希望避免过度地指定信号超出范围时的处理方式。有关详细信息，请参阅[信号范围错误故障排除](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/signal-ranges.html#brdiku9)。 | 溢出会绕回到由数据类型表示的适当值。               | `int8`（有符号 8 位整数）数据类型可以表示的最大值为 127。任何大于此最大值的模块运算结果都会导致 8 位整数溢出。清除该复选框时，软件会将导致溢出的值解释为 `int8`，这可能产生意外结果。例如，以 `int8` 表示的模块结果 130（二进制 1000 0010）为 -126。 |



如果选中此复选框，饱和将应用于模块中的每个内部操作，而不仅仅应用于输出或结果。通常，代码生成过程可以检测何时不会发生溢出。在这种情况下，代码生成器不会生成饱和代码。

#### 编程用法

| **模块参数**：`DoSatur`  |
| ------------------------ |
| **类型**：字符向量       |
| **值**：`'off'` | `'on'` |
|                          |
| **默认值**：`'off'`      | -->


<!-- 暂无
### `线性化时视为增益` — 指定增益值 `On` （默认） | 布尔



Simulink® 软件中的线性化命令将此模块视为状态空间中的增益。选中此复选框将使得这些命令将增益视为 1。清除该框将使得这些命令将增益视为 0。

#### 编程用法

| **模块参数**：`LinearizeAsGain` |
| ------------------------------- |
| **类型**：字符向量              |
| **值**：`'off'` | `'on'`        |
|                                 |
| **默认值**：`'on'`              | -->


<!-- 暂无
### `启用过零检测` — 启用过零检测 `on` （默认） | `off`



选择此项以启用过零检测。有关详细信息，请参阅[过零检测](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/zero-crossing-detection.html)。

#### 编程用法

| **模块参数**：`ZeroCross`    |
| ---------------------------- |
| **类型**：字符向量 \| 字符串 |
| **值**：`'off'` | `'on'`     |
| **默认值**：`'on'`           |
 -->

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

<!-- 部分功能未实现
| **数据类型**     | `double` \| `fixed point` \| `integer` \| `single` |
| ---------------- | ----------------------------------------------- |
| **直接馈通**     | `是`                                            |
| **多维信号**     | `否`                                            |
| **可变大小信号** | `否`                                            |
| **过零检测**     | `是`                                            | -->


<!-- ## 扩展功能 -->


<!-- 
### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 Verilog 代码和 VHDL 代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。 -->



## 版本历史记录

- 在 2024b 之前推出

### 限制信息
不支持部分
1. 参数-对整数溢出进行饱和处理
2. 参数-线性化时视为增益
3. 参数-启用过零检测
4. 参数-采样时间 — -1 以外的采样时间值

## 另请参阅

[DeadZoneDynamic](DeadZoneDynamic.html) | [Backlash](Backlash.html)