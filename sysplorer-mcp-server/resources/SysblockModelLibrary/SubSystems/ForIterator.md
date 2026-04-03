# ForIterator

For Iterator 子系统的控制模块

**库**：Sysblock 模块库 / SubSystems

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SubSystems/ForIterator/1.png')" style="width: 100px; height: auto; transform: scale(1);border:solid 1px black;">

## 描述

ForIterator 模块属于 For 子系统的控制模块。它的作用是在当前时间步中重复执行子系统内的模块，直到迭代变量超过指定的迭代限制。该模块的功能，可以等价为程序中的 for 循环。

## 示例

**示例模型**

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SubSystems/ForIterator.mo">ForIterator.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SubSystems/ForIterator/2.png')" style="width: 600px; height: auto; transform: scale(1);border:solid 1px black;">

**参考结果**

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SubSystems/ForIterator/3.png')" style="width: 600px; height: auto; transform: scale(1);border:solid 1px black;">

## 端口

### 输入

<div class="details-box">
<details open>
<summary>N — 迭代次数输入端口<div>标量</div></summary>
</details>
<div class="details-content">


​	输入信号，指定为标量。您可以通过此端口来控制 For 子系统的迭代次数。当此输入端口的值为负数或 0 时，For 子系统相当于不执行。

**数据类型：double | float | int8 | int16 | int32 | uint8 | uint16 | uint32**

</div>
</div>

<div class="details-box">
<details open>
<summary>Next_i — 迭代变量更新端口<div>标量</div></summary>
</details>
<div class="details-content">


​	输入信号，指定为标量。当**在外部设置下一个 i （迭代变量）**勾选时，该端口启用。您可以通过该端口对迭代变量的值进行更新。需要注意，Next_i 端口的类型需要与迭代变量的输出数据类型保持一致。

**数据类型：double | int8 | int16 | int32 | uint8 | uint16 | uint32**

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>y — 迭代变量输出端口<div>标量</div></summary>
</details>
<div class="details-content">


​	输出信号，指定为标量。当**显示迭代变量**的选项勾选时，该输出端口启用。for 子系统的迭代变量将通过该端口进行输出。

**数据类型：double | int8 | int16 | int32 | uint8 | uint16 | uint32**

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>开始时的状态<div>保持</div></summary>
</details>
<div class="details-content">

选择时间步之间的模块状态。

在时间步之间，for 子系统中的模块的状态值保持不变。

</div>
</div>

<div class="details-box">
<details open>
<summary>迭代限制来源<div>内部（默认）| 外部</div></summary>
</details>
<div class="details-content">

选择迭代次数的数据源。

- **内部**

​	    **迭代限制**参数面板上的值确定迭代次数。

- **外部**

​	    **N** 端口的输入信号值确定迭代次数。信号源必须位于 for 子系统的外部。

</div>
</div>

​	

<div class="details-box">
<details open>
<summary>迭代限制<div>5（默认） | 整数</div></summary>
</details>
<div class="details-content">

选择迭代次数的数据源。

当**迭代限制来源**为内部时，该参数启用。您可以在参数面板的编辑框中指定 for 子系统的迭代次数。

</div>
</div>

<div class="details-box">
<details open>
<summary>在外部设置下一个 i （迭代变量）<div>off（默认） | on</div></summary>
</details>
<div class="details-content">

控制迭代更新输入端口的显示。

当**显示迭代变量**的参数勾选时，该参数启用。您可以通过该选项来控制标签为 Next_i 的输入端口是否显示。

</div>
</div>





<div class="details-box">
<details open>
<summary>显示迭代变量<div>on（默认） | off</div></summary>
</details>
<div class="details-content">


控制 for iterator 的输出端口是否显示。

</div>
</div>


<div class="details-box">
<details open>
<summary>索引模式<div>从 1 开始（默认） | 从 0 开始</div></summary>
</details>
<div class="details-content">

选择从 1 或从 0 开始作为 for 子系统的初始索引。

</div>
</div>


<div class="details-box">
<details open>
<summary>迭代变量数据类型<div>int32（默认） | uint32 | int16 | uint16 | int8 | uint8 | double</div></summary>
</details>
<div class="details-content">

选择迭代变量的数据类型。

</div>
</div>



## 版本历史记录

在 MWORKS 2025b 推出

### 限制信息

无