# ComplexPhaseShift
---
对复信号应用复相移。

**库：** TYCommunication / RFComponentModeling / ComponentsAndImpairments 

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYCommunication/RFComponentModeling/ComponentsAndImpairments/ComplexPhaseShift/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

ComplexPhaseShift 模块对复信号进行复相移。


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

输入信号，指定为复数标量或向量。


**数据类型：** double 

</div>
</div>
<div class="details-box">
<details open>
<summary>phase — 相位偏移<div>标量 | 向量</div></summary>
</details>
<div class="details-content">
 
以弧度为单位的相移，指定为复数标量或向量。如果相移是非标量的，它必须与端口 u 的信号具有相同的维数。

**数据类型：** double 

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>y — 相移信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">
 
相移信号，指定为复数标量或向量。。该输出与输入信号具有相同的维度和数据类型。

**数据类型：** double 

</div>
</div>

### 参数
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
