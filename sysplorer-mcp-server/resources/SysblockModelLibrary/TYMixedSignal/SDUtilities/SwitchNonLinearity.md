# SwitchNonLinearity
---
对采样开关的非线性导通电阻进行建模。

**库：** TYMixedSignal / SDUtilities

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYMixedSignal/SDUtilities/SwitchNonLinearity/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

SwitchNonLinearity 模块可以对采样开关的非线性导通电阻进行建模，其假设采用由尺寸相同的N型金属氧化物半导体（N-MOS）晶体管和P型金属氧化物半导体（P-MOS）晶体管组成的互补型互补金属氧化物半导体（CMOS）开关。


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
<summary>采样电容 — 设置采样电容<div> 正实数标量</div></summary>
</details>
<div class="details-content">

采样电容 $C_s$ 的数值，单位为法拉（F）。

</div>
</div>


<div class="details-box">
<details open>
<summary>正电源电压 — 正电源电压<div> 正实数标量</div></summary>
</details>
<div class="details-content">

用于驱动开关中 N-MOS 晶体管栅极的正电源电压值（$V_{DD}$），单位为伏特（V）。

</div>
</div>


<div class="details-box">
<details open>
<summary>负电源电压 — 负电源电压<div> 负实数标量</div></summary>
</details>
<div class="details-content">

用于驱动开关中 P-MOS 晶体管栅极的负电源电压值（$V_{SS}$），单位为伏特（V）。

</div>
</div>


<div class="details-box">
<details open>
<summary>晶体管尺寸 — 晶体管尺寸<div> 正实数标量</div></summary>
</details>
<div class="details-content">

开关中 N-MOS 和 P-MOS 晶体管的宽长比（$W/L$）数值。

</div>
</div>


<div class="details-box">
<details open>
<summary>N-MOS 增益因子 — N-MOS 增益因子<div> 正实数标量</div></summary>
</details>
<div class="details-content">

开关中 N-MOS 晶体管的增益因子（$K'_N = \mu_N C_{ox}$），单位为安培每平方伏特（A/V²）。

</div>
</div>


<div class="details-box">
<details open>
<summary>P-MOS 增益因子 — P-MOS 增益因子<div> 正实数标量</div></summary>
</details>
<div class="details-content">

开关中 P-MOS 晶体管的增益因子（$K'_P = \mu_P C_{ox}$），单位为安培每平方伏特（A/V²）。

</div>
</div>


<div class="details-box">
<details open>
<summary>N-MOS 阈值电压 — N-MOS 阈值电压<div> 正实数标量</div></summary>
</details>
<div class="details-content">

开关中 N-MOS 晶体管的阈值电压（$V_{thN}$），单位为伏特（V）。

</div>
</div>

<div class="details-box">
<details open>
<summary>P-MOS 阈值电压 — P-MOS 阈值电压<div> 正实数标量</div></summary>
</details>
<div class="details-content">

开关中P-MOS晶体管的阈值电压（$V_{thP}$），单位为伏特（V）。

</div>
</div>


<div class="details-box">
<details open>
<summary>自举因子 — 自举因子<div> 正实数标量</div></summary>
</details>
<div class="details-content">

开关自举效率值（$BS$），取值范围为0（无自举）至1（理想自举）。

</div>
</div>


## 版本历史记录

- 在 2025b 推出