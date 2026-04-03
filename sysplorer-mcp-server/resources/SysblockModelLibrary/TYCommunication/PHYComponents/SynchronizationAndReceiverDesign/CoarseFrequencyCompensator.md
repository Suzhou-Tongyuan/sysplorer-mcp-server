# CoarseFrequencyCompensator
---
补偿 PAM、PSK 或 QAM 中的载波频率偏移。

**库：** TYCommunication / PHYComponents / SynchronizationAndReceiverDesign 

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYCommunication/PHYComponents/SynchronizationAndReceiverDesign/Coarse/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

CoarseFrequencyCompensator 模块在 QAM、8-PSK、BPSK、OQPSK、PAM 和 QPSK 调制方案中补偿载波频率偏移。


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入数据信号<div>向量</div></summary>
</details>
<div class="details-content">

输入信号，指定为复数向量。

**数据类型：** double 

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 输出补偿信号<div>复数向量</div></summary>
</details>
<div class="details-content">
 
补偿输出信号，作为与输入 u 具有相同维数和数据类型的复数向量返回。

**数据类型：** double 

</div>
</div>


<div class="details-box">
<details open>
<summary>FreqEst — 频率偏移估计<div>标量</div></summary>
</details>
<div class="details-content">
 
频率偏移估计，指定为标量返回。

**依赖条件** 

 要添加此端口，需勾选**频率偏移输出端口**选项。

 **数据类型：** double 

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>输入信号调制方式 — 指定输入信号调制方式调制方式<div>QAM（默认）| 8PSK | BPSK | OQPSK | PAM | QPAK </div></summary>
</details>
<div class="details-content">

调制类型，指定为 QAM、8PSK、BPSK、OQPSK、PAM 或 QPSK。

</div>
</div>


<div class="details-box">
<details open>
<summary>估计算法 — 频偏估计算法<div>FFT-based（默认）| Correlation-based</div></summary>
</details>
<div class="details-content">

指定频率偏移估计算法指定为 FFT-based 或 Correlation-based。

:::warning 注意

将**输入信号调制方式**类型设置为 OQPSK 或 QAM 时，该模块使用 FFT-based 估计算法。

:::

**依赖条件：** 

要采用该参数，将**输入信号调制方式**设置为 8PSK、 BPSK、 PAM、 或 QPSK。


</div>
</div>


<div class="details-box">
<details open>
<summary>频率分辨率(Hz) — 频率分辨率<div>0.001（默认）| 正标量</div></summary>
</details>
<div class="details-content">

以Hz为单位的频率分辨率，指定为正实标量。

**依赖条件：** 
当**输入信号调制方式**选择 OQPSK 或 QAM，或**估计算法**设置 FFT-based时，应用此参数。

**数据类型：** double 


</div>
</div>

<div class="details-box">
<details open>
<summary>每符号样本数 — 符号采样数<div>4（默认）| 不少于 4 的偶数标量</div></summary>
</details>
<div class="details-content">

每个符号的样本数，指定为不少于 4 的偶数标量。


**依赖条件：** 

当**输入信号调制方式**选择 OQPSK 时，应用此参数。

**数据类型：** int32 

</div>
</div>


<div class="details-box">
<details open>
<summary>最大频偏(Hz) — 最大可测频偏<div>0.05（默认）| 正标量</div></summary>
</details>
<div class="details-content">

以秒为单位的符号周期，指定为正标量。当您使用此参数时，块确定在模型运行时要添加的采样时间和适当的噪声。

**依赖条件：** 

要采用此端口，将**估计算法**设置为 Correlation-based。

**数据类型：** double 

</div>
</div>


<div class="details-box">
<details open>
<summary>估计频率偏移输出端口 — 估计频率偏移输出端口使能<div>on（默认）| off</div></summary>
</details>
<div class="details-content">

选中此复选框以添加 FreqEst 输出端口。FreqEst 端口以Hz为单位输出估计的频率偏移。

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
