# Convert1Dto2D
---
&nbsp;

将一维或二维输入转换为具有指定尺寸的二维矩阵。

**库：** TYDSPSystem / SignalGenerationManipulationAndAnalysis / SignalAttributesandIndexing 

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYDSPSystem/SignalGeneration/SignalAttributes/Convert1Dto2D/1.png')" style="width: 100px; border:black 1px solid;height: auto; transform: scale(1);">

## 描述

Convert1Dto2D 模块支持将一维或二维输入转换为具有指定尺寸的二维矩阵。输入元素的总数必须在输出中保持不变，例如长度为 6 的向量和 2 乘 3 的矩阵都可以被整形为相同的 3 乘 2 的输出矩阵。


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div> 实数标量 | 实数向量 | 实数矩阵</div></summary>
</details>
<div class="details-content">

输入数据，指定为实数标量、实数向量、实数矩阵。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>实数矩阵</div></summary>
</details>
<div class="details-content">
 
输出数据，作为实值矩阵返回。输入元素的总数必须在输出中保持不变。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean 

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>输出行数 — 设置输出矩阵的行数<div>1（默认）| 正整数</div></summary>
</details>
<div class="details-content">

输出矩阵的行数。

</div>
</div>

<div class="details-box">
<details open>
<summary>输出列数 — 设置输出矩阵的列数<div>1（默认）| 正整数</div></summary>
</details>
<div class="details-content">

输出矩阵的列数。

</div>
</div>

<!-- 
<div class="details-box">
<details open>
<summary>基于帧输出 — 指定是否基于帧输出 <div>off（默认）| on </div></summary>
</details>
<div class="details-content">

指定是否基于帧输出。

</div>
</div>
-->


## 版本历史记录

- 在 2026a 推出

## 限制信息

- 该模块暂不支持**基于帧输出**参数设置。
