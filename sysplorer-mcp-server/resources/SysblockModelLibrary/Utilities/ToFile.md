# ToFile
---
&nbsp;


将数据写入到文件


- **库：** Sysblock / Utilities

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/ToFile/1.png')" style="width: 100px; height: auto;">

## 描述

To File 模块将输入信号数据写入 CSV 文件。此模块以增量方式写入到输出文件中。如果仿真开始时已经存在输出文件，模块将覆盖该文件。暂停仿真或仿真完成时，文件会自动关闭。如果仿真异常终止，To File 模块将保存它在异常终止时间点之前记录的数据。

To File 模块图标会显示输出文件的名称。


## 示例

将 Sine 输出信号和 Constant 输出信号通过 Mux 模块组合，并输入给 ToFile 模块。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/ToFile.mo">ToFile.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/ToFile/2.png')" style="width: 600px; ">

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/ToFile/3.png')" style="width: 600px; border: 1px solid black;">


## 端口

### 输出

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 数组 | 矩阵 </div></summary>
</details>
<div class="details-content">

要存储在文件中的信号。每个采样都包含时间戳和相关数据值。数据可以是数组格式。

**数据类型：** double

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>数据名 — 用于保存数据的变量的名称<div>res.csv（默认）| CSV文件名或路径 </div></summary>
</details>
<div class="details-content">

指定用来存储输出的 CSV 文件的路径名或文件名。如果指定的文件名没有路径信息，会将文件存储在模块所在模型的路径下。如果文件存在，新文件将覆盖旧文件。


</div>
</div>

<div class="details-box">
<details open>
<summary>抽取 — 抽取因子<div>  1（默认） | 正整数 </div></summary>
</details>
<div class="details-content">

指定抽取因子以降低记录数据的有效采样率。对于抽取因子 n，ToWorkspace 模块记录每第 n 个采样值。例如，当抽取值指定为 2 时，ToWorkspace 模块每隔一个数据点记录一个采样。


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

<div id="生成表头" class="jump-target"></div>
<div class="details-box">
<details open>
<summary>生成CSV文件的表头<div>  true | false（默认） </div></summary>
</details>
<div class="details-content">

勾选该选项，在向C文件中写入数据前，会写入文件表头。

默认名称为与ToFile模块连接的组件名和端口名的组合，若存在信号线，则以信号线名称命名。若ToFile模块与Mux模块相连，则会以与Mux模块相连的组件名和端口名组合做为名称。

</div>
</div>

## 版本历史记录

- 在 2025a 推出

### 限制信息

- 暂且仅支持 double 类型数据。