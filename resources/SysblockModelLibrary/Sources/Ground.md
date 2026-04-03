# Ground
---
将未连接的输入端口接地

**库：** Sysblock模块库 / Sources

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/Ground/Ground.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

Ground 模块连接到其输入端口不连接到其他模块的模块。如果您使用具有未连接的输入端口的模块运行仿真，Sysblock 会发出警告。使用 Ground 模块将那些未连接的模块接地可以防止出现这些警告。

### 使用定点数据类型

使用定点数据类型时，可能会出现定点数据类型不能准确表示零的情况。在这些情况下，Ground 模块输出尽可能最接近零的非零值。这种行为仅适用于具有非零偏置的定点数据类型。以下表达式是不能表示零的定点数据类型的示例：

- fixdt(0, 8, 1, 1) - 使用斜率 1 和偏置 1 的无符号 8 位数据类型；
- fixdt(1, 8, 6, 3) - 使用斜率 6 和偏置 3 的有符号 8 位数据类型。

### 使用枚举数据类型

使用枚举数据类型时，Ground 模块输出枚举的默认值。此行为是否适用取决于：

- 枚举是否可以表示零；
- 枚举的默认值是否为零。

如果枚举类型没有默认值，则 Ground 模块输出类型定义中的第一个枚举值。

## 示例

<!-- [![Integer and Enumerated Data Type Support in the Ground Block](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink/win64/IntAndEnumDataTypeSupportGroundBlockExample_01.png)Integer and Enumerated Data Type Support in the Ground BlockUse the Ground block to ground block input ports that have integer and enumerated data types.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/integer-and-enumerated-data-type-support-in-ground.html)

[![Fixed-Point Data Type Support in the Ground Block](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink/win64/FixedPointDataTypeSupportGroundBlockExample_01.png)Fixed-Point Data Type Support in the Ground BlockUse the Ground block to ground block input ports that have fixed-point data types.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/fixed-point-datatype-support-in-ground.html)

[![Double Bouncing Ball: Use of Adaptive Zero-Crossing Location](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink_general/win64/sldemo_doublebounceExample_07.png)Double Bouncing Ball: Use of Adaptive Zero-Crossing LocationChoose the correct zero-crossing location algorithm, based on the system dynamics. For Zeno dynamic systems, or systems with strong chattering, you can select the adaptive zero-crossing detection algorithm through the Configure pane:](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/double-bouncing-ball-use-of-adaptive-zero-crossing-location.html)

[![触发子系统](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/triggeredsubsystemsexample_02_zh_CN.png)触发子系统显示触发子系统和不同类型的触发器的模型。](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/triggered-subsystems.html) -->

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/Ground.mo">Ground.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/Ground/Ground_ex.png')" style="width: 300px; height: auto; transform: scale(0.8);">

### 示例说明

由于 Ground 模块的作用，仿真过程中不会出现未连接输入端口的警告。  

- Ground 模块：提供一个零值信号，用于接地或将未连接的信号端口设置为零值，避免仿真时出现未连接端口的警告；
- Step 模块：生成一个阶跃信号，这里用于提供一个从 0 变为 1 的信号，模拟信号的突变；
- Sum 模块：将两个输入信号相加，这里用于将 Step 模块的输出和 Ground 模块的零值相加，模拟信号的组合。

## 端口

### 输出

<div class="details-box">
<details open>
<summary>y — 接地信号<div>标量</div></summary>
</details>
<div class="details-content">

Ground 模块输出具有零值的标量信号，其数据类型与所连接的端口相同。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | fixedPoint | enum

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

接地信号的数据类型暂不支持 half、int64、uint64、string、bus 和 image 的数据类型。

<!-- ## 扩展功能



### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 Verilog 代码和 VHDL 代码。



HDL Coder™ 提供影响 HDL 实现和综合逻辑的额外配置选项。

**HDL 架构**

此模块具有一个默认 HDL 架构。

**HDL 模块属性**

| **ConstrainedOutputPipeline** | 通过移动设计中现有延迟的方式来放置在输出端的寄存器的数量。分布式流水线处理不会重新分发这些寄存器。默认值为 0。有关详细信息，请参阅[ConstrainedOutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#btp8gmp) (HDL Coder)。 |
| ----------------------------- | ------------------------------------------------------------ |
| **OutputPipeline**            | 要在生成的代码中插入的输出流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 0。有关详细信息，请参阅[OutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-26) (HDL Coder)。 |

**复数数据支持**

此模块支持复信号的代码生成。



### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。

## 版本历史记录

**在 R2006a 之前推出** -->

<!-- ## 另请参阅

### 主题

- [未连接的模块输入端口](https://ww2.mathworks.cn/help/releases/R2022b/simulink/gui/unconnected-block-input-ports.html) -->