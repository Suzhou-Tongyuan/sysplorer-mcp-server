# Variance
---
&nbsp;

按照维度计算方差。

**库：**  TYDSPSystem / StatisticsAndLinearAlgebra / MeasurementsAndStatistics

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYDSPSystem/StatisticsAndLinearAlgebra/MeasurementsAndStatistics/Variance/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

Variance 模块计算输入的每一行或每一列的无偏方差，或计算输入中指定维度向量的无偏方差。它还可以计算整个输入的方差。您可以使用**方差计算方式**参数指定维度。Variance 模块还可以跟踪一段时间内输入序列的方差。要跟踪输入序列的方差，请勾选**即时计算**方差复选框。


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 信号输入<div> 实数矩阵</div></summary>
</details>
<div class="details-content">

输入信号，指定为实数矩阵。

**数据类型：** double 

</div>
</div>


<div class="details-box">
<details open>
<summary>rst — 复位信号<div> 实数标量</div></summary>
</details>
<div class="details-content">

复位信号，指定为实数标量。

**数据类型：** double 

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 输出方差计算结果<div>实数矩阵</div></summary>
</details>
<div class="details-content">
 
如果未选择**即时计算方差**参数，该模块将计算输入的每一行或每一列的方差，或沿输入指定维度向量的方差。它还可以计算每个采样时间整个输入的方差。输出数组 y 中的每个元素是相应列、行或整个输入的方差。输出数组 y 取决于**方差计算方式**参数的设置。

**数据类型：** double 

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>即时计算方差 — 选择是否即时计算方差<div>off (默认) | on</div></summary>
</details>
<div class="details-content">

当选择**即时计算方差**参数时，该模块会按照输入的时间序列跟踪每个通道的方差值。

</div>
</div>

<div class="details-box">
<details open>
<summary>方差计算方式 — 方差计算的维度<div>Each column (默认) | Entire input | Each row</div></summary>
</details>
<div class="details-content">

可选项如下：

 - Each column — 该模块输出每列的方差。

 - Each row — 该模块输出每行的方差。

 - Entire input — 该模块输出整个输入的方差。

**依赖：** 取消勾选**即时计算方差**。

</div>
</div>

<div class="details-box">
<details open>
<summary>输入处理方式 — 在即时计算方差模式下处理输入的方法<div>Columns as channels (frame based)（默认）| Elements as channels (sample based)</div></summary>
</details>
<div class="details-content">

可选项如下：

 - Columns as channels (frame based) —— 该模块将输入的每一列视为一个单独的通道。当发生重置事件时，每个通道的运行方差将成为当前输入帧中所有样本的方差，直到当前输入样本。

 - Elements as channels (sample based) —— 该模块将输入的每个元素视为一个单独的通道。


**依赖：** 勾选**即时计算方差**。

</div>
</div>

<div class="details-box">
<details open>
<summary>复位触发方式 — 复位事件<div>None (默认) | Rising edge | Falling edge | Either edge | Non-zero sample</div></summary>
</details>
<div class="details-content">

当在可选的 Rst 端口检测到重置事件时，该模块都会重置运行方差。重置采样时间必须是输入信号采样时间的正整数倍。

当**输入处理**参数设置为**Elements as channels (sample based)**时发生重置事件，每个通道的运行方差将初始化为当前输入对应通道中的值。同样，当**输入处理**参数设置为 Columns as channels (frame based) 时，每个通道的运行方差将成为当前输入帧中所有样本（包括当前输入样本）的方差。

使用此参数指定重置事件。

 - None  - 禁用 Rst 端口。

 - Rising edge - 当 Rst 输入执行以下操作之一时触发重置操作：

   - 从负值上升到正值或零；

   - 从零上升到正值，但上升过程不是从负值上升到零的延续。

 - Falling edge — 当 Rst 输入发生以下任一情况时触发复位操作：

   - 从正值下降到负值或零；

   - 从零下降到负值，但下降过程并非从正值下降到零的延续。

 - Either edge — 当 Rst 输入为上升沿或下降沿时触发复位操作；

 - Non-zero sample — 当 Rst 输入不为零时，在每个采样时间触发复位操作。

**依赖：** 勾选**即时计算方差**。

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
