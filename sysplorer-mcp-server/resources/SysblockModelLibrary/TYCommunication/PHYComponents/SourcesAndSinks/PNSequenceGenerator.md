# PNSequenceGenerator
---
生成伪噪声序列。

**库：** TYCommunication / PHYComponents / SourcesAndSinks

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYCommunication/PHYComponents/SourcesAndSinks/PNSequenceGenerator/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

PN 序列生成器模块通过线性反馈移位寄存器（LFSR）生成伪随机二进制数列。伪噪声序列通常用于伪随机加扰和直接序列扩频系统。 


## 端口


### 输出

<div class="details-box">
<details open>
<summary>y — 伪随机噪声序列<div>二进制向量</div></summary>
</details>
<div class="details-content">
 
输出 PN 序列，以二进制向量形式返回。输出数据类型由**输出数据类型**参数指定。

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>生成多项式 — 生成多项式<div>二进制向量 </div></summary>
</details>
<div class="details-content">

用于确定移位寄存器反馈连接方式的生成多项式，按降幂顺序排列的多项式系数二进制向量。该向量长度必须为 N+1（N 为多项式阶数），首末元素必须为 1，分别表示最高次项和常数项。

**示例：** {1, 0, 0, 0, 0, 0, 1, 0, 1} 。

</div>
</div>


<div class="details-box">
<details open>
<summary>初始状态 — 移位寄存器初始状态<div>{0, 0, 0, 0, 0, 1}（默认）| 二进制向量</div></summary>
</details>
<div class="details-content">

PN 序列生成器在仿真开始时的移位寄存器初始状态，指定为一个二进制值的向量。该向量的长度必须等于由生成多项式（Generator polynomial）指定的多项式阶数。

:::warning 注意

为使模块生成非零序列，初始状态向量必须包含至少一个非零元素。

:::


</div>
</div>


<div class="details-box">
<details open>
<summary>掩码 — 标量移位值<div>0（默认）| 整数标量</div></summary>
</details>
<div class="details-content">

指定为整数标量移位值。此参数决定了 PN 序列相对于初始时刻的延迟。

</div>
</div>


<div class="details-box">
<details open>
<summary>每帧采样数 — 输出信号每通道包含的采样点数<div>1（默认）| 正整数</div></summary>
</details>
<div class="details-content">

指定输出信号单通道中每帧包含的采样点数，以正整数表示。


</div>
</div>


<div class="details-box">
<details open>
<summary>采样时间 — 输出信号采样间隔<div>1（默认）| -1 | 正标量</div></summary>
</details>
<div class="details-content">

正标量值用于指定输出信号各采样点间的时间间隔（单位：秒）。若设置为 -1，则输出信号将继承下游模块的采样时间。

**示例：**

设定为 1 表示采样间隔为 1 秒。

</div>
</div>



## 版本历史记录

- 在 2025b 推出

