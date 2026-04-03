# Step
---
生成阶跃函数

**库：** Sysblock模块库 / Sources

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/Step/Step.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

Step 可在指定时间在两个定义的电平之间进行阶跃。如果仿真时间小于**阶跃时间**参数值，模块输出将为**初始值**参数值。如果仿真时间大于或等于**阶跃时间**，输出则为**终值**参数值。

在标量扩展后，数值模块参数必须具有相同的维度。如果**将向量参数解释为一维向量**选项设置为 off，模块将输出与参数具有相同维度和维数的信号。如果**将向量参数解释为一维向量**选项设置为 on 且数值参数为行或列向量（即，单行或单列二维数组），模块将输出向量（一维数组）信号。否则，模块将输出与参数具有相同维度和维数的信号。

## 示例

<!-- [![Double Bouncing Ball: Use of Adaptive Zero-Crossing Location](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink_general/win64/sldemo_doublebounceExample_07.png)Double Bouncing Ball: Use of Adaptive Zero-Crossing LocationChoose the correct zero-crossing location algorithm, based on the system dynamics. For Zeno dynamic systems, or systems with strong chattering, you can select the adaptive zero-crossing detection algorithm through the Configure pane:](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/double-bouncing-ball-use-of-adaptive-zero-crossing-location.html)

[![Engine Timing Model with Closed Loop Control](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink_automotive/win64/EngineTimingModelWithClosedLoopControlExample_03.png)Engine Timing Model with Closed Loop ControlEnhance a version of the open-loop engine model described in Modeling Engine Timing Using Triggered Subsystems. This model, sldemo_enginewc, contains a closed-loop and shows the flexibility and extensibility of Simulink® models. In this enhanced model, the objective of the controller is to regulate engine speed with a fast throttle actuator, such that changes in load torque have minimal effect. This is easily accomplished in Simulink by adding a discrete-time PI controller to the engine model.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/engine-timing-model-with-closed-loop-control.html) -->

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/Step.mo">Step.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/Step/Step_ex.png')" style="width: 300px; height: auto; transform: scale(0.8);">

### 示例说明

- Step 模块：用于生成一个阶跃信号，该信号在指定的时间点从初始值突变到最终值。在这个示例中，阶跃信号在仿真开始时（0 秒）从 0 跳变到 1；
- Scope 模块：用于显示模型的输出结果，即 Step 模块生成的阶跃信号。Scope 模块可以帮助用户直观地观察和分析信号的突变。


## 端口

### 输出

<div class="details-box">
<details open>
<summary>y — 输出阶跃信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

由参数**阶跃时间**、**初始值**和**终值**定义的输出阶跃函数信号。

**数据类型：** double

</div>
</div>



## 参数

### 主要

<div class="details-box">
<details open>
<summary>阶跃时间 — 阶跃发生的时间<div>1 （默认） | 标量</div></summary>
</details>
<div class="details-content">

以秒为单位指定输出从**初始值**参数跳到**终值**参数的时间。

</div>
</div>




<!-- #### 编程用法

| **模块参数**：Time                                         |
| ------------------------------------------------------------ |
| **类型**：字符向量                                           |
| **值：**'1' | real- or complex-valued scalar, vector, or matrix |
| **默认值**：'1'                                            | -->


<div class="details-box">
<details open>
<summary>初始值 — 阶跃之前的输出值<div>0 （默认） | 标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

指定仿真时间达到**阶跃时间**参数时的模块输出。

</div>
</div>




<!-- #### 编程用法

| **模块参数**：Before                                       |
| ------------------------------------------------------------ |
| **类型**：字符向量                                           |
| **值：**'1' | real- or complex-valued scalar, vector, or matrix |
| **默认值**：'0'                                            | -->


<div class="details-box">
<details open>
<summary>终值 — 阶跃之后的输出值<div>1 （默认） | 标量</div></summary>
</details>
<div class="details-content">


指定仿真时间达到并超过**阶跃时间**参数时的模块输出。

</div>
</div>



<!-- #### 编程用法

| **模块参数**：After                                        |
| ------------------------------------------------------------ |
| **类型**：字符向量                                           |
| **值：**'1' | real- or complex-valued scalar, vector, or matrix |
| **默认值**：'1'                                            | -->


<div class="details-box">
<details open>
<summary>采样时间 — 采样率<div>-1 （默认） | 标量</div></summary>
</details>
<div class="details-content">

指定阶跃的采样率。

</div>
</div>



<!-- 有关详细信息，请参阅 [指定采样时间](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/how-to-specify-the-sample-time.html)。 -->

<!-- #### 编程用法

| **模块参数**：SampleTime |
| -------------------------- |
| **类型**：字符向量         |
| **值**：标量               |
| **默认值**：'0'          | -->



<!-- ### 将向量参数解释为一维向量 — 将向量视为一维 on （默认） | off



如果**常量值**参数的计算结果为包含 N 个元素的行或列向量，选中此复选框将输出长度为 N 的向量。

- 如果**常量值**参数的计算结果为包含 N 个元素的行或列向量，则选中此复选框时，模块将输出长度为 N 的向量。例如，模块将输出 1-by-N 维或 N-by-1 维矩阵。
- 如果**常量值**参数的计算结果为包含 N 个元素的行或列向量，则清除此复选框时，模块不输出长度为 N 的向量。

#### 编程用法

| **模块参数**：VectorParams1D |
| ------------------------------ |
| **类型：**字符向量             |
| **值：**'on' | 'off'         |
| **默认值：**'on'             | -->



<!-- ### 启用过零检测 — 启用过零检测 on （默认） | off



选择此项以启用过零检测。有关详细信息，请参阅[过零检测](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/zero-crossing-detection.html)。

#### 编程用法

| **模块参数**：ZeroCross    |
| ---------------------------- |
| **类型**：字符向量 \| 字符串 |
| **值**：'off' | 'on'     |
| **默认值**：'on'           | -->


### 信号属性

<div class="details-box">
<details open>
<summary>输出数据类型 — 输出数据类型<div>“double” （默认） | “Inherit: backPropagation” | “float”</div></summary>
</details>
<div class="details-content">

输出数据类型。

<!-- 该类型可以继承、直接指定或表示为数据类型对象，如 Simulink.NumericType。 -->

当选择 “Inherit: Inherit：backpropagation” 时，模块使用驱动模块的数据类型。

单击**显示数据类型帮助**按钮 <img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/Step/Step_button.png')" style="width: 80px; height: auto; vertical-align:middle; display:inline; margin:0;"> 以显示**数据类型帮助**，帮助您设置数据类型属性。  

</div>
</div>
 <!-- | <data type expression> -->




  <!-- 有关详细信息，请参阅[使用数据类型助手指定数据类型]()。 -->

<!-- #### 编程用法

| **模块参数**：OutDataTypeStr                               |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值：**'Inherit: Inherit via internal rule' | 'double' | 'single' \| <数据类型表达式> |
| **默认值：**'double'                                       | -->



<!-- ### 数据类型覆盖 — 为此信号指定数据类型覆盖模式 Inherit | Off



为此信号选择数据类型覆盖模式。

- 当您选择 “inherit” 时，Simulink® 从信号的上下文（即：从 Simulink 中使用该信号的模块、Simulink.Signal 对象或 Stateflow® 图）中继承数据类型覆盖设置。
- 当您选择 “off” 时，Simulink 忽略信号上下文的数据类型覆盖设置。

有关详细信息，请参阅 Simulink 文档中的[使用数据类型助手指定数据类型](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/specify-data-types-using-data-type-assistant.html)。

#### 依存关系

要启用此参数，请点击**显示数据类型助手**按钮，并将**模式**设置为“内置”。

#### 提示

由于能够关闭单个数据类型的数据类型覆盖，您可以在应用数据类型覆盖时更好地控制模型中的数据类型。例如，您可以使用此选项确保数据类型满足下游模块的要求，而忽略数据类型覆盖设置。 -->



<!-- ## 模块特性

| **数据类型**     | double |
| ---------------- | -------- |
| **直接馈通**     | 否     |
| **多维信号**     | 否     |
| **可变大小信号** | 否     |
| **过零检测**     | 是     | -->


## 版本历史记录

- 在 2024b 之前推出

### 限制信息

1. 暂不支持将向量参数解释为一维向量的复选框；    
2. 暂不支持启动过零检测的复选框；   
3. 暂不支持选定 `<data type expression>` 的输出数据类型；  
4. 暂不支持选定数据类型覆盖的功能；  
5. 输出跃进信号暂不支持 single 的数据类型。

<!-- ## 扩展功能



### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。

不建议用于生产代码。

## 版本历史记录

**在 R2006a 之前推出** -->

<!-- ## 另请参阅

[Ramp](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/ramp.html) | [Repeating Sequence Stair](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/repeatingsequencestair.html) | [Signal Editor](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/signaleditorblock.html)

### 主题

- [信号基础知识](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/signal-basics.html) -->