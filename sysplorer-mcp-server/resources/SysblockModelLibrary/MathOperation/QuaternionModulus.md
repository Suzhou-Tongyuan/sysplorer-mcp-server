# QuaternionModulus
---
&nbsp;

计算四元数的模


- **库：** Sysblock / MathOperation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/QuaternionModulus/QuaternionModulus.png')" style="width: 100px; height: auto;">

## 描述

四元数模值模块可计算给定四元数的幅值。

## 示例
计算一个四元数的模。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperation/QuaternionModulus.mo">QuaternionModulus.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/QuaternionModulus/QuaternionModulus01.png')" style="width: 600px; ">

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/QuaternionModulus/QuaternionModulus02.png')" style="width: 600px; ">

## 端口

### 输入

<div class="details-box">
<details open>
<summary>q — 四元数<div>四元数 | 四元数向量</div></summary>
</details>
<div class="details-content">

以 [ q0 , r0 , ..., q1 , r1 , ... , q2 , r2 , ... , q3 , r3 , ...], 形式呈现的四元数，指定为四元数或四元数向量形式。

**数据类型：** double

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>|q| — 四元数模<div>四元数模 | 四元数模向量</div></summary>
</details>
<div class="details-content">

四元数模或者四元数模构成的向量，形式为 [ |q|, |r|, ...]。

**数据类型：** double

</div>
</div>


## 算法

四元数的形式为：

q=q0+iq1+jq2+kq3

四元数模的形式为：

∣q∣=√q20+q21+q22+q23

<!-- ## 参考文献 -->

<!-- [1] Stevens, Brian L., Frank L. Lewis. *Aircraft Control and Simulation*, Second Edition. Hoboken, NJ: Wiley–Interscience. -->

<!-- ## 扩展功能 -->



<!-- ### C/C++ Code Generation Generate C and C++ code using Simulink® Coder™. -->

## 版本历史

- 在 2024b 之前推出

<!-- ### 限制信息
暂无 -->

## 另请参阅

[QuaternionConjugate](QuaternionConjugate.html) | [QuaternionRotation](QuaternionRotation.html) | [QuaternionNormalize](QuaternionNormalize.html) | [QuaternionNorm](QuaternionNorm.html) | [QuaternionMultiplication](QuaternionMultiplication.html) | [QuaternionInverse](QuaternionInverse.html) | [QuaternionDivision](QuaternionDivision.html)