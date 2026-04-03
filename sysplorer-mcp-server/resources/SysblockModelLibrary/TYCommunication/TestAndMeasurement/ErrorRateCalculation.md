# ErrorRateCalculation
---
计算输入数据的误码率或符号误码率。

**库：** TYCommunication / TestAndMeasurement 

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYCommunication/TestAndMeasurement/ErrorRateCalculation/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

ErrorRateCalculation 模块比较来自发射器的输入数据与来自接收器的输入数据。该块通过将不相等数据元素对的总数除以来自一个源的输入数据元素的总数，将错误率计算为运行统计。

可以使用该块来计算符号或误码率，因为它不考虑输入数据元素之间差异的大小。如果输入是位，则模块计算误码率。如果输入是符号，则该模块计算符号错误率。


## 端口

### 输入

<div class="details-box">
<details open>
<summary>Tx — 传输数据<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

以实数标量或向量指定的传输数据。输入信号 Tx 和 Rx 必须具有相同的维度。
- 如果将 Tx 或 Rx 输入指定为标量，则模块将此值与其他输入的所有元素进行比较；
- 如果将 Tx 和 Rx 输入指定为向量，则它们必须具有相同的大小。

**数据类型：** double 

</div>
</div>
<div class="details-box">
<details open>
<summary>Rx — 接收数据<div>标量 | 向量</div></summary>
</details>
<div class="details-content">
 
以实数标量或向量指定的接收数据。

**数据类型：** double 

</div>
</div>
<div class="details-box">
<details open>
<summary>Ind — 样本索引<div>标量 | 向量</div></summary>
</details>
<div class="details-content">
 
比较数据时要考虑的样本指标，指定为正整数标量或正整数向量。

**依赖条件：** 

要采用此端口，设置**计算模式**参数为 Select samples from input port。

**数据类型：** int32

</div>
</div>

<div class="details-box">
<details open>
<summary>reset — 重置错误数<div>标量</div></summary>
</details>
<div class="details-content">
 
重置错误计数，指定为标量。

**依赖条件：** 

要采用此端口，勾选**重置端口**选项。

**数据类型：** bool 

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 收发信号差异<div>向量</div></summary>
</details>
<div class="details-content">
 
传输和接收信号差异，返回一个标向量 {R, N, S}，其中：
- R 代表错误率；
- N 代表错误比特数；
- S 代表比较样本数量。

**数据类型：** double 

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>接收延迟 — 接收信号延迟<div>0（默认）| 非负整数</div></summary>
</details>
<div class="details-content">

接收数据滞后于发送数据的采样数，用非负整数指定。使用此参数在发送和接收的输入数据向量中对样本进行比较。

**数据类型：** int32 

</div>
</div>


<div class="details-box">
<details open>
<summary>计算延迟 — 计算延迟<div>0（默认）| 非负整数</div></summary>
</details>
<div class="details-content">

对象在比较开始时忽略的数据样本数，指定为非负整数。使用此参数忽略两个输入信号的瞬态行为。

**数据类型：** int32

</div>
</div>


<div class="details-box">
<details open>
<summary>计算模式 — 计算模式<div>Entire frame（默认）| Select samples from mask, Select samples from port</div></summary>
</details>
<div class="details-content">

指定为 Entire frame、Select samples from mask 或 Select samples from port ，取决于模块是否应考虑全部或部分输入帧。

</div>
</div>


<div class="details-box">
<details open>
<summary>重置端口 — 复位端口<div>off（默认）| on</div></summary>
</details>
<div class="details-content">

是否启用 reset 输入端口。

</div>
</div>

<div class="details-box">
<details open>
<summary>输入索引向量维度 — 指定输入索引向量维度<div>{1}（默认）| 长度为 1 的整型向量</div></summary>
</details>
<div class="details-content">

指定输入索引向量的维度。指定为长度为 1 的整型向量。

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
