# Display
---
显示输入的值

**库：** Sysblock模块库 / Utilities

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/Display/Display.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

Display 模块显示输入数据的值。您可以指定显示的频率。对于数值输入数据，您还可以指定显示的格式。

如果模块输入是数组，则您可以纵向或横向调整模块大小以显示更多元素，而不是只显示第一个元素。如果模块输入是向量，则模块从左到右、从上到下依次添加显示字段。模块会显示尽可能多的值。实心三角形表示模块并未显示所有的输入数组元素。

Display 模块显示向量信号的前 200 个元素，显示矩阵信号的前 20 行和前 10 列。


::: warning 注意 
如果您指定的数值显示格式不够大，无法显示值的所有位数，则显示的值可能会损失精度。结果取决于您的计算机硬件和操作系统。
:::


<!-- ### 显示缩写词

Display 模块上显示下列缩写词，以帮助您确定值的格式。

| 当您看到... | 显示的值为...                                               |
| :---------- | :---------------------------------------------------------- |
| (SI)      | 存储的整数值**注意**当信号是整数数据类型时，不显示 (SI)。 |
| hex       | 十六进制格式                                                |
| bin       | 二进制格式                                                  |
| oct       | 八进制格式                                                  |

### 显示字符串

使用字符串时，Display 模块显示：

- 带双引号的字符串。
- 将特殊字符显示为转义序列，例如换行符显示为 '\n'。
- 将不可显示的字符显示为转义八进制数，例如 '\201'。

如果输入信号是字符串类型，则**数值显示格式**参数的选择不影响字符串的显示。 -->

## 示例

<!-- [![自动气候控制系统仿真](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/simulatingautomaticclimatecontrolsystemsexample_01_zh_CN.png)自动气候控制系统仿真此示例说明如何使用 Simulink® 和 Stateflow® 对汽车中自动气候控制系统进行仿真。](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/simulating-automatic-climate-control-systems.html)

[![Sum Block Reorders Inputs](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink/win64/SumBlockReordersInputsExample_01.png)Sum Block Reorders InputsHow the Sum block reorders inputs.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/sum-block-reorders-inputs.html)

[![Scalar Expansion with the Coulomb and Viscous Friction Block](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink/win64/ScalarExpansionWithTheCoulombViscousFrictionBlockExample_01.png)Scalar Expansion with the Coulomb and Viscous Friction BlockA model with a scalar input to a Coulomb & Viscous Friction block that uses scalar expansion to output a vector.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/scalar-expansion-with-coulomb-and-viscous-friction.html) -->

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/Display.mo">Display.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/Display/Display_ex.png')" style="width: 300px; height: auto; transform: scale(0.8);">

### 示例说明

- Step 模块：提供从 0 步变到 1 的输入信号，用于模拟实际输入值的变化；
- Display 模块：用于在模型运行时显示输入信号的值。这个模块可以显示各种类型的数据，包括数值、字符串和 Bus 信号。在模型运行时，Display 模块会在结果查看器窗口中显示连接到它的信号的值。

## 端口

### 输入


###  
<div class="details-box">
<details open>
<summary>u — 输入数据<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

要显示的输入数据。

**数据类型：** float | double | half | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | enum


</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>数值显示格式 — 数值输入数据的显示格式<div>“short” （默认） | “long” | “short_e” | “long_e” | “货币格式” | “十六进制(存储整数)” | “二进制(存储整数)” | “十进制(存储整数)” | “八进制(存储整数)”</div></summary>
</details>
<div class="details-content">

指定数值数据的显示格式。

| 如果您选择...              | 模块显示...                                   |
| :------------------------- | :-------------------------------------------- |
| short                    | 具有固定十进制小数点的 5 位数定标值           |
| long                     | 具有固定十进制小数点的 15 位数定标值          |
| short_e                  | 具有浮动小数点的 5 位数值                     |
| long_e                   | 具有浮动小数点的 16 位数值                    |
| bank                     | 具有固定美元和美分格式的值（但没有 $ 或逗号） |
| hex (Stored Integer)     | 以十六进制格式存储的定点输入整数值            |
| binary (Stored Integer)  | 以二进制格式存储的定点输入整数值              |
| decimal (Stored Integer) | 以十进制格式存储的定点输入整数值              |
| octal (Stored Integer)   | 以八进制格式存储的定点输入整数值              |

</div>
</div>




<!-- 如果 Display 模块的数值输入具有枚举数据类型（请参阅[Simulink 枚举](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/about-simulink-enumerations.html)和[定义 Simulink 枚举](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/using-enumerated-data-in-simulink-models.html#brscgt1-1)）：

- 模块将显示枚举值，而非基础整数值。
- 将**数值显示格式**设置为任一 Stored Integer 设置将导致错误。

如果输入信号是字符串类型，则**数值显示格式**参数的选择不影响字符串的显示。

#### 编程用法

| **模块参数**：Format                                       |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值：**'short' | 'long' | 'short_e' | 'long_e' | 'bank' | 'hex (Stored Integer)' | 'binary (Stored Integer)' | 'decimal (Stored Integer)' | 'octal (Stored Integer)' |
| **默认值：**'short'                                        | -->



<!-- ### 抽取 — 显示速率 1 （默认） | integer



指定显示数据的频率。

显示的数据量和显示数据的时间步取决于**抽取**模块参数和 SampleTime 属性。

- **抽取**参数允许您显示间隔为 n 的每个样本数据，其中 n 是抽取因子。默认抽取因子 1 在每个时间步显示数据。

  

  **注意**

  Display 模块在初始时间更新显示，即使**抽取**值大于一也是如此。

- SampleTime 属性（可以使用 [set_param](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/set_param.html) 来设置）允许您指定显示点的采样间隔。使用时间步间隔不同的变步长求解器时，此属性很有用。默认采样时间 -1 导致模块在确定要显示的点时忽略采样间隔。

  

  **注意**

  如果模块继承采样时间 Inf，**抽取**参数将被忽略。

  

#### 编程用法

| **模块参数**：Decimation |
| -------------------------- |
| **类型：**字符向量         |
| **值：**'1' \| 整数      |
| **默认值：**'1'          | -->



<!-- ### 浮动显示 — 浮动显示 off （默认） | on



要使用此模块作为浮动显示，请选中**浮动显示**复选框。模块输入端口消失，模块显示选定信号线上的信号值。

如果您选择**浮动显示**：

- 关闭模型的信号存储重用。有关详细信息，请参阅 [Signal storage reuse](https://ww2.mathworks.cn/help/releases/R2022b/rtw/ref/signalstoragereuse.html) (Simulink Coder)。
- 不要将多维信号连接到浮动显示。

#### 编程用法

| **模块参数**：Floating |
| ------------------------ |
| **类型**：字符向量       |
| **值**：'on' | 'off' |
| **默认值**：'on'       | -->



<!-- ## 模块特性

| **数据类型**     | Boolean | double | enumerated | fixed point | half | integer | single | string |
| ---------------- | ------------------------------------------------------------ |
| **直接馈通**     | 是                                                         |
| **多维信号**     | 否                                                         |
| **可变大小信号** | 是                                                         |
| **过零检测**     | 否                                                         | -->


## 版本历史记录

- 在 2024b 之前推出

### 限制信息

1. 暂不支持设定显示的速率；  
2. 暂不支持浮动显示的复选框；  
3. 输入数据暂不支持 half、int64、uint64、string 和 fixedPoint 的数据类型。


<!-- ## 扩展功能



### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。

在代码生成中将被忽略。



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 Verilog 代码和 VHDL 代码。



此模块可用于生成 HDL 代码的子系统中的仿真可见性，但不包括在硬件实现中。



### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。

## 版本历史记录

**在 R2006a 之前推出** -->

## 另请参阅

[Scope](Scope.html)
 <!-- | [To File](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/tofile.html) | [To Workspace](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/toworkspace.html) -->