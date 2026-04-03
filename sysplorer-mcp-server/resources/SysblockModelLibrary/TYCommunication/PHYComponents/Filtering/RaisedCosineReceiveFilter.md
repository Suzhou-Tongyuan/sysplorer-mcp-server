# RaisedCosineReceiveFilter
---
通过升余弦 FIR 滤波器下采样实现脉冲成形。

**库：** TYCommunication / PHYComponents / Filtering 

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYCommunication/PHYComponents/Filtering/RaisedCosineReceiveFilter/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

升余弦接收滤波器模块使用上升余弦有限脉冲响应（FIR）滤波器滤波输入信号，并选择性地抽取滤波后的信号。FIR 滤波器具有（符号表示的滤波器跨度 × 每个符号的输入样本数 + 1）抽头系数。


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div> 标量 | 实数向量</div></summary>
</details>
<div class="details-content">

输入信号，可指定为标量或实数向量。


**数据类型：** double 

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div> 标量 | 实数向量</div></summary>
</details>
<div class="details-content">
 
通过升余弦 FIR 滤波器下采样后的输出信号。

**数据类型：** double 

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>滤波器形状 — 滤波器形状<div>Square root（默认）| Normal </div></summary>
</details>
<div class="details-content">

滤波器形状，指定为 Square root 或 Normal。

</div>
</div>

<div class="details-box">
<details open>
<summary>滚动因子 — 滚动因子<div>0.2（默认）| 实数标量 </div></summary>
</details>
<div class="details-content">

滤波器滚降系数，指定为 $(0,1]$ 内的实数标量。

**数据类型：** double 

</div>
</div>

<div class="details-box">
<details open>
<summary>符号表示的滤波跨度 — 符号表示的滤波跨度<div>10（默认）|偶数正整数</div></summary>
</details>
<div class="details-content">

以符号表示的滤波器范围，指定为偶数正整数。该块将理想的提升余弦滤波器的无限脉冲响应长度截断为长度等于该参数值的 FIR。


**数据类型：** int32 

</div>
</div>


<div class="details-box">
<details open>
<summary>每个符号的输入样本数 — 每个符号的输入样本数<div>8（默认）| 大于1的正整数</div></summary>
</details>
<div class="details-content">

每个符号的输入样本数，指定为大于 1 的整数值。这个参数定义了在输入信号中代表一个符号的输入样本的数量。

**数据类型：** int32

</div>
</div>


<div class="details-box">
<details open>
<summary>抽取因子 — 抽取因子<div> 8（默认）| 正整数标量</div></summary>
</details>
<div class="details-content">

应用于输入信号的抽取因子（Decimationfactor），指定为正整数。每个符号的输出样本值等于每个符号的输入样本值除以抽取因子。如果抽取因子为 1，则该模块只应用滤波而不进行抽取。

**数据类型：** int32

</div>
</div>


<div class="details-box">
<details open>
<summary>抽取偏移 — 抽取因子<div> 0（默认）| 标量</div></summary>
</details>
<div class="details-content">

采样中的抽取偏移量，指定为 [0，Decimationfactor - 1] 范围内的整数。

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

- Enforce single-rate processing -- 当选择此选项时，模块保持输入采样率，并通过减少输出帧大小 K 来处理信号；
- Allow multirate processing -- 当选择此选项时，模块处理信号使输出采样率比输入采样率慢 K 倍。


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