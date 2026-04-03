# EdgeDetector
---
&nbsp;

响应从零到非零值的转换，输出一个采样周期的单位幅度脉冲。

**库：** TYDSPSystem / SignalGenerationManipulationAndAnalysis / BuffersSwitchesAndCounters 

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYDSPSystem/SignalGeneration/Buffers/EdgeDetector/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

当输入的相应通道从零转换为非零值时，边缘检测器模块会在给定的输出通道中生成一个脉冲。当输入未从零转换为非零值时，该模块会在相应的输出通道中生成零。

此模块仅支持离散时间固定步长信号。不支持连续信号。

输出具有与输入相同的维度和采样率。将**输入处理**参数设置为 **Columns as channels (frame based)** 时，该模块会计算包含非零值的帧中跨两个连续帧的边缘。例如，如果第一帧的底部有一个零，而第二帧的顶部有一个非零值，则该模块会计算第二帧中的边缘。


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
<summary>输入处理 — 输入数据的处理方式<div>Columns as channels (frame based)（默认）| Elements as channels (sample based) </div></summary>
</details>
<div class="details-content">

指定模块如何处理输入。可以将此参数设置为以下选项之一：

 - Columns as channels (frame based)（默认）—— 选择此选项时，模块会将输入的每一列视为一个单独的通道。

 - Elements as channels (sample based) —— 选择此选项时，模块会将输入的每个元素视为一个单独的通道。

</div>
</div>

<div class="details-box">
<details open>
<summary>输入信号维度 — 指定输入信号维度 <div>{1}（默认）| 长度为 1 的整型向量 </div></summary>
</details>
<div class="details-content">

指定输入信号的维度。指定为长度为 1 的整型向量。

</div>
</div>

# 版本历史记录

- 在 2025b 推出

## 限制信息

- 该模块暂不支持自动识别输入信号维度，需通过**输入信号维度**参数手动设定。
