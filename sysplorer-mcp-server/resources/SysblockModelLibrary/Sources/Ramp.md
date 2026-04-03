# Ramp
---
生成持续上升或下降的信号

**库：** Sysblock模块库 / Sources

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/Ramp/Ramp.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

Ramp 模块可生成从指定时间和值开始并以指定的速率发生变化的信号。此模块的**斜率**、**开始时间**和**初始输出**参数确定了输出信号的特征。进行标量扩展后，所有这些参数必须具有相同的维度。

## 示例

<!-- [![Simulating Systems with Variable Transport Delay Phenomena](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink_general/win64/sldemo_VariableTransportDelayExample_04.png)Simulating Systems with Variable Transport Delay PhenomenaTwo cases where you can use Simulink® to model variable transport delay phenomena.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/simulating-systems-with-variable-transport-delay-phenomena.html) -->

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/Ramp.mo">Ramp.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/Ramp/Ramp_ex.png')" style="width: 300px; height: auto; transform: scale(0.8);">

### 示例说明

- Ramp 模块：生成一个线性增加的信号。此模块的参数斜和初始输出决定了信号的起始点和变化速率；
- Scope 模块：用于显示模型的输出结果，即 Ramp 模块生成的线性增加信号。

## 端口

### 输出


<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

产生的输出斜坡信号的特征由**斜率**、**开始时间**和**初始输出**参数确定。

**数据类型：** double

</div>
</div>




## 参数


<div class="details-box">
<details open>
<summary>斜率 — 信号的斜率<div>1 （默认） | 标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

指定生成的信号的变化率。

</div>
</div>




<!-- #### 编程用法

| **模块参数**：slope |
| --------------------- |
| **类型：**字符向量    |
| **值：**标量          |
| **默认值：**'1'     | -->



<div class="details-box">
<details open>
<summary>开始时间 — 输出的开始时间<div>0 （默认） | 标量</div></summary>
</details>
<div class="details-content">

指定模块开始生成信号的时间。

</div>
</div>




<!-- #### 编程用法

| **模块参数**：start |
| --------------------- |
| **类型：**字符向量    |
| **值：**标量          |
| **默认值：**'0'     | -->


<div class="details-box">
<details open>
<summary>初始输出 — 输出信号的初始值<div>0 （默认） | 标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

指定输出信号的初始值。

</div>
</div>




<!-- #### 编程用法

| **模块参数**：InitialOutput |
| ----------------------------- |
| **类型：**字符向量            |
| **值：**标量                  |
| **默认值：**'0'             | -->



<!-- ### 将向量参数解释为一维向量 — 将向量视为一维 on （默认） | off



如果**常量值**参数的计算结果为包含 N 个元素的行或列向量，选中此复选框将输出长度为 N 的向量。

- 如果**常量值**参数的计算结果为包含 N 个元素的行或列向量，则选中此复选框时，模块将输出长度为 N 的向量。例如，模块将输出 1-by-N 维或 N-by-1 维矩阵。
- 如果**常量值**参数的计算结果为包含 N 个元素的行或列向量，则清除此复选框时，模块不输出长度为 N 的向量。

#### 编程用法

| **模块参数**：VectorParams1D |
| ------------------------------ |
| **类型：**字符向量             |
| **值：**'on' | 'off'         |
| **默认值：**'on'             | -->




## 版本历史记录

- 在 2024b 之前推出

### 限制信息

暂不支持将向量参数解释为一维向量的复选框。

<!-- ## 模块特性

| **数据类型**     | double |
| ---------------- | -------- |
| **直接馈通**     | 否     |
| **多维信号**     | 否     |
| **可变大小信号** | 否     |
| **过零检测**     | 否     |

## 扩展功能



### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。

不建议用于生产代码。

## 版本历史记录

**在 R2006a 之前推出** -->

## 另请参阅

[RepeatingSequence](RepeatingSequence.html) | [PulseGenerator](PulseGenerator.html)