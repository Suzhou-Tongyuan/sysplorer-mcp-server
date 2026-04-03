# RaisedCosineTransmitFilter
---
通过升余弦 FIR 滤波器插值实现脉冲成形。

**库：** TYCommunication / PHYComponents / Filtering

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYCommunication/PHYComponents/Filtering/RaisedCosineTransmitFilter/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

升余弦发射滤波器模块通过采用升余弦有限长单位冲激响应 (FIR) 滤波器对输入信号进行插值处理，实现脉冲成形。该 FIR 滤波器的抽头系数数量为（符号滤波跨度 × 每符号输出采样数 + 1）。模块图标显示滤波器的冲激响应特性。


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 实数向量</div></summary>
</details>
<div class="details-content">

输入信号，可指定为标量、实数向量。

**数据类型：** double

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 实数向量</div></summary>
</details>
<div class="details-content">
 
输出信号以标量或实数向量返回。

**数据类型：** double

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>滤波器形状 — 滤波器形状<div>Square root（默认）| Normal</div></summary>
</details>
<div class="details-content">

可指定滤波器类型为 Square root 或 Normal。

</div>
</div>


<div class="details-box">
<details open>
<summary>滚动因子 — 滚动因子<div>0.2（默认）| 实数标量</div></summary>
</details>
<div class="details-content">

定义滤波器的频谱滚动因子，取值范围为 [0, 1] 的标量值。

**数据类型：** double

</div>
</div>


<div class="details-box">
<details open>
<summary>符号表示的滤波跨度 — 符号表示的滤波跨度<div>10（默认） | 正偶数</div></summary>
</details>
<div class="details-content">

指定符号级滤波长度为正偶数。模块将理想升余弦滤波器的无限冲激响应截断为 FIR 滤波器，其长度等于本参数值。

**数据类型：** int32 

</div>
</div>

<div class="details-box">
<details open>
<summary>线性幅度滤波器增益 — 线性幅度滤波器增益<div>1（默认） | 正实数标量</div></summary>
</details>
<div class="details-content">

线性幅度滤波器增益，指定为正实数标量。

**数据类型：** double 

</div>
</div>

<div class="details-box">
<details open>
<summary>输入处理方式 — 输入处理方式<div> Columns as channels (frame based) （默认）| Elements as channels (sample based)</div></summary>
</details>
<div class="details-content">

输入处理方式，指定为以下选项之一：

- Columns as channels (frame based) -- 该模块将输入的每一列视为一个单独的通道；
- Elements as channels (sample based) -- 该模块将输入的每个元素视为单独的通道。

</div>
</div>


<div class="details-box">
<details open>
<summary>速率设置 — 速率设置<div> Enforce single-rate processing（默认）| Allow multirate processing</div></summary>
</details>
<div class="details-content">

输入信号下采样和滤波的处理速率，指定为以下选项之一：

- Enforce single-rate processing -- 当选择此选项时，块保持输入采样率，并通过增加输出帧大小 K 来处理信号；
- Allow multirate processing -- 当选择此选项时，块处理信号使输出采样率比输入采样率快 K 倍。


**依赖条件：**为使用 Enforce single-rate processing 选项，需要将**输入处理方式**参数设置为 Columns as channels (frame based)。

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

### 限制信息

- 该模块暂不支持自动识别输入信号维度，需通过**输入信号维度**参数手动设定