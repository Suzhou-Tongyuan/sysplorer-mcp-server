# SubSystem
---
&nbsp;

对各模块进行分组以创建模型层次结构

- **库：** Sysblock / Subsystems

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SubSystems/subSystem/subSystem.png')" style="width: 200px; ">


## 描述<a id="jump1"></a>

Subsystem 模块包含模型或系统中的一组模块。Subsystem 模块可以表示虚拟子系统或非虚拟子系统。

- 非虚拟子系统 - 子系统中包含的内容作为一个单元进行计算和控制（以原子单位执行）。可以创建条件执行子系统，仅在满足触发条件、函数调用条件、动作条件或使能输入条件的情况下才触发事件并执行。
- 虚拟子系统 - 子系统既不是依条件而执行的子系统，也不是以原子单位执行的子系统。虚拟子系统没有校验和。要确定一个子系统是否为虚拟子系统。

<!-- 
Atomic Subsystem 模块是**视为原子单元**模块参数处于选中状态的 Subsystem 模块，表示这是一个非虚拟子系统。 
-->

<!-- 
Code Reuse Subsystem 模块是选择了**视为原子单元**参数且**函数打包**参数设置为“`可重用函数`”（用于指定子系统的函数代码生成格式）的 Subsystem 模块。 
-->

要创建子系统，请执行以下任一操作：

- 从 Subsystems 模块库中，将一个 Subsystem 模块复制到您的模型中。然后打开 Subsystem 模块并向其中复制模块，以此方式在子系统中添加一些模块。
- 选择构成子系统的所有模块和线条，然后在**多个**选项卡中，单击**创建子系统**。会将这些模块替换为一个 Subsystem 模块以及必要的 Inport 和 Outport 模块，以反映进入和离开子系统的信号。

Subsystem 模块图标上显示的输入端口数对应于子系统中的 Inport 模块数。类似地，模块上显示的输出端口数对应于子系统中的 Outport 模块数。

<!-- 
Subsystem 模块通过子系统 Inport 和 Outport 模块支持[信号标签传播](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/signal-label-propagation.html)。 
-->



::: warning 注意

引用的子系统是存储在使用 Subsystem Reference 模块引用的单独文件中的子系统。要重用该子系统，请添加引用同一子系统文件的多个 Subsystem Reference 模块。引用的子系统在运行时的行为与常规子系统相同。

:::

## 示例
使用子系统封装模块。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SubSystems/Subsystem.mo">Subsystem.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SubSystems/subSystem/subSystem01.png')" style="width: 700px; ">


<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SubSystems/subSystem/subSystem02.png')" style="width: 700px; ">

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SubSystems/subSystem/subSystem03.png')" style="width: 900px; ">

## 端口

### 输入

<div class="details-box">
<details open>
<summary>In — 子系统的信号输入<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

在子系统中放置一个 Inport 模块会向 Subsystem 模块添加一个外部输入端口。端口标签与 Inport 模块的名称相匹配。

使用 Inport 模块可以从局部环境中获取信号。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | Boolean | fixed point | enumerated | bus

</div>
</div>



<!-- 暂无
### reinit — 子系统重新初始化事件的控制信号 标量

重新初始化事件端口提供触发子系统重新初始化事件的函数调用控制信号，这会重置子系统的状态。

对于每个子系统重新初始化事件，子系统必须包含一个对应的 [Reinitialize Function](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/reinitializefunction.html) 模块。 -->

<!-- 有关详细信息，请参阅[使用初始化、重新初始化、重置和终止函数](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/initialize-blocks-with-state.html)。 -->

<!-- 
要指定端口名称，请使用 Reinitialize Function 模块中 Event Listener 模块的**事件名称**参数。

#### 依存关系

要启用这种类型的端口，请选中**显示子系统重新初始化端口**复选框。 -->

### 输出

<div class="details-box">
<details open>
<summary>Out — 子系统的信号输出<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

在子系统中放置一个 Outport 模块会从 Subsystem 模块添加一个输出端口。Subsystem 模块上的端口标签是 Outport 模块的名称。

使用 Outport 模块可以向局部环境发送信号。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | Boolean | fixed point | enumerated | bus

</div>
</div>

## 参数

### 常设

<div class="details-box">
<details open>
<summary>端口标签 — 端口标签的显示选项<div>端口名（默认） | 端口号 | 信号名 | 无</div></summary>
</details>
<div class="details-content">

选择如何在 Subsystem 模块图标上显示端口标签。

- **无**

  不显示端口标签。

- **端口名**

  如果对应的端口图标显示了信号名称，则在 Subsystem 模块上显示信号名称。否则，如果模块名称是默认名称，则显示端口模块名称或端口号。

- **端口号**

  在 Subsystem 模块上显示对应端口模块的名称。

- **信号名**

  如果连接到端口的信号已命名，则会在 Subsystem 模块上显示信号的名称。否则，显示相应端口模块的名称。


</div>
</div>

<!-- 
有关 Subsystem 模块上的端口标签编辑，请参阅[编辑子系统模块上的端口标签](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/creating-subsystems.html#mw_bd5fe001-b8bc-478f-8980-be7e44a89d38)。 
-->

<!-- 
#### 编程用法

| **参数**：`ShowPortLabels`                                   |
| ------------------------------------------------------------ |
| **类型**：字符向量                                           |
| **值**：`'FromPortIcon'` | `'FromPortBlockName'` | `'SignalName'` |
| **默认值**：`'FromPortIcon'`                                 | -->


<!-- 暂无
### 读/写权限 — 子系统内容的访问级别 “ReadWrite” （默认） | “ReadOnly” | “NoReadOrWrite”



控制用户对子系统内容的访问。

- “`ReadWrite`”

  允许打开和修改子系统内容。

- “`ReadOnly`”

  允许打开但不允许修改子系统。如果子系统在模块库中，您可以创建和打开该子系统的链接，创建和修改子系统的本地副本，但不能更改权限或修改原始模块库实例的内容。

- “`NoReadOrWrite`”

  禁止打开或修改子系统。如果子系统在模块库中，您可以在模型中创建该子系统的链接，但不能打开、修改、更改权限或创建子系统的本地副本。



**注意**

如果您尝试查看其**读/写权限**参数设置为 “`NoReadOrWrite`” 的子系统的内容，将不会有响应。例如，当您双击此类子系统时，Simulink 不会打开该子系统，并且不显示任何消息。

#### 编程用法

| **参数**：`Permissions`                                  |
| -------------------------------------------------------- |
| **类型**：字符向量                                       |
| **值**：`'ReadWrite'` | `'ReadOnly'` | `'NoReadOrWrite'` |
| **默认值**：`'ReadWrite'`                                | -->


<!-- 暂无
### 错误回调函数的名称 — 发生错误时要调用的函数的名称 '' （默认） | 函数名称



输入当 Simulink 执行子系统时，如果发生错误，要调用的函数的名称。

Simulink 向函数传递两个参数：子系统的句柄以及指定错误类型的字符向量。如果未指定任何函数，当执行子系统导致错误时，Simulink 将显示常规错误消息。

#### 编程用法

| **参数**：` ErrorFcn`              |
| ---------------------------------- |
| **类型**：字符向量                 |
| **值**：`''` | `'<function name>'` |
| **默认值**：`''`                   | -->


<!-- 暂无
### 允许层次解析 — 工作区变量名称解析 “全部” （默认） | “ExplicitOnly” | “无”



选择是否解析此子系统引用的工作区变量的名称。

有关详细信息，请参阅[符号解析](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/resolving-symbols.html)和[符号解析过程](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/resolving-symbols.html#brjnb77-1_1)。

- “`全部`”

  解析此子系统使用的所有工作区变量的名称，包括用来指定模块参数值和 Simulink 数据对象（例如，[`Simulink.Signal`](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/simulink.signal.html) 对象）的工作区变量的名称。

- “`ExplicitOnly`”

  只解析用来指定模块参数值、数据存储内存（不存在模块）、信号以及标有“must resolve”状态的工作区变量的名称。

- “`无`”

  不解析任何工作区变量名称。

#### 编程用法

| **参数**：`PermitHierarchicalResolution`      |
| --------------------------------------------- |
| **类型**：字符向量                            |
| **值**：`'All'` | `'ExplicitOnly'` | `'None'` |
| **默认值**：`'All'`                           | -->

<div class="details-box">
<details open>
<summary>视为原子单元 — 将子系统作为整个单元执行的选项<div>off （默认） | on</div></summary>
</details>
<div class="details-content">

在确定模块方法的执行顺序时，将子系统视为一个单元。

- **off**

  在确定模块方法的执行顺序时，将子系统子中的所有模块视为与子系统处于模型层次结构中的同一级别。这样将使得子系统内的模块方法的执行与子系统外的模块方法的执行交错在一起。

- **on**

  在确定模块方法的执行顺序时，将子系统视为一个单元。例如，当需要计算子系统的输出时，会先调用子系统中的所有模块的输出方法，然后再调用与 Subsystem 模块同一级别的其他模块的输出方法。

</div>
</div>



<!-- 
#### 编程用法

| **参数**：`TreatAsAtomicUnit` |
| ----------------------------- |
| **类型**：字符向量            |
| **值**：`'off'` | `'on'`      |
| **默认值**：`'off'`           | -->


<!-- 暂无
### 显示子系统重新初始化端口 — 显示重新初始化事件端口的选项 off （默认） | on



选中此参数可显示重新初始化事件端口。清除此参数可删除这些端口。

#### 依存关系

要启用此参数，请选中**视为原子单元**复选框。

#### 编程用法

| **模块参数**：`ShowSubsystemReinitializePorts` |
| ---------------------------------------------- |
| **类型：**字符向量                             |
| **值：**`'off'` | `'on'`                       |
| **默认值：**`'off'`                            | -->


<!-- 暂无
### 尽量减少出现代数环 — 消除人为代数环的选项 off （默认） | on



尝试消除任何包含原子子系统的人为代数环

- ![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/off_check_box.gif) off

  不尝试消除任何包含原子子系统的人为代数环。

- ![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/on_check_box.gif) on

  尝试消除任何包含原子子系统的人为代数环。

#### 依存关系

要启用此参数，请选择**视为原子单元**参数。

#### 编程用法

| **参数**：`MinAlgLoopOccurrences` |
| --------------------------------- |
| **类型**：字符向量                |
| **值**：`'off'` | `'on'`          |
| **默认值**：`'off'`               | -->


<!-- 暂无
### 调度类型 — 调度类型 “采样时间” （默认） | “周期性分区” | “非周期性分区”



指定如何调度子系统。

- “`采样时间`”

  指定此子系统中的所有模块是必须以相同的速率运行，还是能可以不同的速率运行。

- “`周期性分区`”

  将子系统作为周期性分区进行调度。指定分区名称和与分区运行的速率对应的采样时间。

- “`非周期性分区`”

  将子系统作为非周期性分区调度。指定分区名称。

#### 依存关系

要启用此参数，请选择**视为原子单元**参数。

#### 编程用法

| **参数**：`ScheduleAs`                                       |
| ------------------------------------------------------------ |
| **类型**：字符向量                                           |
| **值**：`'SampleTime'` | `'PeriodicParition'` | `'AperiodicPartition'` |
| **默认值**：`'SampleTime'`                                   | -->


<!-- 暂无
### 分区名称 — 分区名称 字符向量



指定子系统的分区的名称。

#### 依存关系

要启用此参数，请选择**视为原子单元**参数，并将**调度类型**设置为“`周期性分区`”或“`非周期性分区`”。

#### 编程用法

| **参数**：`PartitionName` |
| ------------------------- |
| **类型**：字符向量        |
| **值**：`''`              |
| **默认值**：`''`          | -->

<div class="details-box">
<details open>
<summary>采样时间 — 时间间隔<div>-1（默认）| [Ts 0]</div></summary>
</details>
<div class="details-content">

指定此子系统中的所有模块是必须以相同的速率运行，还是能可以不同的速率运行。

- 如果子系统中的模块可以不同的速率运行，则为子系统指定继承采样时间 (-1)。
- 如果所有模块必须以相同的速率运行，则将与此速率对应的采样时间指定为**采样时间**参数的值。

- **-1**

  指定继承的采样时间。如果子系统中的模块可以不同的速率运行，则使用此采样时间。

- **[Ts 0]**

  指定周期性采样时间。

#### 依存关系

要启用此参数，请选择**视为原子单元**参数。

</div>
</div>


<!-- 
#### 编程用法

| **参数**：`SystemSampleTime` |
| ---------------------------- |
| **类型**：字符向量           |
| **值**：`'-1'` | `'[Ts 0]'`  |
| **默认值**：`'-1'`           | -->


<!-- 暂无
### 变体控制项 — 变体控制项（条件）表达式 Variant （默认） | 逻辑表达式



指定变量控制项（条件）表达式，当该表达式的计算结果为 `true` 时执行变体 Simulink Function 模块。

有关详细信息，请参阅 [`Simulink.Variant`](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/simulink.variant-class.html)。

- `Variant`

  逻辑（布尔）表达式的默认名称。

- 逻辑表达式

  逻辑（布尔）表达式或表示逻辑表达式的 `Simulink.Variant` 对象。当表达式的计算结果为 `true` 时将激活函数。如果要为模型生成代码，请将表达式中的变量定义为 `Simulink.Parameter` 对象。

#### 依存关系

通过在 Variant Subsystem 模块内添加一个 Subsystem 模块来启用此参数。

#### 编程用法

| **模块参数：**` VariantControl`                |
| ---------------------------------------------- |
| **类型：**字符向量                             |
| **值：**`'Variant'` | `'<logical expression>'` |
| **默认值：**`'Variant'`                        | -->


<!-- 暂无
### 传播变体条件时视为组合单元 — 传播变体条件时将子系统视为单元的选项 on （默认） | off



当从 Variant Source 模块或者向 Variant Sink 模块传播变体条件时，使 Simulink 将子系统视为一个单元。

- on

  当从 Variant Source 模块或者向 Variant Sink 模块传播变体条件时，Simulink 会将子系统视为一个单元。例如，当 Simulink 计算子系统的变体条件时，它会将该条件传播给子系统中的所有模块。

- off

  在确定模块的变体条件时，Simulink 将子系统子中的所有模块视为与子系统处于模型层次结构中的同一级别。

#### 编程用法

| **参数**：`TreatAsGroupedWhenPropagatingVariantConditions` |
| ---------------------------------------------------------- |
| **类型**：字符向量                                         |
| **值**：`'on'` | `'off'`                                   |
| **默认值**：`'on'`                                         | -->


### 代码生成

<div class="details-box">
<details open>
<summary>函数打包 — 代码格式<div>自动（默认）| 内联 | 不可重用函数 | 可重用函数</div></summary>
</details>
<div class="details-content">

选择要为原子（非虚拟）子系统生成的代码格式。

- **自动**

  将基于模型中存在的子系统的类型和实例数为您选择最佳格式。

- **内联**

  无条件地内联子系统。

- **不可重用函数**

  生成的函数不带参数，因此不支持重用子系统代码。

- **可重用函数**

  可以生成带参数的函数，当模型中包含子系统的多个实例时，将允许重用子系统的代码。

#### 依存关系

要启用此参数，请选择**视为原子单元**参数。

</div>
</div>


<!-- 有关详细信息，请参阅：

- [Generate Code and Executables for Individual Subsystems](https://ww2.mathworks.cn/help/releases/R2022b/rtw/ug/generate-code-and-executables-for-an-individual-subsystem.html) (Simulink Coder)
- [Generate Inlined Subsystem Code](https://ww2.mathworks.cn/help/releases/R2022b/rtw/ug/inline-subsystem-code-ecoder.html) (Simulink Coder)
- [Generate Subsystem Code as Separate Function and Files](https://ww2.mathworks.cn/help/releases/R2022b/rtw/ug/generate-separate-code-and-files-for-subsystems-in-a-model.html) (Simulink Coder)
- [Generate Reusable Code from Library Subsystems Shared Across Models](https://ww2.mathworks.cn/help/releases/R2022b/rtw/ug/generate-reusable-code-from-library-subsystems-shared-across-models.html) (Simulink Coder) -->


<!-- 
#### 提示

- 如果您希望子系统的多个实例表示为一个可重用函数，可以为每个子系统指定“`自动`”或“`可重用函数`”。最好是使用其中一个，因为使用两个将生成两个可重用函数，每个指定一个函数。仅当可以重用时，这些选项的结果才会有区别。选择“`自动`”则不允许控制子系统代码的函数或文件名。

- “`可重用函数`”和“`自动`”选项都尝试确定是否存在子系统的多个实例，以及是否可以重用代码。这两个选项的行为区别体现在不能重用时：

  - “`自动`”生成内联代码，或者在禁止内联的情况下为每个子系统实例生成一个单独的函数。
  - “`可重用函数`”为模型中的每个子系统实例生成一个单独的参数函数。

  

- 如果您在生成的代码处于源代码管理状态下时选择了“`可重用函数`”，请将**文件名选项**设置为“`使用子系统名称`”、“`使用函数名称`”或“`用户指定`”。否则，只要您修改模型，代码文件的名称就会改变，从而无法对文件进行源代码管理。

- 如果您选择除“`自动`”或“`内联`”以外的选项，并且使用模型配置参数**状态**，则代码生成器会生成单独的输出和更新方法。代码生成器不考虑**为代码生成和仿真合并输出和更新方法**设定。

#### 依存关系

- 要启用此参数，请选择**视为原子单元**。 -->


<!-- 
#### 编程用法

| **参数**：`RTWSystemCode`                                    |
| ------------------------------------------------------------ |
| **类型**：字符向量                                           |
| **值**：`'Auto'` | `'Inline'` | `'Nonreusable function'` | `'Reusable function'` |
| **默认值**：`'Auto'`                                         | -->


<!-- 暂无
### 函数名称选项 — 如何命名生成的函数 “自动” （默认） | “使用子系统名称” | “用户指定”


选择 Simulink Coder 如何命名它为子系统生成的函数。

如果您拥有 Embedded Coder 许可证，则可以使用“配置参数”对话框的**代码生成** > **标识符**窗格上的选项来控制函数名称。

- “`自动`”

  使用默认的命名约定 `model_subsystem()` 指定唯一的函数名称，其中 `model` 是模型的名称，`subsystem` 是子系统的名称（或者，在重用代码时，也可以是相同子系统的名称）。如果您为**函数打包**参数选择了“`可重用函数`”，而模型引用层次结构中存在可重用子系统的多个实例，则要为子系统生成可重用代码，必须将**函数名称选项**设置为“`自动`”。

- “`使用子系统名称`”

  使用子系统名称作为函数名称。默认情况下，函数名称使用命名约定 `model_subsystem`。**注意**当子系统在模块库模块中而子系统参数 [函数打包, Function packaging函数打包Function packaging](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/subsystem.html#brp1xt9-91) 设置为“`可重用函数`”时，如果您设置“`使用子系统名称`”选项，代码生成器将使用模块库模块的名称作为子系统函数名和文件名。

- “`用户指定`”

  启用**函数名称**字段。输入任何合法的 C 或 C++ 函数名，此名称必须唯一。

有关详细信息，请参阅[Generate Subsystem Code as Separate Function and Files](https://ww2.mathworks.cn/help/releases/R2022b/rtw/ug/generate-separate-code-and-files-for-subsystems-in-a-model.html) (Simulink Coder)。

#### 依存关系



- 此参数要求具有 Simulink Coder 许可证。
- 要启用此参数，请将**函数打包**设置为“`不可重用函数`”或“`可重用函数`”。



#### 编程用法

| **参数**：`RTWFcnNameOpts`                                   |
| ------------------------------------------------------------ |
| **类型**：字符向量                                           |
| **值**：`'Auto'` | `'Use subsystem name'` | `'User specified'` |
| **默认值**：`'Auto'`                                         | -->

<div class="details-box">
<details open>
<summary>函数名称 — 子系统代码的函数名称<div>''（默认）| 函数名称</div></summary>
</details>
<div class="details-content">

为子系统代码指定唯一的有效 C 或 C++ 函数名称。

如果您想为函数指定特定的名称，而不是让代码生成器分配其自己自动生成的名称或者使用子系统名称，请使用此参数。

#### 依存关系

要启用此参数，需要打包类型为**可重用函数**和**不可重用函数**。

</div>
</div>

<div class="details-box">
<details open>
<summary>文件名(无扩展名) — 所生成文件的名称<div>''（默认）| 文件名</div></summary>
</details>
<div class="details-content">

为子系统代码指定生成的文件名称（无扩展名）。

如果您想将子系统函数打包到单独的文件中，请使用此参数。

#### 依存关系

要启用此参数，需要打包类型为**可重用函数**和**不可重用函数**。

</div>
</div>


<!-- 
#### 依存关系



- 此参数要求具有 Simulink Coder 许可证。
- 要启用此参数，请将**函数名称选项**参数设置为“`用户指定`”。



#### 编程用法

| **参数**：`RTWFcnName`             |
| ---------------------------------- |
| **类型**：字符向量                 |
| **值**：`''` | `'<function name>'` |
| **默认值**：`''`                   | -->


<!-- 暂无
### 文件名选项 — 如何命名生成的文件 “自动” （默认） | “使用子系统名称” | “使用函数名称” | “用户指定”



选择 Simulink Coder 如何命名它为子系统生成的函数的单独文件。

- “`自动`”

  根据子系统的配置以及子系统在模型中的实例数，“`自动`”将生成不同的结果：如果代码生成器*不*为子系统生成单独的文件，将在从子系统的父级系统生成的代码模块内生成子系统代码。如果子系统的父级就是模型本身，将在 `model.c` 或 `model.cpp` 内生成子系统代码。如果您为**函数打包**参数选择了“`可重用函数`”，而您生成的代码处于源代码管理状态下，请不要将**文件名选项**值指定为“`自动`”。这样可以防止由于不相关的模型修改而更改生成的文件名，而在使用源代码管理来管理配置时，文件名的改变会产生问题。如果您为**函数打包**参数选择了“`可重用函数`”，而模块引用层次结构中存在可重用子系统的多个实例，则要为子系统生成可重用代码，必须将**文件名选项**设置为“`自动`”。

- “`使用子系统名称`”

  代码生成器将生成一个单独的文件，并使用子系统（或模块库模块）名称作为文件名。**注意**当**文件名选项**设置为“`使用子系统名称`”时，如果模型中包含 Model 模块，或者正在为模型生成模型引用目标，则子系统文件名将被破坏。在这些情况下，子系统的文件名由子系统名称加上模型名称前缀构成。

- “`使用函数名称`”

  代码生成器使用**函数名称选项**指定的函数名称作为文件名。

- “`用户指定`”

  此选项将启用**文件名(无扩展名)** 文本输入字段。代码生成器将使用您输入的名称作为文件名。可以输入任何文件名，但不要带 `.c` 或 `.cpp`（或任何其他）扩展名。此文件名不必唯一。**注意**虽然子系统的源代码文件名不必唯一，但您必须避免指定可能会导致循环依存关系的不唯一名称（例如 `sys_a.h` 包含 `sys_b.h`，`sys_b.h` 包含 `sys_c.h`，而 `sys_c.h` 包含 `sys_a.h`）。

#### 依存关系



- 此参数要求具有 Simulink Coder 许可证。
- 要启用此参数，请将**函数打包**设置为“`不可重用函数`”或“`可重用函数`”。



#### 编程用法

| **参数**：`RTWFileNameOpts`                                  |
| ------------------------------------------------------------ |
| **类型**：字符向量                                           |
| **值**：`'Auto'` | `'Use subsystem name'` | `'Use function name'` | `'User specified'` |
| **默认值**：`'Auto'`                                         | -->


<!-- 暂无
### 文件名(无扩展名) — 所生成文件的名称 '' （默认） | 文件名



您指定的文件名不必是唯一的。但是，应避免指定可能会导致循环依存关系的不唯一名称（例如，`sys_a.h` 包含 `sys_b.h`，`sys_b.h` 包含 `sys_c.h`，而 `sys_c.h` 包含 `sys_a.h`）。

有关详细信息，请参阅[Generate Subsystem Code as Separate Function and Files](https://ww2.mathworks.cn/help/releases/R2022b/rtw/ug/generate-separate-code-and-files-for-subsystems-in-a-model.html) (Simulink Coder)。

#### 依存关系



- 此参数要求具有 Simulink Coder 许可证。
- 要启用此参数，请将**文件名选项**设置为“`用户指定`”。



#### 编程用法

| **参数**：`RTWFileName`        |
| ------------------------------ |
| **类型**：字符向量             |
| **值**：`''` | `'<file name>'` |
| **默认值**：`''`               | -->


<!-- 暂无
### 函数接口 — 选择生成带参数还是不带参数的函数 “`void_void`” （默认） | “`允许参数(优化)`” | “`允许参数(匹配图形接口)`”



选择是生成带参数还是不带参数的函数。

- “`void_void`”

  生成不带参数的函数，并将数据作为全局变量进行传递。例如：`void subsystem_function(void)`

- “`允许参数(优化)`”

  生成带参数的函数，而不是将数据作为全局变量进行传递。此规范可以减少全局 RAM。它可以减小代码大小、提高执行速度，并支持代码生成器应用更多的优化。例如：`void subsystem_function(real_T rtu_In1, real_T rtu_In2,                         real_T *rty_Out1)`在某些情况下，当生成优化代码时，代码生成器可能不会生成具有参数的函数。

- “`允许参数(匹配图形接口)`”

  生成一个函数接口，该接口使用与子系统图形模块接口相匹配的参数。生成的函数接口是可预知的，并且不会更改。可预知的接口对于调试和测试代码以及与外部应用程序集成非常有用。例如，如果一个模型有两个输入端口和两个输出端口，则生成的函数接口是：`void subsystem_function(real_T rtu_In1, real_T rtu_In2,                         real_T *rty_Out1, real_T *rty_Out2)`

有关详细信息，请参阅：

- [Reduce Global Variables in Nonreusable Subsystem Functions](https://ww2.mathworks.cn/help/releases/R2022b/ecoder/ug/specify-function-arguments-to-reduce-memory-usage.html) (Embedded Coder)
- [Generate Predictable Function Interface to Match Graphical Block Interface](https://ww2.mathworks.cn/help/releases/R2022b/ecoder/ug/generate-predictable-interface.html) (Embedded Coder)
- [为非虚拟子系统生成模块化函数代码](https://ww2.mathworks.cn/help/releases/R2022b/ecoder/ug/atomic-subsystem-code.html) (Embedded Coder)



#### 依存关系



- 此参数需要 Embedded Coder 和一个基于 ERT 的系统目标文件。
- 要启用此参数，请将**函数打包**设置为“`不可重用函数`”。



#### 编程用法

| **参数**：`FunctionInterfaceSpec`                            |
| ------------------------------------------------------------ |
| **类型**：字符向量                                           |
| **值**：`'void_void'` | `'Allow arguments (Optimized)'` | `'Allow arguments (Match graphical interface)'` |
| **默认值**：`'void_void'`                                    | -->


<!-- 暂无
### 具有独立数据的函数 — 控制子系统的代码生成 off （默认） | on



生成其中原子子系统的内部数据与其父级模型分离且归子系统所有的子系统函数代码。

- ![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/off_check_box.gif) off

  不生成其中原子子系统的内部数据与其父级模型分离且归子系统所有的子系统函数代码。

- ![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/on_check_box.gif) on

  生成其中原子子系统的内部数据与其父级模型分离且归子系统所有的子系统函数代码。子系统数据结构的声明独立于父模型数据结构。带单独数据的子系统具有其自己的模块 I/O 和 `DWork` 数据结构。因此，为子系统生成的代码更容易跟踪和检验。数据分离还可以减小整个模型的全局数据结构的最大大小，因为它们被拆分成多个数据结构。

有关如何为原子子系统生成模块化函数代码的详细信息，请参阅[为非虚拟子系统生成模块化函数代码](https://ww2.mathworks.cn/help/releases/R2022b/ecoder/ug/atomic-subsystem-code.html) (Embedded Coder)。

有关如何对原子子系统应用内存段的详细信息，请参阅[Override Default Memory Placement for Subsystem Functions and Data](https://ww2.mathworks.cn/help/releases/R2022b/ecoder/ug/control-data-and-function-placement-in-memory-by-inserting-pragmas.html#bqnrt1v-9) (Embedded Coder)。

#### 依存关系



- 此参数需要具有 Embedded Coder 许可证和基于 ERT 的系统目标文件。
- 要启用此参数，请将**函数打包**设置为“`不可重用函数`”。



#### 编程用法

| **参数**：`FunctionWithSeparateData` |
| ------------------------------------ |
| **类型**：字符向量                   |
| **值**：`'off'` | `'on'`             |
| **默认值**：`'off'`                  | -->


<!-- 暂无
### 用于初始化/终止函数的内存段 — 选择如何应用内存段 “从模型继承” （默认） | “默认” | “感兴趣的内存段”



选择 Embedded Coder 如何将内存段应用于子系统初始化和终止函数。

- “`从模型继承`”

  将根模型内存段应用于子系统函数代码

- “`默认`”

  不将内存段应用于子系统的系统代码，覆盖任何模型级的设置

- “`感兴趣的内存段`”

  将模型的某个内存段应用于子系统

#### 提示

- 可能的值根据您为模型配置设置的内存段数据包（如果有）而不同。请参阅[Control Data and Function Placement in Memory by Inserting Pragmas](https://ww2.mathworks.cn/help/releases/R2022b/ecoder/ug/control-data-and-function-placement-in-memory-by-inserting-pragmas.html) (Embedded Coder)和[模型配置参数：代码生成](https://ww2.mathworks.cn/help/releases/R2022b/rtw/ref/code-generation-pane-general.html) (Simulink Coder)。
- 如果您没有为模块配置数据包，将只显示“`从模型继承`”。否则，列表中将包括“`默认`”以及模型包中的所有内存段。
- 这些选项对于为给定子系统覆盖模型内存段设置很有用。有关如何对原子子系统应用内存段的详细信息，请参阅[Override Default Memory Placement for Subsystem Functions and Data](https://ww2.mathworks.cn/help/releases/R2022b/ecoder/ug/control-data-and-function-placement-in-memory-by-inserting-pragmas.html#bqnrt1v-9) (Embedded Coder)。

#### 依存关系



- 此参数需要具有 Embedded Coder 软件的许可证和一个基于 ERT 的系统目标文件。
- 要启用此参数，请将**函数打包**设置为“`不可重用函数`”或“`可重用函数`”。



#### 编程用法

| **参数**：`RTWMemSecFuncInitTerm`                            |
| ------------------------------------------------------------ |
| **类型**：字符向量                                           |
| **值**：`'Inherit from model'` | `'Default'` | `'The memory section of interest'` |
| **默认值**：`'Inherit from model'`                           | -->


<!-- 暂无
### 用于执行函数的内存段 — 选择如何应用内存段 “从模型继承” （默认） | “默认” | “感兴趣的内存段”



选择 Embedded Coder 如何将内存段应用于子系统执行函数。

- “`从模型继承`”

  将根模型内存段应用于子系统函数代码

- “`默认`”

  不将内存段应用于子系统的系统代码，覆盖任何模型级的设置

- “`感兴趣的内存段`”

  将模型的某个内存段应用于子系统

#### 提示

- 可能的值根据您为模型配置设置的内存段数据包（如果有）而不同。请参阅[Control Data and Function Placement in Memory by Inserting Pragmas](https://ww2.mathworks.cn/help/releases/R2022b/ecoder/ug/control-data-and-function-placement-in-memory-by-inserting-pragmas.html) (Embedded Coder)和[模型配置参数：代码生成](https://ww2.mathworks.cn/help/releases/R2022b/rtw/ref/code-generation-pane-general.html) (Simulink Coder)。
- 如果您没有为模块配置数据包，将只显示“`从模型继承`”。否则，列表中将包括“`默认`”以及模型包中的所有内存段。
- 这些选项对于为给定子系统覆盖模型内存段设置很有用。有关如何对原子子系统应用内存段的详细信息，请参阅[Override Default Memory Placement for Subsystem Functions and Data](https://ww2.mathworks.cn/help/releases/R2022b/ecoder/ug/control-data-and-function-placement-in-memory-by-inserting-pragmas.html#bqnrt1v-9) (Embedded Coder)。

#### 依存关系



- 此参数需要具有 Embedded Coder 软件的许可证和一个基于 ERT 的系统目标文件。
- 要启用此参数，请将**函数打包**设置为“`不可重用函数`”或“`可重用函数`”。



#### 编程用法

| **参数**：`RTWMemSecFuncExecute`                             |
| ------------------------------------------------------------ |
| **类型**：字符向量                                           |
| **值**：`'Inherit from model'` | `'Default'` | `'The memory section of interest'` |
| **默认值**：`'Inherit from model'`                           | -->


<!-- 暂无
### 用于常量的内存段 — 选择如何应用内存段 “从模型继承” （默认） | “默认” | “感兴趣的内存段”



选择 Embedded Coder 如何将内存段应用于子系统常量。

- “`从模型继承`”

  将根模型内存段应用于子系统数据

- “`默认`”

  不将内存段应用于子系统数据，将覆盖任何模型级的设置

- “`感兴趣的内存段`”

  将模型的某个内存段应用于子系统

#### 提示

- 您指定的内存段将应用于生成的代码中对应的全局数据结构。有关为原子子系统生成的全局数据结构的基本信息，请参阅[Standard Data Structures](https://ww2.mathworks.cn/help/releases/R2022b/rtw/ug/data-structures-in-the-generated-code.html#mw_0f14c140-dde6-4239-9a0a-6a9c0d68f447) (Simulink Coder)。
- 可能的值根据您为模型配置设置的内存段数据包（如果有）而不同。请参阅[Control Data and Function Placement in Memory by Inserting Pragmas](https://ww2.mathworks.cn/help/releases/R2022b/ecoder/ug/control-data-and-function-placement-in-memory-by-inserting-pragmas.html) (Embedded Coder)。
- 如果您没有为模块配置数据包，将只显示“`从模型继承`”。否则，列表中将包括“`默认`”以及模型包中的所有内存段。
- 这些选项对于为给定子系统覆盖模型内存段设置很有用。有关如何对原子子系统应用内存段的详细信息，请参阅[Override Default Memory Placement for Subsystem Functions and Data](https://ww2.mathworks.cn/help/releases/R2022b/ecoder/ug/control-data-and-function-placement-in-memory-by-inserting-pragmas.html#bqnrt1v-9) (Embedded Coder)。

#### 依存关系



- 此参数需要具有 Embedded Coder 许可证和基于 ERT 的系统目标文件。
- 要启用此参数，请将**函数打包**设置为“`不可重用函数`”，然后选择**具有独立数据的函数**参数。



#### 编程用法

| **参数**：`RTWMemSecDataConstants`                           |
| ------------------------------------------------------------ |
| **类型**：字符向量                                           |
| **值**：`'Inherit from model'` | `'Default'` | `'The memory section of interest'` |
| **默认值**：`'Inherit from model'`                           | -->


<!-- 暂无
### 用于内部数据的内存段 — 选择如何应用内存段 “从模型继承” （默认） | “默认” | “感兴趣的内存段”



选择 Embedded Coder 如何将内存段应用于子系统内部数据。

- “`从模型继承`”

  将根模型内存段应用于子系统数据

- “`默认`”

  不将内存段应用于子系统数据，将覆盖任何模型级的设置

- “`感兴趣的内存段`”

  将模型的某个内存段应用于子系统

#### 提示

- 您指定的内存段将应用于生成的代码中对应的全局数据结构。有关为原子子系统生成的全局数据结构的基本信息，请参阅[Standard Data Structures](https://ww2.mathworks.cn/help/releases/R2022b/rtw/ug/data-structures-in-the-generated-code.html#mw_0f14c140-dde6-4239-9a0a-6a9c0d68f447) (Simulink Coder)。
- 可能的值根据您为模型配置设置的内存段数据包（如果有）而不同。请参阅[Control Data and Function Placement in Memory by Inserting Pragmas](https://ww2.mathworks.cn/help/releases/R2022b/ecoder/ug/control-data-and-function-placement-in-memory-by-inserting-pragmas.html) (Embedded Coder)。
- 如果您没有为模块配置数据包，将只显示“`从模型继承`”。否则，列表中将包括“`默认`”以及模型包中的所有内存段。
- 这些选项对于为给定子系统覆盖模型内存段设置很有用。有关如何对原子子系统应用内存段的详细信息，请参阅[Override Default Memory Placement for Subsystem Functions and Data](https://ww2.mathworks.cn/help/releases/R2022b/ecoder/ug/control-data-and-function-placement-in-memory-by-inserting-pragmas.html#bqnrt1v-9) (Embedded Coder)。

#### 依存关系



- 此参数需要具有 Embedded Coder 许可证和基于 ERT 的系统目标文件。
- 要启用此参数，请将**函数打包**设置为“`不可重用函数`”，然后选择**具有独立数据的函数**参数。



#### 编程用法

| **参数**：`RTWMemSecDataInternal`                            |
| ------------------------------------------------------------ |
| **类型**：字符向量                                           |
| **值**：`'Inherit from model'` | `'Default'` | `'The memory section of interest'` |
| **默认值**：`'Inherit from model'`                           | -->


<!-- 暂无
### 用于参数的内存段 — 选择如何应用内存段 “从模型继承” （默认） | “默认” | “感兴趣的内存段”



选择 Embedded Coder 如何将内存段应用于子系统参数。

- “`从模型继承`”

  将根模型内存段应用于子系统函数代码

- “`默认`”

  不将内存段应用于子系统的系统代码，覆盖任何模型级的设置

- 感兴趣的内存段

  将模型的某个内存段应用于子系统

#### 提示

- 您指定的内存段将应用于生成的代码中对应的全局数据结构。有关为原子子系统生成的全局数据结构的基本信息，请参阅[Standard Data Structures](https://ww2.mathworks.cn/help/releases/R2022b/rtw/ug/data-structures-in-the-generated-code.html#mw_0f14c140-dde6-4239-9a0a-6a9c0d68f447) (Simulink Coder)。
- 可能的值根据您为模型配置设置的内存段数据包（如果有）而不同。请参阅[Control Data and Function Placement in Memory by Inserting Pragmas](https://ww2.mathworks.cn/help/releases/R2022b/ecoder/ug/control-data-and-function-placement-in-memory-by-inserting-pragmas.html) (Embedded Coder)。
- 如果您没有为模块配置数据包，将只显示“`从模型继承`”。否则，列表中将包括“`默认`”以及模型包中的所有内存段。
- 这些选项对于为给定子系统覆盖模型内存段设置很有用。有关如何对原子子系统应用内存段的详细信息，请参阅[Override Default Memory Placement for Subsystem Functions and Data](https://ww2.mathworks.cn/help/releases/R2022b/ecoder/ug/control-data-and-function-placement-in-memory-by-inserting-pragmas.html#bqnrt1v-9) (Embedded Coder)。

#### 依存关系



- 此参数需要具有 Embedded Coder 许可证和基于 ERT 的系统目标文件。
- 要启用此参数，请将**函数打包**设置为“`不可重用函数`”，然后选择**具有独立数据的函数**参数。



#### 编程用法

| **参数**：`RTWMemSecDataParameters`                          |
| ------------------------------------------------------------ |
| **类型**：字符向量                                           |
| **值**：`'Inherit from model'` | `'Default'` | `'The memory section of interest'` |
| **默认值**：`'Inherit from model'`                           | -->

<!-- ### 子系统引用 -->


<!-- 暂无
### 子系统文件名 — 引用子系统的文件名 字符串标量 | 字符向量



指定要引用的子系统文件。有关子系统引用的信息，请参阅[Subsystem Reference](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/referenced-subsystem-1.html)。

#### 依存关系

要访问此参数，请在**子系统引用**部分中，单击**转换**。

有关如何将子系统转换为引用子系统的详细信息，请参阅[Convert an Existing Subsystem to a Referenced Subsystem](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/referenced-subsystem-1.html#mw_a2c92a5b-3946-4b09-ac09-3024ef1c08ae)。

#### 编程用法

| **参数**：`ReferencedSubsystem` |
| ------------------------------- |
| **类型**：字符向量              |
| **值**：`''` | `'<filename>'`   |
| **默认值**：`''`                | -->


<!-- ## 模块特性 -->
<!-- 
| **数据类型**                                                 | `Booleana` | `busa` | `doublea` | `enumerateda` | `fixed pointa` | `halfa` | `integera` | `singlea` | `stringa` |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| **直接馈通**                                                 | `否`                                                         |
| **多维信号**                                                 | `是a`                                                        |
| **可变大小信号**                                             | `是a`                                                        |
| **过零检测**                                                 | `否`                                                         |
| [a](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/subsystem.html?s_tid=doc_ta#d125e194043) 实际支持的数据类型或功能取决于模块实施。 |                                                              | -->

<!-- ## 扩展功能 -->


<!-- 
### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。

实际代码生成支持取决于模块实现。



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 Verilog 代码和 VHDL 代码。



HDL Coder™ 提供影响 HDL 实现和综合逻辑的额外配置选项。

**HDL 架构**

| 架构               | 描述                                                         |
| :----------------- | :----------------------------------------------------------- |
| “`模块`”（默认值） | 为子系统和子系统内的模块生成代码。                           |
| “`BlackBox`”       | 生成黑盒接口。生成的 HDL 代码仅包括子系统的输入/输出端口定义。因此，您可以在模型中使用子系统来生成与手动编写的现有 HDL 代码的接口。子系统的黑盒接口生成类似于没有时钟信号的 Model 模块接口生成。 |
| “`无 HDL`”         | 从生成的代码中删除子系统。您可以在仿真中使用子系统，但在 HDL 代码中将其视为“无操作”。 |

**黑盒接口自定义**

对于 “`BlackBox`” 架构，您可以自定义端口名称并设置外部组件接口的属性。请参阅[Customize Black Box or HDL Cosimulation Interface](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/customizing-the-generated-interface.html) (HDL Coder)。

**HDL 模块属性**

| 通用                          |                                                              |
| :---------------------------- | ------------------------------------------------------------ |
| **AdaptivePipelining**        | 基于综合工具、目标频率和乘法器字长的自动流水线插入。默认值为 “`inherit`”。另请参阅[AdaptivePipelining](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bve2wds-1) (HDL Coder)。 |
| **BalanceDelays**             | 检测沿一条路径引入的新延迟，并在其他路径上插入匹配的延迟。默认值为 “`inherit`”。另请参阅[BalanceDelays](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#btudq9e) (HDL Coder)。 |
| **ClockRatePipelining**       | 以较快的时钟频率而不是较慢的数据速率插入流水线寄存器。默认值为 “`inherit`”。另请参阅[ClockRatePipelining](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bveex_4-1) (HDL Coder)。 |
| **ConstrainedOutputPipeline** | 通过移动设计中现有延迟的方式来放置在输出端的寄存器的数量。分布式流水线处理不会重新分发这些寄存器。默认值为 `0`。有关详细信息，请参阅[ConstrainedOutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#btp8gmp) (HDL Coder)。 |
| **DistributedPipelining**     | 流水线寄存器分配或寄存器重定时。默认值为 “`inherit`”。另请参阅[DistributedPipelining](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-20) (HDL Coder)。 |
| **DSPStyle**                  | 乘法器映射的综合属性。默认值为“`无`”。另请参阅[DSPStyle](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bubc5wb-1) (HDL Coder)。 |
| **FlattenHierarchy**          | 从生成的 HDL 代码中删除子系统层次结构。默认值为 “`inherit`”。另请参阅[FlattenHierarchy](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#btdc8oq-1) (HDL Coder)。 |
| **InputPipeline**             | 要在生成的代码中插入的输入流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 `0`。有关详细信息，请参阅[InputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-25) (HDL Coder)。 |
| **OutputPipeline**            | 要在生成的代码中插入的输出流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 `0`。有关详细信息，请参阅[OutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-26) (HDL Coder)。 |
| **SharingFactor**             | 要映射到单个共享资源的功能等效的资源的数量。默认值为 0。另请参阅[Resource Sharing](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/resource-sharing.html) (HDL Coder)。 |
| **StreamingFactor**           | 并行数据路径或向量的数量，这些路径或向量通过时间多路复用的方式变换为串行标量数据路径。默认值为 0，表示实现完全并行的数据路径。另请参阅[Streaming](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/streaming.html) (HDL Coder)。 |

如果此模块不是 DUT，将忽略**目标设定**选项卡中的模块属性设置。在 HDL 工作流顾问中，如果您使用 **IP 核生成**工作流，这些目标设定模块属性值将随模型一起保存。如果您使用 `hdlset_param` 指定这些目标设定模块属性值，则当您打开 HDL 工作流顾问时，系统将使用对应的值填充这些字段。

| 目标设定                                 |                                                              |
| :--------------------------------------- | ------------------------------------------------------------ |
| **AdditionalTargetInterfaces**           | 附加目标接口，指定为字符向量。要在模型上保存此模块属性，请在 **IP 核生成**工作流的**设置目标接口**任务中，对应于您要添加更多接口的 DUT 端口，选择 **Add more...**。然后，您可以在“添加新目标接口”对话框中添加更多接口。指定接口类型、附加接口数量以及每个附加接口的唯一名称。值：`''`（默认值）| 字符向量元胞数组示例：`'{{'AXI4-Stream','InterfaceID','AXI4-Stream1'}}'` |
| **ProcessorFPGASynchronization**         | 处理器/FPGA 同步模式，指定为字符向量。要在模型上保存此模块属性，请在 **IP 核生成**工作流的**设置目标接口**任务中指定**处理器/FPGA 同步**。值：`Free running`（默认值）| `Coprocessing - blocking`示例：`'Free running'` |
| **TestPointMapping**                     | 要在模型上保存此模块属性，请在 **IP 核生成**工作流的**设置目标接口**任务中指定测试点端口到目标平台接口的映射。值：`''`（默认值）| 字符向量元胞数组示例：`'{{'TestPoint','AXI4-Lite','x"108"'}}'` |
| **TunableParameterMapping**              | 要在模型上保存此模块属性，请在 **IP 核生成**工作流的**设置目标接口**任务中指定可调参数端口到目标平台接口的映射。值：`''`（默认值）| 字符向量元胞数组示例：`'{{'myParam','AXI4-Lite','x"108"'}}'` |
| **AXI4RegisterReadback**                 | 要在模型上保存此模块属性，请在 **IP 核生成**工作流的**生成 RTL 代码和 IP 核**任务中指定是否对 AXI4 从属站写寄存器启用读回。要了解详细信息，请参阅[Model Design for AXI4 Slave Interface Generation](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/model-design-for-axi4-slave-interface-generation.html) (HDL Coder)。值：`'off'`（默认值）| `'on'` |
| **AXI4SlaveIDWidth**                     | 要在模型上保存此模块属性，请使用 **IP 核生成**工作流的**生成 RTL 代码和 IP 核**任务中的 **AXI4 从属 ID 宽度**设置，指定要将 DUT IP 核连接到的 AXI 管理器接口的数量。要了解详细信息，请参阅[Define Multiple AXI Master Interfaces in Reference Designs to access DUT AXI4 Slave Interface](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/define-multiple-axi-master-interfaces-in-reference-designs-to-access-dut-axi4-slave-interface-1.html) (HDL Coder)。值：`'off'`（默认值）| `'on'` |
| **AXI4SlavePortToPipelineRegisterRatio** | 要在模型上保存此模块属性，请使用 **IP 核生成**工作流的**生成 RTL 代码和 IP 核**任务中的 **AXI4 从属站端口与流水线寄存器的比率**设置，指定要为其插入流水线寄存器的 AXI4 从属端口的数量。要了解详细信息，请参阅[Model Design for AXI4 Slave Interface Generation](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/model-design-for-axi4-slave-interface-generation.html) (HDL Coder)。值：`'off'`（默认值）| `'on'` |
| **GenerateDefaultAXI4Slave**             | 要在模型上保存此模块属性，请在 **IP 核生成**工作流的**生成 RTL 代码和 IP 核**任务中指定是否要禁用默认 AXI4 从属站接口的生成。值：`'on'`（默认值）| `'off'` |
| **IPCoreAdditionalFiles**                | 设计中黑盒的 Verilog® 或 VHDL® 文件。指定每个文件的完整路径，并用分号 (;) 分隔各文件名。您可以在 HDL 工作流顾问的**其他源文件**字段中设置此属性。值：`''`（默认值）| 字符向量示例：`'C:\myprojfiles\led_blinking_file1.vhd;C:\myprojfiles\led_blinking_file2.vhd;'` |
| **IPCoreName**                           | IP 核名称，指定为字符向量。您可以在 HDL 工作流顾问的 **IP 核名称**字段中设置此属性。如果将此属性设置为默认值，HDL 工作流顾问将基于 DUT 的名称构造 IP 核名称。值：`''`（默认值）| 字符向量示例：`'my_model_name'` |
| **IPCoreVersion**                        | IP 核版本号，指定为字符向量。您可以在 HDL 工作流顾问的 **IP 核版本**字段中设置此属性。如果此属性设置为默认值，则 HDL 工作流顾问将设置 IP 核版本。值：`''`（默认值）| 字符向量示例：`'1.3'` |
| **IPDataCaptureBufferSize**              | FPGA 数据采集缓冲区大小，指定为字符向量。当在 FPGA 上运行时，请使用 FPGA 数据采集来观察设计中的信号。缓冲区大小的值为 128*2^n，其中 n 是整数。默认情况下，缓冲区大小为 128 (n=0)。n 的最大值是 13，即缓冲区大小的最大值是 1048576 (=128*2^13)。值：`''`（默认值）| 字符向量示例：`'1.3'` |

**限制**

如果您的 DUT 是封装子系统，则仅当它位于模型的顶层时，您才能生成代码。

有关详细信息，请参阅：

- [External Component Interfaces](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/external-component-interfaces.html) (HDL Coder)
- [Generate Black Box Interface for Subsystem](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/black-box-implementation-for-subsystem-blocks.html) (HDL Coder)





### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。

子系统必须为原子子系统才能支持 PLC 代码生成。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。

实际数据类型支持取决于模块实现。 -->

## 版本历史记录

- 在 2024b 之前推出
- 在 2026a 推出文件名功能

### 限制信息
不支持部分
1. 端口-输入-reinit — 子系统重新初始化事件的控制信号
2. 参数-常设-读取/写入权限 — 子系统内容的访问级别
3. 参数-常设-错误回调函数的名称 — 发生错误时要调用的函数的名称
4. 参数-常设-允许层次解析 — 工作区变量名称解析
5. 参数-常设-显示子系统重新初始化端口 — 显示重新初始化事件端口的选项
6. 参数-常设-尽量减少出现代数环 — 消除人为代数环的选项
7. 参数-常设-调度类型 — 调度类型
8. 参数-常设-分区名称 — 分区名称
9. 参数-常设-变体控制项 — 变体控制项
10. 参数-常设-传播变体条件时视为组合单元 — 传播变体条件时将子系统视为单元的选项
11. 参数-代码生成-函数接口 — 选择生成带参数还是不带参数的函数
12. 参数-代码生成-函数名称选项 — 如何命名生成的函数
13. 参数-代码生成-文件名选项 — 如何命名生成的文件
14. 参数-代码生成-函数接口 — 如何将参量与生成的函数结合使用
15. 参数-代码生成-具有独立数据的函数 — 控制子系统的代码生成
16. 参数-代码生成-用于初始化/终止函数的内存段 — 如何应用内存段
17. 参数-代码生成-用于执行函数的内存段 — 如何应用内存段
18. 参数-代码生成-用于常量的内存段 — 如何应用内存段
19. 参数-代码生成-用于内部数据的内存段 — 如何应用内存段
20. 参数-代码生成-用于参数的内存段 — 如何应用内存段
21. 参数-代码生成-Function-Call Subsystem — 由外部函数调用输入控制执行的子系统
22. 参数-代码生成-For Each terator 子系统 — 当逻辑表达式为 true 时，在仿真时间步中重复执行子系统
23. 参数-代码生成-While ISubsystem — 将算法应用于输入信号或封装参数的单个元素或子数组
24. 参数-代码生成-Message Polling Subsystem — 在定期检查期间其执行由消息输入控制的子系统
25. 参数-代码生成-Message Triggered Subsystem — 由消息输入控制其执行的子系统
26. 参数-代码生成-CodeReuseSubsystem — 将可重用函数指定为代码生成格式的子系统
27. 参数-代码生成-Neighborhood Processing Subsystem — 创建遵循邻域模式的算法



## 另请参阅

[Trigger](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SubSystems/Trigger.html)

<!-- ### 主题 -->

<!-- - [创建子系统](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/creating-subsystems.html)
- [预览模型组件的内容](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/preview-content-of-hierarchical-items.html)
- [使用函数调用子系统](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/using-function-call-subsystems.html)
- [导出函数模型概述](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/export-function-models.html) -->