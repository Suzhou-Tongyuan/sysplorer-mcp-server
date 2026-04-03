# StateSpace
---
&nbsp;

状态空间表示的状态矩阵、输入矩阵和输出矩阵。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/StateSpace/1.png')" style="width: 100px; height: auto; transform: scale(1);">

**库：** Sysblock 模块库 / Continuous

## 描述

StateSpace 模块可实现具有您定义的如下行为的系统：

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/StateSpace/2.png')" style="width: 150px; height: auto; transform: scale(1);">

其中 *x* 是状态向量，*u* 是输入向量，*y* 是输出向量，*x0* 是状态向量的初始条件。A、B、C、D 矩阵可以指定为稀疏矩阵或稠密矩阵。矩阵系数必须具有以下特征：

- *A* 必须是 *n*×*n* 矩阵，其中 *n* 是状态的数量；

- *B* 必须是 *n*×*m* 矩阵，其中 *m* 是输入的数量；

- *C* 必须是 *r*×*n* 矩阵，其中 *r* 是输出的数量；

- *D* 必须是 *r*×*m* 矩阵。

  <img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/StateSpace/3.png')" style="width: 200px; height: auto; transform: scale(1);">

一般情况下，模块有一个输入端口和一个输出端口。C 或 D 矩阵中的行数与输出端口的宽度相同。B 或 D 矩阵中的列数与输入端口的宽度相同。如果您要建立不带任何输入端口的自治线性系统模型，请将 B 和 D 设置为空矩阵。在这种情况下，模块相当于没有输入端口但有一个输出端口的源模块，并实现以下系统：

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/StateSpace/6.png')" style="width: 150px; height: auto; transform: scale(1);">

## 示例

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continuous/StateSpace.mo">StateSpace.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/StateSpace/4.png')" style="width: 500px; height: auto; transform: scale(1);">

### 参考结果

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/StateSpace/5.png')" style="width: 800px; height: auto; transform: scale(1);border-top: 1px solid black;">

## 端口

### 输入

<div class="details-box">
<details open>
<summary>Port_1 — 输入信号<div>标量</div></summary>
</details>
<div class="details-content">

系统的标量时域输入信号。  

**数据类型：** double

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>Port_1 — 输出向量<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

系统的输出建模为一个零极点增益传递函数，以标量或向量信号形式提供。  
对单输出系统建模时，模块生成标量时域信号。  
当对多输出系统建模时，模块生成向量，其中向量的每个元素均为系统的输出。   

**数据类型：** double

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>A — 矩阵系数，A <div>1 (默认) | 标量 | 向量 | 矩阵 | 稀疏矩阵</div></summary>
</details>
<div class="details-content">

将矩阵系数 A 指定为实数值 n_×_n 矩阵，其中 n 是状态的数量。

</div>
</div>


<div class="details-box">
<details open>
<summary>B — 矩阵系数，B <div>1 (默认) | 标量 | 向量 | 矩阵 | 稀疏矩阵</div></summary>
</details>
<div class="details-content">

将矩阵系数 B 指定为实数值 n_×_m 矩阵，其中 n 是状态的数量，m 是输入的数量。

</div>
</div>


<div class="details-box">
<details open>
<summary>C — 矩阵系数 C <div>1(默认) | 标量 | 向量 | 矩阵 | 稀疏矩阵</div></summary>
</details>
<div class="details-content">

将矩阵系数 C 指定为实数值 r_×_n 矩阵，其中 r 是输出的数量，n 是状态的数量。

</div>
</div>

<div class="details-box">
<details open>
<summary>D — 矩阵系数 D<div>1 (默认) | 标量 | 向量 | 矩阵 | 稀疏矩阵</div></summary>
</details>
<div class="details-content">

将矩阵系数 D 指定为实数值 r_×_m 矩阵，其中 r 是输出的数量，m 是输入的数量。

</div>
</div>


<div class="details-box">
<details open>
<summary>初始条件 — 初始状态向量<div>0 (默认) | 标量 | 向量</div></summary>
</details>
<div class="details-content">

指定初始状态向量。  
限制：此模块的初始条件不能为 inf 或 NaN。

</div>
</div>




## 版本历史记录

- 在 2025a 推出

### 限制信息

- 暂不支持嵌入式代码生成；
- 不支持总线、枚举值类型。