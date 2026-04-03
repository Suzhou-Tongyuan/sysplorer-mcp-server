# ColoredNoise
---
&nbsp;

生成有色噪声信号。

**库：** TYDSPSystem / SignalGenerationManipulationAndAnalysis / SignalGeneration

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYDSPSystem/SignalGeneration/SignalGeneration/ColoredNoise/1.png')" style="width: 100px; height: auto; transform: scale(1);">


## 描述

ColoredNoise 模块用于生成有色噪声信号，其整个频率范围内的功率谱密度为 $1/|f|^α$。反向功率谱密度分量 $α$ 可以是区间 [-2 2] 内的任意值。模块生成的有色噪声类型取决于模块对话框中选择的噪声颜色类型。

## 端口

### 输出
<div class="details-box">
<details open>
<summary>y — 有色噪声信号<div>矩阵</div></summary>
</details>
<div class="details-content">

有色噪声输出信号。信号的维度取决于输出通道数以及每个输出通道的采样数。

**数据类型：**  double

</div>
</div>

## 参数
<div class="details-box">
<details open>
<summary>噪声颜色 — 产生噪音的颜色<div>pink（默认） | white | brown | blue | purple | custom</div></summary>
</details>
<div class="details-content">

模块产生的噪音的颜色。可选项有：

 - pink —— 产生粉红噪声。该选项等同于将频率倒数的功率设为 1；

 - white —— 产生白噪声（平坦功率谱密度）。该选项相当于将反向频率的功率设为 0；

 - brown —— 生成棕色噪声。也称为红色或布朗噪声。该选项相当于将反比频率的功率设为 2；

 - blue —— 产生蓝色噪声。也称为蔚蓝色噪音。该选项相当于将反向频率的幂设为-1；

 - purple —— 产生紫色（紫色）噪音。该选项相当于将反向频率的功率设置为-2；

 - custom —— 使用反向频率功率参数指定噪声的功率密度。

</div>
</div>

<div class="details-box">
<details open>
<summary>逆频率的幂 — 指定逆频率的幂<div>1.0（默认） | 实数标量</div></summary>
</details>
<div class="details-content">

逆频率的幂，以实数标量指定。该参数仅在**噪声颜色**参数为 custom 可设置。

</div>
</div>

<div class="details-box">
<details open>
<summary>保证输出是有界的（+1/-1） — 将输出界限设置为 +1 和 -1<div>off（默认） | on</div></summary>
</details>
<div class="details-content">

选择参数，使输出在 +1 和 -1 之间有界。

选择该参数时，产生噪声的内部随机源是均匀的。如果噪声颜色设置为白色，则随机源的输出不会应用颜色滤波器。输出是振幅介于 +1 和 -1 之间的均匀噪声。如果将噪声颜色设置为其他选项，则随机信号源的输出将应用着色滤波器，然后再应用增益，以确保绝对最大输出不超过 1。

不选择该参数时，内部随机源为高斯随机源，输出不受约束。

</div>
</div>

<div class="details-box">
<details open>
<summary>输出通道数 — 输出通道数<div>1（默认） | 正整数标量</div></summary>
</details>
<div class="details-content">

输出通道数，以正整数标量指定。该参数定义了生成信号的列数。

</div>
</div>

<div class="details-box">
<details open>
<summary>每个输出通道的采样数 — 每帧输出采样<div>1024（默认） | 正整数标量</div></summary>
</details>
<div class="details-content">

输出信号每帧的采样数目，以正整数标量指定。该参数定义了生成信号的行数。

</div>
</div>

<div class="details-box">
<details open>
<summary>采样时间 — 采样时间<div>1（默认） | 正实数标量</div></summary>
</details>
<div class="details-content">

输出信号的采样时间，以秒为单位的正标量。

</div>
</div>

<div class="details-box">
<details open>
<summary>随机数种子 — 随机数生成器的初始种子<div>67（默认） | 整数标量</div></summary>
</details>
<div class="details-content">

随机数生成器算法的初始种子，指定为整数标量。

</div>
</div>


## 版本历史记录

- 在 2025b 推出