# VariableTransportDelay
---
&nbsp;

可变传输延迟建模

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/VariableTransportDelay/VariableTransportDelay.png')" style="width:200px; border: 1px solid black;">

**库：** Sysblock 模块库 / Continuous

## 描述

VariableTransportDelay 模块可用于仿真可变传输延迟现象，如管道中的不可压缩液体流动。VariableTransportDelay 模块有两个输入端口，分别是被延迟的输入信号 $u$ 和瞬时传输延迟 $t_i$。模块内部根据瞬时传输延迟 $t_i$ 计算实际传输延迟 $t_d$，然后将输入信号 $u$ 延迟 $t_d$ 秒后作为模块输出 $y$。

假设不可压缩流体以速度 $V(t)$ 通过长度为 $L$ 的管道，入口处的流体速度为 $V_i$，流体温度为 $T_i$，出口处的流体速度为 $V_o$，流体温度为 $T_o$。假设，$t=0$ 时，管道为空，并且直到 $t=2$ 时，在出口处都没有流体。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/VariableTransportDelay/定长管道不可压缩流动.png')" style="width:600px; border: 1px solid black;">


当 $t<2$ 时，出口处实际都没有流体，$T_o$ 的值采用初始输出温度。当 $t\ge2$ 时，出口处的流体温度 $T_o(t)$ 可建模为 $t-t_d$ 时刻入口处的流体温度，即入口处的流体在经历了 $t_d$ 秒的传输延迟之后到达了管道出口，即 $T_o(t)=T_i(t-t_d)$。因此，下式成立：

$$
\begin{align}
\int_{t-t_d}^{t}V(\tau)d\tau&=L\\
\int_{t-t_d}^{t}\frac{1}{\frac{L}{V(\tau)}}d\tau&=1
\end{align}
$$

令 $t_i=\frac{L}{V(\tau)}$，则可将上式整理为：

$$
\int_{t-t_d}^{t}\frac{1}{t_i}=1
$$

利用上式可解出实际传输延迟 $t_d$，进而计算出口处的温度 $T_o$。

## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continuous/VariableTransportDelay.mo">VariableTransportDelay.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/VariableTransportDelay/VariableTransportDelay_example.png')" style="width:1000px; border: 1px solid black;">

### 参考结果

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/VariableTransportDelay/Example_output.png')" style="width:900px; border: 1px solid black;">

## 端口

### 输入

<div class="details-box">
<details open>
<summary> u - 输入信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

输入信号 $u$，指定为标量、向量、矩阵。

**数据类型：** double

</div>
</div>

<div class="details-box">
<details open>
<summary> ti - 瞬时延迟 <div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

瞬时延迟 $t_i$，指定为标量、向量或矩阵。  

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

指定瞬时延迟 $t_i$ 的最大值。  

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
<summary>使用固定缓冲区大小<div>0（默认值：即为不勾选）| 标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

指定是否使用固定大小的缓冲区。勾选后，如果缓冲区已满，新数据将替换缓冲区中已有的数据。

</div>
</div>

## 版本历史记录

- 在 2025a 推出

### 限制信息

- 输入信号 $u$ 和瞬时延迟 $t_i$ 仅支持 double 类型；
- 输入信号 $u$、瞬时延迟 $t_i$、最大延迟、初始输出不能为维度大于 2 的多维数组。若它们中不止一个是非标量，则所有非标量的维度必须相同；
- 瞬时延迟 $t_i$ 端口不允许空悬；
- 瞬时延迟 $t_i$ 为负数或 0 时，模块输出保持不变（维持 $t_i>0$ 的最后时刻值）；
- 初始缓冲区大小必须 $\ge5$；
- 模块不能位于触发子系统、离散的 if action 子系统、离散的 switch case 子系统中；
- 模块暂不支持嵌入式代码生成。
