# MagnitudeAngleToComplex

将幅值/相位角输入转换成复信号

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/MagnitudeAngleToComplex/MagnitudeAngleToComplex.png')" style="width: 100px; border:black 1px solid;">

**库：** Sysblock / MathOperation

## 描述

Magnitude-Angle to Complex 模块将幅值/相位角输入转换为具有复数值的输出信号。角度输入必须以弧度为单位。

当有两个模块输入时，模块支持输入维度的一下组合：

- 两个输入具有相同的维度；

- 一个输入为标量，另一个为 n 维数组。

  如果模块输入为数组，则输出是复信号数组，幅值输入向量的元素映射到对应的复数输出元素的幅值。同样，角度输入向量的元素映射到对应的复数输出元素的角度。如果一个输入是标量，它将映射到所有复数输出信号的对应分量（幅值或角度）。

## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperation/MagnitudeAngleToComplex.mo">MagnitudeAngleToComplex.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/MagnitudeAngleToComplex/Example.png')" style="width: 600px; border:black 1px solid;">

**参考结果**

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/MagnitudeAngleToComplex/Output.png')" style="width: 800px; border:black 1px solid;">

## 端口

### 输入

<div class="details-box">
<details open>
<summary>|u| — 幅值<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

幅值，指定为实数值标量、向量或矩阵。

**数据类型：double | float | int8 | uint8 | int16 | uint16 | int32 | uint32**

</div>
</div>

<div class="details-box">
<details open>
<summary>∠u — 相位角弧度<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

相位角弧度，指定为实数值标量、向量或矩阵。

**数据类型：double | float | int8 | uint8 | int16 | uint16 | int32 | uint32**

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 向量 | 矩阵 </div></summary>
</details>
<div class="details-content">

复信号，由幅值和相位角构成。

**数据类型：double | float | int8 | uint8 | int16 | uint16 | int32 | uint32**

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>输入 — 输入类型<div>幅值（默认值）| 角度 | 幅值和角度</div></summary>
</details>
<div class="details-content">

指定输入的类型：幅值输入、角度输入或者两者同时存在。

</div>
</div>

<div class="details-box">
<details open>
<summary>角度 — 输出的相位角<div>0（默认值）| 有限标量、向量或矩阵</div></summary>
</details>
<div class="details-content">

输出信号的常量相位角，以弧度为单位。

</div>
</div>

<div class="details-box">
<details open>
<summary>幅值 — 输出的幅值<div>0（默认值）| 有限标量、向量或矩阵</div></summary>
</details>
<div class="details-content">

输出信号的常量幅值，指定为实数值标量、向量或矩阵。

</div>
</div>

## 版本历史记录

- 在 2025b 推出


