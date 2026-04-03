# IntegerToBitConverter
---
&nbsp;

将元素为整数的向量映射为元素为比特的向量

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/IntegerToBitConverter/1.png')" style="width: 100px; border:black 1px solid;">

**库：** Sysblock / LogicAndBitOperation

## 描述

Integer to Bit Converter 模块将输入向量中的每个整数映射为输出向量中的二进制比特表示。对于每个输入整数值，模块会生成一组 M 位比特。比特的顺序由输出位顺序参数决定，用于指定最高有效位的位置。因此，输出向量的长度等于输入向量长度的 M 倍。

## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/IntegerToBitConverter.mo">IntegerToBitConverter.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/IntegerToBitConverter/2.png')" style="width: 500px; border:black 1px solid;">

本示例在使用默认参数的情况下，展示了如何使用 Integer to Bit Converter 模块将输入的 3×1 整数列向量转成对应的二进制。

## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 一维数组 | 列向量 </div></summary>
</details>
<div class="details-content">


输入信号，指定为长度为 N 的一维数组、列向量或 N 为 1 的标量。

**数据类型：double | float | int8 | uint8 | int16 | uint16 | int32 | uint32**

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 一维数组 | 列向量</div></summary>
</details>
<div class="details-content">
输出信号，以长度为 M*N 的标量、一维数组或列向量的形式返回。

**数据类型：double | float | int8 | uint8 | int16 | uint16 | int32 | uint32 | boolean**

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>每个整数的位数(M)<div>3 (默认) | 范围在 [1,32] 内的整数</div></summary>
</details>
<div class="details-content">

输入映射到输出中，指定输出信号中每个整数的输出位数。

</div>
</div>

<div class="details-box">
<details open>
<summary>输入位顺序<div>最高有效位优先(默认)|最低有效位优先</div></summary>
</details>
<div class="details-content">
定义输入信号的第一位是最高有效位，还是最低有效位。
</div>
</div>

<div class="details-box">
<details open>
<summary>在位压缩后，将得到的整数值视为<div>无符号(默认) | 有符号</div></summary>
</details>
<div class="details-content">

指定在整数转二进制后，输出结果是否应视为有符号或无符号处理。

</div>
</div>

<div class="details-box">
<details open>
<summary>输出数据类型<div>与输入相同 | double | float | int8 | uint8 | int16 | uint16 | int32 | uint32 | boolean</div></summary>
</details>
<div class="details-content">
其中： 与输入相同 — 该模块根据输入数据类型确定输出数据类型。

</div>
</div>

## 版本历史记录

- 在 2025b 推出

### 限制信息

- 不支持定点

