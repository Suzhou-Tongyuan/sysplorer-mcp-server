# BusToVector
---
将虚拟总线转换为向量

**库：** Sysblock模块库 / SignalRouting

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/BusToVector/BusToVector.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

BustoVector 模块将虚拟总线转换为向量信号。输入总线必须由具有相同的数据类型、信号类型和采样模式的标量或一维、行或列向量组成。如果输入总线包含行向量或列向量，则将分别输出一个行向量或一个列向量。否则，输出是一维数组。

BustoVector 模块仅用于将隐式的总线到向量转换替换为显式转换。

不接受总线的模块可能隐式将总线转换为向量。当总线被视为向量时，总线元素变得不可访问。

<!-- Bus to Vector 模块仅用于将隐式的总线到向量转换替换为显式转换。如果想在不手动插入 Bus to Vector 模块的情况下识别和纠正用作向量的总线，您可以使用模型顾问检查[检查被视为向量的总线信号](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/simulink-checks.html#bvjmey9-1)。您也可以使用 [Simulink.BlockDiagram.addBusToVector](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/simulink.blockdiagram.addbustovector.html) 函数，它会在所需的位置自动插入 Bus to Vector 模块。 -->



<!-- **注意**

如果您在 R2007a 之前的 Simulink® 产品版本中使用**另存为**保存模型，则每个 Bus to Vector 模块会被替换为不输出任何内容的空子系统。要在这种情况下使用模型，您必须重新连接，否则就需要纠正每个用来包含 Bus to Vector 模块但现在被空子系统中断的路径。 -->

## 示例

<!-- [![Manage Bus-to-Vector Conversions](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink/win64/ConvertBusSignalToAVectorExample_02.png)Manage Bus-to-Vector ConversionsUse a Bus to Vector block to convert a bus to a vector, to provide a signal that the Gain block can accept.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/convert-bus-signal-to-a-vector.html) -->

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/BusToVector.mo">BusToVector.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/BusToVector/BusToVector_ex.png')" style="width: 600px; transform: scale(0.8);">

### 示例说明

- Constant 模块：提供固定的数值作为输入信号；
- BusCreator 模块：将多个输入信号合并为一个总线信号；
- BusToVector 模块：将总线信号分解为单独的信号，以便进一步处理或观察；
- Scope 模块：用于显示模型的输出结果，即合并后的总线信号。


## 端口

### 输入


<div class="details-box">
<details open>
<summary>u — 要转换为向量的总线<div>虚拟总线</div></summary>
</details>
<div class="details-content">

输入总线必须由具有相同的数据类型、信号类型和采样模式的标量或一维、行或列向量组成。该模块暂不支持输入是非总线信号，且输入信号需为虚拟总线信号。

**数据类型**： bus

</div>
</div>




### 输出

<div class="details-box">
<details open>
<summary>y — 输出向量<div>标量 | 一维数组 | 行向量 | 列向量</div></summary>
</details>
<div class="details-content">

输出向量的维数取决于输入总线元素的维数。如果输入总线包含行向量或列向量，此模块将分别输出一个行向量或一个列向量。否则，输出是一维向量。

**数据类型**： float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | fixedPoint | enum

</div>
</div>



<!-- 不确定
## 模块特性

| **数据类型**     | Boolean | bus | double | enumerated | fixed point | half | integer | single |
| ---------------- | ------------------------------------------------------------ |
| **直接馈通**     | 否                                                         |
| **多维信号**     | 否                                                         |
| **可变大小信号** | 否                                                         |
| **过零检测**     | 否                                                         | -->


## 版本历史记录

- 在 2024b 之前推出

### 限制信息

输入端口暂不支持float、double、half、int8、int16、int32、int64、uint8、uint16、uint32、uint64、boolean、fixedPoint 和 enum 的数据类型，输出端口暂不支持 half、int64 和 uint64 的数据类型，且都不支持复数。

<!-- ## 扩展功能



### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 Verilog 代码和 VHDL 代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。

## 版本历史记录

**在 R2007a 中推出** -->


## 另请参阅

### 模块

[BusCreator](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SignalRouting/BusCreator.html) | [/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SignalRouting/BusSelector](BusSelector.html) | [/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SignalRouting/Mux](Mux.html) | [TypeConversion](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/TypeConversion.html)

<!-- ### 函数

- [Simulink.BlockDiagram.addBusToVector]()

### 主题

- [Identify Automatic Bus Conversions]()
- [合成接口规范]() -->