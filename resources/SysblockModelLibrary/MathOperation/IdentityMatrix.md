# IdentityMatrix
---
&nbsp;

生成 1 在主对角线上的矩阵，并在其他位置生成 ground 值


- **库：** Sysblock / MathOperation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/IdentityMatrix/IdentityMatrix.png')" style="width: 100px; height: auto;">

## 描述

IdentityMatrix 模块输出一个单位矩阵，该块生成一个正方形或矩形矩阵，其中 1 位于主对角线上，其他位置为 0。

## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperation/IdentityMatrix.mo">IdentityMatrix.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/IdentityMatrix/IdentityMatrix01.png')" style="width: 600px; ">


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

用于确定输出矩阵维度的输入信号，指定为标量、向量或矩阵。当输入信号是 M×N 矩阵时，模块会生成一个 M×N 矩阵输出，其采样周期与输入相同。输入矩阵中的值将被忽略。

#### 依赖

要启用此端口，请选中**从输入端口继承端口属性**复选框。

**数据类型:** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | fixed point

</div>
</div>



### 输出

<div class="details-box">
<details open>
<summary>y — 单位矩阵<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

单位矩阵，指定为标量、向量或矩阵。

**数据类型:** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | fixed point

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>输出端口从输入端口继承属性 — 输出端口从输入端口继承属性的选项<div>off（默认） | no</div></summary>
</details>
<div class="details-content">

选中此复选框，输出端口将从输入端口继承其维度、采样周期和数据类型。否则，请清除此复选框。

</div>
</div>


<!-- 
#### Programmatic Use

| **Block Parameter:** `InheritOutputPortAttributes` |
| -------------------------------------------------- |
| **Type:** character vector                         |
| **Values:** `'on'` | `'off'`                       |
| **Default:** `'off'`                               | -->

<div class="details-box">
<details open>
<summary>输出维度 — 输出矩阵<div>[5,5] (默认 ) | 标量 | 二元素向量</div></summary>
</details>
<div class="details-content">

输出矩阵中的行数和列数。您可以指定：

- 一个正整数标量 M，用于创建 M×M 的正方形输出。
- 一个正整数向量 [M N]，用于创建 M×N 输出。

#### 依赖

要启用此参数，请清除**输出端口从输入端口继承属性**复选框。

</div>
</div>



<!-- #### Programmatic Use

| **Block Parameter:** `OutputDimensions`  |
| ---------------------------------------- |
| **Type:** character vector               |
| **Values:** scalar \| two-element vector |
| **Default:** `'5'`                       |  -->


<div class="details-box">
<details open>
<summary>输出数据类型 — 输出数据类型<div>double (默认) | float | int8 | uint8 | int16 | uint16 | int32 | uint32 | boolean | fixdt(1,16,0) | Inherit: backPropagation</div></summary>
</details>
<div class="details-content">

指定此模块的输出数据类型。您可以选择以下选项之一：

- 继承数据类型的规则，例如 Inherit: backPropagation。当您选择此选项时，输出数据类型和缩放与下一个下游数据块的数据类型和缩放匹配。
- 内置数据类型，例如 double。
- 计算结果为有效数据类型的表达式，例如 fixdt（1,16）。

</div>
</div>




<!-- #### 编程用法

| **Block Parameter**: `OutDataTypeStr`                        |
| ------------------------------------------------------------ |
| **Type**: character vector                                   |
| **Values**: `'Inherit: Inherit via back propagation'` | `'double'` | `'single'` | `'half'` | `'int8'` | `'uint8'` | `'int16'` | `'uint16'` | `'int32'` | `'uint32'` | `'int64'` | `'uint64'` | | `'fixdt(1,16,0)'` | `'<data type expression>'` |
| **Default**: `'double'`                                      | -->

<div class="details-box">
<details open>
<summary>模式 — 数据类型模式<div>Inherit (默认) | Builtin | FixedPoint </div></summary>
</details>
<div class="details-content">

选择要如何指定 **输出数据类型** 的数据类型属性。您可以选择：

- 继承 — 指定用于继承数据类型的规则，例如继承：与输入相同。
- 内置— 指定内置数据类型，例如 double。
- 定点 - 指定数据类型的 fixed-point 属性。

</div>
</div>


<div class="details-box">
<details open>
<summary>有符号 — 指定定点数据<div>有符号 (默认) | 无符号</div></summary>
</details>
<div class="details-content">

指定定点数据是有符号的还是无符号的。有符号数据可以表示正值和负值，但无符号数据仅表示正值。

</div>
</div>

<div class="details-box">
<details open>
<summary>缩放 — 缩放定点数据<div>Best precision 的方法（默认） | 二进制点</div></summary>
</details>
<div class="details-content">

指定缩放定点数据的方法，以避免溢出情况并最大限度地减少量化误差。
#### 依赖

要启用此参数，请将**模式**设置为**定点**。

</div>
</div>

<div class="details-box">
<details open>
<summary>字长 — 包含量化整数<div>16 的字的位大小（默认） |从 2 到 65,535 的整数</div></summary>
</details>
<div class="details-content">

指定将量化整数保存为 2 到 65,535 之间的正整数的字的位大小。

#### 依赖


要启用此参数，请将**模式**设置为**定点**。

</div>
</div>

<div class="details-box">
<details open>
<summary>数据类型覆盖 — 数据类型覆盖模式<div>Inherit（默认） | off</div></summary>
</details>
<div class="details-content">

选择此信号的数据类型覆盖模式。您可以选择：

- Inherit — 继承为模型指定的数据类型覆盖设置。
- Off - 忽略为模型指定的数据类型覆盖设置，并使用您指定的定点数据类型。

#### 依赖

要启用此参数，请将**模式**设置为**内置**或**定点**。

</div>
</div>


<!-- 暂无

### **采样周期** - 输出采样周期 `1` (默认值) | 标量

输出的离散采样周期，以实数形式表示。

#### 依赖

要启用此参数，请清除“**从输入端口继承输出端口属性**”复选框。

#### 编程用法

| **参数:** `SampleTime` |
| --------------------------------- |
| **类型:** 字符向量      |
| **值:** 标量或向量     |
| **默认值:** `'1'`                | -->

<!-- ## 模块特性 -->

<!-- 暂无
| **数据类型**               | `Boolean` | `double` | `fixed point` | `integer` | `float` |
| ---------------------------- | ------------------------------------------------------------ |
| **直接反馈**       | `否`                                                         |
| **多维信号** | `否`                                                         |
| **可变大小信号**    | `否`                                                         |
| **过零检测**  | `否`                                                         | -->

<!-- ## 扩展功能 -->

<!-- ### C/C++ Code Generation Generate C and C++ code using Simulink® Coder™. -->


## 扩展功能

- 在 2024b 之前推出

### 限制信息
不支持部分

采样周期 —  输出采样周期

## 另请参阅

[CrossProduct](CrossProduct.html) 

<!-- 
[eye]() | [Expand Scalar]() | [Hermitian Transpose]() | [IsSymmetric]() | [IsTriangular]() | [Matrix Square]() | [Transpose]() -->
