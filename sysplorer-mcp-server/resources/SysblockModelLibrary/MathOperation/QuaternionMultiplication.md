# QuaternionMultiplication
---
&nbsp;

计算两个四元数的乘积

- **库：** Sysblock / MathOperation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/QuaternionMultiplication/QuaternionMultiplication.png')" style="width: 100px; height: auto;">

## 描述

四元数乘法模块（Quaternion Multiplication block）用于计算两个给定四元数的乘积。

## 示例

计算两个四元数的乘积。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperation/QuaternionMultiplication.mo">QuaternionMultiplication.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/QuaternionMultiplication/QuaternionMultiplication01.png')" style="width: 600px; ">


## 端口

### 输入

<div class="details-box">
<details open>
<summary>q — 第一个四元数<div>四元数 | 四元数向量</div></summary>
</details>
<div class="details-content">

第一个四元数，指定为四元数或四元数向量形式。四元数向量的形式如下, 其中 q 和 p 为四元数：

```
[ q0 , p0 , ..., q1 , p1 , ... , q2 , p2 , ... , q3 , p3 , ...]
```

**数据类型：** double

</div>
</div>

<div class="details-box">
<details open>
<summary>r — 第二个四元数<div>四元数 | 四元数向量</div></summary>
</details>
<div class="details-content">

第二个四元数，指定为四元数或四元数向量形式。四元数向量的形式如下（其中 s 和 r 为四元数）：

```
[ s0 , r0 , ..., s1 , r1 , ... , s2 , r2 , ... , s3 , r3 , ...]
```

**数据类型：** double

</div>
</div>



### 输出

<div class="details-box">
<details open>
<summary>q*r — 乘积<div>向量 | 四元数乘积向量</div></summary>
</details>
<div class="details-content">

两个四元数的乘积，以向量或四元数乘积向量的形式输出。

**数据类型：** double

</div>
</div>


<!-- ## 算法

该模块使用以下形式的四元数

*q*=*q*0+**i***q*1+**j***q*2+**k***q*3

以及

*r*=*r*0+**i***r*1+**j***r*2+**k***r*3.

四元数乘积具有如下形式：

*t*=*q*×*r*=*t*0+**i***t*1+**j***t*2+**k***t*3,

其中：

*t*0=(*r*0*q*0−*r*1*q*1−*r*2*q*2−*r*3*q*3)*t*1=(*r*0*q*1+*r*1*q*0−*r*2*q*3+*r*3*q*2)*t*2=(*r*0*q*2+*r*1*q*3+*r*2*q*0−*r*3*q*1)*t*3=(*r*0*q*3−*r*1*q*2+*r*2*q*1+*r*3*q*0) -->



<!-- ## 参考文献

[1] Stevens, Brian L., Frank L. Lewis. *Aircraft Control and Simulation*, Second Edition. Hoboken, NJ: Wiley–Interscience. -->

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

[QuaternionConjugate](QuaternionConjugate.html) | [QuaternionDivision](QuaternionDivision.html) | [QuaternionInverse](QuaternionInverse.html) | [QuaternionModulus](QuaternionModulus.html) | [QuaternionNorm](QuaternionNorm.html) | [QuaternionNormalize](QuaternionNormalize.html) | [QuaternionRotation](QuaternionRotation.html)

<!-- ### 主题 -->

