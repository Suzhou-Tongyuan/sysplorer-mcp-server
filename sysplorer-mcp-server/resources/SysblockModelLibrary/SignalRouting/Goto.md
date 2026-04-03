# Goto
---
将模块输入传递给 From 模块


**库：** Sysblock模块库 / SignalRouting

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/Goto/Goto.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

Goto 模块将其输入传递给其对应的 From 模块。输入可以是任何数据类型的实数值或复数值信号或向量。From 和 Goto 模块允许您将信号从一个模块传递给另一个模块，而无需实际连接它们。

一个 Goto 模块可将其输入信号传递到多个 From 模块，尽管一个 From 模块只能接收来自一个 Goto 模块的信号。Goto 模块的输入传递到与它关联的 From 模块，就像两个模块进行了物理连接一样。

例如，此模型使用 Goto 模块和 From 模块。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/From/From02.png')" style="width: 510px; height: auto; transform: scale(1);">

等效模型将 Sine Wave 模块信号直接传递给 Gain 模块。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/From/From03.png')" style="width: 320px; height: auto; transform: scale(1);">

Goto 模块和 From 模块通过使用 Goto 标记进行匹配。

**标签可见性**参数确定 From 模块可以访问信号的位置。

Goto 模块支持信号标签传播。

<!-- 有关详细信息，请参阅[信号标签传播]()。 -->

## 示例

<!-- [![Signal Routing with the From, Goto, and Goto Tag Visibility Blocks](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink/win64/FromGotoAndGotoTagVisibilityBlockExample_04.png)Signal Routing with the From, Goto, and Goto Tag Visibility BlocksUse the From, Goto, and Goto Tag Visibility blocks to route signals in your model.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/signal-routing-with-from-goto-and-gototag-visibility-blocks.html)

[![Building a Clutch Lock-Up Model](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink_automotive/win64/BuildingAClutchLockUpModelExample_07.png)Building a Clutch Lock-Up ModelUse Simulink® to model and simulate a rotating clutch system. Although modeling a clutch system is difficult because of topological changes in the system dynamics during lockup, this example shows how Simulink's enabled subsystems easily handle such problems. We illustrate how to employ important Simulink modeling concepts in the creation of the clutch simulation. Designers can apply these concepts to many models with strong discontinuities and constraints that may change dynamically.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/building-a-clutch-lock-up-model.html) -->

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/Goto.mo">Goto.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/Goto/Goto_ex.png')" style="width: 600px;transform: scale(0.8);">

### 示例说明

- From 模块：用指定的标签从 Goto 模块接收信号；
- Goto 模块：向具有指定标签的 From 模块发送信号；
- GotoTagVisibility 模块：与 Goto 和 From 模块结合使用，以定义限定作用域标签的可见性。在这个示例中，它使用从 Goto 模块接收的值来控制指定标签元素的可见性。


## 端口

### 输入


<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 向量 | 矩阵 | N 维数组</div></summary>
</details>
<div class="details-content">

要传递给对应的 From 模块的输入信号，指定为标量、向量、矩阵或 N 维数组。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | fixedPoint | enum | bus

</div>
</div>



## 参数


<div class="details-box">
<details open>
<summary>Goto 标签 — 模块标识符<div>“空” （默认） | ...</div></summary>
</details>
<div class="details-content">

Goto 模块标识符。此参数标识定义了作用域的 Goto 模块。

</div>
</div>




<!-- #### 编程用法

| **模块参数**：GotoTag |
| ----------------------- |
| **类型：**字符向量      |
| **值：**'A' | ...   |
| **默认值：**'A'       | -->


<div class="details-box">
<details open>
<summary>标签可见性 — Goto 模块标记的作用域<div>“全局” （默认） | “本地” | “限定作用域”</div></summary>
</details>
<div class="details-content">

Goto 模块标记的作用域，指定为“全局”、“本地”或“限定作用域”或。当您将此参数设置为“限定作用域”时，您必须使用 [GotoTagVisibility](GotoTagVisibility.md) 模块来定义标记可见性的作用域。

- “全局”（默认值） - 使用同一个标记的 From 和 Goto 模块可以在模型中的任意位置，但超出非虚拟子系统边界的位置除外；

- “本地”- 使用同一个标记的 From 和 Goto 模块必须在同一个子系统中。局部标记名称用方括号 ([]) 括起；

- “限定作用域” - 使用相同标记的 From 和 Goto 模块必须符合以下条件：

  - 在同一子系统中；
  - 在模型层次结构中位于 GotoTagVisibility 模块之下的任何级别且不会超出非虚拟子系统边界。换句话说，它们必须在原子子系统、条件执行子系统或函数调用子系统或模型引用的边界内。

  范围标记名称用花括号 ({}) 括起。


From-Goto 模块连接不能穿过非虚拟子系统边界的规则存在以下例外情况。与一个条件执行子系统的状态端口连接的 Goto 模块，对另一个条件执行子系统中的 From 模块是可见的。

</div>
</div>








<!-- **注意**

封装系统中的“限定作用域” Goto 模块仅在该子系统以及它包含的非虚拟子系统中是可见的。如果您运行或更新模块图，而有一个 Goto Tag Visibility 模块在模块图中的级别高于封装子系统中对应的“限定作用域”Goto 模块，Simulink® 将生成错误。

当使用相同标记名称的 Goto 和 From 模块在同一个子系统中时，请使用 local 标记。当使用相同标记名称的 Goto 和 From 模块在不同的子系统中时，您必须使用 global 或 scoped 标记。如果您将某个标记定义为 global，则所有使用该标记的模块都访问同一个信号。定义为 scoped 的标记可在模型中的多个位置使用。 -->

<!-- #### 编程用法

| **模块参数**：TagVisibility           |
| --------------------------------------- |
| **类型：**字符向量                      |
| **值：**'local' | 'scoped' | 'global' |
| **默认值：**'local'                   | -->



<!-- ### 图标显示 — 要在模块图标上显示的文本 “标记” （默认） | “信号名称” | “标记和信号名称”





指定要在模块图标上显示的文本。选项包括模块标记、模块所代表的信号的名称，或者同时包含标记和信号名称。

#### 编程用法

| **模块参数**：IconDisplay                             |
| ------------------------------------------------------- |
| **类型：**字符向量                                      |
| **值：**'Signal name' | 'Tag' | 'Tag and signal name' |
| **默认值：**'Tag'                                     | -->


<div class="details-box">
<details open>
<summary>全部重命名 — 在整个模型中传播名称<div>按钮</div></summary>
</details>
<div class="details-content">

重命名 Goto 标记。新名称会传播给**对应的模块**框中列出的所有 From 和 GotoTagVisibility 模块。

或者，当您更改 Goto 模块图标上的标记时，通过按 **Shift+Enter** 键将新名称传播到所有对应的 From 和 GotoTagVisibility 模块。

</div>
</div>





<div class="details-box">
<details open>
<summary>对应的模块 — 连接到此 Goto 模块的模块<div>模块路径 | ...</div></summary>
</details>
<div class="details-content">

与此 Goto 模块连接的 From 模块和 GotoTagVisibility 模块的列表。单击列表中的某个项目，以显示并突出显示对应的 From 和 GotoTagVisibility 模块。

或者，在 Sysblck 编辑器中，选择 Goto 模块以突出显示对应的 From 和 GotoTagVisibility 模块。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/Goto/Goto01.png')" style="width: 300px; height: auto; transform: scale(1);">

当对应的 From 或 GotoTagVisibility 模块不在当前图中时，包含该模块的 Subsystem 模块会突出显示。

</div>
</div>




<!-- 要在打开的图或新选项卡中显示对应的模块，请选择 Goto 模块并在省略号上暂停。然后，从操作栏中选择**相关模块** ![Related Blocks button](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/related-blocks-button.png)。当多个模块对应于所选模块时，将打开一个相关模块列表。您可以通过在文本框中输入搜索词来过滤相关模块列表。从列表中选择相关模块后，窗口焦点转至显示该相关模块的打开的图或新选项卡。 -->



<!-- ## 模块特性

| **数据类型**     | Boolean | bus | double | enumerated | fixed point | half | integer | single | string |
| ---------------- | ------------------------------------------------------------ |
| **直接馈通**     | 否                                                         |
| **多维信号**     | 是                                                         |
| **可变大小信号** | 是                                                         |
| **过零检测**     | 否                                                         | -->


## 版本历史记录

- 在 2024b 之前推出

### 限制信息

1. 暂不支持图标显示功能；  
2. 输入信号暂不支持 half、int64、uint64 和 image 的数据类型。

<!-- ## 扩展功能



### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 Verilog 代码和 VHDL 代码。



HDL Coder™ 提供影响 HDL 实现和综合逻辑的额外配置选项。HDL 代码生成不支持将模块的**标记可见性**设置为“全局”。另请参阅[Required HDL Settings for Goto and From Blocks](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/usage-of-delay-blocks-as-registers.html#mw_f4cd43eb-dea6-4782-ac17-c97cf8147d65) (HDL Coder)。

**HDL 架构**

此模块具有一个默认 HDL 架构。

**HDL 模块属性**

| **InputPipeline** | 要在生成的代码中插入的输入流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 0。有关详细信息，请参阅[InputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-25) (HDL Coder)。 |
| ----------------- | ------------------------------------------------------------ |
|                   |                                                              |



### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。

## 版本历史记录

**在 R2006a 之前推出** -->

## 另请参阅

[From](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SignalRouting/From.html) | [GotoTagVisibility](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SignalRouting/GotoTagVisibility.html)

<!-- ### 主题

- [信号标签传播](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/signal-label-propagation.html) -->