# RepeatingSequenceInterpolated
---
&nbsp;

输出离散时间序列并重复，从而在数据点之间插值。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/RepeatingSequenceInterpolated/1.png')" style="width:100px;border:black 1px solid;"> 

- **库：** Sysblock / Sources

## 描述

Repeating Sequence Interpolated 模块根据**时间值的向量**和**输出值的向量**参数中的值输出周期性离散序列。在数据点之间，该模块使用您为**查找方法**参数指定的方法来确定输出。
## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/RepeatingSequenceInterpolated.mo">RepeatingSequenceInterpolated.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/RepeatingSequenceInterpolated/2.png')" style="width:400px;border:black 1px solid;">

### 仿真结果

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/RepeatingSequenceInterpolated/3.png')" style="width:900px;border:black 1px solid;"> 

## 端口

### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量</div></summary>
</details>
<div class="details-content">


根据**时间值的向量**和**输出值的向量**参数中的值生成的输出信号。

**数据类型：** double | float | int8 | uint8 | int16 | uint16 | int32 | uint32 | int64 | uint64 | fixedPoint

</div>
</div>

## 参数

### 主要

<div class="details-box">
<details open>
<summary>输出值的向量<div>[3,1,4,2,1]（默认）| 一维数组 | 向量</div></summary>
</details>
<div class="details-content">



输出值的向量，用于指定输出波形。每个元素对应时间值的向量参数中的时间值。

</div>
</div>

<div class="details-box">
<details open>
<summary>时间值的向量<div>[0,0.1,0.5,0.6,1]（默认）| 一维数组 | 向量 </div></summary>
</details>
<div class="details-content">



指定包含时间值的向量。时间值必须严格递增，并且向量的大小必须与输出值向量的大小相同。

</div>
</div>

<div class="details-box">
<details open>
<summary>查找方法<div>插值-使用最终值（默认）| 取最邻近的输入值| 向下取输入值 | 向上取输入值 </div></summary>
</details>
<div class="details-content">


输出的查找方法，指定查找方法以确定数据点之间的输出。

</div>
</div>

<div class="details-box">
<details open>
<summary>采样时间<div>0.01（默认）| 标量 </div></summary>
</details>
<div class="details-content">


指定采样时间间隔，只能为 -1 或正实数。

</div>
</div>


### 信号属性

<div class="details-box">
<details open>
<summary>输出数据类型<div>Inherit: backPropagation | double（默认） | float | int8 | uint8 | int16 | uint16 | int32 | uint32 | int64 | uint64 | fixdt(1,16,0) | fixdt(1,16,2^0,0)</div></summary>
</details>
<div class="details-content">



指定模块输出信号的数据类型。

</div>
</div>

## 版本历史记录

- 在 2025b 推出

### 限制信息

- 暂无输出最小值、输出最大值编辑框。
- 暂无锁定输出数据类型设置以防止被定点工具更改选项。

