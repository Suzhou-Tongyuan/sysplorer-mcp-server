# GotoTagVisibility
---
定义 Goto 模块标记的作用域

**库：** Sysblock模块库 / SignalRouting

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/GotoTagVisibility/GotoTagVisibility.png')" style="width: 100px; height: auto; transform: scale(1);">


## 描述

GotoTagVisibility 模块定义具有 scoped 可见性的 Goto 模块标记的可访问性。您为 **Goto 标记**模块参数指定的值可由模型层次结构中包含 GotoTagVisibility 模块的同一子系统中及其下层的子系统中的 From 模块进行访问。

对于**标签可见性**参数值为 scoped 的 Goto 模块，GotoTagVisibility 模块是必需的。如果标记可见性为 local 或 global，则不需要 GotoTagVisibility 模块。模块显示的标记名称括在花括号 ({}) 内。

::: warning 注意 
封装系统中的“限定作用域” Goto 模块仅在该子系统以及它包含的非虚拟子系统中是可见的。如果您运行或更新模块图，而有一个 GotoTagVisibility 模块在模块图中的级别低于封装子系统中对应的“限定作用域” Goto 模块，Sysblock 将生成错误。
:::



在 Sysblock 编辑器中，选择 GotoTagVisibility 模块以突出显示对应的 Goto 和 From 模块。当对应的 From 或 Goto 模块不在当前图中时，包含该模块的 Subsystem 模块会突出显示。

<!-- 要在打开的图或新选项卡中显示对应的模块，请选择 Goto Tag Visibility 模块并在省略号上暂停。然后，从操作栏中选择**相关模块** ![Related Blocks button](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/related-blocks-button.png)。当多个模块对应于所选模块时，将打开一个相关模块列表。您可以通过在文本框中输入搜索词来过滤相关模块列表。从列表中选择相关模块后，窗口焦点转至显示该相关模块的打开的图或新选项卡。 -->

## 示例

<!-- [![Signal Routing with the From, Goto, and Goto Tag Visibility Blocks](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink/win64/FromGotoAndGotoTagVisibilityBlockExample_04.png)Signal Routing with the From, Goto, and Goto Tag Visibility BlocksUse the From, Goto, and Goto Tag Visibility blocks to route signals in your model.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/signal-routing-with-from-goto-and-gototag-visibility-blocks.html) -->

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/GotoTagVisibility.mo">GotoTagVisibility.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/GotoTagVisibility/GotoTagVisibility_ex.png')" style="width: 600px; transform: scale(0.8);">

### 示例说明

- From 模块：用指定的标签从 Goto 模块接收信号；
- Goto 模块：向具有指定标签的 From 模块发送信号；
- GotoTagVisibility 模块：与 Goto 和 From 模块结合使用，以定义限定作用域标签的可见性。在这个示例中，它使用从 Goto 模块接收的值来控制指定标签元素的可见性。

## 参数

<div class="details-box">
<details open>
<summary>Goto 标签 — 其可见性由此模块的位置定义的 Goto 模块标记<div>空 （默认） | ...</div></summary>
</details>
<div class="details-content">

其可见性由此模块的位置定义的 Goto 模块标记。使用指定的标记的 From 和 Goto 模块必须在同一个子系统中，或者位于模型层次结构中 GotoTagVisibility 模块之下且不超出非虚拟子系统边界（换言之，原子子系统、条件执行子系统、函数调用子系统或模型引用的边界）的任何级别。范围标记名称用花括号 ( {} ) 括起。



::: tip 提示 
如果您使用多个 From 和 GotoTagVisibility 模块引用同一 Goto 标记，您可以同时在所有这些模块中重命名该标记。使用 [Goto](Goto.html) 模块对话框中的**全部重命名**按钮。或者，当您更改 [Goto](Goto.html) 模块图标上的标记时，通过按 **Shift+Enter** 键将新名称传播到所有对应的 From 和 GotoTagVisibility 模块。
:::

</div>
</div>








<!-- ## 模块特性

| **数据类型**     | Boolean | bus | double | enumerated | fixed point | integer | single |
| ---------------- | ------------------------------------------------------------ |
| **直接馈通**     | 否                                                         |
| **多维信号**     | 否                                                         |
| **可变大小信号** | 否                                                         |
| **过零检测**     | 否                                                         | -->





<!-- ## 扩展功能



### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 Verilog 代码和 VHDL 代码。



HDL Coder™ 提供影响 HDL 实现和综合逻辑的额外配置选项。

**HDL 架构**

此模块具有一个默认 HDL 架构。



### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。

## 版本历史记录

**在 R2006a 之前推出** -->

## 版本历史记录

- 在 2024b 之前推出

## 另请参阅

[Goto](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SignalRouting/Goto.html) | [From](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SignalRouting/From.html)

<!-- ### 主题

- [信号标签传播](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/signal-label-propagation.html) -->