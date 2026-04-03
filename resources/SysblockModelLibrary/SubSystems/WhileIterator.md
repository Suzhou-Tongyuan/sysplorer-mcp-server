# WhileIterator

While 子系统的控制模块

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SubSystems/WhileIterator/WhileIterator1.png')" style="width: 100px; height: auto; transform: scale(1);border:solid 1px black;">

**库：** Sysblock / SubSystem

## 描述

将 While Iterator 模块置于 Subsystem 中，那么该子系统会成为原子子系统。并且当输入条件的值为 true 时，在当前时间步中，子系统里的模块将重复执行。

## 示例

**示例模型**

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SubSystems/WhileIterator.mo">WhileIterator.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SubSystems/WhileIterator/WhileIterator2.png')" style="width: 600px; height: auto; transform: scale(1);border:solid 1px black;">

**参考结果：**

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SubSystems/WhileIterator/WhileIterator3.png')" style="width: 700px; height: auto; transform: scale(1);border:solid 1px black;">

## 端口

### 输入

<div class="details-box">
<details open>
<summary>cond — 逻辑条件信号<div>标量</div></summary>
</details>
<div class="details-content">

​	当 cond 端口的输入为 false 时，while 子系统结束执行。

**数据类型：** double | float | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | enum

</div>
</div>

<div class="details-box">
<details open>
<summary>IC — 初始逻辑条件<div>标量</div></summary>
</details>
<div class="details-content">

​	带有初始逻辑条件的信号。在每个时间步的开始：

- 如果 IC 为 false，则子系统在当前时间步内不执行；
- 如果 IC 为 true，则子系统开始执行，并且只要 cond 信号为 true，就继续重复执行。

**数据类型：** double | float | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | enum

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>Iteration number — 迭代次数输出信号<div>标量</div></summary>
</details>
<div class="details-content">

​	while 子系统在每个时间步的执行次数。

**数据类型：** double | float | int8 | int16 | int32 | uint8 | uint16 | uint32

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>最大迭代次数 — 指定最大迭代次数<div>-1（默认）| 整数</div></summary>
</details>
<div class="details-content">

指定一个时间步内允许的最大迭代次数。

当最大迭代次数为 -1 时，如果在某个时间步内，IC 端口为 true，并且 cond 端口一直为 true，那么 while 子系统将一直执行。在此情况下，只能手动停止仿真。

</div>
</div>

<div class="details-box">
<details open>
<summary>while循环类型 — 选择模块的类型<div>while (默认) | do-while</div></summary>
</details>
<div class="details-content">

**while**

- While Iterator 模块有两种输入：cond (逻辑条件) 输入和 IC (初始逻辑条件) 输入。
- IC 信号必须来自 while 子系统的外部。
- 在每个时间步的开始，如果 IC 输入为 true，并且 cond 输入为 true，子系统中的模块将重复执行。只要 cond 输入为 true 且迭代次数不大于最大迭代次数，此过程就会在时间步内继续。如果 IC 输入为 false，则 While Iterator 模块不执行子系统的内容。

**do-while**

- While Iterator 模块有一个输入，即 cond  (逻辑条件) 输入。
- 在每个时间步中，只要 cond 输入为 true，且迭代次数小于或等于最大迭代次数，子系统中的模块就会重复执行。

</div>
</div>

<div class="details-box">
<details open>
<summary>开始时的状态 — 选择时间步之间的模块状态<div>保持 (默认) | 重置</div></summary>
</details>
<div class="details-content">

- **保持**

  模块的状态值跨时间步保持不变。

- **重置**

  在每个时间步的开始和第一个迭代循环之前，将模块状态重置为其初始值。

</div>
</div>

<div class="details-box">
<details open>
<summary>显示迭代次数端口 —  控制输出端口的显示<div>off（默认）| on</div></summary>
</details>
<div class="details-content">

- **off**

  不显示迭代次数输出端口。

- **on**

  显示迭代次数输出端口。

</div>
</div>

<div class="details-box">
<details open>
<summary>输出数据类型<div>int32（默认） | uint32 | int16 | uint16 | int8 | uint8 | double</div></summary>
</details>
<div class="details-content">
选择迭代次数信号的输出数据类型。

</div>
</div>

## 版本历史记录

- 在 2025a 推出
