# BinaryLinearDecoder
---
解码线性块码以恢复二进制矢量数据

**库：** TYCommunication / PHYComponents / ErrorDetectionAndCorrection

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYCommunication/PHYComponents/ErrorDetectionAndCorrection/BinaryLinearDecoder/1.png')" style="width: 100px; height: auto; transform: scale(1);">


## 描述

BinaryLinearDecoder 模块从线性块码的二进制码字向量中恢复二进制消息向量。

生成器矩阵参数是块码的生成器矩阵。为了正确解码，这应该与相应的 BinaryLinearDecoder 模块中的生成器矩阵参数相匹配。如果 N 是代码的码字长度，则生成器矩阵必须有 N 列。如果 K 是代码的消息长度，则生成器矩阵参数必须有 K 行。

该模块接受包含 N 个元素的列矢量输入信号。此块输出长度为 K 个元素的列向量。

解码器尝试使用解码表参数纠正错误。如果解码表是长度为 1 的向量 {{0}} ，则块默认为通信函数库函数 syndtable 生成的表。否则，解码表必须是一个 $2^{N-K}$ 乘 $N$ 的二进制矩阵。该矩阵的第 r 行是接收到的二进制码字的校正向量，其校验子具有十进制整数值 r-1。接收到的码字的校验子是它与奇偶校验矩阵转置的乘积。

## 端口

### 输入

<div class="details-box">
<details open>
<summary>In — 输入信号实数向量</summary>
</details>
<div class="details-content">

输入信号，指定为一个长度为 N 的实数向量。

**数据类型：** double

</div>
</div>



### 输出

<div class="details-box">
<details open>
<summary>Out — 输出信号实数向量</summary>
</details>
<div class="details-content">

输出相位调制后的信号，指定为一个长度为 K 的实数向量。

**数据类型：** double

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>生成矩阵 — 代码生成器的矩阵<div><!-- {{1,1,0,1,0,0,0},{0,1,1,0,1,0,0}}</div><div>,{{1,1,1,0,0,1,0},{1,0,1,0,0,0,1}}（默认） -->二进制 K*N 整数矩阵</div></summary>
</details>
<div class="details-content">

代码生成器矩阵，与 BinaryLinearDecoder 模块中的相同。

</div>
</div>

<div class="details-box">
<details open>
<summary>解码表 — 参照的解码表<div>{{0}} （默认） | 二维矩阵</div></summary>
</details>
<div class="details-content">

一个 $2^{N-K}$ 乘 $N$ 的矩阵，其中列出了每个码字校验子的校正向量；或者是长度为 1 的向量 {{0}} ，在这种情况下，模块默认为与生成器矩阵参数对应的表。

</div>
</div>


## 版本历史记录

- 在 2026b 推出


