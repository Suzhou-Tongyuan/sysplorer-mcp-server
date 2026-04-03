# SineWaveFunction
---
&nbsp;

使用外部信号作为时间源来生成正弦波


- **库：** Sysblock / MathOperation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/SineWaveFunction/SineWaveFunction.png')" style="width: 100px; height: auto;">

## 描述

SineWaveFunction 模块输出正弦曲线波形。此模块可在基于时间或基于采样的模式下运行。


### 基于时间的模式

<!-- 该模块可计算输出波形。

*y*=*a**m**p**l**i**t**u**d**e*×sin(*f**r**e**q**u**e**n**c**y*×*t**i**m**e*+*p**h**a**s**e*)+*b**i**a**s*. -->

在基于时间的模式下，**采样时间**参数的值确定模块是在连续模式还是离散模式下运行。

<!-- - `0`（默认值）将使得模块在连续模式下运行。
- `>0` 将使得模块在离散模式下运行。 -->


**连续模式下的模块行为**

在连续模式下运行时，由于随着时间变得非常大，导致精度损失，因此 SineWave 模块可能会变得不准确。

**离散模式下的模块行为**

如果**采样时间**参数的值大于零，将会导致模块好像在驱动一个采样时间设置为该值的 Zero-Order Hold 模块。

<!-- 
通过这种方式，您可以构建具有纯离散正弦波源的模型，而不是混合了连续/离散系统的模型。混合系统本质上更复杂，因此需要更长的仿真时间。

在离散模式下，此模块使用微分增量算法，而不是基于绝对时间的算法。因此，此模块对于要在无限长时间内运行的模块（如振动或疲劳测试）非常有用。

微分增量算法根据在上一采样时间计算出的值来计算正弦值。此方法使用下列三角恒等式：

sin(*t*+Δ*t*)=sin(*t*)cos(Δ*t*)+sin(Δ*t*)cos(*t*)cos(*t*+Δ*t*)=cos(*t*)cos(Δ*t*)−sin(*t*)sin(Δ*t*)

采用矩阵形式，这些恒等式表示为：

[sin(*t*+Δ*t*)cos(*t*+Δ*t*)]=[cos(Δ*t*)−sin(Δ*t*)sin(Δ*t*)cos(Δ*t*)][sin(*t*)cos(*t*)]

由于 Δt 是常量，所以下列表达式是常量：

[cos(Δ*t*)−sin(Δ*t*)sin(Δ*t*)cos(Δ*t*)]

因此，问题就变为一种矩阵乘法，用 sin(*t*) 的值乘以一个常量矩阵以得出 sin(*t*+Δ*t*)。

离散模式只能减少但不能消除舍入误差的累积，例如 `(4*eps)`。发生累积是因为模块在每个时间步的输出的计算都取决于上一个时间步的输出值。 -->


### 基于采样的模式

基于采样的模式使用以下公式计算 Sine Wave 模块的输出。

<!-- *y*=*A*sin(2*π*(*k*+*o*)/*p*)+*b*

- A 是正弦波的幅值。
- p 是每个正弦波周期内的时间采样数。
- k 为重复的整数值，范围从 0 到 p–1。
- o 是信号的偏移量（相位偏移）。
- b 是信号偏差。 -->


在计算给定时间步的模块输出时，基于采样的方法不依赖于上一个时间步的输出。因此，这种模式可以避免舍入误差的累积。基于采样的模式还支持在提供语义的子系统中重置语义。例如，如果 SineWave 模块在一个可重置子系统中，子系统收到一个重置触发事件，重复的整数 `k` 将重置，模块输出将重置为其初始条件。

## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperation/SineWaveFunction.mo">SineWaveFunction.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/SineWaveFunction/SineWaveFunction01.png')" style="width: 600px; ">


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 时间源信号<div>标量</div></summary>
</details>
<div class="details-content">

正弦波计算中所使用的时间源输入信号。

**数据类型：** double

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y1 — 正弦波输出信号<div>标量</div></summary>
</details>
<div class="details-content">

所创建的正弦波输出信号。

**数据类型：** double

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>正弦类型 — 正弦波的类型<div>基于时间（默认） | 基于采样</div></summary>
</details>
<div class="details-content">

指定此模块生成的正弦波的类型。根据您选择的是基于时间还是基于采样，对话框中将出现某些参数。

</div>
</div>


<!-- #### 编程用法

| **模块参数**：`SineType`                  |
| ----------------------------------------- |
| **类型**：字符向量                        |
| **值**：`'Time based'` | `'Sample based'` |
| **默认值**：`'Time based'`                | -->

<div class="details-box">
<details open>
<summary>时间(t) — 时间变量的来源<div>使用外部信号（默认） | 使用仿真时间</div></summary>
</details>
<div class="details-content">

指定是使用仿真时间还是外部源作为时间变量值的来源。如果指定外部时间源，模块将为该时间源创建一个输入端口。

</div>
</div>


<!-- #### 编程用法

| **模块参数**：`TimeSource`                                |
| --------------------------------------------------------- |
| **类型**：字符向量                                        |
| **值**：`'Use simulation time'` | `'Use external signal'` |
| **默认值**：`'Use external signal'`                       | -->

<div class="details-box">
<details open>
<summary>振幅 — 正弦波的幅值<div>1 （默认） | 标量</div></summary>
</details>
<div class="details-content">

振幅 — 正弦波的幅值

</div>
</div>


<!-- #### 编程用法

| **模块参数**：`Amplitude` |
| ------------------------- |
| **类型**：字符向量        |
| **值**：标量              |
| **默认值**：`'1'`         | -->


<div class="details-box">
<details open>
<summary>偏置 — 添加到正弦波的常量<div>0（默认） | 标量</div></summary>
</details>
<div class="details-content">


指定为了生成输出在正弦中添加的常量值。

</div>
</div>

<!--
 #### 编程用法

| **模块参数**：`Bias` |
| -------------------- |
| **类型**：字符向量   |
| **值**：标量         |
| **默认值**：`'0'`    | -->



<div class="details-box">
<details open>
<summary>频率(弧度/秒) — 正弦波的频率<div>1（默认） | 标量</div></summary>
</details>
<div class="details-content">

以 rad/sec 为单位指定信号频率。

#### 依存关系

要启用此参数，请将**正弦类型**设置为**基于时间**。

</div>
</div>


<!--
#### 编程用法

 | **模块参数**：`Frequence` |
| ------------------------- |
| **类型**：字符向量        |
| **值**：标量              |
| **默认值**：`'1'`         | -->

<div class="details-box">
<details open>
<summary>相位(弧度) — 正弦波的相移<div>0 （默认） | 标量</div></summary>
</details>
<div class="details-content">

指定正弦波的相移。

如果将**时间 (t)** 设置为**使用仿真时间**，则不能将此参数配置为在生成的代码中显示为可调全局变量。

要生成代码以便在执行期间可以调整相位，请将**时间 (t)** 设置为**使用外部信号**。您可以提供您自己的时间输入信号，或使用 Digital Clock 模块生成时间信号。

</div>
</div>


<!-- #### 编程用法

| **模块参数**：`Phase` |
| --------------------- |
| **类型**：字符向量    |
| **值**：标量          |
| **默认值**：`'0'`     | -->

<div class="details-box">
<details open>
<summary>每周期采样数 — 每个周期的采样数<div>0（默认） | integer</div></summary>
</details>
<div class="details-content">

指定每个周期的采样数。

#### 依存关系

要启用此参数，请将**正弦类型**设置为**基于采样**。

</div>
</div>


<!-- #### 编程用法

| **模块参数**：`Samples` |
| ----------------------- |
| **类型**：字符向量      |
| **值**：标量            |
| **默认值**：`'10'`      |  -->

<div class="details-box">
<details open>
<summary>偏移量(采样数) — 偏移量（以时间采样数为单位）<div>0（默认） | integer</div></summary>
</details>
<div class="details-content">


以采样次数为单位指定偏移量（离散相位偏移）。

#### 依存关系

要启用此参数，请将**正弦类型**设置为**基于采样**。

</div>
</div>

<!-- #### 编程用法

| **模块参数**：`Offset` |
| ---------------------- |
| **类型**：字符向量     |
| **值**：标量           |
| **默认值**：`'0'`      | -->



<div class="details-box">
<details open>
<summary>采样时间 — 采样周期<div>0 （默认） | 标量</div></summary>
</details>
<div class="details-content">

以秒为单位指定采样周期。默认值为 0。如果正弦类型是基于采样，则采样时间必须大于 0。

</div>
</div>


<!-- #### 编程用法

 | **模块参数**：`SampleTime` |
| -------------------------- |
| **类型**：字符向量         |
| **值**：标量               |
| **默认值**：`'0'`          |  -->



<div class="details-box">
<details open>
<summary>将向量参数解释为一维向量 — 单行或单列矩阵的输出维度<div>off（默认） | on</div></summary>
</details>
<div class="details-content">


指定当其他参数是单行和单列矩阵时输出维度为一维向量信号。当利用外部信号指定时间时，此参数不可用。在这种情况下，如果数值参数是列或行矩阵值，输出则为 1 维向量。

</div>
</div>


<!-- 
#### 编程用法

| **模块参数**：`VectorParams1D` |
| ------------------------------ |
| **类型**：字符向量             |
| **值**：`'off'` | `'on'`       |
| **默认值**：`'on'`             | -->

<!-- ## 模块特性 -->

<!-- 部分特性暂无
| **数据类型**     | `double` |
| ---------------- | -------- |
| **直接馈通**     | `是`     |
| **多维信号**     | `否`     |
| **可变大小信号** | `否`     |
| **过零检测**     | `否`     | -->

<!-- ## 扩展功能 -->

<!-- 

### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。

位于触发子系统层次结构中时取决于绝对时间。当配置为基于采样运行时，这些模块不引用绝对时间。在基于时间的运行中，它们依赖于绝对时间。 -->

## 版本历史记录

- 在 2024b 之前推出

<!-- ### 限制信息

暂无

## 另请参阅 -->

<!-- [Sine Wave](SineWave.html) -->