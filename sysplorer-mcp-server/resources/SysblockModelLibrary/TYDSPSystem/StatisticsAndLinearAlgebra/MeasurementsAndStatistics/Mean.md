# Mean
---
&nbsp;

计算输入的平均值。

**库：**  TYDSPSystem / StatisticsAndLinearAlgebra / MeasurementsandStatistics

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYDSPSystem/StatisticsAndLinearAlgebra/MeasurementsAndStatistics/Mean/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

Mean 模块计算输入的每一行或每一列的平均值，或计算输入中指定维度向量的平均值。它还可以计算整个输入的平均值。


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 数据输入<div> 实数矩阵</div></summary>
</details>
<div class="details-content">

输入信号，指定为实数矩阵。

**数据类型：** double 

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>y — 输出平均值<div>实数矩阵</div></summary>
</details>
<div class="details-content">
 
模块计算输入的每一行或每一列的平均值，或沿输入指定维度的向量计算平均值。它还可以计算每个采样时间的整个输入的平均值。输出数组 y 中的每个元素是相应列、行或整个输入的平均值。输出数组 y 取决于**指定求均值维度**参数的设置。

**数据类型：** double 

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>指定求均值维度 — 均值计算的维度<div>Each column (默认) | Entire input | Each row</div></summary>
</details>
<div class="details-content">

可选项如下：

 - Each column — 模块输出每列的方差；

 - Each row — 模块输出每行的方差；

 - Entire input — 模块输出整个输入的方差。

</div>
</div>

<div class="details-box">
<details open>
<summary>输入信号维度 — 指定输入信号维度<div>{1，1}（默认）| 长度为 2 的整型向量</div></summary>
</details>
<div class="details-content">

指定输入信号的维度。指定为长度为 2 的整型向量。

</div>
</div>

## 版本历史记录

- 在 2025b 推出

## 限制信息

- 该模块暂不支持自动识别输入信号维度，需通过**输入信号维度**参数手动设定，且当前 Variance 仅支持输入实数矩阵。
