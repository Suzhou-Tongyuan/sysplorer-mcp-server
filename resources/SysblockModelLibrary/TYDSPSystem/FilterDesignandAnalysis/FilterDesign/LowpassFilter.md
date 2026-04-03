# LowpassFilter
---
&nbsp;

设计 FIR 或 IIR 低通滤波器。

**库：**  TYDSPSystem / FilterDesignandAnalysis / FilterDesign

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYDSPSystem/FilterDesignandAnalysis/FilterDesign/LowpassFilter/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述


LowpassFilter 模块使用模块指定参数进行滤波器设计，随时间独立地对输入信号的每个通道进行滤波。可以使用滤波器类型参数控制该模块是实现 IIR 还是 FIR 低通滤波器。


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div> 实数向量</div></summary>
</details>
<div class="details-content">

输入信号，指定为长度为 N 的列向量。

**数据类型：** double 

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>实数向量</div></summary>
</details>
<div class="details-content">
 
输出信号，与输入信号维度一致。

**数据类型：** double 

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>滤波器类型 — FIR 或 IIR 滤波器<div>FIR（默认）| IIR </div></summary>
</details>
<div class="details-content">

指定组件使用 FIR 低通滤波器还是 IIR 低通滤波器。

</div>
</div>

<div class="details-box">
<details open>
<summary>最小阶滤波器设计 - 用最小阶来设计滤波器<div>on（默认）| off </div></summary>
</details>
<div class="details-content">

当选中该勾选框，模块会使用用最小阶通带、阻带频率来设计一个滤波器；当取消勾选该勾选框，可以将滤波器阶数指定为一个正整数。

</div>
</div>

<div class="details-box">
<details open>
<summary>滤波器阶数 — 指定低通滤波器的阶数<div>50（默认）| 正整数 </div></summary>
</details>
<div class="details-content">

低通滤波器的阶数，指定为一个正整数标量。取消勾选**最小阶滤波器设计**勾选框以启用该参数。

</div>
</div>

<div class="details-box">
<details open>
<summary>通带边缘频率（Hz） — 通带边缘频率<div>8e3（默认）| 正实数标量 </div></summary>
</details>
<div class="details-content">


低通滤波器的通带边缘频率，指定为以赫兹为单位的实数正标量。通带边缘频率必须小于**采样频率 (Hz)** 的一半。

</div>
</div>

<div class="details-box">
<details open>
<summary>阻带边缘频率（Hz） — 阻带边缘频率<div>12e3（默认）| 正实数标量  </div></summary>
</details>
<div class="details-content">


低通滤波器的阻带边缘频率，指定为以赫兹为单位的实数正标量。通带边缘频率必须小于**采样频率 (Hz)** 的一半。

**依赖：** 勾选**最小阶滤波器设计**勾选框以启用这个参数。

</div>
</div>

<div class="details-box">
<details open>
<summary>最大通带波纹（dB） — 最大通带波纹<div>0.1（默认）| 正实数标量 </div></summary>
</details>
<div class="details-content">


通带内滤波器响应的最大纹波，以 dB 为单位的实数正标量指定。

</div>
</div>

<div class="details-box">
<details open>
<summary>最小阻带衰减（dB） — 最小阻带衰减<div>80（默认）| 正实数标量 </div></summary>
</details>
<div class="details-content">


阻带中的最小衰减，指定为以 dB 为单位的正实数标量。

</div>
</div>

<div class="details-box">
<details open>
<summary>采样频率（Hz） — 输入采样频率<div>44100（默认）| 标量 </div></summary>
</details>
<div class="details-content">


设置输入信号的采样频率，以 Hz 为单位的正实数标量。

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
