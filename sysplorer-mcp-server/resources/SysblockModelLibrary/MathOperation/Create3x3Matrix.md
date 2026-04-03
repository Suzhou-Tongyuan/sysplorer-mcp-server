# Create3x3Matrix
---
&nbsp;

根据 9 个输入值创建 3×3 矩阵

- **库：** Sysblock / MathOperation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/Create3x3Matrix/Create3x3Matrix.png')" style="width: 100px; height: auto;">

## 描述

Create3x3Matrix 模块根据 9 个输入值创建一个 3×3 矩阵，其中每个输入对应于矩阵的一个元素。

输出矩阵的形式为

$$
A = \left[\matrix{  \ A11 & A12 & A13\\  \ A21 & A22 & A23\\  \ A31 & A32 & A33\\ }\right]
$$


## 示例
根据 9 个输入值创建 3×3 矩阵。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperation/Create3x3Matrix.mo">Create3x3Matrix.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/Create3x3Matrix/Create3x3Matrix01.png')" style="width: 600px; ">


## 端口

### 输入

<div class="details-box">
<details open>
<summary>A11 — 矩阵矩阵元素的第一行、第一列<div></div></summary>
</details>
<div class="details-content">

矩阵的第一行、第一列，指定为矩阵元素。

**示例:** 1

**数据类型:** double

</div>
</div>


<div class="details-box">
<details open>
<summary>A12 — 矩阵元素的第一行、第二列<div></div></summary>
</details>
<div class="details-content">

矩阵的第一行，第二列，指定为矩阵元素。

**示例:** 2

**数据类型:** double

</div>
</div>

<div class="details-box">
<details open>
<summary>A13 — 矩阵矩阵元素的第一行、第三列<div></div></summary>
</details>
<div class="details-content">

矩阵的第一行、第三列，指定为矩阵元素。

**示例:** 3

**数据类型:** double

</div>
</div>


<div class="details-box">
<details open>
<summary>A21 — 矩阵元素的第二行、第一列<div></div></summary>
</details>
<div class="details-content">

第二行，矩阵的第一列，指定为矩阵元素。

**示例:** 4

**数据类型:** double

</div>
</div>


### **A22** — 矩阵元素的第二行、第二列

<div class="details-box">
<details open>
<summary>A22 — 矩阵元素的第二行、第二列<div></div></summary>
</details>
<div class="details-content">

矩阵的第二行，第二列，指定为矩阵元素。

**示例:** 5

**数据类型:** double

</div>
</div>


<div class="details-box">
<details open>
<summary>A23 — 矩阵矩阵元素的第 2 行、第 3 列<div></div></summary>
</details>
<div class="details-content">

矩阵的第二行、第三列，指定为矩阵元素。

**示例:** 6

**数据类型:** double

</div>
</div>


<div class="details-box">
<details open>
<summary>A31 — 矩阵元素的第 3 行、第 1 列<div></div></summary>
</details>
<div class="details-content">

第三行，矩阵的第一列，指定为矩阵元素。

**示例:** 7

**数据类型:** double

</div>
</div>


<div class="details-box">
<details open>
<summary>A32 — 矩阵矩阵元素的第 3 行、第 2 列<div></div></summary>
</details>
<div class="details-content">

矩阵的第三行，第二列，指定为矩阵元素。

**示例:** 8

**数据类型:** double

</div>
</div>

<div class="details-box">
<details open>
<summary>A33 — 矩阵矩阵元素的第 3 行、第 3 列<div></div></summary>
</details>
<div class="details-content">

矩阵的第三行、第三列，指定为矩阵元素。

**示例:** 9

**数据类型:** double

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>A — 矩阵 3×3 矩阵<div></div></summary>
</details>
<div class="details-content">

矩阵，输出为 3×3 矩阵。

**数据类型:** double

</div>
</div>

<!-- ## 扩展功能 -->



<!-- ### C/C++ Code Generation Generate C and C++ code using Simulink® Coder™. -->

## 版本历史记录

- 在 2024b 之前推出

<!-- ### 限制信息 -->
<!-- 无 -->

## 另请参阅

[Adjointof3x3Matrix](AdjointOf3x3Matrix.html) 