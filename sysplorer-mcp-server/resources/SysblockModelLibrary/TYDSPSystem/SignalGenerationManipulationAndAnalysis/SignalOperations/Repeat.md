# Repeat
---
&nbsp;

通过重复值以更高的速率重新采样输入。

**库：** TYDSPSystem / SignalGenerationManipulationAndAnalysis / SignalOperations

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYDSPSystem/SignalGeneration/SignalOperations/Repeat/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

Repeat 模块将 $m × n$ 输入的每个通道的采样率提高到比输入采样率高L倍的速率。为此，该模块在输出处重复每个连续输入样本 L 次。


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>实数向量 | 实数向量</div></summary>
</details>
<div class="details-content">

指定输入信号为实值标量或向量。

**数据类型：** double 

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>实数向量 | 实数向量</div></summary>
</details>
<div class="details-content">
 
输出的维度取决于**重复数**的值以及在**速率设置**参数中选择的选项。
当设置**重复数**为 L，并且**速率设置**设置如下：
- Enforce single-rate processing - 该块通过将输出帧大小增加 L 倍来保持输入采样率；
- Allow multirate processing - 该块对信号进行重采样，使输出采样率比输入采样率快 L 倍，输出信号具有与输入信号相同的帧大小。

**数据类型：** double

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>重复数 — 对输入信号的重复计数<div>5（默认）| 正整数</div></summary>
</details>
<div class="details-content">

将重复数 L 指定为正整数。该值是模块重复输入值的次数，这是模块增加输出帧大小或采样率的因素。

</div>
</div>


<div class="details-box">
<details open>
<summary>输入处理 — 处理输入信号的方式<div>Columns as channels (frame based)（默认）| Elements as channels (sample based)</div></summary>
</details>
<div class="details-content">

通过将此参数设置为以下选项之一，指定模块应该如何处理输入：
- Columns as channels (frame based) -- 当选择此选项时，该模块将输入的每列视为单独的通道。在这种模式下，模块可以执行单速率或多速率处理；
- Elements as channels (sample based) -- 当选择此选项时，该模块将输入的每个元素视为单独的通道。在这种模式下，模块总是执行多速率处理。

</div>
</div>


<div class="details-box">
<details open>
<summary>速率设置 — 速率选项<div>Enforce single-rate processing （默认）| Allow multirate processing</div></summary>
</details>
<div class="details-content">

通过选择以下选项之一指定模块对输入进行采样的方法：
- Enforce single-rate processing - 当选择此选项时，模块通过将输出帧大小增加 1 倍来保持输入采样率，要采用该种方式，需要将**输入处理**设置为 Columns as channels (frame based)；
- Allow multirate processing - 当选择此选项时，模块对信号进行重新采样，使输出采样率比输入采样率快 L 倍。

</div>
</div>


<div class="details-box">
<details open>
<summary>初始条件 — 指定初始状态<div>0 （默认）| 实数标量</div></summary>
</details>
<div class="details-content">

指定用于初始化非零延迟情况时模块的输出值，指定为实数标量。需将**速率设置**选项设置为 Allow multirate processing 时生效。

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
