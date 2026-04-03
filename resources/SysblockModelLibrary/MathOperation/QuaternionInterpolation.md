# QuaternionInterpolation
---
&nbsp;

两个四元数之间的四元数插值


- **库：** Sysblock / MathOperation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/QuaternionInterpolation/QuaternionInterpolation.png')" style="width: 100px; height: auto;">

## 描述

四元数插值模块（Quaternion Interpolation block）通过区间分数来计算两个归一化四元数之间的四元数插值。

这两个归一化四元数是该模块计算四元数插值时的两个端点值。

## 示例

两个四元数之间的四元数插值。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperation/QuaternionInterpolation.mo">QuaternionInterpolation.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/QuaternionInterpolation/QuaternionInterpolation01.png')" style="width: 600px; ">


## 端口

### 输入

<div class="details-box">
<details open>
<summary>q0 — 第一个归一化四元数<div>4×1 向量 | 1×4 向量</div></summary>
</details>
<div class="details-content">

用于计算插值的第一个归一化四元数，该四元数必须是归一化四元数。

**数据类型：** double

</div>
</div>

<div class="details-box">
<details open>
<summary>q1 — 第二个归一化四元数<div>4×1 向量 | 1×4 向量</div></summary>
</details>
<div class="details-content">

用于计算插值的第二个归一化四元数，指定为 4×1 向量或 1×4 向量形式，该四元数必须是归一化四元数。

**数据类型：** double

</div>
</div>

<div class="details-box">
<details open>
<summary>f — 区间分数<div>标量</div></summary>
</details>
<div class="details-content">

用于计算四元数插值的区间分数。该值在 0 到 1 之间变化，它代表要计算的四元数的中间旋转情况，此分数会影响插值方法的旋转速度。

#### 依赖关系

区间分数会影响方法（Methods）参数中插值方法的旋转速度。

**数据类型：** double

</div>
</div>



### 输出

<div class="details-box">
<details open>
<summary>qf — 自然对数向量<div></div></summary>
</details>
<div class="details-content">

四元数的自然对数，以向量形式返回。

**数据类型：** double

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>Methods — 四元数插值方法<div>SLERP (默认) | LERP | NLERP</div></summary>
</details>
<div class="details-content">

用于计算四元数插值的四元数插值方法，具体说明如下：

- **SLERP**

  球形线性四元数插值方法。

- **LERP**

  线性四元数插值方法。

- **NLERP**

  归一化四元数线性插值方法。

#### 依赖关系

这些方法根据输入端口 f 的区间分数具有不同的旋转速度。

</div>
</div>


<!-- #### 编程用法

| **模块参数**: `method`                |
| -------------------------------------------- |
| **类型**: character vector                   |
| **取值**: `'SLERP'` | `'LERP'` | `'NLERP'` |
| **默认值**: `'SLERP'`                       | -->


<!-- #### 编程用法

| **模块参数**: `action`                  |
| ---------------------------------------------- |
| **类型**: character vector                     |
| **取值**: `'None'` | `'Warning'` | `'Error'` |
| **默认值**: `'Error'`                         | -->

<!-- ## 算法

*S**l**e**r**p*(*p*,*q*,*h*)=*p*(*p*∗*q*)*h* with *h*∈[0,1].

*L**E**R**P*(*p*,*q*,*h*)=*p*(1−*h*)+*q**h* with *h*∈[0,1].

With *r*=*L**E**R**P*(*p*,*q*,*h*),*N**L**E**R**P*(*p*,*q*,*h*)=*r*∣*r*∣. -->

<!-- ## 参考文献 -->

<!-- [1] Dam, Erik B., Martin Koch, Martin Lillholm. "Quaternions, Interpolation, and Animation." University of Copenhagen, København, Denmark, 1998. -->

<!-- ## 扩展功能 -->

<!-- ### C/C++ Code Generation Generate C and C++ code using Simulink® Coder™. -->

## 版本历史记录

- - 在 2025a 推出

<!-- **Introduced in R2016a** -->

<!-- ### 限制信息
暂无 -->

## 另请参阅

[QuaternionNormalize](QuaternionNormalize.html)