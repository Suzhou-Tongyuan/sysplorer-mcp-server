# TransferFcn
---
&nbsp;

将线性系统建模为传递函数。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/TransferFcn/1.png')" style="width: 100px; height: auto; transform: scale(1);">

**库：** Sysblock 模块库 / Continuous

## 描述

Transfer Fcn 模块通过拉普拉斯域变量*`s`*的传递函数为线性系统建模。此模块可为单输入单输出 (SISO) 和单输入多输出 (SIMO) 系统建模。

### 使用此模块的条件

Transfer Fcn 模块假定满足以下条件：

- 传递函数的格式为

  <img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/TransferFcn/2.png')" style="width: 600px; height: auto; transform: scale(1);">

  其中 *u* 和 *y* 分别代表系统输入和输出，*nn* 和 *nd* 分别是分子和分母系数。*num(s)* 和 *den(s)* 包含分子和分母的 *s* 降幂系数；

- 分母的阶必须大于或等于分子的阶；

- 对于多输出系统，所有传递函数具有相同的分母，而所有分子具有相同的阶次。

### 为单输出系统建模

对于单输出系统，模块的输入和输出是标量时域信号。要为此系统建模，请执行以下操作：

1. 在**分子系数**字段中输入传递函数的分子系数向量。
2. 在**分母系数**字段中输入传递函数的分母系数向量。

### 为多输出系统建模

对于多输出系统，模块输入为标量，输出为向量，其中每个元素都是系统的一个输出。要为此系统建模，请执行以下操作：

1. 在**分子系数**字段中输入矩阵。

   此矩阵的每一行包含确定一个模块输出的传递函数的分子系数。

2. 在**分母系数**字段中输入系统所有传递函数的公分母系数向量。

### 指定初始条件

传递函数描述了输入和输出在拉普拉斯（频率）域中的关系。具体而言，它被定义为零初始条件的系统对冲激输入的响应（输出）的拉普拉斯变换。

传递函数的乘法和除法等运算依赖于零初始状态。例如，您可以将一个复杂的传递函数分解为一系列简单的传递函数。按顺序应用它们可获得与原始传递函数相同的响应。如果其中一个传递函数采用非零初始状态，结果将不正确。而且，一个传递函数有无限多个时域实现，大多数状态并没有任何物理意义。

## 示例

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continuous/TransferFcn.mo">TransferFcn.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/TransferFcn/3.png')" style="width: 500px; height: auto; transform: scale(1);">

### 参考结果

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/TransferFcn/4.jpg')" style="width: 800px; height: auto; transform: scale(1);border-top: 1px solid black;">

## 端口

### 输入

<div class="details-box">
<details open>
<summary>Port_1 — 输入信号<div>标量</div></summary>
</details>
<div class="details-content">

输入信号，指定为数据类型为 double 的标量。
仅当传递函数的分子为 0 时，此端口才有直接馈通。

**数据类型：** double

</div>
</div>


### 输出


<div class="details-box">
<details open>
<summary>Port_1 — 输出信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

输出信号，是数据类型为 double 的标量或向量。

对于单输出系统，模块的输入和输出是标量时域信号。

对于多输出系统，输入为标量，输出为向量，其中每个元素都是系统的一个输出。  

**数据类型：** double

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>分子系数 — 分子系数的向量或矩阵<div>[1] (默认) | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

定义传递函数的分子系数。  
- 对于单输出系统，输入传递函数的分子系数向量。
- 对于多输出系统，输入矩阵。此矩阵的每一行包含确定一个模块输出的传递函数的分子系数。

</div>
</div>
 
<div class="details-box">
<details open>
<summary>分母系数 — 分母系数的行向量<div>[1,1] (默认) | 向量</div></summary>
</details>
<div class="details-content">

定义分母系数的行向量。  
- 对于单输出系统，输入传递函数的分母系数向量。
- 对于多输出系统，输入包含对系统所有传递函数公分母系数的向量。

</div>
</div>



## 版本历史记录

- 在 2025a 推出

### 限制信息

- 暂不支持嵌入式代码生成；
- 不支持总线、枚举值类型。