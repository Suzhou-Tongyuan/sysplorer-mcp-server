# AGC
---
自适应调整增益恒定的信号电平输出。

**库：** TYCommunication / PHYComponents / SynchronizationAndReceiverDesign 

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYCommunication/PHYComponents/SynchronizationAndReceiverDesign/AGC/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

自动增益控制器（AGC）块自适应调整其增益以在输出处实现恒定的信号电平。


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入数据信号<div>向量</div></summary>
</details>
<div class="details-content">

输入信号，指定为实数向量。


**数据类型：** double 

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>向量</div></summary>
</details>
<div class="details-content">
 
输出信号，维度与输入信号相同。

**数据类型：** double 

</div>
</div>

<div class="details-box">
<details open>
<summary>powerlevel — 功率估计<div>标量</div></summary>
</details>
<div class="details-content">
 
功率水平估计，作为 Ns 元素列向量返回。NS 是输入信号的长度。您可以使用功率电平作为能量检测器输出。

**依赖条件** 

 要添加此端口，需勾选**使能输入功率估计输出**

 **数据类型：** double 

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>步长 — 增益更新的步长<div>0.01（默认）|正标量 </div></summary>
</details>
<div class="details-content">

增益更新的步长，指定为正标量。增加步长使AGC能够更快地响应输入信号电平的变化，但在达到稳态运行后增加了输出信号电平的变化。

**数据类型：** double 

</div>
</div>


<div class="details-box">
<details open>
<summary>期望输出功率(W) — 期望输出功率<div>1（默认）| 正标量</div></summary>
</details>
<div class="details-content">

目标输出功率电平，指定为正标量。功率等级以瓦特为单位。


**数据类型：** double 

</div>
</div>


<div class="details-box">
<details open>
<summary>平均长度 — 平均窗长度<div>100（默认）| 正整数</div></summary>
</details>
<div class="details-content">

样本中平均窗口的长度，指定为正整数。

**数据类型：** int32

</div>
</div>

<div class="details-box">
<details open>
<summary>最大功率增益 — 最大功率增益（dB）<div>60（默认）| 正标量</div></summary>
</details>
<div class="details-content">

以 dB 为单位的最大功率增益，指定为正标量。当一个小的输入信号功率突然增加时，大的增益调整会引起削波。使用此属性可以通过限制 AGC 应用于输入信号的增益来避免大的增益调整。

**数据类型：** double 

</div>
</div>


<div class="details-box">
<details open>
<summary>使能输入功率估计输出 — 输入功率估计使能<div>on（默认）| off</div></summary>
</details>
<div class="details-content">

选择此复选框可提供一个输出端口Px，该端口返回输入信号功率的估计值。


**数据类型：** String 

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
