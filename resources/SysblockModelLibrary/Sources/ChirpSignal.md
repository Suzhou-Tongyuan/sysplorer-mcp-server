# ChirpSignal
---
输出线性 chirp 信号（频率随时间线性变化的正弦波）。

- **库：** Sysblock / Sources

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/ChirpSignal/ChirpSignal.png')" style="width:100px;border:black 1px solid;"> 

## 描述

ChirpSignal 模块生成频率随时间按线性速率增加的正弦波。可以使用此模块对非线性系统进行频谱分析。模块的输出具体由参数初始频率、目标时间和目标时间的频率所决定。

## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/ChirpSignal.mo">CounterFreeRunning.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/ChirpSignal/ChirpSignal_example.png')" style="width:600px;border:black 1px solid;border-top: 1px solid black;"> 

### 仿真结果

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/ChirpSignal/Example_output.png')" style="width:600px;border:black 1px solid;border-top: 1px solid black;"> 


## 端口

### 输出

<div class="details-box">
<details open>
<summary>Port_1 — chirp 信号<div>标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">

频率随时间按线性速率增加的正弦波。chirp 信号可以是标量、向量、矩阵或多维数组。

**数据类型：** double

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>初始频率（Hz）<div>0.1（默认）| 标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">

指定信号的初始频率。

</div>
</div>

<div class="details-box">
<details open>
<summary>目标时间（秒）<div>100（默认）| 标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">

频率达到目标时间的频率参数值的时间。

</div>
</div>

<div class="details-box">
<details open>
<summary>目标时间的频率（Hz）<div>1（默认）| 标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">

指定信号在目标时间的频率。

</div>
</div>


## 版本历史记录

- 在 2025a 推出

### 限制信息

- 仿真的开始时间必须为 0
- 输出数据类型仅支持 double