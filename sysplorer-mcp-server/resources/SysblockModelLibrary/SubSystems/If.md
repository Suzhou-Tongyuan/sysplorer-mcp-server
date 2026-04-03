# If
---
使用类似于 if-else 语句的逻辑选择子系统执行

**库：** Sysblock模块库 / SubSystems

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SubSystems/If/If.png')" style="width: 200px; height: auto; transform: scale(1);">

## 描述<a id="jump2"></a>

If 模块以及包含 [ActionPort](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SubSystems/ActionPort.html) 模块的 [IfActionSubsystem](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SubSystems/If.html#jump1) 模块实现 if-else 逻辑来控制子系统的执行。

### IfActionSubsystem<a id="jump1"></a>

If Action Subsystem 模块是经过预先配置的 [Subsystem](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SubSystems/Subsystem.html) 模块，可以作为一个起点，用来创建由 If 模块控制执行的子系统。If 模块计算逻辑表达式，然后根据计算结果输出动作信号。子系统的执行由放置在子系统内部的 [ActionPort](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SubSystems/ActionPort.html) 模块控制。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SubSystems/If/IfAS.png')" style="width: 400px; height: auto; transform: scale(0.8);">

<!-- 有关使用 If 模块的示例，请参阅[Select Subsystem Execution](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/select-subsystem-execution.html)。

![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/if_with_if_action_subsystem.png) -->

## 示例<a id="jump3"></a>

<!-- [![Simulink 子系统语义](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/simulinksubsystemsemanticsexample_01_zh_CN.png)Simulink 子系统语义这组示例说明不同类型的 Simulink® 子系统，以及对这些子系统进行仿真时使用的语义。每个示例都提供了对模型的说明以及控制模型执行方式的诀窍。](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/simulink-subsystem-semantics.html)

[![If-Then-Else 模块](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/ifthenelseblocksexample_01_zh_CN.png)If-Then-Else 模块此示例说明将正弦波馈入 If Action Subsystem 模块的效果。它旨在说明 If Action Subsystem 模块和 Enabled Subsystem 模块之间的相似性。](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/if-then-else-blocks.html)

[![Modeling Clutch Lock-Up Using If Blocks](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink_automotive/win64/ModelingClutchLockUpUsingIfBlocksExample_03.png)Modeling Clutch Lock-Up Using If BlocksUse If/Else subsystems to build a clutch model. An 'If' subsystem models the clutch dynamics in the locked position while an 'Else' subsystem models the unlocked position. One or the other is enabled using the 'If' block. The dot-dashed lines from the 'If' block denote control signals, which are used to enable If/Else (or other conditional) subsystems. Checking any of the boxes on the GUI produces a plot of any of the selected variables (versus time).](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/modeling-clutch-lock-up-using-if-blocks.html) -->

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SubSystems/If.mo">If.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SubSystems/If/If_ex.png')" style="width: 800px; height: auto; transform: scale(0.8);">

### 示例说明

- Step 模块：提供从 -1 变到 1 的输入信号，用于模拟实际输入值的变化。这个信号将被用作 If 模块的条件判断依据；
- If 模块：计算逻辑表达式，并根据结果输出动作信号。如果条件为真，则输出一个动作信号，触发连接的 Subsystem 模块执行。如果条件为假，触发连接的 SubSystem1 模块执行。可以在工具栏仿真结果中查看；
- IfActionSubsystem 模块：一个预配置的子系统模块，其执行由 If 模块控制。当接收到来自If模块的动作信号时，IfActionSubsystem 模块将执行其内部逻辑。

## 限制

If 模块具有以下限制：

- 它不支持可调参数。在普通模式或加速模式下的仿真过程中，或在运行生成的代码时，不能调整 if 或 elseif 表达式的值；

  要实现可调整的 if-else 表达式，请在 If 模块外部调整表达式。例如，使用 RelationalOperator 模块计算 If 模块外部的外部表达式或将可调参数作为输入添加到 If 模块。

- 它不支持自定义存储类；
  <!-- 请参阅[使用 Struct 存储类将参数数据组织为结构体](https://ww2.mathworks.cn/help/releases/R2022b/ecoder/ug/configure-parameters-for-code-generation.html#br0debj) (Embedded Coder)。 -->

- **If 表达式**和 **Elseif 表达式**不能接受某些运算符，如 +、-、* 和 /。

## 端口

### 输入

<div class="details-box">
<details open>
<summary>u1 — 用于计算逻辑表达式的值<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

输入 u1,u2,...,un 必须具有相同的数据类型。输入不能是任何用户定义的类型，例如枚举类型。

If 模块不直接支持定点数据类型。但是，可以使用 CompareToConstant 模块解决此限制。

<!-- 请参阅 [Select Subsystem Execution](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/select-subsystem-execution.html)中对定点数据类型的支持。 -->

If 模块不支持布尔数据类型。如果要将布尔信号输入到 If 模块，请使用 DataTypeConversion 模块将该信号转换为整数类型。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean

</div>
</div>


### 输出


<div class="details-box">
<details open>
<summary>y — 用于 IfActionSubsystem 模块的动作信号<div>标量</div></summary>
</details>
<div class="details-content">

来自 if、else 和 elseif 端口的输出是到 IfActionSubsystem 模块的动作信号。

</div>
</div>


## 参数


<div class="details-box">
<details open>
<summary>输入的数目 — 指定输入端口个数<div>1 （默认） | 整数</div></summary>
</details>
<div class="details-content">

- 1

  指定一个输入端口。

- 整数

  指定输入端口个数。模块端口的标签为 'u' 字符后跟数字 1,2,...,n，其中 n 等于您指定的输入的数量。

</div>
</div>



<!-- #### 编程用法

| **模块参数**：NumInputs     |
| ----------------------------- |
| **类型**：字符向量            |
| **值**：'1' | '<integer>' |
| **默认值**：'1'             | -->



<div class="details-box">
<details open>
<summary>If 表达式 — 指定逻辑表达式<div>u1 > 0 （默认） | 逻辑表达式</div></summary>
</details>
<div class="details-content">

连接到 if 端口的 IfActionSubsystem 会在其关联的表达式计算结果为 true 时执行。

- u1 > 0

  指定当输入 u1 大于 0 时在输出端口上发送动作信号。

- 逻辑表达式

  指定逻辑表达式。此表达式在 If 模块上与 **if** 输出端口相邻显示。该表达式只能包含运算符 <, <=, ==, ~=, >, >=, &, |, ~, (), unary-minus。不允许使用 +, -, *, / 和 ^ 等运算符。该表达式不能包含数据类型表达式（例如 int8(6)），并且不能引用数据类型不是 double 或 single 的工作区变量。

</div>
</div>




<!-- #### 编程用法

| **模块参数**：IfExpression                  |
| --------------------------------------------- |
| **类型**：字符向量                            |
| **值**：'u1 > 0' | '<logical expression>' |
| **默认值**：'u1 > 0'                        | -->


<div class="details-box">
<details open>
<summary>Elseif 表达式 — 指定逻辑表达式<div>空 （默认） | 逻辑表达式列表</div></summary>
</details>
<div class="details-content">

连接到 **elseif** 端口的 IfActionSubsystem 在其表达式计算结果为 true 且所有 if 和 elseif 表达式为 false 时执行。

- 空

  未指定逻辑表达式。

- 逻辑表达式列表

  指定由以逗号分隔的逻辑表达式列表。当您选中**显示 else 条件**复选框时，表达式出现在 If 模块上的 **if** 端口下方及 **else** 端口上方。表达式只能包含运算符 <, <=, ==, ~=, >, >=, &, |, ~, (), unary-minus。不允许使用 +, -, *, / 和 ^ 等运算符。表达式不能包含数据类型表达式（例如 int8(6)），并且不能引用数据类型不是 double 或 single 的工作区变量。

</div>
</div>




<!-- #### 编程用法

| **模块参数**：ElseIfExpressions                |
| ------------------------------------------------ |
| **类型**：字符向量                               |
| **值**：'' | '<list of logical expressions>' |
| **默认值**：''                                 | -->


<div class="details-box">
<details open>
<summary>显示 else 条件 — 控制 else 端口的显示<div>on （默认） | off</div></summary>
</details>
<div class="details-content">

当 **if** 端口和所有 **elseif** 端口表达式为 false 时，**else** 端口发送动作信号来执行所连接的 IfActionSubsystem 模块。

- on

  显示 **else** 端口。

- off

  隐藏 **else** 端口。

</div>
</div>




<!-- #### 编程用法

| **模块参数**：ShowElse  |
| ------------------------- |
| **类型：**字符向量        |
| **值：** 'on' | 'off' |
| **默认值：**'on'        | -->



<!-- ### 启用过零检测 — 控制过零检测 on （默认） | off



控制过零检测。

- ![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/on_check_box.gif) on

  检测过零点。

- ![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/off_check_box.gif) off

  不检测过零点。

#### 编程用法

| **模块参数**：ZeroCross |
| ------------------------- |
| **类型：**字符向量        |
| **值：** 'on' | 'off' |
| **默认值：**'on'        | -->



<!-- ## 模块特性

| **数据类型**     | Boolean | double | integer | single |
| ---------------- | ------------------------------------------- |
| **直接馈通**     | 是                                        |
| **多维信号**     | 否                                        |
| **可变大小信号** | 否                                        |
| **过零检测**     | 是                                        | -->

<!-- ## 扩展功能



### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 Verilog 代码和 VHDL 代码。

HDL Coder™ 提供影响 HDL 实现和综合逻辑的额外配置选项。



**HDL 架构**

此模块具有一个默认 HDL 架构。

**HDL 模块属性**

| **ConstrainedOutputPipeline** | 通过移动设计中现有延迟的方式来放置在输出端的寄存器的数量。分布式流水线处理不会重新分发这些寄存器。默认值为 0。有关详细信息，请参阅[ConstrainedOutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#btp8gmp) (HDL Coder)。 |
| ----------------------------- | ------------------------------------------------------------ |
| **InputPipeline**             | 要在生成的代码中插入的输入流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 0。有关详细信息，请参阅[InputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-25) (HDL Coder)。 |
| **OutputPipeline**            | 要在生成的代码中插入的输出流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 0。有关详细信息，请参阅[OutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-26) (HDL Coder)。 | -->

## 版本历史记录

- 在 2024b 之前推出

### 限制信息

暂不支持启用过零检测的功能。

## 另请参阅

[Subsystem](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SubSystems/Subsystem.html) | [ActionPort](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SubSystems/ActionPort.html)

 <!-- | [If Action Subsystem](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/ifactionsubsystem.html) -->

<!-- ### 主题

- [选择子系统执行](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/select-subsystem-execution.html) -->