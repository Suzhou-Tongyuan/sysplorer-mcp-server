# ComplexToMagnitudeAngle

输出复数的幅值和/或相位角

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/ComplexToMagnitudeAngle/ComplexToMagnitudeAngle.png')" style="width: 100px; border:black 1px solid;">

**库：** Sysblock / MathOperation

## 描述

Complex To MagnitudeAngle 模块输出输入信号的幅值和/或相位角，具体取决于输出参数的设置。输出与模块输入具有相同的数据类型。输入可以是复数数组（向量或矩阵），这种情况下，输出信号也是具有相同维度的数组。幅值信号数组包含对应的复数输入元素的幅值。同样，角度输出包含输入元素的角度。

## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperation/ComplexToMagnitude.mo">ComplexToMagnitude.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/ComplexToMagnitudeAngle/Example.png')" style="width: 600px; border:black 1px solid;">

**参考结果**

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/ComplexToMagnitudeAngle/Output.png')" style="width: 800px; border:black 1px solid;">

## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 向量 | 矩阵 </div></summary>
</details>
<div class="details-content">

该模块计算并输出幅值和/或相位角的复数输入信号。

**数据类型：double | float | int8 | uint8 | int16 | uint16 | int32 | uint32**

</div>
</div>

### 输出

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

## 参数

<div class="details-box">
<details open>
<summary>输出 — 幅值和/或相位角输出设定<div>幅值和角度（默认值）| 幅值 | 角度</div></summary>
</details>
<div class="details-content">
指定输出是输入信号的幅值还是相位角（弧度）。

</div>
</div>

## 版本历史记录

- 在 2025b 推出


