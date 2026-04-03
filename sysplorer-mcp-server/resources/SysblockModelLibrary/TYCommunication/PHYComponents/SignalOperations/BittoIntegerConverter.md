# BittoIntegerConverter
---
将比特向量映射为对应的整数向量。

**库：** TYCommunication / PHYComponents / SignalOperations

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYCommunication/PHYComponents/SignalOperations/BittoIntegerConverter/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

比特位到整数转换器模块将输入向量中的比特组映射为输出向量中的整数。


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

输入信号，指定为一个标量或比特向量，其长度必须是每整数位数（M）参数所指定值的整数倍。输入必须是值为 0 或 1 的比特。

**数据类型：** double

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 整数向量</div></summary>
</details>
<div class="details-content">
 
输出信号，以整数或整数列向量形式返回。

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>每个整数的比特位数(M) — 单个整数的比特数<div>3（默认值） | [1, 32] 范围内的整数</div></summary>
</details>
<div class="details-content">

指定输入比特数与输出整数的映射关系，取值范围为 [1, 32] 的整数，表示每个输出整数对应的输入比特位数。

</div>
</div>


<div class="details-box">
<details open>
<summary>输入位序 — 输入位顺序<div>MSB first（默认）| LSB first</div></summary>
</details>
<div class="details-content">

输入位顺序，指定为 MSB first 或 LSB first。

- MSB first —— 输入信号的首位表示最高有效位（MSB）；

- LSB first —— 输入信号的首位表示最低有效位（LSB）。

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

- 该模块暂不支持自动识别输入信号维度，需通过**输入信号维度**参数手动设定
