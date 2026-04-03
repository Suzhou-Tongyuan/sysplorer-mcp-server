# FromWorkspace
---
&nbsp;


将信号数据从 Syslab 工作区加载到 Sysblock 模型中


- **库：** Sysblock / Sources

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/FromWorkspace/1.png')" style="width: 100px; height: auto;">

## 描述

FromWorkspace 模块将数据从 Syslab 工作区读入 Sysblock 模型，并在模块的输出端以信号形式提供数据。

FromWorkspace 模块图标显示数据参数的值。例如，如果您使用 FromWorkspace 模块加载变量 x 中的数据，并且指定 x 作为数据参数的值，则该模块将显示 x。

From Workspace 模块支持的大多数数据格式基本上都由配对的时间值和信号值组成。使用 From Workspace 模块加载包含时间值的数据时，时间值的数据类型必须为 double，并且时间值必须单调递增。

您可在**选项>环境>常规>[**环境**](/Doc/DevelopingModels/CustomizedEnvironment/Options.html#x6b1c95ad)>目标 Syslab 工作区**，配置数据来源工作区。

## 示例

在 Syblab 工作区定义变量 simin = [0.1 1 1; 0.2 2 4; 0.3 3 3; 0.4 4 1]，设置 FromWorkspace 模块维度为 [2]，通过 FromWorkspace 模块获取 simin 的值。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/FromWorkspace.mo">FromWorkspace.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/FromWorkspace/2.png')">

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/FromWorkspace/3.png')" style="width: 600px; border:solid black 1px;">


## 端口

### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>向量</div></summary>
</details>
<div class="details-content">

使用从 Syslab 工作区读取的指定变量创建的输出。根据您指定的维度，输出对应的向量。

**数据类型：** double

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>数据 — 要从Syslab工作区加载的数据<div>simout（默认）| 变量名 </div></summary>
</details>
<div class="details-content">

从 Syslab 工作区读取的变量名称。


</div>
</div>

<div class="details-box">
<details open>
<summary>维度 — 数据维度<div>  向量 </div></summary>
</details>
<div class="details-content">

设置读取到 Sysblock 中 Syslab 工作区变量的信号值数据维度。
以示例模型为例：其为列数为 3，第一列为时间值，因此信号列为 2，维度填写为 [2]。


</div>
</div>

<div class="details-box">
<details open>
<summary>采样时间 — 输出采样周期和可选时间偏移量<div>  0 | 标量 </div></summary>
</details>
<div class="details-content">

采样时间参数指定模块在仿真期间计算新输出值的时间。

默认情况下，采样时间参数值为 -1，表示继承。对于离散信号，请将采样时间指定为离散采样间隔。例如，将采样时间指定为 0.1 以对每 100 毫秒采样一次的离散信号建模。将采样时间指定为 0 以表示没有时间偏移量的连续采样时间。


</div>
</div>

## 版本历史记录

- 在 2025a 推出

### 限制信息

- 暂不支持端口维度与数据类型的推导，需手动配置，且只能设置为一维向量。
- 暂且仅支持 double 类型数据。
- 暂不支持 TimeTable 类型数据。
