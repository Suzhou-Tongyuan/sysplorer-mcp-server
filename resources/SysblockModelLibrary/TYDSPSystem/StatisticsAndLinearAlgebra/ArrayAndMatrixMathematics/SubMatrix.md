# SubMatrix
---
&nbsp;

从矩阵输入中选择元素子集（子矩阵）。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/SubMatrix/SubMatrix1.png')" style="width: 100px; border:black 1px solid;">

**库：** TYDSPSystem / StatisticsAndLinearAlgebra / ArrayAndMatrixMathematics 

## 描述

SubMatrix 模块从 M×N 的输入矩阵 u 中提取一个连续的子矩阵。有关如何选择要提取的行和列的信息，请参阅范围[指定选项](#jump1)。

## 示例

**示例**

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperation/SubMatrix.mo">SubMatrix.mo</helpButton>。

示例模型中展示了如何使用子矩阵模块从 3×3 的输入矩阵的左上角提取一个 2×2 的子矩阵。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/SubMatrix/SubMatrix2.png')" style="width: 700px; border:black 1px solid;">

## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

输入矩阵，从中提取指定子矩阵的块。

**数据类型：** double | float | int8 | int16 | int32 | int64 | uint8 | uint16 | uint32 | uint64 | boolean | enum

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 输出选定的子矩阵<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

从输入信号中选择的子矩阵，输出数据类型与输入相同。

**数据类型：** double | float | int8 | int16 | int32 | int64 | uint8 | uint16 | uint32 | uint64 | boolean | enum

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>行跨度 — 行号范围<div>所有行（默认）| 一行 | 行的范围</div></summary>
</details>
<div class="details-content">

要保留在输出中的输入行范围。

</div>
</div>

<div class="details-box">
<details open>
<summary>行<div>首（默认）| 索引 | 离末尾偏移量 | 末 | 离中间偏移量 | 中间</div></summary>
</details>
<div class="details-content">

要作为输出中的第一行和唯一一行的输入行。

要启用此参数，将行跨度设置为一行。

</div>
</div>

<div class="details-box">
<details open>
<summary>开始行<div>首（默认）| 索引 | 离末尾偏移量 | 末 | 离中间偏移量 | 中间</div></summary>
</details>
<div class="details-content">

要作为输出中的第一行和唯一一行的输入行。

要启用此参数，将行跨度设置为一行。

</div>
</div>

<div class="details-box">
<details open>
<summary>结束行<div>末（默认）| 索引 | 离末尾偏移量 | 离中间偏移量 | 中间</div></summary>
</details>
<div class="details-content">

要用作输出最后一行的输入行。

要启用此参数，将行跨度设置为行的范围，并将开始行设置为除末以外的任何值。

</div>
</div>

<div class="details-box">
<details open>
<summary>列跨度 — 列号范围<div>所有列（默认）| 一列 | 列的范围</div></summary>
</details>
<div class="details-content">

要保留在输出中的输入列范围。

</div>
</div>

<div class="details-box">
<details open>
<summary>列<div>首（默认）| 索引 | 离末尾偏移量 | 末 | 离中间偏移量 | 中间</div></summary>
</details>
<div class="details-content">

要作为输出中的第一列和唯一一列的输入列。

要启用此参数，将行跨度设置为一列。

</div>
</div>

<div class="details-box">
<details open>
<summary>开始列<div>首（默认）| 索引 | 离末尾偏移量 | 末 | 离中间偏移量 | 中间</div></summary>
</details>
<div class="details-content">

要用作输出第一列的输入列。

要启用此参数。将行跨度设置为列的范围。

</div>
</div>

<div class="details-box">
<details open>
<summary>结束列<div>末（默认）| 索引 | 离末尾偏移量 | 离中间偏移量 | 中间</div></summary>
</details>
<div class="details-content">

要用作输出最后一列的输入列。

要启用此参数，将行跨度设置为列的范围，并将开始列设置为除末以外的任何值。

</div>
</div>

**范围指定选项**<a id="jump1"></a>

行跨度参数为指定要保留在子矩阵输出 y 中的输入 u 的行范围提供了三种选项:

- 所有行

指定 y 包含 u 的所有行。

- 一行

指定 y 仅包含 u 的一行。选择一行选项使行参数可用，已选择所需的行。

- 行的范围

指定 y 包含 u 的若干行。选择行的范围选项使开始行和结束行参数可用，已选择所需的行范围。

列跨度参数包含一组与行跨度相对应的三个选项，用于指定要保留在在矩阵 y 中的 u 范围内的列：所有列、一列和列的范围。一列选项启用列参数，列的范围选项启用开始列和结束列参数。

行、列、开始行、开始列、结束行和结束列可以以六种方式指定：

- 首

  对于行或开始行，这指定了应使用 u 的第一行作为 y 的第一行。

  对于列或开始列，这指定了应使用 u 的第一列作为 y 的第一列。

- 索引

  对于行或开始行，这指定了应使用 u 的行，通过行索引参数进行正向索引，作为 y 的第一行。

  对于结束行，这指定了应使用 u 的行，通过结束行索引参数进行正向索引，作为 y 的最后一行。

  对于列或开始列，这指定了应使用 u 的列，通过列索引参数进行正向索引，作为 y 的第一列。

  对于结束列，这指定了应使用 u 的列，通过结束列索引参数进行正向索引，作为 y 的最后一列。

- 离末尾偏移量

  对于行或开始行，模块通过将指定的偏移量添加到输入 u 的最后一行来选择输出 y 的最后一行。

  对于结束行，模块通过将指定的偏移量添加到输入 u 的最后一行来选择输出 y 的最后一行。

  对于列或开始列，模块通过将指定的偏移量添加到输入 u 的最后一列来选择输出 y 的最后一列。

  对于结束列，模块通过将指定的偏移量添加到输入 u 的最后一列来选择输出 y 的最后一列。

- 末

  对于行或开始行，这指定了应使用 u 的第一行作为 y 的唯一一行。

  对于列或开始列，这指定了应使用 u 的第一列作为 y 的唯一一列。

- 离中间偏移量

  对于行或开始行，模块通过将指定的偏移量添加到输入u 的中间行来选择输出 y 的第一行。当输入行数量 M 为偶数时，模块将中间定义为 M/2+1。当输入行的数量为奇数时，模块将中间定义为 ceil(M/2)。

  对于结束行，模块通过将指定的偏移量添加到输入 u 的中间行来选择输出 y 的最后一行。当输入行数量 M 为偶数时，模块将中间定义为 M/2+1。当输入行的数量为奇数时，模块将中间定义为 ceil(M/2)。

  对于列或开始列，模块通过将指定的偏移量添加到输入 u 的中间列来选择输出 y 的第一列。当输入列数量 N 为偶数时，模块将中间定义为 N/2+1。当输入列的数量为奇数时，模块将中间定义为 ceil(N/2)。

  对于结束列，模块通过将指定的偏移量添加到输入 u 的中间列来选择输出 y 的最后一列。当输入列数量 N 为偶数时，模块将中间定义为 N/2+1。当输入列的数量为奇数时，模块将中间定义为 ceil(N/2)。

- 中间

  对于行或开始行，这指定了应使用 u 的中间行作为 y 的第一行。当输入行数量 M 为偶数时，模块将中间定义为 M/2+1。当输入行的数量为奇数时，模块将中间定义为 ceil(M/2)。

  对于结束行，这指定了应使用 u 的中间行作为 y 的最后一行。当输入行数量 M 为偶数时，模块将中间定义为 M/2+1。当输入行的数量为奇数时，模块将中间定义为 ceil(M/2)。

  对于列或开始列，这指定了应使用 u 的中间列作为 y 的第一列。当输入列数量 N 为偶数时，模块将中间定义为 N/2+1。当输入列的数量为奇数时，模块将中间定义为 ceil(N/2)。

  对于结束列，这指定了应使用 u 的中间列作为 y 的最后一列。当输入列数量 N 为偶数时，模块将中间定义为 N/2+1。当输入列的数量为奇数时，模块将中间定义为 ceil(N/2)。

## 版本历史记录

- 在 2026a 推出


## 限制信息

- 输入数据类型不支持定点和总线；
- 开始行的索引不能超过结束行的索引；
- 开始列的索引不能超过结束列的索引。
