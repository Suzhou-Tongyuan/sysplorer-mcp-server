# PolynomialEvaluation
---
多项式计算。

**库：** TYDSPSystem / StatisticsAndLinearAlgebra / ArrayAndMatrixMathematics 

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYDSPSystem/StatisticsAndLinearAlgebra/ArrayAndMatrixMathematics/PolynomialEvaluation/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

PolynomialEvaluation 模块将多项式函数应用于 u 端口的输入。


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div> 实数向量</div></summary>
</details>
<div class="details-content">

将多项式函数应用于输入信号，指定为实数向量。

**数据类型：** double 

</div>
</div>

<div class="details-box">
<details open>
<summary>coeffs — 输入多项式系数<div> 实数向量 </div></summary>
</details>
<div class="details-content">

按指数降序指定系数向量。

**依赖条件：**

要使用此端口请勾选**使用常量参数**参数。

**数据类型：** double 

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>y — 输出多项式计算结果<div>实数向量</div></summary>
</details>
<div class="details-content">
 
模块对输入数据应用多项式函数，输出与输入数据大小的实数向量。

**数据类型：** double 

</div>
</div>

## 参数

</div>
</div>

<div class="details-box">
<details open>
<summary>使用常量系数  — 使用常量系数<div>off（默认）| on</div></summary>
</details>
<div class="details-content">

选择**使用常量系数**参数时，可以在**常量参数**参数中指定多项式表达式。如果不选择**使用常量系数**参数，则可以通过 coeffs 端口指定变量多项式表达式。在这两种情况下，多项式被指定为实数向量，按指数降序排列。

</div>
</div>

<div class="details-box">
<details open>
<summary>常量系数  — 常量系数<div>[5,4,3,2,1]（默认）| 实数向量</div></summary>
</details>
<div class="details-content">

指定要按指数降序应用于输入的多项式系数向量。

例如：在默认条件下，多项式函数表示为：

y = 5 $x^{4}$ + 4 $x^{3}$ + 3 $x^{2}$ + 2 x + 1

**依赖条件：** 要使用此参数，请勾选**使用常量系数**端口。

**数据类型：** double 

</div>
</div>

<div class="details-box">
<details open>
<summary>输入系数维度 — 指定输入系数维度<div>{1}（默认）| 长度为 1 的整型向量</div></summary>
</details>
<div class="details-content">

指定输入系数维度的维度。指定为长度为 1 的整型向量。当**系数源**设置为 Input port 时需配置。

</div>
</div>

<div class="details-box">
<details open>
<summary>输入信号维度 — 指定输入信号维度<div>{1}（默认）| 长度为 1 的整型向量</div></summary>
</details>
<div class="details-content">

指定输入信号的维度。指定为长度为 1 的整型向量。

</div>
</div>


## 版本历史记录

- 在 2025b 推出

## 限制信息

- 该模块暂不支持自动识别输入系数以及输入信号维度，需通过**输入系数维度**和**输入信号维度**参数手动设定。
