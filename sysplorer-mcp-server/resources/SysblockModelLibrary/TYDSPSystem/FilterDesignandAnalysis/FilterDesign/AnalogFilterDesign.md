# AnalogFilterDesign
---
&nbsp;

设计和实现模拟滤波器。

**库：** TYDSPSystem / FilterDesignandAnalysis / FilterDesign

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYDSPSystem/FilterDesignandAnalysis/FilterDesign/AnalogFilterDesign/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

AnalogFilterDesign 模块用于设计和实现巴特沃斯、切比雪夫 I 型、切比雪夫 II 型、椭圆或贝塞尔滤波器，并支持高通、低通、带通或带阻配置。

可以通过对话框中的**设计方法**和**滤波器类型**下拉列表来选择滤波器的设计方法和频段配置。对于每种设计方法和频段配置的组合，都会显示一组相应的辅助参数。

## 端口

### 输入
<div class="details-box">
<details open>
<summary>u — 输入信号<div>实数标量</div></summary>
</details>
<div class="details-content">

要滤波的输入信号，指定为基于采样的连续时间实值标量值。

**数据类型：** double

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>实数标量</div></summary>
</details>
<div class="details-content">
 
滤波后的信号，以实数标量值的形式返回。

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>设计方法 — 滤波器设计<div>Butterworth（默认）| Chebyshev I | Chebyshev II | Elliptic | Bessel</div></summary>
</details>
<div class="details-content">

滤波器的设计方法有：

 - Butterworth —— 巴特沃斯滤波器的幅值响应在通带内是最大平坦的，总体上是单调的。巴特沃斯设计使用工具箱函数 butter；
 - Chebyshev I —— 切比雪夫 I 型滤波器的幅值响应在通带内是等平的，在阻带内是单调的。切比雪夫 I 设计使用了工具箱函数 cheby1；
 - Chebyshev II —— 切比雪夫 II 滤波器的幅值响应在通带内是单调的，在阻带内是等涟波的。Chebyshev II 设计使用工具箱函数 cheby2；
 - Elliptic —— 椭圆滤波器的幅值响应在通带和阻带都是等涟波的。椭圆设计使用工具箱函数 ellip；
 - Bessel —— 贝塞尔滤波器的幅值响应在通带是最大平坦的，总体上是单调的。滤波器具有最大平坦线性相位响应。贝塞尔设计使用函数 besself。

</div>
</div>

<div class="details-box">
<details open>
<summary>滤波器类型 — 滤波器类型<div>Lowpass（默认）| Highpass | Bandpass | Bandstop</div></summary>
</details>
<div class="details-content">

要设计的滤波器类型：

 - Lowpass
 - Highpass
 - Bandpass
 - Bandstop

</div>
</div>

<div class="details-box">
<details open>
<summary>滤波器阶数 — 滤波器阶数<div>8（默认）| 正整数标量</div></summary>
</details>
<div class="details-content">

滤波器类型设置为以下时的滤波器阶数：
 - Lowpass
 - Highpass

当滤波器类型设置为以下时，滤波器阶数为两倍：
 - Bandpass
 - Bandstop

</div>
</div>

<div class="details-box">
<details open>
<summary>通带截止频率（rad/s） — 通带截止频率<div>30（默认）| 正实数标量</div></summary>
</details>
<div class="details-content">

通带截止频率，单位为 rad/s。

</div>
</div>

<div class="details-box">
<details open>
<summary>下通带截止频率（rad/s） — 下通带截止频率<div>30（默认）| 正实数标量</div></summary>
</details>
<div class="details-content">

下通带截止频率，单位为 rad/s。

</div>
</div>


<div class="details-box">
<details open>
<summary>上通带截止频率（rad/s） — 上通带截止频率<div>80（默认）| 正实数标量</div></summary>
</details>
<div class="details-content">

上通带截止频率，单位为 rad/s。

</div>
</div>

<div class="details-box">
<details open>
<summary>通带波纹（dB） — 指定通带波纹<div>2（默认）| 正实数标量</div></summary>
</details>
<div class="details-content">

指定通带波纹，单位为 dB。

</div>
</div>


<div class="details-box">
<details open>
<summary>阻带衰减（dB） — 指定阻带衰减<div>40（默认）| 正实数标量</div></summary>
</details>
<div class="details-content">

指定阻带衰减，单位为 dB。

</div>
</div>


## 版本历史记录

- 在 2025b 推出