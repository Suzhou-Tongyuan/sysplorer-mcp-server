# J_KFlipFlop
---
&nbsp;

负边沿触发的 J-K 触发器建模

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/FlipFlopsPng/JKFlipFlop/JKFlipFlop.png')" style="width:100px; border: 1px solid black;">

**库：** Sysblock 模块库 / FlipFlops

## 描述

J_KFlipFlop 模块对负边沿触发的 J-K 触发器进行建模。J_KFlipFlop 模块有三个输入，即 J、K 和 CLK；有两个输出，即 Q 和 !Q。在时钟信号（CLK）的负（下降）沿，J_KFlipFlop 模块根据以下真值表输出 Q 及其反值 !Q。在此真值表中，Q<sub>n-1</sub> 是前一时间步的输出。

::: tip 提示

J_KFlipFlop 模块将非零输入视为 true(1)。

:::

|  J   |  K   |   Q<sub>n</sub>    |   !Q<sub>n</sub>   |
| :--: | :--: | :----------: | :----------: |
|  0   |  0   | Q<sub>n-1</sub>  | Q<sub>n-1</sub> |
|  0   |  1   |      0       |      1       |
|  1   |  0   |      1       |      0       |
|  1   |  1   | Q<sub>n-1</sub> | Q<sub>n-1</sub>  |

当 J 为 1 且 K 为 0 时，触发器进入设置状态（Q<sub>n</sub> 为 1）。当 J 为 0 且 K 为 1 时，触发器进入重置状态（Q<sub>n</sub> 为 0）。当 J 和 K 都为 0 时，触发器停留在先前的状态（Q<sub>n</sub> 为 Q<sub>n-1</sub>）。当 J 和 K 都为 1 时，触发器会发生切换（Q<sub>n</sub> 为 Q<sub>n-1</sub> 的反值）。

## 示例


参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/FlipFlops/JKFlipFlop.mo">JKFlipFlop.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/FlipFlopsPng/JKFlipFlop/JKFlipFlop_example.png')" style="width:600px; border: 1px solid black;">

### 参考结果


<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/FlipFlopsPng/JKFlipFlop/Example_output.png')" style="width:600px; border: 1px solid black;">


## 端口

### 输入

<div class="details-box">
<details open>
<summary>J — 输入信号<div>标量</div></summary>
</details>
<div class="details-content">

输入信号，指定为标量。

**数据类型：** boolean

</div>
</div>


<div class="details-box">
<details open>
<summary>CLK — 时钟信号<div>标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">

输入信号，指定为标量、向量、矩阵或多维数组。当 CLK 输入为非标量时，任一信号形成下降沿均可触发该模块。

**数据类型：** double | float | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean

</div>
</div>


<div class="details-box">
<details open>
<summary>K — 输入信号<div>标量</div></summary>
</details>
<div class="details-content">

输入信号，指定为标量。

**数据类型：** boolean

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>Q — 输出信号<div>标量</div></summary>
</details>
<div class="details-content">

输出信号，维度为标量。

**数据类型：** boolean

</div>
</div>

<div class="details-box">
<details open>
<summary>!Q — 输出信号<div>标量</div></summary>
</details>
<div class="details-content">

输出信号，维度为标量。

**数据类型：** boolean

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>初始条件 — 指定输出 Q 的初始值<div>0（默认值）| 标量 </div></summary>
</details>
<div class="details-content">

指定输出 Q 的初始值，非零值被视为 true(1)。

</div>
</div>


## 版本历史记录

- 在 2025a 推出

### 限制信息

- J、K 输入仅支持 boolean 类型；

- CLK 输入不支持定点、总线、枚举值类型。
