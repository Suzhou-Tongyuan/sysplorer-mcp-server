# ComplexToRealImag

输出复数输入信号的实部和虚部

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/ComplexToRealImag/ComplexToRealImag.png')" style="width: 100px; border:black 1px solid;">

**库：** Sysblock / MathOperation

## 描述

Complex To Real-Imag 模块输出输入信号的实部/或虚部，具体取决于输出参数的设置。实数输出与复数输入具有相同的数据类型。输入可以是复数数组（向量或矩阵），这种情况下，输出信号也是具有相同维度的数组。实数数组包含对应的复数输入元素的实部。同样，虚数输出包含输入元素的虚部。

## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperation/ComplexToRealImag.mo">ComplexToRealImag.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/ComplexToRealImag/Example.png')" style="width: 600px; border:black 1px solid;">

**参考结果**

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/ComplexToRealImag/Output.png')" style="width: 800px; border:black 1px solid;">

## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 向量 | 矩阵 </div></summary>
</details>
<div class="details-content">

该模块计算并输出实部和/或虚部的复数输入信号。

**数据类型：double | float | int8 | uint8 | int16 | uint16 | int32 | uint32** 

</div>
</div>

### 输出

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

## 参数

<div class="details-box">
<details open>
<summary>输出 — 实部和/或虚部输出设定<div>实部和虚部（默认值）| 虚部 | 实部</div></summary>
</details>
<div class="details-content">

指定输出是输入信号的实部还是虚部。

</div>
</div>

## 版本历史记录

- 在 2025b 推出


