# BitSet
---
&nbsp;

将存储整数的第 i 位设为 1

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/BitSet/BitSet.png')" style="width: 100px; border:black 1px solid;">

**库：** Sysblock / LogicAndBitOperation

## 描述

BitSet 模块将存储的整数的指定位设置为 1。可以使用参数“位的索引”来指定要设置为 1 的位，其中位 0 是最低有效位。

## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/BitSet.mo">BitSet.mo</helpButton>。

**示例**

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/BitSet/BitSet1.png')" style="width: 600px; border:black 1px solid;">

**参考结果**

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/BitSet/Example1.png')" style="width: 700px; border:black 1px solid;">



## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">
输入信号，指定为标量、向量、矩阵或多维数组。

**数据类型：**  int8 | int16 | int32 | int64 | uint8 | uint16 | uint32 | uint64 | boolean

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 向量 | 多维数组</div></summary>
</details>
<div class="details-content">
输出信号，指定为标量、向量、矩阵或多维数组。

**数据类型：** int8 | int16 | int32 | int64 | uint8 | uint16 | uint32 | uint64 | boolean

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>位的索引 — 位的索引<div>0（默认） | 标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">
指定设置为 1 的位的索引，其中 0 是最低有效位。

</div>
</div>

## 版本历史记录

- 在 2025a 推出


### 限制信息

- 参数——**位的索引**最大标量取值为 51。

