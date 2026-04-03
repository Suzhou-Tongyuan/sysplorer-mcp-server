# QuaternionDivision
---
&nbsp;

用一个四元数除以另一个四元数。

- **库：** Sysblock / MathOperation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/QuaternionDivision/QuaternionDivision.png')" style="width: 100px; height: auto;">

## 描述

四元数除法模块（Quaternion Division block）用于将给定的一个四元数除以另一个四元数。使用按照标量优先约定定义的四元数。输出结果是除法运算得到的四元数或者是除法运算所得四元数构成的向量。

## 示例

用一个四元数除以另一个四元数。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperation/QuaternionDivision.mo">QuaternionDivision.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/QuaternionDivision/QuaternionDivision01.png')" style="width: 600px; ">

## 端口

### 输入

<div class="details-box">
<details open>
<summary>q — 被除数四元数<div> 四元数 | 四元数向量</div></summary>
</details>
<div class="details-content">

以 [*q*0, *p*0, ..., *q*1, *p*1, ... , *q*2, *p*2, ... , *q*3, *p*3, ...],  形式呈现的被除数四元数，指定为四元数或四元数向量形式。

**数据类型：** double

</div>
</div>

<div class="details-box">
<details open>
<summary>r — 除数四元数<div> 四元数 | 四元数向量</div></summary>
</details>
<div class="details-content">

以 [*s*0, *r*0, ..., *s*1, *r*1, ... , *s*2, *r*2, ... , *s*3, *r*3, ...] 形式呈现的除数四元数，指定为四元数或四元数向量形式。

**数据类型：** double

</div>
</div>



### 输出


<div class="details-box">
<details open>
<summary>q/r — 输出四元数<div> 四元数 | 向量</div></summary>
</details>
<div class="details-content">

除法运算得到的输出四元数或者是由此产生的四元数向量。

**数据类型：** double

</div>
</div>

<!-- ## 算法
四元数的形式如下：

*q*=*q*0+**i***q*1+**j***q*2+**k***q*3

以及

*r*=*r*0+**i***r*1+**j***r*2+**k***r*3.

除法运算所得的四元数具有如下形式：

*t*=*q**r*=*t*0+**i***t*1+**j***t*2+**k***t*3,

其中：

*t*0=(*r*0*q*0+*r*1*q*1+*r*2*q*2+*r*3*q*3)*r*20+*r*21+*r*22+*r*23*t*1=(*r*0*q*1−*r*1*q*0−*r*2*q*3+*r*3*q*2)*r*20+*r*21+*r*22+*r*23*t*2=(*r*0*q*2+*r*1*q*3−*r*2*q*0−*r*3*q*1)*r*20+*r*21+*r*22+*r*23*t*3=(*r*0*q*3−*r*1*q*2+*r*2*q*1−*r*3*q*0)*r*20+*r*21+*r*22+*r*23 -->



<!-- ## 参考文献 -->

<!-- [1] Stevens, Brian L., Frank L. Lewis. *Aircraft Control and Simulation*, Second Edition. Hoboken, NJ: Wiley–Interscience. -->

<!-- ## 扩展功能 -->



<!-- ### C/C++ Code Generation Generate C and C++ code using Simulink® Coder™. -->

## 版本历史

- 在 2024b 之前推出

<!-- ### 限制信息
暂无 -->

## 另请参阅

[QuaternionConjugate](QuaternionConjugate.html) | [QuaternionInverse](QuaternionInverse.html) | [QuaternionModulus](QuaternionModulus.html) | [QuaternionMultiplication](QuaternionMultiplication.html) | [QuaternionNorm](QuaternionNorm.html) | [QuaternionNormalize](QuaternionNormalize.html) | [QuaternionRotation](QuaternionRotation.html)