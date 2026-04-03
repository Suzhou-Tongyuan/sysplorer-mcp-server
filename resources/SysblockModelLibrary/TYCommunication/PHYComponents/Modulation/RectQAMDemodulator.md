# RectangularQAMDemodulatorBaseband
---
解调矩形正交调幅后的进行基带信号。

**库：** TYCommunication / PHYComponents / Modulation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYCommunication/PHYComponents/Modulation/RectQAMDemodulator/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

矩形正交幅度解调基带模块可对采用正交幅度调制且星座图位于矩形点阵上的信号进行解调。信号星座图包含 M 个点，其中 M 为 M 进制参数值。M 必须为 2 的 K 次方形式，其中 K 为正整数。该模块接受标量或向量形式的输入信号。

## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

输入信号，指定为复数标量或复数向量。

**数据类型：** double

</div>
</div>

<div class="details-box">
<details open>
<summary>var — 噪声方差估计<div>标量</div></summary>
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
<summary>y — 解调后的信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">
 
输出信号以标量或向量形式返回，是输入调制信号的解调结果。

- 当**输出类型**设为 Integer 时，返回的输出信号元素为 [0, M-1] 范围内的整数值；

- 当**输出类型**设为 Bit 时，由于每个符号对应 $K = log2(M)$  比特，返回的输出信号为包含 K 的倍数个元素的向量。

**数据类型：** double 

**数据类型：** int32

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>星座点数 — 指定<div>16（默认）| 正整数</div></summary>
</details>
<div class="details-content">

信号星座图中的点数必须为 2 的 K 次方形式，其中 K 为正整数。

</div>
</div>


<div class="details-box">
<details open>
<summary>输出类型 — 整数或比特对输出指示器<div>Integer（默认）| Bit</div></summary>
</details>
<div class="details-content">

整数或比特对输出指示器，指定为 Integer 或 Bit。

- 当输出类型设为 Integer 且星座图排序设为 Binary 时，模块将点 $e^{(j\phi +j\pi m/2)}$ 映射为 m 值，其中 ϕ 为相位偏移（单位：弧度，见参数**相位偏移（rad）**），m 取值为 [0, M-1] 区间内的整数；

- 当输出类型设为 Bit 且判决类型设为  Hard decision 时，输出包含成对的二进制值。最高有效位（向量中最顶端的比特）为模块最先输出的比特；

- 当输出类型设为 Bit 且判决类型设为 Log-likelihood ratio 或 Approximate log-likelihood ratio 时，输出将分别包含逐比特的对数似然比 (LLR) 值或近似对数似然比值。

</div>
</div>

<div class="details-box">
<details open>
<summary>判决类型 — 指定判决类型<div>Hard decision（默认）| Log-likelihood ratio | Approximate log-likelihood ratio </div></summary>
</details>
<div class="details-content">

指定解调判决类型。

- 当输出类型设为 Bit 且判决类型设为  Hard decision 时，输出包含成对的二进制值。最高有效位（向量中最顶端的比特）为模块最先输出的比特；

- 当输出类型设为 Bit 且判决类型设为 Log-likelihood ratio 或 Approximate log-likelihood ratio 时，输出将分别包含逐比特的对数似然比 (LLR) 值 或近似对数似然比值。

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
<summary>星座排序 — 符号映射方式<div>Gray（默认）| Binary | User-defined</div></summary>
</details>
<div class="details-content">

整数或比特对输入的符号映射方式，指定为 Gray、Binary 或 User-defined。

- 如需使用格雷码排序映射符号，请将此参数设为 Gray；

- 如需使用二进制码排序映射符号，请将此参数设为 Binary；

- 如需人为指定排序映射符号，请将此参数设为 User-defined，此时**星座映射**参数生效。

</div>
</div>


<div class="details-box">
<details open>
<summary>星座映射 — 指定排序映射符号<div>0：15（默认） | 向量</div></summary>
</details>
<div class="details-content">

指定排序映射符号，当**星座排序**参数设为 User-defined 时，**星座映射**参数生效，需设置为**星座点数**参数所指定的长度。

</div>
</div>


<div class="details-box">
<details open>
<summary>标准化方法 — 指定对星座图进行标准化处理的方式<div>0：15（默认） | 向量</div></summary>
</details>
<div class="details-content">

指定模块对星座图的缩放方式，可指定为 Min. distance between symbols、 Average Power 或 Peak Power。

</div>
</div>


<div class="details-box">
<details open>
<summary>最小距离 — 指定两个最近星座点间的距离<div>2（默认）| 正实数标量</div></summary>
</details>
<div class="details-content">

指定两个最近的星座点之间的距离，正实数标量。当**标准化方法**指定为 Min. distance between symbols 时生效。

</div>
</div>

<div class="details-box">
<details open>
<summary>平均功率 — 指定星座中符号的平均功率<div>1（默认）| 正实数标量</div></summary>
</details>
<div class="details-content">

星座中符号的平均功率，参考 1 欧姆，正实数标量。当**标准化方法**指定为 Average Power 时生效。

</div>
</div>


<div class="details-box">
<details open>
<summary>峰值功率 — 指定星座中符号的峰值功率<div>1（默认）| 正实数标量</div></summary>
</details>
<div class="details-content">

星座中符号的峰值功率，参考 1 欧姆，正实数标量。当**标准化方法**指定为 Peak Power 时生效。

</div>
</div>


<div class="details-box">
<details open>
<summary>相位偏移 (rad) — 零点的相位偏移<div>π/4（默认） | 实数标量</div></summary>
</details>
<div class="details-content">

星座图中零点信号的相位偏移（以弧度为单位），指定为实数标量值。

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
