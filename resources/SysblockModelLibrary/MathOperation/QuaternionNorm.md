# QuaternionNorm
---
&nbsp;

计算四元数的范数

- **库：** Sysblock / MathOperation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/QuaternionNorm/QuaternionNorm.png')" style="width: 100px; height: auto;">

## 描述

四元数范数模块（Quaternion Norm block）用于计算给定四元数的范数。

## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperation/QuaternionNorm.mo">QuaternionNorm.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/QuaternionNorm/QuaternionNorm01.png')" style="width: 600px; ">

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/QuaternionNorm/QuaternionNorm02.png')" style="width: 600px; ">

## 端口

### 输入

<div class="details-box">
<details open>
<summary>q — 四元数范数<div>四元数范数 | 四元数范数向量</div></summary>
</details>
<div class="details-content">

以 [ q0 , r0 , ..., q1 , r1 , ... , q2 , r2 , ... , q3 , r3 , ...] 形式呈现的四元数，指定为四元数范数或四元数范数向量形式。

**数据类型：** double

</div>
</div>



### 输出

<div class="details-box">
<details open>
<summary>norm(q) — 四元数范数<div>四元数范数 | 四元数范数向量</div></summary>
</details>
<div class="details-content">

四元数范数或者四元数范数构成的向量，形式为 [ norm(q), norm(r), ...]。

**数据类型：** double

</div>
</div>

## 算法

四元数的形式为：

q=q0+iq1+jq2+kq3

四元数范数的形式为：

norm(q)=q20+q21+q22+q23


<!-- ## 扩展功能 -->


<!-- 
### C/C++ Code Generation Generate C and C++ code using Simulink® Coder™. -->

## 版本历史

- 在 2024b 之前推出


<!-- 
**Introduced before R2006a** -->
<!-- ### 限制信息
暂无 -->

## 另请参阅
[QuaternionConjugate](QuaternionConjugate.html) | [QuaternionDivision](QuaternionDivision.html) | [QuaternionInverse](QuaternionInverse.html) | [QuaternionModulus](QuaternionModulus.html) | [QuaternionMultiplication](QuaternionMultiplication.html) | [QuaternionNormalize](QuaternionNormalize.html) | [QuaternionRotation](QuaternionRotation.html)