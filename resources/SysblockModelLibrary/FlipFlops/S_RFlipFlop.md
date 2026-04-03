# S_RFlipFlop
---
&nbsp;

置位/复位触发器模块

- **库:** Sysblock / FlipFlops

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/FlipFlopsPng/S_RFlipFlop/S_RFlipFlop.png')" style="width:100px;border:black 1px solid;"> 

## 描述

S_RFlipFlop 模块为一个置位（Set）复位（Reset）触发器。

真值表如下表所示：

| S | R | Q<sub>n</sub> | !Q<sub>n</sub> |
| :--- | :----- | :---|:---|
| 0  | 0 | Q<sub>n-1</sub> | !Q<sub>n-1</sub>|
| 0  | 1 | 0 | 1 |
| 1  | 0 | 1 | 0 |
| 1  | 1 | 0 | 0 |
Q<sub>n-1</sub> 表示上一时间步的输出。

## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/FlipFlops/S_RFlipFlop_Demo.mo">S_RFlipFlop_Demo.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/FlipFlopsPng/S_RFlipFlop/S_RFlipFlop_ex.png')" style="width:600px;border:black 1px solid;"> 

### 示例说明

- Step 模块：输出在指定时间的两个电平的阶跃信号；
- TypeConversion 模块：将输入信号转换为指定类型。示例中均为转换为 boolean 类型；
- S_RFlipFlop 模块：置位（Set）复位（Reset）触发器模块；
- Scope 模块：用于显示模型的输出结果，即 S_RFlipFlop 组件输出的信号。

### 仿真结果

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/FlipFlopsPng/S_RFlipFlop/S_RFlipFlop_res.png')" style="width:400px;border:black 1px solid;"> 

## 端口

### 输入

<div class="details-box">
<details open>
<summary>S — 置位输入信号<div>标量</div></summary>
</details>
<div class="details-content">

输入的置位信号

**数据类型：** boolean

</div>
</div>

<div class="details-box">
<details open>
<summary>R — 复位输入信号<div>标量</div></summary>
</details>
<div class="details-content">

输入的复位信号

**数据类型：** boolean

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>Q — 输出信号<div>标量</div></summary>
</details>
<div class="details-content">

输出信号

**数据类型：** boolean

</div>
</div>

<div class="details-box">
<details open>
<summary>!Q — 输出信号<div>标量</div></summary>
</details>
<div class="details-content">

输出信号

**数据类型：** boolean

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>初始条件 — 输出信号 Q 的初始值<div>0（默认）| 标量 </div></summary>
</details>
<div class="details-content">

指定输出信号Q的初始值。非零值作为 `true(1)` 处理。

</div>
</div>

## 版本历史记录

- 在 2025a 推出