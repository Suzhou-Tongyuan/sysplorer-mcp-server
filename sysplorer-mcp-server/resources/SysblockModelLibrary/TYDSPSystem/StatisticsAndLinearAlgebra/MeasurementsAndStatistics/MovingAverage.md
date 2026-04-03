# MovingAverage
---
&nbsp;

计算移动平均。

**库：** TYDSPSystem / StatisticsAndLinearAlgebra / MeasurementsAndStatistics

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYDSPSystem/StatisticsAndLinearAlgebra/MeasurementsAndStatistics/MovingAverage/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

MovingAverage 模块会独立计算每个通道输入信号随时间变化的移动平均值。该模块使用滑动窗口法或指数加权法来计算移动平均值。在滑动窗口法中，指定长度的窗口会逐个移动数据样本，然后模块会计算窗口中数据的平均值。在指数加权法中，模块会将数据样本与一组加权因子相乘，然后将加权数据相加以计算平均值。


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 信号输入<div> 实数向量</div></summary>
</details>
<div class="details-content">

输入信号，指定为长度为 N 的实数向量。

**数据类型：** double 

</div>
</div>

<div class="details-box">
<details open>
<summary>lambda — 遗忘因子<div> 范围 (0, 1] 的正实数标量</div></summary>
</details>
<div class="details-content">

遗忘因子决定了过去数据的权重。0.9 的遗忘因子比 0.1 的遗忘因子赋予更早数据的权重更大。1.0 的遗忘因子表示无限记忆——所有之前的样本都具有相同的权重。将**方法**参数设置为 Exponential weighting 并勾选**从端口指定遗忘因子**选项时可用。

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 输出移动平均值<div>实数向量</div></summary>
</details>
<div class="details-content">
 
移动平均输出的大小与输入的大小匹配。

**数据类型：** double 

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>方法 — 计算移动平均的方法<div>Sliding window (默认) | Exponential weighting</div></summary>
</details>
<div class="details-content">

参数可选项如下：

 - Sliding window——长度为窗口长度的窗口沿每个通道在输入数据上移动。对于窗口移动的每个样本，模块都会计算窗口中数据的平均值；

 - Exponential weighting——该模块将样本乘以一组加权因子。加权因子的幅度会随着数据老化而呈指数下降，但幅度永远不会达到零。为了计算平均值，算法会对加权数据求和。

</div>
</div>

<div class="details-box">
<details open>
<summary>指定窗长度 — 指定窗长度的标志<div>on (默认) | off</div></summary>
</details>
<div class="details-content">

选中此复选框时，滑动窗口的长度等于在**窗长度**中指定的值。取消选中该复选框时，滑动窗口的长度为无限长。在此模式下，模块将计算通道中当前样本和所有先前样本的平均值。将**方法**参数设置为 Sliding window 时可用

</div>
</div>

<div class="details-box">
<details open>
<summary>窗长度 — 滑动窗的长度<div>4 (默认) | 正整数标量</div></summary>
</details>
<div class="details-content">

指定采样的滑动窗的长度。将**方法**参数设置为 Sliding window 并勾选 **指定窗长度** 复选框时可用。

</div>
</div>

<div class="details-box">
<details open>
<summary>从端口指定遗忘因子 — 指定遗忘因子的标志<div>on (默认) | off</div></summary>
</details>
<div class="details-content">

选中此复选框时，遗忘因子通过 lambda 端口输入。取消选中该复选框后，将在模块对话框中通过**遗忘因子**参数指定遗忘因子。 将**方法**参数设置为 Exponential weighting 时可用。

</div>
</div>

<div class="details-box">
<details open>
<summary>遗忘因子 — Exponential weighting 的系数<div> 范围 (0, 1] 的正实数标量</div></summary>
</details>
<div class="details-content">

遗忘因子决定了过去数据的权重。0.9 的遗忘因子比 0.1 的遗忘因子赋予更早数据的权重更大。1.0 的遗忘因子表示无限记忆——所有之前的样本都具有相同的权重。 将**方法**设置为 Exponential weighting 并取消勾选 **从端口指定遗忘因子**选项时可用。

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

## 限制信息

- 该模块暂不支持自动识别输入信号维度，需通过**输入信号维度**参数手动设定。