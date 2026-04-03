# Width
---
&nbsp;
输出输入信号的宽度。

- **库：** Sysblock / SignalAttributes

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalAttributes/Width/1.png')" style="width:100px;border:black 1px solid;"> 

## 描述

Width 模块将输入信号的宽度作为其输出。

## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalAttributes/Width.mo">Width.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalAttributes/Width/2.png')" style="width:450px;border:black 1px solid;"> 

### 仿真结果

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalAttributes/Width/3.png')" style="width:800px;border:black 1px solid;"> 

## 端口

### 输入

<div class="details-box">
<details open>
<summary>Port_1 — 输入信号<div>标量 | 向量 | 矩阵 | N 维数组</div></summary>
</details>
<div class="details-content">

**数据类型：** double | float | int8 | uint8 | int16 | uint16 | int32 | uint32 | boolean | fixed point | enum | bus

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>Port_1 — 输出信号<div>标量</div></summary>
</details>
<div class="details-content">

**数据类型：** double | float | int8 | uint8 | int16 | uint16 | int32 | uint32

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>输出数据类型模式 — 选择固有数据类型<div></div></summary>
</details>
<div class="details-content">

当勾选此选项后，用户可指定 Width 模块的输出数据类型。

Width 模块支持的输出数据类型有 double | float | int8 | uint8 | int16 | uint16 | int32 | uint32。

</div>
</div>



<div class="details-box">
<details open>
<summary>输出数据类型模式 — 通过反向传播继承<div></div></summary>
</details>
<div class="details-content">

Width 模块的输出数据类型由和它输出端口相连的模块的数据类型决定。

</div>
</div>


<div class="details-box">
<details open>
<summary>输出数据类型模式 — 所有端口都具有相同的数据类型<div></div></summary>
</details>
<div class="details-content">

模块的输出数据类型和其输入信号的数据类型保持一致。

</div>
</div>

## 版本历史记录

- 在 2025a 推出

## 限制信息

- 模块的输出不能超过所选数据类型的取值范围。