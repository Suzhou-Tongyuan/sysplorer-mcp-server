# RepeatingSequenceStair
---
&nbsp;
输出并重复离散时间序列。

- **库:** Sysblock / Sources

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/RepeatingSequenceStair/1.png')" style="width:100px;border:black 1px solid;"> 

## 描述

RepeatingSequenceStair 模块输出并重复用户使用**输出值的向量**参数指定的阶梯序列。

## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/RepeatingSequenceStair.mo">RepeatingSequenceStair.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/RepeatingSequenceStair/2.png')" style="width:400px;border:black 1px solid;"> 

### 仿真结果

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/RepeatingSequenceStair/3.png')" style="width:600px;border:black 1px solid;"> 

## 端口

### 输入

<div class="details-box">
<details open>
<summary>Port_1 — 重复离散输出信号<div>标量 </div></summary>
</details>
<div class="details-content">

根据**输出值的向量**和**采样时间**参数中的值生成的输出信号

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | fixed point | enum

</div>
</div>


## 参数

### 主要属性

<div class="details-box">
<details open>
<summary>输出值的向量 — 输出值的向量<div>[3 ,1 ,4 ,2 ,1] (默认) | 标量 | 向量</div></summary>
</details>
<div class="details-content">

指定包含重复的阶梯序列值的向量。

</div>
</div>


<div class="details-box">
<details open>
<summary>采样时间 — 采样时间间隔<div>-1（默认） | 标量</div></summary>
</details>
<div class="details-content">

指定采样时间间隔。不允许指定为连续采样时间（0）。

</div>
</div>



### 信号属性

<div class="details-box">
<details open>
<summary>输出数据类型 — 指定输出数据类型<div>double (默认) | inherit:backPropagation | float| int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | fixed point | enum</div></summary>
</details>
<div class="details-content">

指定输出的数据类型。

</div>
</div>

## 版本历史记录

- 在 2025a 推出

## 限制信息

- 参数“输出值的向量”仅支持标量与向量（包括行向量与列向量），不支持空向量和矩阵。
- 参数“采样时间”必须为离散，不允许指定为联系采样时间（0），仿真会报错。
- 不支持总线。