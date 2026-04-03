# AWGNChannel
---
对输入信号添加白噪声。

**库：** TYCommunication / PropagationAndChannelModels 

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYCommunication/PropagationAndChannelModels/AWGNChannel/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

AWGNChannel 模块向输入信号添加高斯白噪声。它从输入信号中继承采样时间。


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

输入数据信号，指定为实数标量或向量。


**数据类型：** double 

</div>
</div>
<div class="details-box">
<details open>
<summary>var — 添加高斯白噪声的方差<div>正标量</div></summary>
</details>
<div class="details-content">
 
加性高斯白噪声的方差。

**依赖条件：** 

要采用此端口，将**模式**设置为 Variance，且**噪声方差源**设置为 Input port。


**数据类型：** double 


</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>y — 输出数据信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">
 
AWGN 通道的输出数据信号，以实数标量或向量的形式返回。

**数据类型：** double 

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>模式 — 方差模式<div>Signal to noise ratio (SNR)（默认）| Signal to noise ratio (Eb/No)|Signal to noise ratio (Es/No) |Variance </div></summary>
</details>
<div class="details-content">

方差模式，主要包括 noise ratio (Eb/No)、 Signal to noise ratio (Es/No)、 Signal to noise ratio (SNR) 和 Variance。

</div>
</div>


<div class="details-box">
<details open>
<summary>Eb/N0(dB) — 每符号信息比特能量与噪声功率谱密度之比<div>10（默认）| 标量</div></summary>
</details>
<div class="details-content">

每符号信息比特能量与噪声功率谱密度之比（以分贝为单位），指定为实数标量。信息比特能量是未进行信道编码时的幅度。

**依赖条件：** 

要采用此参数，将**模式**设置为 Signal to noise ratio (Eb/No)。

**数据类型：** double 

</div>
</div>

<div class="details-box">
<details open>
<summary>Es/N0(dB) — 每个符号的信息符号能量与噪声功率谱密度之比<div>10（默认）| 标量</div></summary>
</details>
<div class="details-content">

每个符号的信息符号能量与噪声功率谱密度之比（以分贝为单位），指定为实数标量。信息位能量是未进行信道编码时的幅度。

**依赖条件：** 

要采用此参数，将**模式**设置为 Signal to noise ratio (Es/No)。

**数据类型：** double 

</div>
</div>


<div class="details-box">
<details open>
<summary>SNR(dB) — 信噪比<div>10（默认）| 标量</div></summary>
</details>
<div class="details-content">

以分贝表示的信号功率与噪声功率之比。

**依赖条件：** 

要采用此参数，将**模式**设置为 Signal to noise ratio (SNR)。

**数据类型：** double 

</div>
</div>


<div class="details-box">
<details open>
<summary>每符号位数 — 每个输入符号的比特数目<div>1（默认）| 正整数标量</div></summary>
</details>
<div class="details-content">

每个输入符号中的位数，用标量指定。

**依赖条件：** 

要采用此参数，将**模式**设置为 Signal to noise ratio (Eb/No)。

**数据类型：** int32

</div>
</div>

<div class="details-box">
<details open>
<summary>输入信号功率 — 输入信号平均功率<div>1（默认）| 标量</div></summary>
</details>
<div class="details-content">

每个输入符号中的位数，用标量指定。

-当**模式**设置为 Signal to noise ratio (Eb/No)，代表参数是输入符号的均方幂；
-当**模式**设置为 Signal to noise ratio (SNR)， 代表该参数是输入样本的均方功率。


**依赖条件：** 

要采用此参数，将**模式**设置为 Signal to noise ratio (Eb/No), Signal to noise ratio (Es/No) 或 Signal to noise ratio (SNR)。

**数据类型：** double 

</div>
</div>


<div class="details-box">
<details open>
<summary>每符号采样率 — 信息信道的持续时间<div>1（默认）| 标量</div></summary>
</details>
<div class="details-content">

以秒为单位的符号周期，指定为正标量或矢量。当您使用此参数时，块确定在模型运行时要添加的采样时间和适当的噪声。

**依赖条件：** 

要采用此参数，将**模式**设置为 Signal to noise ratio (Eb/No), Signal to noise ratio (Es/No)。

**数据类型：** double

</div>
</div>

<div class="details-box">
<details open>
<summary>噪声方差源 — 指定噪声方差源<div>Parameter（默认）| Input port</div></summary>
</details>
<div class="details-content">

设置噪声方差源，可设置为 Parameter 或 Input port。

**依赖条件：** 

要采用此参数，将**模式**设置为 Variance。

**数据类型：** double 

</div>
</div>


<div class="details-box">
<details open>
<summary>噪声方差 — 白噪声方差<div>1（默认）| 标量</div></summary>
</details>
<div class="details-content">

高斯白噪声的方差，指定为标量。

**依赖条件：** 

要采用此参数，将**模式**设置为 Variance，且**噪声方差源** 设置为 Parameter。

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


<div class="details-box">
<details open>
<summary>随机数源 — 随机数源<div>Global stream（默认）| mt19937ar with seed</div></summary>
</details>
<div class="details-content">

高斯白噪声源，指定为 Global stream 或 mt19937ar with seed。

</div>
</div>

<div class="details-box">
<details open>
<summary>初始随机数种子 — 噪声生成器的随机数源<div>67（默认）| 正整数标量</div></summary>
</details>
<div class="details-content">

噪声生成器的初始种子。

**依赖条件：** 

要采用此端口，将随机数源设置为 mt19937ar with seed。

</div>
</div>

## 版本历史记录

- 在 2025b 推出

### 限制信息

- 该模块暂不支持自动识别输入信号维度，需通过**输入信号维度**参数手动设定
