# PhaseFrequencyOffset
---
应用相位和频率偏移到复杂的基带信号。

**库：** TYCommunication / RFComponentModeling / ComponentsAndImpairments 

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYCommunication/RFComponentModeling/ComponentsAndImpairments/PhaseFrequencyOffset/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

相位/频率偏移块将相位和频率偏移应用于复杂信号。


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 复数信号输入<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

复信号，指定为复数标量或向量。

**数据类型：** double 

</div>
</div>
<div class="details-box">
<details open>
<summary>frequencyOffset— 频率偏移<div>矩阵</div></summary>
</details>
<div class="details-content">
 
频率偏移，指定为实数矩阵。

**依赖条件：** 要添加此端口，勾选**从端口输入频率偏移**选项。


**数据类型：** double 

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">
 
输出信号，作为复数标量或向量返回。

**数据类型：** double 

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>相位偏移(deg) — 相位偏移<div>{{30.0}}（默认）| 实数矩阵 </div></summary>
</details>
<div class="details-content">

以度为单位的相位偏移，指定为实数矩阵。
相位偏移 (deg) 和 频率偏移 (Hz) 维度必须相同。

</div>
</div>


<div class="details-box">
<details open>
<summary>从端口输入频率偏移 — 频率偏移端口输入使能<div>on（默认）| off</div></summary>
</details>
<div class="details-content">

选中此参数，表示添加 frequencyOffset 端口。

- 选择此参数时，frequencyOffset 端口指定频率偏移量；
- 不设置该参数时， **频率偏移 (Hz)** 指定频率偏移量。

</div>
</div>

<div class="details-box">
<details open>
<summary>输入频率偏移维度(Hz) — 频率偏移<div>{{0.0}}（默认）| 实数矩阵</div></summary>
</details>
<div class="details-content">

以赫兹为单位的频率偏移量，指定为实数矩阵。
相位偏移 (deg) 和 频率偏移 (Hz) 维度必须相同。

**依赖条件：** 要添加此端口，需取消勾选**从端口输入频率偏移**选项。

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
