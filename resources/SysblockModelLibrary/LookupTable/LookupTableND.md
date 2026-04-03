# LookupTableND

---

逼近 N 维函数。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LookupTable/LookupTableND/1.png')" style="width: 150px; height: auto; transform: scale(1);">

**库：** Sysblock 模块库 / LookupTable

## 描述

### 支持的模块运算

1-D、2-D 和 n-D LookupTable 模块计算一个函数的 N 变量采样表示：

$
*y*=*F*(*x*1,*x*2,*x*3,...,*x**N*)
$

其中函数 *F* 可以是经验函数。此模块通过查找或插入您使用模块参数定义的值表，将输入映射到输出值。该模块支持均一（常量）、线性（线性点-斜率）、拉格朗日（线性拉格朗日）、最近、三次样条和 Akima 样条插值方法。您可以将这些方法应用于从 1 维到 30 维的表。

在下面的模块中，第一个输入标识第一个维度（行）断点，第二个输入标识第二个维度（列）断点，依此类推。

### 点和表数据

以下模块参数定义断点和表数据。

| 模块参数   | 用途                                   |
| :--------- | :------------------------------------- |
| **表维数** | 指定查找表的维数。                     |
| **断点**   | 指定与查找表的每个维度对应的断点向量。 |
| **表数据** | 定义关联的一组输出值。                 |

n-D、1-D 和 2-D Lookup Table 模块通过基于输入值查找或估计表值来生成输出。

| 模块输入                                 | n-D Lookup Table 模块行为                  |
| :--------------------------------------- | :----------------------------------------- |
| 与断点向量中的索引值匹配                 | 输出位于行、列和更高维度断点的交点处的表值 |
| 与断点向量中的索引值不匹配，但在范围内   | 使用您选择的**内插方法**内插适当的表值     |
| 与断点向量中的索引值不匹配，且不在范围内 | 使用您选择的**外插方法**外插输出值         |

## 示例

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LookupTable/LookupTableND.mo">LookupTableND.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LookupTable/LookupTableND/2.png')" style="width: 500px; height: auto; transform: scale(1);">

### 参考结果

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LookupTable/LookupTableND/3.jpg')" style="width: 800px; height: auto; transform: scale(1);border-top: 1px solid black;">


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u1 — 第一个维度（行）输入<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">



</div>
</div>

<div class="details-box">
<details open>
<summary>uN — 第 n 维输入值<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">



</div>
</div>

### 输出


<div class="details-box">
<details open>
<summary>Port_1 — 通过查找或估算表值计算的输出<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">



</div>
</div>

## 参数

### 表和断点

<div class="details-box">
<details open>
<summary>表维数 — 查找表维度的数量 <div>3 (默认) | 1 | 2 | 4 | ...| 30</div></summary>
</details>
<div class="details-content">



</div>
</div>




<div class="details-box">
<details open>
<summary>数据设定 — 表和断点的设定方法<div>表和断点 (默认) | 查找表对象</div></summary>
</details>
<div class="details-content">



</div>
</div>
 

<div class="details-box">
<details open>
<summary>表数据 — 定义输出值的表<div>reshape(repmat([4 5 6;16 19 20;10 18 23],1,2),[3,3,2]) (默认) | 值组成的矩阵，其维度与“表维数”匹配</div></summary>
</details>
<div class="details-content">



</div>
</div>


<div class="details-box">
<details open>
<summary>断点 — 显式断点值，或断点的第一个点和间距<div>[10,22,31] (默认) | 单调递增值的 1×n 或 n×1 向量</div></summary>
</details>
<div class="details-content">



</div>
</div>

### 算法

**查找方法**

<div class="details-box">
<details open>
<summary>内插方法 — 断点值之间插值的方法<div>线性点-斜率 (默认) | 均一 | 最邻近值</div></summary>
</details>
<div class="details-content">



</div>
</div>
 
 
<div class="details-box">
<details open>
<summary>外插方法 — 处理超出断点向量范围的输入值的方法<div>裁剪 (默认)</div></summary>
</details>
<div class="details-content">



</div>
</div>


<div class="details-box">
<details open>
<summary>索引搜索方法 — 计算表索引的方法<div>线性搜索 (默认) | 二分搜索</div></summary>
</details>
<div class="details-content">



</div>
</div>

### 数据类型


<div class="details-box">
<details open>
<summary>表数据 — 表数据的数据类型<div>Inherit：sameAsinput (默认) | Inherit：backPropagattion | float | double</div></summary>
</details>
<div class="details-content">



</div>
</div>


<div class="details-box">
<details open>
<summary>表数据最小值 — 表数据的最小值<div>空 (默认) | 标量</div></summary>
</details>
<div class="details-content">



</div>
</div>


<div class="details-box">
<details open>
<summary>表数据最大值 — 表数据的最大值<div>空 (默认) | 标量</div></summary>
</details>
<div class="details-content">



</div>
</div>
 

<div class="details-box">
<details open>
<summary>断点 — 断点数据类型<div>Inherit：backPropagattion (默认) | float | double</div></summary>
</details>
<div class="details-content">



</div>
</div>



<div class="details-box">
<details open>
<summary>断点最小值 — 最小值断点数据<div>空 (默认) | 标量</div></summary>
</details>
<div class="details-content">



</div>
</div>


<div class="details-box">
<details open>
<summary>断点最大值 — 最大值断点数据可以有<div>空 (默认) | 标量</div></summary>
</details>
<div class="details-content">



</div>
</div>


<div class="details-box">
<details open>
<summary>区间比 — 区间比数据类型<div>Inherit：sameAsinput (默认) | Inherit：backPropagattion | float | double | int8| uint8 | int16 | uint16 | int32 | uint32| int64 | fixdt(1,16,0) | fixdt(1,16,2^0,0)| | fixdt(1,16,10,0,0.0)</div></summary>
</details>
<div class="details-content">



</div>
</div>


<div class="details-box">
<details open>
<summary>中间值 — 中间值数据类型<div>Inherit：sameAsinput (默认) | Inherit：backPropagattion | float | double | int8| uint8 | int16 | uint16 | int32 | uint32| int64 | fixdt(1,16,0) | fixdt(1,16,2^0,0)| | fixdt(1,16,10,0，0.0)</div></summary>
</details>
<div class="details-content">



</div>
</div>


<div class="details-box">
<details open>
<summary>输出 — 输出数据类型<div>Inherit：sameAsinput (默认) | Inherit：backPropagattion | float | double</div></summary>
</details>
<div class="details-content">



</div>
</div>


<div class="details-box">
<details open>
<summary>输出最小值 — 模块可以输出的最小值<div>空 (默认) | 标量</div></summary>
</details>
<div class="details-content">



</div>
</div>


<div class="details-box">
<details open>
<summary>输出最大值 — 模块可以输出的最大值<div>空 (默认) | 标量</div></summary>
</details>
<div class="details-content">



</div>
</div>


<div class="details-box">
<details open>
<summary>内部规则优先级 — 进行中间计算的内部规则<div>速度 (默认) | 精度</div></summary>
</details>
<div class="details-content">



</div>
</div>


<div class="details-box">
<details open>
<summary>要求所有输入具有相同的数据类型 — 要求所有输入具有相同的数据类型<div>on (默认) | off</div></summary>
</details>
<div class="details-content">



</div>
</div>


## 版本历史记录

- 在 2025a 推出

### 限制信息

- 暂不支持嵌入式代码生成；
- 不支持布尔、总线、枚举类型输入/输出。