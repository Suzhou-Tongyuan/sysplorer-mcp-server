# Integrator
---
&nbsp;
对信号求积分。

**库：** Sysblock 模块库 / Continuous

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/Integrator/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

Integrator 模块求输入信号关于时间的积分，并将结果作为输出信号。
Sysblock将 Integrator 模块作为具有一种状态的动态系统进行处理。模块动态由以下方程指定：

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/Integrator/2.png')" style="width: 100px; height: auto; transform: scale(1);">

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/Integrator/3.png')" style="width: 100px; height: auto; transform: scale(1);">


其中：

- *u* 是模块输入；
- *y* 是模块输出；
- *x* 是模块状态；
- *x0* 是 *x* 的初始条件。

所选求解器会使用当前输入值和前一个时间步的状态值计算 Integrator 模块在当前时间步的输出。为支持此计算模型，Integrator 模块会保存在当前时间步的输出，以供求解器计算其在下一个时间步的输出。该模块还为求解器提供了初始条件，用于计算该模块在仿真开始时的初始状态。初始条件的默认值为 0。使用模块参数对话框可以为初始条件指定其他值，或在模块上创建初始值输入端口。

使用参数对话框可以：

- 定义积分的上限和下限；
- 创建可将模块的输出（状态）重置为初始值的输入，具体取决于输入的变化方式；
- 创建可选的状态输出，以便模块的输出值可以触发模块重置。

### 初始条件

可以在模块对话框上将初始条件定义为参数，或者从外部信号输入初始条件：

- 要将初始条件定义为模块参数，请将**初始条件来源**参数指定为**内部**并在**初始条件**字段中输入值；

- 要从外部源提供初始条件，请将**初始条件来源**参数设置为**外部**。模块上出现一个额外的输入端口。

  <img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/Integrator/4.png')" style="width: 100px; height: auto; transform: scale(1);">

  ::: warning 注意 
  如果选择**限制输出**参数，初始条件必须在饱和界限内。如果初始条件不在模块饱和界限范围内，该模块会显示错误消息。
  :::

  
### 限制输出

要将输出信号限制在指定的值域范围内，请选择**限制输出**并指定饱和界限。当输出达到其中一个限值时，积分动作将终止（效果同 der(x)=0）。在仿真期间，值域上下限可更改，但不能更改是否限制输出。该模块按照以下准则确定输出信号值：

- 当积分值小于或等于饱和下限时，输出信号值为饱和下限；
- 当积分值在饱和下限与饱和上限之间时，输出为积分值；
- 当积分值大于或等于饱和上限时，输出信号值为饱和上限。

要生成指示状态何时受饱和界限限制的信号，请选择**显示饱和端口**。第二个输出端口出现在模块上。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/Integrator/5.png')" style="width: 100px; height: auto; transform: scale(1);">

饱和信号具有以下三个值之一：

- `1` - 状态受饱和上限限制
- `0` - 状态不受限制
- `–1` - 状态受饱和下限限制

当限制 Integrator 模块输出时，该模块有三个过零信号：一个用于检测积分值何时超出饱和上限，一个用于检测积分值何时小于饱和下限，一个用于检测积分值从超限值回归到非超限值(限幅后应该是检测输入值过零)。

### 绕回状态

对于周期性的状态变量，如角度，避免长时间积分后数值过大带来负面问题。一种积分重置的替代方案，状态量正常积分，但将输出值限制到指定值域范围内。**与限制输出选项互斥**。

Integrator 模块支持绕回状态，通过在模块参数对话框上选中**绕回状态**来启用这些状态。

### 重置状态

模块可以根据外部信号将其状态重置为指定的初始条件。要使模块重置其状态，请选中其中一个**外部重置**选项。模块输入端口下方将显示一个触发端口，并指示触发类型。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/Integrator/6.png')" style="width: 100px; height: auto; transform: scale(1);">

- 选择**不重置**信号则不会重置；
- 选择**上升沿**可在重置信号从负值或零上升到正值时重置状态；
- 选择**下降沿**可在重置信号从正值下降到零或负值时重置状态；
- 选择**任一沿**可在重置信号从零变为非零值、从非零值变为零或改变符号时重置状态；
- 选择**电平**可在外部输入电平时重置状态。

重置端口具有直接馈通。如果模块输出直接或通过一系列带直接馈通的模块反馈到此端口中，则会产生代数环。使用 Integrator 模块的状态端口可以反馈该模块的输出，而不会创建代数环。

### 显示状态端口

在 Integrator 模块的参数对话框上选中**显示状态端口**复选框会导致 Integrator 模块的顶部显示一个附加输出端口，即状态端口。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/Integrator/7.png')" style="width: 100px; height: auto; transform: scale(1);">

状态端口的输出在时间步中的显示会早于 Integrator 模块输出端口的输出的显示。使用状态端口打破代数环和提供状态给其它系统用。

### 显示饱和端口

在 Integrator 模块的参数对话框上选中**显示饱和端口**复选框会导致 Integrator 模块的右下侧显示一个附加输出端口，即饱和端口。

使用饱和状况相当于新增一个输出端口，取值 1、0、-1 分别表示状态值超上限、未超限、超下限。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/Integrator/8.png')" style="width: 100px; height: auto; transform: scale(1);">

## 示例

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continuous/Integrator.mo">Integrator.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/Integrator/9.png')" style="width: 500px; height: auto; transform: scale(1);">

**参考结果**

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/Integrator/10.png')" style="width: 800px; height: auto; transform: scale(1);border-top: 1px solid black;">

## 端口

### 输入

<div class="details-box">
<details open>
<summary>Port_1 — 要积分的信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

输入信号是此模块积分的实数值标量、向量或矩阵。此端口没有直接馈通。  

**数据类型：** double

</div>
</div>




<div class="details-box">
<details open>
<summary>External Reset — 将状态重置为初始条件的信号 <div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

外部重置信号是布尔标量、向量或矩阵，用于将模块状态重置为初始条件。

**依存关系：**要启用此端口，请选择**外部重置**。  

**数据类型：** Boolean

</div>
</div>




<div class="details-box">
<details open>
<summary>x0 — 初始条件<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

初始条件信号是为模块设置初始条件的实数值标量、向量或矩阵。此端口具有直接馈通。

**依存关系：**要启用此端口，请将**初始条件**参数设置为**外部**。  

**数据类型：** double

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>Port_1 — 对信号求积分<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

输出信号是具有积分输入信号值的标量、向量或矩阵。积分信号的维度与输入信号的维度匹配。

**数据类型：** double

</div>
</div>



<div class="details-box">
<details open>
<summary>Port_2 — 输出饱和信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

输出饱和信号是标量、向量或矩阵，它指示处于模块状态的每个元素何时受到饱和上限或下限的限制。信号值指示该值是否受限以及应用哪个限制。

- `1` - 值受饱和下限限制

- `0` - 值受饱和下限限制

- `–1` - 值受饱和下限限制

模块状态信号是具有与模块状态值匹配的值的实数值标量、向量或矩阵。

**依存关系：**要启用此端口，请选择**显示饱和端口**。  

**数据类型：** double

</div>
</div>




<div class="details-box">
<details open>
<summary>Port_3 — 模块状态<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

模块状态信号是具有与模块状态值匹配的值的实数值标量、向量或矩阵。

**依存关系：**要启用此端口，请选择**显示状态端口**。  

**数据类型：** double

</div>
</div>


  

## 参数

<div class="details-box">
<details open>
<summary>外部重置 — 将状态重置为其初始条件<div>不重置  (默认) | 上升沿 | 下降沿 | 任一沿 | 电平</div></summary>
</details>
<div class="details-content">

- 选择**不重置**信号则不会重置；
- 选择**上升沿**可在重置信号从负值或零上升到正值时重置状态；
- 选择**下降沿**可在重置信号从正值下降到零或负值时重置状态；
- 选择**任一沿**可在重置信号从零变为非零值、从非零值变为零或改变符号时重置状态；
- 选择**电平**可在外部输入电平时重置状态。

</div>
</div>


 

<div class="details-box">
<details open>
<summary>初始条件来源 — 使用外部信号设置初始条件的选项<div>内部 (默认) | 外部</div></summary>
</details>
<div class="details-content">

选择初始条件的来源：  

- 内部 - 从初始条件参数获取状态的初始条件；

- 外部 - 从外部信号获取状态的初始条件。选择此选项时，输入端口会出现在模块上。

</div>
</div>


<div class="details-box">
<details open>
<summary>初始条件 — 初始状态<div>0 (默认) | 实数标量或数组</div></summary>
</details>
<div class="details-content">

设置 Integrator 模块的初始状态。

</div>
</div>



<div class="details-box">
<details open>
<summary>限制输出 — 将模块输出值限制在指定范围内<div>off（Integrator 的默认值） | on（Integrator Limited 的默认值）</div></summary>
</details>
<div class="details-content">

将模块的输出限制为介于饱和下限和饱和上限参数之间的值。  

- 选中此复选框会将模块输出限制为介于饱和下限和饱和上限参数之间的值；

- 清除此复选框后，不会限制模块的输出值。

</div>
</div>


<div class="details-box">
<details open>
<summary>饱和上限 — 指定积分的上限<div>0.0 (默认) | 标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

将积分的上限指定为标量、向量或矩阵。您必须指定在输出最小值和输出最大值参数值之间的值。

</div>
</div>


<div class="details-box">
<details open>
<summary>饱和下限 — 指定积分的下限<div>0.0 (默认) | 标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

将积分的下限指定为标量、向量或矩阵。您必须指定在输出最小值和输出最大值参数值之间的值。

</div>
</div>




<div class="details-box">
<details open>
<summary>绕回状态 — 启用状态绕回<div>off(默认) | on</div></summary>
</details>
<div class="details-content">

在绕回状态上限值和绕回状态下限值参数之间启用状态绕回。启用绕回状态可在对旋转和循环状态轨迹建模时消除对过零检测的需求，减少求解器重置，提高求解器性能和准确性，并增加仿真时间范围。  
如果将绕回状态上限值指定为 inf 并将绕回状态下限值指定为 -inf，则不会发生绕回。

</div>
</div>


<div class="details-box">
<details open>
<summary>绕回状态上限值 — 指定绕回状态的上限值<div>0.0 (默认) | 标量 | 向量</div></summary>
</details>
<div class="details-content">

模块输出的上限。

</div>
</div>


<div class="details-box">
<details open>
<summary>绕回状态下限值 — 指定绕回状态的下限值<div>0.0 (默认) | 标量 | 向量</div></summary>
</details>
<div class="details-content">

模块输出的下限。

</div>
</div>


<div class="details-box">
<details open>
<summary>显示饱和端口 — 启用饱和输出端口<div>on (默认) | off</div></summary>
</details>
<div class="details-content">

选中此复选框可将饱和输出端口添加到模块中。清除此复选框时，模块没有饱和输出端口。

</div>
</div>


 

<div class="details-box">
<details open>
<summary>显示状态端口 — 启用状态输出端口<div>off(默认) | on</div></summary>
</details>
<div class="details-content">

选中此复选框可将状态输出端口添加到模块中。清除此复选框时，模块没有状态输出端口。

</div>
</div>





<div class="details-box">
<details open>
<summary>启用过零检测 — 启用过零检测<div>on (默认) | off</div></summary>
</details>
<div class="details-content">

选择此项以启用过零检测。

</div>
</div>


## 版本历史记录

- 在 2025a 推出

### 限制信息

- 暂不支持嵌入式代码生成；
- 不支持总线、枚举值类型。