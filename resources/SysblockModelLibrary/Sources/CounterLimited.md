# CounterLimited
---
计数器模块

- **库：** Sysblock / Sources

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/CounterLimited/CounterLimited.png')" style="width:100px;border:black 1px solid;"> 

## 描述

CounterLimited 模块进行累加计数，直到达到指定的上限。然后，该计数器绕回到零并重新启动累加计数。该计数器始终初始化为零。

## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/CounterLimited_Demo.mo">CounterLimited.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/CounterLimited/CounterLimited_ex.png')" style="width:600px;border:black 1px solid;"> 

### 示例说明

- CounterLimited 模块：按照上限及采样时间生成计数信号；
- Scope 模块：显示输入信号曲线。示例中即 CounterLimited 模块输出的信号。

### 仿真结果

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/CounterLimited/CounterLimited_res.png')" style="width:600px;border:black 1px solid;"> 

## 端口

### 输出

<div class="details-box">
<details open>
<summary>res — 输出信号<div>标量</div></summary>
</details>
<div class="details-content">

输出信号

**数据类型：** uint32 | uint16 | uint8

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>上限 — 输出上限<div>16（默认）| 整数标量</div></summary>
</details>
<div class="details-content">

指定输出信号的上限。

</div>
</div>

<div class="details-box">
<details open>
<summary>采样时间 — 采样周期<div>-1（默认）| 标量</div></summary>
</details>
<div class="details-content">

以秒为单位指定采样周期，默认值为 -1。

</div>
</div>

## 版本历史记录

- 在 2025a 推出