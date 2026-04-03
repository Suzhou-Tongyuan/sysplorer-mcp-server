# From
---
接受来自 Goto 模块的输入

**库：** Sysblock模块库 / SignalRouting

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/From/From.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

From 模块从对应的 Goto 模块接受信号，然后将其作为输出传递出去。输出的数据类型与来自 Goto 模块的输入的数据类型相同。From 和 Goto 模块允许您将信号从一个模块传递到另一个模块，而无需实际连接它们。

例如，此模型使用 Goto 模块和 From 模块。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/From/From02.png')" style="width: 510px; height: auto; transform: scale(1);">

等效模型将 SineWave 模块信号直接传递给 Gain 模块。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/From/From03.png')" style="width: 320px; height: auto; transform: scale(1);">

一个 From 模块只能接收来自一个 Goto 模块的信号，尽管 Goto 模块可以将其信号传递给多个 From 模块。

要将 Goto 模块与 From 模块关联，请在 **Goto 标记**参数中输入 Goto 模块标记。

Goto 模块标记的可见性决定了哪些 From 模块能够接收其信号。有关详细信息，请参阅 [Goto](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SignalRouting/Goto.html) 和 [GotoTagVisibility](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SignalRouting/GotoTagVisibility.html)。模块通过以下方式指明 Goto 模块标记的可见性：

- 局部标记名称用方括号 ( [] ) 括起；
- 范围标记名称用花括号 ( {} ) 括起；
- global 标记名称不带其他任何字符。

From 模块支持信号标签传播。

<!-- 有关详细信息，请参阅[信号标签传播]()。 -->

## 示例

<!-- [![Signal Routing with the From, Goto, and Goto Tag Visibility Blocks](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink/win64/FromGotoAndGotoTagVisibilityBlockExample_04.png)Signal Routing with the From, Goto, and Goto Tag Visibility BlocksUse the From, Goto, and Goto Tag Visibility blocks to route signals in your model.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/signal-routing-with-from-goto-and-gototag-visibility-blocks.html)

[![自动气候控制系统仿真](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/simulatingautomaticclimatecontrolsystemsexample_01_zh_CN.png)自动气候控制系统仿真此示例说明如何使用 Simulink® 和 Stateflow® 对汽车中自动气候控制系统进行仿真。](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/simulating-automatic-climate-control-systems.html)

[![带紧急刹车的摩擦模型](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/sldemo_hardstopexample_02_zh_CN.png)带紧急刹车的摩擦模型此示例介绍了一种在 Simulink® 中对摩擦建模的方式。模型中的两个积分器用于计算系统的速度和位置，然后将计算结果用于在 Friction Model 中计算摩擦力。](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/friction-model-with-hard-stops.html)

[![Building a Clutch Lock-Up Model](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink_automotive/win64/BuildingAClutchLockUpModelExample_07.png)Building a Clutch Lock-Up ModelUse Simulink® to model and simulate a rotating clutch system. Although modeling a clutch system is difficult because of topological changes in the system dynamics during lockup, this example shows how Simulink's enabled subsystems easily handle such problems. We illustrate how to employ important Simulink modeling concepts in the creation of the clutch simulation. Designers can apply these concepts to many models with strong discontinuities and constraints that may change dynamically.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/building-a-clutch-lock-up-model.html) -->

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/From.mo">From.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/From/From_ex.png')" style="width: 600px;transform: scale(0.8);">

### 示例说明

- From 模块：用指定的标签从 Goto 模块接收信号；
- Goto 模块：向具有指定标签的 From 模块发送信号；
- GotoTagVisibility 模块：与 Goto 和 From 模块结合使用，以定义限定作用域标签的可见性。在这个示例中，它使用从 Goto 模块接收的值来控制指定标签元素的可见性。


## 端口

### 输出


<div class="details-box">
<details open>
<summary>y — 来自连接的 Goto 模块的信号<div>标量 | 向量 | 矩阵 | N 维数组</div></summary>
</details>
<div class="details-content">

来自连接的 Goto 模块的信号，输出信号的维度和数据类型与 Goto 模块的输入信号的维度和数据类型相同。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | fixedPoint | enum | bus

</div>
</div>



## 参数

<div class="details-box">
<details open>
<summary>关联标签 — 将信号转发给此模块的 Goto 模块的标记<div>空 （默认） | ...</div></summary>
</details>
<div class="details-content">

指定将信号转发给此 From 模块的 Goto 模块的标记。要更改该标记，请从下拉列表中选择新标记。

下拉列表显示 From 模块当前可以看到的 Goto 标记。
<!-- 当您第一次在 Simulink® 会话中显示此列表时，列表的末尾会出现一个标签为 <More Tags...> 的列表项。如果您选择此列表项，模块将更新标记列表，以包括库子系统（由包含此 From 模块的模型引用）中的 Goto 模块的标记。Simulink 软件会在生成库标记列表时显示一个进度条。Simulink 会一直保存更新的标记列表直到该 Simulink 会话结束，或者直到您再次选择旁边的**更新标记**按钮为止。仅在您上次更新标记列表后模型所引用的库又发生变化的情况下，才需要再次更新当前会话中的标记列表。 -->


::: tip 提示 
如果您使用多个 From 和 GotoTagVisibility 模块引用同一 Goto 标记，您可以同时在所有这些模块中重命名该标记。为此，请使用 Goto 模块对话框中的**全部重命名**按钮。或者，当您更改 [Goto](Goto.html) 模块图标上的标记时，通过按 **Shift+Enter** 键将新名称传播到所有对应的 From 和 GotoTagVisibility 模块。

要找到相关 Goto 模块，请使用 From 模块对话框中的 **Goto 源**超链接。
:::

</div>
</div>





<!-- #### 编程用法

| **模块参数**：GotoTag |
| ----------------------- |
| **类型：**字符向量      |
| **值：**'A' | ...   |
| **默认值：**'A'       | -->



<!-- ### 更新标记 — 更新可见标记的列表 



更新对此 From 模块可见的标记列表，包括包含此 From 模块的模型所引用的库中存在的标记。仅在您上次更新标记列表后模型所引用的库又发生变化的情况下，再次更新当前会话中的标记列表。 -->


<div class="details-box">
<details open>
<summary>Goto 源 — 所连接的 Goto 模块的路径<div>模块路径</div></summary>
</details>
<div class="details-content">

连接到此 From 模块的 Goto 模块的路径。单击该路径将在模型中显示并突出显示 Goto 模块。

在 Sysblock 编辑器中，选择 From 模块会突出显示对应的 Goto 和 GotoTagVisibility 模块。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/From/From01.png')" style="width: 300px; height: auto; transform: scale(1);">

当对应的 Goto 或 GotoTagVisibility 模块不在当前图中时，包含该模块的 Subsystem 模块会突出显示。

</div>
</div>




<!-- 要在打开的图或新选项卡中显示对应的模块，请选择 From 模块并在省略号上暂停。然后，从操作栏中选择**相关模块** ![Related Blocks button](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/related-blocks-button.png)。当多个模块对应于所选模块时，将打开一个相关模块列表。您可以通过在文本框中输入搜索词来过滤相关模块列表。从列表中选择相关模块后，窗口焦点转至显示该相关模块的打开的图或新选项卡。 -->



<!-- ### 图标显示 — 要在模块图标上显示的文本 “标记” | “标记和信号名称” | “信号名称”



指定要在 From 模块图标上显示的文本。选项包括模块标记、模块所代表的信号的名称，或者同时包含标记和信号名称。

#### 编程用法

| **模块参数**：IconDisplay                             |
| ------------------------------------------------------- |
| **类型：**字符向量                                      |
| **值：**'Signal name' | 'Tag' | 'Tag and signal name' |
| **默认值：**'Tag'                                     | -->



<!-- ## 模块特性

| **数据类型**     | Boolean | bus | double | enumerated | fixed point | half | integer | single | string |
| ---------------- | ------------------------------------------------------------ |
| **直接馈通**     | 否                                                         |
| **多维信号**     | 是                                                         |
| **可变大小信号** | 是                                                         |
| **过零检测**     | 否                                                         |

## 详细信息



### 搜索 Goto 标记

要在打开 From 模块对话框时在模型引用的库中搜索 Goto 标记，请使用 FollowLinksWhenOpeningFromGotoBlocks 模型参数和 [set_param](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/set_param.html) 函数。

- 'off' - 不搜索 Goto 标记（默认值）。
- 'on' - 搜索 Goto 标记。 -->


## 版本历史记录

- 在 2024b 之前推出

### 限制信息

1. 暂不支持更新标记功能；  
2. 暂不支持图标显示功能；  
3. 暂不支持搜索 Goto 标记；  
4. 输出信号暂不支持 half、int64、uint64 和 image 的数据类型。

<!-- ## 扩展功能



### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 Verilog 代码和 VHDL 代码。



HDL Coder™ 提供影响 HDL 实现和综合逻辑的额外配置选项。另请参阅[Required HDL Settings for Goto and From Blocks](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/usage-of-delay-blocks-as-registers.html#mw_f4cd43eb-dea6-4782-ac17-c97cf8147d65) (HDL Coder)。

**HDL 架构**

此模块具有一个默认 HDL 架构。

**HDL 模块属性**

| **ConstrainedOutputPipeline** | 通过移动设计中现有延迟的方式来放置在输出端的寄存器的数量。分布式流水线处理不会重新分发这些寄存器。默认值为 0。有关详细信息，请参阅[ConstrainedOutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#btp8gmp) (HDL Coder)。 |
| ----------------------------- | ------------------------------------------------------------ |
| **OutputPipeline**            | 要在生成的代码中插入的输出流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 0。有关详细信息，请参阅[OutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-26) (HDL Coder)。 |



### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。

## 版本历史记录

**在 R2006a 之前推出** -->

## 另请参阅

[Goto](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SignalRouting/Goto.html) | [GotoTagVisibility](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SignalRouting/GotoTagVisibility.html)

<!-- ### 主题

- [信号标签传播](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/signal-label-propagation.html) -->