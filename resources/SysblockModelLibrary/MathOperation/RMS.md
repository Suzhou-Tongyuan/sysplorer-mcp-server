# RMS
---
&nbsp;

按照输入信号的指定维度计算均方根。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/RMS/1.jpg')" style="width: 100px; height: auto; transform: scale(1);">

**库：** Sysblock 模块库 / MathOperation

## 描述

RMS模块通过以下公式对输入信号进行数学运算来计算其均方根值；

$
RMS^2 = (x1^2 + x2^2 + ... + xn^2)/N
$

其中 x1、x2....xn 是模块输入，N 是模块输入的元素个数，RMS 是输出。

## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperation/RMS.mo">RMS.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/RMS/2.png')" style="width: 500px; height: auto; transform: scale(1);">

仿真结果如下：

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/RMS/3.png')" style="width: 500px; height: auto; transform: scale(1);border: 1px solid black;">

### 示例说明

- constant模块：生成 2x2 矩阵常量值 [1,2;3,4]。
- RMS模块：将输入信号按元素进行均方根计算。
- Scope 模块：用于显示模型的输出结果。


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入端口<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

输入信号，向该输入信号进行均方根计算以创建输出信号。

**数据类型：** double | float | int8 | uint8 | int16 | uint16 | int32 | uint32 | int64 | fixedpoint

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 输出端口<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

输出信号。

**数据类型：** double | float | int8 | uint8 | int16 | uint16 | int32 | uint32 | int64 | fixedpoint

</div>
</div>


## 参数

### 按元素处理

将输入信号所有 N 个元素，作为 x1,x2,...xn 传入上面的 RMS 计算公式中，得出 RMS 模块输出值。

### 按行处理

将输入信号按行处理进行均方根运算，如 [1,2;3,4] 按行处理，传入上面的 RMS 计算公式中运算后，得到 RMS[1,1]（矩阵第一行 [1,2] 的运算结果）和 RMS[2,1]（矩阵第二行 [3,4] 的运算结果）。

### 按列处理

将输入信号按列处理进行均方根运算，如 [1,2;3,4] 按列处理，传入上面的 RMS 计算公式中运算后，得到 RMS[1,1] （矩阵第一列 [1;3] 的运算结果）和 RMS[1,2]（矩阵第二列 [2,4] 的运算结果）。

### 按选定维度处理

将输入信号按选定维度处理进行均方根运算，如 [1,2;3,4] 按选定维度处理（1 表示一维，2 表示二维），传入上面的 RMS 计算公式中运算后得到对应维度的运算结果。

## 版本历史记录

- 在 2025a 推出


### 限制信息

- 不支持布尔、总线、枚举类型输入/输出。
- 暂不支持 Runging RMS 模式。