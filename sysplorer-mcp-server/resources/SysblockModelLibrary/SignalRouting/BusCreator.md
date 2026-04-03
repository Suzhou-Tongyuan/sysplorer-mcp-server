# BusCreator
---
将输入信号或消息组合到总线中

**库：** Sysblock模块库 / SignalRouting

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/BusCreator/BusCreator.png')" style="width: 100px; height: auto; transform: scale(1);">


## 描述

BusCreator 模块将输入信号或消息合并总线中，该总线保留信号和消息的各自的身份。默认情况下，BusCreator 模块创建一个虚拟总线，它类似于用束线带绑在一起的一捆电线。

总线元素必须具有唯一名称。默认情况下，总线的每个元素都继承连接到 BusCreator 模块的元素的名称。如果存在重复名称，BusCreator 模块会将端口号追加到所有输入元素名称。对于没有名称的元素，BusCreator 模块会生成 signaln 形式的名称，其中 n 是连接到元素的端口号。当您搜索元素源或选择元素以连接到其他模块时，您可以按名称引用元素。
<!-- 有关元素命名规范，请参阅[信号名称和标签]()。 -->

要按名称从总线中提取元素，请使用 [BusSelector](BusSelector.html) 模块。  

要创建包含其他总线的总线，请将其他总线连接到 BusCreator 模块输入端口。  

## 示例

<!-- [![将信号线组合在一个组件内](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/virtualbuscreationfinal_zh_CN.png)将信号线组合在一个组件内](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/getting-started-with-buses.html#bve502j-1)

[![Create Nonvirtual Buses Within a Component](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink/win64/xxNonvirtualBusCreationNestedBus.png)Create Nonvirtual Buses Within a Component](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/create-nonvirtual-buses.html#mw_cf61dd63-1e2a-4e9b-a5ae-60c574ad806d)

[![Simplify Bus Interfaces in Subsystems and Models](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink/win64/xxBusInterfaceConversionFinal.png)Simplify Bus Interfaces in Subsystems and Models](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/simplify-subsystem-bus-interfaces.html#bvmdxtx)

[![了解 Simulink 总线功能](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/simulinkbussignalsexample_01_zh_CN.png)了解 Simulink 总线功能在组件中使用总线，在组件接口上使用总线端口，并更快地执行常见总线工作流。](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/simulink-bus-signals.html) -->

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/BusCreator.mo">BusCreator.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/BusCreator/BusCreator_ex.png')" style=" width: 600px; transform: scale(0.8);">

### 示例说明

- Constant 模块：提供固定的数值作为输入信号；
- BusCreator 模块：将多个输入信号合并为一个总线信号。这个模块可以处理不同类型的元素，包括信号、其他总线，甚至是消息。使用 BusSelector 模块可以访问总线中的元素；
- BusToVector 模块：将总线信号分解为单独的信号，以便进一步处理或观察；
- Scope 模块：用于显示模型的输出结果，即合并后的总线信号。


## 端口

### 输入


<div class="details-box">
<details open>
<summary>u1 — 要包含在总线中的输入元素<div>标量 | 向量 | 矩阵 | 数组 | 总线</div></summary>
</details>
<div class="details-content">

输入端口接受要包含在总线中的元素。输入端口的数量由**输入的数目**参数决定。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | fixedPoint | enum | bus

</div>
</div>



<div class="details-box">
<details open>
<summary>u2 — 要包含在总线中的输入元素<div>标量 | 向量 | 矩阵 | 数组 | 总线</div></summary>
</details>
<div class="details-content">

输入端口接受要包含在总线中的元素。输入端口的数量由**输入的数目**参数决定。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | fixedPoint | enum | bus

</div>
</div>




### 输出

<div class="details-box">
<details open>
<summary>y — 输出总线<div>总线</div></summary>
</details>
<div class="details-content">

输出总线由输入元素组成。
<!-- [以非虚拟总线输出]()参数指定输出总线是虚拟总线还是非虚拟总线。有关总线类型的信息，请参阅[合成接口规范]()。 -->

**数据类型：** bus

</div>
</div>



## 参数

<div class="details-box">
<details open>
<summary>端口数目 — 输入元素的数量<div>2 （默认） | 整数</div></summary>
</details>
<div class="details-content">

输入元素的数量必须为大于或等于 2 的整数。增加输入的数目会向模块添加空的输入端口。在对模型进行仿真之前，请确保为每个输入端口连接了输入元素。

在修改**输入的数目**参数后，单击**刷新**以更新元素列表。

如果所有输入端口都已连接，您可以通过将另一条线连接到 BusCreator 模块来添加一个输入端口。

<!-- ![A line is dragged near a Bus Creator block with two connected ports and a third port appears.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/bus_creator_port_sprouting.png) -->

以交互方式添加端口会更新**输入的数目**参数，并将新元素添加到总线中的元素列表。

</div>
</div>




<!-- #### 编程用法

| **模块参数**：Inputs                                |
| ----------------------------------------------------- |
| **类型：**字符向量                                    |
| **值：**大于或等于 2 的整数，以逗号分隔的元素名称列表 |
| **默认值：**'2'                                     |

默认情况下，Inputs 参数指定输入的数目。当您使用它来指定总线中元素的名称时，输入的数目与您指定的元素名称的数目相匹配。 -->


<div class="details-box">
<details open>
<summary>总线中的信号 — 输入元素的列表<div>元素名称列表</div></summary>
</details>
<div class="details-content">

输入元素列表包括进入模块的所有元素，包括嵌套总线的元素。元素旁边的箭头表示输入元素是总线。要显示该总线的内容，请单击箭头。

<!-- 要突出显示进入模块的元素的来源，请在列表中选择该元素，然后单击**查找**。 -->

如果在对话框打开时更改了元素名称，请单击**重置**以更新列表中的名称。

<!-- 要重新排列输出总线中的元素，请使用**向上**和**向下**按钮。您可以在**总线中的元素**列表中选择多个要进行重新排序或删除的顶层相邻元素。 -->

要添加或删除输入元素，请分别单击**添加**或**移除**。然后，单击**确定**来更新模块图标。在对模型进行仿真之前，请确保为每个输入端口连接了输入元素。

</div>
</div>




<!-- #### 编程用法

| **模块参数**：Inputs                                |
| ----------------------------------------------------- |
| **类型：**字符向量                                    |
| **值：**大于或等于 2 的整数，以逗号分隔的元素名称列表 |
| **默认值：**'2'                                     |

默认情况下，Inputs 参数指定输入的数目。当您使用它来指定总线中元素的名称时，输入的数目与您指定的元素名称的数目相匹配。 -->


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
<summary>输出类型 — 输出总线的数据类型<div>“'Inherit: auto'”</div></summary>
</details>
<div class="details-content">

指定输出总线的数据类型。

</div>
</div>
 <!-- （默认） | “'Bus: <object name>'” | “<data type expression>” -->


<!-- 如果选择 “Bus: <object name>”，请用 [Simulink.Bus](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/simulink.bus.html) 对象的名称替换 <object name>。编辑模型时，必须可以访问 Bus 对象。

要使用**[类型编辑器](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/typeeditor.html)**定义 Bus 对象，请单击**显示数据类型助手**按钮 ![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/show_data_type_asst_button.png)，将**模式**设置为“总线对象”，然后单击**编辑**按钮。

如果选择 “<data type expression>”，请指定一个计算结果为 Bus 对象的表达式。

#### 编程用法

| **模块参数**：OutDataTypeStr                     |
| -------------------------------------------------- |
| **类型：**字符向量                                 |
| **值**：'Inherit: auto' | 'Bus: <object name>' |
| **默认值：**'Inherit: auto'                      | -->


<!-- 暂无
### 要求输入的名称与以上的名称匹配 — 检查输入元素名称是否与对话框中列出的名称相匹配的选项 “off” （默认） | “on”



在以后的版本中可能会删除此参数。要强制实施强数据定型，请使用**[使用来自输入的名称，而不是来自总线对象的名称](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/buscreator.html#mw_54a02d9d-ed3f-4d5e-b851-7caa32cc2ddc)**参数。

当选中时，此参数检查输入元素名称是否与“模块参数”对话框中列出的名称相匹配。如果元素名称不匹配，Simulink® 将返回错误。

#### 依存关系

- 如果您选中**使用来自输入的名称，而不是来自总线对象的名称**，此参数将被忽略。
- 如果您以编程方式更改**[输入数目](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/buscreator.html#mw_b3ffa862-4ff5-4b40-8ced-dfd7f112ae98)**，此参数将还原为 “off”。 -->


<!-- 暂无
### 重命名所选信号 — 所选输入元素的新名称 '' （默认） | 字符向量



指定所选输入元素的新名称。有关名称规范，请参阅[信号名称和标签](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/signal-basics.html#brh77af-1)。

#### 依存关系

要启用此参数，请选中**[要求输入的名称与以上的名称匹配](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/buscreator.html#mw_9c576a23-2d94-4d29-9d3a-3e96cb23d4bc)**。 -->


<div class="details-box">
<details open>
<summary>使用信号线名称，而不是端口名 — 使用来自输入元素（而不是总线对象）的名称的选项<div>“on” （默认） | “off”</div></summary>
</details>
<div class="details-content">

默认情况下，BusCreator 模块使用输入元素名称作为输出总线元素名称。

</div>
</div>



<!-- 即使您将 Simulink.Bus 对象指定为数据类型也是如此。 -->

<!-- 暂无
要从 Bus 对象继承总线元素名称，请清除此参数。清除此参数将：

- 强制应用强数据定型。
- 避免在 Bus 对象和模型中多次输入一个元素名称。多次输入名称可能会无意间创建不匹配的元素名称。
- 支持在数组元素之间必须具有一致的元素名称这一总线数组要求。

您也可以通过检查输入元素名称是否与 Bus 对象元素名称匹配来强制实施强数据定型。保持此参数处于选中状态，并将**[元素名称不匹配](https://ww2.mathworks.cn/help/releases/R2022b/simulink/gui/element-name-mismatch.html)**配置参数设置为“错误”。

#### 依存关系

要启用此参数，请将**[输出数据类型](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/buscreator.html#mw_258f3244-c9b5-421f-bcbf-04948943c193)**设置为 Bus 对象。

#### 编程用法

| **模块参数**：InheritFromInputs |
| --------------------------------- |
| **类型：**字符向量                |
| **值：** 'on' | 'off'         |
| **默认值：**'on'                | -->


<!-- 暂无
### 以非虚拟总线输出 — 输出非虚拟总线的选项 “off” （默认） | “on”



选择此参数以输出非虚拟总线而不是虚拟总线。

非虚拟总线中的所有元素都必须具有相同的采样时间，即使关联的 Bus 对象的元素为某些元素指定了继承采样时间也是如此。任何导致包含不同采样率元素的非虚拟总线的操作都会生成错误。要更改采样时间不同于其他非虚拟总线输入元素的元素或总线的采样时间，请使用 [Rate Transition](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/ratetransition.html) 模块。有关详细信息，请参阅[Modify Sample Times for Nonvirtual Buses](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/specify-bus-signal-sample-times.html)。

要生成使用 C 结构体定义此模块创建的总线结构的代码，请启用此参数。

#### 依存关系

要启用此参数，请将**[输出数据类型](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/buscreator.html#mw_258f3244-c9b5-421f-bcbf-04948943c193)**设置为 Bus 对象。

#### 编程用法

| **模块参数**：NonVirtualBus |
| ----------------------------- |
| **类型：**字符向量            |
| **值：**'on' | 'off'      |
| **默认值：**'off'           | -->


<!-- 不确定
## 模块特性

| **数据类型**     | Boolean | bus | double | enumerated | fixed point | half | integer | float | string |
| ---------------- | ------------------------------------------------------------ |
| **直接馈通**     | 否                                                         |
| **多维信号**     | 是                                                         |
| **可变大小信号** | 是                                                         |
| **过零检测**     | 否                                                         | -->
<!-- 暂无
## 提示

对于位于子系统和模型接口上的总线，您可以使用 [Out Bus Element]() 模块，而不是 Bus Creator 模块和 Outport 模块。Out Bus Element 模块能够：

- 减少模块图中线的复杂度和杂乱无章。
- 使增量更改接口更容易。 -->


## 版本历史记录

- 在 2024b 之前推出

### 限制信息

1. 暂不支持按名称过滤的功能；  
2. 暂不支持启用正则表达式的复选框；  
3. 暂不支持将过滤结果显示为扁平列表的复选框；  
4. 暂不支持 `Bus: <object name>` 和 `<data type expression>` 的输出类型；  
5. 暂不支持要求输入的名称与以上的名称匹配的复选框；   
6. 暂不支持重命名所选信号；  
7. 暂不支持输出非虚拟总线的选项；  
8. 输入端口暂不支持 half、int64、uint64 和 string 的数据类型，输出端口暂不支持float、double、half、int8、int16、int32、int64、uint8、uint16、uint32、uint64、string、boolean、fixedPoint 和 enum 的数据类型，且都不支持复数；


<!-- ## 扩展功能



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

**在 R2006a 之前推出**



### R2014b: 不推荐使用**要求输入的名称与以上的名称匹配**参数

**要求输入的名称与以上的名称匹配**参数可能会在以后的版本中删除。要强制实施强数据定型，请改用**[使用来自输入的名称，而不是来自总线对象的名称](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/buscreator.html#mw_54a02d9d-ed3f-4d5e-b851-7caa32cc2ddc)**参数。 -->


## 另请参阅

[BusSelector](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SignalRouting/BusSelector.html) | [BustoVector](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SignalRouting/BusToVector.html)

<!-- [Bus Assignment]() |  | [Out Bus Element]() -->


<!-- 暂不需要
### 主题

- [将信号或消息组合到虚拟总线中]()
- [Simplify Subsystem and Model Interfaces with Bus Element Ports]()
- [Bus-Capable Blocks]()
- [Assign Signal Values to Bus Elements]()
- [Modify Sample Times for Nonvirtual Buses]()
- [使用 Simulink.Bus 对象数据类型指定总线属性]() -->