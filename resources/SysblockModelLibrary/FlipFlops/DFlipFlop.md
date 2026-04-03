# DFlipFlop
---
&nbsp;

D 触发器

- **库:** Sysblock / FlipFlops

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/FlipFlopsPng/DFlipFlop/DFlipFlop.png')" style="width:100px;border:black 1px solid;"> 

## 描述

DFlipFlop 模块为带使能端口的上升沿触发的 D 触发器模块。

该模块有三个输入端口：数据端口、时钟端口，以及使能端口。该模块将数据端口的数据传输到输出端口 Q，仅当使能端口生效且时钟信号在上升沿转换时，输出才会更新。否则，该模块将输出保持在其先前状态。

## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/FlipFlops/DFlipFlop_Demo.mo">DFlipFlop.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/FlipFlopsPng/DFlipFlop/DFlipFlop_ex.png')" style="width:600px;border:black 1px solid;"> 

### 示例说明

- Constant 模块：输出常量值信号。示例中该模块产生使能信号；
- PulseGenerator 模块：按固定间隔生成方波脉冲。示例中该模块产生时钟信号；
- Step 模块：输出在指定时间的两个电平的阶跃信号。示例中为数据信号；
- TypeConversion 模块：将输入信号转换为指定类型。示例中均为转换为 boolean 类型；
- DFlipFlop 模块：带使能端口的 D 触发器；
- Scope 模块：用于显示模型的输出结果，即 DFlipFlop 组件输出的信号。

### 仿真结果

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/FlipFlopsPng/DFlipFlop/DFlipFlop_res.png')" style="width:400px;border:black 1px solid;"> 

## 端口

### 输入

<div class="details-box">
<details open>
<summary>D — 数据信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

输入的数据信号

**数据类型：** boolean

</div>
</div>

<div class="details-box">
<details open>
<summary>CLK — 时钟信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

输入的时钟信号

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | fixed point | enumerated

</div>
</div>

<div class="details-box">
<details open>
<summary>!CLR — 使能信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

输入的使能信号

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | fixed point | enumerated

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>Q — 输出信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

输出信号

**数据类型：** double | boolean

</div>
</div>

<div class="details-box">
<details open>
<summary>!Q — 输出信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

输出信号

**数据类型：** double | boolean

</div>
</div>

## 版本历史记录

- 在 2025a 推出