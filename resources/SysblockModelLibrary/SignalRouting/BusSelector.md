# BusSelector
---
从输入总线中选择元素

**库：** Sysblock模块库 / SignalRouting

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/BusSelector/BusSelector.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

BusSelector 模块从输入总线层次结构中按名称提取您选择的元素。该模块可以分别输出选定的各个元素或在一个新的虚拟总线中输出所有选定元素。当模块分别输出选定元素时，每个选定元素对应于一个输出端口。当模块输出新的虚拟总线时，对于包含所有选定元素的虚拟总线，该模块具有一个与之对应的输出端口。

虽然多个元素在总线层次结构中的不同位置可以具有相同的名称，但每个元素都有唯一的完全限定名称供 BusSelector 模块使用。例如，顶层总线和一个嵌套总线都可以有名为 chirp 的元素。顶层总线中该元素的完全限定名称为 chirp。嵌套总线中该元素的完全限定名称为 nestedbus.chirp，其中 nestedbus 是嵌套总线的名称。

## 示例

<!-- [![Simplify Bus Interfaces in Subsystems and Models](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink/win64/xxBusInterfaceConversionFinal.png)Simplify Bus Interfaces in Subsystems and Models](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/simplify-subsystem-bus-interfaces.html#bvmdxtx)

[![了解 Simulink 总线功能](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/simulinkbussignalsexample_01_zh_CN.png)了解 Simulink 总线功能在组件中使用总线，在组件接口上使用总线端口，并更快地执行常见总线工作流。](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/simulink-bus-signals.html) -->

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/BusSelector.mo">BusSelector.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/BusSelector/BusSelector_ex.png')" style="width: 600px; transform: scale(0.8);">

### 示例说明

- Constant 模块：提供固定的数值作为输入信号；
- BusCreator 模块：将多个输入信号合并为一个总线信号。这个模块可以处理不同类型的元素，包括信号、其他总线，甚至是消息；
- BusSelector 模块：从总线信号中提取特定的信号，以便进一步处理或观察。在这个示例中，我们从总线中提取了名为 signal1 和 signal2 的信号；
- Scope 模块：用于显示模型的输出结果，即从总线中提取的特定信号。

## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入虚拟或非虚拟总线<div>总线</div></summary>
</details>
<div class="details-content">

输入虚拟或非虚拟总线包含要选择的元素。

对于总线数组，请使用 [Selector](Selector.html) 模块来选择要与 BusSelector 模块结合使用的总线。

**数据类型：**  bus

</div>
</div>




### 输出

<div class="details-box">
<details open>
<summary>y1 — 输入总线的所选元素<div>标量 | 向量 | 矩阵 | 数组 | 总线</div></summary>
</details>
<div class="details-content">

默认情况下，模块将每个所选元素从一个单独的输出端口输出，该端口上标有对应总线元素的名称。当**输出为虚拟总线**参数启用时，模块从一个端口输出所选元素，并在一个虚拟总线中组合这些元素。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | fixedPoint | enum | bus

</div>
</div>





<div class="details-box">
<details open>
<summary>y2 — 输入总线的所选元素<div>标量 | 向量 | 矩阵 | 数组 | 总线</div></summary>
</details>
<div class="details-content">

默认情况下，模块将每个所选元素从一个单独的输出端口输出，该端口上标有对应总线元素的名称。当**输出为虚拟总线**参数启用时，模块从一个端口输出所选元素，并在一个虚拟总线中组合这些元素。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | fixedPoint | enum | bus

</div>
</div>





## 参数

要以交互方式编辑模块参数，请双击该模块。


<div class="details-box">
<details open>
<summary>总线中的信号 — 输入总线中元素的列表<div>元素名称列表</div></summary>
</details>
<div class="details-content">

此属性为只读

输入元素列表包括进入模块的所有元素，包括嵌套总线的元素。元素旁边的箭头表示输入元素是总线。要显示该总线的内容，请单击箭头。

</div>
</div>



<!-- 要突出显示进入模块的元素的来源，请在列表中选择该元素，然后单击**查找**。

如果在对话框打开时更改了元素名称，请单击**刷新**以更新列表中的名称。

#### 编程用法

| **模块参数：**InputSignals |
| ---------------------------- |
| **类型：**元胞数组           |
| **值：**元素名称             | -->


<!-- 暂无
### 按名称过滤 — 用于过滤显示的输入元素的搜索词 文本



要过滤显示的输入元素，请输入搜索词。过滤器可执行部分字符串搜索。请勿将搜索词括在引号内。

要访问过滤选项，请单击**按名称过滤**框右侧的**显示过滤选项** ![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/filter_by_name_button.png) 按钮。 -->


<!-- 暂无
### 启用正则表达式 — 通过正则表达式过滤显示的输入元素的选项 “off” （默认） | “on”



选择此参数以使用正则表达式或部分搜索字符串过滤显示的输入元素。默认情况下，您可以仅使用部分搜索字符串过滤显示的输入元素。

正则表达式允许您根据输入元素是否匹配某个模式进行过滤。例如，在**按名称过滤**框中输入 t$，以显示名称以小写字母 t 结尾的所有元素（及其直接父级）。有关详细信息，请参阅[正则表达式](https://ww2.mathworks.cn/help/releases/R2022b/matlab/matlab_prog/regular-expressions.html)。

#### 依存关系

要访问此参数，请单击**按名称过滤**框右侧的**显示过滤选项** ![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/filter_by_name_button.png) 按钮。 -->


<!-- 暂无
### 将过滤结果显示为扁平列表 — 将过滤结果显示为平面列表的选项 “off” （默认） | “on”





选择此参数以扁平列表形式显示过滤结果，该列表使用圆点表示法来反映总线层次结构。默认情况下，过滤结果显示在层次结构树中。

#### 依存关系

要访问此参数，请单击**按名称过滤**框右侧的**显示过滤选项** ![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/filter_by_name_button.png) 按钮。 -->


<div class="details-box">
<details open>
<summary>选择的信号 — 输入总线的所选元素<div>元素名称的列表</div></summary>
</details>
<div class="details-content">

此列表中的每个元素都包含在模块输出中。

要向模块输出添加元素，请执行以下操作：

1. 从**总线中的信号**列表中选择一个或多个元素。

   如果您是从**总线中的信号**列表中选择多个元素，则您选择它们的顺序将设置它们在**所选元素**列表中的顺序。

2. （可选）指定您要元素出现在**所选元素**列表中的位置。选择希望添加的元素出现在其下方的元素。如果不选择元素，添加的元素会出现在列表的末尾。

3. 单击**选择**。

或者，在 Sysblock 编辑器中，当输入端口接收总线并且所有输出端口都连接到其他端口时，在 BusSelector 模块的输出端口附近绘制一条新信号线。Sysblock 提示您指定要选择的元素，并为您指定的元素添加端口。当**以虚拟总线输出**处于选中状态时，您无法以这种方式创建端口。

要更改输出元素的顺序，请在列表中选择一个元素或多个连续的元素，然后单击**上移**或**下移**。当您更改元素顺序时，端口会保持连接。

要从模块输出中删除元素，请在列表中选择元素，然后单击**移除**。

如果列表中的某个元素不在输入总线中，则该元素名称以三个问号 (???) 开头。请修改输入总线以包含指定名称的元素，或从列表中删除该元素。

**限制：** 为了避免递归限制，请为每个 BusSelector 模块选择少于 500 个元素。

</div>
</div>




<!-- 暂无
#### 编程用法

| **模块参数**：OutputSignals              |
| ------------------------------------------ |
| **类型：**字符向量                         |
| **值：**'signal1,signal2' 形式的字符向量 |
| **默认值：**无                             | -->

 
<div class="details-box">
<details open>
<summary>输出为虚拟总线 — 将所选元素作为虚拟总线输出的选项<div>“off” （默认） | “on”</div></summary>
</details>
<div class="details-content">

默认情况下，模块将每个所选元素从一个单独的输出端口输出，该端口上标有对应总线元素的名称。选择此参数可从一个端口输出所选元素，这些元素组合在一个虚拟总线中。

<!-- 要将输出转换为非虚拟总线，请在 Bus Selector 模块后插入一个 [Signal Conversion]() 模块。将 Signal Conversion 模块的**输出**参数设置为“非虚拟总线”，并将**数据类型**设置为 [Simulink.Bus]() 对象。 -->

当**所选元素**列表中只有一个元素而您启用了**以虚拟总线输出**时，则该元素不会包装在总线中。例如，如果元素是一个总线，则输出元素是该总线。如果该元素不是总线，则输出元素不是总线。

</div>
</div>


<!-- #### 编程用法

| **模块参数**：OutputAsBus |
| --------------------------- |
| **类型：**字符向量          |
| **值：**'on' | 'off'    |
| **默认值：**'off'         | -->

<!-- 不确定
## 模块特性

| **数据类型**     | Boolean | bus | double | enumerated | fixed point | half | integer | float | string |
| ---------------- | ------------------------------------------------------------ |
| **直接馈通**     | 是                                                         |
| **多维信号**     | 是                                                         |
| **可变大小信号** | 是                                                         |
| **过零检测**     | 否                                                         |

## 提示

对于位于子系统和模型接口上的总线，您可以使用 [In Bus Element](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/inbuselement.html) 模块，而不是 Inport 模块和 Bus Selector 模块。In Bus Element 模块能够：

- 减少模块图中线的复杂度和杂乱无章。
- 使增量更改接口更容易。
- 允许访问更靠近使用点的总线元素，避免使用 Bus Selector 和 Goto 模块配置。 -->

## 版本历史记录

- 在 2024b 之前推出

### 限制信息

1. 暂不支持按名称过滤的功能；  
2. 暂不支持启用正则表达式的复选框；  
3. 暂不支持将过滤结果显示为扁平列表的复选框；  
4. 输入端口暂不支持float、double、half、int8、int16、int32、int64、uint8、uint16、uint32、uint64、string、boolean、fixedPoint 和 enum 的数据类型，输出端口暂不支持 half、int64、uint64 和 string 的数据类型，且都不支持复数；

<!-- 暂无
## 扩展功能



### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。

实际数据类型或功能支持取决于模块实现。



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 Verilog 代码和 VHDL 代码。



HDL Coder™ 提供影响 HDL 实现和综合逻辑的额外配置选项。

要了解有关使用总线进行 HDL 代码生成的更多信息，请参阅[Buses](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/signal-and-data-type-support.html#buaqcxf) (HDL Coder) 和[Use Bus Signals to Improve Readability of Model and Generate HDL Code](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/use-bus-signals-to-improve-readability-of-model.html) (HDL Coder)。

**HDL 架构**

此模块具有一个默认 HDL 架构。

**HDL 模块属性**

| **ConstrainedOutputPipeline** | 通过移动设计中现有延迟的方式来放置在输出端的寄存器的数量。分布式流水线处理不会重新分发这些寄存器。默认值为 0。有关详细信息，请参阅[ConstrainedOutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#btp8gmp) (HDL Coder)。 |
| ----------------------------- | ------------------------------------------------------------ |
| **InputPipeline**             | 要在生成的代码中插入的输入流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 0。有关详细信息，请参阅[InputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-25) (HDL Coder)。 |
| **OutputPipeline**            | 要在生成的代码中插入的输出流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 0。有关详细信息，请参阅[OutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-26) (HDL Coder)。 |



### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。

实际数据类型或功能支持取决于模块实现。

## 版本历史记录

**在 R2006a 之前推出** -->


## 另请参阅

[BusCreator](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SignalRouting/BusCreator.html) | [BustoVector](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SignalRouting/BusToVector.html)

 <!-- | [Out Bus Element]()| [Bus Assignment]()  -->

<!-- 暂不需要
### 主题

- [将信号或消息组合到虚拟总线中]()
- [Simplify Subsystem and Model Interfaces with Bus Element Ports]()
- [Bus-Capable Blocks]()
- [Assign Signal Values to Bus Elements]() -->