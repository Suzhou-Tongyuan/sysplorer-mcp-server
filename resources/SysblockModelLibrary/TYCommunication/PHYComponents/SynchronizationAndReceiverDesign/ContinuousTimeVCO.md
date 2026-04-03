# ContinuousTimeVCO
---
实现连续时间压控振荡器。

**库：** TYCommunication / PHYComponents / SynchronizationAndReceiverDesign

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYCommunication/PHYComponents/SynchronizationAndReceiverDesign/ContinuousTimeVCO/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

ContinuousTimeVCO 模块产生一个与输入信号成比例的由静态频率参数指定的频率偏移信号。

## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>实数标量</div></summary>
</details>
<div class="details-content">

输入信号，指定为实数标量。

**数据类型：** double

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>实数标量</div></summary>
</details>
<div class="details-content">
 
输出频率偏移信号，以实数标量值的形式返回。

**数据类型：** double

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>输出振幅 — 指定输出振幅<div>1.0（默认） | 正实数标量</div></summary>
</details>
<div class="details-content">

指定输出频率偏移信号的幅值。

</div>
</div>

<div class="details-box">
<details open>
<summary>静止频率 — 指定静止频率<div>10.0（默认） | 正实数标量</div></summary>
</details>
<div class="details-content">

输入信号为零时振荡器输出的频率。

</div>
</div>

<div class="details-box">
<details open>
<summary>输入灵敏度 — 指定输入灵敏度<div>1.0（默认）| 正实数标量</div></summary>
</details>
<div class="details-content">

该参数值与输入电压成比例，因此与静态频率值的位移成比例。输入灵敏度的单位是赫兹每伏特。

</div>
</div>

<div class="details-box">
<details open>
<summary>初始相位 — 指定初始相位<div>0（默认）| 实数标量</div></summary>
</details>
<div class="details-content">

指定振荡器的初始相位，单位为弧度。

</div>
</div>


## 版本历史记录

- 在 2025b 推出