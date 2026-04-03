# LookupTable1D
---
一维线性查表模块

**库：** Sysblock模块库 / LookupTable

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LookupTable/LookupTable1D/LookupTable1D.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

<!-- 暂无
### 支持的模块运算

1-D、2-D 和 n-D Lookup Table 模块计算一个函数的 N 变量采样表示

*y*=*F*(*x*1,*x*2,*x*3,...,*x**N*)

其中函数 F 可以是经验函数。此模块通过查找或插入您使用模块参数定义的值表，将输入映射到输出值。该模块支持均一（常量）、线性（线性点-斜率）、拉格朗日（线性拉格朗日）、最近、三次样条和 Akima 样条插值方法。您可以将这些方法应用于从 1 维到 30 维的表。

在下面的模块中，第一个输入标识第一个维度（行）断点，第二个输入标识第二个维度（列）断点，依此类推。
nawo
<img :src="$withBase('.png')" style="transform: scale(0.5);">

有关各种模块方向的端口顺序的描述，请参阅[旋转或翻转后的端口位置]()。

设置**数学和数据类型** > **使用针对行优先数组布局优化的算法**配置参数后，2-D 和 n-D Lookup Table 模块行为会从列优先更改为行优先。对于这些模块，列优先算法和行优先算法可能在输出计算的顺序上有所不同，从而可能导致数值略有不同。此功能需要 Simulink® Coder™ 或 Embedded Coder® 许可证。有关行优先支持的详细信息，请参阅[Code Generation of Matrices and Arrays]() (Simulink Coder)。 -->

### 模块说明

一维查表（LookupTable1D）是 Sysblock 中用于查找一维输入与输出之间的关系的模块。它通过将输入信号与预定义的表格数据进行比较，返回相应的输出值。该模块特别适用于输入与输出之间的非线性关系的建模，而无需明确的数据表达式。

### 基本功能

1. **输入输出映射**：该模块根据输入信号在预定义的表格中查找相应的输出值。输入信号的范围由用户指定的**断点向量**（breakpoints）决定。

2. **内插和外插方法**：当输入信号位于表格数据的离散点之间时，模块可以通过插值方法计算输出。常用的插值算法包括线性插值和其他插值方法。对于超出输入向量范围的值，模块还支持外插算法计算。

3. **高效计算**：使用查找表代替复杂的数学运算，能够显著提高仿真速度，尤其适用于实时系统。


### 指定值域和定义域


<!-- ::: tip 提示 
Sysblock环境的名词与Simulink环境内不一致，以Sysblock环境的名词为准。（表数据-值域、断点-定义域）
::: -->

以下模块参数定义断点和表数据。

| 模块参数   | 用途                                   |
| :--------- | :------------------------------------- |
| **定义域**   | 指定与一维查找表对应的断点向量。 |
| **值域** | 定义关联的一组输出值。                 |

<!-- 暂无
| **表维数** | 指定查找表的维度数。                   | -->

<!-- 暂无
**提示**

等间距断点可以使生成的代码无分割。有关详细信息，请参阅 [fixpt_evenspace_cleanup](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/fixpt_evenspace_cleanup.html) 和[Identify questionable fixed-point operations](https://ww2.mathworks.cn/help/releases/R2022b/ecoder/ref/embedded-codersimulink-coder-checks.html#braj1_6-23) (Embedded Coder)。 -->

### 模块如何生成输出

LookupTable1D 模块通过基于输入值查找或估计表值来生成输出。

| 模块输入                                   | LookupTable1D 模块行为                |
| :----------------------------------------- | :----------------------------------------- |
| 与断点数据集中的索引值匹配                 | 输出位于行断点的交点处的表值 |
| 与断点数据集中的索引值不匹配，但在范围内   | 使用您选择的**内插方法**内插适当的表值     |
| 与断点数据集中的索引值不匹配，且不在范围内 | 使用您选择的**外插方法**外插输出值         |

<!-- 暂无
### 执行等效操作的其他模块

您可以将 [Interpolation Using Prelookup](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/interpolationusingprelookup.html) 模块与 [Prelookup](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/prelookup.html) 模块一起使用，以执行等效于一个 n-D Lookup Table 模块的操作。这种模块组合可以提供更大的灵活性，从而为线性插值实现更高效的仿真性能。

当查找操作是不需要插值的数组访问时，请使用 [Direct Lookup Table (n-D)](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/directlookuptablend.html) 模块。例如，如果您有一个整数值 k，而您需要表的第 k 个元素 y = table(k)，则不需要插值。 -->

## 示例

<!-- 暂无
[![创建对数查找表](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/createlogarithmlookuptableexample_01_zh_CN.png)创建对数查找表此示例说明如何使用 n-D Lookup Table 模块来创建对数查找表。](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/create-log-lookup-table.html)

[![防抱死制动系统建模](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/modelinganantilockbrakingsystemexample_07_zh_CN.png)防抱死制动系统建模此示例说明如何对防抱死制动系统 (ABS) 进行简单建模。它对车辆在紧急制动情况下的动态行为进行仿真。该模型表示单个车轮，可以重复多次以创建多轮车辆的模型。](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/modeling-an-anti-lock-braking-system.html) -->

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LookupTable/LookupTable1D.mo">LookupTable1D.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LookupTable/LookupTable1D/LookupTable1D_ex.png')" style="width:600px; transform: scale(0.8);">

### 示例说明

- Ramp 模块：提供线性增加的输入信号，用于模拟实际输入值；
- LookupTable1D 模块：根据输入信号的值在查找表中查找对应的输出值。如果输入值位于两个断点之间，则根据设置的插值方法进行插值计算；如果输入值超出断点范围，则根据设置的外推方法进行处理；
- Scope 模块：用于显示模型的输出结果，即查找表映射后的输出信号。

## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 一维（行）输入<div>标量</div></summary>
</details>
<div class="details-content">

**u** 端口的实数值输入，通过查找您定义的值表或对其进行插值来映射到输出值。

**数据类型：** float | double | int8 | int16 | int32 | fixedPoint

</div>
</div>
<!-- ::: tip 提示 
Simulink环境将N维查表模块统一说明
::: -->



<!-- 暂无
### T — 定义输出值的表 值组成的矩阵，其维度与**表维数**匹配，每个维度与表中每个维度的断点长度匹配



用运行时可调的信号指定输出值表。

在仿真期间，矩阵大小必须与**表维数**参数定义的维度匹配。但是，在编辑模块图的过程中，您可以输入空矩阵（指定为 []）或者未定义的工作区变量。利用此方法，您可以推迟为表数据指定正确设置维度的矩阵，并继续编辑模块图。

#### 依存关系

要启用此端口，请进行如下设置：

- 将**数据设定**设置为“表和断点”。
- 将**表数据**设置为“输入端口”。

**数据类型：** half | single | double | int8 | int16 | int32 | int64 | uint8 | uint16 | uint32 | uint64 | fixed point -->


<!-- 暂无
### bp1 — 显式断点值 单调递增值的 1×n 或 n×1 向量



根据**断点设定**参数的值，使用运行时可调的信号显式指定断点数据。

- 如果您将**断点设定**设置为“显式值”，请在每个**断点**行中输入与表数据的每个维度对应的断点集。对于每个维度，将断点指定为值严格单调递增的 1×n 或 n×1 向量。



**注意**

要以等间距设定格式指定断点，请将**断点设定**设置为“等间距”，并使用**断点的第一个**点和**间距**参数。

#### 依存关系

要启用此端口，请进行如下设置：

- 将**数据设定**设置为“表和断点”。
- 将**断点设定**设置为“显式值”。
- 将**断点 1** 设置为“输入端口”。

**数据类型：** half | single | double | int8 | int16 | int32 | int64 | uint8 | uint16 | uint32 | uint64 | enumerated | fixed point -->

### 输出

<div class="details-box">
<details open>
<summary>y — 通过查找或估算表值计算的输出<div>标量</div></summary>
</details>
<div class="details-content">

通过查找或基于输入值估算表值生成的输出。

| 如果模块输入...                            | LookupTable1D 模块...                   |
| :----------------------------------------- | :----------------------------------------- |
| 与断点数据集中的索引值匹配                 | 输出位于行断点的交点处的表值 |
| 与断点数据集中的索引值不匹配，但在范围内   | 使用您选择的**内插方法**内插适当的表值     |
| 与断点数据集中的索引值不匹配，且不在范围内 | 使用您选择的**外插方法**外插输出值         |

**数据类型：** float | double | int8 | int16 | int32 | fixed point

</div>
</div>


## 参数

### 值域和定义域

<!-- 暂无
### 表维数 — 查找表维度的数量 1 （默认） | 2 | 3 | 4 | ... | 30



输入查找表的维数。此参数确定：

- 表的自变量数量以及模块输入的数量
- 要指定的断点集的数量

| 要指定...    | 执行此操作...                                         |
| :----------- | :---------------------------------------------------- |
| 1、2、3 或 4 | 从下拉列表中选择值。                                  |
| 更高的表维数 | 直接在字段中输入正整数。此模块支持的最大表维数为 30。 |

例如，大小为 M×N×... 的表表示维度 1 的大小是 M，维度 2 的大小是 N，依此类推。M 必须匹配第一个断点长度，N 必须匹配第二个断点长度，依此类推。

#### 编程用法

| **模块参数**：NumberOfTableDimensions    |
| ------------------------------------------ |
| **类型：**字符向量                         |
| **值：**'1' | '2' | '3' | '4' | ... | 30 |
| **默认值：**'1'                          | -->

<!-- 
暂无
### 数据设定 — 表和断点的设定方法 “表和断点” （默认） | “查找表对象”



从列表中，选择：

- “表和断点” - 指定表数据和断点。选中此选项将启用下列参数：

  - **表数据**
  - **断点设定**
  - **断点 1**
  - **编辑表和断点**

  

  要使用输入端口指定表和断点，请查看**源**参数。

- “查找表对象” - 使用现有查找表 (Simulink.LookupTable) 对象。选中此选项将启用**名称**字段和**编辑表和断点**按钮。

#### 编程用法

| **模块参数**：DataSpecification                         |
| --------------------------------------------------------- |
| **类型：**字符向量                                        |
| **值：**'Table and breakpoints' | 'Lookup table object' |
| **默认值：**'Table and breakpoints'                     | -->


<!-- 暂无
### 名称 — 查找表对象的名称 [] （默认） | Simulink.LookupTable 对象



输入查找表 (Simulink.LookupTable) 对象的名称。如果 Simulink.LookupTable 对象不存在，请单击操作按钮 ![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/lookup_table_nd_createobject.png) 并选择**创建**。新查找表对象的对应参数会自动用模块信息填充。

#### 依存关系

要启用此参数，请将**数据设定**设置为“查找表对象”。

#### 编程用法

| **模块参数**：LookupTableObject         |
| ----------------------------------------- |
| **类型：**字符向量                        |
| **值：**Simulink.LookupTable 对象的名称 |
| **默认值：**''                          | -->


<!-- 暂无
### 断点设定 — 断点设定的方法 “显式值” （默认） | “等间距”



指定是以显式断点形式还是参数形式输入数据，以生成等间距断点。

- 要显式指定断点数据，请将此参数设置为“显式值”，并在**断点**参数旁边的文本框中输入断点数据。
- 要指定参数以生成等间距断点，请将此参数设置为“等间距”，并为断点数据的每个维度的**第一个点**和**间距**参数输入值。模块将根据表数据计算要生成的点数。

#### 依存关系

要启用此参数，请将**数据设定**设置为“表和断点”。

#### 编程用法

| **模块参数**：BreakpointsSpecification     |
| -------------------------------------------- |
| **类型：**字符向量                           |
| **值：**'Explicit values' | 'Even spacing' |
| **默认值：**'Explicit values'              | -->


<!-- 暂无
### 源 — 表和断点数据的源 “对话框” （默认） | “输入端口”



表和断点数据的源，指定为：

- “对话框” - 在**值**参数中指定表或断点数据。

- “输入端口” - 通过关联的输入端口指定表或断点数据。

  您最多可以创建三个断点数据输入端口。对于断点 4 到 30，您只能通过对应的**断点**参数指定断点数据。



**注意**

使用输入端口指定表或断点数据可能会因为运行时检查对仿真的模块性能产生负面影响。

#### 依存关系

- 要启用此参数，请将**数据设定**设置为“表和断点”。
- 要启用关联的**值**，请将此参数设置为“对话框”。
- 要启用相关联的输入端口，请将此参数设置为“输入端口”。
- 将此参数设置为“输入端口”将禁用**值**字段，并隐藏**数据类型**选项卡上的对应参数。
- 对于任一参数，将此参数设置为“输入端口”都会禁用**编辑表和断点**按钮。

#### 编程用法

| **模块参数：**TableSource | BreakpointsForDimension1Source | BreakpointsForDimension2Source | BreakpointsForDimension3Source |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值**：Dialog | Input port                              |
| **默认值：**'Dialog'                                       | -->


<div class="details-box">
<details open>
<summary>值域 — 定义输出值的表<div>{1, 10, 7, 12, 16} （默认） | 值的向量</div></summary>
</details>
<div class="details-content">

在相关联的**值**字段中输入输出值的表。

</div>
</div>



<!-- 暂无
在仿真期间，矩阵大小必须与**表维数**参数定义的维度匹配。但是，在编辑模块图的过程中，您可以输入空矩阵（指定为 []）或者未定义的工作区变量。利用此方法，您可以推迟为表数据指定正确设置维度的矩阵，并继续编辑模块图。 -->

<!-- 暂无
#### 依存关系

要启用此参数，请进行如下设置：

- 将**数据设定**设置为“表和断点”。
- 将**表数据:源**设置为“对话框”。

#### 编程用法

| **模块参数**：Table        |
| ---------------------------- |
| **类型：**字符向量           |
| **值：**表值的向量           |
| **默认值：**'tanh([-5:5])' | -->



<div class="details-box">
<details open>
<summary>定义域 — 显式定义域值，或定义域的第一个点和间距<div>{5, 6, 7, 11, 30} （默认） | 单调递增值的 1×n 或 n×1 向量</div></summary>
</details>
<div class="details-content">



</div>
</div>

<!-- 暂无
显式指定断点数据或者指定为等间距断点，具体取决于**断点设定**参数。



- 如果您将**断点设定**设置为“显式值”，请在每个**断点**行中输入与表数据的每个维度对应的断点集。对于每个维度，将断点指定为值严格单调递增的 1×n 或 n×1 向量。
- 如果您将**断点设定**设置为“等间距”，请在每个**断点**行中输入参数**第一个点**和**间距**，以便在各自的维度生成等间距断点。您的表数据决定等距点数。 -->

<!-- 暂无
#### 依存关系

- 要启用此参数，请进行如下设置：
  - 将**数据设定**设置为“表和断点”。
  - 将**表数据:源**设置为“对话框”。
- 当**断点设定**参数设置为“等间距”时，您只能通过对话框指定断点数据。

#### 编程用法

| **模块参数**：BreakpointsForDimension1 |
| ---------------------------------------- |
| **类型：**字符向量                       |
| **值：**单调递增值的 1×n 或 n×1 向量     |
| **默认值：**'[10, 22, 31]'             | -->


<!-- 暂无
### 第一个点 — 等间距断点数据中的第一个点 1 （默认） | 标量



将等间距断点数据中的第一个点指定为实数值有限标量。当**断点设定**设置为“等间距”时，此参数可用。

#### 依存关系

要启用此参数，请将**数据设定**设置为“表和断点”，并将**断点设定**设置为“等间距”。

#### 编程用法

| **模块参数**：BreakpointsForDimension1FirstPoint |
| -------------------------------------------------- |
| **类型：**字符向量                                 |
| **值：**实数值有限标量                             |
| **默认值：**'1'                                  | -->


<!-- 暂无
### 间距 — 等间距断点之间的间距 1 （默认） | 标量



指定等间距断点数据中各点之间的距离。

#### 依存关系

要启用此参数，请将**数据设定**设置为“表和断点”，并将**断点设定**设置为“等间距”。

#### 编程用法

| **模块参数**：BreakpointsForDimension1Spacing |
| ----------------------------------------------- |
| **类型：**字符向量                              |
| **值：**正实数值有限标量                        |
| **默认值：**'1'                               | -->


<div class="details-box">
<details open>
<summary>编辑值域和定义域 — 启动“编译值域和定义域”对话框<div>按钮</div></summary>
</details>
<div class="details-content">

单击此按钮以打开查找表编辑器。

对于查找表对象，单击此按钮可以编辑该对象并为该对象保存新值。

</div>
</div>




<!-- 暂无
有关详细信息，请参阅 [Edit Lookup Tables](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/use-the-lookup-table-editor.html#bqissk7-1)。 -->






### 算法

<!-- **查找方法** -->


<div class="details-box">
<details open>
<summary>内插方法 — 断点值之间插值的方法<div>“线性点-斜率” （默认） | “均一” | “最邻近值” | “线性拉格朗日”</div></summary>
</details>
<div class="details-content">

当输入位于两个断点值之间时，模块将根据相邻断点内插输出值。

</div>
</div>
<!-- 暂无
 | “三次样条” | “Akima 样条” -->



<!-- 暂无
有关插值方法的详细信息，请参阅[内插方法](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/methods-for-estimating-missing-points.html#bqi6gig)。 -->

<!-- 暂无
##### 依存关系

- 如果您选择“三次样条”，则模块仅支持标量信号。其他插值方法支持非标量信号。

- 如果选择 “Akima 样条”，外插方法只能是 “Akima 样条”。

  当设置为修正 Akima 插值方法时，此模块不支持：

  - 行优先数组布局和针对行优先数组布局优化的算法
  - 定标的双精度和定点数据类型
  - Simulink.LookupTable 对象
  - 选中配置参数**代码生成** > **接口** > **支持非有限数**复选框时的代码生成

  当设置为修正 Akima 插值方法时，如果以下条件成立，此模块的运行速度会更慢：

  - 基于代码生成的仿真目标，如加速模式、快速加速模式、受保护模型等的仿真目标。
  - 为大型断点和数据表生成的代码。例如，表大小为 629×1601。 -->

<!-- 暂无
#### 编程用法

| **模块参数**：InterpMethod                                 |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值：**'Linear point-slope' | 'Flat' | 'Nearest' | 'Linear Lagrange' | 'Cubic spline' | 'Akima spline' |
| **默认值：**'Linear point-slope'                           | -->



<div class="details-box">
<details open>
<summary>外插方法 — 处理超出断点数据集范围的输入值的方法<div>“线性” （默认） | “裁剪”</div></summary>
</details>
<div class="details-content">

选择“裁剪”或“线性”。

如果外插方法是“线性”，则基于所选择的线性插值方法计算外插值。例如，如果插值方法是线性拉格朗日，则外插方法继承线性拉格朗日方程以计算外插值。

</div>
</div>
<!-- 暂无
 | “三次样条” | “Akima 样条” -->






<!--暂无 
有关详细信息，请参阅[外插方法](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/methods-for-estimating-missing-points.html#bqi6giz)。 -->



<!-- 暂无
##### 依存关系

- 要为**外插方法**选择“三次样条”，还必须为**内插方法**选择“三次样条”。
- 要为**外插方法**选择 “Akima 样条”，您还必须为**内插方法**选择 “Akima 样条”。 -->

<!-- 暂无
#### 编程用法

| **模块参数**：ExtrapMethod                                 |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值：**'Linear' | 'Clip' | 'Cubic spline' | 'Akima spline' |
| **默认值：**'Linear'                                       | -->



<div class="details-box">
<details open>
<summary>索引搜索方法 — 计算表索引的方法<div>“线性搜索”（默认） | “二分搜索”</div></summary>
</details>
<div class="details-content">

选择**线性搜索**或**二分搜索**。每一种搜索方法在不同的情况下均有各自的速度优势：

  - 如果输入信号在时间步之间的变化不大，选择**线性搜索**可以获得最佳性能；
  - 如果输入信号在每个时间步中跳过的表间隔超过一个或两个，选择**二分搜索**可以获得最佳性能。

对于严重依赖查找表的模型，选择次优索引搜索方法可能会导致性能下降。

</div>
</div>
<!-- 暂无
 “等距点”  | -->



<!-- 暂无
- 对于等间距断点集（例如，10、20、30 等），您可以选择 Evenly spaced points 来计算表索引，以获得最佳速度。

  此算法仅使用断点集的前两个断点来确定其余点的偏移量和间距。

  

  **注意**

  当使用 Simulink.LookupTable 对象指定表数据且引用的 Simulink.LookupTable 对象的**断点设定**参数设置为“等间距”时，请将**索引搜索方法**设置为“等距点”。 -->




<!-- 暂无
**注意**

在以下情况下，生成的代码只存储第一个断点、间距和断点数量：

- 断点数据不可调。
- 索引搜索方法为 Evenly spaced points。 -->

<!-- 暂无
#### 编程用法

| **模块参数**：IndexSearchMethod                            |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值：**'Binary search' | 'Evenly spaced points' | 'Linear search' |
| **默认值：**'Binary search'                                | -->


<!-- 暂无
### 使用上一个索引结果开始索引搜索 — 开始使用来自上一时间步的索引 off （默认） | on



如果您希望模块使用在上一个时间步中找到的索引开始搜索，请选中此复选框。对于相对于间隔大小而言变化缓慢的输入，启用此选项可以提高性能。否则，线性搜索和二分搜索方法可能需要更长的时间，尤其是对于大型断点集来说。

#### 依存关系

要启用此参数，请将**索引搜索方法**设置为“线性搜索”或“二分搜索”。

#### 编程用法

| **模块参数**：BeginIndexSearchUsingPreviousIndexResult |
| -------------------------------------------------------- |
| **类型：**字符向量                                       |
| **值：**'off' | 'on'                                   |
| **默认值：**'off'                                      | -->


<!-- 暂无
### 输入超出范围的诊断 — 当输入超出范围时的模块操作 “无” （默认） | “警告” | “错误”



指定当输入超出范围时，是否生成警告或错误消息。选项包括：

- “无” - 不产生任何响应。
- “警告” - 显示警告并继续进行仿真。
- “错误” - 终止仿真并显示错误。

#### 编程用法

| **模块参数**：DiagnosticForOutOfRangeInput |
| -------------------------------------------- |
| **类型：**字符向量                           |
| **值：**'None' | 'Warning' | 'Error'       |
| **默认值：**'None'                         | -->


<!-- 暂无
### 尽可能应用全精度定点算法 — 更精确的定点表查找 off （默认） | on



尽可能使用此复选框为线性插值查找启用全精度定点算法查找。对于硬件效率高的定点舍入模式，此算法通常可以实现更高的精度。

#### 依存关系

要启用此参数，请进行如下设置：

- 将**表维数**设置为 “1”。
- 将**内插方法**设置为“线性点-斜率”。
- 将**外插方法**设置为“裁剪”。

#### 编程用法

| **模块参数**：ApplyFullPrecisionForLinearInterpolation |
| -------------------------------------------------------- |
| **类型：**字符向量                                       |
| **值：**'off' | 'on'                                   |
| **默认值：**'off'                                      | -->


<!-- 暂无
### 输入等于或高于最后一个断点时使用最后一个表值 — 用于计算最后一个断点上或高于该断点的输入的输出的方法 off （默认） | on



使用此复选框，指定模块用来定位断点集的最后一个元素及其对应表值的索引约定。当输入等于或大于断点数据的最后一个元素时，此复选框才有意义。由于舍入原因，选中和清除此复选框可能会导致仿真与代码生成之间最后一个断点的结果不同。

| 复选框 | 模块使用的索引                                 | 区间比 |
| :----- | :--------------------------------------------- | :----- |
| 选中   | **表和断点**选项卡上的断点数据的最后一个元素   | 0      |
| 清除   | **表和断点**选项卡上的断点数据的倒数第二个元素 | 1      |

假设输入 u 在断点集 bp 的范围内，区间比 f（在 0≦f<1 范围内）按如下所示进行计算。

![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/interval_fraction_diagram.png)

假定断点集为 [1 4 5]，输入 u 为 5.5。如果您选中此复选框，索引则是最后一个元素 (5) 的索引，区间比为 0。如果您清除此复选框，索引则是倒数第二个元素 (4) 的索引，区间比为 1。

#### 依存关系

要启用此参数，请进行如下设置：

- 将**内插方法**设置为“线性”。
- 将**外插方法**设置为“裁剪”。



#### 编程用法

| **模块参数**：UseLastTableValue |
| --------------------------------- |
| **类型：**字符向量                |
| **值：**'off' | 'on'            |
| **默认值：**'off'               |

**输入设置** -->


<!-- 暂无
### 所有输入数据使用一个输入端口 — 只使用一个输入端口 off （默认） | on



选中此复选框，从而对 N 维表只使用一个输入端口，此端口需要宽度为 n 个元素的信号。此选项可以有效减少包含许多查找表的模块图中的杂乱线条。



**注意**

如果您选中此复选框，模块上将出现一个带有 u 标签的输入端口。

#### 编程用法

| **模块参数**：UseOneInputPortForAllInputData |
| ---------------------------------------------- |
| **类型：**字符向量                             |
| **值：**'off' | 'on'                         |
| **默认值：**'off'                            |

**代码生成** -->


<!-- 暂无
### 删除生成代码中防止超范围输入的代码 — 删除检查超出范围的输入值的代码 off （默认） | on



指定是否包含代码以检查超出范围的输入值。

| 复选框 | 结果                                                         | 何时使用                       |
| :----- | :----------------------------------------------------------- | :----------------------------- |
| on   | 生成的代码中未包含用来检查超出范围的断点输入的条件语句。当输入超出范围时，生成的代码可能会发生未定义的行为。 | 提高代码效率                   |
| off  | 生成的代码包含用来检查超出范围的输入的条件语句。             | 适用于安全性至关重要的应用领域 |

如果您的输入没有超出范围，则可以选中**删除生成代码中防止超范围索引的代码**复选框以提高代码效率。默认情况下，此复选框处于清除状态。对于安全性至关重要的应用，不要选中此复选框。要选中**删除生成代码中防止超范围索引的代码**复选框，请先检查模型输入是否在范围内。例如：

1. 清除**删除生成代码中防止超范围索引的代码**复选框。

2. 将**输入超出范围的诊断**参数设置为 Error。

3. 在普通模式下进行模型仿真。

4. 如果发生超出范围错误，请将它们更正到范围之内，然后再次运行仿真。

5. 当仿真不再生成超出范围的输入错误时，选中**删除生成代码中防止超范围索引的代码**复选框。

   

   **注意**

   如果选中了**删除生成代码中防止超范围索引的代码**复选框而输入超出范围，生成的代码将发生未定义的行为。

根据您的具体应用，您可以运行以下模型顾问检查，以验证此复选框的使用情形：

- **按产品** > **Embedded Coder** > **标识哪些查找表模块会生成检查超范围值的高成本代码**
- **按产品** > **Simulink Check** > **建模标准** > **DO-178C/DO-331 检查** > **检查 Lookup Table 模块的使用情形**

有关模型顾问的详细信息，请参阅[运行模型顾问检查](https://ww2.mathworks.cn/help/releases/R2022b/simulink/run-model-checks.html)。

此外，要确定选中此复选框是否安全，如果您拥有 Simulink Design Verifier™ 许可证，请考虑使用 [Detect Block Input Range Violations](https://ww2.mathworks.cn/help/releases/R2022b/sldv/ref/simulink-design-verifier-checks.html#mw_e106ff95-dfb6-455f-ae2f-4552e7c2a799) (Simulink Design Verifier) 检查。

#### 编程用法

| **模块参数**：RemoveProtectionInput |
| ------------------------------------- |
| **类型：**字符向量                    |
| **值：**'off' | 'on'                |
| **默认值：**'off'                   | -->


<!-- 暂无
### 在代码生成中支持可调表大小 — 在生成的代码中启用可调表大小 off （默认） | on



选中此复选框，以使生成的代码中具有可调表大小。利用此选项，您可以更改生成的代码中的查找表与断点数据的大小和值，无需重新生成或重新编译代码。您只能减小查找表和断点数据的大小。

#### 依存关系

如果您将**内插方法**设置为“三次样条”，此复选框将不可用。

#### 编程用法

| **模块参数**：SupportTunableTableSize |
| --------------------------------------- |
| **类型：**字符向量                      |
| **值：**'off' | 'on'                  |
| **默认值：**'off'                     | -->


<!-- 暂无
### 采样时间 — -1 以外的采样时间值 -1 （默认） | 标量 | 向量



将采样时间指定为 -1 以外的值。有关详细信息，请参阅[指定采样时间](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/how-to-specify-the-sample-time.html)。

#### 依存关系

此参数不可见，除非将其显式设置为 -1 以外的值。要了解详细信息，请参阅[不建议设置采样时间的模块](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/sampletimehiding.html)。

#### 编程用法

| **模块参数：**SampleTime     |
| ------------------------------ |
| **类型：**字符串标量或字符向量 |
| **默认值：**"-1"             | -->


<!-- 暂无
### 每个维度的最大索引 — 每个表维度的最大索引值 [] （默认） | scalar or vector of positive integer values



**示例：** [4 6] 用于表示 5×7 的表

使用从零开始的索引方法指定每个表维度的最大索引值。您可以使用以下数据类型，指定正整数标量或向量值：

- 内置浮点类型：double 和 single
- 内置整数类型：int8、int16、int32、uint8、uint16 和 uint32

有效设定的示例包括：

- [4 6] 用于表示 5×7 的表
- [int8(2) int16(5) int32(9)] 用于表示 3×6×10 的表
- Simulink.Parameter，在生成代码后此参数的值比表数据的维度少一。有关详细信息，请参阅[在生成的代码中具有可调表大小](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/1dlookuptable.html#f7-890882_sep_bs0jby5)。

#### 依存关系

要启用此参数，请选择**在代码生成中支持可调表大小**。通过在生成的代码中调整此参数，提供新的表数据和断点以及调整后的参数值。

#### 编程用法

| **模块参数**：MaximumIndicesForEachDimension |
| ---------------------------------------------- |
| **类型：**字符向量                             |
| **值：**正整数值的标量或向量                   |
| **默认值：**'[]'                             | -->

### 数据信息


<!-- 暂无
### 表数据 — 表数据的数据类型 “Inherit: Same as output” （默认） | “double” | “single” | “half” | “int8” | “uint8” | “int16” | “uint16” | “int32” | “uint32” | “int64” | “uint64” | “fixdt(1,16)” | “fixdt(1,16,0)” | “fixdt(1,16,2^0,0)” | “<数据类型表达式>”



指定表数据类型。可以将其设置为：

- 继承数据类型的规则，例如 “Inherit: Same as output”
- 内置数据类型的名称，例如 single
- 数据类型对象的名称，例如 Simulink.NumericType 对象
- 计算结果为数据类型的表达式，例如 fixdt(1,16,0)

单击**显示数据类型助手**按钮 ![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/show_data_type_asst_button.png) 以显示**数据类型助手**，帮助您设置数据类型属性。有关详细信息，请参阅[使用数据类型助手指定数据类型](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/specify-data-types-using-data-type-assistant.html)。



**提示**

对于以下情况，指定与输出数据类型不同的表数据类型：

- 存储表数据（使用的类型小于输出信号）的内存要求较低
- 在具有不同输出数据类型的两个 n-D Lookup Table 模块之间共享预缩放的表数据
- 在为具有不同输出数据类型的模块生成的代码中共享自定义存储表数据

#### 依存关系

要启用此参数，请将**表和断点**选项卡中的**表数据**设置为“对话框”。

#### 编程用法

| **模块参数**：TableDataTypeStr                             |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值：**'Inherit: Inherit from 'Table data'' | 'Inherit: Same as output' | 'double' | 'single' | 'half' | 'int8' | 'uint8' | 'int16' | 'uint16' | 'int32' | 'uint32' | 'int64' | 'uint64' | 'fixdt(1,16)' | 'fixdt(1,16,0)' | 'fixdt(1,16,2^0,0)'|'<data type expression>' |
| **默认值：**'Inherit: Same as output'                      | -->


<div class="details-box">
<details open>
<summary>值域最小值 — 值域的最小值<div>[] | scalar</div></summary>
</details>
<div class="details-content">

指定值域的最小值。默认值为 []（未指定）。

</div>
</div>




<!-- 暂无
#### 编程用法

| **模块参数**：TableMin |
| ------------------------ |
| **类型：**字符向量       |
| **值：**标量             |
| **默认值：**'[]'       | -->



<div class="details-box">
<details open>
<summary><div>值域最大值 — 值域的最大值</div>[] | scalar</summary>
</details>
<div class="details-content">

指定值域的最大值。默认值为 []（未指定）。

</div>
</div>




<!-- 暂无
#### 编程用法

| **模块参数**：TableMax |
| ------------------------ |
| **类型：**字符向量       |
| **值：**标量             |
| **默认值：**'[]'       | -->


<!-- 暂无
### 断点 — 断点数据类型 “Inherit: Same as corresponding input” （默认） | “double” | “single” | “half” | “int8” | “uint8” | “int16” | “uint16” | “int32” | “uint32” | “int64” | “uint64” | “fixdt(1,16)” | “fixdt(1,16,0)” | “fixdt(1,16,2^0,0)” | “Enum: <class name>” | “<数据类型表达式>”



指定一组断点数据的数据类型。可以将其设置为：

- 继承数据类型的规则，例如 “Inherit: Same as corresponding input”
- 内置数据类型的名称，例如 single
- 数据类型类的名称，例如枚举数据类型类
- 数据类型对象的名称，例如 Simulink.NumericType 对象
- 计算结果为数据类型的表达式，例如 fixdt(1,16,0)



**提示**

- 断点支持无序枚举数据。因此，线性搜索也是无序的，这就提供了灵活性，但可能影响性能。搜索从断点中的第一个元素开始。
- 如果选中**使用上一个索引结果开始索引搜索**复选框，则必须使用有序单调递增数据。这种排序可提高性能。
- 对于枚举数据，**外插方法**必须是 Clip。
- 该模块不支持枚举数据的超出范围的输入。指定枚举数据时，请将整个枚举集包含在断点数据集中。例如，使用 [enumeration](https://ww2.mathworks.cn/help/releases/R2022b/matlab/ref/enumeration.html) 函数。

以下是对此模块使用枚举数据的限制：

- 该模块不支持枚举数据的超出范围的输入。指定枚举数据时，请将整个枚举集包含在断点数据集中。例如，使用 [enumeration](https://ww2.mathworks.cn/help/releases/R2022b/matlab/ref/enumeration.html) 函数。

单击**显示数据类型助手**按钮 ![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/show_data_type_asst_button.png) 以显示**数据类型助手**，帮助您设置数据类型属性。有关详细信息，请参阅[使用数据类型助手指定数据类型](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/specify-data-types-using-data-type-assistant.html)。



**提示**

对于以下情况，指定的断点数据类型可以不同于对应的输入数据类型：

- 存储断点数据（使用的类型小于输出信号）的内存要求较低
- 在具有不同输入数据类型的两个 n-D Lookup Table 模块之间共享预缩放的断点数据
- 在为具有不同输入数据类型的模块生成的代码中共享自定义存储断点数据

如果断点数据类型或其对应的输入数据类型具有定点数据类型，请为二者指定相同的斜率和偏置。

#### 依存关系

要启用此参数，请将**表和断点**选项卡中对应的**断点**参数设置为“对话框”。

#### 编程用法

| **模块参数**：BreakpointsForDimension1DataTypeStr | BreakpointsForDimension2DataTypeStr| ... | BreakpointsForDimension30DataTypeStr |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值：**'Inherit: Same as corresponding input' | 'Inherit: Inherit from 'Breakpoint data'' | 'double' | 'single' | 'half' | 'int8' | 'uint8' | 'int16' | 'uint16' | 'int32' | 'uint32' | 'int64' | 'uint64' | 'fixdt(1,16)' | 'fixdt(1,16,0)' | 'fixdt(1,16,2^0,0)'|'<data type expression>' |
| **默认值：**'Inherit: Same as corresponding input'         | -->


<div class="details-box">
<details open>
<summary><div>定义域最小值 — 最小值断点数据可以有</div>[] | scalar</summary>
</details>
<div class="details-content">

指定一组断点数据可以具有的最小值。默认值为 []（未指定）。

</div>
</div>




<!-- 暂无
#### 编程用法

| **模块参数**：BreakpointsForDimension1Min | BreakpointsForDimension2Min | ... | BreakpointsForDimension30Min |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值：**标量                                                 |
| **默认值：**'[]'                                           | -->


<div class="details-box">
<details open>
<summary>定义域最大值 — 最大值断点数据可以有<div>[] | scalar</div></summary>
</details>
<div class="details-content">

指定一组断点数据可以具有的最大值。默认值为 []（未指定）。

</div>
</div>




<!-- 暂无
#### 编程用法

| **模块参数**：BreakpointsForDimension1Max | BreakpointsForDimension2Max | ... | BreakpointsForDimension30Max |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值：**标量                                                 |
| **默认值：**'[]'                                           | -->


<!-- 暂无
### 区间比 — 区间比数据类型 “Inherit: Inherit via internal rule” （默认） | “double” | “single” | “fixdt(1,16,0)” | “<数据类型表达式>”



指定区间比数据类型。可以将其设置为：

- 继承数据类型的规则，例如 “Inherit: Inherit via internal rule”
- 内置数据类型的名称，例如 single
- 数据类型对象的名称，例如 Simulink.NumericType 对象
- 计算结果为数据类型的表达式，例如 fixdt(1,16,0)

单击**显示数据类型助手**按钮 ![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/show_data_type_asst_button.png) 以显示**数据类型助手**，帮助您设置数据类型属性。有关详细信息，请参阅[使用数据类型助手指定数据类型](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/specify-data-types-using-data-type-assistant.html)。

#### 编程用法

| **模块参数**：FractionDataTypeStr                          |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值：**'Inherit: Inherit via internal rule' | 'double' | 'single' | 'fixdt(1,16,0)'|'<data type expression>' |
| **默认值：**'Inherit: Inherit via internal rule'           | -->


<!-- 暂无
### 中间结果 — 中间结果数据类型 “Inherit: Same as output” （默认） | “Inherit: Inherit via internal rule” | “double” | single | “int8” | “uint8” | “int16” | “uint16” | “int32” | “uint32” | “int64” | “uint64” | “fixdt(1,16,0)” | “fixdt(1,16,2^0,0)” | “<数据类型表达式>”



指定中间结果数据类型。可以将其设置为：

- 继承数据类型的规则，例如 “Inherit: Same as output”
- 内置数据类型的名称，例如 single
- 数据类型对象的名称，例如 Simulink.NumericType 对象
- 计算结果为数据类型的表达式，例如 fixdt(1,16,0)

单击**显示数据类型助手**按钮 ![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/show_data_type_asst_button.png) 以显示**数据类型助手**，帮助您设置数据类型属性。有关详细信息，请参阅[使用数据类型助手指定数据类型](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/specify-data-types-using-data-type-assistant.html)。



**提示**

使用此参数为内部计算指定高于（或低于）表数据或输出数据的精度。

#### 编程用法

| **模块参数**：IntermediateResultsDataTypeStr               |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值：**'Inherit: Inherit via internal rule' | 'Inherit: Same as output' | 'double' | 'single' | 'int8' | 'uint8' | 'int16' | 'uint16' | 'int32' | 'uint32' | 'int64' | 'uint64' | 'fixdt(1,16,0)' | 'fixdt(1,16,2^0,0)'|'<data type expression>' |
| **默认值：**'Inherit: Same as output'                      | -->



<div class="details-box">
<details open>
<summary>输出数据类型 — 输出数据类型<div>“Inherit: sameAsInput” （默认） | “Inherit: backPropagation” | “float” | “double” | int8 | uint8 | “int16” | “uint16” | “int32” | “uint32” | “fixdt(1,16,0)” | “fixdt(1,16,2^0,0)” | “fixdt(1,16,1.0,0,0.0)”</div></summary>
</details>
<div class="details-content">


指定输出数据类型。可以将其设置为：

- 继承数据类型的规则，例如 “Inherit: backPropagation”；
- 内置数据类型的名称，例如 float；
<!-- - 数据类型对象的名称，例如 Simulink.NumericType 对象 -->
- 计算结果为数据类型的表达式，例如 fixdt(1,16,0)。

单击**显示数据类型帮助**按钮 <img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LookupTable/LookupTable1D/LookupTable1D_button.png')" style="width: 80px; height: auto; vertical-align:middle; display:inline; margin:0;"> 以显示**数据类型帮助**，帮助您设置数据类型属性。  

</div>
</div>
<!-- 暂无
 | “int64” | “uint64” | <data type expression> -->




  <!-- 有关详细信息，请参阅[使用数据类型助手指定数据类型]()。 -->

<!-- 暂无
#### 编程用法

| **模块参数**：OutDataTypeStr                               |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值：**'Inherit: Inherit via back propagation' | 'Inherit: Inherit from table data' | 'Inherit: Same as first input' | 'double' | 'single' | 'half' | 'int8' | 'uint8' | 'int16' | 'uint16' | 'int32' | 'uint32' | 'int64' | 'uint64' | 'fixdt(1,16,0)' | 'fixdt(1,16,2^0,0)'|'<data type expression' |
| **默认值：**'Inherit: Same as first input'                 | -->


<!-- 暂无
### 输出最小值 — 模块可以输出的最小值 [] | scalar



指定模块输出的最小值。默认值为 []（未指定）。Simulink 软件使用此值执行：

- 参数范围检查（请参阅[指定模块参数的最小值和最大值](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/checking-parameter-values.html)）。
- 仿真范围检查（请参阅[指定信号范围](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/signal-ranges.html)）。
- 定点数据类型的自动定标。
- 从模型生成的代码的优化。此优化可删除算法代码，并影响某些仿真模式（如 SIL 或外部模式）的结果。

#### 编程用法

| **模块参数**：OutMin |
| ---------------------- |
| **类型：**字符向量     |
| **值：**标量           |
| **默认值：**'[]'     | -->

<!-- 暂无
### 输出最大值 — 模块可以输出的最大值 [] | scalar



指定模块可以输出的最大值。默认值为 []（未指定）。Simulink 软件使用此值执行：

- 参数范围检查（请参阅[指定模块参数的最小值和最大值](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/checking-parameter-values.html)）。
- 仿真范围检查（请参阅[指定信号范围](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/signal-ranges.html)）。
- 定点数据类型的自动定标。
- 从模型生成的代码的优化。此优化可删除算法代码，并影响某些仿真模式（如 SIL 或外部模式）的结果。

#### 编程用法

| **模块参数**：OutMax |
| ---------------------- |
| **类型：**字符向量     |
| **值：**标量           |
| **默认值：**'[]'     | -->


<!-- 暂无
### 内部规则优先级 — 进行中间计算的内部规则 “速度” （默认） | “精度”



指定进行中间计算的内部规则。选择“速度”可以提高计算速度。但这样可能会损失精度，通常最多 2 位。

#### 编程用法

| **模块参数**：InternalRulePriority |
| ------------------------------------ |
| **类型：**字符向量                   |
| **值：**'Speed' | 'Precision'      |
| **默认值：**'Speed'                | -->


<!-- 暂无
### 要求所有输入具有相同的数据类型 — 要求所有输入具有相同的数据类型 on （默认） | off



选中此项会要求所有输入具有相同的数据类型。

#### 编程用法

| **模块参数**：InputSameDT |
| --------------------------- |
| **类型：**字符向量          |
| **值：**'off' | 'on'      |
| **默认值：**'on'          | -->


<!-- 暂无
### 锁定数据类型设置以防止被定点工具更改 — 防止定点工具覆盖数据类型 off （默认） | on



选择此参数可防止定点工具覆盖您对此模块指定的数据类型。有关详细信息，请参阅[Lock the Output Data Type Setting](https://ww2.mathworks.cn/help/releases/R2022b/fixedpoint/ug/configuring-blocks-with-fixed-point-output.html#f25236) (Fixed-Point Designer)。

#### 编程用法

| **模块参数**：LockScale |
| ------------------------- |
| **类型：**字符向量        |
| **值：**'off' | 'on'    |
| **默认值：**'off'       | -->


<!-- 暂无
### 整数舍入模式 — 定点运算的舍入模式 “最简” （默认） | “向上” | “收敛” | “向下” | “最邻近值” | “舍入” | “零”



指定在仿真过程中或在执行从模型中生成的代码时发生的定点查找表计算的舍入模式。有关详细信息，请参阅[舍入](https://ww2.mathworks.cn/help/releases/R2022b/fixedpoint/ug/rounding.html) (Fixed-Point Designer)。

此选项不影响模块参数值的舍入。Simulink 将此类值舍入到最邻近的可表示整数值。要控制模块参数的舍入方法，请使用 MATLAB® 舍入函数在模块对话框上的编辑字段中输入表达式。

#### 编程用法

| **模块参数**：RndMeth                                      |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值：**'Ceiling' | 'Convergent' | 'Floor' | 'Nearest' | 'Round' | 'Simplest' | 'Zero' |
| **默认值：**'Simplest'                                     | -->


<!-- 暂无
### 对整数溢出进行饱和处理 — 溢出操作的方法 off （默认） | on



| 操作                     | 执行此操作的原因                                             | 溢出时会发生的情况                                 | 示例                                                    |
| :----------------------- | :----------------------------------------------------------- | :------------------------------------------------- | :------------------------------------------------------ |
| 选中此复选框 (on)。    | 您的模型可能有溢出，并且您希望在生成的代码中具有显式饱和保护。 | 将溢出饱和处理为数据类型能够表示的最小值或最大值。 | 一个有符号的 8 位整数的溢出可以饱和处理为 -128 或 127。 |
| 不选中此复选框 (off)。 | 您需要优化所生成代码的效率。您希望避免过度地指定信号超出范围时的处理方式。有关详细信息，请参阅[信号范围错误故障排除](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/signal-ranges.html#brdiku9)。 | 溢出会绕回到由数据类型表示的适当值。               | 数字 130 不适合一个有符号 8 位整数，因此绕回 -126。     |





**提示**

如果您将模型保存为 R2009a 或更早版本，此复选框设置将不起作用，且不会显示饱和代码。此行为保留了向后兼容性。

如果选中此复选框，饱和将应用于模块中的每个内部操作，而不仅仅应用于输出或结果。一般情况下，代码生成进程可以检测到何时不可能发生溢出。在这种情况下，代码生成器不会生成饱和代码。

#### 编程用法

| **模块参数**：SaturateOnIntegerOverflow |
| ----------------------------------------- |
| **类型：**字符向量                        |
| **值：**'off' | 'on'                    |
| **默认值：**'off'                       | -->



<!-- 不确定
## 模块特性

| **数据类型**     | double | enumerated | fixed point | half | integer | single |
| ---------------- | ------------------------------------------------------------ |
| **直接馈通**     | 是                                                         |
| **多维信号**     | 是                                                         |
| **可变大小信号** | 否                                                         |
| **过零检测**     | 否                                                         | -->


<!-- 暂无
## 详细信息

### 在生成的代码中具有可调表大小

假设您有一个查找表，您希望它在生成的代码中可以调整大小。当使用 Simulink.LookupTable 和 Simulink.Breakpoint 对象来配置用于在生成的代码中进行标定的查找表数据时，请使用对象的 SupportTunableSize 属性启用可调表大小。如果不使用这些类，请使用 n-D Lookup Table 模块中的**在代码生成中支持可调表大小**参数启用可调表大小。

假设：

- 您在模型的预加载函数中定义了一个 Simulink.Parameter 结构体：

  
  p = Simulink.Parameter;
  p.Value.MaxIdx = [2 2];
  p.Value.BP1 = [1 2 3];
  p.Value.BP2 = [1 4 16];
  p.Value.Table = [4 5 6; 16 19 20; 10 18 23];
  p.DataType = 'Bus: slLookupTable';
  p.CoderInfo.StorageClass = 'ExportedGlobal';
  
  % Create bus object slBus1 from MATLAB structure
  Simulink.Bus.createObject(p.Value);
  slLookupTable = slBus1;
  slLookupTable.Elements(1).DataType = 'uint32';
  

- 以下模块参数适用于 n-D Lookup Table 模块。

  | 参数                           | 值         |
  | :----------------------------- | :--------- |
  | **表维数**                     | 2        |
  | **表数据**                     | p.Table  |
  | **断点 1**                     | p.BP1    |
  | **断点 2**                     | p.BP2    |
  | **在代码生成中支持可调表大小** | on       |
  | **每个维度的最大索引**         | p.MaxIdx |

生成的 model_types.h 头文件包含与下面类似的类型定义。


typedef struct {
  uint32_T MaxIdx[2];
  real_T BP1[3];
  real_T BP2[3];
  real_T Table[9];
} slLookupTable;


生成的 model.c 文件包含与下面类似的代码。


/* Exported block parameters */
slLookupTable p = {
  { 2U, 2U },
 
  { 1.0, 2.0, 3.0 },
 
  { 1.0, 4.0, 16.0 },
 
  { 4.0, 16.0, 10.0, 5.0, 19.0, 18.0, 6.0, 20.0, 23.0 }
} ; 

/* More code */

/* Model output function */
static void ex_lut_nd_tunable_table_output(int_T tid)
{
  /* Lookup_n-D: '<Root>/n-D Lookup Table' incorporates:
   *  Inport: '<Root>/In1'
   *  Inport: '<Root>/In2'
   */
  Y = look2_binlcpw(U1, U2, p.BP1, p.BP2, p.Table, ...
p.MaxIdx, p.MaxIdx[0] + 1U);
 
  /* Outport: '<Root>/Out1' */
  ex_lut_nd_tunable_table_Y.Out1 = Y;

  /* tid is required for a uniform function interface.
   * Argument tid is not used in the function. */
  UNUSED_PARAMETER(tid);
}


突出显示的代码行为查找表指定了可调表大小。您可以更改查找表与断点数据的大小和值，无需重新生成或重新编译代码。

### 查找表中的枚举值

假设您有一个具有类似如下定义的枚举类的查找表：


classdef(Enumeration) Gears < Simulink.IntEnumType 
    enumeration 
        GEAR1(1), 
        GEAR2(2), 
        GEAR3(4), 
        GEAR4(8), 
        SPORTS(16),
        REVERSE(-1), 
        NEUTRAL(0)        
    end 
end


n-D Lookup 模块具有以下设置：

- **维数**设置为 “1”。
- **表数据**值为 [5 10 20 40 80 -5 0]。
- **断点 1** 值为 enumeration('Gears')。
- 内插方法为“均一”。
- 对于无序搜索，请将**索引搜索方法**设置为“线性搜索”并清除**使用上一个索引结果开始索引搜索**复选框。

仿真产生对应于 GEAR2、REVERSE 和 SPORTS 的向量 [10 -5 80]。 -->

<!-- <img :src="$withBase('.png')" style="transform: scale(0.5);"> -->

## 版本历史记录

- 在 2024b 之前推出

### 限制信息


1. 输入端口暂不支持定义输出值的表和显式断点值的端口；  
2. 暂不支持查找表维度的数量定义；    
3. 暂不支持表和断点的设定方法；  
4. 暂不支持设定查找表对象的名称；    
5. 暂不支持选择断点设定的方法；  
6. 暂不支持定义表和断点数据的源；  
7. 暂不支持定义等间距断点数据中的第一个点；  
8. 暂不支持定义等间距断点之间的间距；  
9. 暂不支持三次样条和 Akima 样条的内插方法；  
10. 暂不支持三次样条和 Akima 样条的内插方法；  
11. 暂不支持等间距的索引搜索方法；  
12. 暂不支持使用上一个索引结果开始索引搜索；  
13. 暂不支持选择输入超出范围的诊断；  
14. 暂不支持是否选中尽可能应用全精度定点算法；  
15. 暂不支持是否选中输入等于或高于最后一个断点时使用最后一个表值；  
16. 暂不支持是否选中所有输入数据使用一个输入端口；  
17. 暂不支持删除生成代码中防止超范围输入的代码的复选框；  
18. 暂不支持在代码中支持可调表大小；  
19. 暂不支持设定采样时间；  
20. 暂不支持设定每个维度的最大索引；  
21. 暂不支持选择表数据、断点、区间比和中间结果的数据类型，暂不支持 int64、uint64 和 data type expression 的输出数据类型；
22. 暂不支持指定模块可以输出的最大最小值；  
23. 暂不支持指定进行中间计算的内部规则；  
24. 暂不支持要求所有输入具有相的数据类型的复选框；  
25. 暂不支持锁定数据类型设置以防止被定点工具更改的复选框；  
26. 暂不支持选择整数舍去模式；  
27. 暂不支持对整数溢出进行饱和处理的复选框；  
28. 输入端口数据类型暂不支持half、int64、uint8、uint16、uint32、uint64 和 enum 的数据类型，输出端口暂不支持half、int64、uint8、uint16、uint32 和 uint64 的数据类型。


<!-- 暂无
## 扩展功能

### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。

### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 Verilog 代码和 VHDL 代码。

HDL Coder™ 提供影响 HDL 实现和综合逻辑的额外配置选项。有关 1-D Lookup Table 模块的 HDL 代码生成支持的信息，请参阅 [HDL 代码生成]()。

### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。

## 版本历史记录

**在 R2011a 中推出** -->

<!-- 暂不需要
## 另请参阅

[Direct Lookup Table (n-D)]() | [Prelookup]() | [Interpolation Using Prelookup]() | [Lookup Table Dynamic]() | [Simulink.LookupTable]() | [Simulink.Breakpoint]() -->


<!-- 暂不需要
### 主题

- [从 MATLAB 中导入查找表数据]()
- [关于查找表模块]()
- [查找表剖析]()
- [输入断点和表数据]()
- [关于选择查找表的规范]() -->