# Unbuffer
---
&nbsp;

将缓冲输入帧解除为标量输出序列。

**库：** TYDSPSystem / SignalGenerationManipulationAndAnalysis / BuffersSwitchesAndCounters 

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYDSPSystem/SignalGeneration/Buffers/Unbuffer/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

Unbuffer 模块将缓冲输入帧解除为标量输出序列。即，模块输入是逐行无缓冲的，模块接收输入的速率通常小于模块产生输出的速率。


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
<summary>y — 输出信号<div>标量</div></summary>
</details>
<div class="details-content">
 
输出信号，将输入信号帧以更高的采样速率输出。

**数据类型：** double 

</div>
</div>


## 参数

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