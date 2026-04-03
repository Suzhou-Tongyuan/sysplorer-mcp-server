# MinMaxRunningResettable

计算输入信号随时间变化的最小值或最大值。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/MinMaxRunningResettable/MinMaxRunningResettable1.png')" style="width: 100px; border:black 1px solid;">

**库**： Sysblock / MathOperation

## 描述

MinMax Running Resettable 模块可计算输入信号 u 的动态最小值或最大值。您可以使用**函数**参数指定此模块是输出动态最小值还是最大值。

模块可以根据外部重置信号 R 重置其状态。当重置信号 R 为非零 ( true ) 时，模块将输出重置为**初始条件**参数的值。

输入可以是标量、向量、矩阵或多维数组。模块的输出与输入具有相同的数据类型。每个输出元素等于对应输入元素的动态最小值或最大值。

## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperation/MinMaxRunningResettable.mo">MinMaxRunningResettable.mo</helpButton>。

**示例模型**

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/MinMaxRunningResettable/MinMaxRunningResettable2.png')" style="width: 600px; border:black 1px solid;">

**参考结果**

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/MinMaxRunningResettable/MinMaxRunningResettable3.png')" style="width: 600px; border:black 1px solid;">

## 端口

### 输入

<div class="details-box">
<details open>
<summary>u1 — 输入信号<div>标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">

输入信号，指定为标量、向量、矩阵或多维数组。根据**函数**参数指定的内容，模块计算输入 u 的动态最小值或最大值。

如果您为**初始条件**参数指定标量值，模块将扩展该参数，使其与非标量输入 u 具有相同的维度。

**数据类型：** double | float | int8 | int16 | int32 | int64 | uint8 | uint16 | uint32 | uint64 | boolean

</div>
</div>

<div class="details-box">
<details open>
<summary>u2 — 重置信号<div>标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">

重置信号，指定为标量、向量、矩阵或多维数组。当重置信号为零时，模块就会输出输入信号 u 的动态最小值或最大值。否则模块将输出**初始条件**参数的值。

**数据类型：** double | float | int8 | int16 | int32 | int64 | uint8 | uint16 | uint32 | uint64 | boolean

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">

输出信号，指定为标量、向量、矩阵或多维数组，其中每个输出元素等于对应输入元素的动态最小值或最大值。输出信号 y 与输入信号 u 具有相同的数据类型。

当模块接收到非零 ( true ) 重置信号时，模块将输出重置为**初始条件**参数的值。

**数据类型：** double | float | int8 | int16 | int32 | int64 | uint8 | uint16 | uint32 | uint64 | boolean

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>函数 — 指定最小值或最大值<div>最小值（默认）| 最大值</div></summary>
</details>
<div class="details-content">

指定模块是否输出对应输入元素的动态最小值或最大值。

</div>
</div>

<div class="details-box">
<details open>
<summary>初始条件 — 输出重置后的值<div>0.0（默认值）| 标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">

指定初始条件值。当重置输入信号 R 为 非零 ( true ) 时，模块将输出重置为初始条件的值。

</div>
</div>



## 版本历史记录

- 在 2025a 推出
