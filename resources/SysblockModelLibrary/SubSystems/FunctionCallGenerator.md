# FunctionCallGenerator
---
&nbsp;

提供函数调用事件来控制子系统或模型的执行

- **库：** Sysblock / Subsystems

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SubSystems/FunctionCallGenerator/FunctionCallGenerator.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

Function-Call Generator 模块提供函数调用事件，用于以您在**采样时间**参数中指定的速率执行函数调用子系统或函数调用模型。函数调用子系统或函数调用模型是包含 Trigger 模块的子系统或模型，其**触发器类型**参数设置为**函数调用**。

要以迭代方式在每个时间步中多次执行每个函数调用子系统或函数调用模型，请使用**迭代次数**参数。
 

要间歇地（意味着不是在每个时间步）执行函数调用子系统或函数调用模型，请选择**显示使能端口**参数。然后，您可以使用使能端口的输入来控制模块何时输出函数调用事件。实际上，您可以根据需要打开和关闭模块。

## 示例

以指定的速率执行子系统，子系统中设置累加算法。Function-Call Generator 模块中的采样时间设置为 0.2，表示每 0.2s 调用一次 functionCall 子系统(采样时间必须设置为模型仿真步长的整数倍)，迭代次数设置为 1，表示一个仿真步中执行的调用次数。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SubSystems/FunctionCallGenerator.mo">FunctionCallGenerator.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SubSystems/FunctionCallGenerator/FunctionCallGenerator01.png')" style="width:600px">

在子系统中放入触发模块 trigger，并将触发类型选择为 functionCall。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SubSystems/FunctionCallGenerator/FunctionCallGenerator02.png')" style="width:600px">

模型的仿真步长设置为 0.1S，仿真时间设置为 1S，Function-Call Generator 模块设置为 0.2S，代表每 0.2S 调用一次。
预期结果 1S 内该子系统一共被调用 6 次，分别在 0S、0.2S、0.4S、0.6S、0.8S、1S 处生成结果 1、2、3、4、5、6。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SubSystems/FunctionCallGenerator/FunctionCallGenerator03.png')" style="width:600px">

## 端口

### 输入

<div class="details-box">
<details open>
<summary>启用 — 控制信号输入<div>标量</div></summary>
</details>
<div class="details-content">

仅当此端口的输入为正数时，此模块才输出函数调用事件。

#### 依存关系

要启用此端口，请选中**显示使能端口**复选框。

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>函数调用 — 函数调用事件输出<div>标量 | 向量</div></summary>
</details>
<div class="details-content">


将函数调用事件发送到函数调用子系统或函数调用模型的函数调用输入端口。

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>采样时间 — 指定时间间隔<div>1（默认） | 标量 | 向量 | -1</div></summary>
</details>
<div class="details-content">

指定函数调用子系统或含调用模型的函数调用事件之间的时间间隔。如
默认情况下，该模块使用的时间间隔为 1。

#### 依存关系

要启用此参数，请清除**显示使能端口**复选框。如果选择**显示使能端口**，采样时间将自动设置为 -1（继承）。

</div>
</div>


<!-- 
#### 编程用法

| **模块参数**：`sample_time`                      |
| ------------------------------------------------ |
| **类型**：字符向量                               |
| **值**：`'1'` | 标量表达式 | 向量表达式 | `'-1'` |
| **默认值**：`'1'`                                | -->


<div class="details-box">
<details open>
<summary>迭代次数 — 指定在每个时间步中提供函数调用的次数<div>1（默认）| 整数</div></summary>
</details>
<div class="details-content">

此参数的值可以是向量，向量的每个元素指定执行函数调用子系统或模型的次数。如果指定向量，则该模块输出函数调用事件的向量，该向量可以使用 [Demux](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SignalRouting/DeMux.html) 模块拆分成单个函数调用事件，并用于驱动多个函数调用子系统或模型。

假设您将**迭代次数**指定为 [3 2]，并将此模块的输出连接到 Demux 模块，后者又连接到两个函数调用子系统的控制端口。在本例中，第一个函数调用子系统在每个时间步执行三次，第二个函数调用子系统在每个时间步执行两次。

但是，如果您将此模块的输出连接到单个函数调用子系统或模型，则函数调用子系统或模型在每时间步执行的总次数等于向量元素值的总和。因此，在上面的示例中，将**迭代次数**指定为 [3 2] 并将此模块的输出连接到单个函数调用子系统，会导致函数调用子系统在每个时间步执行五次。

#### 设置

- **1**

  在每个时间步期间提供一次函数调用。

- **整数**

  有符号或无符号整数。在每个时间步提供指定数量的函数调用。


</div>
</div>


<!-- 
#### 编程用法

| **模块参数**：`numberOfIterations`                    |
| ----------------------------------------------------- |
| **类型**：字符向量                                    |
| **值**：`'1'` | `'<integer>'``'<vector of integers>'` |
| **默认值**：`'1'`                                     | -->

<div class="details-box">
<details open>
<summary>不允许宽输出 — 防止输出信号的隐式扩展<div>off（默认）| on</div></summary>
</details>
<div class="details-content">

除非选择此参数，否则此模块的输出将扩展为向量，以在必要时驱动连接到它的模块。例如，如果**迭代次数**设置为 2，并且未选择**不允许宽输出**，并且此模块的输出连接到 Demux 模块，此模块又连接到三个单独的函数调用子系统，则每个函数调用子系统在每个时间步接收两个函数调用事件。

</div>
</div>



<!-- 
#### 编程用法

| **模块参数**：`DisallowWideOutput` |
| ---------------------------------- |
| **类型**：字符向量                 |
| **值**：`'off'` | `'on'`           |
| **默认值**：`'off'`                | -->


<div class="details-box">
<details open>
<summary>显示使能端口 — 添加控制信号的输入端口<div>off（默认）| on</div></summary>
</details>
<div class="details-content">

选择此参数可向模块添加控制信号输入端口。仅当控制信号输入端口的值为正数时，该模块才输出函数调用事件。

清除此参数可删除控制信号输入端口。该模块在每个时间步输出函数调用事件。

</div>
</div>

<!-- 
#### 编程用法

| **模块参数**：`ShowEnablePort` |
| ------------------------------ |
| **类型**：字符向量             |
| **值**：`'off'` | `'on'`       |
| **默认值**：`'off'`            | -->
<!-- 
## 模型示例

[![连接到同一函数调用信号的各分支的函数调用模块](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/functioncallfeedbacklatchwithsplitblockexample_01_zh_CN.png)连接到同一函数调用信号的各分支的函数调用模块在此模型中，Function-Call Feedback Latch 模块位于分支模块之间的反馈信号上。](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/function-call-blocks-connected-to-branches-of-same-function-call-signal.html)

[![Function-Call Feedback Latch on Feedback Signal Between Child and Parent](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink/win64/FunctionCallFeedbackLatchParentChildBlockExample_01.png)Function-Call Feedback Latch on Feedback Signal Between Child and ParentIn this model, the Function-Call Feedback Latch block is on the feedback signal between the child and the parent.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/function-call-feedback-latch-on-feedback-signal-between-child-and-parent.html)

[![单一函数调用子系统](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/singlefunctioncallsubsystemblockexample_01_zh_CN.png)单一函数调用子系统在此示例中，单一函数调用子系统输出充当它自己的输入。](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/single-function-call-subsystem.html)

[![Function-Call Subsystem with Merged Signal As Input](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink/win64/FunctionCallSubsystemMergedInputBlockExample_01.png)Function-Call Subsystem with Merged Signal As InputIn this model a merged signal serves as the input to a function-call subsystem.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/function-call-subsystem-with-merged-signal-as-input.html) -->

<!-- ## 模块特性 -->

<!-- | **数据类型**     |      |
| ---------------- | ---- |
| **直接馈通**     | `否` |
| **多维信号**     | `否` |
| **可变大小信号** | `否` |
| **过零检测**     | `否` | -->

<!-- ## 扩展功能 -->



<!-- ### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。 -->

## 版本历史记录

- 在 2024b 之前推出

<!-- ### 限制信息
无 -->

## 另请参阅

[Trigger](Trigger.html)

<!-- ### 主题 -->

<!-- - [使用函数调用子系统](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/using-function-call-subsystems.html) -->