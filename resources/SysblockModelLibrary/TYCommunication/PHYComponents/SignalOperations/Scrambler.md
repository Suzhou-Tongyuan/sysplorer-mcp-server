# Scrambler
---
干扰输入信号。

**库：** TYCommunication / PHYComponents / SignalOperations

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYCommunication/PHYComponents/SignalOperations/Scrambler/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

干扰器模块对输入数据施加乘法干扰处理。

干扰的主要目的是减少传输信号中连续 0 或 1 序列的长度。过长的 0 或 1 序列会导致传输同步问题。该原理图展示了干扰器的工作机制：所有加法器均执行模 N 运算（N 由计算基础参数指定）。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYCommunication/PHYComponents/SignalOperations/Scrambler/2.png')">

在每个时间步长，输入信号会使寄存器内容依次移位。通过设置干扰多项式参数，用户可以指定干扰器中每个开关的通断状态。


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入数据信号<div>向量</div></summary>
</details>
<div class="details-content">

输入数据信号，指定为一个 $N_{s}$ × 1 的向量，其中 $N_{s}$ 表示输入信号的样本数。输入值必须是 0 至（计算基础 -1）之间的整数。

**数据类型：** int32 

</div>
</div>

<div class="details-box">
<details open>
<summary>reset — 复位干扰器<div>标量</div></summary>
</details>
<div class="details-content">

复位干扰器，指定为标量输入。当该端口接收到非零输入时，干扰器将被复位。

**依赖关系：**  

要启用此端口，需将"初始状态源"设为 Dialog Parameter，并勾选"通过端口非零输入复位"。

</div>
</div>

<div class="details-box">
<details open>
<summary>states— 初始状态<div>向量</div></summary>
</details>
<div class="details-content">

仿真开始时干扰器寄存器的初始状态，指定为一个非负整数向量。ISt  的长度必须与"干扰多项式"参数的阶数相同，且向量元素值必须为 0 至（计算基础 -1）之间的整数。

**依赖关系：**  

启用此端口需将**初始状态源**设为 Input port。

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>y — 输出干扰数据<div>向量</div></summary>
</details>
<div class="details-content">

输出经过干扰处理的数据，返回一个 $N_{s}$ × 1 的向量，其中 $N_{s}$ 等于输入信号的样本数。

**数据类型：** double

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>计算基数 — 计算基数<div>4（默认）| 非负整数</div></summary>
</details>
<div class="details-content">

指定干扰器中用于模运算的计算基础，取值为非负整数。该模块的输入和输出均为 0 至（计算基础 - 1）范围内的整数。

</div>
</div>

<div class="details-box">
<details open>
<summary>扰动多项式 — 定义干扰器连接的多项式<div>二进制向量</div></summary>
</details>
<div class="details-content">

定义干扰器内部连接的多项式，可指定为二进制向量。

</div>
</div>

<div class="details-box">
<details open>
<summary>初始状态源 — 干扰器初始状态源<div>Dialog Parameter（默认）| Input port</div></summary>
</details>
<div class="details-content">

- Dialog Parameter - 通过**初始状态**参数设置；

- Input port - 通过 states 端口动态设置。

</div>
</div>

<div class="details-box">
<details open>
<summary>初始状态 — 干扰器寄存器初始状态<div>{0, 1, 2, 3}（默认）| 非负整数向量</div></summary>
</details>
<div class="details-content">

仿真开始时干扰器寄存器的初始状态，指定为非负整数向量。其长度必须与扰动多项式参数的阶数相同，且元素值必须为 0 至（计算基数 - 1）范围内的整数。

**依赖关系：**  

仅当**初始状态源**设为 Dialog Parameter 时生效。

</div>
</div>

<div class="details-box">
<details open>
<summary>通过端口非零输入复位 — 启用复位功能<div>off（默认）| on</div></summary>
</details>
<div class="details-content">

勾选此项可通过 reset 端口复位解扰器

**依赖关系：**

仅当**初始状态源**设为 Dialog Parameter 时有效。

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
