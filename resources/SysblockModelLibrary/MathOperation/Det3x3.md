# Det3x3
---
&nbsp;

计算矩阵的行列式

- **库：** Sysblock / MathOperation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/Abs/Abs.png')" style="width: 100px; height: auto;">

## 描述

Det3x3 模块计算输入矩阵的行列式。

## 示例

计算一个 3x3 矩阵的行列式。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperation/Det3x3.mo">Det3x3.mo</helpButton>。


<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/Det3x3/Det3x301.png')" style="width: 600px; ">

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/Det3x3/Det3x302.png')" style="width: 600px; ">


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入矩阵 3×3 矩阵<div></div></summary>
</details>
<div class="details-content">

输入矩阵，指定为 3×3 矩阵。

**数据类型:** double

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 行列式标量<div></div></summary>
</details>
<div class="details-content">

行列式，输出为标量。

**数据类型:** double

</div>
</div>


## 算法

输入矩阵的形式为：

$$
A = \left[\matrix{  \ A11 & A12 & A13\\  \ A21 & A22 & A23\\  \ A31 & A32 & A33\\ }\right]
$$


矩阵的行列式的形式为：

det(A)=A11(A22A33−A23A32)−A12(A21A33−A23A31)+A13(A21A32−A22A31)



<!-- ## 扩展功能 -->


<!-- 
### C/C++ Code Generation Generate C and C++ code using Simulink® Coder™. -->

## 版本历史记录

- 在 2024b 之前推出

<!-- ### 限制信息 -->


## 另请参阅

[AdjointOf3x3Matrix](Adjointof3x3Matrix.html) | [Create3x3Matrix](Create3x3Matrix.html)