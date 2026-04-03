# AdjointOf3x3Matrix
---
&nbsp;

计算输入矩阵的伴随矩阵

- **库：** Sysblock / MathOperation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/AdjointOf3x3Matrix/AdjointOf3x3Matrix.png')" style="width: 100px; height: auto;">

## 描述

AdjointOf3x3Matrix 模块计算伴随矩阵 对于输入矩阵。

## 示例

计算一个 3x3 矩阵的伴随矩阵。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperation/AdjointOf3x3Matrix.mo">AdjointOf3x3Matrix.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/AdjointOf3x3Matrix/AdjointOf3x3Matrix01.png')" style="width: 600px; ">


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入矩阵 3×3 矩阵<div></div></summary>
</details>
<div class="details-content">

输入矩阵，指定为 3×3 矩阵，以初始加速度单位表示。

**数据类型:** double

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 输出加速 3×3 矩阵<div></div></summary>
</details>
<div class="details-content">

输出加速度，以最终加速度单位以 3×3 矩阵形式返回。

**数据类型:** double

</div>
</div>


## 算法

输入矩阵的形式为

$$
A = \left[\matrix{  \ A11 & A12 & A13\\  \ A21 & A22 & A23\\  \ A31 & A32 & A33\\ }\right]
$$


矩阵的伴随形式为

$$
adj(A) = \left[\matrix{  +\left[
\matrix{
  \  A22 & A23\\
  \  A32 & A33\\ 
}
\right] & - \left[
\matrix{
  \  A12 & A13\\
  \  A32 & A33\\ 
}
\right]&  +\left[
\matrix{
  \  A12 & A13\\
  \  A22 & A23\\ 
}
\right]\\  \  -\left[
\matrix{
  \  A21 & A23\\
  \  A31 & A33\\ 
}
\right] &  +\left[
\matrix{
  \  A11 & A13\\
  \  A31 & A33\\ 
}
\right] & - \left[
\matrix{
  \  A11 & A13\\
  \  A21 & A23\\ 
}
\right]\\  \  +\left[
\matrix{
  \  A21 & A22\\
  \  A31 & A32\\ 
}
\right] & -\left[
\matrix{
  \  A11 & A12\\
  \  A31 & A32\\ 
}
\right]&  +\left[
\matrix{
  \  A11 & A12\\
  \  A21 & A22\\ 
}
\right]\\ }\right]
$$

<!-- ## 详细信息 -->

<!-- ## 扩展功能 -->
<!-- C/C++ Code Generation
Generate C and C++ code using Simulink® Coder™. -->
<!-- ## 版本历史记录 -->
<!-- Introduced before R2006a -->
<!-- ### 限制信息 -->

## 版本历史记录

- 在 2025a 推出

## 另请参阅

[Create3x3Matrix](Create3x3matrix.html)