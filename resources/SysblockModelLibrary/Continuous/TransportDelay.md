# TransportDelay
---
&nbsp;

按给定的时间量延迟输入。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/TransportDelay/1.png')" style="width: 100px; height: auto; transform: scale(1);">

**库：** Sysblock 模块库 / Continuous

## 描述

Transport Delay 模块可按指定的时间量延迟输入。可使用此模块实现时滞的仿真。此模块的输入可以是连续信号和离散信号。

在仿真开始时，模块输出**初始输出**参数，直到仿真时间超过**时滞**参数。然后，模块开始生成延迟的输入。在仿真期间，模块将输入点和仿真时间存储在缓冲区中。可通过**初始缓冲区大小**参数指定此大小。

如果需要某个时间的输出，而存储的输入值没有对应的时间，模块会在点之间进行线性插值。当延迟小于步长时，模块会根据最后一个输出点外插，这可能会导致结果不准确。因为模块没有直接馈通，无法使用当前输入来计算输出值。例如，假定一个定步长仿真的步长为 1，当前时间为 t = 5。如果延迟为 0.5，模块必须在 t = 4.5 时生成点。因为最新存储的时间值是 t = 4，模块将执行正向外插。

Transport Delay 模块不会对离散信号进行插值。相反，模块会返回所需时间处的离散值。
此模块与 Unit Delay 模块不同，后者仅延迟和保持采样命中点的输出。

## 示例

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continuous/TransportDelay.mo">TransportDelay.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/TransportDelay/2.png')" style="width: 500px; height: auto; transform: scale(1);">

### 参考结果

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/TransportDelay/3.png')" style="width: 800px; height: auto; transform: scale(1);border-top: 1px solid black;">

## 端口

### 输入

<div class="details-box">
<details open>
<summary>Port_1 — 输入信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

要延迟的输入信号，指定为标量、向量或矩阵。
当时滞参数值为 0 时，此端口具有直接馈通。由于时滞参数是运行时可调的，因此软件将 Transport Delay 模块视为此端口始终具有直接馈通。  

**数据类型：** double

</div>
</div>


### 输出


<div class="details-box">
<details open>
<summary>Port_1  — 输出信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

输入信号，延迟指定的时间量。输出信号与输入信号具有相同的维度和数据类型。  


</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>时滞 — 时滞 <div>1(默认) | 标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

输入信号在传播到输出之前要延迟的仿真时间量，指定为非负标量、向量或矩阵。

</div>
</div>


<div class="details-box">
<details open>
<summary>初始输出 — 初始输出值<div>0 (默认) | 标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

指定模块在仿真时间首次超过输入的时滞量之前生成的输出，指定为标量、向量或矩阵。  
限制：此模块的初始输出不能为 inf 或 NaN。  
在仿真运行时期间不能更改 Run-to-run tunable parameter。但是，在仿真开始之前更改此参数不会使得加速或快速加速重新生成代码。

</div>
</div>

<div class="details-box">
<details open>
<summary>初始缓冲区大小 — 初始内存分配 <div>1024 (默认) | 正整数标量</div></summary>
</details>
<div class="details-content">

- 如果输入点数超出初始缓冲区大小，模块将分配更多内存；
- 仿真结束后，会通过消息显示需要的总缓冲区大小。

::: tip 提示 
由于分配内存会降低仿真速度，因此如果仿真速度很重要，请谨慎选择此值；
对于长时滞，此模块可能会使用大量内存，特别是对于维度化输入。
:::

</div>
</div>


<div class="details-box">
<details open>
<summary>使用固定缓冲区大小 — 使用固定大小的缓冲区<div>off (默认) | on</div></summary>
</details>
<div class="details-content">

选中此复选框可使用固定大小缓冲区保存之前时间步的输入数据。  
可使用初始缓冲区大小参数指定缓冲区大小。如果缓冲区已满，新数据将替换缓冲区中已有的数据。

</div>
</div>

## 版本历史记录

- 在 2025a 推出

### 限制信息

- 暂不支持嵌入式代码生成；
- 不支持总线、枚举值类型。