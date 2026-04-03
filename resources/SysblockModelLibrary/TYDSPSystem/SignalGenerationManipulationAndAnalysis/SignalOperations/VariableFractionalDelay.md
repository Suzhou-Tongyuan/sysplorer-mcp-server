# VariableFractionalDelay
---
&nbsp;

可变分数延迟。

**库：** TYDSPSystem / SignalGenerationManipulationandAnalysis / SignalOperations

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYDSPSystem/SignalGeneration/SignalOperations/VariableFractionalDelay/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

可变分数延迟块可将输入信号沿输入的每个通道延迟指定数量的分数采样。该模块还可以同时计算同一信号的多个延迟版本（抽头）。

当延迟值为分数时，模块会对输入信号进行插值，以非整数采样间隔获取新样本。可以将插值模式参数设置为线性、FIR 或 Farrow。该模块支持时变延迟值。即延迟值可以在一帧内从一个样本到另一个样本之间变化。

## 端口

### 输入

<div class="details-box">
<details open>
<summary>data — 输入信号<div>实数向量</div></summary>
</details>
<div class="details-content">

待延迟的输入信号。

将数据输入指定为实数向量。数据输入必须与延迟输入的数据类型相同。

**数据类型：** double

</div>
</div>

<div class="details-box">
<details open>
<summary>delay_arr — 延迟输入<div>实数向量</div></summary>
</details>
<div class="details-content">

将延迟输入指定为实数向量。延迟输入可以是整数，也可以是分数。模块对信号进行内插，以非整数采样间隔获取新的采样。延迟输入的数据类型必须与数据输入相同。

**数据类型：** double

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>var — 延迟处理后的信号<div>实数向量</div></summary>
</details>
<div class="details-content">

延迟输出，以实数向量形式返回。输出的数据类型与数据输入的数据类型相匹配。

**数据类型：** double

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>插值方式 — 插值方式<div>Linear（默认）| FIR </div></summary>
</details>
<div class="details-content">

指定插值方式。模块对信号进行内插，以非整数采样间隔获取新样本。

 - Linear（默认） —— 线性内插。在此模式下，模块会存储输入端口接收到的每个通道的 Dmax+1 个最新采样。Dmax 是在最大延迟 (Dmax) 样本参数中指定的值；

 - FIR —— 多相 FIR 插值。在此模式下，模块存储输入端口为每个通道接收的 Dmax+P+1 个最新采样。P 是在插值滤波器半长 (P) 参数中指定的值；


</div>
</div>


<div class="details-box">
<details open>
<summary>插值滤波器半长 — 插值滤波器长度的一半<div>100（默认值） | 范围 [0 65535] 内的整数</div></summary>
</details>
<div class="details-content">

有限冲激响应（FIR）插值滤波器的半长度。对于周期性信号而言，该属性值越大（意味着滤波器阶数越高），对延迟输出样本的估计效果就越好。通常，属性值取 4 至 6 （对应 7 阶至 11 阶滤波器）便已足够。

</div>
</div>


<div class="details-box">
<details open>
<summary>输入采样插值点数 — 输入采样插值点数量<div>10（默认值） | 范围 [2 65535] 内的整数</div></summary>
</details>
<div class="details-content">

针对每个输入样本所计算唯一有限冲激响应（FIR）插值滤波器时所采用的插值点数量。

</div>
</div>


<div class="details-box">
<details open>
<summary>采样最大延迟 — 最大延迟<div>100（默认值） | 范围 [0 65535] 内的整数</div></summary>
</details>
<div class="details-content">

模块能产生的最大延迟，Dmax。超过此最大值的输入延迟值将被剪切为 Dmax。

</div>
</div>

<div class="details-box">
<details open>
<summary>输入处理 — 处理输入信号的方式<div>Columns as channels (frame based)（默认）| Elements as channels (sample based)</div></summary>
</details>
<div class="details-content">

指定该模块应如何处理输入数据。

</div>
</div>

<div class="details-box">
<details open>
<summary>初始状态 — 初始状态<div>0（默认值） | 标量 | 1 × R × D 数组 | 1 × R × (D+L) 数组</div></summary>
</details>
<div class="details-content">

指定模拟开始时模块内存中的初始值。

</div>
</div>

<div class="details-box">
<details open>
<summary>FIR模式输入延迟方式 — 指定最小输入延迟方式<div>Clip to the minimum value necessary for centered kernel (默认) | Use off-centered kernel | Switch to linear interpolation if kernel cannot be centered</div></summary>
</details>
<div class="details-content">

指定当输入延迟值太小而无法使内核居中时块的行为。

</div>
</div>

<div class="details-box">
<details open>
<summary>输入信号与延迟维度 — 输入信号与延迟维度<div>{1}（默认）| 长度为 1 的整型向量</div></summary>
</details>
<div class="details-content">

指定输入信号以及输入延迟的维度。指定为长度为 1 的整型向量。

</div>
</div>

## 版本历史记录

- 在 2025b 推出

## 限制信息

- 该模块暂不支持自动识别输入信号维度，需通过**输入信号与延迟维度**参数手动设定。