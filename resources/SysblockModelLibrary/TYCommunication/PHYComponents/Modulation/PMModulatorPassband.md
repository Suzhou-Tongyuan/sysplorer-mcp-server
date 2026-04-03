# PMModulatorPassband
---
使用相位调制进行调制。

**库：** TYCommunication / PHYComponents / Modulation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYCommunication/PHYComponents/Modulation/PMModulatorPassband/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

PM 调制器通带模块采用相位调制方式对信号进行调制，其输出为已调信号的带通表示形式。输出信号的频率会随输入信号的幅值变化而变化，输入和输出信号均为实标量信号。


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>实数标量</div></summary>
</details>
<div class="details-content">

输入信号，指定为一个实数标量值。

**数据类型：** double

</div>
</div>



### 输出

<div class="details-box">
<details open>
<summary>y — 输出相位调制后的信号<div>实数标量</div></summary>
</details>
<div class="details-content">
 
输出相位调制后的信号。

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>载频 (Hz) — 以 Hz 为单位的载波频率<div>300（默认）| 正标量</div></summary>
</details>
<div class="details-content">

以 Hz 为单位的载波频率，指定为正标量。需确保载波频率 fc 与对应的 PM 解调器通带模块相匹配。

通常情况下，合适的载波频率应远高于输入信号的最高频率。根据奈奎斯特采样定理，1/Ts > (2×fc)，其中 Ts 表示输入信号的采样时间。

</div>
</div>


<div class="details-box">
<details open>
<summary>初始相位 (rad) — 以弧度为单位的初始相位偏移<div>0（默认）| 实数标量</div></summary>
</details>
<div class="details-content">

载波的初始相位偏移（以弧度为单位），指定为实数标量。

</div>
</div>


<div class="details-box">
<details open>
<summary>相位偏差 (rad) — 以弧度为单位的载波频率相位偏差<div>pi/2（默认）| 实数标量</div></summary>
</details>
<div class="details-content">

以弧度为单位的载波频率相位偏差，指定为实数标量。

</div>
</div>



## 版本历史记录

- 在 2025b 推出

