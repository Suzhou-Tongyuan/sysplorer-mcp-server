# RectangularQAMModulatorBaseband
---
采用矩形正交调幅法进行调制。

**库：** TYCommunication / PHYComponents / Modulation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYCommunication/PHYComponents/Modulation/RectQAMModulator/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

矩形正交幅度调制基带模块采用 M 进制正交幅度调制方式进行调制，其星座图位于矩形点阵之上。该模块的输出为调制信号的基带表示形式。此模块接受标量或向量形式的输入信号。


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

输入信号，指定为实数标量或实数向量。

- 当输入类型设为 Integer 时，输入信号元素应为 [0, M-1] 范围内的整数值；

- 当输入类型设为 Bit 时，输入信号应为二进制向量，该模块会将二进制值信号按 $K = log2(M)$ 位一组进行分组。

**数据类型：** int32

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 矩形正交幅度调制基带信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">
 
矩形正交幅度调制后的基带信号，以复数值标量或向量形式输出。该输出为矩形正交幅度调制信号的复数基带表示形式。

**数据类型：** double

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
<summary>输入类型 — 整数或比特对输入指示器<div>Integer（默认）| Bit</div></summary>
</details>
<div class="details-content">

整数或比特对输入指示器，指定为 Integer 或者 Bit。

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
