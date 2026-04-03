# Constant
---
&nbsp;

生成常量值。

**库：** TYDSPSystem / SignalGenerationManipulationAndAnalysis / SignalGeneration

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/Constant/Constant.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

Constant 模块生成实数或复数常量值信号。使用此模块提供常量信号输入。

<!-- 此模块是生成标量、向量还是混合输出要取决于：

- **常量值**参数的维度
- **将向量参数解释为一维向量**参数的设置 -->

此模块的输出与**常量值**参数具有相同的维度和元素。
<!-- 如果为此参数指定向量，即您希望模块将其解析为向量，请选中**将向量参数解释为一维向量**复选框。否则， -->
如果为**常量值**参数指定了向量，模块会将该向量视为一个矩阵。



<!-- **提示**

要输出常量枚举值，请考虑改用 [Enumerated Constant](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/enumeratedconstant.html) 模块。Constant 模块提供不适用于枚举类型的模块参数，例如**输出最小值**和**输出最大值**。 -->

### 使用总线对象作为输出数据类型

Constant 模块支持使用非虚拟总线作为输出数据类型。使用总线对象作为输出数据类型可以帮助简化您的模型。如果使用总线对象作为输出数据类型，请将**常量值**设置为 0。
<!-- 或者与该总线对象匹配的 MATLAB® 结构体。 -->

### 对总线的常量值使用结构体

您指定的结构体中必须为总线对象所代表的总线中的每个元素包含一个值。模块输出为非虚拟总线信号。

<!-- 您可以使用 [Simulink.Bus.createMATLABStruct](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/simulink.bus.creatematlabstruct.html) 创建一个与总线对应的完全结构体。

也可以使用 [Simulink.Bus.createObject](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/simulink.bus.createobject.html) 从 MATLAB 结构体中创建一个总线对象。

如果输出总线中的信号元素使用除 double 之外的其他数字数据类型，则您可以通过使用类型化表达式（例如 uint16(37)）或非类型化表达式（例如 37）来指定结构体字段。要控制字段数据类型，您可以使用总线对象作为 Simulink.Parameter 对象的数据类型。要决定是使用类型化表达式还是非类型化表达式，请参阅[Control Data Types of Initial Condition Structure Fields](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/generate-code-for-bus-signals.html#buxv6qs-1)。 -->

<!-- ### 设置配置参数以支持使用总线对象数据类型

要允许使用总线对象作为输出数据类型，请在开始仿真之前，将**配置参数** > **诊断** > **数据有效性** > **高级参数** > **欠定初始化检测**设置为“简化”。有关详细信息，请参阅 [欠定初始化检测](https://ww2.mathworks.cn/help/releases/R2022b/simulink/gui/underspecified-initialization-detection.html)。 -->

## 示例

<!-- [![Create Nonvirtual Bus from MATLAB Structure](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink/win64/CreateNonvirtualBusFromStructureExample_01.png)Create Nonvirtual Bus from MATLAB Structure](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/create-nonvirtual-buses.html#mw_4bc621b4-576a-46c5-afe9-b43e8bcd16dd)

[![自动气候控制系统仿真](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/simulatingautomaticclimatecontrolsystemsexample_01_zh_CN.png)自动气候控制系统仿真此示例说明如何使用 Simulink® 和 Stateflow® 对汽车中自动气候控制系统进行仿真。](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/simulating-automatic-climate-control-systems.html)

[![使用时序逻辑的 Bang-Bang 控制](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/sldemo_boilerexample_01_zh_CN.png)使用时序逻辑的 Bang-Bang 控制此示例说明如何使用 Stateflow® 为锅炉的 Bang-Bang 温度控制系统建模。在 Simulink® 中对锅炉动态特性进行建模。](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/bang-bang-control-using-temporal-logic.html)

[![弹球的仿真](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/sldemo_bounceexample_04_zh_CN.png)弹球的仿真此示例使用两个弹球 Simulink® 模型来说明对具有 Zeno 行为的混合动态系统进行建模的不同方法。该示例还提供每种方法的优点。](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/simulation-of-a-bouncing-ball.html) -->

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/Constant.mo">Constant.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/Constant/Constant_ex.png')" style="width: 300px; height: auto; transform: scale(0.8);">


### 示例说明

- Constant 模块：生成一个固定的数值信号。这个模块可以用于提供模型中的常数输入，例如设定的参数值、阈值等；
- Scope 模块：用于显示模型的输出结果，即 Constant 模块生成的固定数值信号。

## 端口

### 输出

<div class="details-box">
<details open>
<summary>y — 常量值<div>标量 | 向量 | 矩阵 | N 维数组</div></summary>
</details>
<div class="details-content">

常量值，指定为实数或复数值标量、向量、矩阵或 N 维数组。默认情况下，Constant 模块输出的信号与**常量值**参数具有相同的维度、数据类型和复/实性。但是，您可以为输出指定 Sysblock 支持的任何数据类型，包括定点和枚举数据类型。


<!-- **注意**

如果您指定总线对象作为此模块的数据类型，请不要为模块的总线数据设置最大值。因为 Simulink 会忽略此设置。但请为指定作为数据类型的总线对象的总线元素设置最大值。有关详细信息，请参阅 [Simulink.BusElement](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/simulink.buselement.html)。 -->

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | fixedPoint | enum

</div>
</div>



## 参数



### 主要


<div class="details-box">
<details open>
<summary>常量值 — 常量输出值<div>1 （默认） | 标量 | 向量 | 矩阵 | N 维数组</div></summary>
</details>
<div class="details-content">

为模块指定常量值输出。

</div>
</div>



<!-- - 您可以输入 MATLAB 以矩阵方式运算的任何表达式，包括布尔关键字 true 和 false。

- 如果您将**输出数据类型**设置为总线对象，则可以指定下列选项之一：

  - 与总线对象对应的完全 MATLAB 结构体
  - 0，以表示与总线对象的接地值对应的结构体

  有关详细信息，请参阅[使用总线对象作为输出数据类型](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/constant.html#bslokor)。

- 对于非总线数据类型，Simulink 使用最邻近舍入方法和饱和溢出操作，自动将此参数从其值数据类型转换为指定的输出数据类型。

#### 编程用法

| **模块参数**：Value                    |
| ---------------------------------------- |
| **类型：**字符向量                       |
| **值：**标量 \| 向量 \| 矩阵 \| N 维数组 |
| **默认值：**'1'                        | -->



<!-- ### 将向量参数解释为一维向量 — 将向量视为一维 on （默认） | off



如果**常量值**参数的计算结果为包含 N 个元素的行或列向量，选中此复选框将输出长度为 N 的向量。

- 如果**常量值**参数的计算结果为包含 N 个元素的行或列向量，则选中此复选框时，模块将输出长度为 N 的向量。
- 清除此复选框后，如果**常量值**参数的计算结果为一个包含 N 个元素的行向量或列向量，模块将输出一个维数为 1×N 或 N×1 的矩阵。例如，该模块输出 1×N 或 N×1 矩阵。

#### 编程用法

| **模块参数**：VectorParams1D |
| ------------------------------ |
| **类型：**字符向量             |
| **值：**'on' | 'off'         |
| **默认值：**'on'             | -->



<!-- ### 采样时间 — 采样间隔 inf （默认） | 标量 | 向量



指定仿真过程中 Constant 模块输出可以更改（例如，由于调整了**常量值**参数）的时间间隔。

默认值 inf 表示模块输出永不更改。此设置可通过避免重新计算模块输出，加快仿真和代码生成速度。

有关详细信息，请参阅 [指定采样时间](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/how-to-specify-the-sample-time.html)。

#### 编程用法

| **模块参数**：SampleTime |
| -------------------------- |
| **类型**：字符向量         |
| **值**：标量 \| 向量       |
| **默认值**：'inf'        | -->

### 信号属性



<!-- ### 输出最小值 — 范围检查的最小输出值 [] （默认） | 标量



将 Simulink 检查的输出范围的下限值指定为有限的双精度实数标量值。



**注意**

如果您指定总线对象作为此模块的数据类型，请不要为模块上的总线数据设置最小值。因为 Simulink 会忽略此设置。但请为指定作为数据类型的总线对象的总线元素设置最小值。有关总线元素的“最小值”参数的信息，请参阅 [Simulink.BusElement](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/simulink.buselement.html)。

Simulink 使用最小值执行下列操作：

- 某些模块的参数范围检查（请参阅[指定模块参数的最小值和最大值](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/checking-parameter-values.html)）。
- 仿真范围检查（请参阅[指定信号范围](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/signal-ranges.html)和[启用仿真范围检查](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/signal-ranges.html#brdikvq)）。
- 定点数据类型的自动定标。
- 从模型生成的代码的优化。此优化可删除算法代码，并影响某些仿真模式（如 SIL 或外部模式）的结果。有关详细信息，请参阅[Optimize using the specified minimum and maximum values](https://ww2.mathworks.cn/help/releases/R2022b/ecoder/ref/optimizeusingthespecifiedminimumandmaximumvalues.html) (Embedded Coder)。





**注意**

**输出最小值**不会饱和或剪切实际输出信号。请改用 [Saturation](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/saturation.html) 模块。



#### 编程用法

| **模块参数**：OutMin |
| ---------------------- |
| **类型**：字符向量     |
| **值**：标量           |
| **默认值**：'[ ]'    | -->



<!-- ### 输出最大值 — 范围检查的最大输出值 [] （默认） | 标量



将 Simulink 检查的输出范围的上限值指定为有限的双精度实数标量值。



**注意**

如果您指定总线对象作为此模块的数据类型，请不要为模块的总线数据设置最大值。因为 Simulink 会忽略此设置。但请为指定作为数据类型的总线对象的总线元素设置最大值。有关总线元素的“最大值”参数的信息，请参阅 [Simulink.BusElement](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/simulink.buselement.html)。

Simulink 使用最大值执行下列操作：

- 某些模块的参数范围检查（请参阅[指定模块参数的最小值和最大值](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/checking-parameter-values.html)）。
- 仿真范围检查（请参阅[指定信号范围](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/signal-ranges.html)和[启用仿真范围检查](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/signal-ranges.html#brdikvq)）。
- 定点数据类型的自动定标。
- 从模型生成的代码的优化。此优化可删除算法代码，并影响某些仿真模式（如 SIL 或外部模式）的结果。有关详细信息，请参阅[Optimize using the specified minimum and maximum values](https://ww2.mathworks.cn/help/releases/R2022b/ecoder/ref/optimizeusingthespecifiedminimumandmaximumvalues.html) (Embedded Coder)。





**注意**

**输出最大值**不会饱和或剪切实际输出信号。请改用 [Saturation](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/saturation.html) 模块。



#### 编程用法

| **模块参数**：OutMax |
| ---------------------- |
| **类型**：字符向量     |
| **值**：标量           |
| **默认值**：'[ ]'    | -->


<div class="details-box">
<details open>
<summary>输出数据类型 — 输出数据类型<div>“Inherit: internalRule” （默认） | “Inherit: backPropagation” | “double” | “float” | “int8” | “uint8” | “int16” | “uint16” | “int32” | “uint32” | “boolean” | “fixdt(1,16,0)” | “fixdt(1,16,2^0,0)” | “fixdt(1,16,1.0,0,0.0)”</div></summary>
</details>
<div class="details-content">

指定输出数据类型。该类型可以继承、直接指定或表示为数据类型对象。
<!-- 如 Simulink.NumericType。 -->

单击**显示数据类型帮助**按钮 <img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/Constant/Constant_button.png')" style="width: 80px; height: auto; vertical-align:middle; display:inline; margin:0;"> 以显示**数据类型帮助**，帮助您设置数据类型属性。  

</div>
</div>




  <!-- 有关详细信息，请参阅[使用数据类型助手指定数据类型]()。 -->

<!-- #### 编程用法

| **模块参数**：OutDataTypeStr                               |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值：**'Inherit: Inherit from 'Constant value'' | 'Inherit: Inherit via back propagation' | 'double' | 'single' | 'half' | 'int8' | 'uint8' | 'int16' | 'uint16' | 'int32' | 'uint32' | 'int64' | 'uint64' | 'boolean' | 'fixdt(1,16)' | 'fixdt(1,16,0)' | 'fixdt(1,16,2^0,0)' | 'Enum: <class name>' | 'Bus: <object name>' |
| **默认值：**'Inherit: Inherit from 'Constant value''       | -->



<!-- ### 锁定输出数据类型设置以防止被定点工具更改 — 防止定点工具覆盖输出数据类型 off （默认） | on



选择此参数可防止定点工具覆盖您在模块上指定的**输出**数据类型。有关详细信息，请参阅[Use Lock Output Data Type Setting](https://ww2.mathworks.cn/help/releases/R2022b/fixedpoint/ug/best-practices-for-using-the-fixed-point-tool-to-propose-data-types-for-your-simulink-model.html#br9an48) (Fixed-Point Designer)。

#### 编程用法

| **模块参数**：LockScale |
| ------------------------- |
| **类型：**字符向量        |
| **值：**'off' | 'on'    |
| **默认值：**'off'       | -->



<!-- ## 模块特性

| **数据类型**     | Boolean | bus | double | enumerated | fixed point | half | integer | single |
| ---------------- | ------------------------------------------------------------ |
| **直接馈通**     | 否                                                         |
| **多维信号**     | 是                                                         |
| **可变大小信号** | 否                                                         |
| **过零检测**     | 否                                                         | -->

## 版本历史记录

- 在 2026a 推出

## 限制信息

1. 暂不支持将向量参数解释为一维向量的复选框；  
2. 暂不支持自定义采样时间；  
3. 暂不支持输出的最大、最小值；  
4. 暂不支持部分设定的输出数据类型；  
5. 暂不支持锁定输出数据类型设置以防止被定点工具更改的复选框；  
6. 输出端口暂不支持 half、int64、uint64 和 bus 的数据类型。


<!-- ## 扩展功能



### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 Verilog 代码和 VHDL 代码。

HDL Coder™ 提供影响 HDL 实现和综合逻辑的额外配置选项。



**可调参数**

您可以在 Constant 模块中使用可调参数，用于 HDL 代码生成。有关详细信息，请参阅[Generate DUT Ports for Tunable Parameters](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/generate-code-for-tunable-parameters.html) (HDL Coder)。

**HDL 架构**

| 架构              | 参数                                                         | 描述                                                         |
| :---------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| “默认” “常量” | 无                                                           | 此实现生成 Constant 模块的值。                               |
| “逻辑值”        | 无                                                           | 默认情况下，此实现为信号中的每个位生成字符 'Z'。例如，对于一个 4 位信号，此实现将生成 'ZZZZ'。 |
| {'Value', 'Z'}  | 如果信号处于高阻抗状态，请使用此参数值。此实现为信号中的每个位生成字符 'Z'。例如，对于一个 4 位信号，此实现将生成 'ZZZZ'。 |                                                              |
| {'Value', 'X'}  | 如果信号处于未知状态，请使用此参数值。此实现为信号中的每个位生成字符 'X'。例如，对于一个 4 位信号，此实现将生成 'XXXX'。 |                                                              |

**HDL 模块属性**

| **ConstrainedOutputPipeline** | 通过移动设计中现有延迟的方式来放置在输出端的寄存器的数量。分布式流水线处理不会重新分发这些寄存器。默认值为 0。有关详细信息，请参阅[ConstrainedOutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#btp8gmp) (HDL Coder)。 |
| ----------------------------- | ------------------------------------------------------------ |
| **InputPipeline**             | 要在生成的代码中插入的输入流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 0。有关详细信息，请参阅[InputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-25) (HDL Coder)。 |
| **OutputPipeline**            | 要在生成的代码中插入的输出流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 0。有关详细信息，请参阅[OutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-26) (HDL Coder)。 |

**复数数据支持**

此模块支持复信号的代码生成。

**限制**



- “逻辑值”实现不支持 double 数据类型。如果为 double 类型的常量值指定此实现，则会出现代码生成错误。
- 对于**采样时间**，输入 -1。延迟平衡不支持 inf 采样时间。





### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。

## 版本历史记录

**在 R2006a 之前推出** -->

<!-- ## 另请参阅

[Enumerated Constant](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/enumeratedconstant.html) | [Simulink.Parameter](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/simulink.parameter.html) | [Simulink.BusElement](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/simulink.buselement.html)

### 主题

- [设置模块参数值](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/parameter-values-and-specification-methods.html)
- [使用 Simulink.Bus 对象数据类型指定总线属性](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/when-to-use-bus-objects.html)
- [指定总线元素的初始条件](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/specifying-initial-conditions-for-bus-signals.html)
- [从 MATLAB 结构体创建总线数组](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/combining-buses-into-an-array-of-buses.html#buxurn0-1) -->