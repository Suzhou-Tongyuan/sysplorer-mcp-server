# AveragingPowerSpectralDensity
---
绘制输入信号的平均功率谱密度（PSD）。

**库：** Sysblock模块库 / Sinks

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sinks/AveragingPowerSpectralDensity/1.png')" style="width: 100px; height: auto; transform: scale(1);border:black 1px solid;">

## 描述

AveragingPowerSpectralDensity 模块绘制输入信号的平均功率谱密度（PSD）。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sinks/AveragingPowerSpectralDensity/2.png')" style="width:450px;border:black 1px solid;"> 

AveragingPowerSpectralDensity 模块有一个输入端口，可实时绘制一个实数输入信号的平均功率谱密度，该模块接受实数标量输入信号。


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量</div></summary>
</details>
<div class="details-content">

输入信号，指定为实数标量。

**数据类型：** double 

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>缓冲区长度 — 指定缓冲区长度<div>128（默认） | 正整数标量</div></summary>
</details>
<div class="details-content">

缓冲区长度，以正整数标量指定。缓冲区长度应大于绘图时数据点数。

</div>
</div>


<div class="details-box">
<details open>
<summary>FFT 点数 — 指定 FFT 点数<div>512（默认） | 正整数标量</div></summary>
</details>
<div class="details-content">

FFT 点数，以正整数标量指定。

</div>
</div>


<div class="details-box">
<details open>
<summary>绘图时数据点数 — 指定绘图时数据点数<div>64（默认） | 正整数标量</div></summary>
</details>
<div class="details-content">

绘图时数据点数，以正整数标量指定。绘图时数据点数应小于缓冲区长度。

</div>
</div>


<div class="details-box">
<details open>
<summary>采样时间 — 采样时间<div>0.1（默认） | 正实数标量</div></summary>
</details>
<div class="details-content">

模块输入端口的采样时间，指定为以秒为单位的正实数标量。

</div>
</div>


## 版本历史记录

- 在 2025b 推出
