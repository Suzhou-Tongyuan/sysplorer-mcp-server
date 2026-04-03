# DataStoreMemory
---
定义数据存储

**库：** Sysblock模块库 / SignalRouting

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/DataStoreMemory/DataStoreMemory.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

DataStoreMemory 模块定义并初始化一个命名的共享数据存储，即一个内存区域，供指定相同数据存储名称的 DataStoreRead 和 DataStoreWrite 模块使用。

定义数据存储的 DataStoreMemory 模块的位置确定了哪些 DataStoreRead 和 DataStoreWrite 模块可以访问该数据存储：

- 如果 DataStoreMemory 模块在顶层系统中，则模型中任意位置的 DataStoreRead 和 DataStoreWrite 模块都可以访问该数据存储；
- 如果 Data Store Memory 模块在子系统中，则位于同一子系统或模型层次结构中该子系统下面的任何子系统中的 DataStoreRead 和 DataStoreWrite 模块都可以访问该数据存储。

DataStoreRead 或 DataStoreWrite 模块不能访问位于包含 Model 模块的模型中或引用模型中的 DataStoreMemory 模块。


<!-- 暂无
要从数据存储获取正确的结果，必须确保数据存储按照预期的顺序进行读取和写入。有关详细信息，请参阅：

- [对数据存储访问进行排序](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/model-global-data-using-data-stores.html#brytnz0)
- [数据存储诊断](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/data-store-basics.html#brytn1d-1_1)
- [Log Data Stores](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/logging-data-stores.html)

您可以使用 Data Store Memory 模块结合 [Simulink.Signal](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/simulink.signal.html) 对象来定义数据存储，也可以不使用前者而只使用后者来定义数据存储。在*基础*工作区中定义的具有一个信号对象的数据存储是一个*全局*数据存储。每个模型都可以访问全局数据存储，包括所有引用的模型。有关详细信息，请参阅[数据存储](https://ww2.mathworks.cn/help/releases/R2022b/simulink/data-stores.html)。

您可以选择 Data Store Read、Data Store Write 或 Data Store Memory 模块来突出显示与其相关的模块。要在打开的图或新选项卡中显示相关模块，请在选择后出现的省略号上暂停。然后，从操作栏中选择**相关模块** ![Related Blocks button](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/related-blocks-button.png)。当多个模块对应于所选模块时，将打开一个相关模块列表。您可以通过在文本框中输入搜索词来筛选相关模块列表。从列表中选择相关模块后，窗口焦点转至显示该相关模块的打开的图或新选项卡。 -->

## 示例

<!-- [![Share Data Store Between Instances of a Reusable Algorithm](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink_features/win64/ShareDataStoreBetweenInstancesOfAReusableAlgorithmExample_06.png)Share Data Store Between Instances of a Reusable AlgorithmTo reuse an algorithm, instead of copying and pasting the blocks, you can encapsulate them in a separate model file. Then, you can refer to the model repeatedly with Model blocks. Each Model block is a standalone instance of the algorithm.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/sharing-local-data-stores-across-multiple-instances-of-a-model.html) -->

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/DataStoreMemory.mo">DataStoreMemory.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/DataStoreMemory/DataStoreMemory_ex.png')" style="width: 600px; transform: scale(0.8);">

### 示例说明

- DataStoreMemory 模块：定义并初始化一个命名的共享数据存储，这个数据存储可以被指定相同数据存储名称的 DataStoreRead 和 DataStoreWrite 模块访问；
- DataStoreWrite 模块：将信号数据写入由 DataStoreMemory 模块定义的数据存储中；
- DataStoreRead 模块：从由 DataStoreMemory 模块定义的数据存储中读取信号数据；
- Scope 模块：用于显示模型的输出结果，即从数据存储中读取的数据。



## 参数


### 主要

<div class="details-box">
<details open>
<summary>数据存储名称 — 数据存储的名称<div>X （默认） | 字符向量 | 字符串</div></summary>
</details>
<div class="details-content">

使用此模块指定您正在定义的数据存储的名称。具有相同名称的 DataStoreRead 和 DataStoreWrite 模块可以读取和写入由此模块初始化的数据存储。此名称可以代表一个 DataStoreMemory 模块或者一个定义为数据存储的符号对象。

</div>
</div>




<!-- #### 编程用法

| **模块参数**：DataStoreName |
| ----------------------------- |
| **类型**：字符向量            |
| **值**：'A' | ...           |
| **默认值**：'A'             | -->


<!-- 暂无
### 全部重命名 — 在整个模型中重命名此数据存储 按钮



重命名 Data Store Read 和 Data Store Write 模块使用的位于模型中任意位置的此数据存储。

#### 限制

在下列情况下，不能使用**全部重命名**来重命名数据存储：



- 在工作区中使用 Simulink.Signal 对象来管理为数据存储生成的代码
- 使用 Simulink.Signal 对象而不是 Data Store Memory 模块来定义数据存储



在这些情况下，您必须从模型资源管理器中重命名相应的 Simulink.Signal 对象。有关示例，请参阅[重命名信号对象定义的数据存储](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/model-global-data-using-data-stores.html#buoeaa4)。 -->


<!-- 暂无
### 对应的 Data Store Read/Write 模块 — 所连接的 Data Store Read/Write 模块的路径 模块路径



列出与当前模块具有相同数据存储名称且在当前系统中或者在模型层次结构中位于当前系统下面的任何子系统中的所有 Data Store Read 和 Data Store Write 模块。单击某模块路径将在模型中显示并突出显示该模块。 -->


<div class="details-box">
<details open>
<summary>初始值 — 数据存储的初始值<div>0 （默认） | 标量 | 向量 | 矩阵 | N 维数组</div></summary>
</details>
<div class="details-content">

指定数据存储的一个或多个初始值。**最小值**参数指定此参数的最小值，**最大值**参数指定最大值。

如果指定非标量值，并将**维度**设置为 -1（默认值），数据存储的维度将与数组的维度相同。您（通过使用 DataStoreWrite 模块）写入数据存储的数据必须具有这些维度。

如果将**维度**参数设置为 -1 以外的值，初始值维度必须与您指定的维度相匹配，除非初始值是标量或 MATLAB® 结构体。如果指定标量，则数据存储的每个元素都使用该标量作为初始值。使用这种方法可将同一初始值（您指定的标量）应用到每个元素，而无需手动将初始值的维度与数据存储的维度进行匹配。

</div>
</div>




<!-- 暂无
要使用此模块初始化非虚拟总线信号，请将初始值指定为 MATLAB 结构体，并将模型配置参数[欠定初始化检测](https://ww2.mathworks.cn/help/releases/R2022b/simulink/gui/underspecified-initialization-detection.html)设置为简化。有关使用结构体初始化非虚拟总线信号的详细信息，请参阅[指定总线元素的初始条件](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/specifying-initial-conditions-for-bus-signals.html)。 -->

<!-- #### 编程用法

| **模块参数**：InitialValue             |
| ---------------------------------------- |
| **类型**：字符向量                       |
| **值**：标量 \| 向量 \| 矩阵 \| N 维数组 |
| **默认值**：'0'                        | -->


<!-- 暂无
### 最小值 — 范围检查的最小输出值 [] （默认） | 标量



指定模块应输出的最小值。默认值为 []（未指定）。此数字必须为有限双精度实数标量值。



**注意**

如果您指定总线对象作为此模块的数据类型，请不要为模块上的总线数据设置最小值。Simulink 会忽略此设置。但请为指定作为数据类型的总线对象的总线元素设置最小值。有关总线元素的“最小值”属性的信息，请参阅 [Simulink.BusElement](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/simulink.buselement.html)。

Simulink® 使用最小值执行下列操作：

- 参数范围检查（请参阅[指定模块参数的最小值和最大值](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/checking-parameter-values.html)）。
- 仿真范围检查（请参阅[指定信号范围](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/signal-ranges.html)）。
- 定点数据类型的自动定标。
- 从模型生成的代码的优化。此优化可删除算法代码，并影响某些仿真模式（如 SIL 或外部模式）的结果。有关详细信息，请参阅[Optimize using the specified minimum and maximum values](https://ww2.mathworks.cn/help/releases/R2022b/ecoder/ref/optimizeusingthespecifiedminimumandmaximumvalues.html) (Embedded Coder)。

#### 编程用法

| **模块参数**：OutMin |
| ---------------------- |
| **类型**：字符向量     |
| **值**：标量           |
| **默认值**：'[ ]'    | -->



<!-- ### 最大值 — 范围检查的最大输出值 [] （默认） | 标量



指定模块应输出的最大值。默认值为 []（未指定）。此数字必须为有限双精度实数标量值。



**注意**

如果您指定总线对象作为此模块的数据类型，请不要为模块的总线数据设置最大值。Simulink 会忽略此设置。但请为指定作为数据类型的总线对象的总线元素设置最大值。有关总线元素的“最大值”属性的信息，请参阅 [Simulink.BusElement](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/simulink.buselement.html)。

Simulink 使用最大值执行下列操作：

- 参数范围检查（请参阅[指定模块参数的最小值和最大值](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/checking-parameter-values.html)）。
- 仿真范围检查（请参阅[指定信号范围](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/signal-ranges.html)）。
- 定点数据类型的自动定标。
- 从模型生成的代码的优化。此优化可删除算法代码，并影响某些仿真模式（如 SIL 或外部模式）的结果。有关详细信息，请参阅[Optimize using the specified minimum and maximum values](https://ww2.mathworks.cn/help/releases/R2022b/ecoder/ref/optimizeusingthespecifiedminimumandmaximumvalues.html) (Embedded Coder)。

#### 编程用法

| **模块参数**：OutMax |
| ---------------------- |
| **类型**：字符向量     |
| **值**：标量           |
| **默认值**：'[ ]'    | -->


<div class="details-box">
<details open>
<summary>类型 — 输出数据类型<div>“Inherit: auto” （默认） | “double” | “float” | “int8” | “uint8” | “int16” | “uint16” | “int32” | “uint32” | “boolean” | “fixdt(1,16,0)” | “fixdt(1,16,2^0,0)” | “fixdt(1,16,1.0,0,0.0)”| “enum” | “bus”</div></summary>
</details>
<div class="details-content">

指定输出数据类型。可以将其设置为：

- 继承数据类型的规则（例如，“Inherit: auto）”；
- 内置数据类型的名称（例如，float）；
- 计算结果为数据类型的表达式（例如，fixdt(1,16,0)）；
- 不要在表达式中将总线对象指定为数据类型，请使用 `Bus: <object name>` 指定总线数据类型。
<!-- - 如果您有 Computer Vision Toolbox™，请使用 [Simulink.ImageType](https://ww2.mathworks.cn/help/releases/R2022b/vision/ref/simulink.imagetype.html) (Computer Vision Toolbox) 对象的构造函数，并指定描述图像的属性。默认情况下，数据类型使用 Simulink.ImageType(480,640,3) 表达式，分别表示图像的行、列和通道。 -->

单击**显示数据类型帮助**按钮 <img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/DataStoreMemory/DataStoreMemory_button.png')" style="width: 80px; height: auto; vertical-align:middle; display:inline; margin:0;"> 以显示**数据类型帮助**，帮助您设置数据类型属性。  

</div>
</div>




  <!-- 有关详细信息，请参阅[使用数据类型助手指定数据类型]()。 -->

<!-- #### 编程用法

| **模块参数**：OutDataTypeStr                               |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值：**'Inherit: auto' | 'double' | 'single' | 'half' | 'int8' | 'uint8' | 'int16' | 'uint16' | 'int32' | 'uint32' | 'int64' | 'uint64' | 'boolean' | 'fixdt(1,16,0)' | 'fixdt(1,16,2^0,0)' | 'string' | 'Enum: <class name>' | 'Simulink.ImageType(480,640,3)' |
| **默认值：**'Inherit: auto'                                | -->



<!-- ### 锁定输出数据类型设置以防止被定点工具更改 — 防止定点工具覆盖输出数据类型 off （默认） | on



选择此参数可防止定点工具覆盖您在模块上指定的**输出**数据类型。有关详细信息，请参阅[Use Lock Output Data Type Setting](https://ww2.mathworks.cn/help/releases/R2022b/fixedpoint/ug/best-practices-for-using-the-fixed-point-tool-to-propose-data-types-for-your-simulink-model.html#br9an48) (Fixed-Point Designer)。

#### 编程用法

| **模块参数**：LockScale |
| ------------------------- |
| **类型：**字符向量        |
| **值：**'off' | 'on'    |
| **默认值：**'off'       | -->


<div class="details-box">
<details open>
<summary>维度(-1 表示从初始值推断) — 数据存储的维度<div>-1 （默认） | 标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

数据存储的维度。为默认值 -1 时，您可以使用**初始值**参数来设置数据存储的维度。但是，在这种情况下，不能将标量扩展用于初始值。您必须通过使用具有所需维度的数组来指定初始值。

如果使用除 -1 以外的值，则指定的维度必须与**初始值**参数的维度相同，除非将初始值指定为标量（用于标量扩展）或 Mlang 结构体。如果数据存储表示总线数组，并且初始值使用 MLang 结构体，则可以指定维度以使用此结构体初始化总线数组。

</div>
</div>


<!-- #### 编程用法

| **模块参数**：Dimensions   |
| ---------------------------- |
| **类型：**字符向量           |
| **值：**标量 \| 向量 \| 矩阵 |
| **默认值：**'-1'           | -->



<!-- ### 将向量参数解释为一维向量 — 将向量解释为一维 on （默认） | off



指定数据存储将向量初始值解释为一维。

默认情况下，MATLAB 将向量数据表示为具有两个维度的矩阵。例如，MATLAB 将向量 [1 2 3] 表示为一个 1×3 矩阵。

当选择此参数时，数据存储仅使用一维而不是二维来表示向量数据。例如，如果指定初始值 [1 2 3]，数据存储将存储包含三个元素的一维向量。

有关详细信息，请参阅 [确定源模块的输出维度](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/determining-output-signal-dimensions.html#bsud_ek-4)。

#### 编程用法

| **模块参数**：VectorParams1D |
| ------------------------------ |
| **类型**：字符向量             |
| **值**：'off' | 'on'         |
| **默认值**：'on'             | -->



<!-- ### 信号类型 — 数据存储值的复/实性 “自动” （默认） | “实数” | “复”



指定数据存储内的值的数值类型（实数或复数）。

#### 编程用法

| **模块参数**：SignalType            |
| ------------------------------------- |
| **类型：**字符向量                    |
| **值：**'auto' | 'real' | 'complex' |
| **默认值：**'auto'                  | -->



<!-- ### 跨模型实例共享 — 允许 Model 模块从同一个数据存储中读取数据 off （默认） | on



在单一模型引用层次结构中，当使用多个 Model 模块来引用包含 Data Store Memory 模块的模型时，默认情况下，引用模型的每个实例（每个 Model 模块）都针对数据存储的一个单独副本进行读写。当您选择**跨模型实例共享**而不是与单独副本进行交互时，所有实例都针对同一数据存储进行读写。

将模型配置参数**代码接口打包**设置为“可重用函数”以从模型生成可重入代码 (Simulink Coder™) 时，选择了**跨模型实例共享**的数据存储在代码中将作为生成的入口函数可以直接访问的全局符号出现。例如，全局符号可以是一个全局变量，也可以是全局结构体变量中的一个字段。因此，您的代码对入口函数的每个调用（模型的每个实例）都会共享数据。

有关示例，请参阅[Share Data Store Between Instances of a Reusable Algorithm](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/sharing-local-data-stores-across-multiple-instances-of-a-model.html)。有关详细信息，请参阅[在引用模型实例之间共享数据](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/define-referenced-model-inputs-and-outputs-1.html#mw_cf67482d-bf21-4aec-8eda-e8d60bd5d580)。

#### 编程用法

| **模块参数**：ShareAcrossModelInstances |
| ----------------------------------------- |
| **类型：**字符向量                        |
| **值：**'off' | 'on'                    |
| **默认值：**'off'                       | -->



<!-- ### 数据存储名称必须解析为 Simulink 信号对象 — 要求将数据存储名称解析为 Simulink 信号对象 off （默认） | on



指定 Simulink 软件在编译模型时需在模型和基础工作区中搜索具有相同名称的 [Simulink.Signal](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/simulink.signal.html) 对象，如[符号解析](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/resolving-symbols.html)中所述。如果 Simulink 找不到此类对象，将停止编译并显示错误。否则，Simulink 会将该信号对象的属性与 Data Store Memory 模块的对应属性进行比较。如果模块与对象的属性不一致，Simulink 将中断模型编译并显示错误。

#### 编程用法

| **模块参数**：StateMustResolveToSignalObject |
| ---------------------------------------------- |
| **类型：**字符向量                             |
| **值：**'off' | 'on'                         |
| **默认值：**'off'                            | -->

<!-- ### 诊断



### 检测写前读 — 模型在当前时间步中写入之前尝试读取数据时的操作 “警告” （默认） | “无” | “错误”



选择当模型试图从在当前时间步中未曾写入数据的数据存储中读取数据时要执行的诊断操作。另请参阅**模型配置参数** > **诊断** > **数据有效性** 窗格的 **Data Store Memory 模块**部分中的 [Detect read before write](https://ww2.mathworks.cn/help/releases/R2022b/simulink/gui/detect-read-before-write.html) 诊断。

- “无” - 不产生任何响应。
- “警告” - 显示警告并继续进行仿真。
- “错误” - 终止仿真并显示错误。

#### 编程用法

| **模块参数**：ReadBeforeWriteMsg     |
| -------------------------------------- |
| **类型：**字符向量                     |
| **值：**'none' | 'warning' | 'error' |
| **默认值：**'warning'                |



### 检测读后写 — 模块在同一时间步中读取数据后尝试写入时的操作 “警告” （默认） | “无” | “错误”



选择当模型试图向曾在当前时间步中读取过数据的数据存储中写入数据时要执行的诊断操作。另请参阅**模型配置参数** > **诊断** > **数据有效性** 窗格的 **Data Store Memory 模块**部分中的 [Detect write after read](https://ww2.mathworks.cn/help/releases/R2022b/simulink/gui/detect-write-after-read.html) 诊断。

- “无” - 不产生任何响应。
- “警告” - 显示警告并继续进行仿真。
- “错误” - 终止仿真并显示错误。

#### 编程用法

| **模块参数**：WriteAfterReadMsg      |
| -------------------------------------- |
| **类型：**字符向量                     |
| **值：**'none' | 'warning' | 'error' |
| **默认值：**'warning'                |



### 检测写后写 — 模型在同一时间步中写入两次时的操作 “警告” （默认） | “无” | “错误”



选择当模型试图在当前时间步中连续两次向数据存储中写入数据时要执行的诊断操作。另请参阅**模型配置参数** > **诊断** > **数据有效性** 窗格的 **Data Store Memory 模块**部分中的 [Detect write after write](https://ww2.mathworks.cn/help/releases/R2022b/simulink/gui/detect-write-after-write.html) 诊断。

- “无” - 不产生任何响应。
- “警告” - 显示警告并继续进行仿真。
- “错误” - 终止仿真并显示错误。

#### 编程用法

| **模块参数**：WriteAfterWriteMsg     |
| -------------------------------------- |
| **类型：**字符向量                     |
| **值：**'none' | 'warning' | 'error' |
| **默认值：**'warning'                | -->

<!-- ### 记录



### 记录数据存储数据 — 记录数据存储数据 off （默认） | on



选择此选项可在仿真过程中将此信号的值保存到 MATLAB 工作区。有关详细信息，请参阅[信号记录](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/exporting-signal-data-using-signal-logging.html#bsxca4i-3)。

#### 编程用法

| **模块参数**：DataLogging |
| --------------------------- |
| **类型：**字符向量          |
| **值：**'off' | 'on'      |
| **默认值：**'off'         |



### 记录名称 — 与记录的信号数据相关联的名称 “使用数据存储名称” （默认） | “自定义”



使用这一对控件（包括一个列表框和一个编辑字段）指定与记录的信号数据相关联的名称。

默认情况下，Simulink 使用信号名称作为其记录名称。要指定自定义记录名称，请从列表框中选择“自定义”，然后在旁边的编辑字段中输入自定义名称。

#### 编程用法

| **模块参数**：DataLoggingNameMode |
| ----------------------------------- |
| **类型：**字符向量                  |
| **值：**'SignalName' | 'Custom'   |
| **默认值：**''                    |



**注意**

如果将 DataLoggingNameMode 设置为 Custom，则必须使用 DataLoggingName 参数指定与记录信号数据相关联的名称。

| **模块参数：**DataLoggingName |
| ------------------------------- |
| **类型：**字符向量              |
| **值：**字符向量                |
| **默认值：**''                |



### 将数据点限制为最后 — 丢弃除最后 N 个数据点之外的所有数据 5000 | 非零整数



放弃除最后 N 个数据点之外的所有数据点，其中 N 是您在旁边的编辑字段中输入的数字。有关详细信息，请参阅[Log Data Stores](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/logging-data-stores.html)。

#### 编程用法

| **模块参数**：DataLoggingMaxPoints |
| ------------------------------------ |
| **类型：**字符向量                   |
| **值：**非零整数                     |
| **默认值：**'5000'                 |



### 抽取 — 记录每第 N 个数据点 2 （默认） | 整数



每 N 个数据点记录一次，其中 N 是您在相邻的编辑字段中输入的数字。例如，假设您的模型使用步长为 0.1 秒的定步长求解器。如果您选中此选项并接受默认抽取值 (2)，Simulink 将在 0.0、0.2、0.4 秒等时间记录此信号的数据点。有关详细信息，请参阅[Log Data Stores](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/logging-data-stores.html)。

#### 编程用法

| **模块参数**：DataLoggingLimitDataPoints |
| ------------------------------------------ |
| **类型：**字符向量                         |
| **值：**非零整数                           |
| **默认值：**'2'                          | -->



<!-- ## 模块特性

| **数据类型**     | Boolean | bus | double | enumerated | fixed point | half | integer | single | string |
| ---------------- | ------------------------------------------------------------ |
| **直接馈通**     | 是                                                         |
| **多维信号**     | 是                                                         |
| **可变大小信号** | 否                                                         |
| **过零检测**     | 否                                                         | -->

## 版本历史记录

- 在 2024b 之前推出

### 限制信息

1. 暂不支持在整个模型中重命名此数据存储；  
2. 暂不支持显示所连接的 DataStoreRead/Write 模块的路径；  
3. 暂不支持设定范围检查的最小、最大输出值；  
4. 暂不支持将向量参数解释为一维向量；  
5. 暂不支持对信号类型的选择；  
6. 暂不支持跨模型实例共享的复选框；  
7. 暂不支持数据存储名称必须解析为 Sysplorer 信号对象的复选框；  
8. 暂不支持检测写前读、读后写、写后写的功能；  
9. 暂不支持记录数据存储数据的功能；  
10. 暂不支持记录名称的选择；  
11. 暂不支持将数据点限制为最后的功能；  
12. 暂不支持抽取功能。

<!-- ## 扩展功能



### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。



### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。

要为使用 Data Store Memory 模块的模型生成 PLC 代码，请首先在基础工作区中定义 [Simulink.Signal](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/simulink.signal.html)。然后在模块参数的**信号属性**选项卡中，将数据存储名称设置为解析为 [Simulink.Signal](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/simulink.signal.html) 对象的名称。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。

## 版本历史记录

**在 R2006a 之前推出** -->


## 另请参阅

[DataStoreRead](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SignalRouting/DataStoreRead.html) | [DataStoreWrite](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SignalRouting/DataStoreWrite.html)

<!-- ### 主题

- [使用 Data Store Memory 模块存储数据](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/using-global-data-with-the-matlab-function-block.html#bsdud7d-1)
- [数据存储](https://ww2.mathworks.cn/help/releases/R2022b/simulink/data-stores.html)
- [选择如何存储全局数据](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/using-global-data-with-the-matlab-function-block.html#bsd28st)
- [模型接口元素的 C 代码生成配置](https://ww2.mathworks.cn/help/releases/R2022b/rtw/ug/c-code-generation-configuration-for-model-interface-elements.html) (Simulink Coder)
- [使用 Struct 存储类将参数数据组织为结构体](https://ww2.mathworks.cn/help/releases/R2022b/ecoder/ug/configure-parameters-for-code-generation.html#br0debj) (Embedded Coder)
- [使用 Simulink 模块访问数据存储](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/model-global-data-using-data-stores.html#f4-146588)
- [Log Data Stores](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/logging-data-stores.html) -->