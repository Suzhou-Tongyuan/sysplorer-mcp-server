# TransferFcnLeadorLeg
---
&nbsp;

实现离散时间超前或滞后补偿器

**库：** Sysblock 模型库 / Discrete

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/TransferFcnLeadorLeg/1.png')" style="width: 100px; height: auto;border: 1px solid black;">

## 描述

模块实现输入的离散时间超前或滞后补偿器。补偿器的即时增益为 1，DC 增益等于 (1-z)/(1-p)，其中 z 是零点，p 是补偿器的极点。该模块在 0<z<p<1 时实现一个超前补偿器，在 0<p<z<1 时实现一个滞后补偿器。

## 示例

参考示例模型 ：<helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/TransferFcnLeadorLeg.mo">TransferFcnLeadorLeg.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/TransferFcnLeadorLeg/2.png')" style="width: 600px; height: auto;border: 1px solid black;">

**参考结果**

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/TransferFcnLeadorLeg/3.png')" style="width: 600px; height: auto;">

## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 数组</div></summary>
</details>
<div class="details-content">

模块对其应用离散时间超前或滞后补偿的输入信号。

**数据类型：double | float** 

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 数组</div></summary>
</details>
<div class="details-content">

作为输入符号的离散时间超前或滞后补偿的输出信号。

**数据类型：double | float** 

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>补偿器的极点（在 z 平面内）<div>0.95（默认值）| 标量</div></summary>
</details>
<div class="details-content">

指定 z 平面内的极点。

</div>
</div>

<div class="details-box">
<details open>
<summary>补偿器的零点（在 z 平面内）<div>0.75（默认值）| 标量</div></summary>
</details>
<div class="details-content">
指定 z 平面内的零点。


</div>
</div>

<div class="details-box">
<details open>
<summary>上一输出的初始条件<div>0.0（默认值）| 标量 | 数组 </div></summary>
</details>
<div class="details-content">

指定上一输出的初始条件。

</div>
</div>

<div class="details-box">
<details open>
<summary>上一输入的初始条件<div>0.0（默认值）| 标量 | 数组 </div></summary>
</details>
<div class="details-content">

指定上一输入的初始条件。

</div>
</div>

## 版本历史记录

- 在 2025b 推出

### 限制信息

- 暂不支持 int8、uint8、int16、uint16、int32、uint32、int64、uint64、fixedpoint 类型输入输出；
- 暂无整数舍入模式选项；
- 暂无发生溢出时饱和处理为最大值或最小值选项。