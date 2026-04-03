# RandomIntegerGenerator
---
&nbsp;
生成在指定范围内均匀分布的随机整数。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/RandomIntegerGenerator/RandomIntegerGenerator.png')" style="width:100px;border:black 1px solid;"> 

- **库：** Sysblock / Sources

## 描述

RandomIntegerGenerator 模块生成范围在 [0, M-1] 的均匀分布的随机整数。其中M的值由参数“设置大小”指定。使用此模块可以生成随机的整数值数据。

## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/RandomIntegerGenerator.mo">RandomIntegerGenerator.mo</helpButton>。

我们将一个随机整数模块的参数面板按照如下所示的内容进行设置：

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/RandomIntegerGenerator/RandomIntegerGenerator_Case1.png')" style="width:350px;border:black 1px solid;"> 

在仿真步长为 0.02，仿真时间为 10 时，随机整数模块输出了维度为 2x3 的随机整数。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/RandomIntegerGenerator/RandomIntegerGenerator_Case2.png')" style="width:700px;border:black 1px solid;"> 

## 端口

### 输出

<div class="details-box">
<details open>
<summary>Port_1 — 输出信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

随机整数模块的输出维度为标量，向量或者矩阵。它的数据类型通过“输出数据类型”的参数进行设置。

输出数据中的行数等于“每帧样本数”参数的值。输出数据的列数由参数“设置大小”的维度决定。

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>设置大小 — 随机数的范围大小<div>8（默认） | 正整数 | 正整数组成的向量</div></summary>
</details>
<div class="details-content">

“设置大小”，指定了随机数的范围，为正整数或者正整数组成的向量。该模块生成 [0, M-1] 范围内的随机数。“设置大小”的元素数量决定了从模块中输出的独立通道的数量。

如果该参数为标量，那么所有输出的随机变量是独立的，并且是同分布的。

如果该参数为向量，那么向量的长度决定了输出通道的数量。通道可以具有不同的输出范围。

</div>
</div>




<div class="details-box">
<details open>
<summary>初始种子源 — 随机数种子的初始化方式<div>自动（默认）| 参数</div></summary>
</details>
<div class="details-content">

自动：在仿真时，随机整数模块生成一个随机的种子。

参数：随机整数模块将种子设置为“初始种子”。

</div>
</div>

<div class="details-box">
<details open>
<summary>初始种子 — 随机数种子的初始值<div>0（默认）| 非负数</div></summary>
</details>
<div class="details-content">

如果“初始种子”是常量，那么生成的随机数序列是可重复的。

</div>
</div>


<div class="details-box">
<details open>
<summary>采样时间 — 模块的采样时间<div>1（默认）| 正数，标量</div></summary>
</details>
<div class="details-content">

指定输出信号的每个样本之间的时间（以秒为单位）。如果采样时间为 -1，则输出信号从下游继承采样时间。

</div>
</div>

<div class="details-box">
<details open>
<summary>每帧样本数 — 模块每帧的样本数<div>1（默认）| 正整数</div></summary>
</details>
<div class="details-content">

指定一个正整数，决定输出数据的一个通道中每帧的采样数。

</div>
</div>
  


<div class="details-box">
<details open>
<summary>输出数据类型 — 输出信号的数据类型<div>double（默认）| float | uint8 | uint16 | uint32 | boolean</div></summary>
</details>
<div class="details-content">

输出信号的数据类型可以在“double”, "float", "uint8", "uint16", "uint32", "boolean"中选择。

</div>
</div>

## 版本历史记录

- 在 2025a 推出

## 限制信息

该模块目前仅支持仿真，暂不支持嵌入式代码生成。