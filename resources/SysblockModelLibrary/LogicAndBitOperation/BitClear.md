# BitClear
---
&nbsp;

将存储整数的指定位设置为 0

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/BitClear/BitClear1.png')" style="width: 100px; border:black 1px solid;">

**库：** Sysblock / LogicAndBitOperation

## 描述

Bit Clear 模块将存储整数的指定位（由其索引给定）设置为 0。可以使用 Index of bit 参数指定要设置为 0 的位，其中 0 位是最低有效位。

## 示例

**示例**

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/BitClear1.mo">BitClear1.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/BitClear/BitClear2.png')" style="width: 500px; border:black 1px solid;">

此示例将输入矩阵中的每个元素的第 0 位置 0，得到正确输出结果。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/BitClear2.mo">BitClear2.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/BitClear/BitClear3.png')" style="width: 500px; border:black 1px solid;">

此示例将输入矩阵中的每个元素的第 1 位置 0，得到正确输出结果。

## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">

输入信号，存储整数的指定位。

**数据类型：**  int8 | int16 | int32 | int64 | uint8 | uint16 | uint32 | uint64 | boolean

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 向量 | 多维数组</div></summary>
</details>
<div class="details-content">

输出信号，设置为零的指定位。

**数据类型：** int8 | int16 | int32 | int64 | uint8 | uint16 | uint32 | uint64 | boolean

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>位的索引 — 位的索引<div>0（默认） | 标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">

位的索引，其中 0 是最低有效位。

</div>
</div>

## 版本历史记录

- 在 2025b 推出


### 限制信息

- 仿真的开始时间必须为 0；
- 输入数据类型不支持 double 、定点和总线。