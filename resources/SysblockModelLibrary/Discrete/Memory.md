# Memory
---
&nbsp;
输出上一个时间步的输入

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/Memory/Memory.png')" style="width: 150px; height: auto; border: 1px solid black;">

- **库：** Sysblock / Discrete

## 描述

Memory 模块将它的输入保持并延迟一个主积分时间步。此模块接受离散信号和连续信号，接受一个输入并生成一个输出。每个信号可以是标量，向量，矩阵或者多维数组。当输入为非标量时，它会将输入的所有元素保持并延迟相同的时间步。

使用“初始条件”参数指定第一个时间步时模块的输出。“继承采样时间”参数确定模块的采样时间是继承的还是基于模型的基频。

### 与类似模块的比较

| 模块          | 模块的用途                                                   |
| ------------- | ------------------------------------------------------------ |
| UnitDelay     | 使用指定的离散采样时间实现延迟。该模块接受并输出具有离散采样时间的信号。 |
| Memory        | 将信号延迟一个主积分时间步。该模块既可以接受并输出离散的信号，也可以接受并输出连续的信号。 |
| ZeroOrderHold | 将具有连续采样时间的输入信号转换为具有离散采样时间的输出信号。 |

## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/Memory.mo">Memory.mo</helpButton>。

我们将一个Memory模块和一个Ramp模块相连，如下图所示：

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/Memory/Memory_case1.png')" style="width: 400px; height: auto; border: 1px solid black;">

模型的仿真步长为 0.02，仿真时间为 1。根据下图的对比结果可看出，Memory 模块将来自 Ramp 模块的输入信号保持并延迟了一个时间步。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/Memory/Memory_case2.png')" style="width: 600px; height: auto; border: 1px solid black;">

## 端口

### 输入

<div class="details-box">
<details open>
<summary>Port_1 — 输入信号<div>标量 | 向量 | 矩阵 | N 维数组</div></summary>
</details>
<div class="details-content">

输入信号，指定为标量、向量、矩阵或 N 维数组。输入可以是连续信号或离散信号。

**数据类型：** double | float | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | fixedpoint  | 枚举 | 总线

</div>
</div>


### 输出


<div class="details-box">
<details open>
<summary>Port_1 — 延迟了一个主积分时间步的输入<div>标量 | 向量 | 矩阵 | N维数组</div></summary>
</details>
<div class="details-content">

输出是来自上一时间步的输入。

**数据类型：** double | float | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | fixedpoint | 枚举 | 总线

</div>
</div>




## 参数

<div class="details-box">
<details open>
<summary>初始条件 — 初始条件<div>0 （默认） | 标量 | 向量 | 矩阵 | N 维数组</div></summary>
</details>
<div class="details-content">

指定初始时刻 Memory 模块的输出。当不使用内置输入数据类型时，此值必须为 0。

</div>
</div>



<div class="details-box">
<details open>
<summary>继承采样时间 — 继承采样时间<div>off（默认）| on</div></summary>
</details>
<div class="details-content">

选中此选项可从驱动模块继承采样时间：

- 如果驱动模块具有离散采样时间，模块将继承该采样时间。
- 如果驱动模块具有连续采样时间，则采样时间取决于模型的仿真类型。

如果清除此复选框，模块采样时间将取决于模型的仿真类型：

- 如果仿真类型为变步长，则模块采样时间为连续。
- 如果仿真类型为定步长，则模块采样时间为模型的基频。

</div>
</div>



## 版本历史记录

- 在 2025a 推出
