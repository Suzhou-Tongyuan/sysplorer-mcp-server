# QPSKDemodulatorBaseband
---
QPSK 调制信号解调。

**库：** TYCommunication / PHYComponents / Modulation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYCommunication/PHYComponents/Modulation/QPSKDemodulatorBaseband/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

QPSK 解调器基带模块用于对采用正交相移键控（QPSK）方法调制的信号进行解调。输入信号应为已调制信号的基带表示形式。

该模块的输入必须为复数信号，支持标量或列向量形式的输入信号。


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — QPSK 调制信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

QPSK 调制信号，指定为包含 QPSK 调制信号基带表示的复数标量或向量。


**数据类型：** double 

**支持复数：** 是

</div>
</div>


<div class="details-box">
<details open>
<summary>var — 噪声方差估计<div>正实数标量</div></summary>
</details>
<div class="details-content">
 
噪声方差估计，指定为正实数标量值。

**依赖条件：**

此参数仅在将**噪声方差源**设置为 Input port 时生效。

**数据类型：** double 

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

输出信号以标量或向量形式返回，是输入 PSK 调制信号的解调结果。

- 当**输出类型**设为 Integer 时，返回的输出信号元素为 [0, 3] 范围内的整数值；

- 当**输出类型**设为 Bit 时，由于 QPSK 每个符号对应 2 比特，返回的输出信号为包含偶数个元素的向量。

**数据类型：** double 

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>输出类型 — 整数或比特对输出指示器<div>Integer（默认）| Bit</div></summary>
</details>
<div class="details-content">

整数或比特对输出指示器，指定为 Integer 或 Bit。

- 当输出类型设为 Integer 且星座图排序设为 Binary 时，模块将点 $e^{(j\phi +j\pi m/2)}$ 映射为 m 值，其中 ϕ 为相位偏移（单位：弧度，见参数**相位偏移（rad）**），m 取值为 0、1、2 或 3；

- 当输出类型设为 Bit 且判决类型设为  Hard decision 时，输出包含成对的二进制值。最高有效位（向量中最顶端的比特）为模块最先输出的比特；

- 当输出类型设为 Bit 且判决类型设为 Log-likelihood ratio 或 Approximate log-likelihood ratio 时，输出将分别包含逐比特的对数似然比(LLR)值或近似对数似然比值。

</div>
</div>

<div class="details-box">
<details open>
<summary>判决类型 — 指定判决类型<div>Hard decision（默认）| Log-likelihood ratio | Approximate log-likelihood ratio </div></summary>
</details>
<div class="details-content">

指定解调判决类型。

- 当输出类型设为 Bit 且判决类型设为  Hard decision 时，输出包含成对的二进制值。最高有效位（向量中最顶端的比特）为模块最先输出的比特；

- 当输出类型设为 Bit 且判决类型设为 Log-likelihood ratio 或 Approximate log-likelihood ratio 时，输出将分别包含逐比特的对数似然比 (LLR) 值或近似对数似然比值。

**依赖条件：**将**输出类型**指定为 Bit 时生效。

</div>
</div>


<div class="details-box">
<details open>
<summary>噪声方差源 — 指定噪声方差源<div>Dialog（默认）| Input port </div></summary>
</details>
<div class="details-content">

指定噪声方差源。

- Dialog - 噪声方差从参数面板输入；

- Input port - 噪声方差从端口输入。

**依赖条件：**将**输出类型**指定为 Bit，且**判决类型**设为 Log-likelihood ratio 或 Approximate log-likelihood ratio 时生效。

</div>
</div>

<div class="details-box">
<details open>
<summary>噪声方差 — 指定噪声方差<div>1.0 （默认）| 正实数标量 </div></summary>
</details>
<div class="details-content">

指定噪声方差。

**依赖条件：** 将**输出类型**指定为 Bit，**判决类型**设为 Log-likelihood ratio 或 Approximate log-likelihood ratio ，且**噪声方差源**指定为 Dialog 时生效。

</div>
</div>


<div class="details-box">
<details open>
<summary>星座排序 — 符号映射方式<div>Gray（默认）| Binary</div></summary>
</details>
<div class="details-content">

整数或比特对输出的符号映射方式，可指定为 Gray 或 Binary。

- 如需使用格雷码排序映射符号，请将此参数设为 Gray；

- 如需使用二进制码排序映射符号，请将此参数设为 Binary。

</div>
</div>


<div class="details-box">
<details open>
<summary>相位偏移 (rad) — 零点的相位偏移<div>π/4（默认） | 标量</div></summary>
</details>
<div class="details-content">

定义星座图中零点（zeroth point）的相位偏移量，以弧度为单位指定标量数值。

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

- 该模块暂不支持自动识别输入信号维度，需通过**输入信号维度**参数手动设定。
