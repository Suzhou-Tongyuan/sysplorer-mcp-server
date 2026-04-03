# SwitchCase
---
使用类似于 switch 语句的逻辑选择子系统执行

**库：** Sysblock模块库 / SubSystems

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SubSystems/SwitchCase/SwitchCase.png')" style="width: 200px; height: auto; transform: scale(1);">

## 描述

SwitchCase 模块以及包含 ActionPort 模块的 SwitchCase ActionSubsystem 模块，实现 switch 逻辑来控制子系统的执行。

SwitchCase 模块具有单个输入。要选择一个 case，请使用 **Case 条件**参数定义输入值。计算顺序为从第一种情况开始由上往下进行。

每个 case 都与一个连接到 SwitchCaseActionSubsystem 模块的输出端口相关联。当选择一个 case 时，相关联的输出端口发送动作信号来执行子系统。

在所有其他 case 条件的计算结果都为 false 时，会选择 defaultcase。提供 defaultcase 是可选的，即使其他 case 条件没有用完每个可能的输入值也是如此。

<!-- Switch Case 模块的 case 在 Switch Case Action Subsystem 模块执行后包含一个隐含的中断。因此，Simulink® Switch Case 模块没有标准 C 语言的 switch 语句中存在的 fall-through（落空）行为。 -->

### SwitchCaseActionSubsystem<a id="jump1" class="jump-target"></a>

SwitchCaseActionSubsystem 模块是经过预先配置的 Subsystem 模块，您可基于它创建由 SwitchCase 模块控制执行的子系统。SwitchCase 模块的输入端口选择使用 case 条件参数定义的 case。根据输入值和选择的 case，该模块发送动作信号，以执行 SwitchCaseActionSubsystem 模块。子系统的执行由放置在子系统内部的 ActionPort 模块控制。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SubSystems/SwitchCase/SwitchCaseAS.png')" style="width: 400px; height: auto; transform: scale(0.8);">

## 示例<div id="SwitchCase2" class="jump-target"></div>

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SubSystems/SwitchCase.mo">SwitchCase.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SubSystems/SwitchCase/SwitchCase_ex.png')" style="width: 800px; height: auto; transform: scale(0.8);">


### 示例说明

- Step 模块：提供从 0 变到 1 的输入信号，用于模拟实际输入值的变化。这个信号将被用作 SwitchCase 模块的条件判断依据；
- SwitchCase 模块：计算逻辑表达式，并根据结果输出动作信号。如果满足 case，则输出一个动作信号，触发连接的 Subsystem 模块执行。如果不满足，触发连接的 SubSystem1 模块执行。可以在工具栏仿真结果中查看；
- SwitchCaseActionSubsystem 模块：一个预配置的子系统模块，其执行由 SwitchCase 模块控制。当接收到来自 SwitchCase 模块的动作信号时，SwitchCaseActionSubsystem 模块将执行其内部逻辑。


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u (logicaloperator) — case 选择的值<div> 标量</div></summary>
</details>
<div class="details-content">

对于 SwitchCase 模块上标签为 **u** 的端口，输入可以是：

- 具有 Sysblock 支持的内置数据类型的标量值。然而，SwitchCase 模块不支持布尔或定点数据类型，它将数值输入截断为 32 位有符号整数；
- 任何枚举数据类型的标量值。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | enum


</div>
</div>



### 输出


<div class="details-box">
<details open>
<summary>y — 用于 SwitchCaseActionSubsystem 模块的动作信号<div>标量</div></summary>
</details>
<div class="details-content">

来自 **y1** 和 **y2** 端口的输出是连接到 SwitchCaseActionSubsystem 模块的动作信号。

</div>
</div>



## 参数


<div class="details-box">
<details open>
<summary>Case 条件 — 指定 case 值<div>{1} （默认） | case 列表</div></summary>
</details>
<div class="details-content">

使用 MLang 元胞表示法指定 case 值。

- {1}

  指定当输入端口值为 1 时标签为 case[1] 的输出端口输出动作信号。

- 具有 case 分配的端口列表

  使用 MLang 元胞表示法指定多个 case 和端口。例如，输入 {1,[7,9,4]} 将指定当输入值为 1 时，运行输出端口 case[1]；当输入值为 7、9 或 4 时，运行输出端口 case [7 9 4]。可使用冒号表示法指定某一整数范围内的情况条件。例如，输入 {[1:5]} 将指定当输入值为 1、2、3、4 或 5 时，运行输出端口 **case[1 2 3 4 5]**。根据模块大小，对于较长的 case 条件列表，其中的 case 可能在 Switch Case 模块上以终止省略号 (...) 缩略显示。可使用一个枚举类型的名称指定一个情况条件，其中包含对应于该枚举类型中每个值的情况。

</div>
</div>




<!-- #### 编程用法

| **模块参数**：CaseConditions        |
| ------------------------------------- |
| **类型**：字符向量                    |
| **值**：'{1}' | '<list of cases>' |
| **默认值**：'{1}'                   | -->



<div class="details-box">
<details open>
<summary>显示默认 case — 控制默认输出端口的显示<div>on （默认） | off</div></summary>
</details>
<div class="details-content">

控制默认输出端口的显示。

- on

  将默认输出端口显示为 SwitchCase 模块的最后一个 case。您可由此指定默认 case，以在输入值与任何其他 case 值都不匹配时执行。

- off

  隐藏默认输出端口。

</div>
</div>




<!-- #### 编程用法

| **模块参数**：ShowDefaultCase |
| ------------------------------- |
| **类型**：字符向量              |
| **值**：'on' | 'off'        |
| **默认值**：'on'              | -->



<!-- ### 启用过零检测 — 控制过零检测 on （默认） | off



控制过零检测。

- on

  检测过零点。

- off

  不检测过零点。

#### 编程用法

| **模块参数**：ZeroCross |
| ------------------------- |
| **类型：**字符向量        |
| **值：** 'on' | 'off' |
| **默认值：**'on'        | -->



<!-- ## 模块特性

| **数据类型**     | double | enumerated | integer | single |
| ---------------- | ---------------------------------------------- |
| **直接馈通**     | 是                                           |
| **多维信号**     | 否                                           |
| **可变大小信号** | 否                                           |
| **过零检测**     | 是                                           | -->

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

暂不支持启用过零检测的功能据。

## 另请参阅

[Subsystem](Subsystem.html) | [ActionPort](ActionPort.html)

 <!-- | [Switch Case Action Subsystem](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/switchcaseactionsubsystem.html) -->

<!-- ### 主题

- [选择子系统执行](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/select-subsystem-execution.html) -->