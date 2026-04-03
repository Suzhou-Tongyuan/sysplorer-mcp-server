# CarrierSynchronizer
---
补偿载波频率偏移。

**库：** TYCommunication / PHYComponents / SynchronizationAndReceiverDesign 

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYCommunication/PHYComponents/SynchronizationAndReceiverDesign/CarrierSynchronizer/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

CarrierSynchronizer 模块补偿使用单载波调制方案的信号中的载波频率和相位偏移。载波同步器算法兼容BPSK、QPSK、OQPSK、8-PSK、PAM 和矩形 QAM 调制方案。


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

输入样本，指定为复数标量或向量。


**数据类型：** double 

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 相位补偿信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">
 
相位校正输出信号，作为与输入信号具有相同数据类型和长度的标量或向量返回。输出信号调节输入信号，补偿使用单载波调制方案的信号中的载波频率和相位偏移。

**数据类型：** double 

</div>
</div>

<div class="details-box">
<details open>
<summary>phaseex— 弧度相位估计<div>实数向量</div></summary>
</details>
<div class="details-content">
 
以弧度为单位的相位估计，作为与输入信号长度相同的标量或列向量返回。

**依赖关系：**

要采用此端口，需勾选**估计相位误差输出端口**选项。

**数据类型：** double 

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>调制类型 — 调制类型<div>QAM（默认）| 8PSK | PAM | BPSK | OQPSK | QPSK </div></summary>
</details>
<div class="details-content">

调制类型，指定为 QAM / QPSK / BPAK / 8PSK / QAM / OQPSK。

</div>
</div>

<div class="details-box">
<details open>
<summary>调制相位偏移 — 调制相位偏移方式<div>Auto（默认）| Custom </div></summary>
</details>
<div class="details-content">

调制相位偏移方法，指定为 Auto 或 Custom。

</div>
</div>

<div class="details-box">
<details open>
<summary>自定义相位偏移 — 自定义相位偏移<div>0（默认）|标量</div></summary>
</details>
<div class="details-content">

以弧度为单位的自定义相位偏移，指定为标量。

**依赖关系：** 

要采用此端口，请将**调制相位偏移**设置为 Custom。

**数据类型：** double 

</div>
</div>


<div class="details-box">
<details open>
<summary>每个符号对应样本数  — 符号采样数<div>2（默认）| 正整数</div></summary>
</details>
<div class="details-content">

每个符号的样本数，指定为正整数。

**数据类型：** int32

</div>
</div>


<div class="details-box">
<details open>
<summary>阻尼因子 — 环路滤波器的阻尼因子<div> 0.707（默认）| 正标量</div></summary>
</details>
<div class="details-content">

环路滤波器的阻尼因子，指定为正标量。

**数据类型：** double

</div>
</div>


<div class="details-box">
<details open>
<summary>归一化环路带宽 — 环路滤波器的归一化带宽<div> 0.01（默认）| 小于1的标量</div></summary>
</details>
<div class="details-content">

环路的归一化带宽，指定为 (0,1] 范围内的标量。环路带宽由同步器的采样率归一化。减小环路带宽减少了同步器的收敛时间，同时也减小了同步器的拉入范围。

**数据类型：** double

</div>
</div>


<div class="details-box">
<details open>
<summary>估计相位误差输出端口  — 相位估计差错使能端口<div> on（默认）| off</div></summary>
</details>
<div class="details-content">

选择此复选框可向输出端口phEst提供估计的相位误差。

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
