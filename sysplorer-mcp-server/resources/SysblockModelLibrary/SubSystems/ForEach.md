# ForEach
---
ForEach 子系统的控制模块

**库：** Sysblock模块库 / SubSystems

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SubSystems/ForEach/ForEach.png')" style="width: 100px; height: auto; transform: scale(1);">


<a id="jump1" class="jump-target"></a>
## 描述

ForEach 模块用作 ForEachSubsystem 模块的控制模块。具体来说，ForEach 模块可以使 ForEach 子系统内的模块能够独立处理输入信号或封装参数的元素。此子系统内每个具有状态的模块维护它所处理的每个元素或子数组的一组单独状态。随着该子系统中的模块集对元素（或子数组）的处理，该子系统串联结果以形成输出信号。

<!-- ![For Each Subsystem block icon, displayed alongside contents of for-each subsystem](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/for_each_subsystem_block_contents.png) -->

在更改输入或封装参数后使用 ForEach 子系统迭代计算输出。为此，请在 ForEach 模块对话框中配置输入信号或封装参数的分区。

### ForEachSubsystem
ForEachSubsystem 模块是一个预先配置的 Subsystem 模块，可以作为一个起点，用于创建在仿真时间步期间对输入信号或封装参数数组的每个元素或子数组都要重复执行的子系统。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SubSystems/ForEach/ForEachAS.png')" style="width: 400px; height: auto; transform: scale(0.8);">

子系统中的模块组表示应用于原始信号或封装参数数组的单个元素（或子数组）的算法。在子系统内，具有状态的每个模块维护它所处理的每个元素或子数组的单独状态集。因此，此子系统的操作在行为上类似于复制原始输入信号或封装参数数组中每个元素的子系统的内容，然后使用其各自的子系统副本处理每个元素。随着该子系统中的模块集对元素（或子数组）的处理，该子系统串联结果以形成输出信号。

### 将输入信号分区到子系统

要为 ForEach 子系统中的每次迭代指定要对哪些输入信号分区，请使用 ForEach 模块的对话框中的**输入分区**选项卡。在指定要分区的信号时，指定**分区维度**、**分区宽度**和**分区偏移量**参数。

### 对子系统的封装参数进行分区

您可以对 ForEachSubsystem 模块的封装参数进行分区。对于在每次迭代中结构相同但参数值不同的系统，分区非常有用。在这种情况下，针对每个参数更改模型来对额外输入参数进行分区非常繁琐。请改为将封装参数添加到 ForEach 子系统中。要选择封装参数进行分区，请使用 ForEach 模块对话框中的**参数分区**选项卡。

### 串联输出

通过在**输出串联**选项卡中指定**串联维度**来定义沿哪个维度串联结果。

模块为每个子数组生成的结果沿串联维度 1 堆叠。默认情况下，使用维度 1（y 轴），这意味着结果垂直堆叠。但是，如果指定的串联维度为 2，结果将沿水平方向（x 轴）串联。因此，如果该过程生成行向量，则串联的结果在第一种情况下是矩阵，在第二个种情况下是行向量。

### 选择分区参数

当选择要分区的输入信号或子系统封装参数时，您需要为每次迭代指定如何将其分解为元素或子数组。通过为**分区维度**、**分区宽度**和**分区偏移量**参数设置整数值来执行此操作。

作为说明，以如下形式的输入信号矩阵 A 为例：

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SubSystems/ForEach/ForEach01.png')" style="width: 200px; height: auto; transform: scale(1);">

标签 d1 和 d2 分别定义维度 1 和 2。如果为分区维度和分区宽度均保留默认设置 1，为分区偏移量保留默认设置 0，则 Sysblock 会垂直于分区维度 1 以等于分区宽度（一个元素）的宽度进行切片：

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SubSystems/ForEach/ForEach02.png')" style="width: 200px; height: auto; transform: scale(1);">

矩阵 A 分解为以下三个行向量：

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SubSystems/ForEach/ForEach03.png')" style="width: 200px; height: auto; transform: scale(1);">

如果改为将 2 指定为分区维度，则 Sysblock 将垂直于维度 2 进行切片来形成以下三个列向量：

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SubSystems/ForEach/ForEach04.png')" style="width: 200px; height: auto; transform: scale(1);">

除了将**分区维度**设置为 2 之外，如果再将**分区宽度**设置为 2 并将**分区偏移量**设置为 -1，Sysblock 会将矩阵处理为两个重叠的 3×2 分区。


<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SubSystems/ForEach/ForEach05.png')" style="width: 200px; height: auto; transform: scale(1);">


默认情况下，处理输入信号或封装参数的所有分区。要处理部分分区，请在**迭代次数**中输入要处理的分区的数量。在上面的矩阵示例中，如果**分区偏移量**设置为 0（默认值），并且**迭代次数**设置为 2，则仅处理输入矩阵 A 的前 2 行或前 2 列。


::: warning 注意 
在 Sysblock 中，只有信号被视为一维。封装参数是行向量或列向量，具体取决于其方向。要对行向量进行分区，请将分区维度指定为 2（沿列进行）。要对列向量进行分区，请将分区维度指定为 1（沿行进行）。
:::



## 示例

<!-- [![Partitioning an Input Signal with the For Each Block](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink/win64/PartitioningInputSignalDim1ForEachBlockExample_01.png)Partitioning an Input Signal with the For Each BlockThe following model demonstrates the partitioning of an input signal by a For Each block.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/partitioning-an-input-signal-with-for-each-block.html)

[![Specifying the Concatenation Dimension in the For Each Block](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink/win64/SpecifyingConcatenationDimensionForEachBlockExample_01.png)Specifying the Concatenation Dimension in the For Each BlockSpecify a concatenation dimension in the For Each block.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/specifying-concat-dimension-in-for-each-block.html)

[![Tiled Processing of 2D Signals with For Each Subsystem](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink_features/win64/TiledProcessingOf2DSignalsWithForEachSubsystemExample_01.png)Tiled Processing of 2D Signals with For Each SubsystemUse the For Each Subsystem. In this example the operations are performed on matrices.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/tiled-processing-of-2d-signals-with-for-each-subsystem.html)

[![Vectorizing a Scalar Algorithm with a For Each Subsystem](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink_features/win64/VectorizingAScalarAlgorithmWithForEachSubsystemExample_01.png)Vectorizing a Scalar Algorithm with a For Each SubsystemUse the For Each subsystem. In this example the operations are performed on a vector for simplicity.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/vectorizing-a-scalar-algorithm-with-for-each-subsystem.html)

[![Modeling Objects with Identical Dynamics Using For Each Subsystem](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink_features/win64/ModelingObjectsWithIdenticalDynamicsExample_06.png)Modeling Objects with Identical Dynamics Using For Each SubsystemModel multiple objects with identical dynamics using the For Each subsystem. The number of objects is parameterized by the length of the input signal.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/modeling-objects-with-identical-dynamics-using-for-each-subsystem.html) -->

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SubSystems/ForEach.mo">ForEach.mo</helpButton>。


<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SubSystems/ForEach/2.png')" style="width: 750px; height: auto; transform: scale(0.8);">

### 示例说明

- Constant：生成一个数组 [1，2，3]；
- SubSystem：实现对数组中的每个元素进行开平方操作；
- Scope：显示原始数组和开平方后的数组。

<!-- ## 端口

### 输出

### Partition index — 当前分区的索引 标量


当前分区的索引（从 0 开始），以标量形式返回。

#### 依存关系

要启用此端口，请选择**显示分区索引输出端口**。

**数据类型：** int32 | double -->

## 参数

### “输入分区”选项卡



选择要分区的每个输入信号，并指定对应的**分区维度**、**分区宽度**和**分区偏移量**参数。有关详细信息，请参阅 [Inport](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Port/Inport.html) 模块参考页。


<div class="details-box">
<details open>
<summary>端口 — 输入端口列表<div>无默认值 （默认） | 输入端口名称</div></summary>
</details>
<div class="details-content">

此属性为只读

连接到 ForEachSubsystem 模块的输入端口的列表。

</div>
</div>





<div class="details-box">
<details open>
<summary>分区 — 选择输入端口信号以进行分区<div>off （默认） | on</div></summary>
</details>
<div class="details-content">

选择连接到 ForEachSubsystem 模块的输入端口信号以将其分区为子数组或元素。对于**端口**列中列出的每个端口，选中对应的复选框来对该信号进行分区。

</div>
</div>




<!-- #### 编程用法

| **模块参数**：InputPartition |
| ------------------------------ |
| **类型**：字符向量             |
| **值**：'off' | 'on'       |
| **默认值**：'off'            |  -->


<div class="details-box">
<details open>
<summary>分区维度 — 指定维度<div>1 （默认） | 2 | 正整数</div></summary>
</details>
<div class="details-content">

指定用于对所选输入信号数组进行切片的维度。生成的切片垂直于您指定的维度。切片会视情况将数组分区为子数组或元素。

- 1

  沿列对输入数组进行切片。

- 2

  沿行对输入数组进行切片。

- n

  沿维度 n 对输入数组进行切片。

**依存关系：**要启用此参数，请为相关输入端口选择**分区**。

</div>
</div>




<!-- #### 编程用法

| **模块参数**：InputPartitionDimension        |
| ---------------------------------------------- |
| **类型**：字符向量                             |
| **值**：'1' | '2' | '<positive integer>' |
| **默认值**：'1'                              |  -->


<div class="details-box">
<details open>
<summary>分区宽度 — 指定宽度<div>1 （默认） | 正整数</div></summary>
</details>
<div class="details-content">

指定所选输入信号的每个分区切片的宽度。

**依存关系：**要启用此参数，请为相关输入端口选择**分区**。

</div>
</div>




<!-- #### 编程用法

| **模块参数**： InputPartitionWidth |
| ------------------------------------ |
| **类型**：字符向量                   |
| **值**：'1' | '<integer>'        |
| **默认值**：'1'                    | -->


<div class="details-box">
<details open>
<summary>分区偏移量 — 指定分区偏移量<div>0 （默认） | 整数</div></summary>
</details>
<div class="details-content">

指定所选输入信号的每个分区切片的偏移量。

- 0

  分区切片之间无偏移，即分区切片之间没有间隙且不重叠。

- 整数

  指定分区偏移量，使用正整数指定切片之间的间隙，或使用负整数表示重叠。**分区宽度**和**分区偏移量**之和必须为正整数。例如，**分区宽度**为 3 和**分区偏移量**为 -2 表示每个 3 元素切片中都有 2 个元素与其相邻切片重叠；而**分区宽度**为 2 和**分区偏移量**为 1 表示每对相邻的宽度为 2 个元素的切片之间存在宽度为 1 个元素的间隙。

**依存关系：**要启用此参数，请为相关输入端口选择**分区**。

</div>
</div>




<!-- #### 编程用法

| **模块参数**：InputPartitionOffset |
| ------------------------------------ |
| **类型**：字符向量                   |
| **值**：'0' | '<integer>'        |
| **默认值**：'0'                    | -->

<!-- ### “参数分区”选项卡

选择您要分区的每个封装参数，并指定相应的**分区维度**和**分区宽度**参数。



### 参数 — 封装参数的列表 参数名称



此属性为只读

For Each Subsystem 模块的封装参数的列表。仅当您向 For Each Subsystem 模块的封装添加可编辑参数后，列表中才会显示封装参数。请参阅[创建模块封装](https://ww2.mathworks.cn/help/releases/R2022b/simulink/block-masks.html)。



### 分区 — 选择封装参数以进行分区 off （默认） | on



选择 For Each Subsystem 模块的封装参数以将其分区为子数组或元素。对于**参数**列中列出的每个端口，选中对应的复选框来对该封装参数进行分区。

#### 编程用法

| **模块参数**：SubsysMaskParameterPartition |
| -------------------------------------------- |
| **类型**：字符向量                           |
| **值**：'off' | 'on'                     |
| **默认值**：'off'                          |



### 分区维度 — 指定维度 1 （默认） | 2 | 正整数



指定用于对所选封装参数数组进行切片的维度。生成的切片垂直于您指定的维度。切片会视情况将数组分区为子数组或元素。

- 1

  沿列对封装参数数组进行切片。

- 2

  沿行对封装参数数组进行切片。

- n

  沿维度 n 对封装参数数组进行切片。

#### 依存关系

要启用此参数，请为相关封装参数选择**分区**。

#### 编程用法

| **模块参数**：SubsysMaskParameterPartitionDimension |
| ----------------------------------------------------- |
| **类型**：字符向量                                    |
| **值**：'1' | '<integer>'                         |
| **默认值**：'1'                                     |



### 分区宽度 — 指定分区宽度 1 （默认） | 正整数



指定所选封装参数数组的每个分区切片的宽度。

#### 依存关系

要启用此参数，请为相关封装参数选择**分区**。

#### 编程用法

| **模块参数**：SubsysMaskParameterPartitionWidth |
| ------------------------------------------------- |
| **类型**：字符向量                                |
| **值**：'1' | '<positive integer>'            |
| **默认值**：'1'                                 | -->

### “输出串联”选项卡


对于每个输出端口，指定堆叠（串联）ForEachSubsystem 模块结果所沿的维度。有关详细信息，请参阅 [Outport](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Port/Outport.html) 模块参考页。


<div class="details-box">
<details open>
<summary>端口 — 输出端口的列表<div>无 （默认） | 输出端口名称</div></summary>
</details>
<div class="details-content">

此属性为只读

连接到 ForEachSubsystem 模块的输出端口的列表。

</div>
</div>






<div class="details-box">
<details open>
<summary>串联维度 — 指定维度<div>1 （默认） | 2 | positive integer</div></summary>
</details>
<div class="details-content">

对于每个输出端口，指定堆叠 ForEachSubsystem 模块的结果所沿的维度。

- 1

  结果在 d1 方向堆叠，即垂直堆叠。如果模块生成列向量，则串联过程会生成单个列向量。如果模块生成行向量，则串联过程会生成矩阵。

- 2

  结果在 d2 方向堆叠，即水平堆叠。如果模块生成行向量，则串联过程会生成单个行向量。如果模块生成行向量，则串联过程会生成矩阵。

- n

  结果在 dn 方向堆叠。

</div>
</div>




<!-- #### 编程用法

| **模块参数**：OutputConcatenationDimension |
| -------------------------------------------- |
| **类型**：字符向量                           |
| **值**：'1' | '<integer>'                |
| **默认值**：'1'                            | -->

### 其他参数



<!-- ### 显示分区索引输出端口(从 0 开始的索引) — 控制输出端口的显示 off （默认） | on



控制分区索引输出端口的显示。

- off

  隐藏输出端口。

- on

  在模块上显示输出端口。

#### 编程用法

| **模块参数**：ShowIterationIndex |
| ---------------------------------- |
| **类型**：字符向量                 |
| **值**：'off' | 'on'           |
| **默认值**：'off'                |



### 分区索引输出数据类型 — 指定分区索引数据类型 'int32' （默认） | 'double'



指定输出端口的分区索引数据类型。

- int32

  选择 32 位有符号整数。

- double

  选择双精度实数。

#### 依存关系

要启用此参数，请选择**显示分区索引输出端口**。

#### 编程用法

| **模块参数**：IterationIndexDataType |
| -------------------------------------- |
| **类型**：字符向量                     |
| **值**：'int32' | 'double'         |
| **默认值**：'int32'                  | -->


<div class="details-box">
<details open>
<summary>迭代次数 — 指定要处理的分区的数量<div>-1 （默认） | 整数</div></summary>
</details>
<div class="details-content">

要处理数据子集，请指定要处理的输入信号或封装参数数组的分区切片数；或者，请指定 -1 以处理所有切片。该数量不能大于可用切片的总数。

- -1

  处理所有切片

- 整数

  要处理的切片数例如，**迭代次数**为 3 表示只处理前 3 个切片。


</div>
</div>



<!-- #### 编程用法

| **模块参数**：SpecifiedNumIters |
| --------------------------------- |
| **类型**：字符向量                |
| **值**：'-1' | '<integer>'    |
| **默认值**：'-1'                | -->



<!-- ## 扩展功能



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 Verilog 代码和 VHDL 代码。



HDL Coder™ 提供影响 HDL 实现和综合逻辑的额外配置选项。

**HDL 架构**

此模块具有一个默认 HDL 架构。 -->

## 版本历史记录

- 在 2024b 之前推出

### 限制信息

1. 暂不支持参数分区选项卡及设定参数、分区、分区维度和分区宽度的设定；  
2. 暂不支持显示分区索引输出端口的复选框；  
3. 暂不支持指定分区索引的输出数据类型。


## 另请参阅

[ForEachSubsystem](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SubSystems/ForEach.html#jump1) | [Subsystem](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SubSystems/Subsystem.html)

<!-- ### 主题

- [Repeat an Algorithm Using a For-Each Subsystem](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/repeat-an-algorithm-using-a-for-each-subsystem.html)
- [Log Signals in For Each Subsystems](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/log-signals-in-for-each-subsystems-1.html) -->