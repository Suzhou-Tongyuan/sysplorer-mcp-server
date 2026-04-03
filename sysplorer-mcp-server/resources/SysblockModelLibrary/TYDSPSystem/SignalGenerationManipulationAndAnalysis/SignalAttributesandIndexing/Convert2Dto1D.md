# Convert2Dto1D
---
&nbsp;

将二维矩阵输入转换为一维向量。

**库：** TYDSPSystem / SignalGenerationManipulationAndAnalysis / SignalAttributesandIndexing 

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYDSPSystem/SignalGeneration/SignalAttributes/Convert2Dto1D/1.png')" style="width: 100px; border:black 1px solid;height: auto; transform: scale(1);">

## 描述

Convert2Dto1D 模块支持将二维矩阵转换为一维模块会将一个 $M×N$ 矩阵输入重塑为长度为 $M×N$ 的一维向量。


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>矩阵</div></summary>
</details>
<div class="details-content">

输入数据，指定为二维实数矩阵。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean 

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>向量</div></summary>
</details>
<div class="details-content">
 
输出数据，作为实值向量返回。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean 

</div>
</div>


## 版本历史记录

- 在 2026a 推出

