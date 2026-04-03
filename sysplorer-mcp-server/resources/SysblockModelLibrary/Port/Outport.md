# Outport
---
&nbsp;

输出端口

- **库:** Sysblock / Port

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/PortPng/Outport/Outport.png')" style="width: 100px; height: auto;">

## 描述

Outport 模块将信号从系统内链接到系统外部的目标。它们可以连接从子系统流动到模型其他部分的信号。它们还可以在模型层次结构的顶层提供外部输出。

Outport 模块端口号根据以下规则进行分配：

- 根级系统或子系统中的 Outport 模块按顺序编号，从 1 开始。
- 如果添加一个 Outport 模块，Sysblock 将为其分配下一个可用的编号。
- 如果您删除一个 Outport 模块，其他端口号会自动重新编号，以确保 Outport 模块的连续的且没有遗漏任何编号。

### 子系统中的 Outport 模块

子系统中的 Outport 模块表示来自子系统的输出。到达子系统中某个 Outport 模块的信号将从 Subsystem 模块上的关联输出端口流出。与输出端口关联的 Outport 模块是指**端口号**参数与该输出端口在 Subsystem 模块上的相对位置匹配的模块。例如，**端口号**参数为 `1` 的 Outport 模块将其信号发送给与 Subsystem 模块上最上面的输出端口连接的模块。

如果您对 Outport 模块的**端口号**重新进行编号，模块将连接到一个不同的输出端口。模块会继续将信号发送给子系统外部的同一个模块。

您可以直接编辑 Subsystem 模块上的端口标签。


**提示**

对于包含总线的模型，如果总线信号中包含很多总线元素，则可以考虑使用 In Bus Element 和 Out Bus Element 模块。这些模块可以：

- 减少模块图中信号线的复杂度和杂乱无章。
- 使增量更改接口更容易。
- 允许访问更靠近使用点的总线元素，避免使用 Bus Selector 和 Goto 模块配置。

In Bus Element 模块属于 Inport 模块类型，Out Bus Element 模块属于 Outport 模块类型。

### 模型层次结构中的顶层 Outport 模块

模型层次结构顶层的 Outport 模块有两种用途。它们可以为基础工作区提供外部输出，为 `linmod` 和 `trim` 分析函数提供一种从系统中获取输出的方法。


将 `y` 写入为矩阵，每一列均包含一个不同 Outport 模块的数据。列顺序与 Outport 模块的端口号顺序匹配。

如果您在第二个 (state) 参量之后指定多个变量名称，系统会将来自每个 Outport 模块的数据写入不同的变量。例如，如果系统有两个 Outport 模块，要将 Outport 模块 1 的数据保存到 `speed`，将 Outport 模块 2 的数据保存到 `dist`，请指定以下命令：


### 将总线连接到根级 Outport

只有当虚拟总线中的所有元素均具有相同的数据类型时，模型中的根级 Outport 模块才会接受虚拟总线。Outport 模块自动将总线统一为与总线具有相同元素数的向量并提供该向量作为输出。

如果希望模型的根级 Outport 模块接受包含混合类型的总线，请将 Outport 模块**数据类型**设置为 `Bus: <object name>`。

## 示例

输出一个正弦波。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Port/Outport.mo">Outport.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/PortPng/Outport/Outport01.png')" style="width: 600px; height: auto;">

## 端口

### 输入

<div class="details-box">
<details open>
<summary>Port_1 — 输出端口信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

通过输出端口流向外部子系统或模型的输入信号。

当 Outport 模块不是根级输出端口时，可以接受定点和枚举数据类型。模块输出的复/实性和数据类型与其输入相同。

**数据类型:**  float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | Boolean | fixed point | enumerated | bus

</div>
</div>

## 参数

<!-- ### 常设 -->

<!-- 暂无

### **端口号** — 端口在父模块上的位置 `1` (默认) | 实整数



指定与模块对应的端口在父级 Subsystem 或 Model 模块上的显示顺序。

- 如果新添加的模块创建了一个新端口，则其端口号是下一个可用编号。
- 删除与某端口相关联的所有模块后，该端口也会被删除。其他端口会重新编号，使之依序排列且不跳过任何数字。
- 如果指定的端口号超过端口数量，则会为该编号和中间跳过的每个序号创建端口。



#### 编程用法

要以编程方式设置模块参数值，请使用 [`set_param`](https://ww2.mathworks.cn/help/simulink/slref/set_param.html) 函数。

| **参数:**     | `Port`                                 |
| ------------- | -------------------------------------- |
| **值:**       | `"1"` (默认) \| real integer in quotes |
| **数据类型:** | `char` | `string`                      |

**示例:** `set_param("mymodel/Subsystem1/PortBlock",Port="5")` -->


<!-- 暂无
### **信号名称** — 信号名称 `' '` (默认) | 字符向量



指定生成的代码中的相应信号数据的名称。使用此参数可以指定当您将存储类应用到根级 Outport 模块时信号数据的名称。

#### 依存关系

要启用此参数，该模块必须位于模型的顶层。

#### 编程用法

| **模块参数**：`SignalName` |
| -------------------------- |
| **类型：**字符向量         |
| **值：**字符向量           |
| **默认值：**`' '`          | -->


<!-- 暂无
### **图标显示** — 图标显示 **端口号** (默认) | **信号名称** | **端口号和信号名称**



指定在模块图标上显示的信息。

#### 编程用法

| **模块参数**：`IconDisplay`                                  |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值**：`'Signal name'` | `'Port number'` | `'Port number and signal name'` |
| **默认值**：`'Port number'`                                  |
 -->

<!-- 暂无
### **指定未连接源时的输出** — 指定未连接的输出值 `off` (默认) | `on`



指定未连接信源时的常量输出值。

#### 依存关系

适用于 Variant Subsystem 模块内未连接的 Outport 模块。

#### 编程用法

| **模块参数**：`OutputWhenUnconnected` |
| ------------------------------------- |
| **类型：**字符向量                    |
| **值：**`'on' | 'off'`                |
| **默认值：**`'off'`                   | -->


<!-- 暂无
### **常量值** — 模块未连接时的输出值 `0` (默认) | 标量 | 向量



指定未连接信源时的常量输出值。

#### 依存关系

适用于未连接的 Outport 模块的 Variant Subsystem 模块（**指定未连接源时的输出**处于选中状态）。

#### 编程用法

| **模块参数**：`OutputWhenUnconnectedValue` |
| ------------------------------------------ |
| **类型：**字符向量                         |
| **值：**`scalar` | `vector`                |
| **默认值：**`'0'`                          | -->


<!-- 暂无
### **将向量参数解释为一维向量** — 将向量视为一维 `on` (默认) | `off`



如果**常量值**参数的计算结果为包含 `N` 个元素的行或列向量，选中此复选框将输出长度为 `N` 的向量。

#### 依存关系

适用于未连接的 Outport 模块上的 Variant Subsystem 模块（当您选择了**指定未连接源时的输出**参数时）。

#### 编程用法

| **模块参数**：`VectorParamsAs1DForOutWhenUnconnected` |
| ----------------------------------------------------- |
| **类型：**字符向量                                    |
| **值：**`'on' | 'off'`                                |
| **默认值：**`'on'`                                    | -->



<!-- ### **确保输出端口为虚拟端口** — 确保输出端口为虚拟 `off` (默认) | `on`



清除此参数可允许 Simulink® 在输出端口上使用信号缓冲区。 -->

<!-- 此缓冲区等效于 [Signal Copy](https://ww2.mathworks.cn/help/simulink/slref/signalconversion.html) 模块，但不显示在画布上，可确保 Outport 模块信号的初始化保持一致。

如果选择此参数，Simulink 会尝试删除信号缓冲区。

- 如果不需要信号缓冲区，Simulink 将删除缓冲区。
- 如果为确保数据一致性和正常执行而需要信号缓冲区，Simulink 会显示错误，指示可能无法删除缓冲区。



允许通过 [Assignment](https://ww2.mathworks.cn/help/simulink/slref/assignment.html) 模块部分写入。

有关此参数的详细信息，包括具有条件写入和部分写入的示例，请参阅[Ensure Output Port Is Virtual](https://ww2.mathworks.cn/help/simulink/ug/ensure-outport-is-virtual.html)。 -->



<!-- 
**注意**

如果该模块位于模型的根级，并且由 [Initialize Function](https://ww2.mathworks.cn/help/simulink/slref/initializefunction.html) 模块、[Reset Function](https://ww2.mathworks.cn/help/simulink/slref/resetfunction.html) 模块、[Reinitialize Function](https://ww2.mathworks.cn/help/simulink/slref/reinitializefunction.html) 模块或 [Terminate Function](https://ww2.mathworks.cn/help/simulink/slref/terminatefunction.html) 模块内的另一个 Outport 模块驱动，则该模块始终为虚拟模块。 -->

<!-- #### 依存关系

此参数适用于以下模块：

- 条件子系统
- Assignment
- Merge
- 具有根 Outport 模块的模型 -->

<!-- 
#### 编程用法

| **模块参数**：`EnsureOutportIsVirtual` |
| -------------------------------------- |
| **类型：**字符向量                     |
| **值：**`'on' | 'off'`                 |
| **默认值：**`'off'`                    | -->


<!-- 暂无
### **禁用时的输出** — 禁用时的输出 **保持** (默认) | **重置**



指定子系统被禁用的情况下，模块输出会出现什么情况。选择**保持**表示当子系统被禁用时，输出保持不变。选择**重置**表示当子系统被禁用时，输出将重置为**初始输出**指定的值。

#### 依存关系

当 Outport 模块位于具有有效启用和禁用语义的条件子系统中时可用。例如，该参数适用于 Enabled Subsystem 模块内的 Outport 模块，不适用于 Triggered Subsystem 模块内的 Outport 模块。

如果 Outport 模块位于 Function-Call Subsystem 模块内，则仅当 Function-Call Subsystem 模块连接到 Stateflow® 图中的某个状态时，此参数才有意义。有关详细信息，请参阅[Bind a Function-Call Subsystem to a State](https://ww2.mathworks.cn/help/stateflow/ug/using-bind-actions-to-control-function-call-subsystems.html#bqlq35y) (Stateflow)。

将条件子系统的输出连接到 [Merge](https://ww2.mathworks.cn/help/simulink/slref/merge.html) 模块时，请将此参数设置为**保持**。将其设置为**重置**会返回错误。

#### 编程用法

| **模块参数**：`OutputWhenDisabled` |
| ---------------------------------- |
| **类型：**字符向量                 |
| **值**：`'held' | 'reset'`         |
| **默认值：**`'held'`               | -->


<!-- 暂无
### **初始输出** — 条件执行子系统的初始输出 `[]` (默认) | 标量 | 结构体



对于条件执行子系统，请在子系统执行之前且此选项处于禁用状态时指定模块输出。要从输入信号继承初始输出值，请应用以下两种默认设置：

- 将**初始输出**参数设置为 `[]`。
- 将**[禁用时的输出](https://ww2.mathworks.cn/help/simulink/slref/outport.html#brqe2q3-28)**参数设置为**保持**。

Simulink 尝试从输入信号继承输出值。然而，如果输入信号不是初始输出值的有效源，则初始输出值 `[]` 被视为 `double(0)`。有关详细信息，请参阅[条件子系统初始输出值](https://ww2.mathworks.cn/help/simulink/ug/specify-or-inherit-conditional-subsystem-initial-values.html)。

有关指定初始条件结构体的信息，请参阅[Specify Initial Conditions for Bus Elements](https://ww2.mathworks.cn/help/simulink/ug/specifying-initial-conditions-for-buses.html)。

#### 提示

如果条件子系统驱动的是 Merge 模块，则无需为 Outport 模块指定初始条件 (IC)。有关详细信息，请参阅 [Underspecified initialization detection](https://ww2.mathworks.cn/help/simulink/gui/underspecifiedinitializationdetection.html)。

#### 依存关系

当 Outport 模块位于条件子系统内部时可用。

#### 限制



- 此模块不允许初始输出为 `inf` 或 `NaN`。
- 当输入是虚拟总线时，**初始输出**值 `[]` 被视为 `double(0)`。
- 当输入包含非虚拟总线时，**初始输出**不支持非零标量值。



#### 编程用法

| **模块参数**：`InitialOutput`    |
| -------------------------------- |
| **类型：**字符向量               |
| **值：**`'[]'` \| 标量 \| 结构体 | 
| **默认值：**`'[]'`               |-->

<!-- ### 信号属性 -->

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
| **默认值**：`'[ ]'`    | -->

<div class="details-box">
<details open>
<summary>数据类型 — 输出数据类型<div>Inherit: auto（默认）| double | float | int8 | uint8 | int16 |uint16</div></summary>
</details>
<div class="details-content">

当数据类型指定对象时，软件会忽略此参数的值。

</div>
</div> -->

<!-- 
您可以指定以下任一选项：

- 继承的数据类型
- 内置 Simulink 数据类型 - 例如，指定 **single** 或 **uint8**。请参阅 [Simulink 支持的数据类型](https://ww2.mathworks.cn/help/simulink/ug/data-types-supported-by-simulink.html)。
- 定点数据类型 - 使用 [`fixdt`](https://ww2.mathworks.cn/help/simulink/slref/simulink.numerictype.fixdt.html) 函数。例如，指定 **fixdt(1,16,0)**。
- 枚举数据类型 - 使用以 `Enum:` 开头的类型名称。例如，指定 **Enum: myEnumType**。
- 总线数据类型 - 使用以 `Bus:` 开头的 [`Simulink.Bus`](https://ww2.mathworks.cn/help/simulink/slref/simulink.bus.html) 对象的名称。例如，指定 **Bus: myBusObject**。
- Simulink 图像数据类型 - 如果您有 Computer Vision Toolbox™，请使用 [`Simulink.ImageType`](https://ww2.mathworks.cn/help/vision/ref/simulink.imagetype.html) (Computer Vision Toolbox) 对象的构造函数，并指定描述图像的属性。默认情况下，数据类型使用 `Simulink.ImageType(480,640,3)` 表达式，分别表示图像的行、列和通道。
- 值类型 - 使用以 `ValueType:` 开头的 [`Simulink.ValueType`](https://ww2.mathworks.cn/help/simulink/slref/simulink.valuetype.html) 对象的名称。例如，指定 **ValueType: windVelocity**。
- 自定义数据类型 - 使用指定类型的 MATLAB 表达式。例如，您可以指定一个 [`Simulink.NumericType`](https://ww2.mathworks.cn/help/simulink/slref/simulink.numerictype.html) 对象，其 `DataTypeMode` 属性设置为 `'Fixed-point: unspecified scaling'` 以外的值。



当您指定 `Simulink.ValueType` 或 `Simulink.Bus` 对象作为数据类型时，会忽略 Outport 模块的一些参数。例如，忽略 Outport 模块的 **Min**、**Max** 和 **Unit** 参数。软件改用 `Simulink.ValueType` 对象或 `Simulink.Bus` 对象中 `Simulink.BusElement` 对象的对应属性。例如，假设一个模块将**单位**设置为 `ft/s`。当该模块的**数据类型**指定以 `m/s` 为单位的 `ValueType` 对象时，该模块会使用 `m/s` 而不是 `ft/s` 作为单位。 -->

<!-- 
#### 编程用法

| **模块参数**：`OutDataTypeStr`                               |
| ------------------------------------------------------------ |
| **类型**：字符向量                                           |
| **值**：`'Inherit: auto'` | `'double'` | `'single'` | `'half'` | `'int8'` | `'uint8'` | `'int16'` | `'uint16'` | `'int32'` | `'uint32'` | `'int64'` | `'uint64'` | `'boolean'` | `'fixdt(1,16)'` | `'fixdt(1,16,0)'` | `'fixdt(1,16,2^0,0)'` | `'string'` | `'Enum: <class name>'` | `'Bus: <object name>'` | `'ValueType: <object name>'` | `'<data type expression>'` | `Simulink.ImageType(480,640,3)` |
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
| **默认值**：`'off'`       |
 -->

<!-- 暂无
### **在父模型中以非虚拟总线输出** — 在父模型中以非虚拟总线输出 `off` (默认) | `on`



指定输出总线在父模型中作为非虚拟总线。如果您希望父模型中出现的总线为非虚拟总线，请选择此参数。输入到该端口的总线可以是虚拟或非虚拟总线，无论**在父模型中以非虚拟总线输出**的设置如何。

如果您希望父模型中出现的总线为虚拟总线，则请清除此参数。

#### 提示

- 在非虚拟总线中，所有信号必须具有相同的采样时间，即使关联总线对象的元素指定继承采样时间也是如此。任何操作如果可能会生成违反此要求的非虚拟总线，都会生成错误。有关详细信息，请参阅[Modify Sample Times for Nonvirtual Buses](https://ww2.mathworks.cn/help/simulink/ug/specify-bus-signal-sample-times.html)。

  要对虚拟总线使用多速率信号，请将根级 Outport 模块的**采样时间**参数设置为继承 (`-1`)。

- 对于模型引用层次结构的顶层模型，代码生成将创建 C 结构体，以表示此模块输出的总线。

- 对于引用的模型，选择此选项将创建 C 结构体。否则，代码生成过程将为总线的每个叶元素创建一个参量。

#### 依存关系

要启用此参数，**数据类型**必须解析为 `Simulink.Bus` 对象。例如，将**数据类型**设置为 `Simulink.Bus` 对象，或设置为将 `Simulink.Bus` 对象指定为其数据类型的 `Simulink.ValueType` 对象。

#### 编程用法

| **模块参数**：` BusOutputAsStruct` |
| ---------------------------------- |
| **类型**：字符向量                 |
| **值**：`'off'` | `'on'`           |
| **默认值**：`'off'`                | -->


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


<!-- 
### **端口维度(-1 表示继承)** — 端口维度 `-1` (默认) | 整数 | [整数, 整数]



指定信号要连接到此 Outport 模块所必须具有的维度。

| `-1`    | 任意维度的信号都可以连接到此端口。                   |
| ------- | ---------------------------------------------------- |
| `N`     | 连接到此端口的信号必须是大小为 `N` 的向量。          |
| `[R C]` | 连接到此端口的信号必须是具有 `R` 行和 `C` 列的矩阵。 | -->

<!-- #### 依存关系

当**数据类型**指定对象时，软件会忽略此参数的值。 -->

<!-- 
#### 编程用法

| **模块参数**：` PortDimensions`        |
| -------------------------------------- |
| **类型**：字符向量                     |
| **值**：`'-1'` \| 整数 \| [整数, 整数] |
| **默认值**：`'-1'`                     | -->


<!-- 暂无
### **可变大小信号** — 允许可变大小信号 **继承** (默认) | **否** | **是**



指定此端口的输出端允许的信号类型。要同时允许可变大小和固定大小的信号，请选择 **inherit**。要仅允许可变大小信号，请选择**是**。要仅允许固定大小的信号，请选择**否**。

当此端口的信号为可变大小的信号时，**端口维度**参数将指定信号的最大维度。

#### 依存关系

当**数据类型**指定 `Simulink.ValueType` 对象时，软件会忽略此参数的值。软件改用 `Simulink.ValueType` 对象指定的维度模式。

#### 编程用法

| **参数：**` VarSizeSig`                |
| -------------------------------------- |
| **类型：**字符向量                     |
| **值：**`'Inherit'` | `'No'` | `'Yes'` |
| **默认值：**`'Inherit'`                | -->

<!-- 暂无

### **信号类型** — 输出信号类型 **自动** (默认) | **实数** | **复**



指定信号输出的数值类型。要选择连接到其输入的信号的数值类型，请选择**自动**。否则，请选择实信号或复信号类型。

#### 依存关系

当**数据类型**指定 `Simulink.ValueType` 或 `Simulink.Bus` 对象时，软件会忽略此参数的值。软件改用 `Simulink.ValueType` 对象或 `Simulink.Bus` 对象中的 `Simulink.BusElement` 对象指定的复/实性。

#### 编程用法

| **模块参数**：`SignalType`                |
| ----------------------------------------- |
| **类型：**字符向量                        |
| **值**：`'auto'` | `'real'` | `'complex'` |
| **默认值：**`'auto'`                      | -->

### 信号属性

<div class="details-box">
<details open>
<summary>数据类型 — 输出数据类型<div>double | float | int8 | int16 | int32 | uint8 | uint16 | uint32 | Boolean | fixed point | enumerated | bus </div></summary>
</details>
<div class="details-content">

指定外部输入的输出数据类型。该类型可以继承、直接指定或表示为数据类型对象。

</div>
</div>

### 执行


<div class="details-box">
<details open>
<summary>采样时间(-1 表示继承) — 指定采样时间的选项<div>-1 (默认) | 标量</div></summary>
</details>
<div class="details-content">

指定采样时间命中点之间的离散间隔，或指定另一个采样时间类型，如连续 (0) 或继承 (-1)。

</div>
</div>


<!-- ## 模块特性 -->
<!-- 部分特性暂无
| **数据类型**     | `Boolean` | `bus` | `double` | `enumerated` | `fixed point` | `half` | `integer` | `single` | `string` |
| ---------------- | ------------------------------------------------------------ |
| **直接馈通**     | `否`                                                         |
| **多维信号**     | `是`                                                         |
| **可变大小信号** | `是`                                                         |
| **过零检测**     | `否`                                                         | -->

<!-- ## 扩展功能 -->


<!-- 暂无
### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 VHDL、Verilog 和 SystemVerilog 代码。



HDL Coder™ 提供影响 HDL 实现和综合逻辑的额外配置选项。

**HDL 架构**

此模块具有一个默认 HDL 架构。

**HDL 模块属性**

| 通用                  |                                                              |
| :-------------------- | ------------------------------------------------------------ |
| **BalanceDelays**     | **BalanceDelays** 设置描述**on**（默认值）检测 DUT 中其他路径上引入的延迟，并在 Outport 模块路径上插入匹配的延迟。**off**在 DUT 子系统的输出端口上禁用延迟平衡，以防止 HDL Coder 插入不必要的匹配延迟。例如，当将手动添加的输出端口视为测试点时，可禁用 DUT 子系统中 Outport 模块上的 **BalanceDelays**。**注意**此属性仅影响 DUT 级别的 Outport 模块。 |
| **BidirectionalPort** | **BidirectionalPort** 设置描述**on**将端口指定为双向。需满足以下要求：端口必须位于采用黑盒实现的 Subsystem 模块中。同时，双向端口与对应的顶层 DUT 子系统端口之间不能有逻辑关系。有关详细信息，请参阅 [Specify Bidirectional Ports](https://ww2.mathworks.cn/help/hdlcoder/ug/specify-bidirectional-ports.html) (HDL Coder)。**off**（默认值）不将端口指定为双向。 |

| 目标设定               |                                                              |
| :--------------------- | ------------------------------------------------------------ |
| **IOInterface**        | DUT 端口的目标平台接口类型，指定为字符向量。对于不是 DUT 端口的 Inport 和 Outport 模块，`IOInterface` 模块属性被忽略。要指定有效的 `IOInterface` 设置，请使用 HDL 工作流顾问：在 HDL 工作流顾问中，在**设置目标** > **设置目标接口**步骤中，请在**目标平台接口表**中的**目标平台接口**列中，使用下拉列表设置目标平台接口类型。保存模型。`IOInterface` 值保存为端口的 HDL 模块属性。例如，要查看 `IOInterface` 值，如果 DUT 端口的完整路径是 `hdlcoder_led_blinking/led_counter/LED`，请输入：`hdlget_param('hdlcoder_led_blinking/led_counter/LED', 'IOInterface')` |
| **IOInterfaceMapping** | DUT 端口的目标平台接口端口映射，指定为字符向量。对于不是 DUT 端口的 Inport 和 Outport 模块，`IOInterfaceMapping` 模块属性被忽略。要指定有效的 `IOInterfaceMapping` 设置，请使用 HDL 工作流顾问：在 HDL 工作流顾问中，在**设置目标** > **设置目标接口**步骤中，请在**目标平台接口表**中的**目标平台接口**列中，使用下拉列表设置目标平台接口类型。在**位范围 / 地址 / FPGA 引脚**列中，如果要更改默认值，请输入目标平台接口映射。保存模型。`IOInterfaceMapping` 值保存为端口的 HDL 模块属性。例如，要查看 `IOInterfaceMapping` 值，如果 DUT 端口的完整路径是 `hdlcoder_led_blinking/led_counter/LED`，请输入：`hdlget_param('hdlcoder_led_blinking/led_counter/LED',...             'IOInterfaceMapping')` |
| **IOInterfaceOptions** | DUT 端口的目标平台接口端口映射选项，指定为字符向量。对于不是 DUT 端口的 Inport 和 Outport 模块，`IOInterfaceOptions` 模块属性被忽略。要指定有效的 `IOInterfaceOptions` 设置，请使用 HDL 工作流顾问：在 HDL 工作流顾问的**设置目标** > **设置目标接口**步骤中，在**目标平台接口表**中的**目标平台接口**列中，将输入或输出端口映射到 AXI4 下级接口。在**接口选项**列中，如果要更改默认初始值，请点击**选项**按钮，并为 **RegisterInitialValue** 输入值。保存模型。`IOInterfaceOptions` 值保存为端口的 HDL 模块属性。例如，要查看 `IOInterfaceOptions` 值，如果 DUT 端口的完整路径是 `hdlcoder_led_blinking/led_counter/LED`，请输入：`hdlget_param('hdlcoder_led_blinking/led_counter/LED',...             'IOInterfaceOptions')` |

**`Simulink.ValueType` 对象支持**

此模块支持 `Simulink.ValueType` 对象的生成代码。有关值类型的详细信息，请参阅[Specify Common Set of Signal Properties as Value Type](https://ww2.mathworks.cn/help/simulink/ug/specify-simulink-value-types.html)。



### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。 -->

## 版本历史记录

- 在 2024b 之前推出

<!-- 暂无
**在 R2006a 之前推出** -->

<!-- 
### R2024a: **初始输出值的源**参数已删除

从 R2024a 开始，对于条件执行子系统，初始输出值继承自子系统的输入信号。软件将**初始输出**参数设置为 `[]`，并将**禁用时的输出**参数设置为**保持**。

### R2023b: 记录无界可变大小信号

在普通和加速模式仿真中，Outport 模块支持记录无界可变大小信号。不支持记录包含无界可变大小信号的非虚拟总线。 -->

### 限制信息
不支持部分
1. 参数-常设-信号名称 — 信号名称
2. 参数-常设-图标显示 — 图标显示
3. 参数-常设-指定未连接源时的输出 — 指定未连接的输出值
4. 参数-常设-常量值 — 模块未连接时的输出值
5. 参数-常设-将向量参数解释为一维向量 — 将向量视为一维
6. 参数-常设-确保输出端口为虚拟端口 — 确保输出端口为虚拟
7. 参数-常设-初始输出值的源 — 初始输出值的源
8. 参数-常设-禁用时的输出 — 禁用时的输出
9. 参数-常设-初始输出 — 条件执行子系统的初始输出
10. 参数-信号属性-最小值 — 最小输出值
11. 参数-信号属性-最大值 — 最大输出值
12. 参数-信号属性-锁定输出数据类型设置以防止被定点工具更改 — 防止定点工具覆盖数据类型
13. 参数-信号属性-在父模型中以非虚拟总线输出 — 在父模型中以非虚拟总线输出
14. 参数-信号属性-单位(例如，m、m/s^2、N*m) — 模块的输入信号的物理单位
15. 参数-信号属性-可变大小信号 — 允许可变大小信号
16. 参数-信号属性-信号类型 — 输出信号类型


## 另请参阅

[Inport](Inport.html)

<!-- ### 主题 -->

<!-- 
- [Simplify Subsystem and Model Interfaces with Bus Element Ports](https://ww2.mathworks.cn/help/simulink/ug/simplify-subsystem-bus-interfaces.html)
- [Ensure Output Port Is Virtual](https://ww2.mathworks.cn/help/simulink/ug/ensure-outport-is-virtual.html)
- [使用数据类型助手指定数据类型](https://ww2.mathworks.cn/help/simulink/ug/specify-data-types-using-data-type-assistant.html) -->