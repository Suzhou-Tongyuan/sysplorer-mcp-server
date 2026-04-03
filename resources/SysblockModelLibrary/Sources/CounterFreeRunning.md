# CounterFreeRunning
---
自由运行的计数器模块

- **库：** Sysblock / Sources

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/CounterFreeRunning/CounterFreeRunning.png')" style="width:100px;border:black 1px solid;"> 

## 描述

CounterFreeRunning 模块是一个自由运行的计数器，在达到指定位数的可能最大值后溢出回零。

CounterFreeRunning 模块进行累加计数，直到达到最大值 2<sup>Nbits–1</sup>，其中 Nbits 是模块指定的位数。然后，该计数器将溢出归零并重新开始进行累加计数。

## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/CounterFreeRunning_Demo.mo">CounterFreeRunning.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/CounterFreeRunning/CounterFreeRunning_ex.png')" style="width:600px;border:black 1px solid;border-top: 1px solid black;"> 

### 示例说明

- CounterFreeRunning 模块：按照上限位数及采样时间生成计数信号；
- Scope 模块：显示输入信号曲线；示例中即 CounterFreeRunning 模块输出的信号。

### 仿真结果

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/CounterFreeRunning/CounterFreeRunning_res.png')" style="width:600px;border:black 1px solid;border-top: 1px solid black;"> 


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
<summary>上限位数 — 输出位数上限<div>16（默认）| 整数标量</div></summary>
</details>
<div class="details-content">

指定输出信号位数的上限。

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