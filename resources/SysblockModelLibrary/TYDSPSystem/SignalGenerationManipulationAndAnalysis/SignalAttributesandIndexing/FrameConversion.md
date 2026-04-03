# FrameConversion
---
&nbsp;

指定输出信号的采样方式。

**库：** TYDSPSystem / SignalGenerationManipulationAndAnalysis / SignalAttributesandIndexing 

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYDSPSystem/SignalGeneration/SignalAttributes/FrameConversion/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

FrameConversion 模块将输入传递到输出，并将输出基于为**输出采样模式**参数设定模式采样，该采样模式可以是基于帧的，也可以是基于采样的。输出采样模式也可以从参考输入端口的信号中继承，可以通过选择**输出信号是否继承参考信号**复选框来实现。

除了采样模式之外，FrameConversion 模块对输入信号不做任何改变。

## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div> 实数标量 | 实数向量</div></summary>
</details>
<div class="details-content">

输入数据，指定为实数标量或实数向量。

**数据类型：** double 

</div>
</div>

<div class="details-box">
<details open>
<summary>ref — 参考信号<div> 实数向量</div></summary>
</details>
<div class="details-content">

参考信号，指定为实数向量。选中**输出信号是否继承参考信号**复选框时可用。

**数据类型：** double 

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>实数向量</div></summary>
</details>
<div class="details-content">
 
输出数据，作为实值向量返回。输出维度与输入维度相匹配。

**数据类型：** double 

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>输出信号是否继承参考信号 — 设置输出是否继承参考信号<div>off（默认）| on </div></summary>
</details>
<div class="details-content">

输出是否采用继承采样端口：

- off -- 输出不继承采样端口，信号输出只与信号输入和**输出采样模式**有关；

- on -- 输出继承采样端口，同时信号输出也与信号输入和**输出采样模式**有关。

**数据类型：** String 

</div>
</div>

<div class="details-box">
<details open>
<summary>Sample mode  — 采样模式<div>Sample-based（默认）|Frame-based</div></summary>
</details>
<div class="details-content">

指定块应该如何处理输入。可设置为以下选项之一：

- Frame-based -- 当选择此选项时，模块将输入的每个列视为单独的通道；

- Sample-based -- 当选择此选项时，模块将输入的每个元素视为单独的通道。

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


<div class="details-box">
<details open>
<summary>参考信号维度 — 指定输入参考信号维度 <div>{1}（默认）| 长度为 1 的整型向量 </div></summary>
</details>
<div class="details-content">

指定输入参考信号的维度。指定为长度为 1 的整型向量。

</div>
</div>


# 版本历史记录

- 在 2025b 推出

## 限制信息

- 该模块暂不支持自动识别输入信号维度，需通过**输入信号维度**以及**参考信号维度**参数手动设定。
