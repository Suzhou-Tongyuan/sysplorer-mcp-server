# Inport
---
&nbsp;

输入端口

- **库:** Sysblock / Port

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/PortPng/Inport/Inport.png')" style="width: 100px; height: auto;">

## 描述

Inport 模块将信号从系统外部链接到系统内。

软件根据以下规则分配 Inport 模块端口号：

- 根级系统或子系统中的 Inport 模块按顺序编号，从 1 开始。
- 如果添加 Inport 模块，标签将是下一个可用的编号。
- 如果您删除一个 Inport 模块，其他端口号会重新编号，以确保 Inport 模块的连续的且没有遗漏任何编号。
- 如果将 Inport 模块复制到系统中，其端口号不会重新编号，除非当前编号与系统中已存在的输入端口发生冲突。如果复制的 Inport 模块的端口号不符合顺序，则会对该模块重新进行编号。否则，当您仿真模型或更新模块图时，会出现一条错误消息。

### 顶层系统中的 Inport 模块

您可以在顶层系统中使用 Inport 模块，以进行以下操作：
  - 要使用根级输入端口加载多个信号的数据，请考虑使用根输入端口映射器工具。
  - 通过 linmod 和 trim 分析函数提供模型扰动的方式。


### 子系统中的 Inport 模块

子系统中的 Inport 模块表示子系统的输入。到达 Subsystem 模块上的输入端口的信号从该子系统中的关联 Inport 模块流出。与 Subsystem 模块上的输入端口关联的 Inport 模块是其**端口号**参数与 Subsystem 模块上输入端口的相对位置匹配的模块。例如，**端口号**参数为 1 的 Inport 模块从连接到 Subsystem 模块上最顶层端口的模块获取其信号。

如果对 Inport 模块的**端口号**重新编号，则该模块将连接到其他输入端口。该模块继续从子系统外的同一模块接收其信号。

子系统内的 Inport 模块支持信号标签传播，但根级 Inport 模块不支持。
您可以直接编辑 Subsystem 模块上的端口标签。

::: tip 提示

对于包含总线的模型，如果总线信号中包含很多总线元素，则可以考虑使用 In Bus Element 和 Out Bus Element 模块。这些模块可以：

- 减少模块图中信号线的复杂度和杂乱无章。
- 使增量更改接口更容易。
- 允许访问更靠近使用点的总线元素，避免使用 Bus Selector 和 Goto 模块配置。

In Bus Element 模块属于 Inport 模块类型，Out Bus Element 模块属于 Outport 模块类型。
:::



### 创建重复 Inport 模块

您可以创建任意数量的 Inport 模块副本。副本是原型的图形表示，旨在通过去除不必要的线条来简化模块图。副本与原型具有相同的端口号、属性和输出。

要创建 Inport 模块的副本，请执行以下操作：

1. 在模块图中，选择要复制的未连接的 Inport 模块。
2. 按住 **Ctrl** 键并拖动模块。
3. 释放指针，然后从上下文菜单中选择**生成副本**。

您可以选择具有副本的 Inport 模块来突出显示副本模块。要在打开的图或新选项卡中显示相关模块，请使用光标在选择后出现的省略号上暂停。然后，从操作菜单中选择**相关模块** 。当多个模块对应于所选模块时，将打开一个相关模块列表。您可以通过在文本框中输入搜索词来过滤相关模块列表。从列表中选择相关模块后，窗口焦点转至显示该相关模块的打开的图或新选项卡。

### 将总线连接到根级 Inport 模块

如果您希望模型的根级 Inport 模块生成总线，请将**数据类型**参数设置为总线对象的名称（该总线对象定义 Inport 模块生成的总线）。

## 示例

将接收外部信号放大两倍。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Port/Inport.mo">Inport.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/PortPng/Inport/Inport01.png')" style="width: 600px; height: auto;">

## 端口

### 输出

<div class="details-box">
<details open>
<summary>Port_1 — 输入信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

通过输入端口流入系统的输入信号。

您可以在子系统中使用 Inport 模块，以结构体或任何其他格式提供定点数据。

**数据类型:** double | float | int8 | int16 | int32 | uint8 | uint16 | uint32 | Boolean | fixed point | enumerated | bus 

</div>
</div>


## 参数


### 常设

<div class="details-box">
<details open>
<summary>端口号 — 端口在父模块上的位置<div>1 (默认) | 实整数</div></summary>
</details>
<div class="details-content">

指定与模块对应的端口在父级 Subsystem 或 Model 模块上的显示顺序。

- 如果新添加的模块创建了一个新端口，则其端口号是下一个可用编号。
- 删除与某端口相关联的所有模块后，该端口也会被删除。其他端口会重新编号，使之依序排列且不跳过任何数字。
- 如果指定的端口号超过端口数量，则会为该编号和中间跳过的每个序号创建端口。

</div>
</div>


<!-- #### 编程用法

要以编程方式设置模块参数值，请使用 [`set_param`](https://ww2.mathworks.cn/help/simulink/slref/set_param.html) 函数。

| **参数:**     | `Port`                                 |
| ------------- | -------------------------------------- |
| **值:**       | `"1"` (默认) \| real integer in quotes |
| **数据类型:** | `char` | `string`                      |

**示例:** `set_param("mymodel/Subsystem1/PortBlock",Port="5")` -->

<!-- 暂无
### **图标显示** — 图标显示 **端口号** (默认) | **信号名称** | **端口号和信号名称**



指定在模块图标上显示的信息。

#### 编程用法

| **模块参数**：`IconDisplay`                                  |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值**：`'Signal name'` | `'Port number'` | `'Port number and signal name'` |
| **默认值**：`'Port number'`                                  | -->

<!-- 暂无

### **通过延迟外部信号锁存输入** — 通过延迟锁存信号的选项 `off` (默认) | `on`



选择此项以指定模块输出是上一个时间步的输入信号值。

选择此选项将使软件能够解析属于某个循环的触发子系统之间的数据依存关系。

Inport 模块通过显示 `<Lo>` 来指示已选择此选项。

![img](https://ww2.mathworks.cn/help/simulink/slref/inport_lo.png)



#### 依存关系

仅当模块表示触发子系统中的输入端口时，才会启用此参数。

#### 编程用法

| **模块参数**：`LatchByDelayingOutsideSignal` |
| -------------------------------------------- |
| **类型：**字符向量                           |
| **值：**`'on' | 'off'`                       |
| **默认值：**`'off'`                          | -->


<!-- 暂无
### **针对函数调用子系统输出的反馈信号锁存输入** — 锁存信号以防止更改 `off` (默认) | `on`



选择此选项可指定模块锁存输入值，并防止它在函数调用子系统执行期间发生更改。对于分支出来调用多个函数调用子系统的单次函数调用，使用此选项会中断当信号从一个函数调用子系统反馈到另一个函数调用子系统时形成的循环。选择此选项可防止在包含此模块的子系统执行期间调用的函数调用子系统的反馈信号值发生任何更改。

Inport 模块通过显示 `<Li>` 来指示已选择此选项。

![img](https://ww2.mathworks.cn/help/simulink/slref/inport_li.png)



#### 依存关系

仅当模块表示函数调用子系统中的输入端口时，才会启用此选项。

#### 编程用法

| **模块参数**：`LatchInputForFeedbackSignals` |
| -------------------------------------------- |
| **类型：**字符向量                           |
| **值：**`'on' | 'off'`                       |
| **默认值：**`'off'`                          | -->


<!-- 暂无
### **连接输入** — 打开根输入端口映射器工具的选项 按钮



要将信号和总线数据导入、可视化并映射到根级 Inport 模块，请点击此按钮。根输入端口映射器工具将打开。

#### 依存关系

仅当模块位于模型的根级时，此按钮才会出现。 -->

### 信号属性


<!-- 暂无
### **输出函数调用** — 产生函数调用事件的选项 `off` (默认) | `on`



指定输入信号产生函数调用事件信号。

如果当前模型在顶层模型中被引用时必须接受函数调用事件信号，请选择此选项。

#### 依存关系

- 要启用此选项，该模块必须在异步函数调用中。
- 当**数据类型**指定 `Simulink.ValueType` 对象时，软件会忽略此参数的值。

#### 编程用法

| **模块参数**：`OutputFunctionCall` |
| ---------------------------------- |
| **类型**：字符向量                 |
| **值**：`'off'` | `'on'`           |
| **默认值**：`'off'`                | -->


<!-- 暂无
### **最小** — 最小输出值 `[]` (默认) | 标量



软件检查的输出范围的下限值。

此数字必须为有限双精度实数标量值。

软件使用此值执行：

- 仿真范围检查（请参阅[指定信号范围](https://ww2.mathworks.cn/help/simulink/ug/signal-ranges.html)）。
- 定点数据类型的自动定标。
- 从模型生成的代码的优化。此优化可删除算法代码，并影响某些仿真模式（如 SIL 或外部模式）的结果。有关详细信息，请参阅[Optimize using the specified minimum and maximum values](https://ww2.mathworks.cn/help/ecoder/ref/optimizeusingthespecifiedminimumandmaximumvalues.html) (Embedded Coder)。



#### 依存关系

当**数据类型**指定 `Simulink.ValueType` 或 `Simulink.Bus` 对象时，软件会忽略此参数的值。软件改用 `Simulink.ValueType` 对象或 `Simulink.Bus` 对象中的 `Simulink.BusElement` 对象指定的最小值。

#### 编程用法

| **模块参数**：`OutMin` |
| ---------------------- |
| **类型**：字符向量     |
| **值**：`'[ ]'`\| 标量 |
| **默认值**：`'[ ]'`    | -->


<!-- 暂无
### **最大** — 最大输出值 `[]` (默认) | 标量



软件检查的输出范围的上限值。

此数字必须为有限双精度实数标量值。

软件使用此值执行：

- 仿真范围检查（请参阅[指定信号范围](https://ww2.mathworks.cn/help/simulink/ug/signal-ranges.html)）。
- 定点数据类型的自动定标。
- 从模型生成的代码的优化。此优化可删除算法代码，并影响某些仿真模式（如 SIL 或外部模式）的结果。有关详细信息，请参阅[Optimize using the specified minimum and maximum values](https://ww2.mathworks.cn/help/ecoder/ref/optimizeusingthespecifiedminimumandmaximumvalues.html) (Embedded Coder)。



#### 依存关系

当**数据类型**指定 `Simulink.ValueType` 或 `Simulink.Bus` 对象时，软件会忽略此参数的值。软件改用 `Simulink.ValueType` 对象或 `Simulink.Bus` 对象中的 `Simulink.BusElement` 对象指定的最大值。

#### 编程用法

| **模块参数**：`OutMax` |
| ---------------------- |
| **类型**：字符向量     |
| **值**：`'[ ]'`\| 标量 |
| **默认值**：`'[ ]'`    |
 -->

<div class="details-box">
<details open>
<summary>数据类型 — 输出数据类型<div>Inherit: auto (默认) | double | single | half | int8 | uint8 | int16 | uint16</div></summary>
</details>
<div class="details-content">

指定外部输入的输出数据类型。该类型可以继承、直接指定或表示为数据类型对象。

</div>
</div>


<!-- 
您可以指定以下任一选项：

- 继承的数据类型
- 内置 Simulink® 数据类型 - 例如，指定 **single** 或 **uint8**。请参阅 [Simulink 支持的数据类型](https://ww2.mathworks.cn/help/simulink/ug/data-types-supported-by-simulink.html)。
- 定点数据类型 - 使用 [`fixdt`](https://ww2.mathworks.cn/help/simulink/slref/simulink.numerictype.fixdt.html) 函数。例如，指定 **fixdt(1,16,0)**。
- 枚举数据类型 - 使用以 `Enum:` 开头的类型名称。例如，指定 **Enum: myEnumType**。
- 总线数据类型 - 使用以 `Bus:` 开头的 [`Simulink.Bus`](https://ww2.mathworks.cn/help/simulink/slref/simulink.bus.html) 对象的名称。例如，指定 **Bus: myBusObject**。
- Simulink 图像数据类型 - 如果您有 Computer Vision Toolbox™，请使用 [`Simulink.ImageType`](https://ww2.mathworks.cn/help/vision/ref/simulink.imagetype.html) (Computer Vision Toolbox) 对象的构造函数，并指定描述图像的属性。默认情况下，数据类型使用 `Simulink.ImageType(480,640,3)` 表达式，分别表示图像的行、列和通道。
- 值类型 - 使用以 `ValueType:` 开头的 [`Simulink.ValueType`](https://ww2.mathworks.cn/help/simulink/slref/simulink.valuetype.html) 对象的名称。例如，指定 **ValueType: windVelocity**。
- 自定义数据类型 - 使用指定类型的 MATLAB® 表达式。例如，您可以指定一个 [`Simulink.NumericType`](https://ww2.mathworks.cn/help/simulink/slref/simulink.numerictype.html) 对象，其 `DataTypeMode` 属性设置为 `'Fixed-point: unspecified scaling'` 以外的值。



当您指定 `Simulink.ValueType` 或 `Simulink.Bus` 对象作为数据类型时，会忽略 Inport 模块的一些参数。例如，忽略 Inport 模块的 **Min**、**Max** 和 **Unit** 参数。软件改用 `Simulink.ValueType` 对象或 `Simulink.Bus` 对象中 `Simulink.BusElement` 对象的对应属性。例如，假设一个模块将**单位**设置为 `ft/s`。当该模块的**数据类型**指定以 `m/s` 为单位的 `ValueType` 对象时，该模块会使用 `m/s` 而不是 `ft/s` 作为单位。 -->

<!-- 
#### 编程用法

| **模块参数**：`OutDataTypeStr`                               |
| ------------------------------------------------------------ |
| **类型**：字符向量                                           |
| **值**：`'Inherit: auto'` | `'double'` | `'float'` | `'int8'` | `'uint8'` | `'int16'` | `'uint16'` | `'int32'` | `'uint32'` | `'boolean'` | `'fixdt(1,16)'` | `'fixdt(1,16,0)'` | `'fixdt(1,16,2^0,0)'` | `'Enum: <class name>'` | `'Bus: <object name>'` | `'ValueType: <object name>'` | `'<data type expression>'` | `Simulink.ImageType(480,640,3)` |
| **默认值**：`'Inherit: auto'`                                | -->


<!-- 暂无
### **锁定输出数据类型设置以防止被定点工具更改** — 防止定点工具覆盖数据类型的选项 `off` (默认) | `on`



选择此参数可防止定点工具覆盖您在模块上指定的输出数据类型。有关详细信息，请参阅[Use Lock Output Data Type Setting](https://ww2.mathworks.cn/help/fixedpoint/ug/best-practices-for-using-the-fixed-point-tool-to-propose-data-types-for-your-simulink-model.html#br9an48) (Fixed-Point Designer)。

#### 依存关系

当**数据类型**指定 `Simulink.ValueType` 对象时，软件会忽略此参数的值。

#### 编程用法

| **模块参数**：`LockScale` |
| ------------------------- |
| **值**：`'off'` | `'on'`  |
| **默认值**：`'off'`       | -->


<!-- 暂无
### **以非虚拟总线输出** — 指定总线输出的虚拟性的选项 `off` (默认) | `on`



指定用于加载总线数据的顶层 Inport 模块的输出是虚拟的还是非虚拟的。

- 选择此参数可指定非虚拟总线输出。
- 清除此参数可指定虚拟总线输出。



#### 提示

- 非虚拟总线中的所有信号都必须具有相同的采样时间，即使关联的总线对象为某些元素指定了继承采样时间也是如此。任何可能导致包含不同采样率信号的非虚拟总线的操作都会生成错误。您不能为非虚拟总线加载多速率数据。有关如何将具有不同采样率的信号作为非虚拟总线传递给引用模型的详细信息，请参阅[Modify Sample Times for Nonvirtual Buses](https://ww2.mathworks.cn/help/simulink/ug/specify-bus-signal-sample-times.html)。

  要为总线加载多速率数据，请清除**以非虚拟总线输出**参数，并将**采样时间**参数设置为继承 (`-1`)。

- 对于模型引用层次结构的顶层模型，代码生成将创建一个 C 结构体来表示非虚拟总线输出。

- 对于引用的模型，选择此选项将在生成的代码中创建一个 C 结构体。否则，代码生成过程将为总线的每个叶元素创建一个参量。

#### 依存关系

要启用此参数，请进行如下设置：

- 该模块必须位于模型的顶层。
- **数据类型**模块参数必须解析为 `Simulink.Bus` 对象。例如，将**数据类型**设置为 `Simulink.Bus` 对象，或设置为将 `Simulink.Bus` 对象指定为其数据类型的 `Simulink.ValueType` 对象。



#### 编程用法

| **模块参数**：`BusOutputAsStruct` |
| --------------------------------- |
| **类型**：字符向量                |
| **值**：`'off'` | `'on'`          |
| **默认值**：`'off'`               | -->


<!-- 暂无
### **单位(例如，m、m/s^2、N\*m)** — 模块的输入信号的物理单位 `inherit` (默认) | `<Enter unit>`



指定模块的输入信号的物理单位。要指定单位，请在文本框中键入需要的值。随着您的键入，参数将显示可能匹配的单位。有关支持的单位列表，请使用 [`showunitslist`](https://ww2.mathworks.cn/help/simulink/slref/showunitslist.html) 函数。

要约束单位制，请点击参数右侧的链接：

- 如果组件中存在 [Unit System Configuration](https://ww2.mathworks.cn/help/simulink/slref/unitsystemconfiguration.html) 模块，将打开其对话框。使用该对话框为组件指定允许和不允许使用的单位制。
- 如果组件中不存在 [Unit System Configuration](https://ww2.mathworks.cn/help/simulink/slref/unitsystemconfiguration.html) 模块，将显示模型的“配置参数”对话框。使用该对话框为模型指定允许和不允许使用的单位制。

#### 依存关系

当**数据类型**指定 `Simulink.ValueType` 或 `Simulink.Bus` 对象时，软件会忽略此参数的值。软件改用 `Simulink.ValueType` 对象或 `Simulink.Bus` 对象中的 `Simulink.BusElement` 对象指定的单位。

#### 编程用法

| **模块参数**：`Unit`                   |
| -------------------------------------- |
| **类型：**字符向量                     |
| **值**：`'inherit'` | `'<Enter unit>'` |
| **默认值**：`'inherit'`                |

要指定模块的输入信号的物理单位而不传播，请使用 `UnitNoProp`。 -->

<div class="details-box">
<details open>
<summary>端口维度(-1 表示继承) — 端口维度<div>-1 (默认) | 整数 | [整数 整数]</div></summary>
</details>
<div class="details-content">

指定输出信号的维度。

| `-1`    | 端口可以为具有任何维度的信号加载数据。端口从连接的信号继承维度。 |
| ------- | ------------------------------------------------------------ |
| `N`     | 端口可以为大小是 `N` 的向量信号加载数据。                    |
| `[R C]` | 端口可以为 `R` 行 `C` 列矩阵信号加载数据。                   |

</div>
</div>



<!-- 
#### 编程用法

| **模块参数**：`PortDimensions`        |
| ------------------------------------- |
| **类型**：字符向量                    |
| **值**：`'-1'` \| 整数 \| [整数 整数] |
| **默认值**：`'-1'`                    | -->


<!-- 暂无
### **可变大小信号** — 允许或不允许可变大小信号的选项 **继承** (默认) | **否** | **是**



指定此端口允许的信号类型。要同时允许可变大小和固定大小的信号，请选择 **inherit**。要仅允许可变大小信号，请选择**是**。要仅允许固定大小的信号，请选择**否**。

当此端口的信号为可变大小的信号时，**端口维度**参数将指定信号的最大维度。

#### 依存关系

当**数据类型**指定 `Simulink.ValueType` 对象时，软件会忽略此参数的值。软件改用 `Simulink.ValueType` 对象指定的维度模式。

#### 编程用法

| **参数**：`VarSizeSig`                 |
| -------------------------------------- |
| **类型：**字符向量                     |
| **值：**`'Inherit'` | `'No'` | `'Yes'` |
| **默认值：**`'Inherit'`                | -->

<!-- 暂无

### **信号类型** — 输出信号类型 **自动** (默认) | **实数** | **复**



指定信号输出的复/实性。要继承与其输入相连的信号的复/实性，请选择**自动**。否则，请选择实信号或复信号类型。

#### 依存关系

当**数据类型**指定 `Simulink.ValueType` 或 `Simulink.Bus` 对象时，软件会忽略此参数的值。软件改用 `Simulink.ValueType` 对象或 `Simulink.Bus` 对象中的 `Simulink.BusElement` 对象指定的复/实性。

#### 编程用法

| **模块参数**：`SignalType`                |
| ----------------------------------------- |
| **类型：**字符向量                        |
| **值**：`'auto'` | `'real'` | `'complex'` |
| **默认值：**`'auto'`                      | -->

### 执行

<div class="details-box">
<details open>
<summary>采样时间（-1 表示继承） — 指定采样时间的选项<div>-1 (默认) | 标量</div></summary>
</details>
<div class="details-content">

指定采样时间命中点之间的离散间隔，或指定另一个采样时间类型。

默认情况下，模块根据模型中的模块上下文继承其采样时间。

#### 依存关系

仅当模块表示根级输入端口时，此参数才可见。

</div>
</div>


<!-- 
#### 编程用法

| **模块参数**：`SampleTime` |
| -------------------------- |
| **类型：**字符向量         |
| **值：**标量               |
| **默认值：**`'-1'`         | -->


<!-- 
### **数据插值** — 对输出数据进行线性插值的选项 `on` (默认) | `off`



从将数据从工作区加载到根级别 Inport 模块中时，指定模块在没有对应数据的时间步处是否对输出值进行线性内插和外插。

要从工作区加载离散数据，请执行以下操作：

1. 将**采样时间**设置为离散速率，例如 `2`。
2. 清除**数据插值**。


软件使用以下内插和外插：

- 对于第一个指定数据点与最后一个指定数据点之间的时间步 - 零阶保持。
- 对于第一个指定数据点之前和最后一个指定数据点之后的时间步 - 接地值。
- 对于第一个指定数据点之前的时间步的大小可变信号 - 如果是单精度或双精度数据类型，则记录 `NaN` 值，如果是其他数据类型，则记录接地值。对于最后一个指定数据点之后的时间步，软件使用接地值。 -->

<!-- 
#### 编程用法

| **模块参数**：`Interpolate` |
| --------------------------- |
| **类型：**字符向量          |
| **值：**`'on' | 'off'`      |
| **默认值：**`'on'`          | -->


<!-- 
### **事件** — 根据流入端口的数据流触发模型分区的选项 事件触发器对象的元胞数组



在基于速率的系统中，您可以在顶层模型或模型引用接口上配置输入端口，以触发执行一个或多个模型分区，从而响应流入端口的数据流。**事件**参数存储与端口相关联的事件触发器。每个事件触发器都会将一个输入事件映射到它所触发的调度事件的名称。模型的调度指定因响应调度事件而执行的分区以及执行分区时的优先级。

下表总结了您可以配置的事件触发器。对于每个输入端口，您可以为每个输入事件配置一个事件触发器。

| 输入事件     | 输入事件描述                       | 事件触发器对象                                               |
| :----------- | :--------------------------------- | :----------------------------------------------------------- |
| 输入写入     | 输入端口更新了值。                 | [`simulink.event.InputWrite`](https://ww2.mathworks.cn/help/simulink/slref/simulink.event.inputwrite.html) |
| 输入写入超时 | 输入端口值未在指定的时间量内更新。 | [`simulink.event.InputWriteTimeout`](https://ww2.mathworks.cn/help/simulink/slref/simulink.event.inputwritetimeout.html) |
| 输入写入丢失 | 输入端口值更新覆盖了未处理的数据。 | [`simulink.event.InputWriteLost`](https://ww2.mathworks.cn/help/simulink/slref/simulink.event.inputwritelost.html) |

要为您的模型配置调度，请使用[调度编辑器](https://ww2.mathworks.cn/help/simulink/slref/scheduleeditor.html)。 -->


<!-- 
#### 编程用法

| **模块参数**：`EventTriggers`                                |
| ------------------------------------------------------------ |
| **值：**`1`×`1` 元胞数组 | `2`×`1` 元胞数组 | `3`×`1` 元胞数组 |
| **默认值：**`[]`                                             | -->

<!-- ## 模块特性 -->
<!-- 部分特性暂无
| **数据类型**     | `Boolean` | `bus` | `double` | `enumerated` | `fixed point` | `half` | `integer` | `single` | `string` |
| ---------------- | ------------------------------------------------------------ |
| **直接馈通**     | `否`                                                         |
| **多维信号**     | `是`                                                         |
| **可变大小信号** | `是`                                                         |
| **过零检测**     | `否`                                                         |-->

<!-- ## 扩展功能  -->
<!-- 


### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 VHDL、Verilog 和 SystemVerilog 代码。



HDL Coder™ 提供影响 HDL 实现和综合逻辑的额外配置选项。

**HDL 架构**

此模块具有一个默认 HDL 架构。

**HDL 模块属性**

| 通用                  |                                                              |
| :-------------------- | ------------------------------------------------------------ |
| **BalanceDelays**     | **BalanceDelays** 设置描述**on**（默认值）检测 DUT 中其他路径上引入的延迟，并在 Inport 模块路径上插入匹配的延迟。**off**在 DUT 子系统的输入端口上禁用延迟平衡，以防止 HDL Coder 插入不必要的匹配延迟。例如，如果 DUT 子系统中的 Inport 模块位于具有稳定输入的路径上，即输入端口的输入信号是来自 DUT 之外的稳定输入信号，则可禁用该模块上的 **BalanceDelays**。**注意**此属性仅影响 DUT 级别的 Inport 模块。 |
| **BidirectionalPort** | **BidirectionalPort** 设置描述**on**将端口指定为双向。需满足以下要求：端口必须位于采用黑盒实现的 Subsystem 模块中。同时，双向端口与对应的顶层 DUT 子系统端口之间不能有逻辑关系。有关详细信息，请参阅 [Specify Bidirectional Ports](https://ww2.mathworks.cn/help/hdlcoder/ug/specify-bidirectional-ports.html) (HDL Coder)。**off**（默认值）不将端口指定为双向。 |

| 目标设定               |                                                              |
| :--------------------- | ------------------------------------------------------------ |
| **IOInterface**        | DUT 端口的目标平台接口类型，指定为字符向量。对于不是 DUT 端口的 Inport 和 Outport 模块，`IOInterface` 模块属性被忽略。要指定有效的 `IOInterface` 设置，请使用 HDL 工作流顾问：在 HDL 工作流顾问中，在**设置目标** > **设置目标接口**步骤中，请在**目标平台接口表**中的**目标平台接口**列中，使用下拉列表设置目标平台接口类型。保存模型。`IOInterface` 值保存为端口的 HDL 模块属性。例如，要查看 `IOInterface` 值，如果 DUT 端口的完整路径是 `hdlcoder_led_blinking/led_counter/LED`，请输入：`hdlget_param('hdlcoder_led_blinking/led_counter/LED', 'IOInterface')` |
| **IOInterfaceMapping** | DUT 端口的目标平台接口端口映射，指定为字符向量。对于不是 DUT 端口的 Inport 和 Outport 模块，`IOInterfaceMapping` 模块属性被忽略。要指定有效的 `IOInterfaceMapping` 设置，请使用 HDL 工作流顾问：在 HDL 工作流顾问中，在**设置目标** > **设置目标接口**步骤中，请在**目标平台接口表**中的**目标平台接口**列中，使用下拉列表设置目标平台接口类型。在**位范围 / 地址 / FPGA 引脚**列中，如果要更改默认值，请输入目标平台接口映射。保存模型。`IOInterfaceMapping` 值保存为端口的 HDL 模块属性。例如，要查看 `IOInterfaceMapping` 值，如果 DUT 端口的完整路径是 `hdlcoder_led_blinking/led_counter/LED`，请输入：`hdlget_param('hdlcoder_led_blinking/led_counter/LED',...             'IOInterfaceMapping')` |
| **IOInterfaceOptions** | DUT 端口的目标平台接口端口映射选项，指定为字符向量。对于不是 DUT 端口的 Inport 和 Outport 模块，`IOInterfaceOptions` 模块属性被忽略。要指定有效的 `IOInterfaceOptions` 设置，请使用 HDL 工作流顾问：在 HDL 工作流顾问的**设置目标** > **设置目标接口**步骤中，在**目标平台接口表**中的**目标平台接口**列中，将输入或输出端口映射到 AXI4 下级接口。在**接口选项**列中，如果要更改默认初始值，请点击**选项**按钮，并为 **RegisterInitialValue** 输入值。保存模型。`IOInterfaceOptions` 值保存为端口的 HDL 模块属性。例如，要查看 `IOInterfaceOptions` 值，如果 DUT 端口的完整路径是 `hdlcoder_led_blinking/led_counter/LED`，请输入：`hdlget_param('hdlcoder_led_blinking/led_counter/LED',...             'IOInterfaceOptions')` |

| 帧到采样的转换       |                                                              |
| :------------------- | ------------------------------------------------------------ |
| **ConvertToSamples** | **ConvertToSamples** 设置描述**on**使用帧到采样的转换优化将传入的矩阵输入信号转换为采样。要使用此属性，请启用模型配置参数**启用帧到采样的转换**。有关详细信息，请参阅[Enable frame to sample conversion](https://ww2.mathworks.cn/help/hdlcoder/ref/enableframetosampleconversion.html) (HDL Coder)。**off**（默认值）不将传入的矩阵输入信号转换为采样。 |

**`Simulink.ValueType` 对象支持**

此模块支持 `Simulink.ValueType` 对象的生成代码。有关值类型的详细信息，请参阅[Specify Common Set of Signal Properties as Value Type](https://ww2.mathworks.cn/help/simulink/ug/specify-simulink-value-types.html)。



### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。 -->

## 版本历史记录

- 在 2024b 之前推出

### 限制信息
不支持部分
1. 参数-常设-通过延迟外部信号锁存输入 — 通过延迟锁存信号的选项
2. 参数-常设-针对函数调用子系统输出的反馈信号锁存输入的选项 — 锁存信号以防止更改
3. 参数-常设-连接输入 — 打开根输入端口映射器工具的选项
4. 参数-常设-输出函数调用 — 产生函数调用事件的选项
5. 参数-信号属性-输出函数调用 — 产生函数调用事件的选项
6. 参数-信号属性-最小值 — 最小输出值
7. 参数-信号属性-最大值 — 最大输出值
8. 参数-信号属性-锁定输出数据类型设置以防止被定点工具更改 — 防止定点工具覆盖数据类型
9. 参数-信号属性-以非虚拟总线输出 — 指定总线输出的虚拟性的选项
10. 参数-信号属性-单位(例如，m、m/s^2、N*m) — 模块的输入信号的物理单位
11. 参数-信号属性-可变大小信号 — 允许或不允许可变大小信号的选项
12. 参数-信号属性-信号类型 — 输出信号类型
13. 参数-执行-数据插值 — 对输出数据进行线性插值的选项
14. 参数-执行-事件 — 根据流入端口的数据流触发模型分区的选项


## 另请参阅

[Outport](Outport.html) 


<!-- ### 主题

- [将数据加载到根级输入端口](https://ww2.mathworks.cn/help/simulink/ug/load-data-to-root-level-input-ports-1.html)
- [使用函数调用子系统](https://ww2.mathworks.cn/help/simulink/ug/using-function-call-subsystems.html)
- [使用根输入端口映射器工具映射数据](https://ww2.mathworks.cn/help/simulink/ug/map-data-using-root-inport-mapper-tool.html)
- [Load Big Data for Simulations](https://ww2.mathworks.cn/help/simulink/ug/load-big-data-for-simulations.html)
- [Comparison of Signal Loading Techniques](https://ww2.mathworks.cn/help/simulink/ug/comparison-of-signal-loading-techniques.html)
- [Map Root Inport Signal Data](https://ww2.mathworks.cn/help/simulink/ug/overview-of-root-inport-signal-data-mapping.html) -->
