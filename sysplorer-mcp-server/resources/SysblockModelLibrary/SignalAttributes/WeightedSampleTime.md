# WeightedSampleTime

支持涉及采样时间的计算

**库：**Sysblock 模型库 / SignalAttributes

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalAttributes/WeightedSampleTime/WeightedSampleTime.png')" style="width: 100px; height: auto; border:solid 1px black;">

## 描述

Weighted Sample Time 模块输出加权采样时间、加权采样率或经过数学调整后的加权采样时间。

## 示例

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalAttributes/WeightedSampleTime.mo">WeightedSampleTime.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalAttributes/WeightedSampleTime/WeightedSampleTime_example.png')" style="width: 600px; height: auto; border:solid 1px black;">

使用 Weighted Sample Time 模块，采样时间为 0.2。指定不同的运算模式与权重值，可将输入信号与加权采样时间联合进行计算。

## 端口

### 输入

<div class="details-box">
<details open>
<summary>Port_1—输入信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

​	输入信号，指定为标量、向量或矩阵。

**数据类型：double | float | int8 | uint8 | int16 | uint16 | int32 | uint32 | int64 | uint64 | boolean**

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>y—输入信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

​	根据设置的运算模式与权重值参数，输出加权采样时间、加权采样率或经过数学调整后的加权采样时间。

**数据类型：double | float | int8 | uint8 | int16 | uint16 | int32 | uint32 | int64 | uint64**

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>运算<div>“仅限Ts”（默认值）| “+” | “-” | “*” | “/” | “仅限1/Ts”</div></summary>
</details>
<div class="details-content">

​	指定用于调整输入信号的运算模式。

</div>
</div>


<div class="details-box">
<details open>
<summary>权重值<div>1.0（默认值） | 标量</div></summary>
</details>
<div class="details-content">

​	为采样时间的权重指定一个实型标量。

</div>
</div>



## 信号属性

<div class="details-box">
<details open>
<summary>输出数据类型<div>Inherit: internalRule（默认值） | Inherit: backPropagation | double | float | int8 | uint8 | int16 | uint16 | int32 | uint32 | int64 | uint64</div></summary>
</details>
<div class="details-content">

​	指定模块输出信号的数据类型。

</div>
</div>



## 版本历史记录

在 MWORKS 2025b 推出

### 限制信息

- 权重值参数仅支持实型标量
- 涉及除法运算时，权重值参数不能为 0
- 暂不支持指定整数舍入模式，当前默认为“零”舍入模式

