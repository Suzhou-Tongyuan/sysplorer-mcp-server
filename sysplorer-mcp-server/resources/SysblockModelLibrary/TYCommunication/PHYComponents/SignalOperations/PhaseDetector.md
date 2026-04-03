# PhaseDetector
---
相位检测器。

**库：** TYCommunication / PHYComponents / SignalOperations

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYCommunication/PHYComponents/SignalOperations/PhaseDetector/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

PhaseDetector 模块可以测量两个输入信号之间的相位差值。

## 端口

### 输入
<div class="details-box">
<details open>
<summary>u1 — 输入信号<div>实数标量</div></summary>
</details>
<div class="details-content">

输入信号 u1，与 u2 端口输入信号进行相位差值检测，指定为实数标量。

**数据类型：** double

</div>
</div>

<div class="details-box">
<details open>
<summary>u2 — 输入信号<div>实数标量</div></summary>
</details>
<div class="details-content">

输入信号 u2，与 u1 端口输入信号进行相位差值检测，指定为实数标量。

**数据类型：** double

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>实数标量</div></summary>
</details>
<div class="details-content">
 
输出 u1 与 u2 端口输入信号之间的相位差，以实数标量值的形式返回。

**数据类型：** double

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>实时电荷泵 — 实时电荷泵<div>1.0（默认） | 正实数标量</div></summary>
</details>
<div class="details-content">

实时电荷泵通过精确控制充放电电流，缩小相位差。

</div>
</div>

<div class="details-box">
<details open>
<summary>过零判决 — 过零判决<div>-1.4901e-8（默认） | 实数标量</div></summary>
</details>
<div class="details-content">

过零判决参数确保鉴相器在信号过零时准确触发，避免误判。

</div>
</div>


## 版本历史记录

- 在 2025b 推出