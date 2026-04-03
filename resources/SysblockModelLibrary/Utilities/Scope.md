# Scope
---
&nbsp;

显示仿真过程中生成的信号

**库：** Sysblock模块库 / Utilities

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/Scope/Scope.png')" style="width: 100px;">

## 描述

双击 Scope 模块后打开 Scope 曲线窗口，并将输入以曲线的形式显示出来。

<!-- Simulink® Scope 模块和 DSP System Toolbox™ Time Scope 模块显示时域信号。

![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/timescope_block_open.png)![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/scope_block_open.png)

这两个模块具有相同的功能，但是默认设置不同。Time Scope 针对离散时间处理进行了优化。Scope 针对一般时域仿真进行了优化。如需并排比较，请参阅 [Simulink Scope 与 DSP System Toolbox Time Scope 的比较](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/simulation-data-display-and-capture-using-scopes.html#buw7l4r-5)。

示波器具有以下功能面板：

- [触发器](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/scope-trigger-panel.html) - 设置触发器，在发生指定事件时同步重复的信号并暂停显示。
- [游标测量](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/cursor-measurements-panel.html) - 使用垂直游标和水平游标测量信号值。
- [信号统计](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/signal-statistics-panel.html) - 显示所选信号的最大值、最小值、峰间差、均值、中位数和 RMS 值。
- [峰值查找器](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/peak-finder-panel.html) - 查找最大值，显示出现最大值时的 x 轴值。
- [双电平测量](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/bilevel-measurements-panel.html) - 测量过渡过程、过冲、下冲和循环。

您必须拥有 Simscape™ 或 DSP System Toolbox 许可证，才能使用峰值查找器、双电平测量和信号统计这些功能面板。

示波器画面支持：

- 仿真控制 - 从“范围”窗口中使用**运行**、**步进**和**步退**工具栏按钮可以调试模型。

- 多个信号 - 可使用多个输入端口在同一个 *y* 轴（视图）上绘制多个信号。

- 多个 y 轴（显示）- 显示多个 *y* 轴。所有 *y* 轴在 *x* 轴上具有共同的时间范围。

- 修改参数 - 在仿真之前和仿真期间修改波形参数值。

- 自动缩放轴范围 - 在仿真期间或仿真结束时自动缩放轴范围。在坐标区的顶部和底部会留有边距。

- 仿真后显示数据 - 仿真期间保存波形数据。如果在仿真开始时波形视图关闭，则当您在仿真后打开波形视图时，波形视图将显示附加的输入信号的仿真结果。

  

  **注意**

  如果采样率高或仿真时间长，可能会遇到内存或系统性能问题，因为示波器在内部保存数据。要限制为波形可视化保存的数据量，请使用 [将数据点限制为最后, Limit data points to last将数据点限制为最后Limit data points to last](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/scope.html#f5-1117037_sep_buuaefi-1) 属性。

  



有关以编程方式控制示波器的信息，请参阅[Control Scope Blocks Programmatically](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/control-scopes-programmatically.html)。 -->

<!-- ## 限制

- 不要在库中使用 Scope 模块。如果您将 Scope 模块放在具有锁定链接的库或者锁定的库中，当尝试打开示波器窗口时，Simulink 会显示错误。要显示某个库模块中的内部数据，请为库模块添加一个输出端口，然后将此端口连接到您模型中的 Scope 模块。
- 如果步进模型，波形仅在示波器模块运行时才会更新。这意味着状态栏中显示的时间可能与模型时间不匹配。
- 示波器模块在连接到常量信号时将绘制单个点。
- 当信号值为 NaN 时，示波器会在显示画面上显示缺口。
- 当您在示波器内可视化多个基于帧的信号时，部分帧大小为 1 的信号采样可能不会显示。要可视化这些信号，请将帧大小为 1 的信号转移到单独的示波器。
- 示波器显示画面在快速加速模式下有限制。请参阅 [示波器和查看器在快速加速模式下的行为](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/designing-your-model-for-effective-acceleration.html#brdcu1i-1)。
- 当示波器位于 ForEach 子系统中时，示波器仅显示最后一个索引。 -->

## 示例

<!-- [![房屋的热模型](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/sldemo_househeatexample_05_zh_CN.png)房屋的热模型此示例说明如何使用 Simulink® 来创建房屋的热模型。此系统对室外环境、房屋的热特性和房屋供暖系统进行建模。](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/thermal-model-of-a-house.html)

[![Simulating Systems with Variable Transport Delay Phenomena](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink_general/win64/sldemo_VariableTransportDelayExample_04.png)Simulating Systems with Variable Transport Delay PhenomenaTwo cases where you can use Simulink® to model variable transport delay phenomena.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/simulating-systems-with-variable-transport-delay-phenomena.html) -->

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/Scope.mo">Scope.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/Scope/Scope_ex.png')" style="width: 300px; ">


### 示例说明

- SineWave 模块：生成一个正弦波信号，其振幅和频率可以在模块参数中设置。在这个示例中，我们使用了一个振幅为 1，频率为 1 Hz 的正弦波；
- Scope 模块：用于显示模型中的信号。当你将信号连接到 Scope 模块并运行仿真时，可以在 Scope 的图形界面中观察到信号随时间的变化。Scope 模块是分析和调试 Syblock 模型中信号的常用工具。


## 端口

### 输入


<div class="details-box">
<details open>
<summary>u1 — 要可视化的信号<div>标量 | 向量 | 矩阵 | 数组</div></summary>
</details>
<div class="details-content">

连接要可视化的信号。您最多可以有 96 个输入端口。输入信号可以具有以下特性：

- **类型** - 连续（基于采样）或离散（基于采样和基于帧）；
<!-- - **数据类型** - Simulink 支持的任何数据类型； -->
<!-- 请参阅 [Simulink 支持的数据类型](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/data-types-supported-by-simulink.html)。 -->
- **维度** - 标量、一维（向量）、二维（矩阵）或多维（数组）。根据维度在一个信号中显示多个通道。

**输入限制：**

- 当输入是常量信号时，示波器绘制单个点；
- 当信号值为 NaN 时，示波器会在显示画面上显示缺口；
- 当您在示波器内可视化多个基于帧的信号时，部分帧大小为 1 的信号采样可能不会显示。要可视化这些信号，请将帧大小为 1 的信号转移到单独的示波器。

<!-- #### 总线支持

可将非虚拟总线和总线信号数组连接到示波器。要显示总线信号，请使用普通或加速仿真模式。示波器按照元素在总线中出现的顺序从上到下显示每个总线元素信号。嵌套的总线元素以平铺方式显示。 -->

<!-- 要使用示波器记录非虚拟总线信号，请将**保存格式**参数设置为“数据集”。您可以使用任何**保存格式**记录虚拟总线信号。 -->

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | enum


</div>
</div>



## 属性



### 配置属性

“配置属性”对话框控制有关 Scope 画面的各种属性。从Scope 工具栏中选择配置属性。


<div class="details-box">
<details open>
<summary>仿真开始时打开 — 指定示波器窗口何时打开<div>off（Scope 的默认值） | on</div></summary>
</details>
<div class="details-content">

选中此复选框可以在仿真开始时打开 Scope 窗口。

</div>
</div>




<!-- #### 编程用法

请参阅 [OpenAtSimulationStart](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/spbscopes.scope.timescopeconfiguration.html#buvw6zv-1-OpenAtSimulationStart)。 -->



<!-- ### 显示完整路径 — 在示波器标题栏上显示模块路径 off （默认） | on



选中此复选框将显示模块名称以及模块路径。 -->


<div class="details-box">
<details open>
<summary>输入端口数 — Scope 模块上输入端口的数量<div>1 （默认） | 整数</div></summary>
</details>
<div class="details-content">

指定 Scope 模块上输入端口的数量（指定为整数）。输入端口的最大数量为 96。

</div>
</div>




<!-- #### 编程用法

请参阅 [NumInputPorts](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/spbscopes.scope.timescopeconfiguration.html#mw_9dd54e75-40d5-495f-97f3-fefb913332bb)。 -->


<div class="details-box">
<details open>
<summary>显示类型 — 指定示波器显示的信号类型<div>y(t)plot (默认) | y(x)plot</div></summary>
</details>
<div class="details-content">

指定 Scope 显示的信号类型。

</div>
</div>





<!-- ### 布局 — 显示画面的数量和排列方式 1×1 画面 （默认） | m×n 个坐标区



指定显示画面的数量和排列方式。最大布局为 16 行 × 16 列。

要扩大布局网格使其超过 4×4，请在对话框内点击并拖动。最大为 16 行 × 16 列。

![Animated GIF of changing the layout from one display to three displays](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/layout.gif)



如果画面数等于端口数，每个端口的信号将单独显示。如果画面数小于端口数，多出的端口信号将显示在最后一个画面上。对于具有多列和多行的布局，端口先从上到下，再从左到右进行映射。

#### 编程用法

请参阅 [LayoutDimensions](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/spbscopes.scope.timescopeconfiguration.html#buvw6zv-1-LayoutDimensions)。



### 采样时间 — 示波器更新之间的仿真间隔 -1（表示继承） （默认） | 正实数



指定示波器显示画面更新之间的时间间隔。此属性不适用于浮动示波器和波形查看器。有关示波器中采样时间的更详细说明，请参阅[Sample Time with Scope Blocks](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/sample-time-with-scope-blocks-example.html)

#### 编程用法

请参阅 [SampleTime](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/spbscopes.scope.timescopeconfiguration.html#buvw6zv-1-SampleTime)。



### 输入处理 — 信道或元素信号处理 “元素作为通道(基于采样)”（Scope 的默认值） | “列作为通道(基于帧)”（Time Scope 的默认值）



- “元素作为通道(基于采样)” - 将每个元素作为唯一采样进行处理。
- “列作为通道(基于帧)” - 将信道中的信号值作为一组不同时间间隔的值进行处理。基于帧的处理方式仅对离散输入信号可用。

#### 编程用法

请参阅 [FrameBasedProcessing](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/spbscopes.scope.timescopeconfiguration.html#buvw6zv-1-FrameBasedProcessing)。



### 最大化坐标区 — 最大化图的大小 “off”（Scope 的默认值） | “自动”（Time Scope 的默认值） | “on”



- “自动” - 如果未指定 [标题, Title标题Title](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/scope.html#f5-1117037_sep_buzep8m-1) 和 [Y 标签, Y-labelY 标签Y-label](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/scope.html#f5-1117037_sep_buzep8m-23) 属性，则最大化所有图。
- “on” - 最大化所有图。**标题**和 **Y 标签**值被隐藏。
- “off” - 不最大化图。

#### 编程用法

请参阅 [MaximizeAxes](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/spbscopes.scope.timescopeconfiguration.html#buvw6zv-1-MaximizeAxes)。

**时间**



### 时间跨度 — 要显示的 x 轴的长度 “自动” （默认） | “用户定义” | “一帧周期”



- “自动” - 仿真开始时间与停止时间之间的时间差。

  此模块使用 [时间显示偏移量, Time display offset时间显示偏移量Time display offset](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/scope.html#f5-1117037_sep_buzep61-12) 和 [时间跨度, Time span时间跨度Time span](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/scope.html#f5-1117037_sep_buzep61-1) 属性来计算时间范围的开始时间和结束时间。例如，如果将**时间显示偏移量**设置为 10，将**时间跨度**设置为 20，波形会将时间范围设置为从 10 到 30。

- “用户定义” - 输入小于总仿真时间的任何值。

- “一帧周期” - 将输入信号的帧周期用于 Time Scope 模块。仅当**输入处理**参数设置为“列作为通道(基于帧)” 时，此选项才可用。

#### 编程用法

请参阅 [TimeSpan](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/spbscopes.scope.timescopeconfiguration.html#buvw6zv-1-TimeSpan)。



### 时间跨度超限操作 — 显示超出 x 轴可见范围的数据 “绕回” （默认） | “滚动”



指定如何显示超出 x 轴可见范围的数据。

只有在由于模型较大或者步长较小而导致绘图速度缓慢时，才能看到此操作的效果。

- “绕回” - 从左到右全屏绘制数据，之后擦除屏幕，然后再从左到右重新开始绘制数据。
- “滚动” - 在右侧绘制新数据时，旧数据向左移动。此模式由于有密集的图形操作，可能会影响运行时性能。

#### 编程用法

请参阅 [TimeSpanOverrunAction](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/spbscopes.scope.timescopeconfiguration.html#buvw6zv-1-TimeSpanOverrunAction)。



### 时间单位 — x 轴单位 “无”（Scope 的默认值） | “度量”（Time Scope 的默认值） | “秒”



- “度量” - 基于 [时间跨度, Time span时间跨度Time span](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/scope.html#f5-1117037_sep_buzep61-1) 的长度显示时间单位。
- “秒” - 以秒为单位显示时间。
- “无” - 不显示时间单位。

#### 编程用法

请参阅 [TimeUnits](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/spbscopes.scope.timescopeconfiguration.html#buvw6zv-1-TimeUnits)。



### 时间显示偏移量 — x 轴偏移量 0 （默认） | 标量 | 向量



将 x 轴偏移指定的时间值，指定为实数或由实数组成的向量。

对于具有多个信道的输入信号，可以输入标量或向量：

- 标量 - 按相同的时间值偏移输入信号的所有信道。
- 向量 - 分别偏移每个通道。

#### 编程用法

请参阅 [TimeDisplayOffset](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/spbscopes.scope.timescopeconfiguration.html#buvw6zv-1-TimeDisplayOffset)。



### 时间轴标签 — x 轴标签的显示 “仅底部显示”（Scope 的默认值） | “全部”（Time Scope 的默认值） | “无”



指定如何显示 x 轴（时间）标签：

- “全部” - 在所有 y 轴上显示 x 轴标签。
- “无” - 不显示标签。选择“无”也将清除**显示时间轴标签**复选框。
- “仅底部显示” - 在底部 y 轴上显示 x 轴标签。



#### 依存关系

要启用此属性，请进行如下设置：

- 将 [显示时间轴标签, Show time-axis label显示时间轴标签Show time-axis label](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/scope.html#f5-1117037_sep_buzep61-18) 设置为 on。
- 将 [最大化坐标区, Maximize axes最大化坐标区Maximize axes](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/scope.html#buzep1u-1) 设置为 off。



[活动画面, Active display活动画面Active display](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/scope.html#f5-1117037_sep_buw9onn-1) 属性确定哪个画面受到影响。

#### 编程用法

请参阅 [TimeAxisLabels](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/spbscopes.scope.timescopeconfiguration.html#buvw6zv-1-TimeAxisLabels)。



### 显示时间轴标签 — 显示或隐藏 x 轴标签 off（Scope 的默认值） | on（Time Scope 的默认值）



选中此复选框可显示活动显示屏的 x 轴标签

#### 依存关系

要启用此属性，请将 [时间轴标签, Time-axis labels时间轴标签Time-axis labels](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/scope.html#f5-1117037_sep_buzep61-15) 设置为“全部”或“仅底部显示”。

[活动画面, Active display活动画面Active display](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/scope.html#f5-1117037_sep_buw9onn-1) 属性确定哪个画面受到影响。

#### 编程用法

请参阅 [ShowTimeAxisLabel](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/spbscopes.scope.timescopeconfiguration.html#buvw6zv-1-ShowTimeAxisLabel)。

**显示**



### 活动画面 — 所选的画面 1 （默认） | 正整数



所选的画面。使用此属性来控制当更改样式属性和特定于坐标区的属性时会更改哪个画面。

使用与列放置索引相对应的正整数来指定所需的画面。对于具有多列和多行的布局，显示屏编号先从上到下，再从左到右进行映射。

#### 编程用法

请参阅 [ActiveDisplay](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/spbscopes.scope.timescopeconfiguration.html#buvw6zv-1-ActiveDisplay)。



### 标题 — 画面名称 %<SignalLabel> （默认） | 字符串



画面的标题。默认值 %<SignalLabel> 使用输入信号名称作为标题。

#### 依存关系

[活动画面, Active display活动画面Active display](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/scope.html#f5-1117037_sep_buw9onn-1) 属性确定哪个画面受到影响。

#### 编程用法

请参阅 [Title](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/spbscopes.scope.timescopeconfiguration.html#buvw6zv-1-Title)。



### 显示图例 — 显示信号图例。 off （默认） | on



切换信号图例。图例中列出的名称是来自模型的信号名称。对于有多个通道的信号，信号名称后面会附加一个通道索引。连续信号的名称前面带有直线条，离散信号的名称前面带有楼梯形线条。

从图例中，您可以控制哪些信号可见。此控制项等效于更改**样式**属性中的可见性。在示波器图例中，点击某信号名称可在示波器中隐藏该信号。要显示该信号，请再次点击信号名称。要只显示一个信号，请右键点击该信号名称，这将隐藏所有其他信号。要显示所有信号，请按 **Esc**。



**注意**

图例只显示前 20 个信号。任何其他信号都无法从图例中控制。



#### 依存关系

[活动画面, Active display活动画面Active display](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/scope.html#f5-1117037_sep_buw9onn-1) 属性确定哪个画面受到影响。

#### 编程用法

请参阅 [ShowLegend](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/spbscopes.scope.timescopeconfiguration.html#buvw6zv-1-ShowLegend)。



### 显示网格 — 显示内部网格线 on （默认） | off



选中此复选框可显示网格线。

#### 依存关系

[活动画面, Active display活动画面Active display](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/scope.html#f5-1117037_sep_buw9onn-1) 属性确定哪个画面受到影响。

#### 编程用法

请参阅 [ShowGrid](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/spbscopes.scope.timescopeconfiguration.html#buvw6zv-1-ShowGrid)。



### 绘制信号的幅值和相位图 — 将画面拆分为幅值图和相位图。 off （默认） | on



- On - 显示幅值图和相位图。如果信号是实数，则绘制信号的绝对值作为幅值。正值的相位为 0 度，负值的相位为 180 度。此功能对于复数值输入信号很有用。如果输入是实数值信号，则选中此复选框将返回信号的绝对值作为幅值。
- Off - 显示信号图。如果信号是复信号，则基于同一 y 轴绘制实部和虚部。

#### 依存关系

[活动画面, Active display活动画面Active display](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/scope.html#f5-1117037_sep_buw9onn-1) 属性确定哪个画面受到影响。

#### 编程用法

请参阅 [PlotAsMagnitudePhase](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/spbscopes.scope.timescopeconfiguration.html#buvw6zv-1-PlotAsMagnitudePhase)。



### Y 范围(最小值) — 最小 y 轴值 -10 （默认） | 实数标量



将 y 轴的最小值指定为一个实数。

**可调：** Yes

#### 依存关系

如果选择了**绘制信号的幅值和相位图**，此属性将仅应用于幅值图。相位图的 y 轴范围始终为 [-180 180]。

[活动画面, Active display活动画面Active display](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/scope.html#f5-1117037_sep_buw9onn-1) 属性确定哪个画面受到影响。

#### 编程用法

请参阅 [YLimits](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/spbscopes.scope.timescopeconfiguration.html#buvw6zv-1-YLimits)。



### Y 范围(最大值) — 最大 y 轴值 10 （默认） | 实数标量



将 y 轴的最大值指定为一个实数。

**可调：** Yes

#### 依存关系

如果选择了**绘制信号的幅值和相位图**，此属性将仅应用于幅值图。相位图的 y 轴范围始终为 [-180 180]。

[活动画面, Active display活动画面Active display](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/scope.html#f5-1117037_sep_buw9onn-1) 属性确定哪个画面受到影响。

#### 编程用法

请参阅 [YLimits](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/spbscopes.scope.timescopeconfiguration.html#buvw6zv-1-YLimits)。



### Y 标签 — Y 轴标签 none（Scope 的默认值） | Amplitude（Time Scope 的默认值） | 字符串



指定要在 y 轴上显示的文本。要显示信号单位，请在标签中添加 (%<SignalUnits>)。仿真开始时，Simulink 会将 (%SignalUnits) 替换为与信号关联的单位。

**示例：** 对于单位为 m/s 的速度信号，输入 Velocity (%<SignalUnits>)。

#### 依存关系

如果选择了**绘制信号的幅值和相位图**，则此属性不适用。两个 y 轴将分别显示 Magnitude 和 Phase 标签。

[活动画面, Active display活动画面Active display](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/scope.html#f5-1117037_sep_buw9onn-1) 属性确定哪个画面受到影响。

#### 编程用法

请参阅 [YLabel](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/spbscopes.scope.timescopeconfiguration.html#buvw6zv-1-YLabel)。

**记录**



### 将数据点限制为最后 — 限制缓冲的数据值 off，5000 （默认） | on | 正整数



限制示波器内部保存的数据。默认情况下保存所有数据点，以便您在仿真完成后查看波形可视化。对于**停止时间**设置为 inf 的仿真，请考虑选择**将数据点限制为最后**。



**注意**

如果您没有选择**将数据点限制为最后**，并且所用的采样率较高或仿真时间较长，则您可能遇到内存或系统性能问题。

选择此属性时，示波器会保存最新的 n 个数据点，其中 n 指定数据点的数量。

- Off - 保存并绘制所有数据值。

- On - 为每个信号保存指定数量的数据值。如果信号基于帧，则缓冲的数据值数量等于指定的数据值数量乘以帧大小。

  在某些情况下（例如采样时间较短时），选择此属性可能会使得绘制信号的时间长度小于整个仿真时间范围。如果波形只绘制了信号的一部分，请考虑增加要保存的数据点数量。

此属性会限制在示波器中绘制的数据值的数量，以及保存到 [变量名称, Variable name变量名称Variable name](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/scope.html#buuaegp-1) 中指定的 MATLAB®[变量名称, Variable name变量名称Variable name](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/scope.html#buuaegp-1) 变量的数据值的数量。

#### 编程用法

请参阅 [DataLoggingLimitDataPoints](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/spbscopes.scope.timescopeconfiguration.html#buvw6zv-1-DataLoggingLimitDataPoints) 和 [DataLoggingMaxPoints](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/spbscopes.scope.timescopeconfiguration.html#buvw6zv-1-DataLoggingMaxPoints)。



### 抽取 — 减少要显示和保存的波形数据量 off，2 （默认） | on | 正整数



- On - 绘制并记录（保存）每 N 个数据点的波形数据，其中 N 是在文本框中输入的抽取因子。值为 1 将缓冲所有数据值。
- Off - 保存所有波形数据值。

#### 依存关系

要启用此属性，请选择 [将数据记录到工作区, Log data to workspace将数据记录到工作区Log data to workspace](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/scope.html#buuaegb-1)。

此属性会限制在示波器中绘制的数据值的数量，以及保存到 [变量名称, Variable name变量名称Variable name](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/scope.html#buuaegp-1) 中指定的 MATLAB 变量的数据值的数量。

#### 编程用法

请参阅 [DataLoggingDecimateData](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/spbscopes.scope.timescopeconfiguration.html#buvw6zv-1-DataLoggingDecimateData) 和 [DataLoggingDecimation](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/spbscopes.scope.timescopeconfiguration.html#buvw6zv-1-DataLoggingDecimation)。



### 将数据记录到工作区 — 将数据保存到 MATLAB 工作区 off （默认） | on



选中此复选框可启用日志记录，并启用**变量名称**、**保存格式**和**抽取**属性。此属性不适用于浮动示波器和波形查看器。

有关使用 Scope 模块将信号保存到 MATLAB 工作区的示例，请参阅[使用 Scope 模块保存仿真数据](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/scope-block-tasks.html#bu55s2j-1)。

#### 编程用法

请参阅 [DataLogging](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/spbscopes.scope.timescopeconfiguration.html#buvw6zv-1-DataLogging)。



### 变量名称 — 所保存数据变量的名称 “ScopeData” （默认） | 字符串



指定一个用于在 MATLAB 工作区中保存波形数据的变量名称。此属性不适用于浮动示波器和波形查看器。

#### 依存关系

要启用此属性，请选择 [将数据记录到工作区, Log data to workspace将数据记录到工作区Log data to workspace](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/scope.html#buuaegb-1)。

#### 编程用法

请参阅 [DataLoggingVariableName](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/spbscopes.scope.timescopeconfiguration.html#buvw6zv-1-DataLoggingVariableName)。



### 保存格式 — MATLAB 变量格式 “数据集” （默认） | “带时间的结构体” | “结构体” | “数组”



选择一个用于在 MATLAB 工作区中保存数据的变量格式。此属性不适用于浮动示波器和波形查看器。

- “数据集” - 将数据保存为 [Dataset](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/simulink.simulationdata.dataset.html) 对象，默认为 timeseries 对象。
- “带时间的结构体” - 将数据保存为带有关联时间信息的结构体。
- “结构体” - 将数据保存为结构体。
- “数组” - 将数据保存为带有相关时间信息的数组。此格式不支持可变大小数据。



#### 依存关系

要启用此属性，请选择 [将数据记录到工作区, Log data to workspace将数据记录到工作区Log data to workspace](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/scope.html#buuaegb-1)。

#### 编程用法

请参阅 [DataLoggingSaveFormat](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/spbscopes.scope.timescopeconfiguration.html#buvw6zv-1-DataLoggingSaveFormat)。 -->

<!-- ### 坐标区缩放属性

**坐标区缩放**对话框控制示波器的坐标区范围。要打开坐标区缩放属性，请在示波器菜单中，选择**工具** > **坐标区缩放** > **坐标区缩放属性**。



### 坐标区缩放 — Y 轴缩放模式 “手动” （默认） | “自动” | “N 次更新后”



- “手动” - 使用**缩放 Y 轴范围**工具栏按钮手动缩放 y 轴范围。
- “自动” - 在仿真期间和仿真后缩放 y 轴范围。选择此选项将显示**不允许 Y 轴范围收缩**复选框。如果您希望通过信号的最大值来增加或减小 y 轴范围，请将**坐标区缩放**设置为“自动”，并清除**不允许 Y 轴范围收缩**复选框。
- “N 次更新后” - 在**更新次数**文本框中指定的时间步数（默认值为 10）后，缩放 y 轴。每次运行期间仅发生一次缩放。

#### 编程用法

请参阅 [AxesScaling](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/spbscopes.scope.timescopeconfiguration.html#buvw6zv-1-AxesScaling)。



### 不允许 Y 轴范围收缩 — 当 y 轴范围可以更改时，对其范围施加限制 on （默认） | off



在仿真期间允许增大 y 轴范围，但不允许缩小范围。

#### 依存关系

要使用此属性，请将**坐标区缩放**设置为“自动”。



### 更新次数 — 缩放之前的更新次数 10 （默认） | 整数



设置此属性可延迟 y 轴的自动缩放。

#### 依存关系

要使用此属性，请将**坐标区缩放**设置为 “N 次更新后”。

#### 编程用法

请参阅 [AxesScalingNumUpdates](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/spbscopes.scope.timescopeconfiguration.html#buvw6zv-1-AxesScalingNumUpdates)。



### 停止时缩放坐标区范围 — 当 y 轴范围可以更改时，对其范围施加限制 on （默认） | off



- On - 在仿真停止时缩放坐标区。
- Off - 连续缩放坐标区。

#### 依存关系

要使用此属性，请将**坐标区缩放**设置为“自动”。



### Y 轴数据范围(%) — 绘图空间占 y 轴范围的百分比 80 （默认） | [1, 100] 之间的整数



指定绘制数据图时所使用的 y 轴范围的百分比。如果将此属性设置为 100，绘图数据将使用整个 y 轴范围。



### Y 轴对齐 — 沿 y 轴对齐 Center （默认） | Top | Bottom



指定当 **Y 轴数据范围**设置小于 100% 时，绘图数据沿 y 轴数据范围对齐的位置。

- “顶端” - 将信号与 y 轴范围的最大值对齐。
- “居中” - 使信号在最小值和最大值之间居中。
- “底端” - 将信号与 y 轴范围的最小值对齐。





### 自动缩放 X 轴范围 — 缩放 x 轴范围界限 off （默认） | on



缩放 x 轴范围以容纳所有信号值。如果**坐标区缩放**设置为 Auto，则只缩放当前在坐标区范围内的数据，而不是数据缓冲区中的整个信号。



### X 轴数据范围(%) — 绘图空间占 x 轴范围的百分比 100 （默认） | 范围 [1, 100] 内的整数



指定绘制数据图时所使用的 x 轴范围的百分比。例如，如果将此属性设置为 100，绘图数据将使用整个 x 轴范围。



### X 轴对齐 — 沿 x 轴对齐 Center （默认） | Left | Right



指定当 **X 轴数据范围**设置小于 100% 时，绘图数据沿 x 轴数据范围对齐的位置。

- “右侧” - 将信号与 x 轴范围的最大值对齐。
- “居中” - 使信号在最小值和最大值之间居中。
- “左侧” - 将信号与 x 轴范围的最小值对齐。 -->

<!-- ### 样式属性

要打开“样式”对话框，请从示波器菜单中，选择**视图** > **样式**。



### 图窗颜色 — 窗口的背景色 黑色 （默认） | 颜色



示波器的背景色。



### 绘图类型 — 如何绘制信号 “自动”（Scope 的默认值） | “线图”（Time Scope 的默认值） | “阶梯图” | “针状图”



当您选择“自动”时，绘图类型是对连续信号使用线图、对离散信号使用阶梯图、对 Simulink 消息信号使用针状图。



### 坐标区颜色 — 各个画面的背景色和坐标区颜色 黑色 （默认） | 颜色



使用第一个调色板选择坐标区（视图）的背景色。使用第二个调色板选择网格和标签颜色。



### 保留复制到剪贴板的颜色 — 复制波形而不更改颜色 off （默认） | on



指定复制时是否使用显示的示波器颜色。

如果您选择**文件** > **复制到剪贴板**，软件会将示波器的颜色更改为适合打印机的颜色（白色背景、可见线条）。如果要按显示的颜色复制并粘贴示波器，请选中此复选框。



### 线条的属性 — 要更改的线条 “通道 1” （默认）



选择设置线型属性所针对的活动线条。



### 可见 — 线条可见性 on （默认） | off



在图上显示或隐藏信号。

#### 依存关系

[活动画面, Active display活动画面Active display](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/scope.html#f5-1117037_sep_buw9onn-1) 和 [线条的属性, Properties for line线条的属性Properties for line](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/scope.html#f5-1117037_sep_mw_4f8bb55d-996e-40da-baa1-9da1f86b13a5) 的值决定哪个线条受到影响。



### 线图 — 线型 实线（默认样式） | 0.75（默认宽度） | 黄色（默认颜色）



选择线型、线宽和颜色。

#### 依存关系

[活动画面, Active display活动画面Active display](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/scope.html#f5-1117037_sep_buw9onn-1) 和 [线条的属性, Properties for line线条的属性Properties for line](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/scope.html#f5-1117037_sep_mw_4f8bb55d-996e-40da-baa1-9da1f86b13a5) 的值决定哪个线条受到影响。



### 标记 — 数据点标记样式 “无” （默认） | 标记样式



选择标记样式。

#### 依存关系

[活动画面, Active display活动画面Active display](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/scope.html#f5-1117037_sep_buw9onn-1) 和 [线条的属性, Properties for line线条的属性Properties for line](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/scope.html#f5-1117037_sep_mw_4f8bb55d-996e-40da-baa1-9da1f86b13a5) 的值决定哪个线条受到影响。 -->



<!-- ## 模块特性

| **数据类型**                                                 | Boolean | busa | double | enumerated | fixed point | half | integer | single |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| **直接馈通**                                                 | 否                                                         |
| **多维信号**                                                 | 是                                                         |
| **可变大小信号**                                             | 是                                                         |
| **过零检测**                                                 | 否                                                         |
| [a](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/scope.html?s_tid=doc_ta#d125e165211) 不支持虚拟总线。非虚拟总线仅在 Normal 模式和 Accelerator 模式的仿真中受支持。非虚拟总线的数据记录只支持数据集格式 |                                                              | -->


## 版本历史记录

- 在 2024b 之前推出

### 限制信息

1. 暂不支持配置显示完整路径、布局、采样时间、输入处理 和 最大化坐标等主要属性；  
2. 暂不支持配置时间跨度、时间跨度超限操作、时间单位、时间显示偏移量、时间轴标签和显示时间轴的时间属性；  
3. 暂不支持配置活动画面、标题、显示图例、显示网络、绘制信号的幅值和相位图、Y 范围的最大最小值和 Y 标签的显示属性；  
4. 暂不支持配置将数据点限制为最后，将帧数限制为最后、抽取，抽取帧、将数据记录到工作区、变量名称和保存格式的记录属性；  
5. 暂不支持坐标区缩放、不允许 Y 轴范围收缩、更新次数、停止时缩放坐标区范围、Y 轴数据范围（%）、Y 轴对齐、自动缩放 X 轴范围、X 轴数据范围（%）和 X 轴对齐的坐标区缩放属性；  
6. 暂不支持图窗颜色、绘图类型、坐标区颜色、保留复制到剪贴板的颜色、线条的属性、可见、线图和标记的样式属性；  
7. 可视化的信号暂不支持总线和非虚拟总线的结构，暂不支持 half、int64、uint64、fixedPoint 和 bus 的数据类型。

<!-- ## 扩展功能



### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。

此模块可用于在对要生成代码的系统进行仿真时查看仿真情况，但生成的代码中不会包含此模块。



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 Verilog 代码和 VHDL 代码。



此模块可用于生成 HDL 代码的子系统中的仿真可见性，但不包括在硬件实现中。



### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。

此模块可用于在对要生成代码的系统进行仿真时查看仿真情况，但生成的代码中不会包含此模块。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。

此模块接受定点输入，但将其转换为 double 进行显示。

## 版本历史记录

**在 R2015b 中推出** -->

<!-- ## 另请参阅

[Floating Scope](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/scopeviewer.html) | [Scope Viewer](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/scopeviewer.html)

### 主题

- [Scope 模块和波形查看器概述](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/simulation-data-display-and-capture-using-scopes.html)
- [步进仿真](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/stepping-through-a-simulation.html)
- [常见的示波器模块任务](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/scope-block-tasks.html)
- [Control Scope Blocks Programmatically](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/control-scopes-programmatically.html)
- [Scope Block with Android Devices](https://ww2.mathworks.cn/help/releases/R2022b/supportpkg/android/ref/scope-with-android-devices.html) (Simulink Support Package for Android Devices)
- [使用 Apple iOS 设备的 Scope 模块](https://ww2.mathworks.cn/help/releases/R2022b/supportpkg/appleios/ug/getting-started-with-apple-ios-devices.html) (Simulink Support Package for Apple iOS Devices)
- [Simulink Scope Block and Mobile Apps](https://ww2.mathworks.cn/help/releases/R2022b/supportpkg/android/ug/simulink-scope-block-and-mobile-apps.html) (Simulink Support Package for Android Devices) -->