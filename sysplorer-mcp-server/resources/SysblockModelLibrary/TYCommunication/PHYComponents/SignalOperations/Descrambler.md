# Descrambler
---
解扰输入信号。

- **库:**  TYCommunication / PHYComponents / SignalOperations

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYCommunication/PHYComponents/SignalOperations/Descrambler/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

解扰器模块对输入数据实施乘法解扰处理，其功能与发射端使用的加扰器模块互为逆运算。

该原理图展示了乘法解扰器的运算过程。其中加法器与减法器均采用模 N 运算，N 值由**计算基数**参数指定。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYCommunication/PHYComponents/SignalOperations/Descrambler/2.png')"> 

在每个时间步长，输入信号会触发寄存器内容顺序移位。通过**扰动多项式**参数可配置解扰器各开关的通断状态。要使解扰器准确还原加扰器操作，需确保两个模块采用相同的参数配置。若加扰器与解扰器之间不存在信号延迟，二者的**初始状态**参数必须保持一致。


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>向量</div></summary>
</details>
<div class="details-content">

输入信号，指定为 $N_{s}$ × 1 的向量，其中 $N_{s}$ 表示输入信号的样本数。输入值必须为 0 至（计算基数 -1）范围内的整数。

**数据类型：** int32

</div>
</div>

<div class="details-box">
<details open>
<summary>reset — 重置加扰器<div>标量</div></summary>
</details>
<div class="details-content">

加扰器复位信号，指定为标量。当该端口接收到非零输入时，将触发加扰器复位。

**依赖关系：**

启用此端口需同时满足：

- 将**初始状态源**设为 Dialog Parameter；

- 勾选**通过端口非零输入复位**。

</div>
</div>


<div class="details-box">
<details open>
<summary>states — 寄存器初始状态<div>标量</div></summary>
</details>
<div class="details-content">

仿真开始时解扰器寄存器的初始状态，指定为非负整数向量。ISt 向量的长度必须与"加扰多项式"参数的阶数相同，且各元素值必须为 0 至（计算基数 -1）范围内的整数。

**依赖关系：**

启用此端口需将**初始状态源**设为 Input port。

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 解扰数据输出<div>向量</div></summary>
</details>
<div class="details-content">

解扰后的输出数据，以 $N_{s}$ × 1 的向量形式返回，其中 $N_{s}$ 等于输入信号的样本数。

**数据类型：** double

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>计算基数 — 计算基数<div>4（默认）| 非负整数</div></summary>
</details>
<div class="details-content">

用于解扰器中模运算的计算基数，指定为非负整数。该模块的输入和输出均为 0 至（计算基数 -1）范围内的整数。

</div>
</div>


<div id="扰动多项式—定义解扰器连接的多项式" class="jump-target"></div>
<div class="details-box">
<details open>
<summary>扰动多项式 — 定义解扰器连接的多项式<div>二进制向量</div></summary>
</details>
<div class="details-content">

定义解扰器连接的多项式，可指定为二进制向量。

</div>
</div>

<div id="初始状态源—解扰器初始状态设置方式" class="jump-target"></div>
<div class="details-box">
<details open>
<summary>初始状态源 — 解扰器初始状态设置方式<div>Dialog Parameter（默认）| Input port</div></summary>
</details>
<div class="details-content">

- Dialog Parameter - 通过**初始状态**参数设置；
- Input port - 通过 states 端口动态设置。

</div>
</div>

<div id="初始状态—解扰器寄存器初始值" class="jump-target"></div>
<div class="details-box">
<details open>
<summary>初始状态 — 解扰器寄存器初始值<div>{0, 1, 2, 3}（默认）| 非负整数向量</div></summary>
</details>
<div class="details-content">

仿真开始时解扰器寄存器的初始状态，指定为非负整数向量。向量长度必须与扰动多项式阶数相同，元素取值必须在 0 至（计算基数 -1）范围内。

**依赖关系：**仅当**初始状态源**设为 Dialog Parameter 时生效

</div>
</div>


<div id="通过端口非零输入复位—启用端口复位功能" class="jump-target"></div>
<div class="details-box">
<details open>
<summary>通过端口非零输入复位 — 启用端口复位功能<div>off（默认）| on</div></summary>
</details>
<div class="details-content">

勾选此项可通过 reset 端口复位解扰器。

**依赖关系：** 仅当**初始状态源**设为 Dialog Parameter 时有效

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
