# FIRInterpolation
---
&nbsp;

构建 FIR 插值器模型。

**库：** TYDSPSystem / FilterImplementation / MultirateandMultistageFilters 

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYDSPSystem/FilterImplementation/MultirateandMultistageFilters/FIRInterpolation/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

FIRInterpolation 模块使用沿第一维的整数上采样因子 L 执行有效的多相插值。

从概念上讲，FIR 插值器由上采样器和 FIR 滤波器组成，FIR 滤波器通常是理想带限插值滤波器的近似值。上采样器通过在采样之间插入 L-1 个零，将输入的每个通道上采样到更高的速率。随后的 FIR 滤波器对上采样数据的每个通道进行滤波，得到的离散时间信号的采样率是原始采样率的L 倍。

## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div> 实数向量</div></summary>
</details>
<div class="details-content">

输入信号，指定为实数向量。

**数据类型：** double 

</div>
</div>

<div class="details-box">
<details open>
<summary>Num — 滤波器系数<div> 实数向量 </div></summary>
</details>
<div class="details-content">

FIR 滤波器的系数，指定为实数向量。要使用此端口请将**系数源**设置为 Input port。

**数据类型：** double 

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 插值输出<div>实数向量</div></summary>
</details>
<div class="details-content">
 
插值滤波后的信号输出，指定为实数向量。

当**速率设置**设置为：

- Enforce single-rate processing -- 当选择此选项时，模块保持输入采样率，并通过将输出帧大小增加 1 倍来输出插值信号；
- Allow multirate processing -- 当选择此选项时，模块插值信号，使输出采样率比输入采样率快 L 倍。

**数据类型：** Double 

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>系数源 — 系数源<div>Auto（默认）| Input port</div></summary>
</details>
<div class="details-content">

指定 FIR 滤波器系数源为以下之一：
- Auto -- 当选择 Auto 时，该模块使用在**插值因子**中指定的插值因子设计 FIR 插值器。
- Input port -- 通过 Num 输入端口指定滤波器系数。

</div>
</div>

<div class="details-box">
<details open>
<summary>插值因子  — 插值因子<div>3（默认）| 正整数标量</div></summary>
</details>
<div class="details-content">

指定插值因子 L 。模块按该插值因子增加输入信号的采样率。

</div>
</div>

<div class="details-box">
<details open>
<summary>输入处理  — 指定输入处理方式<div>Columns as channels（frame based）（默认）| Element as channels（Sample based）</div></summary>
</details>
<div class="details-content">

指定模块应该如何处理输入。可设置为以下选项之一：

- Columns as channels（frame based）-- 当选择此选项时，块将输入的每个列视为单独的通道；
- Element as channels（Sample based）-- 当选择此选项时，块将输入的每个元素视为单独的通道。
- 
</div>
</div>

<div class="details-box">
<details open>
<summary>速率设置  — 设置速率模式<div> Enforce single-rate processing（默认）| Allow multirate processing</div></summary>
</details>
<div class="details-content">

指定模块应该使用的速率模式。您可以选择以下选项之一：

- Enforce single-rate processing -- 当选择此选项时，模块保持输入采样率，并通过将输出帧大小增加l倍来插值信号。要选择此选项，您必须将**输入处理**参数设置为 Columns as channels (frame based)。
- Allow multirate processing -- 当选择此选项时，模块插值信号，使输出采样率比输入采样率快 L 倍。

</div>
</div>

<div class="details-box">
<details open>
<summary>输出缓存初始状态  — 初始状态<div>0.0（默认）| 实数标量</div></summary>
</details>
<div class="details-content">

当模块显示延迟时，默认初始条件为 0。当将**速率设置**参数设置为 Allow multirate processing，配置模块执行多速率处理时，此参数可配置。

</div>
</div>

<div class="details-box">
<details open>
<summary>输入系数维度 — 指定输入系数维度<div>{1}（默认）| 长度为 1 的整型向量</div></summary>
</details>
<div class="details-content">

指定输入系数维度的维度。指定为长度为 1 的整型向量。当**系数源**设置为 Input port 时需配置。

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

- 该模块暂不支持自动识别输入系数以及输入信号维度，需通过**输入系数维度**和**输入信号维度**参数手动设定。

