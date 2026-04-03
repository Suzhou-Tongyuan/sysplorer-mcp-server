# DataStoreWrite
---
向数据存储中写入数据

**库：** Sysblock模块库 / SignalRouting

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/DataStoreWrite/DataStoreWrite.png')" style="width: 100px; height: auto; transform: scale(1);">



## 描述

DataStoreWrite 模块将其输入端口的值复制到指定的数据存储中。由 DataStoreWrite 模块执行的每个写入操作都会覆盖数据存储或其所选部分，并替换以前的内容。

此模块写入的数据存储由定义数据存储的 DataStoreMemory 模块或信号对象的位置决定。
<!-- 有关详细信息，请参阅[数据存储](https://ww2.mathworks.cn/help/releases/R2022b/simulink/data-stores.html)和 [Data Store Memory](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/datastorememory.html)。数据存储的大小由定义并初始化数据存储的信号对象或 Data Store Memory 模块决定。写入该数据存储的每个 Data Store Write 模块最多可以写入数据存储中的数据量。 -->

多个 DataStoreWrite 模块可以写入同一数据存储。但是，如果两个 DataStoreWrite 模块尝试在同一个仿真步中写入同一个数据存储，将发生不可预知的结果。

要从数据存储获取正确的结果，必须确保数据存储按照预期的顺序进行读取和写入。
<!-- 有关详细信息，请参阅[对数据存储访问进行排序](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/model-global-data-using-data-stores.html#brytnz0)和[数据存储诊断](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/data-store-basics.html#brytn1d-1_1)。 -->

您可以记录某个局部或全局数据存储数据变量在一次仿真过程的所有时间步中的值。
<!-- 有关详细信息，请参阅[Log Data Stores](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/logging-data-stores.html)。 -->

您可以选择 DataStoreRead、DataStoreWrite 或 DataStoreMemory 模块来突出显示与其相关的模块。
<!-- 要在打开的图或新选项卡中显示相关模块，请在选择后出现的省略号上暂停。然后，从操作栏中选择**相关模块** ![Related Blocks button](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/related-blocks-button.png)。当多个模块对应于所选模块时，将打开一个相关模块列表。您可以通过在文本框中输入搜索词来筛选相关模块列表。从列表中选择相关模块后，窗口焦点转至显示该相关模块的打开的图或新选项卡。 -->

## 示例

<!-- [![Share Data Store Between Instances of a Reusable Algorithm](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink_features/win64/ShareDataStoreBetweenInstancesOfAReusableAlgorithmExample_06.png)Share Data Store Between Instances of a Reusable AlgorithmTo reuse an algorithm, instead of copying and pasting the blocks, you can encapsulate them in a separate model file. Then, you can refer to the model repeatedly with Model blocks. Each Model block is a standalone instance of the algorithm.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/sharing-local-data-stores-across-multiple-instances-of-a-model.html) -->

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/DataStoreWrite.mo">DataStoreWrite.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/DataStoreWrite/DataStoreWrite_ex.png')" style=" width: 600px;transform: scale(0.8);">

### 示例说明

- Step 模块：提供从 0 步变到 1 的输入信号，用于模拟实际输入值；
- DataStoreWrite 模块：将输入信号的数据写入到一个命名的数据存储中。在这个示例中，我们使用 MyDataStore 作为数据存储的名称；
- 结果查看器：用于查看和验证数据存储的内容。通过仿真-结果查看器，我们可以在工作空间中加载并查看 X 中的数据。

## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 要写入数据存储的值<div>标量 | 向量 | 矩阵 | N 维数组</div></summary>
</details>
<div class="details-content">

要写入指定数据存储的值。DataStoreWrite 模块接受实信号或复信号。

您可以将总线数组与 DataStoreWrite 模块结合使用。
<!-- 有关定义和使用总线数组的详细信息，请参阅[使用总线数组组合非虚拟总线](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/combining-buses-into-an-array-of-buses.html)。 -->

<!-- 要将总线或矩阵元素的子集赋给相关联的数据存储，请使用**元素赋值**窗格。Data Store Write 模块图标反映您指定的元素。有关详细信息，请参阅[访问特定的总线和矩阵元素](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/model-global-data-using-data-stores.html#bsvjg1i)。 -->

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | fixedPoint | enum | bus

</div>
</div>




<!-- ### IdxN — 第 N 个索引信号 标量 | 向量



外部端口，用于指定对应数据存储子元素的赋值的索引。

#### 依存关系

要启用外部索引端口，请在**元素赋值**选项卡上选择**启用索引**。然后，在**索引选项**表的第 N 行中，将**索引选项**设置为“索引向量(端口)” 或“起始索引(端口)”。

**数据类型：** int8 | int16 | int32 | uint8 | uint16 -->

## 参数


### 参数

<div class="details-box">
<details open>
<summary>数据存储名称 — 模块写入的数据存储的名称<div>X （默认） | 数据存储的名称</div></summary>
</details>
<div class="details-content">

指定此模块向其中写入数据的数据存储的名称。旁边的列表列出了模型中与 DataStoreWrite 模块在同一级别或更高级别的 DataStoreMemory 模块的名称。

</div>
</div>



<!-- 该列表中还包括基础工作区和模型工作区中的所有 Simulink.Signal 对象。要更改名称，请从该列表中选择名称，或者直接在编辑字段中输入名称。 -->

<!-- 当编译包含此模块的模型时，Simulink® 从该模块级别向上搜索模型，寻找具有指定数据存储名称的 Data Store Memory 模块。如果 Simulink 找不到这样的模块，它将在模型工作区和 MATLAB® 工作区中搜索具有相同名称的 [Simulink.Signal](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/simulink.signal.html) 对象。如果 Simulink 找到信号对象，它将在模型的根级创建一个隐藏的 Data Store Memory 模块，此模块的属性由信号对象指定，初始值设置全零数组。该数组的维度从信号对象的 Dimensions 属性继承。

如果 Simulink 既找不到 Data Store Memory 模块，也找不到信号对象，它将停止编译并显示错误。有关搜索路径的详细信息，请参阅[符号解析](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/resolving-symbols.html)。 -->

<!-- #### 编程用法

| **模块参数**：DataStoreName |
| ----------------------------- |
| **类型**：字符向量            |
| **值**：数据存储名称          |
| **默认值**：'A'             | -->



<!-- ### Data Store Memory 模块 — Data Store Memory 模块名称 模块路径



此属性为只读

此字段列出 Data Store Memory 模块，该模块对它要向其写入数据的存储进行了初始化。
 -->


<!-- ### 对应的 Data Store Read 模块 — 对应的 Data Store Read 模块列表 模块路径



此属性为只读

此字段列出符合以下条件的所有 Data Store Read 模块的路径：与此模块具有相同的数据存储名称，且在模型层次结构中位于同一（子）系统级别或其下的任何子系统中。点击此列表中的任何条目以在模型中突出显示对应的模块。 -->



<!-- ### 采样时间 — 采样时间 -1 （默认） | 标量 | 向量



采样时间，用来控制模块何时写入数据存储。值为 -1 表示继承采样时间。有关详细信息，请参阅 [指定采样时间](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/how-to-specify-the-sample-time.html)。

#### 编程用法

| **模块参数**：SampleTime |
| -------------------------- |
| **类型**：字符向量         |
| **值**：标量 \| 向量       |
| **默认值**：'-1'         | -->

<!-- ### 元素赋值



### 数组中的元素(总线中的信号) — 关联的数据存储中的元素 字符向量（无默认值）



关联的数据存储中元素的列表。对于包含数组的数据存储，您可以写入整个数据存储，也可以将一个或多个元素赋给整个数据存储。对于总线数据类型的数据存储，您可以展开树视图以查看并选择总线元素。此列表在括号中显示每个元素的最大维度。

如果未选择**启用索引**，请选择一个元素并使用以下方法之一：

- 点击**选择>>** 在**所选元素**列表中显示该元素及其所有子元素。
- 使用**指定要赋值的元素**编辑框指定您要选择进行写入的子元素。然后点击**选择>>**。

要选择多个元素，请对每个元素重复上述过程。

您也可以选择**启用索引**，然后选择单个元素，并使用**索引选项**参数动态指定子元素。

要刷新显示并反映对数据存储中使用的数组或总线的修改，请点击**刷新**。

#### 依存关系

对此部分（**数组中的元素**或**总线中的信号**）的提示取决于数据存储中数据的类型。

#### 编程用法

| **模块参数**：DataStoreElements                            |
| ------------------------------------------------------------ |
| **类型**：字符向量                                           |
| **值**：以井号分隔的元素列表（请参阅[使用命令行指定](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/model-global-data-using-data-stores.html#bsvla4x)。） |
| **默认值**：''                                             |



### 指定要赋值的元素 — 定义要分配的元素的 MATLAB 表达式 字符向量（无默认值）



输入 MATLAB 表达式以定义要写入的特定元素，然后点击**选择>>** 将该元素添加到**赋值的元素**表中。重复以上操作以选择其他元素。

例如，对于名为 DSM、最大维度为 [3,5] 的数据存储，您可以在编辑框中输入表达式，如 DSM(2,4) 或 DSM([1 3],2)。请参阅[访问特定的总线和矩阵元素](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/model-global-data-using-data-stores.html#bsvjg1i)。

要应用元素选择，请点击**确定**或**应用**。

#### 依存关系

仅当未选择**启用索引**时，才会出现**指定要赋值的元素**编辑框。

#### 编程用法

| **模块参数**：DataStoreElements                            |
| ------------------------------------------------------------ |
| **类型**：字符向量                                           |
| **值**：以井号分隔的元素列表（请参阅[使用命令行指定](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/model-global-data-using-data-stores.html#bsvla4x)。） |
| **默认值**：''                                             |



### 赋值的元素 — 选定元素的列表 字符向量（无默认值）



您选择要分配的元素。Data Store Write 模块图标为您指定的每个元素显示输入端口。

要更改列表中的总线或矩阵元素的顺序，请在列表中选择元素，然后点击**向上**或**向下**。更改列表中的元素顺序会同时更改端口的顺序。要移除某个元素，请点击**删除**。

#### 依存关系

仅当未选择**启用索引**时，才会出现**赋值的元素**表。

#### 编程用法

| **模块参数**：DataStoreElements                            |
| ------------------------------------------------------------ |
| **类型**：字符向量                                           |
| **值**：以井号分隔的元素列表（请参阅[使用命令行指定](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/model-global-data-using-data-stores.html#bsvla4x)。） |
| **默认值**：''                                             |



### 启用索引 — 启用索引以指定要写入的数据存储元素的子元素 'off' （默认） | 'on'



选中此参数可启用类似于 [Assignment](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/assignment.html) 模块所使用的索引，由此您可以使用一个或多个索引输入端口动态指定要写入的子元素的索引，以及使用模块对话框指定索引。选中此参数时，Data Store Write 模块只能写入数据存储的单个元素（即总线中的单个信号）。要使用动态索引写入数据存储的多个元素，请使用多个 Data Store Write 模块。

清除此参数可禁用 Assignment 模块样式索引。您可以选择多个要写入的数据存储元素，但只能通过使用模块对话框指定要写入哪些子元素。



**注意**

如果关联的数据存储只包含一个标量元素，请不要选择**启用索引**。

#### 编程用法

| **模块参数**：EnableIndexing |
| ------------------------------ |
| **类型**：字符向量             |
| **值**：'off' | 'on'       |
| **默认值**：'off'            |



### 维数 — 数据存储元素的维数 1 （默认） | 正整数



所选数据存储元素的维数。您必须显式指示此数目。

#### 依存关系

仅当选中**启用索引**时，此参数才会启用。

#### 编程用法

| **模块参数**：NumberOfDimensions |
| ---------------------------------- |
| **类型**：字符向量                 |
| **值**：positive integer         |
| **默认值**：'1'                  |



### 索引模式 — 索引模式 “从 1 开始” （默认） | “从 0 开始”



选择索引模式。如果选择“从 1 开始”，则索引 1 指定输入向量的第一个元素。如果选择“从 0 开始”，则索引 0 指定输入向量的第一个元素。

#### 依存关系

仅当选中**启用索引**时，此参数才会启用。

#### 编程用法

| **参数：**IndexMode                  |
| -------------------------------------- |
| **类型：**字符向量                     |
| **值：**'Zero-based' | 'One-based' |
| **默认值：**'One-based'              |



### 索引选项 — 子元素的索引方法 “索引向量(对话框)” （默认） | “全选” | “索引向量(端口)” | “起始索引(对话框)” | “起始索引(端口)”



按维度定义所选数据存储元素的子元素的索引方式。从列表中，选择：

| 菜单项               | 操作                                                         |
| :------------------- | :----------------------------------------------------------- |
| “全选”             | 禁用**索引**列。所有子元素都被分配。                         |
| “索引向量(对话框)” | 启用**索引**列。输入包含要赋值的子元素索引的向量。           |
| “索引向量(端口)”   | 禁用**索引**列。相关索引端口定义要赋值的子元素的索引。       |
| “起始索引(对话框)” | 启用**索引**列。输入要赋值的子元素范围的起始索引。范围的大小继承于输入数据信号的相关维度的大小。 |
| “起始索引(端口)”   | 禁用**索引**列。相关索引端口定义要赋值的元素范围的起始索引。范围的大小继承于输入数据信号的相关维度的大小。 |

**索引**列显示为相关。

#### 依存关系

仅当选中**启用索引**时，此参数才会启用。

#### 编程用法

| **参数：**IndexOptionArray                                 |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值：** 'Select all' | 'Index vector (dialog)' | 'Index vector (port)' | 'Starting index (dialog)' | 'Starting index (port)' |
| **默认值：**'Index vector (dialog)'                        |



### 索引 — 子元素的索引或起始索引 1 （默认） | 整数 | 整数向量



如果**索引选项**是“索引向量(对话框)”，请输入包含要写入的每个子元素的索引的向量。

如果**索引选项**设置为“起始索引(对话框)”，则输入要写入的子元素范围的起始索引。

#### 依存关系

仅当选择**启用索引**并且维度的**索引选项**为“索引向量(对话框)” 或“起始索引(对话框)” 时，此参数才启用。

#### 编程用法

| **参数：**IndexParamArray |
| --------------------------- |
| **类型：**字符向量          |
| **值：**元胞数组            |
| **默认值：**'{ }'         | -->



<!-- ## 模块特性

| **数据类型**     | Boolean | bus | double | enumerated | fixed point | half | integer | single | string |
| ---------------- | ------------------------------------------------------------ |
| **直接馈通**     | 否                                                         |
| **多维信号**     | 是                                                         |
| **可变大小信号** | 否                                                         |
| **过零检测**     | 否                                                         | -->

## 版本历史记录

- 在 2024b 之前推出

### 限制信息

1. 暂不支持第 N 个索引信号的输入端口；  
2. 暂不支持显示 DataStoreMemory 模块名称和对应的 DataStoreRead 模块列表；  
3. 暂不支持自定义采样时间；  
4. 暂不支持设定数组中的元素；  
5. 暂不支持指定要赋值的元素；  
6. 暂不支持设定赋值的元素；  
7. 暂不支持启用索引的复选框；  
8. 暂不支持设定维数；  
9. 暂不支持设定索引、索引模式、索引选项；  
10. 输入端口暂不支持half、int64、uint64 和 image 的数据类型。

<!-- ## 扩展功能



### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。

## 版本历史记录

**在 R2006a 之前推出** -->

## 另请参阅

[DataStoreMemory](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SignalRouting/DataStoreMemory.html) | [DataStoreRead](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SignalRouting/DataStoreRead.html)

<!-- ### 主题

- [数据存储](https://ww2.mathworks.cn/help/releases/R2022b/simulink/data-stores.html)
- [重命名数据存储](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/model-global-data-using-data-stores.html#buoeaac)
- [对数据存储访问进行排序](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/model-global-data-using-data-stores.html#brytnz0)
- [使用 Simulink 模块访问数据存储](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/model-global-data-using-data-stores.html#f4-146588)
- [Log Data Stores](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/logging-data-stores.html)
- [数据存储诊断](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/data-store-basics.html#brytn1d-1_1) -->