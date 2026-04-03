# RandomSource
---
&nbsp;

生成随机分布的数据。

**库：** TYDSPSystem / SignalGenerationManipulationAndAnalysis / SignalGeneration

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYDSPSystem/SignalGeneration/SignalGeneration/RandomSource/1.png')" style="width: 100px; height: auto; transform: scale(1);border:black 1px solid;">

## 描述

RandomSource 模块生成一帧包含 M 个值的帧，这些值取自均匀分布或高斯伪随机分布。


## 端口

### 输出

<div class="details-box">
<details open>
<summary>y — 随机值信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">
 
具有均匀或高斯（正态）分布的随机值信号。

**数据类型：** double 

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>源类型 — 均匀或高斯<div>Uniform (默认) | Gaussian </div></summary>
</details>
<div class="details-content">

随机值的分布类型，可以是**均匀分布**或**高斯分布**。

 - 将**源类型**参数设置为**均匀分布**时，输出样本将遵循均匀分布，其最小值和最大值分别由**最小值**和**最大值**参数指定。此范围内的所有值被选中的概率相同；

 - 将**源类型**参数设置为**高斯分布**时，还必须设置**方法**参数，该参数决定了模块计算输出的方法。

</div>
</div>

<div class="details-box">
<details open>
<summary>方法 - 计算高斯随机值的方法<div>Ziggurat （默认） | Sum of uniform values</div></summary>
</details>
<div class="details-content">

模块计算高斯随机值的方法：
 - Ziggurat - 使用 Ziggurat 方法生成高斯随机值；
 - Sum of uniform values - 根据中心极限定理，通过对均匀分布的随机信号进行加法和缩放来生成高斯随机值。该定理指出，足够多的随机变量之和的概率分布趋近于高斯分布。必须设置**求和值数目**参数，该参数决定了需要求和的均匀分布随机数的数量，以生成单个高斯随机值。

对于**方法**参数的两种设置，输出样本均来自由**均值**和**方差**参数定义的正态分布。

**依赖：** 将**源类型**设置为 Gaussian。

</div>
</div>

<div class="details-box">
<details open>
<summary>求和值的数目 - 求和值的数目<div>12（默认）</div></summary>
</details>
<div class="details-content">

需要相加以计算高斯随机分布中单个数字的均匀分布随机值的数量。

**依赖：** 将**源类型**设置为Gaussian并将方法设置为Sum of uniform values。

</div>
</div>

<div class="details-box">
<details open>
<summary>最小值 - 均匀分布的最小值<div>0（默认）| 标量</div></summary>
</details>
<div class="details-content">

均匀分布的最小值，指定为一个有限的标量。

**依赖：** 将**源类型**设置为Uniform。

</div>
</div>

<div class="details-box">
<details open>
<summary>最大值 - 均匀分布的最大值<div>1（默认）| 标量</div></summary>
</details>
<div class="details-content">

均匀分布的最大值，指定为一个有限的标量。

**依赖：** 将**源类型**设置为 Uniform。

</div>
</div>

<div class="details-box">
<details open>
<summary>均值 - 高斯分布的均值<div>0（默认）| 标量</div></summary>
</details>
<div class="details-content">

高斯分布的均值，指定为一个有限的标量。

**依赖：** 将**源类型**设置为 Gaussian。

</div>
</div>

<div class="details-box">
<details open>
<summary>方差 - 高斯分布的方差<div>1（默认）| 标量</div></summary>
</details>
<div class="details-content">

高斯分布的方差，指定为一个有限的标量。

**依赖：** 将**源类型**设置为 Gaussian。

</div>
</div>

<div class="details-box">
<details open>
<summary>可复现性 - 组件输出的可复现性<div>Specify seed (默认) | Not repeatable</div></summary>
</details>
<div class="details-content">

**可复现性**参数决定了模块在每次运行仿真时是否输出相同的信号。可以将该参数设置为以下选项之一：

 - Specify seed - 每次运行仿真时输出相同的信号。每次运行仿真时，模块都会使用在“初始种子”参数中指定的初始种子；
 - Not repeatable - 每次运行仿真时输出不同的信号。每次运行仿真时，模块都会随机选择一个初始种子。

</div>
</div>

<div class="details-box">
<details open>
<summary>初始种子 - 随机数生成器的初始种子<div>1 (默认) | 整数标量</div></summary>
</details>
<div class="details-content">

用于随机数生成器的初始种子，指定为有限标量。每次使用特定的初始种子执行时，生成器都会生成相同的伪随机数序列。在N个通道的输出的情况下，会使用该标量生成 N 个随机值作为 N 通道输出的种子。

**依赖：** 将**可复现性**设置为 Specify seed。

</div>
</div>

<div class="details-box">
<details open>
<summary>采样时间 - 输出采样周期<div>1（默认）| 正实数标量</div></summary>
</details>
<div class="details-content">

随机输出序列的采样周期 Ts，指定为正的有限标量。输出帧周期为 MTs，其中 M 为每帧采样数。

</div>
</div>

<div class="details-box">
<details open>
<summary>每帧采样数 - 输出帧采样数<div>1（默认）| 正整数标量</div></summary>
</details>
<div class="details-content">

每个输出帧中的样本数 M，指定为正整数。输出帧周期为 MTs，其中 Ts 为采样时间。

</div>
</div>


## 版本历史记录

- 在 2025b 推出