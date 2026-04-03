# JitteredSineWave
---

产生具有采样抖动的正弦波。

**库：** TYMixedSignal / SDUtilities

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYMixedSignal/SDUtilities/JitteredSineWave/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

带抖动的正弦波模块用于生成带有采样时钟抖动（jitter）的正弦信号，其信号导数通过解析方式计算。

开关电容（SC）电路的性能依赖于每个时钟相位期间电荷的完全转移。当模拟信号被采样后，SC电路即成为采样数据系统，此时时钟周期的变化不会直接影响电路性能。因此，时钟抖动对SC电路的影响可通过分析其对输入信号采样的影响来完全描述。这也意味着时钟抖动对 Σ-Δ 调制器的影响与调制器结构或阶数无关。时钟抖动会导致非均匀采样时间序列，并产生误差，该误差会增大量化器输出的总误差功率。误差大小既取决于抖动的统计特性，也与调制器输入信号相关。

## 端口

### 输出

<div class="details-box">
<details open>
<summary>y — 输出具有抖动的正弦波 <div>实数标量</div></summary>
</details>
<div class="details-content">
 
输出具有抖动的正弦波信号，信号的倒数是解析计算的。

**数据类型：** double

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>幅值 — 设置幅值<div> 正实数数标量 </div></summary>
</details>
<div class="details-content">

正弦信号的幅值，单位为伏特（V）。

</div>
</div>


<div class="details-box">
<details open>
<summary>偏置 — 设置偏置<div> 正实数数标量 </div></summary>
</details>
<div class="details-content">

正弦信号的直流偏置值，单位为伏特（V）。


</div>
</div>


<div class="details-box">
<details open>
<summary>频率 — 设置频率<div> 正实数标量 </div></summary>
</details>
<div class="details-content">

正弦信号的频率，单位为弧度/秒（rad/s）。

</div>
</div>


<div class="details-box">
<details open>
<summary>相位 — 设置相位<div> 正实数标量 </div></summary>
</details>
<div class="details-content">

正弦信号的初始相位，单位为弧度（rad）。

</div>
</div>


<div class="details-box">
<details open>
<summary>采样抖动 — 设置采样抖动 PSD<div> 正实数标量 </div></summary>
</details>
<div class="details-content">

样时钟抖动的均方根值（RMS），单位为秒（s）。

</div>
</div>

<div class="details-box">
<details open>
<summary>采样周期 — 设置采样周期<div> 正实数标量 </div></summary>
</details>
<div class="details-content">

采样信号的周期，单位为秒（s）（Ts = 1/fs，fs 为采样频率）。

</div>
</div>


<div class="details-box">
<details open>
<summary>随机数种子 — 设置随机数种子 PSD<div> 整数标量 </div></summary>
</details>
<div class="details-content">

随机数生成器种子（不同种子保证不同模块的随机序列无相关性）。

</div>
</div>

## 版本历史记录

- 在 2025b 推出
