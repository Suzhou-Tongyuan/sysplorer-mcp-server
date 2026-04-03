# DiscreteFIRFilter
---
&nbsp;

离散 FIR 滤波器模型。

**库：** TYDSPSystem / FilterImplementation / SingleRateFilters 

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYDSPSystem/FilterImplementation/SingleRateFilters/DiscreteFIRFilter/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

DiscreteFIRFilter 模块使用指定的数字 FIR 滤波器单独对输入信号的每个通道进行滤波。该模块可以实现系数固定的静态滤波器以及系数随时间变化的时变滤波器。

随时间的推移单独对输入信号的每个元素通道进行滤波，将输入的每个元素作为独立通道处理（基于采样的处理）。

## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div> 实值标量 | 实数向量</div></summary>
</details>
<div class="details-content">

输入数据，指定为实数向量。


**数据类型：** double 

</div>
</div>

<div class="details-box">
<details open>
<summary>coeff — 滤波器系数<div> 实数向量</div></summary>
</details>
<div class="details-content">

滤波器系数，指定为实数向量。要启用该端口，需设置**系数源**参数为 Input port。

**数据类型：** double 

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>y — 滤波输出信号<div>实值标量 | 实数向量</div></summary>
</details>
<div class="details-content">
 
滤波后的信号，实值标量或实值向量。输出的尺寸与输入的尺寸相匹配。

**数据类型：** double 

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>系数源 — 指定 FIR 滤波器系数源<div>Dialog parameters（默认）| Input port </div></summary>
</details>
<div class="details-content">

选择以指定是使用可调参数对话框参数还是通过输入端口指定滤波器系数。
</div>
</div>

<div class="details-box">
<details open>
<summary>滤波器结构 — 指定 FIR 滤波器结构<div>Direct form（默认）</div></summary>
</details>
<div class="details-content">

指定滤波器结构，当前版本仅支持 Direct form 型滤波器。

</div>
</div>

<div class="details-box">
<details open>
<summary>系数  — 滤波器系数<div>{0.5, 0.5}（默认）| 实数向量</div></summary>
</details>
<div class="details-content">

指定传递函数的系数向量。滤波器系数指定为实数向量。要启用该端口，需设置**系数源**参数为 Dialog parameters。
</div>
</div>

<div class="details-box">
<details open>
<summary>输入处理 — 处理输入信号的方式<div>Elements as channels (sample based)（默认）</div></summary>
</details>
<div class="details-content">

指定模块对输入信号的处理方式，当前版本仅支持 Elements as channels (sample based) 处理方式。

</div>
</div>


<div class="details-box">
<details open>
<summary>初始状态 — 指定滤波器初始状态<div>{0}（默认）| 实数向量 </div></summary>
</details>
<div class="details-content">

指定滤波器状态的初始条件。

</div>
</div>

<div class="details-box">
<details open>
<summary>输入滤波器系数维度 — 指定输入滤波器系数维度<div>{2}（默认）| 长度为 1 的整型向量</div></summary>
</details>
<div class="details-content">

指定输入滤波器系数维度。指定为长度为 1 的整型向量。

</div>
</div>

<div class="details-box">
<details open>
<summary>采样时间 — 指定模块采样时间<div> -1 | 正实数标量</div></summary>
</details>
<div class="details-content">

指定模块的采样时间。特别地，指定采样时间为 -1 时，模块继承模型的采样时间。

</div>
</div>


## 版本历史记录

- 在 2025b 推出

## 限制信息

- 该模块暂不支持自动识别输入滤波器系数维度，需通过**输入滤波器系数维度**参数手动设定。
