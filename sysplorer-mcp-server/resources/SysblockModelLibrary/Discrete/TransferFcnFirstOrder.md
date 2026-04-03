# TransferFcnFirstOrder
---
&nbsp;

实现离散时间一阶传递函数

**库：** Sysblock 模型库 / Discrete

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/TransferFcnFirstOrder/1.png')" style="width: 100px; height: auto;border: 1px solid black;">

## 描述

TransferFcn First Order 模块实现输入的离散时间一阶传递函数。传递函数具有一个单位 DC 增益。
## 示例

参考示例模型 ：<helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/TransferFcnFirstOrder.mo">TransferFcnFirstOrder.mo</helpButton>

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/TransferFcnFirstOrder/2.png')" style="width: 600px; height: auto;border: 1px solid black;">

**参考结果**

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/TransferFcnFirstOrder/3.png')" style="width: 600px; height: auto;">

## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 数组</div></summary>
</details>
<div class="details-content">

一阶传递函数算法的输入信号。

**数据类型：double | float** 

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 数组</div></summary>
</details>
<div class="details-content">

输出信号，它是具有单位 DC 增益的输入的离散时间一阶传递函数。

**数据类型：double | float** 

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>极点（在 z 平面内）<div>0.95（默认值）| 标量 | 数组</div></summary>
</details>
<div class="details-content">

指定 z 平面内的极点。

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

## 版本历史记录

- 在 2025b 推出

### 限制信息

- 暂不支持 int8、uint8、int16、uint16、int32、uint32、int64、uint64、fixedpoint 类型输入输出；
- 暂无整数舍入模式选项；
- 暂无发生溢出时饱和处理为最大值或最小值选项。