# IDEALResonator
---
建立考虑运放饱和的离散谐振器延迟模型。

**库：** TYMixedSignal / SDUtilities

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYMixedSignal/SDUtilities/IDEALResonator/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

IDEALResonator 模块模拟了一个考虑运算放大器饱和的延迟离散谐振器。

在 z 域中实现的传递函数为

$$
H(z) = \frac{z^{-2}}{1 + z^{-2}}
$$

使用谐振器反馈回路内的饱和模块来模拟运算放大器的饱和电平。
 

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