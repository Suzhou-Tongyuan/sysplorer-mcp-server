# SineWave
---
使用仿真时间作为时间源以生成正弦波

**库：** Sysblock模块库 / Sources

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/SineWave/SineWave.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

SineWave 模块输出正弦曲线波形。此模块可在基于时间或基于采样的模式下运行。


::: warning 注意

此模块相当于 MathOperation 模块库中的 [SineWaveFunction](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/SineWaveFunction.html) 模块。如果您在模块对话框中为**时间**参数选择了“使用外部信号”，您将获得 Sine Wave Function 模块。

:::

### 基于时间的模式

该模块可计算输出波形。

O(t)= Amp\*Sin(Freq\*t+相位)+偏置

在基于时间的模式下，**采样时间**参数的值确定模块是在连续模式还是离散模式下运行。

- 0（默认值）将使得模块在连续模式下运行；
- \>0 将使得模块在离散模式下运行。

有关详细信息，请参阅[指定采样时间](/Doc/Sysblock/Modeling/ConfigureSignals/SampleTime/SpecifyTime.md)。

**连续模式下的模块行为**

在连续模式下运行时，由于随着时间变得非常大，导致精度损失，因此 SineWave 模块可能会变得不准确。

**离散模式下的模块行为**

通过这种方式，您可以构建具有纯离散正弦波源的模型，而不是混合了连续/离散系统的模型。混合系统本质上更复杂，因此需要更长的仿真时间。

在离散模式下，此模块使用微分增量算法，而不是基于绝对时间的算法。因此，此模块对于要在无限长时间内运行的模块（如振动或疲劳测试）非常有用。

微分增量算法根据在上一采样时间计算出的值来计算正弦值。此方法使用下列三角恒等式：

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/SineWave/SineWave01.png')" style="width: 350px; height: auto; transform: scale(1);">

采用矩阵形式，这些恒等式表示为：

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/SineWave/SineWave02.png')" style="width: 350px; height: auto; transform: scale(1);">

由于 Δt 是常量，所以下列表达式是常量：

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/SineWave/SineWave03.png')" style="width: 150px; height: auto; transform: scale(1);">

因此，问题就变为一种矩阵乘法，用 `sin(t)` 的值乘以一个常量矩阵以得出 `sin(t+Δt)`。

离散模式只能减少但不能消除舍入误差的累积,例如 `(4*eps)`。发生累积是因为模块在每个时间步的输出的计算都取决于上一个时间步的输出值。

<!-- **离散模式下的舍入误差的处理方法**

要处理 Sine Wave block 模块在基于时间的离散模式下运行时产生的舍入误差，请使用下列方法之一。

| 方法                                                         | 原理说明                                                     |
| :----------------------------------------------------------- | :----------------------------------------------------------- |
| 在 Sine Wave 模块的直接下游插入一个 [Saturation](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Discontinuities/Saturation.html) 模块。 | 通过为 Sine Wave 模块输出设置饱和界限，可以避免由于舍入误差累积而出现的过冲。 |
| 将 Sine Wave 模块设置为使用 sin() 数学模块库函数来计算模块输出。<br> 1.在 Sine Wave 模块对话框中，将**时间**设置为“使用外部信号”，这样模块图标上将出现一个输入端口。2.使用 [Clock](Clock.html) 模块将一个时钟信号连接到此输入端口上。3.将时钟信号的采样时间设置为 Sine Wave 模块的采样时间。 | sin() 数学模块库函数*单独*计算每个时间步的模块输出，从而可以避免舍入误差的累积。 | -->

### 基于采样的模式

基于采样的模式使用以下公式计算 SineWave 模块的输出。

`y = A sin(2π (k + o)/ p) + b`

- A 是正弦波的幅值；
- p 是每个正弦波周期内的时间采样数；
- k 为重复的整数值，范围从 0 到 p–1；
- o 是信号的偏移量（相位偏移）；
- b 是信号偏差。

在此模式下，Sysblock 将第一个时间步的 k 设置为等于 0，并使用该公式计算模块输出。在下一个时间步，Sysblock 递增 k，然后重新计算模块输出。当 k 达到 p 时，Sysblock 在计算模块输出之前将 k 重置为 0。此过程会一直继续，直到仿真结束。

在计算给定时间步的模块输出时，基于采样的方法不依赖于上一个时间步的输出。因此，这种模式可以避免舍入误差的累积。基于采样的模式还支持在提供语义的子系统中重置语义。例如，如果 Sine Wave 模块在一个可重置子系统中，子系统收到一个重置触发事件，重复的整数 k 将重置，模块输出将重置为其初始条件。

## 示例

<!-- [![房屋的热模型](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/sldemo_househeatexample_05_zh_CN.png)房屋的热模型此示例说明如何使用 Simulink® 来创建房屋的热模型。此系统对室外环境、房屋的热特性和房屋供暖系统进行建模。](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/thermal-model-of-a-house.html)

[![Simulating Systems with Variable Transport Delay Phenomena](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink_general/win64/sldemo_VariableTransportDelayExample_04.png)Simulating Systems with Variable Transport Delay PhenomenaTwo cases where you can use Simulink® to model variable transport delay phenomena.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/simulating-systems-with-variable-transport-delay-phenomena.html)

[![精确的过零检测](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/sldemo_zeroxingexample_02_zh_CN.png)精确的过零检测此示例说明 Simulink® 中过零的工作原理。在此模型中，三个经过偏移的正弦波被馈送到绝对值模块及饱和模块中。在正好 t = 5 时，开关模块的输出从绝对值变为饱和模块。Simulink 中的过零将自动检测到开关模块具体何时更改其输出，求解器将步进到事件发生的确切时间。您可以通过检查示波器输出来查看这些信息。](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/accurate-zero-crossing-detection.html) -->


参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/SineWave.mo">SineWave.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/SineWave/SineWave_ex.png')" style="width: 300px; height: auto; transform: scale(0.8);">

### 示例说明

- SineWave 模块：用于生成一个标准的正弦波信号。此模块允许用户设置振幅、频率、相位和偏置，以自定义正弦波的形状和特性；
- Scope 模块：用于显示模型的输出结果，即 Sine Wave 模块生成的正弦波信号。Scope 模块可以帮助用户直观地观察和分析信号的波形。




## 端口

### 输出

<div class="details-box">
<details open>
<summary>y — 正弦波输出信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

基于模块参数值创建的正弦波输出信号。

**数据类型：** double

</div>
</div>



## 参数


<div class="details-box">
<details open>
<summary>正弦类型 — 正弦波的类型<div>“基于时间” （默认） | “基于采样”</div></summary>
</details>
<div class="details-content">

指定此模块生成的正弦波的类型。根据您选择的是基于时间还是基于采样，对话框中将出现某些参数。

</div>
</div>




<!-- #### 编程用法

| **模块参数**：SineType                  |
| ----------------------------------------- |
| **类型**：字符向量                        |
| **值**：'Time based' | 'Sample based' |
| **默认值**：'Time based'                | -->


<div class="details-box">
<details open>
<summary>时间(t) — 时间变量的来源<div>“使用仿真时间” （默认） | “使用外部信号”</div></summary>
</details>
<div class="details-content">

指定是使用仿真时间还是外部源作为时间变量值的来源。如果指定外部时间源，模块将为该时间源创建一个输入端口。选择外部时间源时，该模块与 Sine Wave Function 模块相同。

</div>
</div>



<!-- #### 编程用法

| **模块参数**：TimeSource                                |
| --------------------------------------------------------- |
| **类型**：字符向量                                        |
| **值**：'Use simulation time' | 'Use external signal' |
| **默认值**：'Use simulation time'                       | -->


<div class="details-box">
<details open>
<summary>振幅 — 正弦波的幅值<div>1 （默认） | 标量 | 向量</div></summary>
</details>
<div class="details-content">

指定正弦波输出信号的幅值。

</div>
</div>




<!-- #### 编程用法

| **模块参数**：Amplitude |
| ------------------------- |
| **类型**：字符向量        |
| **值**：标量              |
| **默认值**：'1'         | -->


<div class="details-box">
<details open>
<summary>偏置 — 添加到正弦波的常量<div>0 （默认） | 标量 | 向量</div></summary>
</details>
<div class="details-content">

指定为了生成输出在正弦中添加的常量值。

</div>
</div>




<!-- #### 编程用法

| **模块参数**：Bias |
| -------------------- |
| **类型**：字符向量   |
| **值**：标量         |
| **默认值**：'0'    | -->

<div class="details-box">
<details open>
<summary>频率(弧度/秒) — 正弦波的频率<div>1 （默认） | 标量 | 向量</div></summary>
</details>
<div class="details-content">

指定频率，以 rad/sec 为单位。

**依存关系：**要启用此参数，请将**正弦类型**设置为“基于时间”。

</div>
</div>



<!-- #### 编程用法

| **模块参数**：Frequency |
| ------------------------- |
| **类型**：字符向量        |
| **值**：标量              |
| **默认值**：'1'         | -->



<div class="details-box">
<details open>
<summary>相位(弧度) — 正弦波的相移<div>0 （默认） | 标量 | 向量</div></summary>
</details>
<div class="details-content">

指定正弦波的相移。

<!-- 如果将**时间(t)** 设置为“使用仿真时间”，则不能将此参数配置为在生成的代码中显示为可调全局变量。例如，如果将**默认参数行为**设置为“可调”或将某个存储类应用于 Simulink.Parameter 对象，则**相位**参数不会在生成的代码中显示为可调全局变量。

要生成代码以便在执行期间可以调整相位，请将**时间(t)** 设置为“使用外部信号”。您可以提供您自己的时间输入信号，或使用 Digital Clock 模块生成时间信号。有关示例，请参阅[Tune Phase Parameter of Sine Wave Block During Code Execution](https://ww2.mathworks.cn/help/releases/R2022b/rtw/ug/tune-phase-parameter-of-sine-wave-block-during-code-execution.html) (Simulink Coder)。 -->

**依存关系：**要启用此参数，请将**正弦类型**设置为“基于时间”。

</div>
</div>




<!-- #### 编程用法

| **模块参数**：Phase |
| --------------------- |
| **类型**：字符向量    |
| **值**：标量          |
| **默认值**：'0'     | -->


<div class="details-box">
<details open>
<summary>每周期采样数 — 每个周期的采样数<div>0 （默认） | integer scalar | integer vector</div></summary>
</details>
<div class="details-content">

指定每个周期的采样数。

**依存关系：**要启用此参数，请将**正弦类型**设置为“基于采样”。

</div>
</div>




<!-- #### 编程用法

| **模块参数**：Samples |
| ----------------------- |
| **类型**：字符向量      |
| **值**：标量            |
| **默认值**：'10'      | -->


<div class="details-box">
<details open>
<summary>偏移量(采样数) — 偏移量（采样时间数）<div>0 （默认） | integer scalar | integer vector</div></summary>
</details>
<div class="details-content">

以采样次数为单位指定偏移量（离散相位偏移）。

**依存关系：**要启用此参数，请将**正弦类型**设置为“基于采样”。

</div>
</div>



<!-- #### 编程用法
s
| **模块参数**：Offset |
| ---------------------- |
| **类型**：字符向量     |
| **值**：标量           |
| **默认值**：'0'      | -->


<div class="details-box">
<details open>
<summary>采样时间 — 采样周期<div>-1 （默认） | 标量 | 向量</div></summary>
</details>
<div class="details-content">

以秒为单位指定采样周期。默认值为 -1。如果正弦类型是基于采样，则采样时间必须大于 0。

</div>
</div>


<!-- 请参阅 [指定采样时间](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/how-to-specify-the-sample-time.html)。 -->

<!-- #### 编程用法

| **模块参数**：SampleTime |
| -------------------------- |
| **类型**：字符向量         |
| **值**：标量               |
| **默认值**：'0'          | -->



<!-- ### 将向量参数解释为一维向量 — 单行或单列矩阵的输出维度 off （默认） | on



指定当其他参数是单行和单列矩阵时输出维度为一维向量信号。如果不选中此框，模块将输出与数值参数具有相同维数的信号。请参阅[确定源模块的输出维度](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/determining-output-signal-dimensions.html#bsud_ek-4)。当利用外部信号指定时间时，此参数不可用。在这种情况下，如果数值参数是列或行矩阵值，输出则为 1 维向量。

#### 编程用法

| **模块参数**：VectorParams1D |
| ------------------------------ |
| **类型**：字符向量             |
| **值**：'off' | 'on'       |
| **默认值**：'on'             | -->



<!-- ## 模块特性

| **数据类型**     | double |
| ---------------- | -------- |
| **直接馈通**     | 是     |
| **多维信号**     | 否     |
| **可变大小信号** | 否     |
| **过零检测**     | 否     | -->


## 版本历史记录

- 在 2024b 之前推出

### 限制信息

暂不支持将向量参数解释为一维向量的复选框。


<!-- ## 扩展功能



### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。

位于触发子系统层次结构中时取决于绝对时间。当配置为基于采样运行时，这些模块不引用绝对时间。在基于时间的运行中，它们依赖于绝对时间。

## 版本历史记录

**在 R2006a 之前推出** -->

## 另请参阅

<!-- [Sine, Cosine](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/sine.html) |  -->
[SineWaveFunction](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/SineWaveFunction.html)