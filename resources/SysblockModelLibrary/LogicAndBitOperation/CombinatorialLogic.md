# CombinatorialLogic
---
&nbsp;

真值表

<img :src="$withBase('/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/CombinatorialLogic/CombinatorialLogic.png')" style="width:120px; border: 1px solid black;">

**库：** Sysblock 模块库/ LogicAndBitOperation

## 描述

Combinatorial Logic 模块实现一个标准真值表，用于建模可编程逻辑数组（PLA）、逻辑电路、决策表和其他布尔表达式。

## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/CombinatorialLogic.mo">CombinatorialLogic.mo</helpButton>。

<img :src="$withBase('/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/CombinatorialLogic/CombinatorialLogic_example.png')" style="width:600px; border: 1px solid black;">

### 示例说明

使用默认的真值表参数时，对应三个输入与两个输出，下表显示每种输入值组合的对应输出。

| input1 | input2 | input3 | output1 | output2 |
| :----: | :----: | :----: | :-----: | :-----: |
|   0    |   0    |   0    |    0    |    0    |
|   0    |   0    |   1    |    0    |    1    |
|   0    |   1    |   0    |    0    |    1    |
|   0    |   1    |   1    |    1    |    0    |
|   1    |   0    |   0    |    0    |    1    |
|   1    |   0    |   1    |    1    |    0    |
|   1    |   1    |   0    |    1    |    0    |
|   1    |   1    |   1    |    1    |    1    |

### 参考结果

<img :src="$withBase('/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/CombinatorialLogic/Example_output.png')" style="width:600px; border: 1px solid black;">

## 端口

### 输入

<div class="details-box">
<details open>
<summary>Port_1 — 输入信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

输入信号，输入个数与真值表参数的行数之间的关系为：$行数 = 2^{输入个数}$。

**数据类型：** double | boolean

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>Port_1 — 输出信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

输出信号，如果真值表中包含非布尔值，则输出类型为 double；否则输出类型为 boolean。输出个数等于真值表参数的列数。

**数据类型：** double | boolean

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>真值表 — 将所有可能的模块输出定义为真值表参数<div>[0 0;0 1;0 1;1 0;0 1;1 0;1 0;1 1]（默认值）| 矩阵 </div></summary>
</details>
<div class="details-content">

将所有可能的模块输出定义为真值表参数

</div>
</div>


## 版本历史记录

- 在 2025a 推出

### 限制信息

- 仅支持 double、boolean 类型

