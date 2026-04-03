# IDEALIntegratorNoDelay
---
在考虑运算放大器饱和的情况下，建立理想非延迟的离散积分器模型。

**库：** TYMixedSignal / SDUtilities

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYMixedSignal/SDUtilities/IDEALIntegratorNoDelay/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

IDEALIntegratorNoDelay 模块是考虑运放饱和的非延迟离散积分器的模型。

在 z 域中实现的传递函数为

$$
H(z) = \frac{1}{1 - z^{-1}}
$$

利用积分器反馈回路内的饱和块对运算放大器的饱和电平进行建模。
 

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
<summary>饱和 — 饱和电压<div> 正实数标量</div></summary>
</details>
<div class="details-content">

积分器中运放的输出饱和电压，单位为伏特（V）。

</div>
</div>


## 版本历史记录

- 在 2025b 推出