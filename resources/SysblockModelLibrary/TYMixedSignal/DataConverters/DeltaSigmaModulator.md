# DeltaSigmaModulator
---
基于 Delta Sigma 调制器的 ADC 模型。

**库：** TYMixedSignal / DataConverters

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYMixedSignal/DataConverters/DeltaSigmaModulator/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

DeltaSigmaModulator 模块可对基于 Delta Sigma 调制技术的 ADC 进行建模，支持以下四种架构类型：

 - CIFB：带反馈的积分器级联
 - CRFB：带反馈的谐振器级联
 - CIFF：带前馈的积分器级联
 - CRFF：带前馈的谐振器级联


该模块支持 1 阶至 6 阶的 Delta Sigma 调制器（DSM）建模，并可用于设计多级噪声整形（MASH）和稳健型 MASH（S-MASH）等级联结构，同时支持电路级噪声建模。

## 端口

### 输入

<div class="details-box">
<details open>
<summary>input — 模拟输入信号<div>实数标量</div></summary>
</details>
<div class="details-content">

模拟输入信号，标量。

**数据类型：** double

</div>
</div>


<div class="details-box">
<details open>
<summary>reset — Delta Sigma 调制器复位信号<div>实数标量</div></summary>
</details>
<div class="details-content">

复位信号，标量。

**数据类型：** double

</div>
</div>


<div class="details-box">
<details open>
<summary>feedback — 下一级输出反馈<div>实数标量</div></summary>
</details>
<div class="details-content">

来自下一级的输出反馈信号，标量。建模多级 DSM 时，通过此端口将输出反馈至模块；若无反馈，则接地。用于构建 MASH 和 S-MASH 等级联结构。

**数据类型：** double

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>dsmOut — 数字输出信号<div>实数标量</div></summary>
</details>
<div class="details-content">
 
数字输出信号，标量。

**数据类型：** double

</div>
</div>

<div class="details-box">
<details open>
<summary>filterOut — 环路滤波器输出<div>实数标量</div></summary>
</details>
<div class="details-content">
 
Delta Sigma 调制器内部环路滤波器的输出，标量。

**数据类型：** double

</div>
</div>

<div class="details-box">
<details open>
<summary>quantOut — 量化器输出<div>实数标量</div></summary>
</details>
<div class="details-content">
 
Delta Sigma 调制器内部量化器的输出，标量。若未使用此端口，需连接至终结器；若未使用反馈端口，则 quantOut 与 dsmOut值相同，用于构建 MASH 和 S-MASH 等级联结构。

**数据类型：** int8

</div>
</div>


## 参数

### 输入参数

<div class="details-box">
<details open>
<summary>Delta Sigma 调制器架构 — Delta Sigma 调制器架构<div> CIFB（默认） </div></summary>
</details>
<div class="details-content">

选择 Delta Sigma 调制器的架构类型：

 - CIFB（默认）：反馈积分器级联
 - CRFB：反馈谐振器级联
 - CIFF：前馈积分器级联
 - CRFF：前馈谐振器级联

</div>
</div>


<div class="details-box">
<details open>
<summary>Delta Sigma 调制器阶数 — Delta Sigma调制器阶数<div> 默认 1 阶 | 可选 1 阶至 6 阶</div></summary>
</details>
<div class="details-content">

选择 Delta Sigma 调制器的阶数。选项为 1 阶至 6 阶，默认 1 阶。


</div>
</div>


<div class="details-box">
<details open>
<summary>系统带宽 — 系统带宽<div> 非负实数标量</div></summary>
</details>
<div class="details-content">

Delta Sigma 调制器系统的带宽，非负实数标量。

</div>
</div>


<div class="details-box">
<details open>
<summary>OSR — 过采样率<div> 非负实数标量 </div></summary>
</details>
<div class="details-content">

Delta Sigma 调制器采样率与奈奎斯特率的比值，非负实数标量。高过采样率可降低抗混叠滤波器要求并减少带内量化噪声。

</div>
</div>


<div class="details-box">
<details open>
<summary>采样频率 — 采样频率<div> 正实数标量 </div></summary>
</details>
<div class="details-content">

Delta Sigma 调制器的采样频率，正实数标量（只读参数，由系统带宽和 OSR 计算得出）。

</div>
</div>

<div class="details-box">
<details open>
<summary>量化器位数 — 量化器位数<div> 正实数整数 </div></summary>
</details>
<div class="details-content">

Delta Sigma 调制器中量化器的位数，正实数整数。

</div>
</div>


<div class="details-box">
<details open>
<summary>量化器输出范围 — 量化器输出范围<div> 实数向量 </div></summary>
</details>
<div class="details-content">

Delta Sigma 调制器架构中量化器的输出范围，实数向量（只读参数）。

</div>
</div>


<div class="details-box">
<details open>
<summary>使用自定义系数值 — 使用自定义系数值<div> off（默认）| on </div></summary>
</details>
<div class="details-content">

选择是否使用自定义系数值（'a'、'g'、'b'、'c'）。

</div>
</div>

<div class="details-box">
<details open>
<summary>系数 a — 反馈系数或前馈系数<div> 实数向量 </div></summary>
</details>
<div class="details-content">

来自量化器的反馈系数或至量化器的前馈系数，实数向量。需启用**使用自定义系数值**选项。

</div>
</div>


<div class="details-box">
<details open>
<summary>系数 g — 谐振器系数<div> 实数向量 </div></summary>
</details>
<div class="details-content">

谐振器系数，实数向量。需启用**使用自定义系数值**选项。

</div>
</div>


<div class="details-box">
<details open>
<summary>系数 b — 积分器的输入系数<div> 实数向量 </div></summary>
</details>
<div class="details-content">

从调制器输入至各积分器的输入系数，实数向量。需启用**使用自定义系数值**选项。

</div>
</div>


<div class="details-box">
<details open>
<summary>系数 c — 积分器级间系数<div> 实数向量 </div></summary>
</details>
<div class="details-content">

积分器级间系数，实数向量。需启用**使用自定义系数值**选项。

</div>
</div>


### 扰动

<div class="details-box">
<details open>
<summary>积分器运放器增益 — 积分器运放增益<div> 正实数标量 </div></summary>
</details>
<div class="details-content">

内部运放的开环增益，正实数标量（用于噪声传递函数 NTF 分析，理想 NTF 假设运放增益无限大）。

</div>
</div>


<div class="details-box">
<details open>
<summary>启用噪声扰动 — 启用噪声扰动<div> off（默认）| on </div></summary>
</details>
<div class="details-content">

是否在 Delta Sigma 调制器 ADC 中启用噪声计算。

</div>
</div>

<div class="details-box">
<details open>
<summary>热噪声值 — 热噪声值<div> 实数标量 </div></summary>
</details>
<div class="details-content">

热噪声密度，实数标量（单位：V rms 或 dB/Hz）。需启用**启用噪声损耗**选项。

</div>
</div>


<div class="details-box">
<details open>
<summary>参考电阻 — 参考电阻（欧姆）<div> 正实数标量 </div></summary>
</details>
<div class="details-content">

用于功率计算的参考电阻，正实数标量（单位：欧姆）。需启用**启用噪声损耗**选项。

</div>
</div>


<div class="details-box">
<details open>
<summary>1/f 噪声拐角频率 — 1/f 噪声拐角频率（Hz）<div> 正实数标量 </div></summary>
</details>
<div class="details-content">

闪烁噪声（1/f 噪声）的拐角频率，正实数标量（单位：Hz）。在此频率下，1/f 噪声近似等于热噪声。。需启用**启用噪声损耗**选项。

</div>
</div>


## 版本历史记录

- 在 2025b 推出
