# IsTriangular

检测输入信号是否为上三角矩阵或下三角矩阵

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/IsTriangular/IsTriangular1.png')" style="width: 100px; border:black 1px solid;">

**库：** Sysblock / MathOperation

## 描述

IsTriangular 模块用于判断输入信号是否为上三角矩阵或下三角矩阵。

## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperation/IsTriangular.mo">IsTriangular.mo</helpButton>。

**示例**

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/IsTriangular/IsTriangular2.png')" style="width: 500px; border:black 1px solid;">

**参考结果**

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/IsTriangular/IsTriangular3.png')" style="width: 900px; border:black 1px solid;">



## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 矩阵</div></summary>
</details>
<div class="details-content">

输入标量或矩阵。

**数据类型：**  double | float | int8 | int16 | int32 | int64 | uint8 | uint16 | uint32 | uint64

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量</div></summary>
</details>
<div class="details-content">

当输入信号是上三角矩阵或下三角矩阵时，输出为真，否则为假。

**数据类型：** double | float | int8 | int16 | int32 | int64 | uint8 | uint16 | uint32 | uint64

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>模式 — 矩阵为上三角矩阵还是下三角矩阵<div>上限（默认）| 下限</div></summary>
</details>
<div class="details-content">

检测输入信号是否是上三角矩阵，或者是否是下三角矩阵。

</div>
</div>

## 版本历史记录

- 在 2025a 推出


