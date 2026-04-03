# ADC_DAC
---
考虑不匹配的多比特 ADC 与 DAC 模型。

**库：** TYMixedSignal / SDUtilities

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYMixedSignal/SDUtilities/ADC_DAC/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

ADC_DAC模块用于建模多比特 ADC 和 DAC，并考虑电容不匹配的影响。该模块根据量化器中所需比较器数量（$N_{ADC}$）自动确定 ADC 的阈值电平和 DAC 的输出电平。DAC 的输出电平数量为 $N_{ADC} + 1$。模块的输入范围和输出范围均为 [-1, 1]。若需要其他范围，需在 ADC_DAC 模块前放置增益模块（调整输入范围）并在模块后放置增益模块（恢复输出范围）。例如，若需实现 [-2, 2] 范围，模块前需添加 1/2 增益，模块后添加 2 增益。模块的 ADC 输出代表 Sigma-Delta 调制器的数字输出，而 DAC 输出则是 Sigma-Delta 调制器的反馈信号。

在多比特 Sigma-Delta 调制器中，内部DAC电容的不匹配会导致噪声基底和谐波失真的增加，其性能退化与电容标准差（σ）相关，其表达式为:

$$
\sigma\left(\frac{\Delta C}{C}\right)=\frac{A_{C}}{\sqrt{W L}}=\frac{k}{\sqrt{C}}, k=A_{C} \sqrt{C_{s p}}
$$

其中，$C_{\text{sp}}$ 为比电容（单位：$F/µm²$），$A_{C}$为电容面积（单位：$µm$），k 为工艺相关常数。若 k 或 $A_{C}$ 未知，可通过以下公式根据总电容 $C_{\text{TOT}}$ 计算 k 值: 

$$
k=\sigma \sqrt{\frac{C_{T O T}}{N_{A D C}}}
$$

其中，$C_{TOT}$ 为 DAC 的总电容。

由于采样电容值会影响几乎所有基础模块（如运算放大器、电压基准）的设计约束，需在设计初期确定其值。基于电路仿真（如蒙特卡洛仿真）的方法因耗时且低效，通常不适用。

该 ADC_DAC 模块可用于评估：给定采样电容尺寸时，不匹配引起的性能退化是否可忽略（相对于热噪声），或是否需要采用动态元件匹配等校正技术。内部 DAC 假设为奇对称结构（与实际全差分电路及精心设计的单端电路一致），即相同元件用于构建正负值。此假设可避免 DAC 引入偶次失真，对准确评估不匹配对输出频谱的影响至关重要。

不匹配信息可通过参数 σ 或预定义的外部方差向量提供。

## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 信号输入<div>实数标量或向量</div></summary>
</details>
<div class="details-content">

输入信号。

**数据类型：** double

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>ADC — 调制器的数字输出<div>实数标量或向量</div></summary>
</details>
<div class="details-content">
 
Sigma-Delta 调制器的数字信号输出。

**数据类型：** double

</div>
</div>

<div class="details-box">
<details open>
<summary>DAC — 调制器的反馈信号<div>实数标量或向量</div></summary>
</details>
<div class="details-content">
 
Sigma-Delta 调制器的反馈信号。

**数据类型：** double

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>量化器中的比较器数目 — 量化器中的比较器数量<div> 正整数 </div></summary>
</details>
<div class="details-content">

ADC 中使用的比较器数量（$N_{ADC}$）.

</div>
</div>


<div class="details-box">
<details open>
<summary>考虑不匹配 — 启用DAC电容不匹配的建模<div> 布尔量 </div></summary>
</details>
<div class="details-content">

设置是否启用 DAC 电容不匹配的建模。


</div>
</div>


<div class="details-box">
<details open>
<summary>匹配参数 — 匹配参数<div> 实数标量</div></summary>
</details>
<div class="details-content">

提供匹配参数 k（单位：√F），仅当选择**考虑不匹配**且未选择**额外设置方差向量**时生效。

</div>
</div>


<div class="details-box">
<details open>
<summary>总电容 — 总电容<div> 实数标量 </div></summary>
</details>
<div class="details-content">

DAC 的总电容（单位：F），仅当选择**考虑不匹配**且未选择**额外设置方差向量**时生效。

</div>
</div>


<div class="details-box">
<details open>
<summary>外部提供方差向量 — 外部提供方差向量<div> 布尔值 </div></summary>
</details>
<div class="details-content">

选择是否通过外部输入向量提供不匹配信息（替代匹配参数）。

</div>
</div>

<div class="details-box">
<details open>
<summary>方差向量 — 方差向量<div> 实数向量 </div></summary>
</details>
<div class="details-content">

包含 $N_{ADC}$ 个元素的向量，提供不匹配方差，均值需为 0，方差需为 1，仅当选择**考虑不匹配**且选择**外部提供方差向量**时生效。

</div>
</div>


<div class="details-box">
<details open>
<summary>输入信号维度 — 设置输入信号维度<div> {1}（默认）| 长度为 1 的正整数向量 </div></summary>
</details>
<div class="details-content">

设置输入信号的维度。仅支持长度为 1 的正整数向量，即输入端口仅支持标量或向量输入。特别的，将该参数设置为 {1} 时可兼容标量输入。

</div>
</div>

## 版本历史记录

- 在 2025b 推出

### 限制信息

- 该模块暂不支持自动识别输入信号维度，需通过**输入信号维度**参数手动设定