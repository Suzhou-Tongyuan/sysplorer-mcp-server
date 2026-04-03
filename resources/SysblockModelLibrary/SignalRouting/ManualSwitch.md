# ManualSwitch

在两个输入之间切换

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/ManualSwitch/ManualSwitch.png')" style="width: 100px; height: auto; border:black 1px solid;">

**库：** Sysblock / SignalRouting

## 描述

Manual Switch 模块是一个拨动开关，可以从两个输入中选择一个来传递给输出。要在输入之间进行切换，请双击此模块。可以在仿真开始之前设置开关，或者在仿真执行过程中更改开关，从而控制信号流。当保存模型时，Manual Switch 模块将保留其当前状态。

::: warning 注意 
双击 Manual Switch 模块不会打开模块对话框，而是会切换输入选项。
:::

## 示例

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/ManualSwitch.mo">ManualSwitch.mo</helpButton>。

本示例展示了如何使用 Manual Switch 模块控制信号流。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/ManualSwitch/ManualSwitch_1.png')" style="width: 600px; border:black 1px solid;">

双击此模块后：

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/ManualSwitch/Example_ManualSwitch_2.png')" style="width: 600px;  border:black 1px solid;">



## 端口

### 输入

<div class="details-box">
<details open>
<summary>u1 — 第一个数据输入信号<div>标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">
Manual Switch 模块的两个输入中的第一个。此模块将选定的输入传播到输出。要选择输入信号，请通过双击模块切换开关。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | fixedPoint | enum | bus

</div>
</div>

<div class="details-box">
<details open>
<summary>u2 — 第二个数据输入信号<div>标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">
Manual Switch 模块的两个输入中的第二个。此模块将选定的输入传播到输出。要选择输入信号，请通过双击模块切换开关。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | fixedPoint | enum | bus

</div>
</div>



### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">
输出信号是从第一个或第二个输入信号传播的。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | fixedPoint | enum | bus

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>允许两个输入具有不同大小（产生可变大小的输出信号）— 允许不同大小的输入<div>off（默认） | on</div></summary>
</details>
<div class="details-content">

选中此复选框可允许不同大小的输入并将所选输入信号的大小传播给输出信号。如果清除该框，模块会扩展标量输入，使其具有与非标量输入相同的维度。

</div>
</div>

## 版本历史记录

- 在 2025b 推出


