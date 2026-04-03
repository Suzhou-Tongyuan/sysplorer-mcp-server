# SignalFromWorkspace
---
&nbsp;

从 Syslab 工作区导入信号。

**库：** TYDSPSystem / SignalGenerationManipulationAndAnalysis / SignalGeneration

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYDSPSystem/SignalGeneration/SignalGeneration/SignalFromWorkspace/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

SignalFromWorkspace 模块将信号从 Syslab 工作区导入 Sysblock 模型。**信号源**参数指定包含要导入信号的 Syslab 工作区变量的名称。

## 端口

### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>实数标量 | 实数向量</div></summary>
</details>
<div class="details-content">
 
输出信号，维度与每帧信号采样数一致。

**数据类型：** double 

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>信号源 — 导入的信号<div>1:10（默认） </div></summary>
</details>
<div class="details-content">

从 Syslab 中导入信号的 Syslab 工作区变量的名称。

</div>
</div>

<div class="details-box">
<details open>
<summary>信号源维度 — 指定信号源维度<div>{1}（默认） </div></summary>
</details>
<div class="details-content">

Syslab 信号源的维度。指定为长度为 1 的整型向量。

</div>
</div>

<div class="details-box">
<details open>
<summary>采样时间 - 输出采样周期<div>1（默认）| 正实数标量</div></summary>
</details>
<div class="details-content">

随机输出序列的采样周期 Ts，指定为正的有限标量。输出帧周期为 MTs，其中 M 为每帧采样数。

</div>
</div>

<div class="details-box">
<details open>
<summary>每帧采样数 - 输出帧采样数<div>1（默认）| 正整数标量</div></summary>
</details>
<div class="details-content">

每个输出帧中的样本数 M，指定为正整数标量。

</div>
</div>

<div class="details-box">
<details open>
<summary>尾部信号的输出方式 - 最终导入信号的输出值<div>Setting to zero (default) | Holding final value | Cyclic repetition</div></summary>
</details>
<div class="details-content">

指定生成所有指定信号样本后的输出。

 - 当指定为 **Setting to zero** 时，模块在导入信号的最后一帧后，会在仿真持续时间内生成零值输出；
 - 当指定为 **Holding final value** 时，模块在生成信号的最后一帧后，会在仿真持续时间内重复最后一个样本；
 - 当指定为 **Cyclic repetition** 时，模块在到达信号的最后一个样本后，会从头开始重复信号。

模块不会将导入信号外推到最后一个样本之后。

</div>
</div>

## 版本历史记录

- 在 2025b 推出

## 限制信息

- 该模块暂不支持自动识别信号源维度，需通过**信号源维度**参数手动设定；
- 使用该模块从 Syslab 工作区需从使 Syslab 中打开Sysplorer，同时勾选: 主页——>选项——>环境——>常规——>检查前自动同步syslab工作区数据选项，且仅支持导入一维向量信号。
