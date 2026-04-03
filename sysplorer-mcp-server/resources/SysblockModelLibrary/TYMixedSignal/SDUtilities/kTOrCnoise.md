# kTOrCnoise
---
对开关电容 $C_{s}$ 的 kT/C 噪声进行建模。

**库：** TYMixedSignal / SDUtilities

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYMixedSignal/SDUtilities/kTOrCnoise/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

热噪声由载流子的热运动引起的随机涨落产生，即使在平衡状态下也存在。其频谱为白色噪声，带宽仅受限于开关电容的时间常数或运算放大器的带宽。开关电容（SC）Σ-Δ 调制器的采样电容 $C_{s}$ 与有限导通电阻 Ron 的开关串联，开关周期性导通时将噪声电压采样到 $C_{s}$ 上。

Sigma-Delta 调制器的积分器或谐振器可以包括多个开关电容输入支路，每个支路都对总噪声功率有贡献。每个分支都必须使用单独的 kTOrCnoise 模块进行建模。
 

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
<summary>采样电容 — 设置采样电容值<div> 正实数标量</div></summary>
</details>
<div class="details-content">

采样电容 $C_s$ 的容值，单位为法拉（F）。

</div>
</div>


<div class="details-box">
<details open>
<summary>绝对温度 — 设置系统工作绝对温度值<div> 正实数标量</div></summary>
</details>
<div class="details-content">

设置系统工作绝对温度，单位为开尔文（K）。

</div>
</div>


<div class="details-box">
<details open>
<summary>Boltzman 常数 — Boltzman 常数 <div> 1.38 x 10^-23 J/K |正实数标量</div></summary>
</details>
<div class="details-content">

物理常数，用于计算热噪声功率，用户可根据实际环境调整。

</div>
</div>


<div class="details-box">
<details open>
<summary>随机数种子 — 随机数种子 <div> 整数标量</div></summary>
</details>
<div class="details-content">

设置随机数种子，确保多次仿真中噪声序列的独立性。

</div>
</div>


## 版本历史记录

- 在 2025b 推出