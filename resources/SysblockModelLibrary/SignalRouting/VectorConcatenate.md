# VectorConcatenate

串联相同数据类型的输入向量以进行迭代处理。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/VectorConcatenate/1.png')" style="width: 100px; height: auto; transform: scale(1);">

**库：** Sysblock 模块库 / SignalRouting

## 描述

- Vector Concatenate 模块会串联输入信号以创建一个非标量信号，可以使用子系统（例如，For Each 子系统）对其进行迭代处理。
- 可以使用多个 Vector Concatenate 模块分多个阶段创建输出信号，但结果是平面结构。

## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/VectorConcatenate.mo">VectorConcatenate.mo</helpButton>。

Vector Concatenate 模块串联它接收的向量，并创建变量输出。
将输入向量 [1,2] 和 [3,4] 串联起来以创建输出向量 [1,2,3,4]。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalRouting/VectorConcatenate/2.png')" style="width: 500px; height: auto; transform: scale(1);">

## 端口

### 输入

<div class="details-box">
<details open>
<summary>Port_1 — 要串联的第一个输入<div>标量 | 向量 | 矩阵 | 数组</div></summary>
</details>
<div class="details-content">

要串联的第一个输入，指定为标量、向量、矩阵或数组。
输入必须具有相同的数据类型。
仅当模式设置为多维数组时，才支持矩阵和数组输入。
当数据类型是 Bus 对象时，输入必须为非虚拟总线。  
数据类型: float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | Boolean | fixed point | enum | bus

</div>
</div>





<div class="details-box">
<details open>
<summary>Port_N — 要串联的第 *N* 个输入<div>标量 | 向量 | 矩阵 | 数组</div></summary>
</details>
<div class="details-content">

要串联的第 *N* 个输入，指定为标量、向量、矩阵或数组。
输入必须具有相同的数据类型。
仅当模式设置为多维数组时，才支持矩阵和数组输入。
依存关系: 要添加输入端口，请将输入的数目设置为大于或等于 2 的整数。  
数据类型: float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | Boolean | fixed point | enum | bus

</div>
</div>




### 输出
 
<div class="details-box">
<details open>
<summary>Port_1 — 输入信号的串联<div>标量 | 向量 | 矩阵 | 数组</div></summary>
</details>
<div class="details-content">

输入信号沿指定维度的串联，输出的数据类型与输入相同。

**数据类型:** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | Boolean | fixed point | enum | bus

</div>
</div>



## 参数


<div class="details-box">
<details open>
<summary>输入数目 — 输入端口的数目<div></div></summary>
</details>
<div class="details-content">

默认值为 2。

只能为正整数且不大于 65536。

</div>
</div>



<div class="details-box">
<details open>
<summary>模式 — 串联类型<div></div></summary>
</details>
<div class="details-content">

分为向量 | 多维数组，选择模块是以向量模式还是多维数组串联模式运行。
Vector Concatenate 模块的默认模式是向量。
选择向量时，模块将执行向量串联。
选择多维数组时，模块会执行矩阵串联。

| **模式设置** | **输入信号**                                                 | 输出信号                                                     |
| ------------ | :----------------------------------------------------------- | ------------------------------------------------------------ |
| 向量         | 1. 向量<br />2. 行向量（1 x M 矩阵）<br />3. 列向量（M x 1 矩阵）<br />4. 向量与行向量或列向量的组合 | 1. 当所有输入都是向量时，输出是向量<br />2. 如果输入是行向量或列向量，则输出分别是行向量或列向量 |
| 多维数组     | 任何维度的信号（标量、向量和矩阵）                           | 1. 输出始终都是数组<br />2. 对于维度较低的输入，尾部维度假定为 `1`。例如，如果输出是 3 维，输入为 `[2x2`（2 维），此模块会将输入视为 `[2x2x1]`<br />3. 串联会在使用串联维度参数指定的维度上进行 |

</div>
</div>


<div class="details-box">
<details open>
<summary>串联维度 — 沿其串联输入数组的输出维度<div></div></summary>
</details>
<div class="details-content">

为标量整数，指定沿哪个输出维度串联输入数组。
 - 垂直串联输入。垂直矩阵串联将输入矩阵上下堆叠在输出矩阵中。当模式设置为多维数组时，默认值为 1；
 - 水平串联输入。水平矩阵串联将输入矩阵并排放置在输出矩阵中。当插入 Matrix Concatenate 模块时，默认值为 2。


</div>
</div>
  

## 版本历史记录

- 在 2025a 推出

## 限制信息

- 输入数目只能为标量；

- 串联维度只能为标量。