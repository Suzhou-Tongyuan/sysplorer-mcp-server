# HammingEncoder
---
从二进制矢量数据创建汉明码

**库：** TYCommunication / PHYComponents / ErrorDetectionAndCorrection

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYCommunication/PHYComponents/ErrorDetectionAndCorrection/HammingEncoder/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

HammingEncoder 模块创建具有消息长度 K 和码字长度 N 的汉明码。数字N的形式必须为 $2^M-1$ ，其中 M 是大于或等于 3 的整数。那么 K 等于 N-M 。

该模块接受长度为 K 的列矢量输入信号。输出信号是长度为N的列矢量。 

编码方案使用有限域 GF（2M） 的元素。目前只支持默认设置：
* 要使用默认基本多项式，只需分别输入 N 和 K 作为第一个和第二个对话框参数。该算法使用 gfprimdf（M） 作为 GF（2M）的原始多项式。

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


