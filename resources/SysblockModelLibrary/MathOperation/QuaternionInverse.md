# QuaternionInverse
---
&nbsp;

计算四元数的逆

- **库：** Sysblock / MathOperation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/QuaternionInverse/QuaternionInverse.png')" style="width: 100px; height: auto;">

## 描述

四元数求逆模块（Quaternion Inverse block）用于计算给定四元数的逆。

## 示例

计算四元数的逆。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperation/QuaternionInverse.mo">QuaternionInverse.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/QuaternionInverse/QuaternionInverse01.png')" style="width: 600px; ">


## 端口

### 输入

<div class="details-box">
<details open>
<summary>q — 四元数<div>四元数 | 四元数向量</div></summary>
</details>
<div class="details-content">

以[ q0 , r0 , ..., q1 , r1 , ... , q2 , r2 , ... , q3 , r3 , ...], 形式呈现的四元数，指定为四元数或四元数向量形式。

**数据类型：** double

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>Inv(q) — 四元数逆<div>四元数逆  | 四元数逆向量</div></summary>
</details>
<div class="details-content">

四元数的逆或者四元数逆构成的向量。

**数据类型：** double

</div>
</div>

<!-- ## 算法

四元数的形式为：

*q*=*q*0+**i***q*1+**j***q*2+**k***q*3.

四元数逆的形式为：
*q*−1=*q*0−**i***q*1−**j***q*2−**k***q*3*q*20+*q*21+*q*22+*q*23. -->

<!-- ## 参考文献

[1] Stevens, Brian L., Frank L. Lewis. *Aircraft Control and Simulation*, Second Edition. Hoboken, NJ: Wiley–Interscience. -->

<!-- ## 扩展功能 -->

<!-- 
### C/C++ Code Generation Generate C and C++ code using Simulink® Coder™. -->

 ## 版本历史 
<!-- 
**Introduced before R2006a** -->

- 在 2024b 之前推出

<!-- ### 限制信息
暂无 -->

## 另请参阅

[QuaternionRotation](QuaternionRotation.html) | [QuaternionNormalize](QuaternionNormalize.html) | [QuaternionNorm](QuaternionNorm.html) | [QuaternionMultiplication](QuaternionMultiplication.html) | [QuaternionModulus](QuaternionModulus.html) | [QuaternionDivision](QuaternionDivision.html) | [QuaternionConjugate](QuaternionConjugate.html)