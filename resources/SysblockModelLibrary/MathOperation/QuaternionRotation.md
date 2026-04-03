# QuaternionRotation
---
&nbsp;

求四元数旋转向量

- **库：** Sysblock / MathOperation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/QuaternionRotation/QuaternionRotation.png')" style="width: 100px; height: auto;">

## 描述

四元数旋转模块（Quaternion Rotation block）用于计算初始向量 vec 经过四元数 q 的被动旋转后得到的结果向量，并返回最终向量（即旋转后的向量或旋转后向量构成的向量）。

## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperation/QuaternionRotation.mo">QuaternionRotation.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/QuaternionRotation/QuaternionRotation01.png')" style="width: 600px; ">


## 端口

### 输入

<div class="details-box">
<details open>
<summary>q — 四元数<div>四元数 | 向量</div></summary>
</details>
<div class="details-content">

以 [q0, r0, ..., q1, r1, ... , q2, r2, ... , q3, r3, ...] 形式呈现的四元数，指定为四元数或四元数向量形式。

**数据类型：** double

</div>
</div>

<div class="details-box">
<details open>
<summary>vec — 初始向量<div>向量 | 向量组</div></summary>
</details>
<div class="details-content">

以 [v1, u1, ... , v2, u2, ... , v3, u3, ...] 形式呈现的初始向量或向量组。

**数据类型：** double

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>vec_rot — 最终四元数<div>旋转后的四元数 | 旋转后四元数向量</div></summary>
</details>
<div class="details-content">

最终向量或旋转后向量构成的向量。

**数据类型：** double

</div>
</div>


<!-- ## 参考文献 -->

<!-- [1] Stevens, Brian L., Frank L. Lewis. *Aircraft Control and Simulation*, Second Edition. Hoboken, NJ: Wiley–Interscience.

[2] Diebel, James. "Representing Attitude: Euler Angles, Unit Quaternions, and Rotation Vectors." Stanford University, Stanford, California, 2006. -->

<!-- ## 扩展功能 -->



<!-- ### C/C++ Code Generation Generate C and C++ code using Simulink® Coder™. -->

## 版本历史 

- 在 2024b 之前推出

<!-- ### 限制信息
暂无 -->

## 另请参阅

[QuaternionConjugate](QuaternionConjugate.html) | [QuaternionDivision](QuaternionDivision.html) | [QuaternionInverse](QuaternionInverse.html) | [QuaternionMultiplication](QuaternionMultiplication.html) | [QuaternionNorm](QuaternionNorm.html) | [QuaternionNormalize](QuaternionNormalize.html)

<!-- ### 主题 -->

<!-- - [Passive Transformations](https://ww2.mathworks.cn/help/aeroblks/about-aerospace-coordinate-systems.html#mw_6c57d18c-77d4-436f-aa27-b08932edf23d) -->