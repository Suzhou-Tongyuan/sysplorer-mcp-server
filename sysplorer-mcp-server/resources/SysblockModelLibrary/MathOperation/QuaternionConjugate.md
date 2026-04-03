# QuaternionConjugate
---
&nbsp;

计算四元数的共轭

- **库：** Sysblock / MathOperation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/QuaternionConjugate/QuaternionConjugate.png')" style="width: 100px; height: auto;">


## 描述

四元数共轭模块（Quaternion Conjugate block）用于计算给定四元数的共轭

## 示例
计算一个四元数的共轭。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperation/QuaternionConjugate.mo">QuaternionConjugate.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/QuaternionConjugate/QuaternionConjugate01.png')" style="width: 600px; ">


## 端口

### 输入

<div class="details-box">
<details open>
<summary>q — 输入 输入四元数<div>四元数 | 四元数向量</div></summary>
</details>
<div class="details-content">

以 [q0, r0, …, q1, r1, …, q2, r2, …, q3, r3, …] 形式呈现的四元数，指定为四元数或向量形式。

**数据类型：** double

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>q — 四元数共轭<div>四元数共轭 | 四元数共轭向量</div></summary>
</details>
<div class="details-content">

以 [q0, r0, …, q1, r1, …, q2, r2, …, q3, r3, …] 形式呈现的四元数共轭，以四元数或向量形式返回。

**数据类型：** double 

</div>
</div>


<!-- ## 算法 -->


<!-- ## 参考文献 -->

<!-- [1] Stevens, Brian L., Frank L. Lewis. *Aircraft Control and Simulation*, Second Edition. Hoboken, NJ: Wiley–Interscience. -->

<!-- ## 扩展功能 -->



<!-- ### C/C++ Code Generation Generate C and C++ code using Simulink® Coder™. -->

## 版本历史记录

- 在 2024b 之前推出


<!-- ### 限制信息
暂无 -->

## 另请参阅

[QuaternionDivision](QuaternionDivision.html) | [QuaternionInverse](QuaternionInverse.html) | [Quaternion Modulus](QuaternionModulus.html) | [QuaternionMultiplication](QuaternionMultiplication.html) | [QuaternionNorm](QuaternionNorm.html) | [QuaternionRotation](QuaternionRotation.html) | [QuaternionNormalize](QuaternionNormalize.html)