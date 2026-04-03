# DiscreteTransferFcn
---
&nbsp;

实现离散传递函数

- **库：** Sysblock / Discrete


<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/DiscreteTransferFcn/DiscreteTransferFcn.png')" style="width: 100px; height: auto;">

## 描述

DiscreteTransferFcn 模块实现 z 变换传递函数。

<!-- ，如下所示：

*H*(*z*)=*n**u**m*(*z*)*d**e**n*(*z*)=*n**u**m*0*z**m*+*n**u**m*1*z**m*−1+...+*n**u**m**m**d**e**n*0*z**n*+*d**e**n*1*z**n*−1+...+*d**e**n**n*

其中 *m+1* 和 *n+1* 分别是分子和分母系数的数量。*num* 和 *den* 包含按 *z* 的降幂顺序排列的分子和分母系数。*num* 可以是向量或矩阵，而 *den* 必须为向量。分母的阶必须大于或等于分子的阶。

按 *z* 的降幂顺序指定分子和分母多项式的系数。利用此模块，您可以使用 *z* 形式的多项式来表示离散系统，这是控制工程师通常使用的方法。与之相反，Discrete Filter 模块则允许使用 *z-1*（延迟算子）形式的多项式来表示离散系统，这是信号处理工程师通常使用的方法。当分子和分母多项式的长度相同时，这两种方法相同。

Discrete Transfer Fcn 模块将 *z* 变换传递函数应用于输入的每个独立通道。**输入处理**参数用于指定该模块将输入的每个列作为单个通道处理（基于帧的处理）还是将输入的每个元素作为单个通道处理（基于采样的处理）。要执行基于帧的处理，您必须拥有 DSP System Toolbox™ 许可证。 -->

<!-- ### 指定初始状态

使用**初始状态**参数可以指定初始滤波器状态。要确定您必须指定的初始状态数量以及如何指定这些状态，请使用下列各表。

**基于帧的处理**

| 输入                     | 通道数 | 有效初始状态（对话框）                 | 有效初始状态（输入端口） |
| :----------------------- | :----- | :------------------------------------- | :----------------------- |
| 列向量 (K×1) 无向向量 (K) | 1      | 标量列向量 (M×1) 行向量 (1×M)           | 标量列向量  (M×1)         |
| 行向量 (1×N) 矩阵 (K×N)   | N      | 标量列向量 (M×1) 行向量 (1×M) 矩阵 (M×N) | 标量矩阵 (M×N)           | -->

<!-- 
**基于采样的处理**

| 输入                                 | 通道数 | 有效初始状态（对话框）                     | 有效初始状态（输入端口）     |
| :----------------------------------- | :----- | :----------------------------------------- | :--------------------------- |
| 标量                                 | 1      | 标量列向量 (M×1)行向量 (1×M)               | 标量列向量 (M×1)行向量 (1×M) |
| 行向量 (1×N)列向量 (N×1)无向向量 (N) | N      | 标量列向量 (M×1)行向量 (1×M)矩阵 (M×N)     | 标量                         |
| 矩阵 (K×N)                           | K×N    | 标量列向量 (M×1)行向量 (1×M)矩阵 (M×(K×N)) | 标量                         |

当**初始状态**为标量时，模块将所有滤波器状态初始化为相同的标量值。要将所有状态初始化为零，请输入 `0`。当**初始状态**为向量或矩阵时，每个向量或矩阵元素都为相应通道中的相应延迟元素指定唯一的初始状态：

- 向量长度必须等于滤波器中的延迟元素数，`M = max(number of zeros, number of poles)`。
- 矩阵的行数必须与滤波器中的延迟元素数相同，`M = max(number of zeros, number of poles)`。矩阵的每一列还须对应输入信号的一个通道。 -->

<!-- 
以下示例说明了初始滤波器输出与初始输入和状态之间的关系。假定有一个初始输入 u1，则第一个输出 y1 与初始状态 [x1, x2] 和初始输入的关系如下所示：

*y*1=4*x*1*x*2=1/2(*u*1−3*x*1) 
-->



## 示例

拖放一个 Step 模块。这个模块将作为系统的输入，模拟一个阶跃信号。双击该模块，设置阶跃时间为 0，初始值为 0，终值为 1。拖放一个 discreteTransferFcn 模块，用于表示离散系统。将 Step 模块的输出连接到 discreteTransferFcn 模块的输入端口，将 discreteTransferFcn 模块的输出连接到 display 模块的输入端口。
设置 discreteTransferFcn 模块的参数，分子系数设置为[0.5]，分母系数设置为[1,-0.5]。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/DiscreteTransferFcn.mo">DiscreteTransferFcn.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/DiscreteTransferFcn/DiscreteTransferFcn01.png')" style="width: 600px; height: auto;">

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/DiscreteTransferFcn/DiscreteTransferFcn02.png')" style="border: 1px solid black;width: 600px; height: auto;">

## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

输入信号，指定为标量、向量或矩阵。

**数据类型：** double

</div>
</div>



<!-- `float` | `double` | `int8` | `int16` | `int32` | `fixed point` -->

<!-- 暂无
### Num — 分子系数 标量 | 向量 | 矩阵



分子多项式的系数指定为 *z* 的降幂顺序的向量或矩阵。使用行向量可指定单个分子多项式的系数。使用矩阵可以指定要应用于同一输入的多个滤波器的系数。矩阵的每一行表示一组滤波器抽头。分母的阶必须大于或等于分子的阶。

#### 依存关系

要启用此端口，请将**分子源**设置为“`输入端口`”。

分子和分母系数必须具有相同的复/实性。它们可以有不同的字长和小数长度。

**数据类型：** `double` -->
<!-- `float` | `double` | `int8` | `int16` | `int32` | `fixed point` -->

<!-- 暂无
### Den — 分母系数 标量 | 向量 | 矩阵



分母多项式的系数指定为 *z* 的降幂形式的向量。使用行向量可指定单个分母多项式的系数。使用矩阵可以指定要应用于同一输入的多个滤波器的系数。矩阵的每一行表示一组滤波器抽头。分母的阶必须大于或等于分子的阶。分母首项系数不能为 `0`。

#### 依存关系

要启用此端口，请将**分母源**设置为“`输入端口`”。

分子和分母系数必须具有相同的复/实性。它们可以有不同的字长和小数长度。

**数据类型：** `double` -->
<!-- `float` | `double` | `int8` | `int16` | `int32` | `fixed point` -->

<!-- 暂无
### `External reset` — 外部重置信号 标量



外部重置信号，指定为标量。当指定的触发事件发生时，模块将状态重置为其初始条件。



**提示**

此端口的图标根据**外部重置**参数的值更改。



#### 依存关系

要启用此端口，请将**外部重置**设置为“`上升沿`”、“`下降沿`”、“`任一沿`”、“`电平`”或“`电平保持`”。

#### 限制

重置信号必须是单精度、双精度、布尔或整数类型的标量。不支持 `ufix1` 以外的定点数据类型。

**数据类型：** `double` -->
<!-- `float` | `double` | `int8` | `int16` | `int32` | `fixed point` -->

<!-- 暂无
### x0 — 初始状态 标量 | 向量 | 矩阵



初始状态，指定为标量、向量或矩阵。有关指定状态的详细信息，请参阅[指定初始状态](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/discretetransferfcn.html#br74ug2-1)。当输入或系数为复数时，状态为复数。

#### 依存关系

要启用此端口，请将**初始状态源**设置为“`输入端口`”。

**数据类型：** `double` -->
<!-- `float` | `double` | `int8` | `int16` | `int32` | `fixed point` -->

### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

输出信号，指定为标量、向量或矩阵。

**数据类型：** double

</div>
</div>


<!-- `float` | `double` | `int8` | `int16` | `int32` | `fixed point` -->

## 参数



### 常设

<!-- 暂无

### `分子源` — 分子系数的信源 “`对话框`” （默认） | “`输入端口`”



将分子系数的信源指定为“`对话框`”或“`输入端口`”。

#### 编程用法

| **模块参数**：`NumeratorSource`   |
| --------------------------------- |
| **类型：**字符向量                |
| **值：**`'Dialog' | 'Input port'` |
| **默认值：**`'Dialog'`            | -->


<!-- 暂无
### `分子值` — 分子系数 `[1]` （默认） | 标量 | 向量 | 矩阵



离散传递函数的分子系数。要指定系数，请将**源**设置为“`对话框`”。然后，在**值**中按 *z* 的降幂顺序输入系数。使用行向量可指定单个分子多项式的系数。使用矩阵可以指定要应用于同一输入的多个滤波器的系数。矩阵的每一行表示一组滤波器抽头。

#### 依存关系

要启用此参数，请将**分子源**设置为“`对话框`”。

#### 编程用法

| **模块参数**：`分子多项式系数`    |
| ---------------------------- |
| **类型：**字符向量           |
| **值：**标量 \| 向量 \| 矩阵 |
| **默认值：**`'[1]'`          | -->


<!-- 暂无

### `分母源` — 分母系数的信源 “`对话框`” （默认） | “`输入端口`”



将分母系数的信源指定为“`对话框`”或“`输入端口`”。

#### 编程用法

| **模块参数**：`DenominatorSource` |
| --------------------------------- |
| **类型：**字符向量                |
| **值：**`'Dialog' | 'Input port'` |
| **默认值：**`'Dialog'`            | -->

<div class="details-box">
<details open>
<summary>分母值 — 分母系数<div>[1 0.5]（默认） | 标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

离散传递函数的分母系数。要指定系数，请将**源**设置为**对话框**。然后，在**值**中按 z 的降幂顺序输入系数。使用行向量可指定单个分母多项式的系数。使用矩阵可以指定要应用于同一输入的多个滤波器的系数。矩阵的每一行表示一组滤波器抽头。

#### 依存关系

要启用此参数，请将**分母源**设置为**对话框**。

</div>
</div>



<!-- 
#### 编程用法

| **模块参数**：`分母多项式系数`  |
| ---------------------------- |
| **类型：**字符向量           |
| **值：**标量 \| 向量 \| 矩阵 |
| **默认值**：`'[1 0.5]'`      | -->


<!-- 暂无
### `初始状态源` — 初始状态的信源 “`对话框`” （默认） | “`输入端口`”



将初始状态的信源指定为“`对话框`”或“`输入端口`”。

#### 编程用法

| **模块参数**：`InitialStatesSource` |
| ----------------------------------- |
| **类型：**字符向量                  |
| **值：**`'Dialog' | 'Input port'`   |
| **默认值：**`'Dialog'`              | -->

<div class="details-box">
<details open>
<summary>初始状态值 — 初始滤波器状态<div>0（默认） | 标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

将初始滤波器状态指定为标量、向量或矩阵。

#### 依存关系

要启用此参数，请将**初始状态源**设置为**对话框**。

</div>
</div>



<!-- 
#### 编程用法

| **模块参数**：`初始状态值` |
| ----------------------------- |
| **类型：**字符向量            |
| **值：**标量 \| 向量 \| 矩阵  |
| **默认值：**`'0'`             | -->


<!-- 暂无
### `外部重置` — 外部状态重置 “`无`” （默认） | “`上升沿`” | “`下降沿`” | “`任一沿`” | “`电平`” | “`电平保持`”



指定用于将状态重置为初始条件的触发事件。

| 重置模式     | 行为                                                         |
| :----------- | :----------------------------------------------------------- |
| “`无`”       | 不重置。                                                     |
| “`上升沿`”   | 在上升边重置。                                               |
| “`下降沿`”   | 在下降边重置。                                               |
| “`任一沿`”   | 在上升或下降边重置。                                         |
| “`电平`”     | 在下列任一情况下重置：当重置信号在当前时间步为非零值时当重置信号值从上一时间步的非零更改为当前时间步的零时 |
| “`电平保持`” | 当重置信号在当前时间步为非零值时重置                         |

#### 编程用法

| **模块参数**：`ExternalReset`                                |
| ------------------------------------------------------------ |
| **类型**：字符向量                                           |
| **值**：`'None'` | `'Rising'` | `'Falling'` | `'Either'` | `'Level'` | `'Level hold'` |
| **默认值**：`'None'`                                         | -->


<!-- 暂无
### `输入处理` — 基于采样或基于帧的处理 “`元素作为通道(基于采样)`” （默认） | “`列作为通道(基于帧)`”



指定模块是执行基于采样还是基于帧的处理。

- “`元素作为通道(基于采样)`” - 将输入的每个元素作为独立通道处理。

- “`列作为通道(基于帧)`” - 将输入的每列作为独立通道处理。

  

  **注意**

  基于帧的处理需要具有 DSP System Toolbox 许可证。

  有关详细信息，请参阅[Sample- and Frame-Based Concepts](https://ww2.mathworks.cn/help/releases/R2022b/dsp/ug/sample-and-frame-based-concepts.html) (DSP System Toolbox)。

#### 编程用法

| **模块参数**：`InputProcessing`                              |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值：**`'Elements as channels (sample based)' | 'Columns as channels (frame based)'` |
| **默认值：**`'Elements as channels (sample based)'`          |
 -->

<!-- 暂无
### `通过跳过除以分母首项系数(a0)进行优化` — 跳过除以 a0 的运算 `off` （默认） | `on`



当分母的首项系数 a0 等于 1 时选择。此参数可以优化您的代码。

当选中此复选框时，该模块在仿真或生成的代码中不会执行对 a0 的除法运算。如果 a0 不等于 1，则会出错。

当清除此复选框时，该模块在仿真期间完全可调，并且在仿真和代码生成中均会执行除以 a0 的运算。

#### 编程用法

| **模块参数**：`a0EqualsOne` |
| --------------------------- |
| **类型：**字符向量          |
| **值：**`'off' | 'on'`      |
| **默认值：**`'off'`         |
 -->


<div class="details-box">
<details open>
<summary>采样时间（-1 表示继承）— 采样之间的时间间隔<div>-1（默认） | 标量 | 向量</div></summary>
</details>
<div class="details-content">

指定采样时间间隔。要继承采样时间，请将此参数设置为 -1。

</div>
</div>



<!-- 
#### 编程用法

| **模块参数**：`SampleTime` |
| -------------------------- |
| **类型：**字符向量         |
| **值：**标量 \| 向量       |
| **默认值：**`'-1'`         | -->

<!-- ### 数据类型 -->


<!-- 只有部分类型
### `状态` — 状态数据类型 `Inherit: Same as input` （默认） | “`int8`” | “`int16`” | “`int32`” | “`int64`” | “`fixdt(1,16,0)`” | “`<data type expression>`”



指定状态数据类型。可以将其设置为：

- 继承数据类型的规则，例如 “`Inherit: Same as input`”
- 内置整数，例如 `int8`
- 数据类型对象，例如 `Simulink.NumericType` 对象
- 计算结果为数据类型的表达式，例如 `fixdt(1,16,0)`

点击**显示数据类型助手**按钮 ![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/show_data_type_asst_button.png) 以显示**数据类型助手**，帮助您设置数据类型属性。有关详细信息，请参阅[使用数据类型助手指定数据类型](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/specify-data-types-using-data-type-assistant.html)。 -->


<!-- 暂无
### `分子系数` — 分子系数数据类型 `Inherit: Inherit via internal rule` （默认） | “`int8`” | “`int16`” | “`int32`” | “`int64`” | “`fixdt(1,16)`” | “`fixdt(1,16,0)`” | “`<data type expression>`”



指定分子系数数据类型。可以将其设置为：

- 继承数据类型的规则，例如 “`Inherit: Inherit via internal rule`”
- 内置整数，例如 `int8`
- 数据类型对象，例如 `Simulink.NumericType` 对象
- 计算结果为数据类型的表达式，例如 `fixdt(1,16,0)`

点击**显示数据类型助手**按钮 ![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/show_data_type_asst_button.png) 以显示**数据类型助手**，帮助您设置数据类型属性。有关详细信息，请参阅[使用数据类型助手指定数据类型](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/specify-data-types-using-data-type-assistant.html)。

#### 编程用法

| **模块参数**：` NumCoeffDataTypeStr`                         |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值：**`'Inherit: Inherit via internal rule' | 'int8' | 'int16' | 'int32' | 'int64' | 'fixdt(1,16)' | 'fixdt(1,16,0)' | '<data type expression>'` |
| **默认值：**`'Inherit: Inherit via internal rule'`           |



### `分子系数最小值` — 分子系数的最小值 `[]` （默认） | 标量



指定分子系数可以具有的最小值。默认值为 `[]`（未指定）。Simulink® 软件使用此值执行：

- 参数范围检查（请参阅[指定模块参数的最小值和最大值](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/checking-parameter-values.html)）
- 定点数据类型的自动定标

#### 编程用法

| **模块参数**：`NumCoeffMin` |
| --------------------------- |
| **类型：**字符向量          |
| **值：**标量                |
| **默认值：**`'[]'`          |



### `分子系数最大值` — 分子系数的最大值 `[]` （默认） | 标量



指定分子系数可以具有的最大值。默认值为 `[]`（未指定）。Simulink 软件使用此值执行：

- 参数范围检查（请参阅[指定模块参数的最小值和最大值](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/checking-parameter-values.html)）
- 定点数据类型的自动定标

#### 编程用法

| **模块参数**：`NumCoeffMax` |
| --------------------------- |
| **类型：**字符向量          |
| **值：**标量                |
| **默认值：**`'[]'`          |



### `分子乘积输出` — 分子乘积输出数据类型 `Inherit: Inherit via internal rule` （默认） | “`Inherit: Same as input`” | “`int8`” | “`int16`” | “`int32`” | “`int64`” | “`fixdt(1,16,0)`” | “`<data type expression>`”



指定分子系数的乘积输出数据类型。可以将其设置为：

- 继承数据类型的规则，例如 “`Inherit: Inherit via internal rule`”
- 内置数据类型，例如 `int8`
- 数据类型对象，例如 `Simulink.NumericType` 对象
- 计算结果为数据类型的表达式，例如 `fixdt(1,16,0)` -->

<!-- 只有部分类型
点击**显示数据类型助手**按钮 ![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/show_data_type_asst_button.png) 以显示**数据类型助手**，帮助您设置数据类型属性。有关详细信息，请参阅[使用数据类型助手指定数据类型](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/specify-data-types-using-data-type-assistant.html)。

#### 编程用法

| **模块参数**：`NumProductDataTypeStr`                        |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值：**`'Inherit: Inherit via internal rule' | 'Inherit: Same as input' | 'int8' | 'int16' | 'int32' | 'int64' | 'fixdt(1,16,0)' | '<data type expression>'` |
| **默认值**：`'Inherit: Inherit via interal rule'`            | -->


<!-- 暂无
### `分子累加器` — 分子累加器数据类型 `Inherit: Inherit via internal rule` （默认） | “`Inherit: Same as input`” | “`Inherit: Same as product output`” | “`int8`” | “`int16`” | “`int32`” | “`int64`” | “`fixdt(1,16,0)`” | “`<data type expression>`”



指定分子系数的累加器数据类型。可以将其设置为：

- 继承数据类型的规则，例如 “`Inherit: Inherit via internal rule`”
- 内置数据类型，例如 `int8`
- 数据类型对象，例如 `Simulink.NumericType` 对象
- 计算结果为数据类型的表达式，例如 `fixdt(1,16,0)`

点击**显示数据类型助手**按钮 ![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/show_data_type_asst_button.png) 以显示**数据类型助手**，帮助您设置数据类型属性。有关详细信息，请参阅[使用数据类型助手指定数据类型](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/specify-data-types-using-data-type-assistant.html)。

#### 编程用法

| **模块参数**：`NumAccumDataTypeStr`                          |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值：**`'Inherit: Inherit via internal rule' | 'Inherit: Same as input' | 'Inherit: Same as product output' | 'int8' | 'int16' | 'int32' | 'int64' | 'fixdt(1,16,0)' | '<data type expression>'` |
| **默认值**：`'Inherit: Inherit via interal rule'`            |



### `分母系数` — 分母系数数据类型 `Inherit: Inherit via internal rule` （默认） | “`int8`” | “`int16`” | “`int32`” | “`int64`” | “`fixdt(1,16)`” | “`fixdt(1,16,0)`” | “`<data type expression>`”



指定分母系数数据类型。可以将其设置为：

- 继承数据类型的规则，例如 “`Inherit: Inherit via internal rule`”
- 内置整数，例如 `int8`
- 数据类型对象，例如 `Simulink.NumericType` 对象
- 计算结果为数据类型的表达式，例如 `fixdt(1,16,0)`

点击**显示数据类型助手**按钮 ![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/show_data_type_asst_button.png) 以显示**数据类型助手**，帮助您设置数据类型属性。有关详细信息，请参阅[使用数据类型助手指定数据类型](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/specify-data-types-using-data-type-assistant.html)。

#### 编程用法

| **模块参数**：`DenCoeffDataTypeStr`                          |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值：**`'Inherit: Inherit via internal rule' | 'int8' | 'int16' | 'int32' | 'int64' | 'fixdt(1,16)' | 'fixdt(1,16,0)' | '<data type expression>'` |
| **默认值：**`'Inherit: Same wordlength as input'`            |



### `分母系数最小值` — 分母系数的最小值 `[]` （默认） | 标量



指定分母系数可以具有的最小值。默认值为 `[]`（未指定）。Simulink 软件使用此值执行：

- 参数范围检查（请参阅[指定模块参数的最小值和最大值](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/checking-parameter-values.html)）
- 定点数据类型的自动定标

#### 编程用法

| **模块参数**：`DenCoeffMin` |
| --------------------------- |
| **类型：**字符向量          |
| **值：**标量                |
| **默认值：**`'[]'`          |



### `分母系数最大值` — 分母系数的最大值 `[]` （默认） | 标量



指定分母系数可以具有的最大值。默认值为 `[]`（未指定）。Simulink 软件使用此值执行：

- 参数范围检查（请参阅[指定模块参数的最小值和最大值](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/checking-parameter-values.html)）
- 定点数据类型的自动定标

#### 编程用法

| **模块参数**：`DenCoeffMax` |
| --------------------------- |
| **类型：**字符向量          |
| **值：**标量                |
| **默认值：**`'[]'`          |



### `分母乘积输出` — 分母乘积输出数据类型 `Inherit: Inherit via internal rule` （默认） | “`Inherit: Same as input`” | “`int8`” | “`int16`” | “`int32`” | “`int64`” | “`fixdt(1,16,0)`” | “`<data type expression>`”



指定分母系数的乘积输出数据类型。可以将其设置为：

- 继承数据类型的规则，例如 “`Inherit: Inherit via internal rule`”
- 内置数据类型，例如 `int8`
- 数据类型对象，例如 `Simulink.NumericType` 对象
- 计算结果为数据类型的表达式，例如 `fixdt(1,16,0)`

点击**显示数据类型助手**按钮 ![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/show_data_type_asst_button.png) 以显示**数据类型助手**，帮助您设置数据类型属性。有关详细信息，请参阅[使用数据类型助手指定数据类型](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/specify-data-types-using-data-type-assistant.html)。

#### 编程用法

| **模块参数**：`DenProductDataTypeStr`                        |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值：**`'Inherit: Inherit via internal rule' | 'Inherit: Same as input' | 'int8' | 'int16' | 'int32' | 'int64' | 'fixdt(1,16,0)' | '<data type expression>'` |
| **默认值**：`'Inherit: Inherit via interal rule'`            |



### `分母累加器` — 分母累加器数据类型 `Inherit: Inherit via internal rule` （默认） | “`Inherit: Same as input`” | “`Inherit: Same as product output`” | “`int8`” | “`int16`” | “`int32`” | “`int64`” | “`fixdt(1,16,0)`” | “`<data type expression>`”



指定分母系数的累加器数据类型。可以将其设置为：

- 继承数据类型的规则，例如 “`Inherit: Inherit via internal rule`”
- 内置数据类型，例如 `int8`
- 数据类型对象，例如 `Simulink.NumericType` 对象
- 计算结果为数据类型的表达式，例如 `fixdt(1,16,0)`

点击**显示数据类型助手**按钮 ![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/show_data_type_asst_button.png) 以显示**数据类型助手**，帮助您设置数据类型属性。有关详细信息，请参阅[使用数据类型助手指定数据类型](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/specify-data-types-using-data-type-assistant.html)。

#### 编程用法

| **模块参数**：`DenAccumDataTypeStr`                          |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值：**`'Inherit: Inherit via internal rule' | 'Inherit: Same as input' | 'Inherit: Same as product output' | 'int8' | 'int16' | 'int32' | 'int64' | 'fixdt(1,16,0)' | '<data type expression>'` |
| **默认值**：`'Inherit: Inherit via interal rule'`            |



### `输出` — 输出数据类型 `Inherit: Inherit via internal rule` （默认） | `Inherit: Same as input` | “`int8`” | “`int16`” | “`int32`” | “`int64`” | “`fixdt(1,16)`” | “`fixdt(1,16,0)`” | “`<data type expression>`”



指定输出数据类型。可以将其设置为：

- 继承数据类型的规则，例如 “`Inherit: Inherit via internal rule`”
- 内置数据类型，例如 `int8`
- 数据类型对象，例如 `Simulink.NumericType` 对象
- 计算结果为数据类型的表达式，例如 `fixdt(1,16,0)`

点击**显示数据类型助手**按钮 ![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/show_data_type_asst_button.png) 以显示**数据类型助手**，帮助您设置数据类型属性。有关详细信息，请参阅[使用数据类型助手指定数据类型](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/specify-data-types-using-data-type-assistant.html)。

#### 编程用法

| **模块参数**：`OutDataTypeStr`                               |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值：**`'Inherit: Inherit via internal rule' | 'Inherit: Same as input' | 'int8' | 'int16' | 'int32' | 'int64' | 'fixdt(1,16)' | 'fixdt(1,16,0)' | '<data type expression>'` |
| **默认值**：`'Inherit: Inherit via interal rule'`            |



### `输出最小值` — 输出的最小值 `[]` （默认） | 标量



指定模块可以输出的最小值。默认值为 `[]`（未指定）。Simulink 使用此值来执行：

- 仿真范围检查（请参阅[指定信号范围](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/signal-ranges.html)）
- 定点数据类型的自动定标

#### 编程用法

| **模块参数**：`OutMin` |
| ---------------------- |
| **类型：**字符向量     |
| **值：**标量           |
| **默认值：**`'[]'`     |



### `输出最大值` — 输出的最大值 `[]` （默认） | 标量



指定模块可以输出的最大值。默认值为 `[]`（未指定）。Simulink 使用此值来执行：

- 仿真范围检查（请参阅[指定信号范围](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/signal-ranges.html)）
- 定点数据类型的自动定标

#### 编程用法

| **模块参数**：`OutMax` |
| ---------------------- |
| **类型：**字符向量     |
| **值：**标量           |
| **默认值：**`'[]'`     |



### `锁定数据类型设置以防止被定点工具更改` — 防止定点工具覆盖数据类型 `off` （默认） | `on`



选择此参数可防止定点工具覆盖您对此模块指定的数据类型。有关详细信息，请参阅[Lock the Output Data Type Setting](https://ww2.mathworks.cn/help/releases/R2022b/fixedpoint/ug/configuring-blocks-with-fixed-point-output.html#f25236) (Fixed-Point Designer)。

#### 编程用法

| **模块参数**：`LockScale` |
| ------------------------- |
| **类型：**字符向量        |
| **值：**`'off' | 'on'`    |
| **默认值：**`'off'`       |



### `整数舍入模式` — 定点运算的舍入模式 “`向下`” （默认） | “`向上`” | “`收敛`” | “`最邻近值`” | “`舍入`” | “`最简`” | “`零`”



指定定点运算的舍入模式。有关详细信息，请参阅[舍入](https://ww2.mathworks.cn/help/releases/R2022b/fixedpoint/ug/rounding.html) (Fixed-Point Designer)。

模块参数始终舍入到最邻近的可表示值。要控制模块参数的舍入方法，请在封装字段中使用 MATLAB® 舍入函数输入表达式。

#### 编程用法

| **模块参数**：`RndMeth`                                      |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值：**`'Ceiling' | 'Convergent' | 'Floor' | 'Nearest' | 'Round' | 'Simplest' | 'Zero'` |
| **默认值：**`'Floor'`                                        |



### `对整数溢出进行饱和处理` — 溢出操作的方法 `off` （默认） | `on`



指定对溢出是进行饱和处理还是绕回处理。

| 操作                     | 原理说明                                                     | 对溢出的影响                                       | 示例                                                         |
| :----------------------- | :----------------------------------------------------------- | :------------------------------------------------- | :----------------------------------------------------------- |
| 选中此复选框 (`on`)。    | 您的模型可能有溢出，并且您希望在生成的代码中具有显式饱和保护。 | 将溢出饱和处理为数据类型能够表示的最小值或最大值。 | `int8`（有符号 8 位整数）数据类型可以表示的最大值为 127。任何大于此最大值的模块运算结果都会导致 8 位整数溢出。如果选中此复选框，模块输出将在达到 127 时饱和。类似地，模块输出将在达到最小输出值 -128 时饱和。 |
| 不选中此复选框 (`off`)。 | 您需要优化所生成代码的效率。您希望避免过度地指定信号超出范围时的处理方式。有关详细信息，请参阅[信号范围错误故障排除](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/signal-ranges.html#brdiku9)。 | 溢出会绕回到由数据类型表示的适当值。               | `int8`（有符号 8 位整数）数据类型可以表示的最大值为 127。任何大于此最大值的模块运算结果都会导致 8 位整数溢出。清除该复选框时，软件会将导致溢出的值解释为 `int8`，这可能产生意外结果。例如，以 `int8` 表示的模块结果 130（二进制 1000 0010）为 -126。 |



如果选中此复选框，饱和将应用于模块中的每个内部操作，而不仅仅应用于输出或结果。通常，代码生成过程可以检测何时不会发生溢出。在这种情况下，代码生成器不会生成饱和代码。

#### 编程用法

| **模块参数**：`SaturateOnIntegerOverflow` |
| ----------------------------------------- |
| **类型：**字符向量                        |
| **值：**`'off' | 'on'`                    |
| **默认值：**`'off'`                       |

### 状态属性



### `状态名称` — 模块状态的唯一名称 `''` （默认） | 字母数字字符串



使用此参数为模块状态指定唯一名称。默认值为 `' '`。如果此字段为空，则表示未指定任何名称。使用此参数时，请记住以下注意事项：

- 有效的标识符以字母或下划线字符开始，后跟字母数字或下划线字符。
- 状态名称仅适用于所选模块。

当您点击**应用**时，此参数将启用**状态名称必须解析为 Simulink 信号对象**。

有关详细信息，请参阅[模型接口元素的 C 代码生成配置](https://ww2.mathworks.cn/help/releases/R2022b/rtw/ug/c-code-generation-configuration-for-model-interface-elements.html) (Simulink Coder)。

#### 编程用法

| **模块参数**：`StateName` |
| ------------------------- |
| **类型：**字符向量        |
| **值：**唯一名称          |
| **默认值：**`''`          |



### `状态名称必须解析为 Simulink 信号对象` — 要求将状态名称解析为信号对象 `off` （默认） | `on`



选中此复选框会要求将状态名称解析为 Simulink 信号对象。

#### 依存关系

要启用此参数，请为**状态名称**指定值。仅当将模型配置参数**信号解析**设置为除“`无`”以外的值时，才会显示此参数。

#### 编程用法

| **模块参数**：`StateMustResolveToSignalObject` |
| ---------------------------------------------- |
| **类型：**字符向量                             |
| **值：**`'off' | 'on'`                         |
| **默认值：**`'off'`                            |

## 模型示例

![Designing a High Angle of Attack Pitch Mode Control](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink_aerospace/win64/DesigningAHighAngleOfAttackPitchModeControlExample_13.png)

### Designing a High Angle of Attack Pitch Mode Control

Use the Control System Toolbox™ and Simulink® Control Design™ to interact with Simulink to design a digital pitch control for the aircraft. In this example, we will design the controller to permit the aircraft to operate at a high angle of attack with minimal pilot workload. -->

<!-- ## 模块特性 -->

<!-- 只有数据类型部分实现
| **数据类型**                                                 | `double` \| `fixed pointa` \| `integera` \| `single` |
| ------------------------------------------------------------ | ------------------------------------------------- |
| **直接馈通**                                                 | `否`                                              |
| **多维信号**                                                 | `否`                                              |
| **可变大小信号**                                             | `否`                                              |
| **过零检测**                                                 | `否`                                              |
| [a](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/discretetransferfcn.html?searchHighlight=DiscreteTransferFcn&s_tid=doc_srchtitle#d125e52503) 此模块仅支持有符号定点数据类型。 |                                                   | -->

<!-- ## 扩展功能 -->

<!-- 

### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 Verilog 代码和 VHDL 代码。



HDL Coder™ 提供影响 HDL 实现和综合逻辑的额外配置选项。

**HDL 架构**

此模块具有一个默认 HDL 架构。

**HDL 模块属性**

| 通用                            |                                                              |
| :------------------------------ | ------------------------------------------------------------ |
| **ConstMultiplierOptimization** | 正则有符号数 (CSD) 或因子化 CSD 优化。默认值为“`无`”。另请参阅[ConstMultiplierOptimization](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-3) (HDL Coder)。 |
| **ConstrainedOutputPipeline**   | 通过移动设计中现有延迟的方式来放置在输出端的寄存器的数量。分布式流水线处理不会重新分发这些寄存器。默认值为 `0`。有关详细信息，请参阅[ConstrainedOutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#btp8gmp) (HDL Coder)。 |
| **InputPipeline**               | 要在生成的代码中插入的输入流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 `0`。有关详细信息，请参阅[InputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-25) (HDL Coder)。 |
| **OutputPipeline**              | 要在生成的代码中插入的输出流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 `0`。有关详细信息，请参阅[OutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-26) (HDL Coder)。 |

| 本机浮点                     |                                                              |
| :--------------------------- | ------------------------------------------------------------ |
| **HandleDenormals**          | 指定是否希望 HDL Coder 在设计中插入额外的逻辑来处理非正规数字。非规范数是量级非常小、必须使用包含前导零的尾数才能表示的浮点数。默认值为 “`inherit`”。另请参阅[HandleDenormals](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/hdl-block-properties-native-floating-point.html#mw_34395404-aeac-43da-bb3c-96c4a420c9e1) (HDL Coder)。 |
| **LatencyStrategy**          | 指定对于浮点运算符是否将设计中的模块映射到 `inherit`、`Max`、`Min` 或 `Zero`。默认值为 “`inherit`”。另请参阅[LatencyStrategy](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/hdl-block-properties-native-floating-point.html#mw_a99b0822-f2a6-4f5b-aca9-7f7251a67c7c) (HDL Coder)。 |
| **MantissaMultiplyStrategy** | 指定在代码生成期间如何实现尾数乘法运算。通过使用不同设置，您可以控制目标 FPGA 设备上 DSP 的使用。默认值为 “`inherit`”。另请参阅[MantissaMultiplyStrategy](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/hdl-block-properties-native-floating-point.html#mw_425f11cb-a3a5-45aa-a3aa-df5a7c765b5f) (HDL Coder)。 |

**限制**



- 此模块不支持双精度数据类型。请改用单精度数据类型。
- 不支持帧、矩阵和向量输入数据类型。
- 分母首项系数 (a0) 必须为 1 或 -1。



以下优化中不包括 Discrete Transfer Fcn 模块：

- 资源共享
- 分布式流水线处理





### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。

此模块仅支持有符号定点数据类型。 -->

## 版本历史记录

- 在 2024b 之前推出

### 限制信息
1. 端口-输入-Num — 分子系数
2. 端口-输入-Den — 分母系数
3. 端口-输入-External reset — 外部重置信号
4. 端口-输入-x0 — 初始状态
5. 参数-常设-分子源 — 分子系数的信源
6. 参数-常设-分母源 — 分母系数的信源
7. 参数-常设-初始状态源 — 初始状态的信源
8. 参数-常设-初始状态值 — 初始滤波器状态
9. 参数-常设-外部重置 — 外部状态重置
10. 参数-常设-输入处理 — 基于采样或基于帧的处理
11. 参数-常设-通过跳过除以分母首项系数(a0)进行优化 — 跳过除以 a0 的运算
12. 参数-数据类型-状态 — 状态数据类型
13. 参数-数据类型-分子系数 — 分子系数数据类型
14. 参数-数据类型-分子系数最小值 — 分子系数的最小值
15. 参数-数据类型-分子系数最大值 — 分子系数的最大值
16. 参数-数据类型-分子乘积输出 — 分子乘积输出数据类型
17. 参数-数据类型-分子累加器 — 分子累加器数据类型
18. 参数-数据类型-分母系数 — 分母系数数据类型
19. 参数-数据类型-分母系数最小值 — 分母系数的最小值
20. 参数-数据类型-分母系数最大值 — 分母系数的最大值
21. 参数-数据类型-分母乘积输出 — 分母乘积输出数据类型
22. 参数-数据类型-分母累加器 — 分母累加器数据类型
23. 参数-数据类型-输出 — 输出数据类型
24. 参数-数据类型-输出最小值 — 输出的最小值
25. 参数-数据类型-输出最大值 — 输出的最大值
26. 参数-数据类型-锁定数据类型设置以防止被定点工具更改 — 防止定点工具覆盖数据类型
27. 参数-数据类型-整数舍入模式 — 定点运算的舍入模式
28. 参数-数据类型-对整数溢出进行饱和处理 — 溢出操作的方法
29. 参数-状态属性-状态名称 — 模块状态的唯一名称




<!-- ## 另请参阅 -->

<!-- [Discrete Filter]() | [Transfer Fcn]() -->


