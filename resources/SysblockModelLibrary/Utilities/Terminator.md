# Terminator
---
&nbsp;

终止未连接的输出端口

**库：** Sysblock模块库 / Utilities

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/Terminator/Terminator.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

使用 Terminator 模块终止输出端口未连接其他模块的模块。如果您运行的仿真中有一些模块的输出端口未连接任何模块，Sysblock 将发出警告消息。使用 Terminator 模块终止这些模块，可以防止出现此类警告消息。

## 示例

<!-- [![弹球的仿真](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/sldemo_bounceexample_04_zh_CN.png)弹球的仿真此示例使用两个弹球 Simulink® 模型来说明对具有 Zeno 行为的混合动态系统进行建模的不同方法。该示例还提供每种方法的优点。](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/simulation-of-a-bouncing-ball.html)

[![容错燃油控制系统建模](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/modelingafaulttolerantfuelcontrolsystemexample_02_zh_CN.png)容错燃油控制系统建模此示例说明如何结合使用 Stateflow® 和 Simulink® 来高效地进行混合系统建模。这种类型的建模对于具有基于离散事件的多种可能运行模式的系统特别有用。传统的信号流在 Simulink 中处理，而控制配置的更改在 Stateflow 中实现。下面所述的模型表示汽油引擎的燃油控制系统。该系统具有很强的稳健性，因为它可以检测到单个传感器的故障，并且可以动态重新配置控制系统以实现不间断运行。](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/modeling-a-fault-tolerant-fuel-control-system.html)

[![六自由度 (6-DoF) 运动平台](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/sixdegreesoffreedom6dofmotionplatformexample_03_zh_CN.png)六自由度 (6-DoF) 运动平台此示例介绍了一种在 Simulink® 中对六自由度运动建模的方式。您可以使用 Variant Subsystem 模块的“变体 > 覆盖”上下文菜单，在使用“欧拉角”和“四元数”之间进行切换来对运动方程建模。](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/six-degrees-of-freedom-6-dof-motion-platform.html) -->

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/Terminator.mo">Terminator.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/Terminator/Terminator_ex.png')" style="width: 300px; height: auto; transform: scale(0.8);">

### 示例说明

- Step 模块：提供从 0 步变到 1 的输入信号，用于模拟实际输入值的变化；
- Terminator 模块：结束信号线，表示信号在此结束，不再继续传播。这个模块在模型中通常用作占位符，以避免未连接的信号线引发警告或错误。

## 端口

### 输入

<div class="details-box">
<details open>
<summary>x — 输入信号<div>标量 | 向量 | 矩阵 | N 维数组</div></summary>
</details>
<div class="details-content">

使用此端口来处理仿真过程中并不连接到其他端口的输出端口的信号。该端口接受所有数据类型的实信号或复信号。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean

</div>
</div>




<!-- ## 模块特性

| **数据类型**     | Boolean | bus | double | enumerated | fixed point | half | integer | single | string |
| ---------------- | ------------------------------------------------------------ |
| **直接馈通**     | 否                                                         |
| **多维信号**     | 是                                                         |
| **可变大小信号** | 否                                                         |
| **过零检测**     | 否                                                         | -->


## 版本历史记录

- 在 2024b 之前推出

### 限制信息

输入信号暂不支持总线结构，不支持 half、int64、uint64、string、fixedPoint、enum、bus 和 image 的数据类型。

<!-- ## 扩展功能



### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 Verilog 代码和 VHDL 代码。



当您将此模块与生成 HDL 代码的子系统结合使用时，您可以使用该模块来终止仿真。该模块不能包含在硬件实现中。

**HDL 模块属性**

| **PreserveUpstreamLogic** | 控制是否删除未连接的逻辑。默认值为 “off”，这意味着未连接的逻辑不会保留在 HDL 代码中。有关详细信息，请参阅[PreserveUpstreamLogic](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#mw_7ebd067c-8648-4c12-aea5-74d878dc8c21) (HDL Coder)。 |
| ------------------------- | ------------------------------------------------------------ |
|                           |                                                              |



### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。

## 版本历史记录

**在 R2006a 之前推出** -->

## 另请参阅

[Ground](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Sources/Ground.html)

 <!-- | [未连接的模块输出端口](https://ww2.mathworks.cn/help/releases/R2022b/simulink/gui/unconnected-block-output-ports.html)

### 主题

- [模型配置参数：连接诊断](https://ww2.mathworks.cn/help/releases/R2022b/simulink/gui/diagnostics-pane-connectivity.html)
- [对错误和警告进行系统化诊断](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/systematic-diagnosis-of-simulation-errors-and-warnings.html) -->