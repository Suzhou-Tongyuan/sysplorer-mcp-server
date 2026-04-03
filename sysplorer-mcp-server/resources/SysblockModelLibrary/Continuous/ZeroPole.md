# ZeroPole
---
&nbsp;

使用零极点增益传递函数进行系统建模。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/ZeroPole/1.png')" style="width: 100px; height: auto; transform: scale(1);">

**库：** Sysblock 模块库 / Continuous

## 描述

Zero-Pole 模块可以通过指定零点、极点和拉普拉斯域传递函数增益定义的系统进行建模。可以使用此模块对单输入单输出（SISO）和单输入多输出（SIMO）系统进行建模。

Zero-Pole 模块有以下要求：

- 传递函数的形式必须为

  <img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/ZeroPole/2.png')" style="width: 500px; height: auto; transform: scale(1);">

  其中 *Z* 表示零点，*P* 表示极点，*K* 表示传递函数的增益。

- 极点数必须大于或等于零点数；

- 复极点和复零点必须为复共轭对组；

- 对于多输出系统，所有传递函数必须具有相同的极点。零点的值可以不同，但每个传递函数的零点数必须相同

### 对单输出系统建模

一个单输出系统具有标量时域输入和输出信号。要对这种类型的系统建模，请执行以下操作：

1. 在**零点**字段中输入传递函数的零点向量。
2. 在**极点**字段中输入传递函数的极点向量。
3. 在**增益**字段中输入传递函数的增益标量。

### 对多输出系统建模

一个多输出系统具有一个标量时域输入信号和一个向量时域输出信号。向量输出中的每个元素均为该系统的一个输出。要对这种类型的系统建模，请执行以下操作：

1. 在**零点**字段中输入全零矩阵。

   矩阵的每一列包含一个传递函数（将系统输入信号与输出信号中的一个元素相关联）的零点。

2. 在**极点**字段中输入对系统的所有传递函数都通用的极点向量。

3. 在**增益**字段中输入增益向量。

   每个元素代表对应的传递函数在零点矩阵中的增益。

## 示例

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continuous/ZeroPole.mo">ZeroPole.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/ZeroPole/3.png')" style="width: 500px; height: auto; transform: scale(1);">

### 参考结果

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/ZeroPole/4.png')" style="width: 800px; height: auto; transform: scale(1);border-top: 1px solid black;">

## 端口

### 输入

<div class="details-box">
<details open>
<summary>Port_1 — 输入信号<div>标量</div></summary>
</details>
<div class="details-content">

系统的标量时域输入信号。  
**数据类型:** double

</div>
</div>



### 输出

<div class="details-box">
<details open>
<summary>Port_1 — 输出信号<div>标量 | 向量</div></summary>
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
<summary>零点 — 零点矩阵<div>1 (默认) | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

定义零点矩阵。  

- 对于单输出系统，输入传递函数的零点向量；
- 对于多输出系统，输入矩阵。此矩阵的每列包含一个传递函数的零点，该传递函数将系统输入与输出向量的一个元素相关联；
- 要对不带零点的系统建模，请输入 []。

</div>
</div>


<div class="details-box">
<details open>
<summary>极点 — 极点向量 <div>[0,1] (默认) | 向量</div></summary>
</details>
<div class="details-content">

定义极点向量。


- 对于单输出系统，输入传递函数的极点向量；
- 对于多输出系统，输入对系统的所有传递函数通用的极点向量。

</div>
</div>


<div class="details-box">
<details open>
<summary>增益 — 增益向量<div>1 (默认) | 向量</div></summary>
</details>
<div class="details-content">

定义增益向量。


- 对于单输出系统，输入传递函数的 1×1 增益向量；
- 对于多输出系统，输入增益向量。每个元素代表对应的传递函数在零点矩阵中的增益。

</div>
</div>
 



## 版本历史记录

- 在 2025a 推出

### 限制信息

- 暂不支持嵌入式代码生成；
- 不支持总线、枚举值类型。