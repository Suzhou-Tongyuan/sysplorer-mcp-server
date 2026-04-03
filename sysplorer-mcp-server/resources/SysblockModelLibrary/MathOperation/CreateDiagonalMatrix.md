# CreateDiagonalMatrix
---
&nbsp;

从对角线元素创建方形对角矩阵

- **库：** Sysblock / MathOperation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/CreateDiagonalMatrix/CreateDiagonalMatrix.png')" style="width: 100px; height: auto;">

## 描述

CreateDiagonalMatrix 模块使用长度为 M 向量输入 D 中包含的元素填充 M×M 矩阵输出的对角线。对角线外的元素为零。

```
A = diag(D)		
```

## 示例

从对角线元素创建方形对角矩阵。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperation/CreateDiagonalMatrix.mo">CreateDiagonalMatrix.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/CreateDiagonalMatrix/CreateDiagonalMatrix01.png')" style="width: 600px; ">

## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号向量<div></div></summary>
</details>
<div class="details-content">

Input 转换为对角矩阵，指定为 M 元素向量。

**数据类型:** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | Boolean | fixed point

</div>
</div>



<!-- **复数支持:** Yes -->

### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号矩阵<div></div></summary>
</details>
<div class="details-content">

输出指定为 M×M 矩阵，其中 M 是输入向量的长度。

输出等效于：


```
A = diag(D)		
```

**数据类型:** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | Boolean | fixed point

</div>
</div>


<!-- **复数支持:** Yes -->



<!-- ## 模块特性 -->

<!--部分功能暂无 
| **数据类型**               | `Boolean` \| `double` \| `fixed point` \| `integer` \| `single` |
| ---------------------------- | ----------------------------------------------------------- |
| **直接馈入**       | `否`                                                        |
| **多维信号** | `否`                                                        |
| **可变大小信号**    | `否`                                                        |
| **过零检测**  | `否`                                                        | -->

<!-- ## 扩展功能 -->


<!-- 
### C/C++ Code Generation Generate C and C++ code using Simulink® Coder™.

Generated code relies on the `memcpy` or `memset` function (`string.h`) under certain conditions.



### Fixed-Point Conversion Design and simulate fixed-point systems using Fixed-Point Designer™. -->

## 版本历史记录 

- 在 2024b 之前推出

<!-- 
**Introduced before R2006a**


### R2021b: Create Diagonal Matrix Block Moved to Simulink Matrix Operations Library

The Create Diagonal Matrix block has been moved from the **DSP System Toolbox** > **Math Functions** > **Matrices and Linear Algebra** > **Matrix Operations** library to the **Simulink** > **Matrix Operations**library. All existing models continue to work. -->

<!-- ### 限制信息 -->


<!-- ## 另请参阅 -->


