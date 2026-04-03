# DiscreteStateSpace

实现离散状态空间系统

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/DiscreteStateSpace/DiscreteStateSpace.png')" style="width: 100px; height: auto;border:solid 1px black;">

**库：** Sysblock / Discrete

## 描述

Discrete StateSpace 模块实现由以下方程所描述的系统：
$$
x(n+1)=Ax(n)+Bu(n)
$$
$$
y(n)=Cx(n)+Du(n)
$$

其中 $u$ 表示输入，$x$ 表示状态，$y$ 表示输出。矩阵系数必须具有这些特征，如下所示：

- $A$ 必须是 $n×n$ 矩阵，其中 $n$ 是状态的数量。

- $B$必须是$n×m$矩阵，其中 $m$ 是输入的数量。

- $C$ 必须是 $r×n$ 矩阵，其中 $r$ 是输出的数量。

- $D$ 必须是 $r×m$ 矩阵。

  <img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/DiscreteStateSpace/DiscreteStateSpaceDimension.png')" style="width: 200px; height: auto;border:solid 1px black;">

此模块接受一个输入并生成一个输出。输入向量的宽度是 $B$ 和 $D$ 矩阵中的列数。输出向量的宽度是 $C$ 和 $D$ 矩阵中的行数。要定义初始状态向量，请使用初始条件参数。

## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/DiscreteStateSpace.mo">DiscreteStateSpace.mo</helpButton>。

**示例**

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/DiscreteStateSpace/DiscreteStateSpace_example.png')" style="width: 600px; height: auto;border:solid 1px black;">

**参考结果**

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/DiscreteStateSpace/DiscreteStateSpace_output.png')" style="width: 800px; height: auto;border:solid 1px black;">

## 端口

### 输入

<div class="details-box">
  <details open>
  <summary>u — 输入信号<div>标量 | 向量 </div></summary>
  </details>
  <div class="details-content">

  ​	输入向量，其宽度等于$B$和$D$的矩阵中的列数。


  **数据类型：** double | float

</div>
</div>

### 输出

<div class="details-box">
  <details open>
  <summary>y — 输出信号<div>标量 | 向量 </div></summary>
  </details>
  <div class="details-content">


  ​	输出向量，其宽度等于 $C$ 和 $D$ 矩阵中的行数。

  **数据类型：** double | float

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>A — 矩阵系数，A <div>1 (默认) | 标量 | 矩阵</div></summary>
</details>
<div class="details-content">


将矩阵系数 A 指定为实数值 n_×_n 矩阵，其中 n 是状态的数量。

</div>
</div>

<div class="details-box">
<details open>
<summary>B — 矩阵系数，B <div>1 (默认) | 标量 | 矩阵</div></summary>
</details>
<div class="details-content">


将矩阵系数 B 指定为实数值 n_×_m 矩阵，其中 n 是状态的数量，m 是输入的数量。

</div>
</div>

<div class="details-box">
<details open>
<summary>C — 矩阵系数 C <div>1(默认) | 标量 | 矩阵</div></summary>
</details>
<div class="details-content">


将矩阵系数 C 指定为实数值 r_×_n 矩阵，其中 r 是输出的数量，n 是状态的数量。

</div>
</div>

<div class="details-box">
<details open>
<summary>D — 矩阵系数 D<div>1 (默认) | 标量 | 矩阵</div></summary>
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

<div class="details-box">
<details open>
<summary>采样时间 — 指定采样时间间隔<div>-1 (默认) | 标量</div></summary>
</details>
<div class="details-content">
 
 指定采样时间间隔。

</div>
</div>



## 版本历史记录

- 在 2025b 推出

### 限制信息

- 暂不支持模块的 A，B，C，D 与初始条件参数为空矩阵。

