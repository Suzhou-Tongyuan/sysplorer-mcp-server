# FindNonzeroElements

查找数组中的非零元素

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/FindNonzeroElements/1.png')" style="width: 100px; height: auto;border: 1px solid black;">

**库：** Sysblock / MathOperation

## 描述

FindNonzeroElements 模块找到输入信号的所有非零元素，并返回这些元素的线性索引。如果输入是多维信号，则 FindNonzeroElements 模块还可以返回非零输入元素的下标。在这两种情况下，您都可以显示具有非零输入值的输出端口。

## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperation/FindNonzeroElements.mo">FindNonzeroElements.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/FindNonzeroElements/2.png')" style="width: 400px;border: 1px solid black; ">

**参考结果**

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/FindNonzeroElements/3.png')" style="width: 600px;border: 1px solid black; ">

## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">

输入信号，模块将从中查找所有非零元素。


**数据类型：double | float | int8 | uint8 | int16 | uint16 | int32 | uint32 | int64 | uint64 | boolean | fixdt(1, 16, 0) | fixdt(1, 16, 2^0, 0)**

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>y — 非零元素的索引<div>标量 | 一维数组</div></summary>
</details>
<div class="details-content">

FindNonzeroElements 模块将非零元素的索引输出为标量或一维数组。您可以在**输出数据类型**的参数面板中选择输出的数据类型。


**数据类型：int8 | uint8 | int16 | uint16 | int32 | uint32 | int64 | uint64 | fixdt(1, 16, 0)**

</div>
</div>

<div class="details-box">
<details open>
<summary>y0 — 非零元素的值<div>标量 | 一维数组</div></summary>
</details>
<div class="details-content">

（可选）FindNonzeroElements 模块可以将所有非零元素的值输出为标量或一维数组，该端口的数据类型和输入端口的类型保持一致。

**数据类型：double | float | int8 | uint8 | int16 | uint16 | int32 | uint32 | int64 | uint64 | boolean | fixdt(1, 16, 0) | fixdt(1, 16, 2^0, 0)**

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>索引输出格式 — 非零元素索引的格式<div>线性索引（默认值）| 下标</div></summary>
</details>
<div class="details-content">

选择非零输入值的索引的输出格式。

- 选择**线性索引**将以向量形式提供任何维度信号的元素索引。对于一维（向量）信号，索引对应于向量内非零值的位置。对于具有多个维度的信号，会沿第一个维度将下标转换为索引。
- 选择**下标**将以下标形式提供二维或更大信号的元素索引。由于该模块显示每个维度的输出端口，因此该选项要求您指定**输入维数**。

</div>
</div>

<div class="details-box">
<details open>
<summary>输入维数 — 输入信号的维度数<div>3（默认值）| 标量</div></summary>
</details>
<div class="details-content">

将输入信号的维度数指定为 1 到 32 之间的正整数值，该参数的值需要和实际的输入维数保证一致。

</div>
</div>

<div class="details-box">
<details open>
<summary>索引模式 — 指导从 0 或 1 开始的索引<div>从0开始（默认值）| 从 1 开始</div></summary>
</details>
<div class="details-content">


将索引模式指定为**从 0 开始**或**从 1 开始**。

</div>
</div>

<div class="details-box">
<details open>
<summary>显示非零输入值的输出端口 — 为非零值启用输出端口<div>off（默认值）| on</div></summary>
</details>
<div class="details-content">

显示或隐藏非零输入值的输出端口。

</div>
</div>

<div class="details-box">
<details open>
<summary>输出数据类型<div>Inherit: internalRule （默认值） | int8 | uint8 | int16 | uint16 | int32 | uint32 | int64 | uint64 | fixdt(1, 16, 0)</div></summary>
</details>
<div class="details-content">

指定模块输出信号的数据类型。


</div>
</div>



## 版本历史记录

- 在 2025b 推出

### 限制信息

- 暂不支持 FindNonzeroElements 模块的输出信号为可变大小信号。

