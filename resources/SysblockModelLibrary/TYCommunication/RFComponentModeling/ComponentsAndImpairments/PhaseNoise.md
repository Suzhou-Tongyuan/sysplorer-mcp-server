# PhaseNoise
---
相位噪声。

**库：** TYCommunication / RFComponentModeling / ComponentsAndImpairments

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYCommunication/RFComponentModeling/ComponentsAndImpairments/PhaseNoise/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

相位噪声模块将相位噪声添加到复杂信号中。该模块模拟由无线通信发射机或接收机的本地振荡器引入的损伤。该块根据指定的频谱掩模产生滤波后的相位噪声，并将其加到输入信号中。 


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


### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">
 
输出信号，作为与输入信号具有相同数据类型和大小的信号返回。

**数据类型：** double 

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>相位噪声 — 相位噪声<div>{-80, -100}（默认）| 向量</div></summary>
</details>
<div class="details-content">

相位噪声水平，以分贝为单位，相对于载波每赫兹（dBc/Hz），指定为负实数向量。

**数据类型：** double 

</div>
</div>


<div class="details-box">
<details open>
<summary>频率偏移 — 频率偏移<div>{2000.0, 20000}（默认）| 向量</div></summary>
</details>
<div class="details-content">

以 Hz 为单位的频率偏移，指定为正递增值的实数向量。最大频率偏移值必须小于 Fs / 2，其中 Fs 为**采样频率**参数值。**相位噪声**和**频率偏移**的长度必须相同。

**数据类型：** double 

</div>
</div>


<div class="details-box">
<details open>
<summary>采样频率 — 采样率<div>1e6（默认）| 正标量 </div></summary>
</details>
<div class="details-content">

采样率（以 Hz 为单位），指定为大于**频率偏移**参数所指定最大值的两倍的正标量。

**数据类型：** double

</div>
</div>


<div class="details-box">
<details open>
<summary>初始化随机数种子 — 噪声随机数种子<div>2137（默认）| 正整数标量</div></summary>
</details>
<div class="details-content">

噪声发生器的初始种子，指定为正整数标量。

**数据类型：** double

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
