# QPSKModulatorBaseband
---
采用正交相移键控方法进行调制。

**库：** TYCommunication / PHYComponents / Modulation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYCommunication/PHYComponents/Modulation/QPSKModulatorBaseband/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

QPSK 调制器基带模块采用正交相移键控（QPSK）方法对信号进行调制，输出为调制信号的基带表示形式。该模块支持标量或向量形式的输入信号。


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

输入信号，指定为实数标量或实数向量。

- 当输入类型设为 Integer 时，输入信号元素应为 [0, 3] 范围内的整数值；

- 当输入类型设为 Bit 时，输入信号应为包含偶数个元素的二进制向量，以确保生成完整的 2 比特 QPSK 调制符号。


**数据类型：** double

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — QPSK 调制基带信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">
 
QPSK 调制后的基带信号，以复数值标量或向量形式输出。该输出为 QPSK 调制信号的复数基带表示形式。



**数据类型：** double

</div>
</div>


## 参数

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
<summary>星座排序 — 符号映射方式<div>Gray（默认）| Binary</div></summary>
</details>
<div class="details-content">

整数或比特对输入的符号映射方式，指定为 Gray 或 Binary。

- 如需使用格雷码排序映射符号，请将此参数设为 Gray；

- 如需使用二进制码排序映射符号，请将此参数设为 Binary。

</div>
</div>


<div class="details-box">
<details open>
<summary>相位偏移 (rad) — 零点的相位偏移<div>π/4（默认） | 标量</div></summary>
</details>
<div class="details-content">

星座图中零点信号的相位偏移（以弧度为单位），指定为标量值。

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
