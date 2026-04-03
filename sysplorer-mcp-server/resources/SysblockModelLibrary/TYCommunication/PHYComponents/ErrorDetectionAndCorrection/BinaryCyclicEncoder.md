# BinaryCyclicEncoder
---
从二进制向量数据创建系统循环码

**库：** TYCommunication / PHYComponents / ErrorDetectionAndCorrection

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYCommunication/PHYComponents/ErrorDetectionAndCorrection/BinaryCyclicEncoder/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

描述二进制循环编码器块创建具有消息长度 K 和码字长度 N 的系统循环码。

该块接受包含 K 个元素的列矢量输入信号。输出信号是包含 N 个元素的列向量。

您可以通过以下两种方式之一确定系统循环编码方案：

* 要创建 [N，K] 码，请分别输入 N 和 K 作为第一个和第二个对话框参数。该块计算一个适当的生成多项式，即循环多项式 （N，K，'min'）。
* 要创建具有码字长度N和特定次数 （N-K） 二进制生成器多项式的代码，请输入 N 作为第一个参数，输入多项式字符向量或二进制向量作为第二个参数。该向量通过按指数升序列出其系数来表示生成器多项式。

## 端口

### 输入

<div class="details-box">
<details open>
<summary>In — 输入信号<div>实数向量</div></summary>
</details>
<div class="details-content">

输入信号，指定为一个长度为 N 的实数向量。

**数据类型：** double

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>Out — 输出信号<div>实数向量</div></summary>
</details>
<div class="details-content">

输出相位调制后的信号，指定为一个长度为 K 的实数向量。

**数据类型：** double

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>码字长度 N — 输入信号的码字长度<div>7 （默认） | 正整数</div></summary>
</details>
<div class="details-content">

码字长度 N ，也是输出向量长度。

</div>
</div>

<div class="details-box">
<details open>
<summary>消息长度 K — 输出信号的消息长度<div>4 （默认） | 正整数</div></summary>
</details>
<div class="details-content">

消息长度 K ，也是输入向量长度。

</div>
</div>

## 版本历史记录

- 在 2026b 推出


