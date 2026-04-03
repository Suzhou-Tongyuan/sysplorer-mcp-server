# PermuteMatrix
---
&nbsp;

重新排序矩阵的行或列。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/PermuteMatrix/PermuteMatrix1.png')" style="width: 100px; border:black 1px solid;">

**库：** TYDSPSystem / StatisticsAndLinearAlgebra / ArrayAndMatrixMathematics 

## 描述

PermuteMatrix 模块根据索引输入 P 指定的顺序重新排列 M×N 输入矩阵 A 的行或列。
## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperation/PermuteMatrix.mo">PermuteMatrix.mo</helpButton>。

矩阵 A 的行和列可以根据索引向量的要求，在输出中出现任意次数或不出现。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/PermuteMatrix/PermuteMatrix2.png')" style="width: 600px; border:black 1px solid;">

## 端口

### 输入

<div class="details-box">
<details open>
<summary>u1 — 输入矩阵<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">
输入矩阵，指定为标量、一维数组、向量或矩阵。

**数据类型：** double | float | int8 | int16 | int32 | int64 | uint8 | uint16 | uint32 | uint64 | boolean | enum

</div>
</div>

<div class="details-box">
<details open>
<summary>u2 — 索引矩阵<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">
输入矩阵，指定为标量、一维数组、向量或矩阵。

**数据类型：** double | float | int8 | int16 | int32 | int64 | uint8 | uint16 | uint32 | uint64 | boolean | enum

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>y — 输出矩阵<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">
输出矩阵，以向量或矩阵的形式输出。输出数据类型与输入矩阵 u1 相同。

**数据类型：** double | float | int8 | int16 | int32 | int64 | uint8 | uint16 | uint32 | uint64 | boolean | enum

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>置换 — 置换方法<div>列（默认）| 行</div></summary>
</details>
<div class="details-content">

​	行 — 模块使用 A 的行来创建一个具有相同列维度的矩阵。输入 P 是一个长度为 L 的向量，其元素决定 A 的每一行必须放置在 L×N 输出矩阵中的位置。

​	对于行置换，模块将端口 A 处的长度为 M 的无方向向量输入视为一个 M×1 矩阵。

​	列 — 模块使用 A 的列来创建一个具有相同行维度的矩阵。输入 P 是一个长度为 L 的向量，其元素决定 A 的每一列必须放置在 M×L 输出矩阵中的位置。

​	对于列重排，该模块将端口 A 处的长度为 N 的无方向向量输入视为一个 1×N 矩阵。

</div>
</div>

<div class="details-box">
<details open>
<summary>索引模式<div>从 1 开始（默认）| 从 0 开始</div></summary>
</details>
<div class="details-content">
当设置为从 1 开始是，置换向量 P 中的 1 的值指的是输入矩阵 A 的第一行或第一列。当设置为从 0 开始时，P 的 0 值指的是 A 的第一行或第一列。

</div>
</div>

<div class="details-box">
<details open>
<summary>无效的置换索引 — 选择对无效索引值作出的响应<div>裁剪索引（默认）| 裁剪和警告 | 报错</div></summary>
</details>
<div class="details-content">

对无效索引值的响应。当输入 P 中的索引值引用矩阵 A 中不存在的行或列时，该模块将按照此参数中指定的方式作出反应。可用的选项有

裁剪索引 — 将索引裁剪到最近的有效值（对于行重排为 1 或 M，对于列重排为 1 或 N），且不发出警告。示例：对于 3 行 7 列的输入矩阵，列索引 9 被裁剪为 7，行索引 -2 被裁剪为 1。

裁剪和警告 — 显示警告消息，并按前述要求裁剪索引。

报错 — 显示错误对话框并终止仿真。

</div>
</div>

<div class="details-box">
<details open>
<summary>当 P 的长度不等于排列维度大小时出现错误 — 选择是否触发 P 长度错误信息<div>off（默认）| on</div></summary>
</details>
<div class="details-content">

显示错误对话框并在置换向量 P 的长度不等于输入矩阵 A 的行数或列数时终止仿真的选项。

通过将此参数设置为 on，您可以选择打开错误对话框并终止仿真。

</div>
</div>

## 版本历史记录

- 在 2026a 推出


## 限制信息

- 输入数据类型不支持定点和总线。

  
