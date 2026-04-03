# Delay
---
&nbsp;

按固定或可变采样周期延迟输入信号

- **库：** Sysblock / Discrete

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/delay/delay.png')" style="width: 100px; height: auto;">

## 描述

Delay 模块会在一段延迟之后再输出模块的输入。此模块根据**延迟长度**参数的值来确定延迟时间。此模块支持：

- 可变延迟长度
- 来自输入端口的初始条件的规范
- 用外部重置信号重置初始条件的状态
- 利用外部使能信号控制模块在每一时间步的执行

初始模块输出取决于几个因素，例如**初始条件**参数和仿真开始时间等。**外部重置**参数确定模块输出是否在触发时重置为初始条件。**显示使能端口**参数确定是否由外部使能信号控制每一时间步的模块执行。

### 使用外部使能信号时的行为

选中**显示使能端口**复选框将启用 Enable 端口。如果启用了使能端口，则该模块将按以下顺序运行：

1. 检查是否满足使能条件。
2. 如果启用了重置端口，将检查重置条件。
3. 执行 Delay 模块功能。

该模块通过 Enable 端口执行以下操作：

- 当出现第一个模块使能信号时，模块输出是初始条件值（x0）。
- 对于连续的使能信号，该模块取输入信号 u 的最后一个状态。
- 如果端口在仿真开始时未启用，则 Delay 模块输出 0。
- 在仿真期间，如果端口在启用后变为禁用，则该模块不执行并保持其最后值。


<!-- 暂无
### 可变大小支持

Delay 模块为可变大小信号提供下列支持：

- 数据输入端口 `u` 接受可变大小信号。其他输入端口不接受可变大小信号。
- 对于可变大小输入，输出端口与数据输入端口 `u` 具有相同的信号维度。

对可变大小信号应用的规则取决于 Delay 模块的输入处理模式。

| 输入处理模式               | 对可变大小信号的支持规则                                     |
| :------------------------- | :----------------------------------------------------------- |
| “`元素作为通道(基于采样)`” | 信号维度仅在启用模块时的状态重置期间发生变化。初始条件必须为标量。 |
| “`列作为通道(基于帧)`”     | 不支持                                                       | -->

<!-- ### 总线支持

Delay 模块为总线信号提供下列支持：

- 数据输入 `u1` 接受虚拟和非虚拟总线信号。除了输入端口 `x0`，其他输入端口不接受总线信号。
- 初始条件 `x0` 端口接受非虚拟总线信号。
- 对于总线输入，输出端口与数据输入端口 `u` 具有相同的总线类型。
- 总线使用：
  - 基于采样和基于帧的处理
  - 固定和可变延迟长度
  - 数组和环形缓冲区

要使用总线信号作为 Delay 模块的输入，请在对话框中或通过 `x0` 端口指定初始条件。对虚拟和非虚拟总线的支持取决于您指定的初始条件，以及**状态名称**参数是否为空。对于 `x0` 输入端口，仅支持非虚拟总线。

| 初始条件     | 状态名称             |                  |
| :----------- | :------------------- | ---------------- |
| 空           | 非空                 |                  |
| 零           | 支持虚拟和非虚拟总线 | 仅支持非虚拟总线 |
| 非零标量     | 支持虚拟和非虚拟总线 | 不支持总线       |
| 非标量       | 不支持总线           | 不支持总线       |
| 结构体       | 支持虚拟和非虚拟总线 | 仅支持非虚拟总线 |
| 非完全结构体 | 支持虚拟和非虚拟总线 | 仅支持非虚拟总线 | -->

<!--暂无 
### 字符串支持

仅在以下情况下，Delay 模块才能接受和输出字符串数据类型：

- 模块配置为采用**初始条件**参数的默认值 (0)。
- **延迟长度**值等于或小于 1。 -->

## 示例

创建一个 sineWave 模块输出正弦波，将 delay 模块延迟长度设置为 50，从结果可以看到输出延迟了。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/Delay.mo">Delay.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/delay/delay01.png') " style="width: 600px; height: auto;">

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/delay/delay02.png')" style="width: 600px; height: auto;">


## 端口

<div class="details-box">
<details open>
<summary>u — 数据输入信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

根据参数设置延迟的输入数据信号。

**数据类型：**  float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | Boolean | fixed point | bus 

</div>
</div>

<div class="details-box">
<details open>
<summary>d — 延迟长度<div>标量</div></summary>
</details>
<div class="details-content">

指定为从输入端口继承的延迟长度。当您对**延迟长度:源**参数选择**外部输入**时启用。

**数据类型：**  float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | fixed point 

</div>
</div>

<div class="details-box">
<details open>
<summary>Enable — 外部使能信号<div>标量</div></summary>
</details>
<div class="details-content">

使能信号，用于启用或禁用模块的执行。要创建此端口，请选择**显示使能端口**参数。


**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | Boolean | fixed point 

</div>
</div>

<div class="details-box">
<details open>
<summary>External reset — 外部重置信号<div>标量</div></summary>
</details>
<div class="details-content">

将模块的执行重置为初始状态的外部信号。要创建此端口，请选择**外部重置**参数。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | Boolean | fixed point 

</div>
</div>

<div class="details-box">
<details open>
<summary>x0 — 初始条件<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

指定为从输入端口继承的初始条件。当您对**初始条件:源**参数选择**外部输入**时启用。


**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | fixed point | bus 

</div>
</div>

### 输出

</div>
</div>

<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

输出信号，它是按参数**延迟长度**指定的时间长度延迟后的输入信号。输出信号的初始值取决于几个条件。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | Boolean | fixed point | bus

</div>
</div>

## 参数
### 常设

<div class="details-box">
<details open>
<summary>延迟长度 — 延迟长度<div>内部输入 （默认） | “输入端口”</div></summary>
</details>
<div class="details-content">

指定是直接在对话框中输入延迟长度（固定延迟），还是从输入端口继承（可变延迟）。

- 如果将**源**设置为**内部输入**，请在**值**下面的编辑框中输入延迟长度。
- 如果将**源**设置为**外部输入**，请验证上游信号为 `d` 输入端口提供了延迟长度。您还可以通过指定参数**上限**来指定其最大值。

将标量延迟长度指定为非负实数整数。如果对话框中的值（固定延迟）超出范围或者为非整数，将返回错误。如果来自输入端口的值（可变延迟）超出范围，将被转换为位于范围之内的值。如果来自输入端口的值（可变延迟）为非整数，将截断为整数。

<!-- 
#### 编程用法

| **模块参数**：`延迟长度来源`   |
| ----------------------------------- |
| **类型**：字符向量                  |
| **值**：`'内部输入'` | `'外部输入'` |
| **默认值**：`'内部输入'`              |

| **模块参数**：`延迟长度` |
| --------------------------- |
| **类型**：字符向量          |
| **值**：标量                |
| **默认值**：`'2'`           |

| **模块参数**：`延迟长度上限` |
| ------------------------------------- |
| **类型**：字符向量                    |
| **值**：标量                          |
| **默认值**：`'100'`                   | -->

</div>
</div>


<div class="details-box">
<details open>
<summary>初始条件 — 初始条件<div>内部输入（默认） | “输入端口”</div></summary>
</details>
<div class="details-content">

指定是直接在对话框中输入初始条件，还是从输入端口继承初始条件。

- 如果将**源**设置为**内部输入**，请在**值**下面的编辑框中输入初始条件。
- 如果将**源**设置为**外部输入**，请验证上游信号为 `x0` 输入端口提供了初始条件。

使用舍入到最邻近值运算和饱和处理，将**初始条件**的数据类型脱机转换为输入信号 `u` 的数据类型。


<!-- 
#### 编程用法

| **模块参数**：`初始条件来源` |
| -------------------------------------- |
| **类型**：字符向量                     |
| **值**：`'内部输入'` | `'外部输入'`    |
| **默认值**：`'内部输入'`                 |

| **模块参数**：`初始条件` |
| -------------------------------- |
| **类型**：字符向量               |
| **值**：标量                     |
| **默认值**：`'0'`              | -->

</div>
</div>


<!--暂无
<div class="details-box">
<details open>
<summary>输入处理 — 指定基于采样或基于帧的处理<div>“元素作为通道(基于采样)” （默认） | “列作为通道(基于帧)”</div></summary>
</details>
<div class="details-content">

指定模块是执行基于采样还是基于帧的处理：

- “`列作为通道(基于帧)`” - 将输入信号的每一列视为一个单独的通道（基于帧的处理）。

::: warning 注意 
基于帧的处理需要具有 DSP System Toolbox™ 许可证。

有关详细信息，请参阅[Sample- and Frame-Based Concepts](https://ww2.mathworks.cn/help/releases/R2022b/dsp/ug/sample-and-frame-based-concepts.html) (DSP System Toolbox)。
:::  

- “`元素作为通道(基于采样)`” - 将输入信号的每个元素视为一个单独的通道（基于采样的处理）。

可以使用**输入处理**指定模块是执行基于采样的处理还是基于帧的处理。有关这两种处理模式的详细信息，请参阅[Sample- and Frame-Based Concepts](https://ww2.mathworks.cn/help/releases/R2022b/dsp/ug/sample-and-frame-based-concepts.html) (DSP System Toolbox)。

#### 编程用法

| **模块参数**：`InputProcessing`                              |
| ------------------------------------------------------------ |
| **类型**：字符向量                                           |
| **值**：`'Columns as channels (frame based)'` | `'Elements as channels (sample based)'` |
| **默认值**：`'Elements as channels (sample based)'`          |

</div>
</div>
-->


<!--暂无
<div class="details-box">
<details open>
<summary>使用环形缓冲区保存状态 — 存储状态的环形缓冲区<div>off （默认） | on</div></summary>
</details>
<div class="details-content">

选择在仿真和代码生成时使用环形缓冲区来存储状态。在其他情况下，则使用数组缓冲区来存储状态。

当延迟长度值很大时，使用环形缓冲区可以提高执行速度。对于数组缓冲区，复制操作的数量随着延迟长度的增加而增加。对于环形缓冲区，不管延迟长度如何增加，复制操作的数量保持不变。

如果符合下列任一条件，都应使用数组缓冲区来存储状态，因为环形缓冲区不会提高执行速度。

- 对于基于采样的信号，延迟长度为 1。
- 对于基于帧的信号，延迟长度不大于帧大小。

#### 编程用法

| **模块参数**：`UseCircularBuffer` |
| --------------------------------- |
| **类型**：字符向量                |
| **值**：`'off'` | `'on'`          |
| **默认值**：`'off'`               |

</div>
</div>
-->

<!--
<div class="details-box">
<details open>
<summary>防止直接馈通 — 防止直接馈通<div>off （默认） | on</div></summary>
</details>
<div class="details-content">

对于**输入处理**模式，选择此项可将延迟长度从零增加到下限值。

- 对于基于采样的信号，将最小延迟长度增加到 1。
- 对于基于帧的信号，将最小延迟长度增加到帧的长度。

选中此复选框可防止从输入端口 `u` 到输出端口的直接馈通。但是，此复选框无法阻止从初始条件端口 `x0` 到输出端口的直接馈通。

#### 依存关系

要启用此参数，请将**延迟长度:源**设置为“`输入端口`”时，此复选框可用。

#### 编程用法

| **模块参数**：`PreventDirectFeedthrough` |
| ---------------------------------------- |
| **类型**：字符向量                       |
| **值**：`'off'` | `'on'`                 |
| **默认值**：`'off'`                      |

</div>
</div>
-->

<!--暂无
<div class="details-box">
<details open>
<summary>在生成代码中去除延迟长度检查 — 删除延迟长度超出范围检查<div>off （默认） | on</div></summary>
</details>
<div class="details-content">

选择此选项可删除用来检查超出范围的延迟长度的代码。

| 复选框 | 结果                                                     | 何时使用                       |
| :----- | :------------------------------------------------------- | :----------------------------- |
| 选中   | 生成的代码中未包含用来检查超出范围的延迟长度的条件语句。 | 提高代码效率                   |
| 清除   | 生成的代码中包含检查超范围延迟长度的条件语句。           | 适用于安全性至关重要的应用领域 |

#### 依存关系

要启用此参数，请将**延迟长度:源**设置为“`输入端口`”时，此复选框可用。

#### 编程用法

| **模块参数**：`RemoveDelayLengthCheckInGeneratedCode` |
| ----------------------------------------------------- |
| **类型**：字符向量                                    |
| **值**：`'off'` | `'on'`                              |
| **默认值**：`'off'`                                   |

</div>
</div>
-->

<!--暂无
<div class="details-box">
<details open>
<summary>延迟长度的诊断 — 延迟长度的诊断检查<div>无” （默认） | “警告” | “错误”</div></summary>
</details>
<div class="details-content">

指定当输入 `d` 小于下限或大于**延迟长度:上限**时是否生成警告或错误。下限取决于**防止直接馈通**的设置。

- 如果清除此复选框，则下限为零。
- 如果选中此复选框，对于基于采样的信号，下限为 1；对于基于帧的信号，下限为帧的长度。

诊断选项包括：

- `None` - Simulink 软件不执行任何操作。
- `Warning` - Simulink 软件显示警告并继续进行仿真。
- `Error` - Simulink 软件终止仿真并显示错误。

#### 依存关系

要启用此参数，请将**延迟长度:源**设置为“`输入端口`”时，此复选框可用。

#### 编程用法

| **模块参数**：`DiagnosticForDelayLength`   |
| ------------------------------------------ |
| **类型**：字符向量                         |
| **值**：`'None'` | `'Warning'` | `'Error'` |
| **默认值**：`'None'`                       |

</div>
</div>
-->


<div class="details-box">
<details open>
<summary>显示使能端口 — 创建使能端口<div>off （默认） | on</div></summary>
</details>
<div class="details-content">

此选项使用使能端口来控制此模块的执行。当此端口的输入非零时，模块被视为启用；当输入为 0 时，模块被视为禁用。输入的值在执行模块的同一时间步进行检查。

<!-- 
#### 编程用法

| **模块参数**：`显示使能端口` |
| ------------------------------ |
| **类型：**字符向量             |
| **值：**`'off' | 'on'`         |
| **默认值：**`'off'`            | -->

</div>
</div>

<div class="details-box">
<details open>
<summary>外部重置 — 外部状态重置<div>“无” （默认） | “上升沿” | “下降沿” | “任一沿” | “电平” | “电平保持”</div></summary>
</details>
<div class="details-content">

指定用于将状态重置为初始条件的触发事件。

| 重置模式     | 行为                                                         |
| :----------- | :----------------------------------------------------------- |
| `无`       | 不重置。                                                     |
| `上升沿`   | 在上升边重置。                                               |
| `下降沿`   | 在下降边重置。                                               |
| `任一沿`   | 在上升或下降边重置。                                         |
| `电平`     | 在下列任一情况下重置：当重置信号在当前时间步为非零值时当重置信号值从上一时间步的非零更改为当前时间步的零时 |
| `电平保持` | 当重置信号在当前时间步为非零值时重置                         |

<!-- 
#### 编程用法

| **模块参数**：`外部重置`                                |
| ------------------------------------------------------------ |
| **类型**：字符向量                                           |
| **值**：`'不重置'` \| `'上升沿'` \| `'下降沿'` \| `'任一沿'` \| `'电平'` \| `'电平保持'` |
| **默认值**：`'不重置'`                                         | -->

</div>
</div>


<div class="details-box">
<details open>
<summary>采样时间（-1 表示继承） — 采样时间命中点之间的离散间隔<div>-1 （默认） | scalar</div></summary>
</details>
<div class="details-content">

指定采样时间间隔，要继承采样时间，请将此参数设置为 -1。此模块支持离散采样时间，但不支持连续采样时间。

<!-- 
#### 编程用法

| **模块参数**：`采样时间` |
| -------------------------- |
| **类型**：字符向量         |
| **值**：实数标量           |
| **默认值**：`'-1'`         | -->

</div>
</div>


<!-- ### 状态属性 -->

<!--暂无
<div class="details-box">
<details open>
<summary>状态名称 — 模块状态的唯一名称<div>'' （默认） | 字母数字字符串</div></summary>
</details>
<div class="details-content">

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

</div>
</div>
-->

<!--暂无
<div class="details-box">
<details open>
<summary>状态名称必须解析为 Simulink 信号对象 — 要求将状态名称解析为信号对象<div>off （默认） | on</div></summary>
</details>
<div class="details-content">

选中此复选框会要求将状态名称解析为 Simulink 信号对象。

#### 依存关系

要启用此参数，请为**状态名称**指定值。仅当将模型配置参数**信号解析**设置为除“`无`”以外的值时，才会显示此参数。

#### 编程用法

| **模块参数**：`StateMustResolveToSignalObject` |
| ---------------------------------------------- |
| **类型：**字符向量                             |
| **值：**`'off' | 'on'`                         |
| **默认值：**`'off'`                            |

</div>
</div>
-->

<!-- ## 模块特性 -->

<!--暂无
| **数据类型**     | `Boolean` | `bus` | `double` | `enumerated` | `fixed point` | `half` | `integer` | `single` | `string` |
| ---------------- | ------------------------------------------------------------ |
| **直接馈通**     | `是`                                                         |
| **多维信号**     | `是`                                                         |
| **可变大小信号** | `是`                                                         |
| **过零检测**     | `否`                                                         |
-->

<!-- ## 扩展功能 -->



<!-- ### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。
 
生成的代码在特定条件下依赖于 `memcpy` 或 `memset` 函数 (`string.h`)。



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 Verilog 代码和 VHDL 代码。 -->

<!-- 

HDL Coder™ 提供影响 HDL 实现和综合逻辑的配置选项。

| 模块参数设置                                                 | 描述                                                         |
| :----------------------------------------------------------- | :----------------------------------------------------------- |
| 将**外部重置**设置为“`电平`”。                               | 在 HDL 代码中生成重置端口。                                  |
| 选择**显示使能端口**。                                       | 在 HDL 代码中生成使能端口。                                  |
| 对于**初始条件**，将**源**设置为“`对话框`”，并输入值。       | 指定模块的初始条件。                                         |
| 将**输入处理**设置为“`列作为通道(基于帧)`” 或“`元素作为通道(基于采样)`”。 | 需要向量输入数据，其中向量的每个元素表示一个时间点上的采样。 |

**使用 State Control 模块时的附加设置**

如果您要在一个 Simulink 模型子系统中结合使用 State Control 模块和 Delay 模块，请使用以下附加设置。

| 模块参数设置                                                 | 描述                                                        |
| :----------------------------------------------------------- | :---------------------------------------------------------- |
| 将“`同步`”模式下的**外部重置**设置为“`电平保持`”，并设置 State Control 模块的“`典型`”模式的“`电平`”。 | 在 HDL 代码中生成重置端口。                                 |
| 对于具有外部使能端口的 Delay 模块，将**延迟长度**设置为零。  | 仅在 State Control 模块的“`同步`”模式下视为一条线。         |
| 对于具有外部重置端口的 Delay 模块，将**延迟长度**设置为零。  | 在 State Control 模块的“`同步`”和“`典型`”模式下视为一条线。 |

有关 State Control 模块的详细信息，请参阅[State Control](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ref/statecontrol.html) (HDL Coder)。

**HDL 架构**

此模块具有一个默认 HDL 架构。

**HDL 模块属性**

| **InputPipeline**  | 要在生成的代码中插入的输入流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 `0`。有关详细信息，请参阅[InputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-25) (HDL Coder)。 |
| ------------------ | ------------------------------------------------------------ |
| **OutputPipeline** | 要在生成的代码中插入的输出流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 `0`。有关详细信息，请参阅[OutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-26) (HDL Coder)。 |
| **ResetType**      | 隐藏重置逻辑生成。默认值为“`默认`”，它生成重置逻辑。另请参阅[ResetType](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-27) (HDL Coder)。 |
| **UseRAM**         | 将延迟映射到 RAM 而不是寄存器。默认值为 “`off`”。另请参阅[UseRAM](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bs04098) (HDL Coder)。 |

**可变整数延迟支持**

- 您可以为通过“`输入端口`”设置**延迟长度**的 Delay 模块生成 HDL 代码。输入延迟长度可以是整数类型或浮点类型。
- 代码生成在 Delay 模块的 'd' 端口支持正整数值。通过输入端口设置的延迟长度必须在 `0` 和 `Upper limit` 之间，在“模块参数”对话框中指定。
- 对于负延迟长度值，HDL Coder 将这些负延迟长度转换为 `0`。
- 同样，如果您指定的延迟长度大于上限，HDL Coder 会将延迟长度转换为 `Upper limit` 值。
- 上限范围由延迟长度输入数据类型的范围定义。例如，如果将延迟长度输入数据类型指定为 `uint8`，则上限不能超过 `255`。
- 对于 Variable Integer Delay 模块，您可以使用使能端口和重置端口。

**复数数据支持**

此模块支持复信号的代码生成。

**限制**



- 对于**初始条件**，HDL 代码生成不支持将**源**设置为“`输入端口`”。
- HDL 代码生成仅在重置端口和使能端口上支持布尔数据类型。
- 通过“`输入端口`”设置**延迟长度**的 Delay 模块不支持 RAM 映射的 HDL 模块属性 **UseRAM**。


 -->


<!-- ### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。 -->



## 版本历史记录

- 在 2024b 之前推出

### 限制信息
不支持部分
1. 描述-字符串支持
2. 描述-可变大小支持
3. 参数-常设-输入处理 — 指定基于采样或基于帧的处理
4. 参数-常设-使用环形缓冲区保存状态 — 存储状态的环形缓冲区
5. 参数-常设-防止直接馈通 — 防止直接馈通
6. 参数-常设-在生成代码中去除延迟长度检查 — 删除延迟长度超出范围检查
7. 参数-常设-延迟长度的诊断 — 延迟长度的诊断检查
8. 参数-状态属性-状态名称 — 模块状态的唯一名称
9. 参数-状态属性-状态名称必须解析为信号对象 — 要求将状态名称解析为信号对象


## 另请参阅

[UnitDelay](UnitDelay.html) | [TappedDelay](TappedDelay.html)

<!-- ### 主题 -->

