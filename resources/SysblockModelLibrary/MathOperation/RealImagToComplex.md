# RealImagToComplex

将实部/虚部输入转换成复信号

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/RealImagToComplex/RealImagToComplex.png')" style="width: 100px; border:black 1px solid;">

**库：** Sysblock / MathOperation

## 描述

Real-Imag to Complex 模块将实部/虚部输入转换为具有复数值的输出信号。

这两个输入可以都是具有相同维度的数组（向量或矩阵）；也可以一个输入为数组，另一个输入为标量。如果模块具有数组输入，则输出具有相同维度的复数数组。实数输入的元素映射到对应的复数输出元素的实部。同样，虚数输入映射到复数输出信号的虚部。如果一个输入是标量，它将映射到所有复数输出信号的对应分量（实部和虚部）。

## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperation/RealImagToComplex.mo">RealImagToComplex.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/RealImagToComplex/Example.png')" style="width: 600px; border:black 1px solid;">

**参考结果**

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/RealImagToComplex/Output.png')" style="width: 800px; border:black 1px solid;">

## 端口

### 输入

<div class="details-box">
<details open>
<summary>Re — 复数输出的实部<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

要转换为复数值输出信号的实数值，指定为标量、向量或矩阵。

**数据类型：double | float | int8 | uint8 | int16 | uint16 | int32 | uint32** 

</div>
</div>

<div class="details-box">
<details open>
<summary>Im — 复数输出的虚部<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

要转换为复数值输出信号的虚数值，指定为标量、向量或矩阵。

**数据类型：double | float | int8 | uint8 | int16 | uint16 | int32 | uint32** 

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 向量 | 矩阵 </div></summary>
</details>
<div class="details-content">

复信号，由实数和虚数值构成。

**数据类型：double | float | int8 | uint8 | int16 | uint16 | int32 | uint32** 

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>输入 — 实数输入，虚数输入，或两者同时存在<div>实部（默认值）| 虚部 | 实部和虚部</div></summary>
</details>
<div class="details-content">

指定输入的类型：实数输入、虚数输入或者两者同时存在。

</div>
</div>

<div class="details-box">
<details open>
<summary>虚部 — 复数输出的虚部<div>0（默认值）| 有限标量、向量或矩阵</div></summary>
</details>
<div class="details-content">

指定将输入转换成复数值输出信号时使用的虚数值。

</div>
</div>

<div class="details-box">
<details open>
<summary>实部 — 复数输出的实部<div>0（默认值）| 有限标量、向量或矩阵</div></summary>
</details>
<div class="details-content">

指定将输入转换成复数值输出信号时使用的实数值。

</div>
</div>

## 版本历史记录

- 在 2025b 推出


