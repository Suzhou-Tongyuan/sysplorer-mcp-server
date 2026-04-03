# Chirp
---
&nbsp;

产生扫频余弦（chirp）信号。

**库：** TYDSPSystem / SignalGenerationManipulationAndAnalysis / SignalGeneration

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYDSPSystem/SignalGeneration/SignalGeneration/Chirp/1.png')" style="width: 100px; height: auto; transform: scale(1);border:black 1px solid;">

## 描述

Chirp 模块输出振幅统一、相位连续的扫频余弦（chirp）信号。要指定所需的输出 chirp 信号，必须定义其瞬时频率函数，也称为输出频率扫描。频率扫描可以是线性、二次或对数，默认情况下每扫描一次重复一次。


## 端口

### 输出

<div class="details-box">
<details open>
<summary>y — 输出扫频余弦（chirp）信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

扫频余弦（chirp）信号。在线性、对数和二次模式下（由频率扫描参数设置），模块输出扫频余弦信号，其瞬时频率值由频率和时间参数指定。在扫频余弦模式下，模块输出扫频余弦，其线性瞬时输出频率可能与频率和时间参数指定的频率不同。

**数据类型：** double

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>频率扫描 — 频率扫描类型<div>Linear（默认） | Swept cosine | Logarithmic | Quadratic</div></summary>
</details>
<div class="details-content">

输出瞬时频率扫描的类型，即 fi(t)： 线性、对数、二次或余弦扫频。

如果需要线性扫频的啁啾信号，建议使用线性扫频。虽然余弦扫频也能产生线性扫频的啁啾信号，但输出可能会有意外的频率内容。

目标时间的余弦扫频值不一定是目标频率。这是因为用户指定的扫频并非扫频余弦输出的实际扫频，如扫频余弦扫频的输出计算方法中所述。

在余弦扫频模式下，请勿将参数设置为 $1/T_{sw}$ 远大于初始频率和目标频率参数值。在这种情况下，余弦扫频的实际频率内容可能更接近 $1/T_{sw}$，远远超过初始频率和目标频率参数值。

</div>
</div>

<div class="details-box">
<details open>
<summary>扫描方式 — 扫描方式<div>Unidirectional（默认）| Bidirectional</div></summary>
</details>
<div class="details-content">

扫频模式参数决定扫频是单向还是双向，这将影响输出频率扫频的形状。

</div>
</div>

<div class="details-box">
<details open>
<summary>初始频率 — 初始频率<div>1000（默认） | 正实数标量</div></summary>
</details>
<div class="details-content">

对于线性扫描、二次扫描和余弦扫描，输出啁啾信号的初始频率 f0。您可以将初始频率 (Hz) 指定为大于或等于零的标量。对于对数扫描，初始频率比扫描的实际初始频率小一。此外，当扫描为对数扫描时，必须将初始频率设置为小于目标频率。

</div>
</div>

<div class="details-box">
<details open>
<summary>目标频率 — 目标频率<div>4000（默认） | 正实数标量</div></summary>
</details>
<div class="details-content">

对于线性、二次和对数扫描，目标时间 $t_g$ 时输出的瞬时频率 $f_i(t_g)$。您可以将目标频率 (Hz) 指定为大于或等于零的标量。对于余弦扫频，目标频率是目标时间 $t_g/2$ 的一半时的输出瞬时频率。频率扫描为对数扫描时，目标频率必须大于初始频率。

</div>
</div>

<div class="details-box">
<details open>
<summary>目标时间 — 扫频的目标时间<div>1（默认） | 正实数标量</div></summary>
</details>
<div class="details-content">


对于线性、二次和对数扫频，目标时间 $t_g/2$ 是扫频达到目标频率 $f_i(t_g)$ 的时间。对于余弦扫频，目标时间是扫频达到 $f_i(t_g) - f_0$ 的时间。目标时间必须是一个大于或等于零的标量，且小于或等于扫频时间，$T_{sw}≥t_g$。

</div>
</div>

<div class="details-box">
<details open>
<summary>扫频时间 — 扫频时间<div>1（默认） | 正实数标量</div></summary>
</details>
<div class="details-content">

在单向扫频模式下，扫频时间 Tsw 是输出频率扫频的周期。在双向扫频模式下，扫频时间是输出频率扫频周期的一半。扫频时间必须是大于或等于目标时间的标量，$T_{sw}≥t_g$。

</div>
</div>


<div class="details-box">
<details open>
<summary>初始相位 — 余弦输出的初始相位<div>0（默认） | 实数标量</div></summary>
</details>
<div class="details-content">

仿真时间为零为时余弦输出的相位 $ϕ_0$；$y_{chirp}(t)=cos(ϕ_)0$。可以将初始相位（rad）指定为大于或等于零的标量。

</div>
</div>

<div class="details-box">
<details open>
<summary>采样时间 — 输出采样周期<div>1/8000（默认） | 正实数标量</div></summary>
</details>
<div class="details-content">

输出的采样周期 $T_{S'}$。输出帧周期为 $M_OT_{S'}$，其中 $M_O$ 是每帧的采样次数。

</div>
</div>

<div class="details-box">
<details open>
<summary>每帧采样数 — 每帧采样数<div>1（默认） | 正整数标量</div></summary>
</details>
<div class="details-content">

每帧输出缓冲的采样个数（$M_{O'}$），以正整数标量指定。

</div>
</div>


## 版本历史记录

- 在 2025b 推出