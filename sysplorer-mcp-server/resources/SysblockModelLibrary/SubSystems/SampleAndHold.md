# SampleAndHold

采样并保持输入信号

- **库:** Sysblock / SubSystems

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SubSystems/SampleAndHold/SampleAndHold.png')" style="width:100px;border:black 1px solid;"> 

## 描述

SampleAndHold 模块每当在触发端口接收到触发事件时，都会在信号端口获取输入。然后，该模块将输出保持获取的输入值，直到下一个触发事件发生。

此模块支持接收的触发事件包括：**上升沿**、**下降沿**和**任一沿**。


## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SubSystems/SampleAndHold_Demo.mo">SampleAndHold.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SubSystems/SampleAndHold/SampleAndHold_ex.png')" style="width:600px;border:black 1px solid;"> 

### 示例说明

- PulseGenerator模块：按固定间隔生成方波脉冲。此模块的波形参数振幅、脉冲宽度、周期和相位延迟确定了输出波形的形状；
- SineWave模块：输出正弦曲线波形；
- SampleAndHold模块：接收到触发信号时保持输入信号。示例中为上升沿触发；
- Scope模块：用于显示模型的输出结果，即SampleAndHold组件输出的信号。


### 仿真结果

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SubSystems/SampleAndHold/SampleAndHold_res.png')" style="width:600px;border:black 1px solid;"> 

## 端口

### 输入

<div class="details-box">
<details open>
<summary>inport — 输入信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

输入数据

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | fixed point | boolean | enumerated | bus

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>outport — 输出信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

输出数据

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | fixed point | boolean | enumerated | bus

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>触发类型 — 模块的触发方式<div> “上升沿”（默认）| “下降沿” | “任一沿” </div></summary>
</details>
<div class="details-content">

指定模块接受的触发信号的类型

</div>
</div>

## 版本历史记录

- 在 2025a 推出

### 限制信息

暂不支持设置模块输出信号的初始值。