# ToWorkspace
---
&nbsp;


将数据从 Sysblock 模型记录到 Syslab 工作区


- **库：** Sysblock / Utilities

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/ToWorkspace/1.png')" style="width: 100px; height: auto;">

## 描述

ToWorkspace 模块将连接到其输入端口的数据从 Sysblock 模型记录到 Syslab 工作区。通常，记录的数据在基础工作区中返回。在仿真期间，记录的数据会流式传输到仿真数据检查器。当仿真暂停或停止时，记录的数据会写入工作区。

您可以使用 ToWorkspace 模块记录信号的数据。ToWorkspace 模块支持记录标量和多维数据。

您可以配置存储 ToWorkspace 模块所记录数据的变量的名称。您还可以通过指定模块或模型参数来控制 ToWorkspace 模块记录的值。

您可在**选项>环境>常规>目标 Syslab 工作区**[环境](/Doc/DevelopingModels/CustomizedEnvironment/Options.html#x6b1c95ad)，配置数据输出的目标工作区。

## 示例

将 Sine 输出信号和 Constant 输出信号通过 Mux 模块组合，并输入给 ToWorkspace 模块。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/ToWorkspace.mo">ToWorkspace.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/ToWorkspace/2.png')" style="width: 600px; ">

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/ToWorkspace/3.png')" style="width: 600px; border: 1px solid black;">


## 端口

### 输入

<div class="details-box">
<details open>
<summary>y — 输入信号<div>向量</div></summary>
</details>
<div class="details-content">

使用从 Syslab 工作区读取的指定变量创建的输出。根据您指定的维度，输出对应的向量。

**数据类型：** double | float | int8 | uint8 | int16 | uint16 | int32 | uint32  | int64 | uint64 | boolean

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>数据名 — 用于保存数据的变量的名称<div>simout（默认）| 变量名 </div></summary>
</details>
<div class="details-content">

为包含所记录数据的变量指定名称。默认情况下，ToWorkspace 模块将记录的数据保存在名为 simout 的变量中。当一个模型包含多个 To Workspace 模块时，每个模块的变量名称参数值必须是唯一的。

</div>
</div>

<div class="details-box">
<details open>
<summary>限制数据点数 — 最后保存的数据点数 <div>  inf（默认） | 正整数 </div></summary>
</details>
<div class="details-content">

指定抽限制数据点数以降低记录数据的数据规模。对于抽限制数据点数 n，ToWorkspace 模块记录每最后 n 个采样值。例如，当限制数据点数指定为 100 时，ToWorkspace 模块仅将最后 100 个数据传递到 Syslab 工作区。若限制数据点数超过仿真采样次数，则将该次仿真所有的仿真数据都传递到 Syslab 工作区。
限制数据点数支持使用基础工作区、模型工作区和数据字典中定义的参数。


</div>
</div>

<div class="details-box">
<details open>
<summary>抽取 — 抽取因子<div>  1（默认） | 正整数 </div></summary>
</details>
<div class="details-content">

指定抽取因子以降低记录数据的有效采样率。对于抽取因子 n，ToWorkspace 模块记录每第 n 个采样值。例如，当抽取值指定为 2 时，ToWorkspace 模块每隔一个数据点记录一个采样。

抽取因子支持使用基础工作区、模型工作区和数据字典中定义的参数。


</div>
</div>

<div class="details-box">
<details open>
<summary>采样时间 — 输出采样周期<div>  0 | 标量 </div></summary>
</details>
<div class="details-content">

采样时间参数指定模块在仿真期间计算新输出值的时间。

默认情况下，采样时间参数值为 -1，表示继承。对于离散信号，请将采样时间指定为离散采样间隔。例如，将采样时间指定为 0.1 以对每 100 毫秒采样一次的离散信号建模。将采样时间指定为 0 以表示没有时间偏移量的连续采样时间。


</div>
</div>

## 版本历史记录

- 在 2025a 推出

### 限制信息

- 仅支持标量、一维数组、行向量、列向量数据