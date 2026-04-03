# REALIntegratorWithDelay
---
考虑运算放大器非理想特性的离散积分器。

**库：** TYMixedSignal / SDUtilities

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYMixedSignal/SDUtilities/REALIntegratorWithDelay/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

带延迟的实际积分器模块用于建模考虑运算放大器非理想特性的离散积分器，具体包括：饱和效应、有限增益、有限带宽和压摆率（slew rate）的影响。

理想带延迟积分器的 z 域传递函数为：

$$
H(z) = \frac{z^{-1}}{1 - z^{-1}}
$$

实际电路中，积分器的模拟实现会因多种非理想效应偏离理想特性。在开关电容（SC）Σ-Δ 调制器中，性能下降的主要原因之一是 SC 积分器的电荷转移不完全。该非理想效应由运算放大器的非理想特性导致，具体包括：有限增益、有限带宽、压摆率限制和饱和电压。
 

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
<summary>有限增益 — 设置有限增益<div> 正实数标量 </div></summary>
</details>
<div class="details-content">

积分器中运放的开环增益，需考虑积分器反馈因子的影响。


</div>
</div>


<div class="details-box">
<details open>
<summary>饱和 — 饱和电压<div> 正实数标量</div></summary>
</details>
<div class="details-content">

积分器中运放的输出饱和电压，单位为伏特（V）。

</div>
</div>


<div class="details-box">
<details open>
<summary>转换速率 — 转换速率<div> 正实数标量 </div></summary>
</details>
<div class="details-content">

积分器中运放的压摆率（最大转换速率），需考虑负载影响，单位为伏特/微秒（V/µs）。

</div>
</div>


<div class="details-box">
<details open>
<summary>增益带宽 — 增益带宽<div> 正实数标量 </div></summary>
</details>
<div class="details-content">

积分器中运放的增益带宽积，需考虑积分器反馈因子及负载影响，单位为赫兹（Hz）。

</div>
</div>

## 版本历史记录

- 在 2025b 推出
