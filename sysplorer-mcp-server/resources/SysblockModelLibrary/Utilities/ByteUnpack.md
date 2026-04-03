# ByteUnpack
---
将 uint8 向量转换为输入信号

**库：** Sysblock 模块库 / Utilities

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/ByteUnpack/ByteUnpack.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

ByteUnpack 模块接收 uint8 向量，并基于输入向量的内容将该向量转换为不同 Sysblock 数据类型的输出信号。您可以使用模块参数来指定输出信号的维度和数据类型，以及模块输出的各个向量中的数据对齐方式。
<!-- 由于 UDP 协议以 uint8 格式传输数据，因此您可以将此模块的输入连接到 [UDP Send]() 模块的输出，以使用此模块来重新格式化作为 UDP 数据包接收的数据，以便在模型中使用。 -->

## 示例

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/ByteUnpack.mo">ByteUnpack.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/ByteUnpack/2.png')" style="width: 750px; height: auto; transform: scale(0.8);">

### 示例说明

- Constant：生成一个 double 类型的整数；
- BytePack：将 Constant 模块的输出转换为 uint8 向量；
- ByteUnpack：将 uint8 向量转换为一个 double 类型的整数；
- Scope：显示转换后的整数信号。

## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 要转换的信号<div>向量</div></summary>
</details>
<div class="details-content">

uint8 类型的输入向量。

**数据类型：** uint8

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y1 — 转换后的信号数据<div>double 类型的信号 （默认） | 信号数据数组</div></summary>
</details>
<div class="details-content">

一种或多种数据类型的输入信号数组。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | fixedPoint | enum | bus

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>输出端口维度（元胞数组） — 模块输出信号的维度<div>{[1]} （默认） | 由数据维度设定组成的元胞数组</div></summary>
</details>
<div class="details-content">

以元胞数组形式指定模块输出的输出信号的维度。数组中的每个元素指定 Syslab size 函数为对应信号返回的维度。指定与模型中对应 [BytePack](BytePack.html) 模块所转换的数据对齐的维度。

例如，假设对应的 Byte Pack 模块指定以下输入端口数据类型：

```
 {'uint32','uint32','uint16','double','uint8','double','single'}
```

要指定标量和矩阵输出，您可以将**输出端口维度(元胞数组)** 参数设置为：

```
 {1,1,[2,4],[4,4],[2,2],1,[3,3]}
```

要对输出信号应用相同的维度，可以指定一个维度值。

</div>
</div>


<div class="details-box">
<details open>
<summary>输出端口数据类型(元胞数组) — 模块输出信号的数据类型<div>{'double'} （默认） | 由 Sysblock 数据类型组成的元胞数组</div></summary>
</details>
<div class="details-content">

以元胞数组形式指定模型中对应 BytePack 模块接收的单个输入信号的 Sysblock 数据类型。

例如，如果对应的 BytePack 模块指定以下输入端口数据类型，请为此参数指定相同的元胞数组。

```
 {'uint32','uint32','uint16','double','uint8','double','single'}
```

要对每个输出信号应用相同的数据类型，只需指定一次数据类型。

</div>
</div>


<div class="details-box">
<details open>
<summary>字节对齐方式 — 数据类型对齐方式的字节边界<div>1 （默认） | 2 | 4 | 8</div></summary>
</details>
<div class="details-content">

指定如何对齐输出数据的数据类型，以形成以字节为单位的 uint8 向量输入。指定与为模型中对应 [BytePack](BytePack.html) 模块指定的值匹配的对齐值。

例如，如果对应的 BytePack 模块将字节对齐设置为 2，则将此参数设置为 2。

</div>
</div>


## 版本历史记录

- 在 2024b 之前推出



## 另请参阅

[BytePack](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Utilities/BytePack.md)
 <!-- | [Byte Reversal](https://ww2.mathworks.cn/help/releases/R2022b/ecoder/ref/bytereversal.html) | [UDP Receive](https://ww2.mathworks.cn/help/releases/R2022b/ecoder/ref/udpreceive.html) -->