# DiscreteDerivative

计算离散时间导数

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/DiscreteDerivative/DiscreteDerivative.png')" style="width: 100px; height: auto;border:solid 1px black;">


**库：** Sysblock 模型库 / Discrete

## 描述

Discrete Derivative 模块计算有选择性缩放的离散时间导数，如下所示：
$$
y(t_n)=K(\frac{u(t_n)-u(t_{n-1})}{T_s})
$$
其中：

- $u(t_n)$和$y(t_n)$分别是模块在当前时间步的输入和输出。

- $u(t_{n-1})$是在上一个时间步的模块输入。
- $K$是可选的缩放因子，使用增益值参数指定。
- $T_s$是仿真的离散步长（必须是固定值）。

请勿在具有非周期性触发器的子系统（例如，非周期函数调用子系统）中使用此模块，可能会产生不准确的结果。

## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/DiscreteDerivative.mo">DiscreteDerivative.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/DiscreteDerivative/DiscreteDerivative_example.png')" style="width: 600px; height: auto;border:solid 1px black;">

**参考结果**

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/DiscreteDerivative/DiscreteDerivative_output.png')" style="width: 600px; height: auto;border:solid 1px black;">



## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">


​	输入信号，指定为标量、向量或矩阵。

**数据类型：double | float | int8 | uint8 | int16 | uint16 | int32 | uint32 | int64 | uint64 | boolean**

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">

​	可选择缩放的离散时间导数。

**数据类型：double | float | int8 | uint8 | int16 | uint16 | int32 | uint32 | int64 | uint64**

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>增益值<div>1.0（默认值）| 标量</div></summary>
</details>
<div class="details-content">

应用于计算的导数的缩放因子。

</div>
</div>

<div class="details-box">
<details open>
<summary>上一加权输入 K*u/Ts 的初始条件<div>0.0（默认值）| 标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">

上一个经过缩放的输入的初始条件。

</div>
</div>




## 信号属性

<div class="details-box">
<details open>
<summary>输出数据类型<div>Inherit: internalRule （默认值） | Inherit: backPropagation | double | float | int8 | uint8 | int16 | uint16 | int32 | uint32 | int64 | uint64</div></summary>
</details>
<div class="details-content">

指定模块输出信号的数据类型。

</div>
</div>



## 版本历史记录

在 MWORKS 2025b 推出

### 限制信息

- 增益值参数必须为标量，且不能为 0
- 暂不支持指定整数舍入模式，当前默认为“向零”舍入模式

