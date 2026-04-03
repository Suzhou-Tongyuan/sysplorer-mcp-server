# ActionPort
---
IfActionSubsystem 或 SwitchCaseActionSubsystem 模块的动作信号的控制端口

**库：** Sysblock模块库 / SubSystems

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SubSystems/ActionPort/ActionPort.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

ActionPort 模块控制下列子系统模块的执行：

- 连接到 [If](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SubSystems/If.html) 模块的 [IfActionSubsystem](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SubSystems/If.html#jump1) 模块；
- 连接到 [SwitchCase](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SubSystems/SwitchCase.html) 模块的 [SwitchCaseActionSubsystem](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SubSystems/SwitchCase.html#jump1) 模块。

<!-- - Stateflow® 图中基于 Simulink 的状态。请参阅[Create and Edit Simulink Based States](https://ww2.mathworks.cn/help/releases/R2022b/stateflow/ug/create-a-simulink-state.html) (Stateflow)。 -->

## 示例

ActionPort 模块的应用示例请参见 [If](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SubSystems/If.html#jump3) 模块和 [SwitchCase](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SubSystems/SwitchCase.html#SwitchCase2) 模块的示例。

<!-- [![Simulink 子系统语义](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/simulinksubsystemsemanticsexample_01_zh_CN.png)Simulink 子系统语义这组示例说明不同类型的 Simulink® 子系统，以及对这些子系统进行仿真时使用的语义。每个示例都提供了对模型的说明以及控制模型执行方式的诀窍。](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/simulink-subsystem-semantics.html)

[![If-Then-Else 模块](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/ifthenelseblocksexample_01_zh_CN.png)If-Then-Else 模块此示例说明将正弦波馈入 If Action Subsystem 模块的效果。它旨在说明 If Action Subsystem 模块和 Enabled Subsystem 模块之间的相似性。](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/if-then-else-blocks.html)

[![Modeling Clutch Lock-Up Using If Blocks](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink_automotive/win64/ModelingClutchLockUpUsingIfBlocksExample_03.png)Modeling Clutch Lock-Up Using If BlocksUse If/Else subsystems to build a clutch model. An 'If' subsystem models the clutch dynamics in the locked position while an 'Else' subsystem models the unlocked position. One or the other is enabled using the 'If' block. The dot-dashed lines from the 'If' block denote control signals, which are used to enable If/Else (or other conditional) subsystems. Checking any of the boxes on the GUI produces a plot of any of the selected variables (versus time).](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/modeling-clutch-lock-up-using-if-blocks.html) -->


## 参数

<div class="details-box">
<details open>
<summary>恢复执行时的状态 — 选择内部状态的处理<div>“保持” （默认）</div></summary>
</details>
<div class="details-content">

选择当重新启用包含 ActionPort 模块的子系统时如何处理内部状态。

当子系统重新启用时，保留该子系统的以前状态值。各调用之间的以前状态值会保留，即使调用连接到 If 或 SwitchCase 模块的其他子系统模块也是如此。

</div>
</div>




<!-- - “重置”

  当子系统重新启用时，重新初始化状态值。如果子系统的动作端口的逻辑表达式之前的计算结果为 false，然后计算结果变为 true，则该子系统会重新启用。在下面的示例中，A 和 B 两个执行子系统的 Action Port 模块的**恢复执行时的状态**参数都设置为“重置”。![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/action_port_reset.png)当 **case[1]** 为 true 时，执行子系统 **A**。当 **case [1]** 保持为 true 时，重复调用子系统 **A** 不会重置其状态值。相同的行为也适用于子系统 **B**。 -->

<!-- #### 编程用法

**模块参数**：InitializeStates

| **类型**：字符向量           |
| ---------------------------- |
| **值**：'held' | 'reset' |
| **默认值**：'held'         | -->



<!-- ### 传播可变大小信号的大小 — 选择何时传播可变大小信号 “仅当恢复执行时” （默认） | “执行期间”



选择何时传播可变大小信号。

- “仅当恢复执行时”

  仅当重新启用包含 Action Port 模块的子系统时，才传播可变大小信号。

- “执行期间”

  在每个时间步传播可变大小的信号。

#### 编程用法

**模块参数**：PropagateVarSize

| **类型**：字符向量                                           |
| ------------------------------------------------------------ |
| **值**：'Only when execution is resumed' | 'During execution' |
| **默认值**：'Only when execution is resumed'               | -->



<!-- ## 扩展功能



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 Verilog 代码和 VHDL 代码。



HDL Coder™ 提供影响 HDL 实现和综合逻辑的额外配置选项。

**HDL 架构**

此模块具有一个默认 HDL 架构。 -->

## 版本历史记录

- 在 2024b 之前推出

### 限制信息

1. 暂不支持将恢复执行时的状态设定为重置；  
2. 暂不支持传播可变大小信号的功能。



## 另请参阅

[If](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SubSystems/If.html) | [IfActionSubsystem](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SubSystems/If.html#jump1) | [SwitchCase](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SubSystems/SwitchCase.html) | [SwitchCaseActionSubsystem](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SubSystems/SwitchCase.html#jump1)

<!-- ### 主题

- [选择子系统执行](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/select-subsystem-execution.html) -->