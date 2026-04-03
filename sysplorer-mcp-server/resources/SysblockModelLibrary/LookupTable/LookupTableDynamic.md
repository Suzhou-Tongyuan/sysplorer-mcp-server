# LookupTableDynamic

使用所选的查找方法动态逼近一维函数。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LookupTable/LookupTableDynamic/1.png')" style="width: 150px; height: auto; transform: scale(1);border: 1px solid black;">

**库：** Sysblock 模型库 / LookupTable

## 描述

LookupTableDynamic 模块使用动态表逼近一维函数。
## 示例

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LookupTable/LookupTableDynamic.mo">LookupTableDynamic.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LookupTable/LookupTableDynamic/2.png')" style="width: 500px; height: auto; transform: scale(1);border: 1px solid black;">

**参考结果**

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LookupTable/LookupTableDynamic/3.png')" style="width: 800px; height: auto; transform: scale(1);border-top: 1px solid black;">

## 端口

### 输入

<div class="details-box">
<details open>
<summary>x — 输入信号<div>标量 | 向量 | 二维数组</div></summary>
</details>
<div class="details-content">

输入信号。

**数据类型：double | float | int8 | uint8 | int16 | uint16 | int32 | uint32 | int64 | uint64 | boolean | fixedPoint** 

</div>
</div>

<div class="details-box">
<details open>
<summary>xdat — 断点数据<div>向量</div></summary>
</details>
<div class="details-content">

xdat 向量是断点数据，它必须严格单调递增。xdat 断点数据和 x 输入必须具有相同的符号、偏置和小数斜率。此外，x 的精度和范围必须大于或等于 xdat 的精度和范围。

**数据类型：double | float | int8 | uint8 | int16 | uint16 | int32 | uint32 | int64 | uint64 | boolean | fixedPoint** 

</div>
</div>

<div class="details-box">
<details open>
<summary>ydat — 表数据<div>向量</div></summary>
</details>
<div class="details-content">

ydat 向量是表数据，它必须与 xdat 数据一一对应。

**数据类型：double | float | int8 | uint8 | int16 | uint16 | int32 | uint32 | int64 | uint64 | boolean | fixedPoint** 

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 向量 | 二维数组</div></summary>
</details>
<div class="details-content">

该模块使用 xdat  和  ydat 输入向量来计算函数 y = f(x) 的近似值。

**数据类型：double | float  | int8 | uint8 | int16 | uint16 | int32 | uint32 | int64 | uint64 | boolean | fixedPoint**  

</div>
</div>

## 参数

### 主要

<div class="details-box">
<details open>
<summary>查找方法<div>内插-外插 | 插值-使用最终值（默认）| 取最邻近的输入值| 向下取输入值 | 向上取输入值 </div></summary>
</details>
<div class="details-content">

该模块通过将您选择的查找方法应用于断点数据 ( xdat ) 和表数据 ( ydat ) 的输入向量来计算输出。

</div>
</div>

### 信号属性

<div class="details-box">
<details open>
<summary>输出数据类型<div>Inherit: backPropagation | double（默认） | float | int8 | uint8 | int16 | uint16 | int32 | uint32 | int64 | uint64 | boolean | fixdt(1,16,0) | fixdt(1,16,2^0,0)</div></summary>
</details>
<div class="details-content">

该模块使用 xdat 和 ydat 输入向量来计算函数 y = f(x) 的近似值。

</div>
</div>

## 版本历史记录

- 在 2025b 推出

### 限制信息

- 输出数据类型暂不支持half数据类型；
- 暂无锁定数据类型设置以防止被定点工具更改选项；
- 暂无整数舍入模式选项；
- 暂无发生溢出时饱和处理为最大值或最小值选项。