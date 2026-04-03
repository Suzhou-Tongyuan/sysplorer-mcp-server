# Buffer
---
&nbsp;

将输入序列缓冲为更小或更大的帧大小。

**库：** TYDSPSystem / SignalGenerationManipulationAndAnalysis / BuffersSwitchesAndCounters 

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYDSPSystem/SignalGeneration/Buffers/Buffer/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

缓冲区模块总是执行基于帧的处理，重新分配输入的每列中的数据，以产生具有不同帧大小的输出。将信号缓冲为更大的帧会产生比输入帧速率慢的输出帧速率。


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div> 标量 | 向量</div></summary>
</details>
<div class="details-content">

输入信号，指定为实数标量或向量。

**数据类型：** double 

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">
 
输出信号，由**输出缓冲区大小**参数指定。

**数据类型：** double 

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>输出缓冲区大小 — 输出缓冲区大小<div>64（默认）| 正整数 </div></summary>
</details>
<div class="details-content">

指定从缓冲区到输出帧的连续采样的个数。

</div>
</div>


<div class="details-box">
<details open>
<summary>缓冲重叠 — 指定缓冲重叠数量<div>0（默认）| 非负整数 </div></summary>
</details>
<div class="details-content">

指定每个连续输出帧中重叠样本的数量。限制为小于**输出缓冲区大小**参数的非负整数。

</div>
</div>


<div class="details-box">
<details open>
<summary>初始条件 — 指定缓冲输出<div>0（默认）| 实数标量 </div></summary>
</details>
<div class="details-content">

在非零延迟的情况下，指定模块的初始输出值。

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