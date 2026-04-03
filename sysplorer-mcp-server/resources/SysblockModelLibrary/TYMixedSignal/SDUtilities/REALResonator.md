# REALResonator
---
考虑运算放大器饱和、有限增益、有限带宽和摆幅率，对一个真实的带延迟的离散谐振器进行建模。

**库：** TYMixedSignal / SDUtilities

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYMixedSignal/SDUtilities/REALResonator/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

RealResonator 模块考虑运算放大器饱和、有限增益、有限带宽和摆幅率等因素，对具有延迟的真实离散谐振器进行建模。

具有延迟的理想谐振器的 z 域传递函数为

$$
H(z) = \frac{z^{-2}}{1 + z^{-2}}
$$

由于几种非理想效应，谐振器的模拟电路实现偏离了这种理想行为。开关电容（SC） Sigma-Delta 调制器性能下降的主要原因之一是SC谐振器中电荷的不完全转移。这种非理想效应是运算放大器非理想性的结果，即有限的增益和带宽、摆压率和饱和电压。
 

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

考虑到积分器反馈因子，积分器中使用的运算放大器的增益。


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
