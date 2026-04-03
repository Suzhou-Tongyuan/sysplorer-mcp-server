# Counter
---
&nbsp;
在指定的数据范围内进行计数

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/Counter/Counter.png')" style="width:150px;border:black 1px solid;"> 

- **库：** Sysblock模块库 / Utilities

## 描述

Counter 模块可以在指定的数据范围内进行计数。

计数可以设置为**向上递增计数(Inc)**或**向下递减计数(Dec)**，当“**计数事件**”参数设置为“自由运行”，该模块会禁用“**Inc**”或“**Dec**”端口，并以固定时间间隔计数。

对于“**计数事件**”参数设置为其他选项设置，每当“**Inc**”或“**Dec**”输入端口出现触发事件时，该模块就会对计数器进行递增或递减操作。

同时模块具有一个可选的“**Rst**”端口，当“**Rst**”端口出现触发事件时，计数器会被重置为初始状态，当“**Rst**”端口和“**Inc/Dec**”端口同时接收到触发事件，计数器会先复位，然后再进行递增递减操作。

## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/Counter.mo">Counter.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/Counter/counter_example.png')" style="width:500px;border:black 1px solid;"> 

## 端口

### 输入

<div class="details-box">
<details open>
<summary>Inc/Dec—触发计数事件的输入信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

接收触发计数事件的输入信号，输入为标量时，每当“Inc”或“Dec”输入端口出现触发事件时，该模块就会对计数器进行递增或递减操作。

**依赖条件：**

1. 面板参数“计数方向”设置为“递增”时，启用“Inc”端口，设置为“递减”时，启用“Dec”端口；

2. 面板参数“计数事件”设置为“自由运行”，则“**Inc/Dec**”端口会被禁用，并以恒定的时间间隔进行计数。

**数据类型：** double | float | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean

</div>
</div>

​	



<div class="details-box">
<details open>
<summary>Rst—重置信号<div>标量</div></summary>
</details>
<div class="details-content">

​接收触发重置事件的输入信号，当“Rst”端口和“Inc/Dec”端口同时接收到触发事件，计数器会先复位，然后再进行递增递减操作。

**依赖条件：** 需勾选面板参数“重置输入”才会显示生效

**数据类型：** double | float | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean

</div>
</div>




<div class="details-box">
<details open>
<summary>Max—最大计数值<div>非负整数标量</div></summary>
</details>
<div class="details-content">

​输入计数器最大计数值

**依赖条件：** 面板参数“计数器大小”设置为“通过输入端口指定”才能显示生效

**数据类型：** uint8 | uint16 | uint32

</div>
</div>






### 输出

<div class="details-box">
<details open>
<summary>Cnt—当前计数器的值<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

输出计数器当前值，面板参数“计数事件”设置为“自由运行”时，根据面板参数“每个输出帧的样本数”的值 M，输出`Mx1`向量，端口采样时间和“Inc/Dec”输入端口采样时间相同。

**依赖条件：** 面板参数“输出”需设置为“计数”或“计数和命中端口”才能显示生效

**数据类型：** double | float | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean

</div>
</div>







<div class="details-box">
<details open>
<summary>Hit—命中状态值<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

​输出计数器是否达到了预先设定的命中值，例如计数器当前值为 5 和面板参数“命中值” 5 相等，输出 1,其余输出 0，类型为 boolean 类型（true 表示命中，false 表示未命中）。端口采样时间和“Inc/Dec”输入端口采样时间相同。

**依赖条件：** 面板参数“输出”需设置为“计数”或“计数和命中端口”才能显示生效

**数据类型：** boolean

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>计数方向<div>递增 | 递减</div></summary>
</details>
<div class="details-content">

指定进行递增计数还是递减计数

</div>
</div>


<div class="details-box">
<details open>
<summary>计数事件<div>上升沿 | 下降沿 | 任意沿 | 非零采样值 | 自由运行</div></summary>
</details>
<div class="details-content">

指定在“递增/递减”和“重置”端口接受的触发事件类型

</div>
</div>



<div class="details-box">
<details open>
<summary>计数器大小<div>8bits（默认）| 16bits | 32bits | 用户自定义 | 输入端口指定</div></summary>
</details>
<div class="details-content">

指定数据块计数的整数值的范围

</div>
</div>


<div class="details-box">
<details open>
<summary>最大计数值<div>255（默认值）| 正整数</div></summary>
</details>
<div class="details-content">

将计数器大小最大值设置为“计数数据类型”参数所能表示的任意无符号整数

</div>
</div>



<div class="details-box">
<details open>
<summary>初始计数值<div>0（默认值）| 正整数</div></summary>
</details>
<div class="details-content">

将计数器的初始值指定为参数“计数器大小”所定义范围内的任意无符号整数

</div>
</div>



<div class="details-box">
<details open>
<summary>输出<div>计数端口（默认）| 命中端口 | 计数和命中端口</div></summary>
</details>
<div class="details-content">

选择要启用的输出端口类型

</div>
</div>



<div class="details-box">
<details open>
<summary>命中值<div>32（默认值）| 标量 | 向量</div></summary>
</details>
<div class="details-content">

当计数器出现“命中值”设定的值

</div>
</div>


<div class="details-box">
<details open>
<summary>重置输入<div>开启 | 关闭</div></summary>
</details>
<div class="details-content">

启用重置输入

</div>
</div>



<div class="details-box">
<details open>
<summary>每个输出帧的样本数<div>1（默认值）| 正整数</div></summary>
</details>
<div class="details-content">

将每个输出向量中的样本数量 M 指定为一个正整数标量

</div>
</div>


<div class="details-box">
<details open>
<summary>采样时间<div>1（默认值）| -1 （继承）| 大于 0 的实数标量</div></summary>
</details>
<div class="details-content">

在自由运行模式下对计数器进行递增或递减操作的固定时间间隔

</div>
</div>


<div class="details-box">
<details open>
<summary>计数数据类型<div>double（默认值） | float | int8 | uint8 | int16 | uint16 | int32 | uint32</div></summary>
</details>
<div class="details-content">

指定“计数”端口输出的数据类型

</div>
</div>



<div class="details-box">
<details open>
<summary>命中数据类型<div>boolean</div></summary>
</details>
<div class="details-content">

指定“命中”端口输出的数据类型

</div>
</div>


## 版本历史记录

- 在 2025a 推出

### 限制信息

- 不支持总线、枚举值类型

