# TrigonometricFunction
---
&nbsp;

指定应用于输入信号的三角函数

- **库：** Sysblock / MathOperation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/TrigonometricFunction/TrigonometricFunction.png')" style="width: 100px; height: auto;">

## 描述

TrigonometricFunction 模块执行常见的三角函数，并以 rad 或 rev 为单位输出结果。

### 支持的函数

可以从**函数**下拉列表中选择以下函数之一。

| 函数         | 描述                           | 数学表达式 | Syslab 等效函数                                             |
| :----------- | :----------------------------- | :--------- | :----------------------------------------------------------- |
| `sin`        | 输入信号的正弦                 | `sin(u)`   | [`sin`] |
| `cos`        | 输入信号的余弦                 | `cos(u)`   | [`cos`] |
| `tan`        | 输入信号的正切                 | `tan(u)`   | [`tan`] |
| `asin`       | 输入信号的反正弦               | `asin(u)`  | [`asin`] |
| `acos`       | 输入信号的反余弦               | `acos(u)`  | [`acos`] |
| `atan`       | 输入信号的反正切               | `atan(u)`  | [`atan`] |
| `atan2`      | 输入信号的四象限反正切         | `atan2(u)` | [`atan2`] |
| `sinh`       | 输入信号的双曲正弦             | `sinh(u)`  | [`sinh`] |
| `cosh`       | 输入信号的双曲余弦             | `cosh(u)`  | [`cosh`] |

<!--暂无
 | `tanh`       | 输入信号的双曲正切             | `tanh(u)`  | [`tanh`](https://ww2.mathworks.cn/help/releases/R2022b/matlab/ref/tanh.html) |
| `asinh`      | 输入信号的反双曲正弦           | `asinh(u)` | [`asinh`](https://ww2.mathworks.cn/help/releases/R2022b/matlab/ref/asinh.html) |
| `acosh`      | 输入信号的反双曲余弦           | `acosh(u)` | [`acosh`](https://ww2.mathworks.cn/help/releases/R2022b/matlab/ref/acosh.html) |
| `atanh`      | 输入信号的反双曲正切           | `atanh(u)` | [`atanh`](https://ww2.mathworks.cn/help/releases/R2022b/matlab/ref/atanh.html) |
| `sincos`     | 输入信号的正弦；输入信号的余弦 | —          | —                                                            |
| `cos + jsin` | 输入信号的复指数               | —          | —                                                            | -->
<!-- 
### CORDIC 逼近方法

CORDIC 是 COordinate Rotation DIgital Computer（坐标旋转数字计算方法）的缩写。基于 Givens 旋转的 CORDIC 算法是最节省硬件资源的可用算法之一，因为它只需进行迭代移位相加运算。有关详细信息，请参阅[详细信息](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/trigonometricfunction.html#bse50_6)。模块输入有进一步的要求。

有关何时将**函数**设置为 `sin`、`cos`、`sincos` 或 `cos + jsin`，并将**逼近方法**设置为 “`CORDIC`” 的详细信息，请参阅 [Port_1, Port_1Port_1Port_1](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/trigonometricfunction.html#mw_2a13281f-2c80-469d-bf6b-b9bed27e85f3)。

下表概述了输入无效时发生的情况。

| 模块用法   | 无效输入的影响                                           |
| :--------- | :------------------------------------------------------- |
| 仿真模式   | 出现错误。                                               |
| 生成的代码 | 发生未定义的行为。对于生成的代码，避免依赖未定义的行为。 | -->

<!-- 
### 查找逼近方法

有关何时将**函数**设置为 `sin`、`cos`、`sincos` 或 `cos + jsin`，并将**逼近方法**设置为“`查找`”的详细信息，请参阅 [Port_1, Port_1Port_1Port_1](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/trigonometricfunction.html#mw_2a13281f-2c80-469d-bf6b-b9bed27e85f3)。 -->

## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperation/TrigonometricFunction.mo">TrigonometricFunction.mo</helpButton>。

计算 sin1° 的值，将 Constant 模块的值设为 1，TrigonometricFunction 模块的函数选择 sin。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/TrigonometricFunction/TrigonometricFunction01.png')" style="width: 600px; ">

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/TrigonometricFunction/TrigonometricFunction02.png')" style="width: 600px; ">


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u1 — 输入信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

指定为标量、向量或矩阵的输入。此模块接受以下数据类型的输入信号：

| 函数                                                         | 输入数据类型                                 |
| :----------------------------------------------------------- | :------------------------------------------- |
| `sin` `cos` `sincos` `cos + jsin` `atan2` <!--暂无  `tanh``asinh``acosh``atanh` -->                       | 浮点定点 |
| `tan` `asin` `acos` `atan` `sinh` `cosh` <!--暂无  `tanh``asinh``acosh``atanh` -->| 浮点                                         |

CORDIC 逼近定点类型传播：

| 输入数据类型         | 函数                                   | 输出数据类型                                                 |
| :------------------- | :------------------------------------- | :----------------------------------------------------------- |
| 定点，有符号或无符号 | `sin`、`cos`、`sincos` 和 `cos + jsin` | `fixdt` `(1, WL, WL - 2)` |
| 定点，有符号         | `atan2`                                | `fixdt` `(1, WL, WL – 3)`                                     |
| 定点，无符号         | `atan2`                                | `fixdt` `(1, WL, WL – 2)`                                     |

查找逼近定点类型传播：

| 输入数据类型 | 函数                                          | 输出数据类型             |
| :----------- | :-------------------------------------------- | :----------------------- |
| 定点，有符号 | `sin`、`cos`、`sincos`、<!--`cos + jsin`、`atan2`--> | `fixdt` `(1, WL, FL)`     |
| 定点，无符号 | `sin`、`cos`、`sincos`、<!--`cos + jsin`、`atan2`--> | `fixdt` `(1, WL - 1, FL)` |

#### 依存关系
当您将**函数**设置为 `atan2` 时，模块显示两个输入端口。第一个输入 (**u1**) 是函数参数的 y 轴坐标，即虚部。第二个输入 (**u2**) 是函数参数的 x 轴坐标，即实部。

**数据类型：**  float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | fixed point

</div>
</div>



<!-- 
- 如果您将**逼近方法**设置为“`无`”、“`CORDIC`” 或“`查找`”，则可以使用浮点输入信号。但是，模块输出的数据类型取决于您选择的逼近方法选项。

| 输入数据类型 | 逼近方法   | 输出数据类型                                                 |
| :----------- | :--------- | :----------------------------------------------------------- |
| 浮点         | “`无`”     | 取决于您选择的**输出信号类型**。选项为 `auto`（与输入的数据类型相同）、`real` 或 `complex`。 |
| 浮点         | “`CORDIC`” | 与输入相同。当您使用 CORDIC 逼近方法计算模块输出时，**输出信号类型**不可用。 |
| 浮点         | “`查找`”   | 与输入相同。当您使用 Lookup 逼近方法计算模块输出时，**输出信号类型**不可用。 |

对于 CORDIC 和查找逼近：

- `sin`、`cos`、`sincos`、`cos + jsin` 和 `atan2` 函数的输入必须是实数。
- `sin`、`cos`、`sincos` 和 `atan2` 函数的输出为实数。
- `cos + jsin` 函数的输出为复数。 -->

<!-- #### 限制 -->

<!-- 
- 仅当**逼近方法**设置为 “`CORDIC`” 或“`查找`”时，才可以使用定点输入信号。CORDIC 和查找逼近可用于 `sin`、`cos`、`sincos`、`cos + jsin` 和 `atan2` 函数。

- 除 `atan2` 之外，此模块中的所有函数都支持复数输入信号。

- 当您将**逼近方法**设置为“`查找`”时，数据点的数量受到以下因素的限制：

- `smallEnoughNumDataPoints = 2(inputFractionLen-2)+1`
- `bigEnoughFractionLen = log2(numberOfDataPoints - 1)+2`

其中：

- smallEnoughNumDataPoints 是由指定的输入小数长度 inputFractionLen 表示的最大数据点数。
- bigEnoughFractionLen 是表示指定的数据点数 numberOfDataPoints 所需的最小小数长度。

- 当您将**函数**设置为 `sin`、`cos`、`sincos` 或 `cos + jsin` 并将**逼近方法**设置为 “`CORDIC`” 时，模块具有以下限制：

- 当您使用有符号定点类型时，输入角必须在 [–2π, 2π) 弧度范围内。
- 当您使用无符号定点类型时，输入角必须在 [0, 2π) 弧度范围内。

当您将**函数**设置为 `atan2` 且**逼近方法**设置为 “`CORDIC`” 时，模块具有以下限制：

- 输入的大小必须相同，或者至少一个值必须是标量值。
- 两个输入必须具有相同的数据类型。
- 当您使用有符号定点类型时，字长必须等于或小于 `126`。
- 当您使用无符号定点类型时，字长必须等于或小于 `125`。

- 当您将**函数**设置为 `sin`、`cos`、`sincos` 或 `cos + jsin` 并将**逼近方法**设置为“`查找`”时，模块具有以下限制。

- 当您使用有符号定点类型时，输入角必须在 [-2π,2π] 弧度范围内。
- 当您使用无符号定点类型时，输入角必须在 [0,2π) 弧度范围内。
- 当您将**函数**设置为 `atan2` 且**逼近方法**设置为“`查找`”时，模块具有以下限制：
    - 输入的大小必须相同，或者至少一个值必须是标量值。
    - 两个输入必须具有相同的数据类型。 -->


<div class="details-box">
<details open>
<summary>u2 — atan2 的函数参数的 x 轴坐标，即实部<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

输入 atan2 的函数参数的 x 轴坐标，即实部。当您将**函数**设置为 atan2 时，模块显示两个输入端口。第一个输入 (**u1**) 是函数参数的 y 轴坐标，即虚部。第二个输入 (**u2**) 是函数参数的 x 轴坐标，即实部。

#### 依存关系

要启用此端口，请将**函数**设置为 atan2。

**数据类型：**  float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | fixed point

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y1 — 指定输入信号的三角函数<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

将指定的三角函数应用于一个或多个输入（以 rad 为单位）的结果。每个函数支持：

- 标量运算
- 按元素的向量和矩阵运算

**数据类型：** flaot | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | fixed point

</div>
</div>

<div class="details-box">
<details open>
<summary>sin — 输入信号的正弦<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

输入信号的正弦，以 rad 和 rev 为单位。

#### 依存关系

要启用此端口，请将**函数**设置为 **sincos**。

**数据类型：**  float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | fixed point

</div>
</div>

<!-- 
#### 限制

仅当**逼近方法**设置为 “`CORDIC`” 或“`查找`”时才支持定点输入信号。 -->

<div class="details-box">
<details open>
<summary>cos — 输入信号的余弦<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

输入信号的余弦，以 rad 和 rev 为单位。

#### 依存关系

要启用此端口，请将**函数**设置为 **sincos**。

**数据类型：**  float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | fixed point

</div>
</div>


<!-- #### 限制

仅当**逼近方法**设置为 “`CORDIC`” 或“`查找`”时才支持定点输入信号。 -->



## 参数


### 算法


<div class="details-box">
<details open>
<summary>函数 — 三角函数<div>sin （默认） | cos | tan | asin | acos | atan | atan2 | sinh | cosh | Tanh | asinh | acosh | atanh | sincos | cos + jsin</div></summary>
</details>
<div class="details-content">

指定三角函数。模块图标上的函数名称发生变化以反映您的选择。

</div>
</div>

<!-- 
有关何时将**函数**设置为 `sin`、`cos`、`sincos` 或 `cos + jsin`，并将**逼近方法**设置为 “`CORDIC`” 的详细信息，请参阅 [限制](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/trigonometricfunction.html#mw_8dc8be52-5bca-4e8b-bc47-679e20220fc1)。 -->

<!-- 
#### 编程用法

| **模块参数**：`Operator`                                     |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值：**`'sin' | 'cos' | 'tan' | 'asin' | 'acos' | 'atan' | 'atan2' | 'sinh' | 'cosh' | 'tanh' | 'asinh' | 'acosh' | 'atanh' | 'sincos' | 'cos + jsin'` |
| **默认值：**`'sin'`                                          | -->


<!-- 暂无
### `逼近方法` — CORDIC、查找或无 “`无`” （默认） | “`CORDIC`” | “`查找`”



指定计算输出的逼近方法类型。

| 逼近方法         | 支持的数据类型               | 何时使用此方法               |
| :--------------- | :--------------------------- | :--------------------------- |
| “`无`”（默认值） | 浮点                         | 您想使用默认的泰勒级数算法。 |
| “`CORDIC`”       | 浮点和定点                   | 您需要快速的近似迭代计算。   |
| “`查找`”         | 浮点和定点（双精度和单精度） | 您需要快速的近似查找表实现。 |

有关何时将**函数**设置为 `sin`、`cos`、`sincos` 或 `cos + jsin`，并将**逼近方法**设置为 “`CORDIC`” 的详细信息，请参阅 [限制](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/trigonometricfunction.html#mw_8dc8be52-5bca-4e8b-bc47-679e20220fc1)。

#### 依存关系

- 要启用此参数，请将**函数**设置为 “`sin`”、“`cos`”、“`sincos`”、“`cos + jsin`” 或 `atan2`。
- 要使用定点输入信号，必须将**逼近方法**设置为 “`CORDIC`” 或“`查找`”。
- 要启用**表数据类型**参数，请将此方法设置为“`查找`”。

#### 编程用法

| **模块参数**：`ApproximationMethod`    |
| -------------------------------------- |
| **类型：**字符向量                     |
| **值：**`'None' | 'CORDIC' | 'Lookup'` |
| **默认值：**`'None'`                   | -->



<!-- 
### 内插方法 — 断点值之间插值的方法 “线性点-斜率” （默认） | “均一”



当输入位于两个断点值之间时，模块将根据相邻断点内插输出值。 -->

<!-- 
#### 编程用法

| **模块参数**：`InterpMethod`            |
| --------------------------------------- |
| **类型：**字符向量                      |
| **值：**`'Linear point-slope' | 'Flat'` |
| **默认值：**`'Linear point-slope'`      | -->


<!-- 暂无
### `迭代次数` — CORDIC 算法的迭代次数 `11` （默认） | 正整数，小于或等于定点输入的字长



指定要执行 CORDIC 算法的迭代次数。默认值为 11。

- 当模块输入使用浮点数据类型时，迭代次数可以是正整数。

- 当模块输入是定点数据类型时，迭代次数不能超过字长。

例如，如果模块输入是 `fixdt(1,16,15)`，字长为 16。在这种情况下，迭代次数不能超过 16。

#### 依存关系

要启用此参数，必须按如下所示设置**函数**和**逼近方法**参数：

- 将**函数**设置为 “`sin`”、“`cos`”、“`sincos`”、“`cos + jsin`” 或 `atan2`。
- 将**逼近方法**设置为 “`CORDIC`”。

#### 编程用法

| **模块参数**：`NumberOfIterations`     |
| -------------------------------------- |
| **类型：**字符向量                     |
| **值：**正整数，小于等于定点输入的字长 |
| **默认值：**`'11'`                     | -->


<!-- 暂无
### `角度单位` — 角度单位 “`radian`” （默认） | “`revolution`”



将查找方法的角度单位指定为 “`radian`” 或 “`revolution`”。

#### 依存关系

要启用此参数，请进行如下设置：

- 将**函数**设置为 “`sin`”、“`cos`”、“`sincos`”、“`cos + jsin`” 或 `atan2`。
- 将**逼近方法**设置为“`查找`”。

#### 编程用法

| **模块参数**：`AngleUnit`         |
| --------------------------------- |
| **类型：**字符向量                |
| **值：**`'radian' | 'revolution'` |
| **默认值：**`'radian'`            | -->


<!-- 暂无
### `数据点数` — 查找表的数据点数 `16` （默认） | 标量



将查找表的数据点数指定为标量实数。

#### 依存关系

要启用此参数，请进行如下设置：

- 将**函数**设置为 “`sin`”、“`cos`”、“`sincos`”、“`cos + jsin`” 或 `atan2`。
- 将**逼近方法**设置为“`查找`”。

#### 编程用法

| **模块参数**：`NumberOfDataPoints` |
| ---------------------------------- |
| **类型：**字符向量                 |
| **值：**标量                       |
| **默认值：**`'16'`                 | -->


<!-- 暂无
### `输出信号类型` — 输出信号的复/实性 “`自动`” （默认） | “`实数`” | “`复`”



将 Trigonometric Function 模块输出信号类型指定为 `auto`、`real` 或 `complex`。

| 函数                   | 输入信号类型 | 输出信号类型 |      |      |
| :--------------------- | :----------- | :----------- | ---- | ---- |
| 自动                   | 实数         | 复数         |      |      |
| 任意**函数**参数选择项 | 实数         | 实数         | 实数 | 复数 |
| 复数                   | 复数         | 错误         | 复数 |      |

#### 依存关系

将**逼近方法**设置为 “`CORDIC`” 将禁用此参数。



**注意**

当**函数**为 `atan2` 时，仿真或代码生成不支持复数输入信号。

#### 编程用法

| **模块参数**：`OutputSignalType`      |
| ------------------------------------- |
| **类型：**字符向量                    |
| **值：**`'auto' | 'real' | 'complex'` |
| **默认值：**`'auto'`                  | -->

<!-- 暂无


### `删除防止超范围输入的代码` — 删除防止超范围输入的代码 off （默认） | on



对于 “`acos`” 和 “`asin`”，选中此复选框将不会防范超出范围的输入，从而减少冗余。

- 如果清除此复选框，则会启用防范。在执行任何操作之前，模块会将超出范围的输入饱和处理为 `1` 或 `-1`。生成的代码包含用于检查超出范围输入的代码。
- 如果选中此复选框，则会取消防范。模块将对输入值执行所有运算而不进行任何更改。生成的代码不包含用于检查超出范围输入的代码。

如果输入已在范围内，启用此复选框可以消除冗余。

#### 依存关系

将**函数**设置为 “`acos`” 和 “`asin`” 会启用此参数。

#### 编程用法

| **模块参数**：`RemoveProtectionAgainstOutOfRangeInput` |
| ------------------------------------------------------ |
| **类型：**字符向量                                     |
| **值：**`'off' | 'on'`                                 |
| **默认值：**`'off'`                                    | -->


<!-- 暂无
### `采样时间` — `-1` 以外的采样时间值 `-1` （默认） | 标量 | 向量



将采样时间指定为 `-1` 以外的值。有关详细信息，请参阅[指定采样时间](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/how-to-specify-the-sample-time.html)。

#### 依存关系

此参数不可见，除非将其显式设置为 `-1` 以外的值。要了解详细信息，请参阅[不建议设置采样时间的模块](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/sampletimehiding.html)。

#### 编程用法

| **模块参数：**`SampleTime`     |
| ------------------------------ |
| **类型：**字符串标量或字符向量 |
| **默认值：**`"-1"`             | -->


<!-- 暂无
### 数据类型



### `表数据类型` — 表的数据类型 “`Inherit: Inherit via input`” （默认） | “`double`” | “`single`” | “`fixdt(1,16,0)`” | “`<data type expression>`”



查找表的数据类型，指定为：

- “`Inherit: Inherit via input`”
- “`double`”
- “`single`”
- “`fixdt(1,16,0)`”
- “`<data type expression>`”

有关设置数据类型的详细信息，请参阅[控制信号的数据类型](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/control-signal-data-types.html)。

#### 编程用法

| **模块参数**：`TableDataTypeStr`                             |
| ------------------------------------------------------------ |
| **类型：**字符串标量或字符向量                               |
| **值：** `Inherit: Inherit via input` | `single` | `double` | `fixdt(1,16,0)` \| 数据类型表达式 |
| **默认值：**`Inherit: Inherit via input`                     | -->


<!-- 暂无
### `模式` — 要指定的数据的类别 “`继承`” （默认） | “`内置`” | “`定点`” | “`表达式`”



选择您要如何指定**输出**数据类型的数据类型属性。您可以选择：

- “`继承`” - 用于指定继承数据类型的规则，例如 “`Inherit:Inherit via internal rule`”
- “`内置`” - 用于指定内置数据类型。
- “`定点`” - 用于指定数据类型的定点属性。
- “`表达式`” - 用于指定计算结果为有效数据类型的表达式，例如 `fixdt([],16,0)`



#### 依存关系

要启用此参数，请在**输出数据类型**参数处单击 **>>**。 -->


<!-- 暂无
### `符号性` — 指定有符号或无符号 `Signed` （默认） | `Unsigned`



为**输出**数据类型指定**符号性**。

#### 依存关系

要启用此参数，请将**模式**设置为“`定点`”。



### `定标` — 定标定点数据的方法 “`二进制小数点`” （默认）



为**输出**数据类型指定**定标**。

#### 依存关系

要启用此参数，请将**模式**设置为“`定点`”。 -->


<!-- 暂无
### `数据类型覆盖` — 为此信号指定数据类型覆盖模式 `Inherit` | `Off`



为此信号选择数据类型覆盖模式。

- “`继承`” - 继承为模型指定的数据类型覆盖设置。
- “`关闭`” - 忽略为模型指定的数据类型覆盖设置，并使用您指定的定点数据类型

有关详细信息，请参阅 Simulink® 文档中的[使用数据类型助手指定数据类型](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/specify-data-types-using-data-type-assistant.html)。

#### 提示

由于能够关闭单个数据类型的数据类型覆盖，您可以在应用数据类型覆盖时更好地控制模型中的数据类型。例如，您可以使用此选项确保数据类型满足下游模块的要求，而忽略数据类型覆盖设置。

#### 依存关系

要启用此参数，请单击**显示数据类型助手**按钮，并将**模式**设置为“`内置`”或“`定点`”。 -->


<!-- 暂无
### `字长` — 存储量化整数的字的位大小 `16` （默认） | 从 0 到 32 的整数



指定存储量化整数的字的位大小。有关详细信息，请参阅[指定定点数据类型](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/specify-data-types-using-data-type-assistant.html#bsnnyna-1)。

#### 依存关系

要启用此参数，请将**模式**设置为“`定点`”。 -->


<!-- 暂无
### `小数长度` — 指定定点数据类型的小数长度 `0` （默认） | 标量整数



将定点数据类型的小数长度指定为正整数或负整数。有关详细信息，请参阅[指定定点数据类型](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/specify-data-types-using-data-type-assistant.html#bsnnyna-1)。

#### 依存关系

要启用此参数，请进行如下设置：

- 将**模式**设置为“`定点`”
- 将**定标**设置为“`二进制小数点`” -->


<!-- ## 模块特性 -->
<!-- 暂无
| **数据类型**                                                 | `double` \| `fixed pointa` \| `half` \| `integera` \| `single` |
| ------------------------------------------------------------ | ---------------------------------------------------------- |
| **直接馈通**                                                 | `是`                                                       |
| **多维信号**                                                 | `是`                                                       |
| **可变大小信号**                                             | `是`                                                       |
| **过零检测**                                                 | `否`                                                       |
| [a](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/trigonometricfunction.html?s_tid=doc_ta#d125e209982) 当采用 CORDIC 逼近方法时，此模块支持定点和基整数数据类型。 |                                                            | -->

<!-- ## 详细信息 -->


<!-- 暂无
### CORDIC

## 参考

[1] Volder, Jack E., “The CORDIC Trigonometric Computing Technique.” IRE Transactions on Electronic Computers EC-8 (1959); 330–334.

[2] Andraka, Ray “A Survey of CORDIC Algorithm for FPGA Based Computers.” Proceedings of the 1998 ACM/SIGDA Sixth International Symposium on Field Programmable Gate Arrays. Feb. 22–24 (1998): 191–200.

[3] Walther, J.S., “A Unified Algorithm for Elementary Functions,” Proceedings of the Spring Joint Computer Conference, May 18-20, 1971: 379–386.

[4] Schelin, Charles W., “Calculator Function Approximation,” The American Mathematical Monthly 90, no. 5 (1983): 317–325. -->

<!-- ## 扩展功能 -->

<!-- 

### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。

并非所有编译器都支持 `asinh`、`acosh` 和 `atanh` 函数。如果您使用不支持这些函数的编译器，将会出现警告，且生成的代码无法链接。



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 Verilog 代码和 VHDL 代码。



### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。

当**函数**设置为 “`sin`”、“`cos`”、“`sincos`”、“`cos + jsin`” 或 `atan2` 且**逼近方法**设置为 “`CORDIC`” 时，此模块支持定点和基整数数据类型。 -->

## 版本历史记录

- 在 2024b 之前推出

### 限制信息
不支持部分
1. 描述-CORDIC 逼近方法
2. 描述-查找逼近方法
3. 参数-算法-逼近方法 — CORDIC、查找或无
4. 参数-算法-插值方法 — 断点值之间插值的方法
5. 参数-算法-迭代次数 — CORDIC 算法的迭代次数
6. 参数-算法-输出信号类型 — 输出信号的复/实性
7. 参数-算法-数据点数 — 查找表的数据点数


## 另请参阅
[MathFunction](MathFunction.html) | [Sqrt](Sqrt.html)

