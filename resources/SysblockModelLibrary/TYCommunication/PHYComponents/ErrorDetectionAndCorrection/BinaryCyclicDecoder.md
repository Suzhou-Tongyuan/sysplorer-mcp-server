# BinaryCyclicDecoder
---
解码系统循环码以恢复二进制矢量数据

**库：** TYCommunication / PHYComponents / ErrorDetectionAndCorrection

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYCommunication/PHYComponents/ErrorDetectionAndCorrection/BinaryCyclicDecoder/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

BinaryCyclicDecoder 模块从二进制系统循环码的码字向量中恢复消息向量。为了正确解码，此块中的参数值应与相应的 BinaryCyclicEncoder 模块中的值相匹配。

该块接受包含 N 个元素的列矢量输入信号，其中 N 是码字长度。输出信号是包含 K 个元素的列向量，其中 K 是循环码的消息长度。

您可以通过以下两种方式之一确定系统循环编码方案：

* 要创建 [N，K] 码，请分别输入 N 和 K 作为第一个和第二个对话框参数。该块计算一个适当的生成多项式，即循环多项式 （N，K，'min'）。
* 要创建具有码字长度 N 和特定次数 （N-K） 二进制生成器多项式的代码，请输入 N 作为第一个参数，输入多项式字符向量或二进制向量作为第二个参数。该向量通过列出其系数来表示生成多项式按指数升序排列。

## 端口

### 输入

<div class="details-box">
<details open>
<summary>In — 输入信号<div>实数向量</div></summary>
</details>
<div class="details-content">

输入信号，指定为一个长度为 K 的实数向量。

**数据类型：** double

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>Out — 输出信号<div>实数向量</div></summary>
</details>
<div class="details-content">

输出相位调制后的信号，指定为一个长度为 N 的实数向量。

**数据类型：** double

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>码字长度 N — 输入信号的码字长度<div>7 （默认） | 正整数</div></summary>
</details>
<div class="details-content">

码字长度 N ,也是输入向量长度。

</div>
</div>

<div class="details-box">
<details open>
<summary>消息长度 K — 输出信号的消息长度<div>4 （默认） | 正整数</div></summary>
</details>
<div class="details-content">

消息长度 K ，也是输出向量长度。

</div>
</div>

## 版本历史记录

- 在 2026b 推出


