# BinaryLinearEncoder
---
从二进制矢量数据创建线性块码

**库：** TYCommunication / PHYComponents / ErrorDetectionAndCorrection

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYCommunication/PHYComponents/ErrorDetectionAndCorrection/BinaryLinearEncoder/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

BinaryLinearEncoder 模块使用指定的生成器矩阵创建二进制线性块码。如果 K 是代码的消息长度，则生成器矩阵参数必须有 K 行。如果 N 是代码的码字长度，则生成器矩阵必须有 N 列。

该模块接受包含 K 个元素的列矢量输入信号。此块输出长度为 N 个元素的列向量。

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
<summary>生成矩阵 — 代码生成器的矩阵<div></div></summary>
</details>
<div class="details-content">

K 乘 N 矩阵，其中 K 是消息长度，N 是码字长度。

</div>
</div>


## 版本历史记录

- 在 2026b 推出


