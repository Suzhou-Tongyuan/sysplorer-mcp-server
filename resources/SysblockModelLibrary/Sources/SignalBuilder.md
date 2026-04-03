# SignalBuilder
---
创建和生成可互换的分段线性波形信号组

<!-- **不推荐使用 Signal Builder 模块。请改用 [Signal Editor](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/signaleditorblock.html) 模块。** -->

**库：** Sysblock模块库 / Sources

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/SignalBuilder/SignalBuilder.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

SignalBuilder 模块允许您创建可交替的分段线性信号源组，并在模型中使用。您可以快速将信号组切换入模型或切换出模型，以便于测试。在信号构建器窗口中，创建信号并定义输出波形。要打开该窗口，请双击模块。

### 数据导入

数据导入对话框支持 CSV 格式文件（`.csv`）和 MAT 格式文件：

CSV 格式文件需要满足以下要求：

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/SignalBuilder/SignalBuilder_import.png')" style="width: 500px; border:solid 1px black;">

- 变量名必须以字母和下划线开头，并且只能包含字母、数字和下划线。
- 变量名之间不能重名。
- 变量名不能与内置关键字重名，请参阅[组件命名不可使用的关键字](/Doc/Sysblock/SysblockBasic/InteractiveModelEditing/unuseablekeywordinfunction.md)。
- 时刻点必须是浮点型数值，不能小于 0 ，且下一个时刻点不能小于上一个时刻点。
- 变量值必须是浮点型数值或为空，为空则保持前一个有效值，如果没有前一个有效值则为 0 。

<!-- 请参阅 [信号组](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/working-with-signal-groups.html)。 -->

MAT 格式文件需要满足以下需求：

- Matlab 中导出的 MAT 文件，仅支持工作区创建的数组格式数据，若是非数组格式数据，需要先转化成数组格式数据。
- Sysplorer 结果查看器导出的 MAT 文件数据可以直接导入到 SignalBuilder 中。

<!-- **注意**

可以使用 [signalbuilder](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/signalbuilder_cmd.html) 函数以编程方式创建和访问 Signal Builder 模块。 -->
## 示例

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/SignalBuilder.mo">SignalBuilder.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/SignalBuilder/SignalBuilder_ex.png')" style="width: 300px; ">

### 示例说明

- Scope 模块：用于显示模型的输出结果，即 SignalBuilder 模块生成的自定义信号。

- SignalBuilder 模块：创建和生成可互换的分段线性波形信号组，在示例中我们使用默认信号，如有需要，可以将曲线导出为`csv`文件或者将`csv`文件导入为曲线。

- 双击进入 SignalBuilder 模块后，单击数据导入，导入`csv`文件作为输出曲线，单击保存保存当前曲线为`csv`文件。

    <img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/SignalBuilder/inputoutput.png')" style="width: 500px;border:solid 1px black;">

## 端口

### 输出

<div class="details-box">
<details open>
<summary>Signal 1 — 第一个输出信号<div>标量</div></summary>
</details>
<div class="details-content">

来自 SignalBuilder 窗口中当前可见信号组的第一个输出信号。

**数据类型：** double

</div>
</div>


<div class="details-box">
<details open>
<summary>Signal n — 第 n 个输出信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

来自 SignalBuilder 窗口中当前可见的信号组的第 n 个输出信号。n 对应于信号索引。

**数据类型：** double

</div>
</div>



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

输出信号暂不支持 bus 的数据类型。

<!-- ## 扩展功能



### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。

## 版本历史记录

**在 R2006a 之前推出**



### R2019a: 不推荐使用 Signal Builder 模块 -->

<!-- ## 另请参阅

[Signal Editor](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/signaleditorblock.html) | [Subsystem, Atomic Subsystem, Nonvirtual Subsystem, CodeReuse Subsystem](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/subsystem.html) | [signalbuilder](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/signalbuilder_cmd.html) | [signalBuilderToSignalEditor](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/signalbuildertosignaleditor.html)

### 主题

- [Migrate from Signal Builder Block to Signal Editor Block](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/migrate-from-signal-builder-block-to-signal-editor-block.html)
- [信号组](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/working-with-signal-groups.html)
- [Load Data with Interchangeable Scenarios](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/load-data-with-interchangeable-scenarios.html)
- [信号基础知识](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/signal-basics.html) -->