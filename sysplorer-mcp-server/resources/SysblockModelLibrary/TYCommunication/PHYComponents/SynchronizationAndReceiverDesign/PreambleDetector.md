# PreambleDetector
---
检测数据包中的序文。

**库：** TYCommunication / PHYComponents / SynchronizationAndReceiverDesign 

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYCommunication/PHYComponents/SynchronizationAndReceiverDesign/PreambleDetector/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

PreambleDetector 模块检测数据包中的前言结束部分。序言是一组符号或位，用于基于分组的通信系统中，以指示分组的开始。包由前导数据和用户数据组成。在模拟运行期间，数据包的用户数据部分的长度可以变化。


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 信号输入<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

符号或位的输入数据，指定为实数标量、向量。输入的数据可以包含多个报文。

**数据类型：** double 

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>idx — 序列符号的索引<div>标量 | 向量</div></summary>
</details>
<div class="details-content">
 
最后一个序言符号的索引，作为实数标量或向量返回。

- 当**检测**参数设置为 All 时，idx 端口输出与每个检测到的序言的最后一个元素对应的索引；

- 当**检测**参数设置为 First 时，idx 端口输出与第一个检测到的序言的最后一个元素对应的索引。

**数据类型：** double 

</div>
</div>

<div class="details-box">
<details open>
<summary>xcor — 检测度量<div>标量 | 向量</div></summary>
</details>
<div class="details-content">
 
检测度量，作为与输入数据包In具有相同维度和数据类型的标量或列向量返回。检测度量是前导和输入数据的相互关系。

**数据类型：** double 

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>输入处理方式 — 输入形式<div>Symbol（默认）| Bit </div></summary>
</details>
<div class="details-content">

输入处理形式，包括 Symbol 和 Bit。

- 对于二进制输入，将参数设置为 Bit；
- 对于其他输入，将参数设置为 Symbol。


**数据类型：** String 

</div>
</div>


<div class="details-box">
<details open>
<summary>参考序列 — 序言序列<div>{1.0, 1}（默认）| 实数向量</div></summary>
</details>
<div class="details-content">

序言序列，指定为列向量。

- 如果**输入处理方式**参数设置为 Bit，则序言必须为二进制；
- 如果**输入处理方式**参数设置为 Symbol，则序言可以是任何实数。

**数据类型：** double 

</div>
</div>

<div class="details-box">
<details open>
<summary>参考门限 — 判决门限<div>3（默认）| 非负标量</div></summary>
</details>
<div class="details-content">

检测阈值，指定为非负标量。当检测指标大于等于阈值时，块检测序言，更新Idx。

**依赖条件：** 

要使用该参数，将**输入处理方式**参数设置为 Symbol。

**数据类型：** double 

</div>
</div>


<div class="details-box">
<details open>
<summary>输出检测度量 — 输出度量检测<div> off（默认）| on</div></summary>
</details>
<div class="details-content">

选择此参数输出检测指标，开启DtMt输出端口。

**依赖条件：** 
要使用该参数，将**输入处理方式**参数设置为 Symbol。

</div>
</div>


<div class="details-box">
<details open>
<summary>检测 — 检测方式<div> All（默认）| First</div></summary>
</details>
<div class="details-content">

返回的检测，指定为 All 或者 First。指定 All 返回所有检测到的前言，指定 First 则只返回第一个检测到的序言。


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
