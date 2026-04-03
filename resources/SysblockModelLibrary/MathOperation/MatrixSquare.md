# MatrixSquare

计算输入矩阵的平方

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/MatrixSquare/MatrixSquare1.png')" style="width: 100px; border:black 1px solid;">

**库：** Sysblock / MathOperation

## 描述

MatrixSquare 模块计算输入矩阵的平方。矩阵平方模块通过共轭转置前乘来计算 M×N 的输入矩阵 u 的平方。等效公式为：
$$
y=u'*u
$$
该模块将长度为 M 的无方向向量输入视为 M×1 矩阵。当输入为 M×N 矩阵时，模块的输出为 N×N 矩阵。

## 示例

**示例**

矩阵平方模块可用于多种应用：

- 一般矩阵平方—矩阵平方模块计算输出矩阵 y 时，无需显示形成 u'。因此，它比其它计算矩阵平方的方法更高效。

  参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperation/MatrixSquare1.mo">MatrixSquare1.mo</helpButton>。

  <img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/MatrixSquare/MatrixSquare2.png')" style="width: 600px; border:black 1px solid;">

- 平方和—当输入是一个列向量（N=1）时，该模块的操作相当于矩阵元素的平方累加过程，或内积。输出是输入元素的平方和，始终是一个实数标量。

  参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperation/MatrixSquare2.mo">MatrixSquare2.mo</helpButton>。

  <img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/MatrixSquare/MatrixSquare3.png')" style="width: 600px; border:black 1px solid;">

- 相关矩阵—当输入是一个行向量（M=1）时，输出y是对称自相关矩阵，或外积。

  参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperation/MatrixSquare3.mo">MatrixSquare3.mo</helpButton>。

  <img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/MatrixSquare/MatrixSquare4.png')" style="width: 600px; border:black 1px solid;">



## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>M×1 矩阵 | 1×N 矩阵 | M×N 矩阵</div></summary>
</details>
<div class="details-content">

输入矩阵，指定为 M×1、1×N 或 M×N 矩阵。

**数据类型：** double | float | int8 | int16 | int32 | int64 | uint8 | uint16 | uint32 | uint64

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>M×M矩阵 | N×N矩阵</div></summary>
</details>
<div class="details-content">

输出矩阵，以 M×M、N×N 矩阵的形式输出。

**数据类型：** double | float | int8 | int16 | int32 | int64 | uint8 | uint16 | uint32 | uint64

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>输出数据类型 — 指定输出数据的类型<div>Inherit:auto（默认）| double | float | int8 | int16 | int32 | int64 | uint8 | uint16 | uint32 | uint64 | fixdt(1,16,0) | fixdt(1,16,2^0,0) </div></summary>
</details>
<div class="details-content">

指定此模块输出数据的类型。

</div>
</div>

<div class="details-box">
<details open>
<summary>对整数溢出进行饱和处理<div>off（默认值）| on</div></summary>
</details>
<div class="details-content">

选中此复选框，以便让溢出饱和到数据类型所能表示的最大值或最小值。如果不勾选此复选框，模块将所有溢出进行环绕处理。

</div>
</div>

## 版本历史记录

- 在 2025b 推出


### 限制信息

- 输入数据类型不支持定点和总线；
- 输入数据维度不支持标量和一维数组。
