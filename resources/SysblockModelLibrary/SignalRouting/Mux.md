# Mux
---
将相同数据类型和输入信号合并为虚拟向量

**库：** Sysblock模块库 / SignalRouting

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/Mux/Mux.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

Mux 模块将具有相同数据类型和输入合并为一个虚拟向量。您可以使用多个 Mux 模块分多个阶段创建复路信号，但结果是平面结构，就像您只使用一个 Mux 模块一样。


::: tip 提示 
使用 [BusCreator](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SignalRouting/BusCreator.html) 模块，而不是 Mux 模块。Bus Creator 模块会创建虚拟总线，让您能够灵活地将不同数据类型和元素进行组合。虚拟总线还允许您按名称而不是索引来访问元素。如果模块需要虚拟向量而不是虚拟总线，模型编译会将总线转换为向量。
<!-- 有关复路信号和虚拟总线的比较，请参阅[Choose Among Composite Interfaces](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/choose-among-composite-interfaces.html)。 -->

:::



## 示例

<!-- [![Function-Call Subsystems with Multiple Initiators](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink/win64/FunctionCallSubsystemsWithMultipleInitiatorsExample_01.png)Function-Call Subsystems with Multiple InitiatorsA function-call subsystem that is called by multiple different function-call initiators that are grouped by a Mux block.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/function-call-subsystems-with-multiple-initiators.html) -->

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/Mux.mo">Mux.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/Mux/Mux_ex.png')" style="width: 600px; transform: scale(0.8);">

### 示例说明

- Mux 模块：Mux 模块用于将多个信号合并成一个信号。它将多个输入信号打包成一个向量输出信号，输出信号的每个元素对应一个输入信号。在这个示例中，我们使用 Mux 模块将两个输入信号和一个选择信号合并成一个单一的输出信号；
- Step 模块：提供不同的步变信号作为 Mux 的数据输入和选择信号；
- Scope 模块：用于显示模型的输出结果，即根据选择信号选择的输入信号。


## 端口

### 输入


<div class="details-box">
<details open>
<summary>u1 — 要包含在复路信号中的输入信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

要包含在复路信号中的输入信号，指定为标量或向量。

Mux 模块的输入信号可以是标量和向量的任意组合，但它们必须具有相同的数据类型和复/实性或为函数调用信号。

**数据类型：** float | double | half | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | fixedPoint | enum

</div>
</div>





<div class="details-box">
<details open>
<summary>u2 — 要包含在复路信号中的输入信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

要包含在复路信号中的输入信号，指定为标量或向量。

Mux 模块的输入信号可以是标量和向量的任意组合，但它们必须具有相同的数据类型和复/实性或为函数调用信号。

**数据类型：** float | double | half | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | fixedPoint | enum

</div>
</div>




### 输出

<div class="details-box">
<details open>
<summary>y — 输出复路信号<div>向量</div></summary>
</details>
<div class="details-content">

由合并的输入信号组成的输出复路信号，以向量形式返回。

输出复路信号的元素按照输入信号的端口顺序排列。
<!-- 有关各种模块方向的端口顺序的描述，请参阅[旋转或翻转后的端口位置](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/changing-a-blocks-appearance.html#f13-83952)。 -->

**数据类型：** float | double | half | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | fixedPoint | enum

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>输入数目 — 输入信号的数量<div>2 （默认） | 标量 </div></summary>
</details>
<div class="details-content">

输入信号的数量，指定为正整数标量。使用此格式时，模块接受任意大小的标量或向量信号。Sysblock 为每个输入指定名称 signalN，其中 N 表示输入端口号。


</div>
</div>




<!-- #### 编程用法

| **模块参数：**Inputs                                       |
| ------------------------------------------------------------ |
| **类型：**标量、向量、元胞数组、以逗号分隔的信号名称列表     |
| **值：**整数、端口大小向量、元胞数组、以逗号分隔的信号名称列表 |
| **默认值：**'2'                                            | -->



<!-- ### 显示选项 — 模块图标外观 “bar” （默认） | “信号” | “无”



模块图标外观，指定为“竖线”、“信号”或“无”。

- “竖线” - 不显示文本
- “信号” - 显示输入信号名称
- “无” - 显示模块的类型 (Mux)

根据需要调整模块的大小，以适合模块图标上的文本。

#### 编程用法

| **模块参数**：DisplayOption               |
| ------------------------------------------- |
| **类型：**字符向量                          |
| **值：**'bar' 'signals' 'none''bar' |
| **默认值：**'bar'                         | -->



<!-- ## 模块特性

| **数据类型**     | Boolean | double | enumerated | fixedPoint | half | integer | single |
| ---------------- | ------------------------------------------------------------ |
| **直接馈通**     | 是                                                         |
| **多维信号**     | 否                                                         |
| **可变大小信号** | 否                                                         |
| **过零检测**     | 否                                                         | -->


## 版本历史记录

- 在 2024b 之前推出

### 限制信息

1. 暂不支持显示选项的功能；  
2. 输入和输出端口暂不支持half、int64、uint64 和 image 的数据类型；
3. 输入端口仅支持正整数标量输入。

<!-- ## 扩展功能



### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。

实际数据类型或功能支持取决于模块实现。



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 Verilog 代码和 VHDL 代码。



HDL Coder™ 提供影响 HDL 实现和综合逻辑的额外配置选项。

**HDL 架构**

此模块具有一个默认 HDL 架构。

**HDL 模块属性**

| **ConstrainedOutputPipeline** | 通过移动设计中现有延迟的方式来放置在输出端的寄存器的数量。分布式流水线处理不会重新分发这些寄存器。默认值为 0。有关详细信息，请参阅[ConstrainedOutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#btp8gmp) (HDL Coder)。 |
| ----------------------------- | ------------------------------------------------------------ |
| **InputPipeline**             | 要在生成的代码中插入的输入流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 0。有关详细信息，请参阅[InputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-25) (HDL Coder)。 |
| **OutputPipeline**            | 要在生成的代码中插入的输出流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 0。有关详细信息，请参阅[OutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-26) (HDL Coder)。 |

**复数数据支持**

此模块支持复信号的代码生成。

**限制**

HDL 代码生成不支持总线。



### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。

实际数据类型或功能支持取决于模块实现。

## 版本历史记录

**在 R2006a 之前推出** -->

## 另请参阅

[DeMux](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SignalRouting/DeMux.html) | [BusCreator](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SignalRouting/BusCreator.html) | [BustoVector](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SignalRouting/BusToVector.html)



<!--
| [Vector Concatenate](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/vectorconcatenate.html)

### 主题

- [虚拟和非虚拟信号](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/signal-types.html#bq4ic6w-1)
- [合成接口规范](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/composite-signal-techniques.html)
- [Simplify Subsystem and Model Interfaces with Bus Element Ports](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/simplify-subsystem-bus-interfaces.html) -->