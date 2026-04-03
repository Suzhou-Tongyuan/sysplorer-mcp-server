# FromFile
---
&nbsp;

将 CSV 或 MAT 文件中的数据加载到 Sysblock 模型中

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/FromFile/1.png')" style="width: 100px; height: auto;">

- **库：** Sysblock / Sources

## 描述

FromFile 模块用于将数据从 CSV 或 MAT 文件读入 Sysblock 模型，并以信号的形式进行输出。一个模型中可以包含多个 FromFile 模块，多个 FromFile 模块也可以从同一文件中读取数据。

FromFile 模块具有一个输出端口，用于输出模块所读入文件中的数据。您可以指定模块从文件中数据构造输出的方式，包括输出数据维度、输出采样时间、数据插值方法以及是否启用过零检测。

FromFile 模块图标显示所读入文件的相对路径（相对 Sysblock 工作目录的路径）。

例如如果从 Sysblock 工作目录上一级目录中读入文件 Data.csv，该模块将显示 ../Data.csv。

### CSV文件数据

FromFile 模块可以从 CSV 格式文件中加载数据，其中第一列为时间数据，后续列为标量或向量的信号数据。

| CSV文件数据要求 | 说明                                                         |
| --------------- | ------------------------------------------------------------ |
| 文件编码格式    | ·UTF-8 编码格式                                              |
| 时间数据要求    | ·时间数据值必须单调递增；<br>·时间数据值必须为有限值（不支持 Inf 或 NaN） |
| 信号数据要求    | ·信号数据值必须为有限值（不支持 Inf 或 NaN）                 |
| 文件格式要求    | ·文件中除时间数据外必须具有信号数据                          |
| 输出类型要求    | ·标量或向量信号                                              |

注：对于具有非数据表头的 CSV 文件，FromFile 会跳过非数据表头正常读取文件数据。

### MAT 文件数据

FromFile 模块可以从 MAT 格式文件中加载数据，其中第一行为时间数据，后续行为标量或向量的信号数据。目前可支持 v4、v6、v7 三种版本的数组格式 MAT 文件，

| MAT文件数据要求 | 说明                                                         |
| --------------- | ------------------------------------------------------------ |
| 时间数据要求    | ·时间数据类型必须为数值类型；<br>·时间数据值必须单调递增；<br>·时间数据值必须为有限值（不支持 Inf 或 NaN） |
| 信号数据要求    | ·信号数据类型必须为数值类型；<br/>·信号数据值必须为有限值（不支持 Inf 或 NaN）<br>·信号数据不可为复数 |
| 文件格式要求    | ·文件中除时间数据外必须具有信号数据<br>·文件需为数组格式     |
| 输出类型要求    | ·标量或向量信号                                              |
| 文件版本要求    | ·v4、v6、v7                                                  |

注：对于包含多个变量的 MAT 文件，FromFile 将始终读取其中的第一个变量数据，故此需提前确保所加载的 MAT 文件中仅包含单个变量。


## 示例

在 FromFile 模块文件名编辑框中选择文件 Data.csv，设置维度为 2，通过 FromFile 模块获取文件中的数据。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/FromFile.mo">FromFile.mo</helpButton>。


<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/FromFile/2.png')" style="width:600px">


仿真结果如下：


<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/FromFile/3.png')" style="width:600px">



## 端口

### 输出



<div class="details-box">
<details open>
<summary>y — 输出信号<div>向量</div></summary>
</details>
<div class="details-content">

使用从指定的 CSV 或 MAT 文件加载的数据创建的输出。根据指定的维度，输出对应的向量。

**数据类型：** double

</div>
</div>



## 参数

<div class="details-box">
<details open>
<summary>文件名 — CSV 文件名或 CSV 文件的路径<div>file_name.csv（默认） | CSV 文件名 | MAT 文件名 | CSV 文件相对路径 | MAT 文件相对路径</div></summary>
</details>
<div class="details-content">


包含模块待读取的 CSV 或 MAT 文件名或相对路径。

可在文本框中直接键入文件名或相对路径（当文件不在模型所在路径中时，需指定文件相对路径），也可通过单击**浏览**按钮加载待读取文件。

对于待读取文件的格式要求可参阅模块描述。

</div>
</div>



<div class="details-box">
<details open>
<summary>指定源数据类别 — 文件中源数据类别<div>分段连续（默认）| 离散阶梯</div></summary>
</details>
<div class="details-content">


指定读取文件中源数据类别，包括“分段连续”与“离散阶梯”两种，默认值为“分段连续”。

- 选择“分段连续”时，模块会将加载数据的本源信号视为连续，模块各功能均开放使用。
- 选择“离散阶梯”时，模块会将加载数据的本源信号视为离散，模块将关闭插值方法、过零检测等功能的启用，仅在文件中信号数据发生改变时更新计算。

</div>
</div>



<div class="details-box">
<details open>
<summary>维度 — CSV 文件的数据维度<div>-1（默认）| 标量 | 向量</div></summary>
</details>
<div class="details-content">


指定读取文件中数据的输出维度，默认值为 -1。支持以下四种设置场景：

- 维度设置为 -1，输出读取文件中的全部维度信号数据。
- 维度设置为标量 N，N 为正整数，输出读取文件中的前 N 维信号数据。
- 维度设置为向量 [a1,a2,...,aN]，a1、a2、...、aN 为正整数，输出读取文件中的第 a1、a2、...、aN 维信号数据。
- 维度设置为向量 [m:n]，m,n 为正整数且 m<n，输出读取文件中的第 m 到 n 维信号数据。

所有设置的维度应当在读取文件中信号数据的维度范围内。

</div>
</div>



<div class="details-box">
<details open>
<summary>第一个数据点之前的数据外插 — 确定文件中第一个数据点之前的输出方法<div>线性外插（默认） | 保持第一个值 | 接地值</div></summary>
</details>
<div class="details-content">


用于指定仿真时刻在文件中第一个数据点前的输出外插方法，包括线性外插、保持第一个值、接地值三种选项，默认值为线性外插。

- 线性外插：根据文件中前两个数据点，基于一次线性外插公式计算第一个数据点之前的输出值。若文件中数据只存在一个，则直接输出该数据值。
- 保持第一个值：直接以文件中第一个值作为输出值。
- 接地值：第一个数据点之前的输出值直接置0。

</div>
</div>



<div class="details-box">
<details open>
<summary>时间范围内的数据插值 — 确定文件中时间范围内的输出方法<div>线性内插（默认值） | 零阶保持</div></summary>
</details>
<div class="details-content">

用于指定仿真时刻在文件中时间范围内的输出内插方法，包括线性内插、零阶保持两种选项，默认值为线性内插。

- 线性内插：根据文件中与当前仿真时刻前后相邻的两个数据点，基于一次线性内插公式计算时间范围内的输出值。
- 零阶保持：时间范围内的输出值会从文件中与当前仿真时刻前相邻数据点保持到后相邻数据点。

</div>
</div>



<div class="details-box">
<details open>
<summary>末尾数据点后的数据外插<div>线性外插（默认值） | 保持最后一个值 | 接地值</div></summary>
</details>
<div class="details-content">

用于指定仿真时刻在文件中末尾数据点后的输出外插方法，包括线性外插、保持最后一个值、接地值三种选项，默认值为线性外插。

- 线性外插：根据文件中最后两个数据点，基于一次线性外插公式计算末尾数据点之后的输出值。若文件中数据只存在一个，则直接输出该数据值。
- 保持最后一个值：直接以文件中最后一个值作为输出值。
- 接地值：末尾数据点后的输出值直接置0。

</div>
</div>



<div class="details-box">
<details open>
<summary>采样时间 — 输出采样周期和可选时间偏移量<div>-1（默认）| 0 | 标量</div></summary>
</details>
<div class="details-content">

采样时间参数指定模块在仿真器件计算新输出值的时间。默认值为 -1。

采样时间参数值为 -1 表示继承。采样时间参数值为 0 表示连续采样时间。对于离散信号，请将采样时间指定为离散采样间隔。例如，将采样时间指定为 0.1 以对每 0.1s 采样一次的离散信号进行建模。

</div>
</div>



<div class="details-box">
<details open>
<summary>启用过零检测<div>off（默认）| on</div></summary>
</details>
<div class="details-content">

选择此选项以启用过零检测，该模块的过零检测功能用于定位不连续点。FromFile 模块会在连续采样时间时支持过零检测功能。

当所读取文件中存在时间数据相同的两个数据点时将会产生不连续性，如对于以下数据，不连续点将产生在时刻 3。

| 时间数据 |  1   |  2   |  3   |  3   |  5   |
| :------: | :--: | :--: | :--: | :--: | :--: |
| 信号数据 |  0   |  3   |  1   |  2   |  7   |

除此之外，FromFile 还会根据插值方法设置的不同产生不连续点：

- 当第一个数据点之前的数据外插设置为**接地值**时，模块将在文件中第一个数据点处产生不连续性；
- 当末尾数据点后的数据外插设置为**接地值**时，模块将在文件中最后一个数据点处产生不连续性；
- 当时间范围内的数据插值设置为**零阶保持**时，模块将在文件中每个数据点处产生不连续性；

此模块仅在变步长求解设置下支持过零检测功能，当使用定步长求解设置时，模块将不进行不连续点的检测定位。

</div>
</div>



## 版本历史记录

- 在 2025a 推出

### 限制信息

- 暂仅支持 v4、v6、v7 版本的数组格式 MAT 文件读取；
- 暂不支持嵌入式代码生成；
- 暂不支持 FMU 导出。