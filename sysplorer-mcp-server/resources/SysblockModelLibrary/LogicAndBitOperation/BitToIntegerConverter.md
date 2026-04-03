# BitToIntegerConverter
---
&nbsp;

将元素为比特的向量映射为元素为整数的向量

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/BittoIntegerConverter/1.png')" style="width: 100px; border:black 1px solid;">

**库：** Sysblock / LogicAndBitOperation

## 描述

Bit to Integer Converter 模块将输入的比特向量映射到输出向量中的整数。

如果将**每个整数的位数（M）**参数指定为 M 时，则：

- 当**在位压缩后，将得到的整数值视为**无符号，该模块将每组 M 比特映射到输出值是 [0, 2^M-1] 范围内的整数。因此，输出向量长度是输入向量长度的 1/M 倍。

- 当**在位压缩后，将得到的整数值视为**有符号，该模块将每组 M 比特映射到输出值是 [-2^(M-1) , 2^(M-1)-1] 范围内的整数。

## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/BittoIntegerConverter.mo">BittoIntegerConverter.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/BittoIntegerConverter/2.png')" style="width: 500px; border:black 1px solid;">

本示例在使用默认参数的情况下，展示了如何使用 Bit to Integer Converter 模块将输入的 6×1 二进制列向量转成对应的整数。

## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量|一维数组 | 列向量 </div></summary>
</details>
<div class="details-content">

输入信号，指定输入宽度为每个整数的位数(M)整数倍的标量、一维数组或列向量。输入值必须是值为 0 或 1。


**数据类型：double | float | int8 | uint8 | int16 | uint16 | int32 | uint32 | boolean**

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 一维数组 | 列向量 </div></summary>
</details>
<div class="details-content">
输出信号，以整数标量、一维数组或列向量的形式返回。在二进制转换时，可根据参数指定是否将输入位视为无符号或有符号。

**数据类型：double | float | int8 | uint8 | int16 | uint16 | int32 | uint32**

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>每个整数的位数(M)<div>3 (默认) | 范围在 [1,32] 内的整数</div></summary>
</details>
<div class="details-content">


输入映射到输出中，指定对输入信号每隔 M 位进行二进制转整数。

</div>
</div>

<div class="details-box">
<details open>
<summary>输入位顺序<div>最高有效位优先(默认) | 最低有效位优先</div></summary>
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

指定输入信号是否应视为有符号或无符号处理。此参数设置决定哪些输出数据类型选项可选。

</div>
</div>

<div class="details-box">
<details open>
<summary>输出数据类型<div>与输入相同 | double | float | int8 | uint8 | int16 | uint16 | int32 | uint32</div></summary>
</details>
<div class="details-content">


- 如果**在位压缩后，将得到的整数值视为**无符号，输出数据类型选择为：

  与输入相同 | double | float | int8 | uint8 | int16 | uint16 | int32 | uint32

- 如果**在位压缩后，将得到的整数值视为**有符号，输出数据类型选择为：

  与输入相同 | double | float | int8 | int16 | int32

  其中：与输入相同-该模块根据输入数据类型确定输出数据类型。

</div>
</div>

## 版本历史记录

- 在 2025b 推出

### 限制信息

- 不支持定点

