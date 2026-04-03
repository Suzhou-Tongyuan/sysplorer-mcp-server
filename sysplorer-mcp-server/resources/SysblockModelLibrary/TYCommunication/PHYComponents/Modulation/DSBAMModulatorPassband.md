# DSBAMModulatorPassband
---
利用双边带调幅进行调制

**库：** TYCommunication / PHYComponents / Modulation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYCommunication/PHYComponents/Modulation/DSBAMModulatorPassband/1.png')" style="width: 150px; height: auto; transform: scale(1);">

## 描述

DSBAMModulatorPassband 模块使用双边带幅度调制进行调制。输出是调制信号的通带表示。输入和输出信号都是实标量信号。如果输入是 $u(t)$作为时间 t 的函数，则输出是：

$（u（t）+k）cos（2πfct+θ）$，其中：

* k 是输入信号偏移参数。

* fc 是载波频率参数。

* θ 是初始相位参数。

通常将 k 的值设置为输入信号 $u(t)$ 负部分的最大绝对值。通常，适当的载波频率值远高于输入信号的最高频率。根据奈奎斯特采样定理，模型采样时间的倒数（由模型的信号源定义）必须超过载波频率参数的两倍。此块仅适用于 double 类型的实际输入。此块在触发的子系统内不起作用。

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

**数据类型：** double

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>输入信号延迟 — 输入信号的偏移量<div>1 （默认） | 正整数</div></summary>
</details>
<div class="details-content">

偏移系数 k 。该值应大于或等于输入信号最小值的绝对值。

</div>
</div>

<div class="details-box">
<details open>
<summary>载波频率(Hz) — 输入信号的载波频率<div>300 （默认） | 正实数</div></summary>
</details>
<div class="details-content">

载波的频率。

</div>
</div>

<div class="details-box">
<details open>
<summary>初始相位 (rad) — 载波的初始相位<div>0 （默认） | 实数</div></summary>
</details>
<div class="details-content">

载波的初始相位。

</div>
</div>

## 版本历史记录

- 在 2026b 推出


