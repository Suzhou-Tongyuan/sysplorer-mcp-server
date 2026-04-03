# BernoulliBinaryGenerator

生成符合伯努利分布的随机二进制数

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/BernoulliBinaryGenerator/1.png')" style="width:100px;border:black 1px solid;"> 

**库**：Sysblock 模块库 / Sources

## 描述

Bernoulli Binary Generator 模块使用伯努利分布生成随机二进制数。一般使用此模块，生成随机数据以进行数字通信系统的仿真并获取某些性能指标，比如误码率。

该模块的输出可以为标量，行向量，列向量或二维矩阵。输出信号中的行数对应一帧中的样本数，由参数“**每帧样本数**”决定；输出信号中的列数对应通道数，由参数“**输出为 0 的概率**”的元素个数所决定。

## 示例

**示例模型**

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/BernoulliBinaryGenerator.mo">BernoulliBinaryGenerator.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/BernoulliBinaryGenerator/2.png')" style="width:600px;border:black 1px solid;"> 

**参数面板**

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/BernoulliBinaryGenerator/3.png')" style="width:350px;border:black 1px solid;"> 

**参考结果**

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/BernoulliBinaryGenerator/4.png')" style="width:600px;border:black 1px solid;"> 

## 端口

### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">


​	输出信号，可以为标量，向量或矩阵。

**数据类型：double | float | uint8 | uint16 | uint32 | boolean**

</div>
</div>

## 参数


<div class="details-box">
<details open>
<summary>输出为 0 的概率<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

模块输出的值等于 0 的概率。

该参数的值必须在 [0, 1] 之间，并且它的元素个数决定了输出的列数。

</div>
</div>

<div class="details-box">
<details open>
<summary>初始种子源<div>随机数的初始种子的来源</div></summary>
</details>
<div class="details-content">

随机数模块的种子来源，指定为：

​	**自动** — 模块的初始种子由模块自动设置。

​	**参数** — 模块将根据**初始种子**的值来设置随机数种子的初始值。

</div>
</div>



<div class="details-box">
<details open>
<summary>初始种子<div>非负数的初始种子</div></summary>
</details>
<div class="details-content">

随机数种子的初始值，可以为非负数标量。当此参数为常量时，生成的序列是可重复的。虽然初始种子的值可以设置为浮点数，但实例上会进行取整处理。因此如果需要生成不同序列的随机数，应该设置不同整数值的初始种子。

</div>
</div>



<div class="details-box">
<details open>
<summary>采样时间<div>1（默认）| -1 | 正数变量</div></summary>
</details>
<div class="details-content">

该参数和每帧样本数共同控制模块的采样时间。当采样时间为 -1 时，随机数模块将继承模型或其他模块的采样时间。

</div>
</div>



<div class="details-box">
<details open>
<summary>每帧样本数<div>输出信号的每帧的样本数</div></summary>
</details>
<div class="details-content">

输出信号的一个通道中每帧的样本数，指定为正整数标量。该参数的值决定了输出的行数。

</div>
</div>




<div class="details-box">
<details open>
<summary>输出数据类型<div>double（默认）| float | uint8 | uint16 | uint32 | boolean</div></summary>
</details>
<div class="details-content">

输出信号的数据类型。

</div>
</div>






## 版本历史记录

在 MWORKS 2025b 推出

## 限制信息

暂不支持嵌入式代码生成