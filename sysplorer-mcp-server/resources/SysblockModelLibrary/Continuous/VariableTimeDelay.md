# VariableTimeDelay

可变时滞建模

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/VariableTimeDelay/VariableTimeDelay.png')" style="width: 100px; border: 1px solid black;">

**库：** Sysblock / Continuous

## 描述

Variable Time Delay 模块具有两个输入端口，分别是数据输入 $u$ 和时滞输入 $t_o$ 。模块将输入信号 $u$ 延迟 $t_o$ 秒后作为数据输出 $y$，即：
$$
y(t) = u(t-t_o(t))
$$
其中，时滞输入 $t_o$ 是随时间变化的。若 $t-t_o(t)\le0$，则模块输出 $y$ 为初始输出。

时滞输入 $t_o$ 为负数时，模块内部会将其截减为 0。时滞输入 $t_o$ 大于最大延迟参数时，模块内部会将其截减为最大延迟。

## 示例

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continuous/VariableTimeDelay.mo">VariableTimeDelay.mo</helpButton>。

**示例**

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/VariableTimeDelay/VariableTimeDelay_example.png')" style="width: 600px; border: 1px solid black;">

**参考结果**

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/VariableTimeDelay/Example_output.png')" style="width: 800px; border: 1px solid black;">

## 端口

### 输入

<div class="details-box">
<details open>
<summary> u - 输入信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

输入信号  $u$ ，指定为标量、向量、矩阵。


**数据类型：** double

</div>
</div>

<div class="details-box">
<details open>
<summary> t0 - 时滞输入 <div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

瞬时延迟 $t_0$ ，指定为标量、向量或矩阵。 

**数据类型：** double

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary> y - 输出信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

 输出信号 $y$，维度为标量、向量或矩阵。 

**数据类型：** double

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>最大延迟<div>10（默认值）| 标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

  指定瞬时延迟 $t_0$ 的最大值。

</div>
</div>

<div class="details-box">
<details open>
<summary>初始输出<div>0（默认值）| 标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

指定模块输出 $y$ 的初始值。 

</div>
</div>

<div class="details-box">
<details open>
<summary>初始缓冲区大小<div>1024（默认值）| 标量</div></summary>
</details>
<div class="details-content">

指定模块内部初始缓冲区的大小。

</div>
</div>

<div class="details-box">
<details open>
<summary>使用固定缓冲区大小<div>off（默认）| on</div></summary>
</details>
<div class="details-content">

指定是否用固定大小的缓冲区。勾选后，如果缓冲区已满，新数据将替换缓冲区中已有的数据。

</div>
</div>

## 版本历史记录

- 在 2025a 推出

### 限制信息

- 数据输入 $u$ 和时滞输入 $t_o$ 仅支持 double 类型；
- 数据输入 $u$、时滞输入 $t_o$、最大延迟、初始输出不能为维度大于 2 的多维数组。若它们中不止一个是非标量，则所有非标量的维度必须相同；
- 数据输入 $u$ 端口和数据输出 $y$ 相连，或时滞输入 $t_o$ 和数据输出 $y$ 相连都将引入代数环；
- 初始缓冲区大小必须 $\ge5$；
- 模块不能位于触发子系统、离散的 if action 子系统、离散的 switch case 子系统中；
- 模块暂不支持嵌入式代码生成.
