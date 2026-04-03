# CrossProduct
---
&nbsp;

两个向量的叉积

- **库：** Sysblock / MathOperation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/CrossProduct/CrossProduct.png')" style="width: 100px; height: auto;">

## 描述
CrossProduct 模块返回两个 3×1 向量的叉积或向量积。

## 示例

返回两个向量的叉积。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperation/CrossProduct.mo">CrossProduct.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/CrossProduct/CrossProduct01.png')" style="width: 600px; ">

## 端口

### 输入

<div class="details-box">
<details open>
<summary>u1 — 第一个输入向量 三元素向量<div></div></summary>
</details>
<div class="details-content">

第一个输入向量，指定为三元素向量。

**数据类型:** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | fixed point

</div>
</div>

<div class="details-box">
<details open>
<summary>u2 — 第二个输入向量 三元素向量<div></div></summary>
</details>
<div class="details-content">

第二个输入向量，指定为三元素向量。

**数据类型:** float | double | int8 | int16| int32 | uint8 | uint16 | uint32 | fixed point

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>y — 输入向量的叉积 三元素向量<div></div></summary>
</details>
<div class="details-content">

输入向量的叉积，以三元素向量形式返回。

**数据类型:** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | fixed point 

</div>
</div>


<!-- ## 模块特性 -->
<!-- 部分特性暂无
| **数据类型**     | `Boolean` | `double` | `fixed point` | `half` | `integer` | `single` |
| ---------------- | ------------------------------------------------------------ |
| **直接馈通**     | `是`                                                         |
| **多维信号**     | `否`                                                         |
| **可变大小信号** | `否`                                                         |
| **过零检测**     | `否`                                                         | -->


<!-- ## 扩展功能 -->

<!-- ### C/C++ 代码生成
使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。 -->

## 版本历史记录 

- 在 2024b 之前推出

<!-- ## 另请参阅 -->
<!-- [Hermitian Transpose](https://ww2.mathworks.cn/help/simulink/slref/hermitiantranspose.html) | [Identity Matrix](https://ww2.mathworks.cn/help/simulink/slref/identitymatrix.html) | [IsSymmetric](https://ww2.mathworks.cn/help/simulink/slref/issymmetric.html) | [IsTriangular](https://ww2.mathworks.cn/help/simulink/slref/istriangular.html) | [Matrix Square](https://ww2.mathworks.cn/help/simulink/slref/matrixsquare.html) | [Transpose](https://ww2.mathworks.cn/help/simulink/slref/transpose.html) 

### 主题                                                      
[基本运算的兼容数组大小](https://ww2.mathworks.cn/help/matlab/matlab_prog/compatible-array-sizes-for-basic-operations.html)     
[MATLAB® 矩阵运算](https://ww2.mathworks.cn/help/matlab/matlab_prog/vectorization.html#btjk58d-1)  -->
                                             
