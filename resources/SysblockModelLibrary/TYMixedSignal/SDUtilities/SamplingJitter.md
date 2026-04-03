# SamplingJitter
---
模拟输入信号的采样抖动。

**库：** TYMixedSignal / SDUtilities

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYMixedSignal/SDUtilities/SamplingJitter/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

开关电容电路的运行依赖于每个时钟相位期间电荷的完全转移。一旦模拟信号被采样，开关电容电路就成为一个采样数据系统，此时时钟周期的变化不会对该电路性能产生直接影响。因此，开关电容电路中时钟抖动的影响，完全可以通过计算其对输入信号采样的影响来描述。这也意味着，时钟抖动对 Sigma-Delta 调制器的影响与调制器的结构或阶数无关。时钟抖动会导致采样时间序列不均匀，并产生误差，该误差会增加量化器输出端的总误差功率。此误差的大小既取决于抖动的统计特性，也取决于调制器的输入信号。

可以通过将误差添加到输入信号中，在行为级对该效应进行仿真模拟。采用数值计算方法求出输入信号的导数 dx(t)/dt。对于正弦输入信号，最好使用 JitteredSineWave 模块，因为它更为精确。
 

## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 信号输入<div>实数标量</div></summary>
</details>
<div class="details-content">

信号输入。

**数据类型：** double

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>y — 信号输出<div>实数标量</div></summary>
</details>
<div class="details-content">

信号输出。

**数据类型：** double

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>采样时间 — 设置模块采样时间<div> 正实数标量 </div></summary>
</details>
<div class="details-content">

信号的采样周期，单位为秒（s）。

</div>
</div>


<div class="details-box">
<details open>
<summary>采样抖动 — 设置采样抖动<div> 正实数标量</div></summary>
</details>
<div class="details-content">

采样抖动的均方根值（RMS），单位为秒（s）。

</div>
</div>


<div class="details-box">
<details open>
<summary>随机数种子 — 设置随机数种子<div> 整数标量</div></summary>
</details>
<div class="details-content">

在使用随机数生成器的不同模块中使用不同的种子，可确保生成的随机序列互不相关。

</div>
</div>


## 版本历史记录

- 在 2025b 推出