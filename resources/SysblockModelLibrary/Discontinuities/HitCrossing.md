# HitCrossing

检测穿越点

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/DiscontinuitiesPng/HitCrossing/HitCrossing.png')" style="width: 100px; border: 1px solid black;">

**库：** Sysblock / Discontinuities

## 描述

HitCrossing 模块用以检测输入信号相对其偏移量的穿越方向。可通过参数**输出类型**将模块输出配置为**信号**或**函数调用事件**。若输出类型为信号，则输入信号在指定方向上越过偏移值时，则模块输出 true ，反之则为 false。若**输出类型**为函数调用，则输入信号在指定方向上越过偏移值时，模块输出函数调用事件，此时模块输出可作为函数调用子系统的控制信号或状态机输入事件。

## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discontinuities/HitCrossing.mo">HitCrossing.mo</helpButton>。

**示例**

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/DiscontinuitiesPng/HitCrossing/HitCrossing01.png')" style="width: 600px; border: 1px solid black;">

**参考结果**

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/DiscontinuitiesPng/HitCrossing/HitCrossing02.png')" style="width: 600px; border: 1px solid black;">

## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 向量 | 多维数组</div></summary>
</details>
<div class="details-content">

输入信号，模块会检测其何时在指定方向上达到偏移值。

**数据类型：** double

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 向量 | 多维数组</div></summary>
</details>
<div class="details-content">

输出为布尔类型变量，表示是否发生穿越。


**数据类型：** boolean

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>穿越偏移量 — 检测的穿越值<div>1（默认） | 实数值</div></summary>
</details>
<div class="details-content">

指定输入信号在指定穿越方向上是否发生穿越的检测值。

</div>
</div>

<div class="details-box">
<details open>
<summary>穿越方向 — 输入信号的穿越方向<div>任一沿（默认）| 下降沿 | 上升沿</div></summary>
</details>
<div class="details-content">

检测穿越时输入信号接近穿越偏移值方向，穿越方向为上升沿、下降沿或任一沿。

</div>
</div>

<div class="details-box">
<details open>
<summary>输出类型 — 选择信号或函数调用输出<div>信号（默认）| 函数调用</div></summary>
</details>
<div class="details-content">

当输出类型为信号时，只要输入信号穿越穿越方向中的穿越偏移量值且在其他时间输出为 false，输出信号就会设置为 true。当输出类型为函数调用时，输出信号成为函数调用事件。

</div>
</div>

<div class="details-box">
<details open>
<summary>过零检测 — 启用过零检测<div>on（默认）| off</div></summary>
</details>
<div class="details-content">

当仿真设置配置为变步长时可启用该选项。若启用过零检测，模块会精确定位穿越行为的触发时刻，并产生状态事件；反之则只会在主时间步检测过零，并产生主时间步事件。


</div>
</div>

## 版本历史记录

- 在 2025a 推出


### 限制信息

- 输入信号仅支持 double 类型；
- 穿越偏移量必须是有限的实数值，维度可以是标量、向量、矩阵或多维数组。非标量时，维度需与输入信号的维度匹配；
- 输出类型未支持消息选项；
- 只有仿真设置配置为变步长算法时才会显示启用过零检测选项；
- 不支持在 while 子系统中使用；
- 不支持在代数环中使用。

