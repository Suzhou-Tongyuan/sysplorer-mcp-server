# RandomNumber

生成正态分布的随机数。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/RandomNumber/1.png')" style="width: 100px; height: auto; transform: scale(1);">

**库：** Sysblock 模块库/Sources

## 描述

- Random Number 模块可生成正态分布的随机数。要生成均匀分布的随机数，请使用 Uniform Random Number 模块。
- 可以使用任何 Random Number 模块，利用相同的非负种子和参数生成可重复的序列，每次开始仿真时，种子都会重置为指定的值；默认情况下，此模块会生成一个均值为 0、方差为 1 的序列，要生成具有相同均值和方差的随机数向量，请将种子参数指定为向量。
- 应避免对随机信号求积分，因为求解器积分针对的只能为相对平滑的信号，这种情况请改用 Band Limited White Noise 模块。
- 此模块的数值参数在标量扩展后必须具有相同的维度。

## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/RandomNumber.mo">RandomNumber.mo</helpButton>。

方差为 {1,2}，其余参数默认。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/RandomNumber/2.png')" style="width: 800px; height: auto; transform: scale(1);border-top: 1px solid black;">

## 端口

### 输入


<div class="details-box">
<details open>
<summary>Port_1 — 随机数输出信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

- 输出信号，即落入正态高斯分布内的生成的随机数。
- 给定种子的输出可以重复。
- **数据类型：** double

</div>
</div>


## 参数


<div class="details-box">
<details open>
<summary>均值 — 随机数的均值<div>标量 | 数组</div></summary>
</details>
<div class="details-content">

- 指定生成的随机数的均值。
- **数据类型：** double

</div>
</div>



<div class="details-box">
<details open>
<summary>方差 — 随机数的方差<div>标量 | 数组</div></summary>
</details>
<div class="details-content">

- 指定随机数的方差。
- **数据类型：** double

</div>
</div>



<div class="details-box">
<details open>
<summary>种子 — 起始种子<div>标量 | 数组</div></summary>
</details>
<div class="details-content">

- 指定随机数生成器的起始种子，对于给定种子，生成的数字的输出可以重复。
- 随机数生成器实际上会按照取整后的种子值去生成随机数。
- 比如种子值为 1.2 或 1.7 时，它们生成的随机数是一样的。
- **数据类型：** double

</div>
</div>



<div class="details-box">
<details open>
<summary>采样时间 — 间隔时间<div></div></summary>
</details>
<div class="details-content">

- 指定采样时间间隔。
- **数据类型：** integer，非负整数或 -1。

</div>
</div>


## 版本历史记录

- 在 2025a 推出

## 限制信息

- 参数类型均只能为 double。