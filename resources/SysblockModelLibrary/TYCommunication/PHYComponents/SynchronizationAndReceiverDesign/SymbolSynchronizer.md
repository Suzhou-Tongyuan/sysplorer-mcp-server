# SymbolSynchronizer
---
纠正符号计时时钟偏差。

**库：** TYCommunication / PHYComponents / SynchronizationAndReceiverDesign 

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYCommunication/PHYComponents/SynchronizationAndReceiverDesign/SymbolSynchronizer/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

SymbolSynchronizer 模块校正单载波发射器和接收器之间的 PAM、PSK、QAM 或 OQPSK 调制方案的符号定时时钟偏差。


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入样本<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

输入样本，指定为PAM， PSK， QAM 或 OQPSK调制的单载波信号的复数标量或向量。

**数据类型：** double 

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">
 
输出信号符号。

**数据类型：** double 

</div>
</div>

<div class="details-box">
<details open>
<summary>err — 时间误差估计<div>实数向量</div></summary>
</details>
<div class="details-content">
 
每个输入样本的估计定时误差，以标量或列向量的形式返回，其值范围为 [0,1]。估计的定时误差由输入样本时间归一化。err 与输入信号具有相同的数据类型和大小。

**依赖关系：**

要采用此端口，勾选**差错输出有效位**选项。

**数据类型：** double 

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>调制方式 — 调制类型<div>QAM（默认）| PAM | PSK | OQPSK </div></summary>
</details>
<div class="details-content">

调制类型，指定为 PAM / PSK / QAM 或 OQPSK。

</div>
</div>


<div class="details-box">
<details open>
<summary>时间差错检测方式 — 时间误差检测器<div>Zero-Crossing (decision-directed)（默认）| Gardner (non-data-aided) | Early-Late (non-data-aided) | Mueller-Muller (decision-directed)</div></summary>
</details>
<div class="details-content">

定时错误检测器的类型，指定为 Zero-Crossing（决策导向）、Gardner（非数据辅助）、Early-Late（非数据辅助）或 Mueller-Muller（决策导向）。该参数指定同步器中使用的定时错误检测方案。

</div>
</div>

<div class="details-box">
<details open>
<summary>每帧采样数  — 符号采样数<div>2（默认）| 大于1的正整数</div></summary>
</details>
<div class="details-content">

每个符号的样本数，指定为大于1的正整数。

**数据类型：** int32

</div>
</div>


<div class="details-box">
<details open>
<summary>环路滤波器阻尼系数 — 环路滤波器的阻尼因子<div> 1（默认）| 正标量</div></summary>
</details>
<div class="details-content">

环路滤波器的阻尼因子，指定为正标量。

**数据类型：** int32

</div>
</div>


<div class="details-box">
<details open>
<summary>环路滤波器的归一化带宽 — 环路滤波器的归一化带宽<div> 0.01（默认）| 小于1的标量</div></summary>
</details>
<div class="details-content">

环路滤波器的归一化带宽，指定为小于1的正标量。环路带宽（Bn）由输入信号的符号率（Ts）归一化。

:::warning 注意

要确保符号同步器锁定，请将归一化环路带宽参数设置为小于0.1的值。
:::

**数据类型：** double

</div>
</div>


<div class="details-box">
<details open>
<summary>相位检测器增益  — 检测器增益<div> 2.7（默认）| 正标量</div></summary>
</details>
<div class="details-content">

相位检测器增益，指定为正标量。

**数据类型：** double

</div>
</div>


<div class="details-box">
<details open>
<summary>差错输出有效位 — 归一化时间差错使能端口<div> on（默认）| off</div></summary>
</details>
<div class="details-content">

选择该参数，输出 err的规范化定时错误数据。


**数据类型：** String

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
