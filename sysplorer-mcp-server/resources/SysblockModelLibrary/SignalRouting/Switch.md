# Switch
---
基于第二个输入的值在第一个输入和第三个输入之间切换输出

**库：** Sysblock模块库 / SignalRouting

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/Switch/Switch.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

Switch 模块根据第二个输入的值，传递第一个输入或第三个输入信号。第一个和第三个输入是数据输入。第二个输入是控制输入。可以使用**首个输入传递条件**和**阈值**参数指定模块传递第一个输入的条件。

### 总线支持

Switch 模块支持总线。数据输入可以是满足下列限制条件的虚拟或非虚拟总线信号：

- 所有总线必须相同（所有元素的层次结构相同并具有相同的名称和属性）；
- Switch 模块的非虚拟总线输入中的所有信号必须具有相同的采样时间。即使关联总线对象的元素指定了继承的采样时间，此要求也同样适用。
<!-- 
您可以使用 [Rate Transition](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/ratetransition.html) 模块更改总线中单个信号或所有信号的采样时间。有关详细信息，请参阅[Modify Sample Times for Nonvirtual Buses](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/specify-bus-signal-sample-times.html)和[支持总线的模块](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/bus-capable-blocks-1.html)。 -->

可使用总线数组作为 Switch 模块的输入信号。
<!-- 有关定义和使用总线数组的详细信息，请参阅[使用总线数组组合非虚拟总线](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/combining-buses-into-an-array-of-buses.html)。使用总线数组时，请将**阈值**参数设置为标量值。 -->

### 限制

如果 Switch 模块的数据输入是总线，两个总线的元素名称必须相同。使用相同的元素名称可以确保输出总线具有相同的元素名称，而不管模块选择了哪些输入总线。要确保您的模型满足此要求，请使用总线对象定义总线并将**元素名称不匹配**诊断设置为“错误”。
<!-- 有关详细信息，请参阅[模型配置参数：连接诊断](https://ww2.mathworks.cn/help/releases/R2022b/simulink/gui/diagnostics-pane-connectivity.html)。 -->

## 示例

<!-- [![具有布尔控制端口的 Switch 模块示例](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/switchblockwithabooleancontrolportexample_01_zh_CN.png)具有布尔控制端口的 Switch 模块示例此示例显示一个控制端口为布尔输入的 Switch 模块。](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/switch-block-with-boolean-control-port-example.html)

[![容错燃油控制系统建模](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/modelingafaulttolerantfuelcontrolsystemexample_02_zh_CN.png)容错燃油控制系统建模此示例说明如何结合使用 Stateflow® 和 Simulink® 来高效地进行混合系统建模。这种类型的建模对于具有基于离散事件的多种可能运行模式的系统特别有用。传统的信号流在 Simulink 中处理，而控制配置的更改在 Stateflow 中实现。下面所述的模型表示汽油引擎的燃油控制系统。该系统具有很强的稳健性，因为它可以检测到单个传感器的故障，并且可以动态重新配置控制系统以实现不间断运行。](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/modeling-a-fault-tolerant-fuel-control-system.html)

[![精确的过零检测](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/sldemo_zeroxingexample_02_zh_CN.png)精确的过零检测此示例说明 Simulink® 中过零的工作原理。在此模型中，三个经过偏移的正弦波被馈送到绝对值模块及饱和模块中。在正好 t = 5 时，开关模块的输出从绝对值变为饱和模块。Simulink 中的过零将自动检测到开关模块具体何时更改其输出，求解器将步进到事件发生的确切时间。您可以通过检查示波器输出来查看这些信息。](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/accurate-zero-crossing-detection.html) -->

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/Switch.mo">Switch.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/Switch/Switch_ex.png')" style="width: 600px; transform: scale(0.8);">

### 示例说明

- Step 模块：提供不同的步变信号作为 Switch 模块的输入信号；
- Ramp 模块：提供线性增加的信号作为 Switch 模块的控制信号。控制信号的值决定了哪个输入信号被选择作为输出；
- Switch 模块：根据控制信号选择两个输入信号中的一个作为输出。如果控制信号为 0，输出第一个输入信号；如果控制信号为 1，输出第二个输入信号；
- Scope 模块：用于显示模型的输出结果，即根据控制信号选择的输入信号。


## 端口

### 输入


<div class="details-box">
<details open>
<summary>u1 — 第一个数据输入信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

两个数据输入中的第一个。模块将第一个或第二个数据输入传播到输出。模块根据控制输入选择要传递的输入。使用**首个输入传递条件**和**阈值**参数指定控制输入传递第一个输入的条件。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | fixedPoint | enum | bus

</div>
</div>



<div class="details-box">
<details open>
<summary>u2 — 控制输入信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

控制信号，模块用该信号来确定是将第一个还是第二个数据输入传递给输出。如果控制输入满足**首个输入传递条件**参数中设置的条件，则模块将传递第一个数据输入。否则，模块将传递第二个数据输入。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | fixedPoint | enum

</div>
</div>


<div class="details-box">
<details open>
<summary>u3 — 第二个数据输入信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

两个数据输入中的第二个。模块将第一个或第二个数据输入传播到输出。模块根据控制输入选择要传递的输入。使用**首个输入传递条件**和**阈值**参数指定控制输入传递第一个或第二个输入的条件。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | fixedPoint | enum | bus

</div>
</div>



### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

根据控制信号值从第一个或第二个输入信号传播而来的输出信号。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | fixedPoint | enum | bus

</div>
</div>


## 参数



### 主要

<div class="details-box">
<details open>
<summary>首个输入传递条件 — 传递第一个数据输入的条件<div>“u2 > 阈值” （默认） | “u2 >= 阈值” | “u2~=0”</div></summary>
</details>
<div class="details-content">

选择模块传递第一个数据输入的条件。如果控制输入满足**首个输入传递条件**参数中设置的条件，模块将传递第一个输入。否则，模块将从输入 Port_3 传递第二个数据输入信号。

- “u2 >= 阈值”

  检查控制输入是否大于或等于阈值。

- “u2 > 阈值”

  检查控制输入是否大于阈值。

- “u2~=0”

  检查控制输入是否非零。

::: warning 注意 
对于枚举数据类型，Switch 模块不支持 “u2 ~= 0” 模式。
:::
  

::: tip 提示 
当控制输入为布尔信号时，可使用条件和阈值的以下组合之一：

- “u2 >= 阈值”，其中阈值等于 1；
- “u2 > 阈值”，其中阈值等于 0；
- “u2~=0”。

否则，Switch 模块将忽略阈值，并使用布尔值进行信号路由。如果值为 1，模块将传递第一个输入；如果值为 0，模块将传递第三个输入。
:::

</div>
</div>





<!-- MATLAB® 命令行窗口中也会显示描述此行为的警告消息。 -->

<!-- #### 编程用法

| **模块参数**：Criteria                                     |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值：**'u2 >= Threshold' | 'u2 > Threshold' | 'u2 ~= 0' |
| **默认值：**'u2 > Threshold'                               | -->



<div class="details-box">
<details open>
<summary>阈值 — 条件中使用的阈值<div>0 （默认） | scalar</div></summary>
</details>
<div class="details-content">

指定**首个输入传递条件**中使用的阈值，该阈值用于确定模块将哪个输入传递给输出的条件。**阈值**必须大于**输出最小值**且小于**输出最大值**。

<!-- 要指定非标量阈值，请使用括号。例如，以下输入是有效的：

- [1 4 8 12]
- [MyColors.Red, MyColors.Blue] -->

**依存关系：**将**首个输入传递条件**设置为 “u2 ~= 0” 将禁用此参数。

</div>
</div>




<!-- #### 编程用法

| **模块参数**：Threshold |
| ------------------------- |
| **类型：**字符向量        |
| **值：**标量              |
| **默认值：**'0'         | -->



<!-- ### 启用过零检测 — 启用过零检测 on （默认） | off



选择此项以启用过零检测。有关详细信息，请参阅[过零检测](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/zero-crossing-detection.html)。

#### 编程用法

| **模块参数**：ZeroCross    |
| ---------------------------- |
| **类型**：字符向量 \| 字符串 |
| **值**：'off' | 'on'     |
| **默认值**：'on'           | -->

### 信号属性

单击**显示数据类型帮助**按钮 <img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/DataStoreMemory/DataStoreMemory_button.png')" style="width: 80px; height: auto; vertical-align:middle; display:inline; margin:0;"> 
<!-- ![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/show_data_type_asst_button.png)  -->
以显示**数据类型帮助**，帮助您设置数据类型属性。
<!-- 有关详细信息，请参阅[使用数据类型助手指定数据类型](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/specify-data-types-using-data-type-assistant.html)。 -->



<!-- ### 要求所有数据端口输入具有相同的数据类型 — 要求数据端口具有相同的数据类型 off （默认） | on



要求所有数据输入具有相同的数据类型。

#### 编程用法

| **模块参数**：InputSameDT |
| --------------------------- |
| **类型：**字符向量          |
| **值：'off' | 'on'**    |
| **默认值：**'off'         | -->



<!-- ### 输出最小值 — 范围检查的最小输出值 [] （默认） | 标量



Simulink® 检查的输出范围的下限值。

Simulink 使用最小值执行下列操作：

- 某些模块的参数范围检查（请参阅[指定模块参数的最小值和最大值](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/checking-parameter-values.html)）。
- 仿真范围检查（请参阅[指定信号范围](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/signal-ranges.html)和[启用仿真范围检查](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/signal-ranges.html#brdikvq)）。
- 定点数据类型的自动定标。
- 从模型生成的代码的优化。此优化可删除算法代码，并影响某些仿真模式（如 SIL 或外部模式）的结果。有关详细信息，请参阅[Optimize using the specified minimum and maximum values](https://ww2.mathworks.cn/help/releases/R2022b/ecoder/ref/optimizeusingthespecifiedminimumandmaximumvalues.html) (Embedded Coder)。





**注意**

**输出最小值**不会饱和或剪切实际输出信号。请改用 [Saturation](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/saturation.html) 模块。



#### 编程用法

| **模块参数**：OutMin |
| ---------------------- |
| **类型**：字符向量     |
| **值**：'[ ]'\| 标量 |
| **默认值**：'[ ]'    | -->



<!-- ### 输出最大值 — 范围检查的最大输出值 [] （默认） | 标量



Simulink 检查的输出范围的上限值。

Simulink 使用最大值执行下列操作：

- 某些模块的参数范围检查（请参阅[指定模块参数的最小值和最大值](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/checking-parameter-values.html)）。
- 仿真范围检查（请参阅[指定信号范围](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/signal-ranges.html)和[启用仿真范围检查](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/signal-ranges.html#brdikvq)）。
- 定点数据类型的自动定标。
- 从模型生成的代码的优化。此优化可删除算法代码，并影响某些仿真模式（如 SIL 或外部模式）的结果。有关详细信息，请参阅[Optimize using the specified minimum and maximum values](https://ww2.mathworks.cn/help/releases/R2022b/ecoder/ref/optimizeusingthespecifiedminimumandmaximumvalues.html) (Embedded Coder)。





**注意**

**输出最大值**不会饱和或剪切实际输出信号。请改用 [Saturation](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/saturation.html) 模块。



#### 编程用法

| **模块参数**：OutMax |
| ---------------------- |
| **类型**：字符向量     |
| **值**：'[ ]'\| 标量 |
| **默认值**：'[ ]'    | -->


<div class="details-box">
<details open>
<summary>输出数据类型 — 输出数据类型<div>“Inherit: internalRule” （默认） | “Inherit: backPropagation” | “Inherit: sameAsFirstInput” | “double” | “float” | “int8” | “uint8” | “int16” | “uint16” | “int32” | “uint32” | “boolean” | “fixdt(1,16,0)” | “fixdt(1,16,2^0,0)” | “fixdt(1,16,1.0,0,0.0)”</div></summary>
</details>
<div class="details-content">

指定输出数据类型。

- “Inherit: internalRule”

  使用以下规则确定输出数据类型。第一个输入端口的数据类型输出数据类型大于第三个输入端口的正数范围从第一个输入端口继承等于第三个输入端口的正数范围从第三个输入端口继承具有比第三个输入端口更小的正数范围是布尔值，第三个输入端口是 uint8是 uint8，第三个输入端口是布尔值是布尔值，另一个是 int8设置为布尔值是 uint8，另一个是布尔值两个输入端口的数据类型输出数据类型一个输入类型为布尔值，另一个是 uint8设置为第三个数据端口的数据类型一个输入是布尔值，另一个是 int8设置为布尔值。

- “Inherit: backPropagation”

  使用驱动模块的数据类型。

- “Inherit: sameAsFirstInput”

  使用第一个数据输入端口的数据类型。

- “double”

  指定输出数据类型为 double。

- “float”

  指定输出数据类型为 float。

- “half”

  指定输出数据类型为 half。

- “int8”

  指定输出数据类型为 int8。

- “uint8”

  指定输出数据类型为 uint8。

- “int16”

  指定输出数据类型为 int16。

- “uint16”

  指定输出数据类型为 uint16。

- “int32”

  指定输出数据类型为 int32。

- “uint32”


- “boolean”

  指定输出数据类型为 boolean。


<!-- - “int64”

  指定输出数据类型为 int64。

- “uint64”

  指定输出数据类型为 uint64。 -->

- “fixdt(1,16,0)”

  指定输出数据类型为定点 fixdt(1,16,0)。

- “fixdt(1,16,2^0,0)”

  指定输出数据类型为定点 fixdt(1,16,2^0,0)。

- “fixdt(1,16,1.0,0,0.0)”

  指定输出数据类型为定点 fixdt(1,16,1.0,0,0.0)。

</div>
</div>


  

<!-- - “Enum: <class name>”

  使用枚举数据类型，例如 Enum: BasicColors。 -->

<!-- - “Simulink.ImageType(480,640,3)”

  如果您有 Computer Vision Toolbox™，请使用 [Simulink.ImageType](https://ww2.mathworks.cn/help/releases/R2022b/vision/ref/simulink.imagetype.html) (Computer Vision Toolbox) 对象。 -->

<!-- - “字符串”

  指定输出数据类型为字符串。 -->

<!-- - “<data type expression>”

  使用数据类型对象，例如 “Simulink.NumericType”。 -->



<!-- #### 提示

如果输出是枚举类型，则两个数据输入必须使用与输出相同的枚举类型。 -->

<!-- #### 编程用法

| **模块参数**：OutDataTypeStr                               |
| ------------------------------------------------------------ |
| **类型**：字符向量                                           |
| **值**：'Inherit: Inherit via internal rule | 'Inherit: Inherit via back propagation' | 'Inherit: Same as first input' | 'double' | 'single' | 'half' | 'int8' | 'uint8' | 'int16' | 'uint16', 'int32' | 'uint32' | 'int64' | 'uint64' | 'fixdt(1,16)' | 'fixdt(1,16,0)' | 'fixdt(1,16,2^0,0)' | Enum: <class name> | Simulink.ImageType(480,640,3) | 'string' | '<data type expression>' |
| **默认值**：'Inherit: Inherit via internal rule'           | -->



<!-- ### 锁定数据类型设置以防止被定点工具更改 — 防止定点工具覆盖数据类型 off （默认） | on



选择此参数可防止定点工具覆盖您对此模块指定的数据类型。有关详细信息，请参阅[Lock the Output Data Type Setting](https://ww2.mathworks.cn/help/releases/R2022b/fixedpoint/ug/configuring-blocks-with-fixed-point-output.html#f25236) (Fixed-Point Designer)。

#### 编程用法

| **模块参数**：LockScale |
| ------------------------- |
| **类型：**字符向量        |
| **值：**'off' | 'on'    |
| **默认值：**'off'       | -->



<!-- ### 整数舍入模式 — 指定定点运算的舍入模式 “向下” （默认） | “向上” | “收敛” | “最邻近值” | “舍入” | “最简” | “零”



选择下列舍入模式之一。

- “向上”

  将正值和负值朝正无穷方向舍入。等同于 MATLAB ceil 函数。

- “收敛”

  将数值舍入到最邻近的可表示值。如果出现结值，则舍入到最邻近的偶数整数。等同于 Fixed-Point Designer™ convergent 函数。

- “向下”

  将正值和负值朝负无穷方向舍入。等同于 MATLAB floor 函数。

- “最邻近值”

  将数值舍入到最邻近的可表示值。如果出现结值，则朝正无穷方向舍入。等同于 Fixed-Point Designer nearest 函数。

- “舍入”

  将数值舍入到最邻近的可表示值。如果出现结值，则将正数朝正无穷方向舍入，将负数朝负无穷方向舍入。等同于 Fixed-Point Designer round 函数。

- “最简”

  自动选择是向负无穷大方向舍入还是向零舍入，以生成尽可能有效的舍入代码。

- “零”

  将数值向零舍入。等同于 MATLAB fix 函数。



#### 编程用法

| **模块参数**：RndMeth                                      |
| ------------------------------------------------------------ |
| **类型**：字符向量                                           |
| **值**：'Ceiling' | 'Convergent' | 'Floor' | 'Nearest' | 'Round' | 'Simplest' | 'Zero' |
| **默认值**：'Floor'                                        |

#### 另请参阅

有关详细信息，请参阅[舍入](https://ww2.mathworks.cn/help/releases/R2022b/fixedpoint/ug/rounding.html) (Fixed-Point Designer)。 -->



<!-- ### 对整数溢出进行饱和处理 — 溢出操作的方法 off （默认） | on



指定对溢出是进行饱和处理还是绕回处理。

- off - 溢出将绕回到数据类型可以表示的合适值。

  例如，数字 130 不适合一个有符号的 8 位整数，因此绕回 -126。

- on - 将溢出饱和处理为数据类型能够表示的最小值或最大值。

  例如，一个有符号的 8 位整数的溢出可以饱和处理为 -128 或 127。



**提示**

- 如果您的模型存在可能的溢出，而您希望在生成的代码中进行显式饱和保护，请考虑选中此复选框。

- 如果您希望优化生成的代码的效率，请考虑清除此复选框。

  清除此复选框还可以帮助您避免过度地指定信号超出范围时的处理方式。有关详细信息，请参阅[信号范围错误故障排除](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/signal-ranges.html#brdiku9)。

- 如果选中此复选框，饱和将应用于模块中的每个内部操作，而不仅仅应用于输出或结果。

- 一般情况下，代码生成进程可以检测到何时不可能发生溢出。在这种情况下，代码生成器不会生成饱和代码。

#### 编程用法

| **模块参数**：SaturateOnIntegerOverflow |
| ----------------------------------------- |
| **类型：**字符向量                        |
| **值：**'off' | 'on'                    |
| **默认值：**'off'                       | -->


<div class="details-box">
<details open>
<summary>允许不同数据输入大小 — 允许不同数据输入大小<div>off （默认） | on</div></summary>
</details>
<div class="details-content">

选中此复选框将允许输入信号具有不同大小。模块将输入信号大小传播到输出信号。如果两个数据输入都是可变大小信号，信号的最大大小可以相同，也可以不相同。

</div>
</div>




<!-- #### 编程用法

| **模块参数**：AllowDiffInputSizes |
| ----------------------------------- |
| **类型：**字符向量                  |
| **值：**'on' | 'off'            |
| **默认值：**'off'                 | -->



<!-- ## 模块特性

| **数据类型**     | Boolean | bus | double | enumerated | fixedPoint | half | integer | single | string |
| ---------------- | ------------------------------------------------------------ |
| **直接馈通**     | 是                                                         |
| **多维信号**     | 是                                                         |
| **可变大小信号** | 是                                                         |
| **过零检测**     | 是                                                         | -->


## 版本历史记录

- 在 2024b 之前推出

### 限制信息

1. 暂不支持启动过零检测的功能；  
2. 暂不支持要求所有数据端口输入具有相同的数据类型的复选框；  
3. 暂不支持设定输出的最大、最小值；  
4. 暂不支持设定为 int64、uint64、`Enum: <class name>`、字符串和 `<data type expression>` 的输出数据类型；  
5. 暂不支持锁定数据类型设置以防止被定点工具更改的复选框；  
6. 暂不支持设定整数舍入模式的功能；  
7. 暂不支持对整数溢出进行饱和处理的复选框；  
8. 控制信号暂不支持 half、int64、uint64、bus 和 image 的数据类型，输入和输出信号暂不支持 half、int64、uint64 和 imag 的数据类型。

<!-- ## 扩展功能



### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。

生成的代码在特定条件下依赖于 memcpy 或 memset 函数 (string.h)。



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 Verilog 代码和 VHDL 代码。

HDL Coder™ 提供影响 HDL 实现和综合逻辑的额外配置选项。



**HDL 架构**

此模块具有一个默认 HDL 架构。

**HDL 模块属性**

| **ConstrainedOutputPipeline** | 通过移动设计中现有延迟的方式来放置在输出端的寄存器的数量。分布式流水线处理不会重新分发这些寄存器。默认值为 0。有关详细信息，请参阅[ConstrainedOutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#btp8gmp) (HDL Coder)。 |
| ----------------------------- | ------------------------------------------------------------ |
| **InputPipeline**             | 要在生成的代码中插入的输入流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 0。有关详细信息，请参阅[InputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-25) (HDL Coder)。 |
| **OutputPipeline**            | 要在生成的代码中插入的输出流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 0。有关详细信息，请参阅[OutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-26) (HDL Coder)。 |

**复数数据支持**

此模块支持复信号的代码生成。



### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。

## 版本历史记录

**在 R2006a 之前推出** -->

## 另请参阅

[MultiportSwitch](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SignalRouting/MultiportSwitch.html)
 <!-- | [Manual Switch](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/manualswitch.html) -->