# BiquadFilter
---
&nbsp;

使用 Biquad 结构实现一个通用 IIR 滤波器。

**库：**  TYDSPSystem / FilterImplementation / SingleRateFilters

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYDSPSystem/FilterImplementation/SingleRateFilters/BiquadFilter/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

BiquadFilter 模块使用指定的二阶节无限冲激响应（IIR）滤波器对输入信号的每个通道进行独立滤波。


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div> 实数向量</div></summary>
</details>
<div class="details-content">

输入信号，指定为长度为 N 的列向量。

**数据类型：** double 

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>实数向量</div></summary>
</details>
<div class="details-content">
 
输出信号，与输入信号维度一致。

**数据类型：** double 

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>SOS 矩阵 — SOS 矩阵<div>{{1, 0.3, 0.4, 1, 0.1, 0.2}} (默认) | M × 6 矩阵</div></summary>
</details>
<div class="details-content">

指定一个 M×6 的矩阵，其中 M 为二阶节滤波器的节数。该二阶节（SOS）矩阵的每一行均包含滤波器对应节段的分子系数和分母系数。

</div>
</div>

<div class="details-box">
<details open>
<summary>缩放值 - 缩放值<div>{1.0, 1.0}| 长度为 M+1 的实数向量</div></summary>
</details>
<div class="details-content">

指定二阶节（SOS）滤波器各节段之间使用的缩放值，指定为长度为 M+1 的向量：

</div>
</div>

<div class="details-box">
<details open>
<summary>初始条件 — 指定滤波器初始状态<div>0（默认）| 实数标量</div></summary>
</details>
<div class="details-content">

指定滤波器状态的初始条件。

</div>
</div>

<div class="details-box">
<details open>
<summary>输入信号维度 — 指定输入信号维度<div>{1}（默认）| 长度为 1 的整型向量</div></summary>
</details>
<div class="details-content">

指定输入信号的维度。指定为长度为 1 的整型向量。

</div>
</div>


## 版本历史记录

- 在 2025b 推出

## 限制信息

- 该模块暂不支持自动识别输入信号维度，需通过**输入信号维度**参数手动设定。