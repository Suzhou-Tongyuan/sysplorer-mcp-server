# Merge
---
&nbsp;

将多个信号合并为一个信号

**库：** Sysblock模块库 / Utilities

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/Merge/Merge.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

Merge 模块可将多个输入合并为单个输出。输出值始终等于其驱动模块最近计算的输出。通过设置**输入数目**参数来指定输入数目。

请将一个 Merge 模块用于将在不同时间更新的输入信号交叉成一个合并信号，交叉值在合并信号中保留其各自的身份和时间。

<!-- 要将同时更新的信号合并成数组或矩阵信号，请使用 [Concatenate](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/vectorconcatenate.html) 模块。 -->

### Merge 模块的使用原则

使用 Merge 模块时，请遵循以下原则：

- 始终使用条件执行子系统来驱动 Merge 模块，而不涉及任何中间模块；
- 确保在任何时间步都最多只有一个驱动条件执行子系统在执行中；
- 确保所有输入信号具有相同的采样时间；
- 不要为 Merge 模块的输入信号创建分支；
- 不要记录输入到 Merge 模块的信号；
- 不要指定 Merge 模块的模块执行优先级；
- Merge 模块支持将不同任务中的信号合并到一个根 Outport 模块。

<!-- 对于一个 Merge 模块的每个输入，最顶层的非虚拟源必须为条件执行子系统（不包括 For Iterator 或 While Iterator 子系统）。

下一个图显示了有效的 Merge 模块用法，它合并来自两个条件执行子系统的信号。

![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/merge_usage.png) -->

<!-- ### 总线支持

Merge 模块支持总线。输入可以是满足下列限制条件的虚拟或非虚拟总线信号：

- 输入数目必须大于一；
- **初始输出**必须为零、非零标量或有限数值结构体；
- 必须清除**允许端口宽度不等**复选框；
- 所有输入都必须为总线且必须相同（所有元素的层次结构相同，并具有相同的名称和属性）。

Merge 模块的非虚拟总线输入中的所有信号必须具有相同的采样时间。 -->
<!-- 您可以使用 [Rate Transition](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/ratetransition.html) 模块更改总线中单个信号或所有信号的采样时间。 -->

<!-- ### 合并 S-Function 输出

对于来自 S-Function 模块的信号，仅当用来存储 S-Function 模块输出的内存可重用时，才能使用 Merge 模块合并该信号。如果某个模型将不可重用的 S-Function 模块端口连接到 Merge 模块，则当您尝试更新或仿真模型时，Simulink® 将显示错误消息。请参阅 [ssSetOutputPortOptimOpts](https://ww2.mathworks.cn/help/releases/R2022b/simulink/sfg/sssetoutputportoptimopts.html)。 -->

### 多任务根输出

连接到一个根 Outport 模块的 Merge 模块允许合并不同任务中的信号，方法是允许这些信号同时写入该根 Outport 模块。源的联合采样时间会赋给该 Merge 模块。

同一任务中的 Merge 模块的所有源均应在条件执行子系统中，且这些子系统不应在同一时间步中同时输出。

<!-- ## 限制 -->

<!-- - 所有连接到 Merge 模块的信号在功能上都是同一信号。因此，这些信号必须满足一个给定信号最多只能有一个关联信号对象的限制条件。有关详细信息，请参阅 [Simulink.Signal](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/simulink.signal.html)。

- 如果 Merge 模块的输入来自单一发起方，则不会对其执行运行时诊断。例如，单一发起方可以是一个执行连接到 Merge 模块的函数调用子系统的 Stateflow 图。

- 禁用时，不要将要合并的多个条件执行子系统的输出端口设置为重置。此操作可能导致多个子系统同时更新该模块。尤其是，禁用的子系统通过重置其输出来更新 Merge 模块，而使能子系统通过计算其输出来更新该模块。

  为了防止此行为的发生，对于要合并的每个条件执行子系统，请将 Outport 模块参数**禁用时的输出**设置为“保持”。

- Merge 模块不接受其元素被重新排序或者只有部分元素被选中的输入信号，如下图所示。

  ![Simulink block diagram including 2 enabled subsystems, each of whose outputs is connected to a Selector block. The outputs of both Selector blocks are connected to a Merge block. One Selector block reorders its input signal before passing it to the Merge block, and the other Selector block selects a subset of its input signal before passing it to the Merge block.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/merge_block_reorder_sigs_not_allowed.png)

- 不要将已在条件执行子系统外部进行了合并的输入信号连接到模块。

可使用总线数组作为 Merge 模块的输入信号，但存在以下限制：

- **允许端口宽度不等** - 清除此参数。

- **初始条件** - 可为此参数指定：

  

  - 值 0。在这种情况下，总线数组中的每个信号都使用初始值 0。
  - 结构体数组，为总线数组中的每个信号指定初始条件。
  - 标量结构体，为总线类型定义的每个元素指定初始条件。使用此方法可为数组中的每条总线指定相同的初始条件。 -->

  
## 示例

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/Merge2.mo">Merge2.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/Merge/Merge_ex.png')" style="width: 900px; height: auto; transform: scale(0.8);">

<!-- [![Merge Block with Input from Atomic Subsystems](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink/win64/MergeBlockWithInputFromAtomicSubsystemsExample_02.png)Merge Block with Input from Atomic SubsystemsA Merge block with inputs from two atomic subsystems.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/merge-block-with-input-from-atomic-subsystems.html)

[![Merge Block with Unequal Input Widths Example](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink/win64/MergeBlockWithUnequalInputWidthsExample_02.png)Merge Block with Unequal Input Widths ExampleUse the Merge block with inputs ports that have different widths.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/merge-block-with-unequal-input-widths-example.html)

[![Merging Signals](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink_features/win64/MergingSignalsExample_01.png)Merging SignalsUse conditionally executed subsystems and the Merge block to combine two inputs into a single output.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/merging-signals.html) -->


## 端口


### 示例说明

在这个示例中，我们使用了一个 RepeatingSequence 模块生成一个控制信号，该信号的值在 1 和 2 之间交替变化。这个控制信号输入到 If 模块中，根据条件 u1 > 0 判断哪个 [IfActionSubsystem](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SubSystems/If.html#jump1) 模块应该执行。

- If 模块的作用：

  If 模块根据条件表达式 u1 > 0 判断哪个子系统应该执行。如果条件成立，则激活第一个 IfActionSubsystem 模块；否则，激活第二个 IfActionSubsystem 模块；

- IfActionSubsystem 模块的作用：

  IfActionSubsystem 模块是一个条件执行子系统，只有在其控制信号满足条件时才会执行。
  在这个示例中，第一个 IfActionSubsystem 模块输出值为 1，第二个 IfActionSubsystem 模块输出值为 0。

- Merge 模块的作用：

  Merge 模块将两个条件执行子系统的输出合并为一个信号。在任何时间步，Merge 模块的输出值等于其驱动块中最最近计算的输出。
  通过设置“输入的数目”为 2，Merge 模块可以接受两个输入信号。
  为了确保在任何时间步最多只有一个条件执行子系统执行，必须确保所有输入信号具有相同的采样时间。

## 端口

### 输入

<div class="details-box">
<details open>
<summary>u1 — 第一个输入信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

第一个输入信号与其他输入信号合并。

**数据类型：** float | double | half | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | fixedPoint | enum

</div>
</div>



<div class="details-box">
<details open>
<summary>un — 第 n 个输入信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

第 n 个输入信号与其他输入信号合并。

**数据类型：** float | double | half | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | fixedPoint | enum

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

由输入信号合并而成的输出信号。

**数据类型：** float | double | half | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | fixedPoint | enum

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>输入的数目 — 要合并的输入信号的数量<div>2 （默认） | integer</div></summary>
</details>
<div class="details-content">

指定要合并的输入信号的数量。该模块为每个输入信号创建一个端口。

</div>
</div>




<!-- #### 编程用法

| **模块参数**：Inputs |
| ---------------------- |
| **类型：**字符向量     |
| **值：**整数           |
| **默认值：**'2'      | -->


<div class="details-box">
<details open>
<summary>初始输出 — 初始输出值<div>0（默认） | 标量 | 向量</div></summary>
</details>
<div class="details-content">

指定输出信号的初始值。如果不指定初始输出值，初始输出将取决于初始化模式和驱动模块。

</div>
</div>




<!-- 在 [Simplified Initialization Mode](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/simplified-initialization-mode.html) 中，若未指定**初始输出**的值（空矩阵 []），模块将使用输出数据类型的默认初始值。有关默认初始值的信息，请参阅[初始化信号值](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/signal-values.html#bs9ikmf)。在 [Classic Initialization Mode](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/classic-initialization-mode.html)中，若未指定**初始输出**的值（空矩阵 []），则模块的初始输出等于最近计算的驱动模块的初始输出。由于这些来源的初始化顺序可能不同，因此模型的仿真和代码生成的初始化可能不一致。

#### 编程用法

| **模块参数**：InitialOutput |
| ----------------------------- |
| **类型：**字符向量            |
| **值：**标量 \| 向量          |
| **默认值：**'[ ]'           | -->



<!-- ### 允许端口宽度不等 — 允许输入具有不同维度 off （默认） | on



选择此参数可允许模块接受元素数目彼此不同的输入，或接受与输出具有不同元素数目的输入。模块还允许您为每个输入信号指定相对于输出信号开始时的偏移量。输出信号的宽度为


max(w1+o1, w2+o2, ... wn+on)


其中 w1, ... wn 是输入信号的宽度，o1, ... on 是输入信号的偏移量。

如果清除该参数，Merge 模块只接受相同维度的输入，并输出与输入具有相同维度的信号。



**注意**

除非您的模型在使用经典初始化模式，否则不要选择此参数。

#### 编程用法

| **模块参数**：AllowUnequalInputPortWidths |
| ------------------------------------------- |
| **类型：**字符向量                          |
| **值：**'off' | 'on'                    |
| **默认值：**'off'                         | -->


<!-- 
### 输入端口偏移量 — 输入信号的偏移量 [ ] （默认） | 向量



输入向量以指定每个输入信号相对于输出信号开始时的偏移量。

#### 依存关系

要启用此参数，请选择**允许端口宽度不等**。

#### 编程用法

| **模块参数**：InputPortOffsets |
| -------------------------------- |
| **类型：**字符向量               |
| **值：**标量 \| 向量             |
| **默认值：**'[ ]'              | -->



<!-- ## 模块特性

| **数据类型**     | Boolean | bus | double | enumerated | fixed point | half | integer | single | string |
| ---------------- | ------------------------------------------------------------ |
| **直接馈通**     | 是                                                         |
| **多维信号**     | 是                                                         |
| **可变大小信号** | 否                                                         |
| **过零检测**     | 否                                                         | -->


## 版本历史记录

- 在 2024b 之前推出

### 限制信息


1. 暂不支持允许端口宽度不等的复选框；  
2. 暂不支持设定输入端口偏移量；    
3. 暂不支持int64、uint64、bus 和 image 的输入输出数据类型。


<!-- ## 扩展功能



### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。

在代码生成工作流中，当 Merge 模块接收固定值和非固定采样时间时，必须满足以下条件之一。否则 Simulink 将显示错误。

- 常量值的来源是接地信号。

- 常量值的来源是具有不可调参数的常量模块。

  - 只有一个常量模块为 Merge 模块提供值。
  - Merge 模块的所有其他输入信号都来自条件执行子系统。
  - Merge 模块以及所有条件执行子系统的 Outport 模块不指定任何初始输出。

  



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 Verilog 代码和 VHDL 代码。

HDL Coder™ 提供影响 HDL 实现和综合逻辑的额外配置选项。



**HDL 架构**

此模块具有一个默认 HDL 架构。

**HDL 模块属性**

| **ConstrainedOutputPipeline** | 通过移动设计中现有延迟的方式来放置在输出端的寄存器的数量。分布式流水线处理不会重新分发这些寄存器。默认值为 0。有关详细信息，请参阅[ConstrainedOutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#btp8gmp) (HDL Coder)。 |
| ----------------------------- | ------------------------------------------------------------ |
| **InputPipeline**             | 要在生成的代码中插入的输入流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 0。有关详细信息，请参阅[InputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-25) (HDL Coder)。 |
| **OutputPipeline**            | 要在生成的代码中插入的输出流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 0。有关详细信息，请参阅[OutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-26) (HDL Coder)。 |



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。

## 版本历史记录

**在 R2006a 之前推出** -->

## 另请参阅

[Switch](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SignalRouting/Switch.html)
 <!-- | [Manual Switch](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/manualswitch.html) -->

<!-- ### 主题 -->
<!-- 
- [条件执行子系统概述](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/about-conditional-subsystems.html)
- [条件子系统初始输出值](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/specify-or-inherit-conditional-subsystem-initial-values.html)
- [Conditional Subsystem Output Values When Disabled](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/set-output-values-when-conditional-subsystem-is-disabled.html) -->