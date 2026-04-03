# FloatExtractBits
---
&nbsp;

用来指定浮点输入的输出位。

使用 "输出模式" 参数选择要输出的位。选择 "所有位"、"位范围"、""符号"、"尾数" 或 "指数" 将根据输入的 IEEE 754 标准表示输出对应的位。

**库：** Sysblock / LogicAndBitOperation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/FloatExtractBits/FloatExtractBits.png')" style="width:100px;border:black 1px solid;"> 

## 描述

FloatExtractBits 模块接受包含浮点数据的信号，并输出包含数据二进制表示的信号。有关这种二进制表示的更多信息，请参阅 IEEE 浮点算术标准。

## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/FloatExtractBits.mo">FloatExtractBits.mo</helpButton>。

本示例展示了如何使用 FloatExtractBits 输出包含数据二进制表示的信号。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/FloatExtractBits/Example_FloatExtractBits.png')" style="width:800px;border:black 1px solid;"> 

## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

​	包含浮点数据的信号，指定为标量、一维数组、向量、矩阵。

  **数据类型：** double | float

</div>

</div>

### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

​	数据的二进制表示形式，作为标量、矢量或矩阵返回。FloatExtractBits 根据输出模式参数计算定点输出。

  **数据类型：** int8 | int16 | int32 | int64 | uint8 | uint16 | uint32 | uint64 | fixed point

</div>

</div>

## 参数

<div class="details-box">
<details open>
<summary>输出模式 — 输出部分数据<div>所有位（默认） | 位范围 | 符号 | 尾数 | 指数</div></summary>
</details>
<div class="details-content">

​	以二进制形式输出部分数据，指定为：

- 所有位
- 位范围
- 符号
- 尾数
- 指数

</div>

</div>

<div class="details-box">
<details open>
<summary>位范围（[start end]，相对于 LSB 的从 0 开始的索引） — 返回的位范围<div>[0 15]（默认） | 向量</div></summary>
</details>
<div class="details-content">

​	要返回的信号的位范围，指定为向量。

</div>

</div>

## 版本历史记录

- 在 2025b 推出

## 限制信息

- 参数——“位范围”仅支持输入由两个元素组成的向量。
- 参数——“位范围”仅支持输入正整数。
- 参数——“位范围”起始索引必须小于等于结束索引，且结束索引不能超过输入位长。