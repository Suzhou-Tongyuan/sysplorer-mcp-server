# IntervalTest
---
&nbsp;

确定信号是否在指定区间中


**库：** Sysblock模块库 / LogicAndBitOperation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/IntervalTest/IntervalTest.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

如果输入介于**下限**和**上限**指定的值之间，IntervalTest 模块将输出 true (1)。如果输入在这些值的范围之外，模块将输出 false (0)。当输入等于**下限**或**上限**时，模块的输出取决于您是选中**左半闭区间**还是**右半闭区间**复选框。

## 示例

<!-- 暂无
[![Variable-Size Signal Length Adaptation](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink_features/win64/VariableSizeSignalLengthAdaptationExample_01.png)Variable-Size Signal Length AdaptationModel showing how to change the length of a signal over time.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/variable-size-signal-length-adaptation.html) -->

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/IntervalTest.mo">IntervalTest.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/IntervalTest/IntervalTest_ex.png')" style="width: 800px; transform: scale(0.8);">

### 示例说明

- SignalBuilder 模块：用于提供随时间变化的输入信号。在这个例子中，信号可以是正弦波或阶跃信号；
- IntervalTest 模块：用于检测输入信号是否在指定的区间内。当信号值在下界和上界之间时，输出 1（真）；
- Scope 模块：用于显示模型的输出。在这个例子中，它显示了区间测试的结果，即输入信号是否在指定的区间内。

## 端口

### 输入


###  
<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 向量 | 矩阵 | N 维数组</div></summary>
</details>
<div class="details-content">

输入信号，指定为标量、向量、矩阵或 N 维数组。

**限制：** 当输入信号为枚举类型时，**上限**和**下限**值必须具有相同的枚举类型。


**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | fixedPoint | enume

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>0 | 1</div></summary>
</details>
<div class="details-content">

指示输入值是否在指定区间内的输出信号。您可以将**输出数据类型**指定为 “boolean” 或 “Inherit: auto”。

**数据类型：** boolean

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>右半闭区间 — 包含上限值<div>on （默认） | off</div></summary>
</details>
<div class="details-content">

当选中此复选框时，**上限**包括在模块对其输出 true (1) 的区间中。

</div>
</div>



<!-- 暂无
#### 编程用法

| **模块参数**： IntervalClosedRight |
| ------------------------------------ |
| **类型：**字符向量                   |
| **值：**'on' | 'off'               |
| **默认值：**'on'                   | -->


<div class="details-box">
<details open>
<summary>上限 — 区间的上限<div>0.5 （默认） | 标量 | 向量 | 矩阵 | N 维数组</div></summary>
</details>
<div class="details-content">

模块对其输出 true (1) 的区间的上限值。

</div>
</div>


<!-- 暂无
#### 编程用法

| **模块参数**：uplimit                   |
| ----------------------------------------- |
| **类型：**字符向量                        |
| **值：** 标量 \| 向量 \| 矩阵 \| N 维数组 |
| **默认值：**'0.5'                       | -->


<div class="details-box">
<details open>
<summary>左半闭区间 — 包含下限值<div>on （默认） | off</div></summary>
</details>
<div class="details-content">

当选中此复选框时，**下限**包括在模块对其输出 true (1) 的区间中。

</div>
</div>


<!-- 暂无
#### 编程用法

| **模块参数**： IntervalClosedLeft |
| ----------------------------------- |
| **类型：**字符向量                  |
| **值：**'on' | 'off'              |
| **默认值：**'on'                  | -->


<div class="details-box">
<details open>
<summary>下限 — 区间的下限<div>-0.5 （默认） | 标量 | 向量 | 矩阵 | N 维数组</div></summary>
</details>
<div class="details-content">

模块对其输出 true (1) 的区间的下限值。

</div>
</div>




<!-- 暂无
#### 编程用法

| **模块参数**：lowlimit                  |
| ----------------------------------------- |
| **类型：**字符向量                        |
| **值：** 标量 \| 向量 \| 矩阵 \| N 维数组 |
| **默认值：**'-0.5'                      | -->


<div class="details-box">
<details open>
<summary>输出数据类型 — 输出数据类型<div>“boolean” （默认） | “Inherit: auto”</div></summary>
</details>
<div class="details-content">

将输出数据类型指定为 boolean 或 Inherit: auto。

</div>
</div>


<!-- 暂无
#### 编程用法

| **模块参数**：OutDataTypeStr |
| ------------------------------ |
| **类型：**字符向量             |
| **值：**'boolean' | 'uint8'  |
| **默认值：**'boolean'        | -->



<!-- 不确定
## 模块特性

| **数据类型**     | Boolean | double | enumerated | fixed point | integer | single |
| ---------------- | ------------------------------------------------------------ |
| **直接馈通**     | 是                                                         |
| **多维信号**     | 是                                                         |
| **可变大小信号** | 否                                                         |
| **过零检测**     | 否                                                         | -->


## 版本历史记录

- 在 2024b 之前推出

### 限制信息
 
输入信号暂不支持 int64 和 uint64 的数据类型，输出信号暂不支持 uint8 的数据类型。

<!-- 暂无
## 扩展功能



### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 Verilog 代码和 VHDL 代码。



HDL Coder™ 提供影响 HDL 实现和综合逻辑的额外配置选项。

**HDL 架构**

| 架构               | 描述                                                         |
| :----------------- | :----------------------------------------------------------- |
| “模块”（默认值） | 为子系统和子系统内的模块生成代码。                           |
| “BlackBox”       | 生成黑盒接口。生成的 HDL 代码仅包括子系统的输入/输出端口定义。因此，您可以在模型中使用子系统来生成与手动编写的现有 HDL 代码的接口。子系统的黑盒接口生成类似于没有时钟信号的 Model 模块接口生成。 |
| “无 HDL”         | 从生成的代码中删除子系统。您可以在仿真中使用子系统，但在 HDL 代码中将其视为“无操作”。 |

**黑盒接口自定义**

对于 “BlackBox” 架构，您可以自定义端口名称并设置外部组件接口的属性。请参阅[Customize Black Box or HDL Cosimulation Interface](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/customizing-the-generated-interface.html) (HDL Coder)。

**HDL 模块属性**

| 通用                          |                                                              |
| :---------------------------- | ------------------------------------------------------------ |
| **AdaptivePipelining**        | 基于综合工具、目标频率和乘法器字长的自动流水线插入。默认值为 “inherit”。另请参阅[AdaptivePipelining](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bve2wds-1) (HDL Coder)。 |
| **BalanceDelays**             | 检测沿一条路径引入的新延迟，并在其他路径上插入匹配的延迟。默认值为 “inherit”。另请参阅[BalanceDelays](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#btudq9e) (HDL Coder)。 |
| **ClockRatePipelining**       | 以较快的时钟频率而不是较慢的数据速率插入流水线寄存器。默认值为 “inherit”。另请参阅[ClockRatePipelining](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bveex_4-1) (HDL Coder)。 |
| **ConstrainedOutputPipeline** | 通过移动设计中现有延迟的方式来放置在输出端的寄存器的数量。分布式流水线处理不会重新分发这些寄存器。默认值为 0。有关详细信息，请参阅[ConstrainedOutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#btp8gmp) (HDL Coder)。 |
| **DistributedPipelining**     | 流水线寄存器分配或寄存器重定时。默认值为 “inherit”。另请参阅[DistributedPipelining](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-20) (HDL Coder)。 |
| **DSPStyle**                  | 乘法器映射的综合属性。默认值为“无”。另请参阅[DSPStyle](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bubc5wb-1) (HDL Coder)。 |
| **FlattenHierarchy**          | 从生成的 HDL 代码中删除子系统层次结构。默认值为 “inherit”。另请参阅[FlattenHierarchy](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#btdc8oq-1) (HDL Coder)。 |
| **InputPipeline**             | 要在生成的代码中插入的输入流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 0。有关详细信息，请参阅[InputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-25) (HDL Coder)。 |
| **OutputPipeline**            | 要在生成的代码中插入的输出流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 0。有关详细信息，请参阅[OutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-26) (HDL Coder)。 |
| **SharingFactor**             | 要映射到单个共享资源的功能等效的资源的数量。默认值为 0。另请参阅[Resource Sharing](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/resource-sharing.html) (HDL Coder)。 |
| **StreamingFactor**           | 并行数据路径或向量的数量，这些路径或向量通过时间多路复用的方式变换为串行标量数据路径。默认值为 0，表示实现完全并行的数据路径。另请参阅[Streaming](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/streaming.html) (HDL Coder)。 |

如果此模块不是 DUT，将忽略**目标设定**选项卡中的模块属性设置。在 HDL 工作流顾问中，如果您使用 **IP 核生成**工作流，这些目标设定模块属性值将随模型一起保存。如果您使用 hdlset_param 指定这些目标设定模块属性值，则当您打开 HDL 工作流顾问时，系统将使用对应的值填充这些字段。

| 目标设定                                 |                                                              |
| :--------------------------------------- | ------------------------------------------------------------ |
| **AdditionalTargetInterfaces**           | 附加目标接口，指定为字符向量。要在模型上保存此模块属性，请在 **IP 核生成**工作流的**设置目标接口**任务中，对应于您要添加更多接口的 DUT 端口，选择 **Add more...**。然后，您可以在“添加新目标接口”对话框中添加更多接口。指定接口类型、附加接口数量以及每个附加接口的唯一名称。值：''（默认值）| 字符向量元胞数组示例：'{{'AXI4-Stream','InterfaceID','AXI4-Stream1'}}' |
| **ProcessorFPGASynchronization**         | 处理器/FPGA 同步模式，指定为字符向量。要在模型上保存此模块属性，请在 **IP 核生成**工作流的**设置目标接口**任务中指定**处理器/FPGA 同步**。值：Free running（默认值）| Coprocessing - blocking示例：'Free running' |
| **TestPointMapping**                     | 要在模型上保存此模块属性，请在 **IP 核生成**工作流的**设置目标接口**任务中指定测试点端口到目标平台接口的映射。值：''（默认值）| 字符向量元胞数组示例：'{{'TestPoint','AXI4-Lite','x"108"'}}' |
| **TunableParameterMapping**              | 要在模型上保存此模块属性，请在 **IP 核生成**工作流的**设置目标接口**任务中指定可调参数端口到目标平台接口的映射。值：''（默认值）| 字符向量元胞数组示例：'{{'myParam','AXI4-Lite','x"108"'}}' |
| **AXI4RegisterReadback**                 | 要在模型上保存此模块属性，请在 **IP 核生成**工作流的**生成 RTL 代码和 IP 核**任务中指定是否对 AXI4 从属站写寄存器启用读回。要了解详细信息，请参阅[Model Design for AXI4 Slave Interface Generation](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/model-design-for-axi4-slave-interface-generation.html) (HDL Coder)。值：'off'（默认值）| 'on' |
| **AXI4SlaveIDWidth**                     | 要在模型上保存此模块属性，请使用 **IP 核生成**工作流的**生成 RTL 代码和 IP 核**任务中的 **AXI4 从属 ID 宽度**设置，指定要将 DUT IP 核连接到的 AXI 管理器接口的数量。要了解详细信息，请参阅[Define Multiple AXI Master Interfaces in Reference Designs to access DUT AXI4 Slave Interface](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/define-multiple-axi-master-interfaces-in-reference-designs-to-access-dut-axi4-slave-interface-1.html) (HDL Coder)。值：'off'（默认值）| 'on' |
| **AXI4SlavePortToPipelineRegisterRatio** | 要在模型上保存此模块属性，请使用 **IP 核生成**工作流的**生成 RTL 代码和 IP 核**任务中的 **AXI4 从属站端口与流水线寄存器的比率**设置，指定要为其插入流水线寄存器的 AXI4 从属端口的数量。要了解详细信息，请参阅[Model Design for AXI4 Slave Interface Generation](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/model-design-for-axi4-slave-interface-generation.html) (HDL Coder)。值：'off'（默认值）| 'on' |
| **GenerateDefaultAXI4Slave**             | 要在模型上保存此模块属性，请在 **IP 核生成**工作流的**生成 RTL 代码和 IP 核**任务中指定是否要禁用默认 AXI4 从属站接口的生成。值：'on'（默认值）| 'off' |
| **IPCoreAdditionalFiles**                | 设计中黑盒的 Verilog® 或 VHDL® 文件。指定每个文件的完整路径，并用分号 (;) 分隔各文件名。您可以在 HDL 工作流顾问的**其他源文件**字段中设置此属性。值：''（默认值）| 字符向量示例：'C:\myprojfiles\led_blinking_file1.vhd;C:\myprojfiles\led_blinking_file2.vhd;' |
| **IPCoreName**                           | IP 核名称，指定为字符向量。您可以在 HDL 工作流顾问的 **IP 核名称**字段中设置此属性。如果将此属性设置为默认值，HDL 工作流顾问将基于 DUT 的名称构造 IP 核名称。值：''（默认值）| 字符向量示例：'my_model_name' |
| **IPCoreVersion**                        | IP 核版本号，指定为字符向量。您可以在 HDL 工作流顾问的 **IP 核版本**字段中设置此属性。如果此属性设置为默认值，则 HDL 工作流顾问将设置 IP 核版本。值：''（默认值）| 字符向量示例：'1.3' |
| **IPDataCaptureBufferSize**              | FPGA 数据采集缓冲区大小，指定为字符向量。当在 FPGA 上运行时，请使用 FPGA 数据采集来观察设计中的信号。缓冲区大小的值为 128*2^n，其中 n 是整数。默认情况下，缓冲区大小为 128 (n=0)。n 的最大值是 13，即缓冲区大小的最大值是 1048576 (=128*2^13)。值：''（默认值）| 字符向量示例：'1.3' |



### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。

## 版本历史记录

**在 R2006a 之前推出** -->


## 另请参阅

[IntervalTestDynamic](IntervalTestDynamic.html)