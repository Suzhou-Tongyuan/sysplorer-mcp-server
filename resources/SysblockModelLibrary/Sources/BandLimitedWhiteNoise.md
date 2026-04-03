# BandLimitedWhiteNoise
---
生成适合在连续系统或混合系统中使用的正态分布随机数

**库：** Sysblock模块库 / Sources

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/BandLimitedWhiteNoise/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

BandLimitedWhiteNoise 模块生成适合在连续系统或混合系统中使用的正态分布随机数。

### 白噪声仿真

从理论上讲，连续白噪声的相关时间为 0，功率谱密度 (PSD) 呈水平状态，总能量为无穷大。在实践中，物理系统永远不受白噪声干扰，尽管当噪声干扰的相关时间相对于系统的自然带宽非常小时，白噪声是很有用的理论逼近。

在 Sysplorer 软件中，您可以使用相关时间比系统的最短时间常数小很多的随机序列来仿真白噪声的作用。BandLimitedWhiteNoise 模块就生成这样的序列。噪声的相关时间是指模块的采样率。要进行准确的仿真，请使用比系统的最快动态小很多的相关时间。您可以通过指定以下方程来获得满意的结果：

tc ≈ 1 ⁄ (100 fₘₐₓ) × 2π ，

其中 fₘₐₓ 是以弧度/秒为单位的系统带宽。

### 与 RandomNumber 模块的比较

此模块与 RandomNumber 模块之间的主要区别在于，BandLimitedWhiteNoise 模块以特定的采样率生成输出。此采样率与噪声的相关时间有关。

<!-- ### 与 Averaging Power Spectral Density 模块一起使用

Band-Limited White Noise 模块指定双边频谱，其单位为赫兹。Averaging Power Spectral Density 模块指定单边频谱，其单位为每单位径向频率幅值的平方：mag^2/(rad/sec)。当您将 Band-Limited White Noise 模块的输出馈入 Averaging Power Spectral Density 模块时，平均 PSD 值比 Band-Limited White Noise 模块的**噪声功率**小 π 倍。这种差异是模块之间的单位转换造成的，即 1/(1/2)(2`π`) = 1/`π`，其中：

- 1/2 是从双边频谱转换为单边频谱的因子。
- 2`π` 是从赫兹转换为弧度/秒的因子。 -->

## 示例

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/BandLimitedWhiteNoise.mo">BandLimitedWhiteNoise.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/BandLimitedWhiteNoise/2.png')" style="width: 500px; height: auto; transform: scale(1);border-top: 1px solid black;">

### 示例说明

- BandLimitedWhiteNoise 模块：生成带限白噪声信号。模块参数包括噪声的功率、采样时间和种子。示例中，该模块按照指定的参数生成带限白噪声信号；
- Scope 模块：显示输入信号曲线。示例中，Scope 模块显示 BandLimitedWhiteNoise 模块生成的噪声信号。

### 仿真结果

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/BandLimitedWhiteNoise/3.png')" style="width: 450px; height: auto; transform: scale(1);border-top: 1px solid black;">

## 端口

### 输出

<div class="details-box">
<details open>
<summary>outport — 正态分布的随机数<div>标量 | 向量 | 矩阵 | N 维数组</div></summary>
</details>
<div class="details-content">

正态分布的随机数，指定为标量、向量、矩阵或 N 维数组。

**数据类型：** double

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>噪声功率 — 白噪声的 PSD 高度<div>0.1 (默认) | 标量 | 向量 | 矩阵 | N 维数组</div></summary>
</details>
<div class="details-content">

将白噪声的 PSD 高度指定为正值的标量、向量、矩阵或 N 维数组。

</div>
</div>


<div class="details-box">
<details open>
<summary>采样时间 — 噪声的相关时间<div>0.1 (默认) | 标量 | 向量</div></summary>
</details>
<div class="details-content">

噪声的相关时间。有关详细信息，请参阅[指定采样时间](/Doc/Sysblock/Modeling/ConfigureSignals/SampleTime/SpecifyTime.html)。

</div>
</div>

<div class="details-box">
<details open>
<summary>种子 — 起始种子<div>23341 (默认) | 标量 | 向量 | 矩阵 | N 维数组</div></summary>
</details>
<div class="details-content">

将随机数生成器的起始种子指定为标量、向量、矩阵或 N 维数组。值必须是有限的正实数值。

</div>
</div>

<!-- ### **将向量参数解释为一维向量** — 将向量参数视为一维 `on` (默认) | `off`


当模块参数为向量时，选择此选项将输出一维数组。否则，将输出二维数组，其中一个维度为 `1`。有关详细信息，请参阅 [确定源模块的输出维度](https://ww2.mathworks.cn/help/simulink/ug/determining-output-signal-dimensions.html#bsud_ek-4)。 -->


## 算法

要为此噪声生成正确的强度，需要对噪声的协方差进行缩放，以反映从连续 PSD 向离散噪声协方差的隐式转换。合适的缩放因子为 1 / tc，其中 tc 是噪声的相关时间。这种缩放可以确保连续系统对近似白噪声的响应与系统对真实白噪声的响应具有相同的协方差。这种缩放导致 BandLimitedWhiteNoise 模块的信号协方差与**噪声功率**（强度）参数不相同。此参数实际上是白噪声的 PSD 高度。此模块将白噪声的协方差近似为**噪声功率**除以 tc。

::: warning 注意 
此模块不能在触发子系统层次结构中使用。
:::

## 版本历史记录

- 在 2025a 推出

### 限制信息

1. 暂不支持与 AveragingPowerSpectralDensity 模块一起使用；
2. 暂不支持将向量参数解释为一维向量的复选框。

## 另请参阅

### 主题

- [采样时间](/Doc/Sysblock/Modeling/ConfigureSignals/SampleTime/SampleTime_Main.html)