# ExtractBits
---
&nbsp;

将输入信号转换为 int32 类型，并输出选择的连续位

- **库:** Sysblock / LogicAndBitOperation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/ExtractBits/ExtractBits.png')" style="width:100px;border:black 1px solid;"> 

## 描述

ExtractBits 模块首先将输入信号转换为 int32 类型，然后从输入信号存储的数值中输出选择的连续位。使用**提取位**参数定义选择输出位的方法。

## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/ExtractBits_Demo.mo">ExtractBits.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/ExtractBits/ExtractBits_ex.png')" style="width:800px;border:black 1px solid;"> 

### 示例说明

- Constant 模块：生成实数或复数常量值信号，使用此模块提供常量值信号；
- Display 模块：显示输入信号值；
- ExtractBits 模块：将输入信号转换为 int32 类型，然后从输入信号的存储数值中输出选择的连续位。


### 仿真结果

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/ExtractBits/ExtractBits_res.png')" style="width:800px;border:black 1px solid;"> 


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量</div></summary>
</details>
<div class="details-content">

输入信号

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量</div></summary>
</details>
<div class="details-content">

输出信号

**数据类型：** int32

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>提取位 — 输出位的方式<div> “Upper half”（默认）| “Lower half” | “Range starting with most significant bit” | “Range ending with least significant bit” | “Range of bits” </div></summary>
</details>
<div class="details-content">

**Upper half**：输出一半的输入位，其中包含最高有效位；

**Lower half**：输出一半的输入位，其中包含最低有效位；

**Range starting with most significant bit**：输出一定数量的输入信号最高有效位；

**Range ending with least significant bit**：输出一定数量的输入信号最低有效位；

**Range of bits**：指定要输出的输入信号的一系列连续位；

</div>
</div>


<div class="details-box">
<details open>
<summary>比特数量 — 输出的比特数量<div> 0（标量）| 整数标量 </div></summary>
</details>
<div class="details-content">

指定输出的 bit 数量。（使用此参数，请将**提取位**参数设置为 “Range starting with most significant bit” 或者 “Range ending with least significant bit”）

</div>
</div>

<div class="details-box">
<details open>
<summary>比特数量 — 输出的比特数量<div> {0,7}（默认） | 二维向量 </div></summary>
</details>
<div class="details-content">

指定输出的 bit 范围。（参数值为 {start,end}，0 对应最低位。使用此参数，请将**提取位**参数设置为 “Range of bits”）

</div>
</div>

## 版本历史记录

- 在 2025a 之前推出

### 限制信息
输入数据类型均被转换为 int32 类型，输出数据类型为 int32，其他数据类型暂不支持。
