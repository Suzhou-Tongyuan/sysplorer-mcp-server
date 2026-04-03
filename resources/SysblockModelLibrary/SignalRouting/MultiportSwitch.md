# MultiportSwitch
---
基于控制信号选择输出信号

**库：** Sysblock模块库 / SignalRouting

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/MultiportSwitch/MultiportSwitch.png')" style="width: 150px; height: auto; transform: scale(1);">

## 描述

MultiportSwitch 模块用于确定将多个模块输入中的哪一个传递给输出。此模块根据第一个输入的值来确定选择哪个输入。第一个输入是控制输入，其余输入是数据输入。控制输入的值确定将哪个数据输入传递给输出。

下表概述了此模块如何解释控制输入，以及如何确定传递给输出的数据输入。

<!-- | 控制输入               | 截断                             | 数据端口顺序的设置                               | 仿真过程中的模块行为 |                                               |
| :--------------------- | :------------------------------- | :----------------------------------------------- | :------------------- | --------------------------------------------- |
| 选择数据输入的索引方式 | 超出范围的情况                   |                                                  |                      |                                               |
| 整数值                 | 无                               | “从 0 开始连续”                                | 从零开始进行索引     | 控制输入小于 0 或大于数据输入数减 1。       |
| “从 1 开始连续”      | 从一开始进行索引                 | 控制输入小于 1 或大于数据输入数。              |                      |                                               |
| “指定索引”           | 按用户指定进行索引               | 控制输入与任何指定的数据端口索引均不对应。       |                      |                                               |
| 非整数值               | 模块通过向零舍入将值截断为整数。 | “从 0 开始连续”                                | 从零开始进行索引     | 截断的控制输入小于 0 或大于数据输入数减 1。 |
| “从 1 开始连续”      | 从一开始进行索引                 | 截断的控制输入小于 1 或大于数据输入数。        |                      |                                               |
| “指定索引”           | 按用户指定进行索引               | 截断的控制输入与任何指定的数据端口索引均不对应。 |                      |                                               | -->

<table border="1">
  <tr>
    <th rowspan="2">控制输入</th>
    <th rowspan="2">截断</th>
    <th colspan="2">数据端口顺序的设置</th>
    <th rowspan="2">超出范围的情况</th>
  </tr>
  <tr>
    <th>选择数据输入的索引方式</th>
    <th>仿真过程中的模块行为</th>
  </tr>
  <tr>
    <td rowspan="3">整数值</td>
    <td rowspan="3">无</td>
    <td>"从0开始连续"</td>
    <td>从零开始进行索引</td>
    <td>控制输入小于0或大于数据输入数减1。</td>
  </tr>
  <tr>
    <td>"从1开始连续"</td>
    <td>从一开始进行索引</td>
    <td>控制输入小于1或大于数据输入数。</td>
  </tr>
  <tr>
    <td>"指定索引"</td>
    <td>按用户指定进行索引</td>
    <td>控制输入与任何指定的数据端口索引均不对应。</td>
  </tr>
  <tr>
    <td rowspan="3">非整数值</td>
    <td rowspan="3">模块通过向零舍入将值截断为整数。</td>
    <td>"从0开始连续"</td>
    <td>从零开始进行索引</td>
    <td>截断的控制输入小于0或大于数据输入数减1。</td>
  </tr>
  <tr>
    <td>"从1开始连续"</td>
    <td>从一开始进行索引</td>
    <td>截断的控制输入小于1或大于数据输入数。</td>
  </tr>
  <tr>
    <td>"指定索引"</td>
    <td>按用户指定进行索引</td>
    <td>截断的控制输入与任何指定的数据端口索引均不对应。</td>
  </tr>
</table>


<!-- 有关此模块如何处理超出范围的情况的信息，请参阅[模块如何处理超出范围的控制输入](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/multiportswitch.html#bsgs21t)。 -->

<!-- ### 配置为 Index Vector 模块的 Multiport Switch



[Index Vector](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/indexvector.html) 是特殊配置的 Multiport Switch 模块，需要指定一个数据输入，控制输入从 0 开始。模块输出是其索引与控制输入匹配的输入向量的元素。例如，如果输入向量为 [18 15 17 10]，控制输入为 3，则与索引 3（从 0 开始）匹配的元素为 10，它将成为输出值。

要将 Multiport Switch 模块配置为 Index Vector 模块，请将**数据端口数量**设置为 “1” 且**数据端口顺序**设置为“从 0 开始连续”。 -->

<!-- ### 模块如何处理超出范围的控制输入

对于整数值小于 intmax(‘int32’) 的输入，当此值与任何数据端口索引均不匹配时，即说明输入超出了范围。对于非整数值控制输入，当*截断*的值与任何数据端口索引均不匹配时，即说明输入超出了范围。在这两种情况下，模块行为均取决于**默认情况数据端口**和**默认情况诊断**的设置。



**注意**

如果控制输入大于 intmax(‘int32’)，模块会将输入值绕回为整数。 -->

<!-- **仿真行为**

以下行为仅适用于模型仿真。

| 默认情况数据端口                                             | 默认情况诊断                                            |                                                 |                      |
| :----------------------------------------------------------- | :------------------------------------------------------ | :---------------------------------------------- | -------------------- |
| 无                                                           | 警告                                                    | 错误                                            |                      |
| “最后一个数据端口”![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/multiport_switch_last_data_port_icon.png) | 使用最后一个数据端口，不报告任何警告或错误。            | 使用最后一个数据端口并报告警告消息。            | 报告错误并停止仿真。 |
| “附加数据端口”![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/multiport_switch_additional_data_port_icon.png) | 使用带有 * 标签的其他数据端口，不报告任何警告或错误。 | 使用带有 * 标签的其他数据端口并报告警告消息。 | 报告错误并停止仿真。 | -->

<!-- **代码生成行为**

以下行为适用于模型的代码生成。

| 默认情况数据端口                                             | 默认情况诊断                      |                                   |                                   |
| :----------------------------------------------------------- | :-------------------------------- | :-------------------------------- | --------------------------------- |
| 无                                                           | 警告                              | 错误                              |                                   |
| “最后一个数据端口”![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/multiport_switch_last_data_port_icon.png) | 使用最后一个数据端口。            | 使用最后一个数据端口。            | 使用最后一个数据端口。            |
| “附加数据端口”![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/multiport_switch_additional_data_port_icon.png) | 使用带有 * 标签的其他数据端口。 | 使用带有 * 标签的其他数据端口。 | 使用带有 * 标签的其他数据端口。 | -->

### 使用具有不同维度的数据输入

如果两个信号具有不同数量的维度或不同的维度长度，您可以将这两个信号用作 MultiportSwitch 模块的数据输入。在模块对话框中，选择参数**允许不同数据输入大小**。在此例中，模块的输出是大小可变信号。如果您不选择此参数，模块将生成错误。

<!-- 有关该参数的详细信息，请参阅[允许不同数据输入大小(产生可变大小的输出信号), Allow different data input sizes (Results in variable-size output signal)允许不同数据输入大小(产生可变大小的输出信号)Allow different data input sizes (Results in variable-size output signal)](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/multiportswitch.html#f7-891602_sep_br57goc-57)。有关大小可变信号的详细信息，请参阅[可变大小信号基础知识](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/variable-size-signal-basics.html)。 -->

### 确定模块行为的规则

您可以使用**数据端口数量**指定数据输入的数目。

- 如果将**数据端口数量**设置为 1，则模块相当于一个*索引选择器*或*索引向量*，而不是一个 MultiportSwitch 模块；
<!-- 有关详细信息，请参阅[配置为 Index Vector 模块的 Multiport Switch](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/multiportswitch.html#bukl725)。 -->
- 如果将**数据端口数量**设置为大于 1 的整数，模块则相当于一个 MultiportSwitch 模块。模块输出是与控制输入值对应的数据输入。如果数据输入中至少有一个是向量，模块输出即为向量。在这种情况下，模块会将任何标量输入都扩展为向量；
- 如果所有数据输入都为标量，则输出为标量。

<!-- ### 枚举控制端口的参数设置原则

当 Multiport Switch 模块上的控制端口为枚举类型时，请遵循以下原则：

| 情况                                                         | 操作                                                         | 原理说明                                             |
| :----------------------------------------------------------- | :----------------------------------------------------------- | :--------------------------------------------------- |
| 枚举类型包含的值代表无效、超出范围或未初始化的值。           | 将**数据端口顺序**设置为“指定索引”。将**数据端口索引**设置为针对最后一个数据端口使用此值。将**默认情况数据端口**设置为“最后一个数据端口”。 | 此模块配置用于处理枚举类型显式表示的无效值。         |
| 枚举类型仅包含有效的枚举值。但是，数据输入端口可以获得无效的枚举类型值。 | 将**默认情况数据端口**设置为“附加数据端口”。               | 此模块配置用于处理枚举类型未显式表示的无效值。       |
| 枚举类型仅包含有效的枚举值。数据输入端口永远不会获得无效的枚举类型值。 | 将**默认情况数据端口**设置为“最后一个数据端口”。将**默认情况诊断**设置为“无”。 | 此模块配置可避免不必要的诊断操作。                   |
| 模块没有为枚举类型的每个值提供一个数据输入端口。             | 将**默认情况数据端口**设置为“附加数据端口”。               | 此模块配置用于处理没有数据输入端口的枚举值和无效值。 | -->

### 限制

如果 MultiportSwitch 模块的数据输入是总线，两个总线的元素名称必须相同。使用相同的元素名称可以确保输出总线具有相同的元素名称，而不管模块选择了哪些输入总线。

<!-- 要确保您的模型满足此要求，请使用总线对象定义总线并将**元素名称不匹配**诊断设置为“错误”。有关详细信息，请参阅[模型配置参数：连接诊断](https://ww2.mathworks.cn/help/releases/R2022b/simulink/gui/diagnostics-pane-connectivity.html)。
- 对于总线数组，**数据端口数量**必须设置为 2 或更大的值。 -->

## 示例

<!-- [![Noncontiguous Values for Data Port Indices of Multiport Switch Block](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink/win64/NoncontiguousDataPortIndicesMultiportSwitchBlockExample_01.png)Noncontiguous Values for Data Port Indices of Multiport Switch BlockUse a Multiport Switch block that specifies noncontiguous integer values for data ports.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/noncontiguous-values-for-data-port-indices-of-multiport-switch-block.html)

[![Zero-Based Indexing for Multiport Switch Data Ports](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink/win64/ZeroBasedIndexingMultiportSwitchBlockExample_01.png)Zero-Based Indexing for Multiport Switch Data PortsThe sf_aircontrol model uses a Multiport Switch block in the Physical Plant subsystem.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/zerobased-indexing-for-multiport-switch-data-ports.html)

[![One-Based Indexing for Multiport Switch Data Ports](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink/win64/OneBasedIndexingMultiportSwitchBlockExample_01.png)One-Based Indexing for Multiport Switch Data PortsThe sf_semantics_hotel_checkin model uses a Multiport Switch block.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/onebased-indexing-for-multiport-switch-data-ports.html)

[![Enumerated Names for Data Port Indices of the Multiport Switch Block](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink/win64/EnumeratedDataPortIndicesMultiportSwitchBlockExample_01.png)Enumerated Names for Data Port Indices of the Multiport Switch BlockThe sldemo_fuelsys model uses a Multiport Switch block in the fuel_rate_control/fuel_calc/feedforward_fuel_rate subsystem.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/enumerated-names-for-data-port-indices-of-multiport-switch.html) -->

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/MultiportSwitch.mo">MultiportSwitch.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/MultiportSwitch/MultiportSwitch_ex.png')" style="width: 600px; transform: scale(0.8);">

### 示例说明

- MultiportSwitch 模块：根据控制信号从多个输入信号中选择一个输出。控制信号决定了哪个数据输入信号被传递到输出。如果控制信号是整数，它将作为索引来选择数据输入端口；
- Step 模块：提供不同的步变信号作为 Multiport Switch 的数据输入和控制信号；
- Scope 模块：用于显示模型的输出结果，即根据控制信号选择的输入信号。

## 端口

### 输入

<div class="details-box">
<details open>
<summary>controlSignal — 控制信号<div>标量</div></summary>
</details>
<div class="details-content">

控制信号可以是 Sysblock 支持的任何数据类型，包括定点和枚举类型。当控制输入不是整数值时，模块通过向零舍入将值截断为整数。

<!-- 有关枚举类型的控制信号的信息，请参阅[枚举控制端口的参数设置原则](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/multiportswitch.html#btiipg7-5)。

有关此模块如何处理超出范围的情况的信息，请参阅[模块如何处理超出范围的控制输入](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/multiportswitch.html#bsgs21t)。 -->

**限制：**

- 如果控制信号为数值，则控制信号不能为复数；
- 如果控制信号为枚举信号，模块将使用基础整数值来选择数据端口；
- 如果基础整数没有对应的数据端口，将出现错误。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | enum

</div>
</div>



<div class="details-box">
<details open>
<summary>u1 — 第一个数据输入<div>标量 | 向量 | 矩阵 | N 维数组</div></summary>
</details>
<div class="details-content">

第一个数据输入，指定为标量、向量、矩阵或 N 维数组。所有数据信号可以是 Sysblock 支持的任何数据类型。

- 如果所有数据输入都为标量，则输出为标量；
- 如果数据输入中至少有一个是向量，模块输出即为向量。在这种情况下，模块会将任何标量输入都扩展为向量；
- 如果任何两个非标量信号具有不同维度数量或不同维度长度，请选中**允许不同数据输入大小**复选框；
<!-- 有关详细信息，请参阅[使用具有不同维度的数据输入]()。 -->
- 如果有任何数据信号为枚举类型，则所有其他信号也必须为相同的枚举类型。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | enum

</div>
</div>



<div class="details-box">
<details open>
<summary>u2 — 第二个数据输入<div>标量 | 向量 | 矩阵 | N 维数组</div></summary>
</details>
<div class="details-content">

第二个数据输入，指定为标量、向量、矩阵或 N 维数组。所有数据信号可以是 Sysblock 支持的任何数据类型。

- 如果所有数据输入都为标量，则输出为标量；
- 如果数据输入中至少有一个是向量，模块输出即为向量。在这种情况下，模块会将任何标量输入都扩展为向量；
- 如果任何两个非标量信号具有不同维度数量或不同维度长度，请选中**允许不同数据输入大小**复选框；
  <!-- 有关详细信息，请参阅[使用具有不同维度的数据输入]()。 -->
- 如果有任何数据信号为枚举类型，则所有其他信号也必须为相同的枚举类型。

**依存关系：**要启用此端口，请将**数据端口数量**设置为大于 1 的整数。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | enum

</div>
</div>




<div class="details-box">
<details open>
<summary>uN — 第 N 个数据输入<div>标量 | 向量 | 矩阵 | N 维数组</div></summary>
</details>
<div class="details-content">

第 N 个数据输入，指定为标量、向量、矩阵或 N 维数组。所有数据信号可以是 Sysblock 支持的任何数据类型。

- 如果所有数据输入都为标量，则输出为标量；
- 如果数据输入中至少有一个是向量，模块输出即为向量。在这种情况下，模块会将任何标量输入都扩展为向量；
- 如果任何两个非标量信号具有不同维度数量或不同维度长度，请选中**允许不同数据输入大小**复选框；
 
<!-- 有关详细信息，请参阅[使用具有不同维度的数据输入]()。 -->

- 如果有任何数据信号为枚举类型，则所有其他信号也必须为相同的枚举类型。

**依存关系：**要启用第 **N** 个输入端口，请将**数据端口数量**设置为大于或等于 N 的整数值。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | enum


</div>
</div>



<!-- ### * — 用于超出范围的输入的数据端口 标量 | 向量 | 矩阵 | N 维数组



用于超出范围的控制信号输入的输入数据端口，指定为标量、向量、矩阵或 N 维数组。所有数据信号可以是 Sysblock 支持的任何数据类型。如果有任何数据信号为枚举类型，则所有其他信号也必须为相同的枚举类型。如果任何两个信号具有不同维度数量或不同维度长度，请选中**允许不同数据输入大小**复选框。有关详细信息，请参阅[使用具有不同维度的数据输入]()。

#### 依存关系

要为超出范围的控制信号输入创建一个附加数据端口，请将**默认情况数据端口**设置为“附加数据端口”。如果将**默认情况数据端口**设置为“最后一个数据端口”，则当控制信号值与任何数据端口索引都不匹配时，模块将使用最后一个数据端口进行输出。

**数据类型：** single | double | half | int8 | int16 | int32 | int64 | uint8 | uint16 | uint32 | uint64 | Boolean | fixed point | enumerated | bus | image -->

### 输出

<div class="details-box">
<details open>
<summary>y — 所选数据输入，基于控制信号值<div>标量 | 向量 | 矩阵 | N 维数组</div></summary>
</details>
<div class="details-content">

模块输出根据控制信号值选择的数据输入之一。输出的维度与对应的数据输入相同。输出数据类型是需要最大内存空间的输入端口的数据类型。当您选中**允许不同数据输入大小**复选框时，模块的输出是可变大小信号。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | enum

</div>
</div>




## 参数



### 主要


<div class="details-box">
<details open>
<summary>数据端口顺序 — 数据输入端口的排序类型<div>“从 1 开始连续” | “从 0 开始连续” | “指定索引”</div></summary>
</details>
<div class="details-content">

指定数据输入端口的排序类型。

- “从 0 开始连续” - 模块使用从 0 开始的索引方式为连续数据端口排序。这是 IndexVector 模块的默认值；
- “从 1 开始连续” - 模块使用从 1 开始的索引方式为连续数据端口排序。这是 MultiportSwitch 模块的默认值；
- “指定索引” - 模块使用不连续的索引方式为数据端口排序。

::: tip 提示 
- 当控制端口为枚举类型时，请选择“指定索引”；

- 如果选择“从 0 开始连续”或“从 1 开始连续”，请确认控制端口不是枚举类型。此配置已弃用，如果使用将会生成错误。您可以在模型上运行升级顾问，将此配置中的每个 MultiportSwitch 模块替换为显式指定数据端口索引的模块；
<!-- 请参阅[模型升级](https://ww2.mathworks.cn/help/releases/R2022b/simulink/model-upgrades.html)。 -->

- 在仿真或代码生成中，应避免出现模块包含未使用的数据端口的情况。当控制端口为定点或内置数据类型时，请确认所有数据端口索引都可用该类型表示。否则，将发生以下模块行为：

  | 如果模块具有未使用的数据端口且数据端口顺序为： | 该模块产生： |
  | :--------------------------------------------- | :----------- |
  | “从 0 开始连续”或“从 1 开始连续”           | 警告         |
  | “指定索引”                                   | 错误         |

:::

**依存关系：**

- 选择“从 0 开始连续”或“从 1 开始连续”将启用**数据端口数量**参数；

- 选择“指定索引”将启用**数据端口索引**参数。

</div>
</div>




<!-- #### 编程用法

| **模块参数**：DataPortOrder                                |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值：**'Zero-based contiguous' | 'One-based contiguous' | 'Specify indices' |
| **默认值：**'One-based contiguous' (Multiport Switch) 'Zero-based contiguous' (Index Vector) | -->


<div class="details-box">
<details open>
<summary>数据端口数量 — 数据输入端口的个数<div>1 | 3 | 在 1 和 65535 之间的整数</div></summary>
</details>
<div class="details-content">

指定模块的数据输入端口数。输入端口的总数是您指定的数量加 1（用于控制信号输入端口）；如果您将**默认情况数据端口**设置为“附加数据端口”，则还要再加 1（用于额外的输入端口）。

**依存关系：**要启用此参数，请将**数据端口顺序**设置为“从 0 开始连续”或“从 1 开始连续”。

</div>
</div>




<!-- #### 编程用法

| **模块参数**：Inputs                                    |
| --------------------------------------------------------- |
| **类型：**字符向量                                        |
| **值：**1 和 65536 之间的整数                             |
| **默认值：**'3' (Multiport Switch) '1' (Index Vector) | -->


<div class="details-box">
<details open>
<summary>数据端口索引 — 数据端口的索引数组<div>{1,2,3} （默认） | 索引数组</div></summary>
</details>
<div class="details-content">

为数据端口指定索引数组。模块图标将发生变化以匹配您指定的数据端口索引。

::: tip 提示 
- 要指定与枚举类型的所有值对应的索引数组，请输入类型的名称；

  例如，如果 MyColors 是枚举类型的名称，则 MyColors 是有效条目。

- 要输入枚举类型的特定值，请使用 type_name.enumerated_name 格式。请不要输入基础整数值；

  例如，{MyColors.Red, MyColors.Green, MyColors.Blue} 就是有效的输入。

- 要指示多个值映射到一个数据端口，请使用方括号；

  例如，以下两个输入均有效：

  - {MyColors.Red, MyColors.Green, [MyColors.Blue, MyColors.Yellow]}
  - {[3,5],0,18}

- 如果控制端口为定点或内置数据类型，**数据端口索引**的值必须能用该类型表示。否则，编译时将出现错误，提醒您存在未使用的数据端口；

- 如果控制端口为枚举数据类型，**数据端口索引**的值必须为该类型的枚举值；

- 如果**数据端口索引**包含枚举类型的值，控制端口必须为该数据类型。
:::



**依存关系：**要启用此参数，请将**数据端口顺序**设置为“指定索引”。

</div>
</div>



<!-- #### 编程用法

| **模块参数**：DataPortIndices |
| ------------------------------- |
| **类型：**字符向量              |
| **值：**索引数组                |
| **默认值：**'{1,2,3}'         | -->


<div class="details-box">
<details open>
<summary>默认情况数据端口 — 用于超出范围的输入的端口<div>“最后一个数据端口” （默认） | “附加数据端口”</div></summary>
</details>
<div class="details-content">

指定对于超出范围的输入，是使用最后一个数据端口还是使用其他端口。端口名称旁的星号 (*) 表示控制端口值不匹配任何数据端口索引时模块将使用的端口。

- “最后一个数据端口” - 当控制端口值与任何数据端口索引均不匹配时，模块将使用最后一个数据端口进行输出；
- “附加数据端口” - 当控制端口值与任何数据端口索引均不匹配时，模块将使用其他数据端口进行输出。

::: tip 提示 
如果将此参数设置为“附加数据端口”且**数据端口数量**为 “3”，则模块上的输入端口数为 5。第一个输入是控制端口，后面三个输入为数据端口，第五个输入是用于超出范围的输入的默认端口。
:::

</div>
</div>






<!-- #### 编程用法

| **模块参数**：DataPortForDefault                  |
| --------------------------------------------------- |
| **类型：**字符向量                                  |
| **值：**'Last data port' | 'Additional data port' |
| **默认值：**'Last data port'                      | -->



<!-- ### 默认情况诊断 — 控制端口值与数据端口索引不匹配时的诊断操作 “错误” （默认） | “警告” | “无”



指定当控制端口值与任何端口索引均不匹配时要采取的诊断操作。

- “无” - 不产生任何响应。
- “警告” - 显示警告并继续进行仿真。
- “错误” - 终止仿真并显示错误。在这种情况下，**默认情况数据端口**只用于代码生成，而不用于仿真。

有关详细信息，请参阅[模块如何处理超出范围的控制输入](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/multiportswitch.html#bsgs21t)。

#### 编程用法

| **模块参数**：DiagnosticForDefault   |
| -------------------------------------- |
| **类型：**字符向量                     |
| **值：**'None' | 'Warning' | 'Error' |
| **默认值：**'Error'                  | -->



<!-- ### 采样时间 — -1 以外的采样时间值 -1 （默认） | 标量 | 向量



将采样时间指定为 -1 以外的值。有关详细信息，请参阅[指定采样时间](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/how-to-specify-the-sample-time.html)。

#### 依存关系

此参数不可见，除非将其显式设置为 -1 以外的值。要了解详细信息，请参阅[不建议设置采样时间的模块](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/sampletimehiding.html)。

#### 编程用法

| **模块参数：**SampleTime     |
| ------------------------------ |
| **类型：**字符串标量或字符向量 |
| **默认值：**"-1"             | -->

### 信号属性



<!-- ### 要求所有数据端口输入具有相同的数据类型 — 要求所有输入具有相同的数据类型 off （默认） | on



选中此复选框将要求所有数据输入端口具有相同的数据类型。清除此复选框时，模块允许数据端口输入具有不同数据类型。

#### 编程用法

| **模块参数**：InputSameDT |
| --------------------------- |
| **类型：**字符向量          |
| **值：**'off' | 'on'      |
| **默认值：**'off'         | -->



<!-- ### 输出最小值 — 范围检查的最小输出值 [] （默认） | 标量



Simulink 检查的输出范围的下限值。

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
| **值**：'[ ]'\| 标量 |
| **默认值**：'[ ]'    | -->



<!-- ### 输出最大值 — 范围检查的最大输出值 [] （默认） | 标量



Simulink 检查的输出范围的上限值。

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
| **值**：'[ ]'\| 标量 |
| **默认值**：'[ ]'    | -->


<div class="details-box">
<details open>
<summary>输出数据类型 — 输出数据类型<div>“Inherit: internalRule” （默认） | “Inherit: backPropagation” | “Inherit: sameAsFirstInput” | “double” | “float” | “int8” | “uint8” | “int16” | “uint16” | “int32” | “uint32” | “boolean”</div></summary>
</details>
<div class="details-content">

为输出选择数据类型。该类型可以继承、直接指定或表示为数据类型对象，如 Sysblock.NumericType。

当您选择继承的选项时，模块的行为如下所示：

- “Inherit: internalRule” - Sysblock 在考虑嵌入式目标硬件的属性的同时，会选择相应的数据类型来平衡数值准确性、性能和生成的代码大小。如果更改了嵌入式目标的设置，则依内部规则选择的数据类型可能会发生变化。有时软件不能同时满足优化代码效率和保证数值准确性这两个需求。如果内部规则不能满足您对数值准确性或性能的特定需求，请使用下列选项之一：
  - 显式指定输出数据类型；
  - 显式指定默认数据类型（例如 fixdt(1,32,16)），然后使用定点工具为您的模型提供数据类型建议；
  <!-- 有关详细信息，请参阅 [fxptdlg](https://ww2.mathworks.cn/help/releases/R2022b/fixedpoint/ref/fxptdlg.html) (Fixed-Point Designer)。 -->
  <!-- - 要指定您自己的继承规则，请使用 “Inherit: backPropagation”，然后使用 [Data Type Propagation](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/datatypepropagation.html) 模块。有关如何使用此模块的示例说明，请参阅 Signal Attributes 模块库中的 Data Type Propagation Examples 模块。 -->
- “Inherit: backPropagation” - 使用驱动模块的数据类型；
- “Inherit: sameAsFirstInput” - 使用第一个数据输入端口的数据类型。

</div>
</div>






<!-- #### 编程用法

| **模块参数**：OutDataTypeStr                               |
| ------------------------------------------------------------ |
| **类型**：字符向量                                           |
| **值**：'Inherit: Inherit via internal rule | 'Inherit: Inherit via back propagation' | 'Inherit: Same as first input' | 'double' | 'single' | 'half' | 'int8' | 'uint8' | 'int16' | 'uint16' | 'int32' | 'uint32' | 'int64' | 'uint64' | 'fixdt(1,16)' | 'fixdt(1,16,0)' | 'fixdt(1,16,2^0,0)' | 'string' | Simulink.ImageType(480,640,3) | '<data type expression>' |
| **默认值**：'Inherit: Inherit via internal rule'           | -->



<!-- ### 锁定输出数据类型设置以防止被定点工具更改 — 防止定点工具覆盖数据类型 off （默认） | on



选中此选项将锁定此模块的输出数据类型设置，从而防止通过定点工具和定点顾问进行更改。有关详细信息，请参阅[Use Lock Output Data Type Setting](https://ww2.mathworks.cn/help/releases/R2022b/fixedpoint/ug/best-practices-for-using-the-fixed-point-tool-to-propose-data-types-for-your-simulink-model.html#br9an48) (Fixed-Point Designer)。

#### 编程用法

| **模块参数**：LockScale |
| ------------------------- |
| **类型**：字符向量        |
| **值**：'off' | 'on'  |
| **默认值**：'off'       | -->



<!-- ### 整数舍入模式 — 指定定点运算的舍入模式 “向下” （默认） | “向上” | “收敛” | “最邻近值” | “舍入” | “最简” | “零”



选择下列舍入模式之一。

- “向上”

  将正值和负值朝正无穷方向舍入。等同于 MATLAB® ceil 函数。

- “收敛”

  将数值舍入到最邻近的可表示值。如果出现结值，则舍入到最邻近的偶数整数。等同于 Fixed-Point Designer™ convergent 函数。

- “向下”

  将正值和负值朝负无穷方向舍入。等同于 MATLAB floor 函数。

- “最邻近值”

  将数值舍入到最邻近的可表示值。如果出现结值，则朝正无穷方向舍入。等同于 Fixed-Point Designer nearest 函数。

- “舍入”

  将数值舍入到最邻近的可表示值。如果出现结值，则将正数朝正无穷方向舍入，将负数朝负无穷方向舍入。等同于 Fixed-Point Designer round 函数。

- “最简”

  自动选择是向负无穷大方向舍入还是向零舍入，以生成尽可能有效的舍入代码。

- “零”

  将数值向零舍入。等同于 MATLAB fix 函数。



#### 编程用法

| **模块参数**：RndMeth                                      |
| ------------------------------------------------------------ |
| **类型**：字符向量                                           |
| **值**：'Ceiling' | 'Convergent' | 'Floor' | 'Nearest' | 'Round' | 'Simplest' | 'Zero' |
| **默认值**：'Floor'                                        |

#### 另请参阅

有关详细信息，请参阅[舍入](https://ww2.mathworks.cn/help/releases/R2022b/fixedpoint/ug/rounding.html) (Fixed-Point Designer)。 -->



<!-- ### 对整数溢出进行饱和处理 — 溢出操作的方法 off （默认） | on



指定对溢出是进行饱和处理还是绕回处理。

- off - 溢出将绕回到数据类型可以表示的合适值。

  例如，数字 130 不适合一个有符号的 8 位整数，因此绕回 -126。

- on - 将溢出饱和处理为数据类型能够表示的最小值或最大值。

  例如，一个有符号的 8 位整数的溢出可以饱和处理为 -128 或 127。



**提示**

- 如果您的模型存在可能的溢出，而您希望在生成的代码中进行显式饱和保护，请考虑选中此复选框。

- 如果您希望优化生成的代码的效率，请考虑清除此复选框。

  清除此复选框还可以帮助您避免过度地指定信号超出范围时的处理方式。有关详细信息，请参阅[信号范围错误故障排除](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/signal-ranges.html#brdiku9)。

- 如果选中此复选框，饱和将应用于模块中的每个内部操作，而不仅仅应用于输出或结果。

- 一般情况下，代码生成进程可以检测到何时不可能发生溢出。在这种情况下，代码生成器不会生成饱和代码。

#### 编程用法

| **模块参数**：SaturateOnIntegerOverflow |
| ----------------------------------------- |
| **类型：**字符向量                        |
| **值：**'off' | 'on'                    |
| **默认值：**'off'                       | -->


<div class="details-box">
<details open>
<summary>允许不同数据输入大小(产生可变大小的输出信号) — 允许不同大小的输入信号<div>off （默认） | on</div></summary>
</details>
<div class="details-content">

选中此复选框将允许输入信号具有不同大小。

- On - 允许输入信号具有不同大小，并将输入信号的大小传播给输出信号。在此模式下，模块产生可变大小的输出信号；
- Off - 要求所有非标量数据输入信号的大小相同。

</div>
</div>



<!-- #### 编程用法

| **参数：**AllowDiffInputSizes |
| ------------------------------- |
| **类型：**字符向量              |
| **值：**'on' | 'off'        |
| **默认值：**'off'             | -->



<!-- ## 模块特性

| **数据类型**     | Boolean | bus | double | enumerated | fixed point | half | integer | single | string |
| ---------------- | ------------------------------------------------------------ |
| **直接馈通**     | 是                                                         |
| **多维信号**     | 是                                                         |
| **可变大小信号** | 是                                                         |
| **过零检测**     | 否                                                         | -->


## 版本历史记录

- 在 2024b 之前推出

### 限制信息

1. 暂不支持默认情况诊断功能；  
2. 暂不支持自定义采样时间；  
3. 暂不支持要求所有数据端口输入具有相同的数据类型的复选框；  
4. 暂不支持设定输出的最大最小值；  
5. 暂不支持锁定输出数据类型设置以防止被定点工具更改的复选框；  
6. 暂不支持设定整数舍入模式；  
7. 暂不支持对整数溢出进行饱和处理的复选框；  
8. 控制信号暂不支持half、int64、uint64、fixdPoint 和 image 的数据类型，数据输入暂不支持half、int64、uint64、fixdPoint、string 和 image 的数据类型，输出端口暂不支持half、int64、uint64、fixdPoint、string 和 image 的数据类型。

<!-- ## 扩展功能



### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 Verilog 代码和 VHDL 代码。



HDL Coder™ 提供影响 HDL 实现和综合逻辑的额外配置选项。

**HDL 架构**

此模块具有一个默认 HDL 架构。

**HDL 模块属性**

| 通用                          |                                                              |
| :---------------------------- | ------------------------------------------------------------ |
| **CodingStyle**               | 指定是用 case 语句还是 if-else 语句生成 HDL 代码。默认情况下，HDL Coder 会生成 if-else 语句。另请参阅[CodingStyle](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#mw_8759fc8a-90b4-451c-8e68-cb6ffa44fc81) (HDL Coder)。 |
| **ConstrainedOutputPipeline** | 通过移动设计中现有延迟的方式来放置在输出端的寄存器的数量。分布式流水线处理不会重新分发这些寄存器。默认值为 0。有关详细信息，请参阅[ConstrainedOutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#btp8gmp) (HDL Coder)。 |
| **InputPipeline**             | 要在生成的代码中插入的输入流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 0。有关详细信息，请参阅[InputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-25) (HDL Coder)。 |
| **OutputPipeline**            | 要在生成的代码中插入的输出流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 0。有关详细信息，请参阅[OutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-26) (HDL Coder)。 |

| 本机浮点            |                                                              |
| :------------------ | ------------------------------------------------------------ |
| **LatencyStrategy** | 指定对于浮点运算符是否将设计中的模块映射到 inherit、Max、Min 或 Zero。默认值为 “inherit”。另请参阅[LatencyStrategy](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/hdl-block-properties-native-floating-point.html#mw_a99b0822-f2a6-4f5b-aca9-7f7251a67c7c) (HDL Coder)。 |

**复数数据支持**

此模块支持复信号的代码生成。

**使用枚举类型作为端口索引**

您可以将**数据端口顺序**设置为**指定索引**，并为**数据端口索引**输入枚举值。例如，您可以将 Enumerated Constant 模块连接到 Multiport Switch 控制端口，并将枚举类型用作数据端口索引。

![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/multiportswitchwithenum.png)





### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。

## 版本历史记录

**在 R2006a 之前推出** -->

## 另请参阅

<!-- [Index Vector](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/indexvector.html) |  -->
[Switch](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SignalRouting/Switch.html)

<!-- ### 主题

- [可变大小信号基础知识](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/variable-size-signal-basics.html) -->