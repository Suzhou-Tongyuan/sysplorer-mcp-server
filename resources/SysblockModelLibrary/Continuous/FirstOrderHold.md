# FirstOrderHold

计算输入信号的一阶保持

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/FirstOrderHold/1.png')" style="width: 100px; height: auto; transform: scale(1); border: solid 1px black;">

**库：** Sysblock / Continuous

## 描述

FirstOrderHold 模块通过线性外推来实现输入信号的一阶保持，其**输出信号 y** 为**输入信号 u** 的连续分段线性近似信号。该模块具有如下两种作用：

1. 将离散采样信号转换为连续信号；
2. 用来打破模型代数环

FirstOrderHold 的一阶保持输出计算方式依赖用户所选择的线性外推算法（缓慢或快速，详见后续算法解释）。

## 示例

<helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continuous/FirstOrderHold.mo">FirstOrderHold.mo</helpButton>。

**参考示例模型**

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/FirstOrderHold/2.png')" style="width: 500px; height: auto; transform: scale(1); border: solid 1px black;">

**参考结果**

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/FirstOrderHold/3.png')" style="width: 500px; height: auto; transform: scale(1); border: solid 1px black;">

## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">

输入信号，指定为标量、向量、矩阵或多维数组。

**数据类型：double**

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">

输出信号，指定为标量、向量、矩阵或多维数组。

**数据类型：double**

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>初始输出<div> 0（默认值）| 标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">

模块的初始输出值。
**数据类型：double**

</div>
</div>

<div class="details-box">
<details open>
<summary>输出算法<div> 缓慢（避免过冲）（默认值）| 快速（最小化误差）</div></summary>
</details>
<div class="details-content">

设置用于生成输出信号的线性外推算法。缓慢算法可避免输入信号过冲；快速算法可将输出中的误差降至最低，但可能会使输入信号过冲。

</div>
</div>

<div class="details-box">
<details open>
<summary>容差<div>1e7（默认值）| 标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">

相对外插误差超过容差值时，下一步的输出重置为上一步的输入。

**数据类型：double**

</div>
</div>

<div class="details-box">
<details open>
<summary>允许连续输入<div> true（默认值）| false </div></summary>
</details>
<div class="details-content">

勾选允许连续输入，则输入信号可为连续也可为离散。当前版本默认勾选，暂不支持设置。

</div>
</div>

## 输出算法

### 缓慢（防止过冲）

缓慢算法执行的线性外插可以描述为：

$$
y(t) = M_k (t - T_k) + C_k \quad \forall \;  t \in [T_k, T_{k + 1})
$$

其中 

- $T_k$ 是执行第 $k$ 个主时间步的时间；
- $U_k$ 是第 $k$ 个主时间步的输入；
- $C_k$ 和 $M_k$ 是线性外插的系数；
- $y_k$ 是时间 $T_k$ 处的连续输出；

$$
\begin{aligned}
&M_{k + 1} = \frac{U_k - U_{k - 1}}{T_k - T_{k - 1}} \\
&C_k = {y_k}
\end{aligned}
$$

### 快速（最小化误差）

$$
y(t) = N_k (t - T_k) + C_k \quad \forall \;  t \in [T_k, T_{k + 1})
$$

其中 

- $T_k$ 是执行第 $k$ 个主时间步的时间；
- $U_k$ 是第 $k$ 个主时间步的输入；
- $\hat{U}$ 是第 (k+1) 个主时间步的输入的预测值；
- $C_k$ 和 $N_k$ 是线性外插的系数；
- $y_k$ 是时间 $T_k$ 处的连续输出；

$$
\begin{aligned}
&H_k = T_k - T_{k - 1} \\
&M_{k + 1} = \frac{U_k - U_{k - 1}}{H_k} \\
&\hat{U} = U_k + M_{k + 1} H_k \\
&N_{k + 1} = \frac{\hat{U} - y_k}{H_k} = \frac{(U_k - y_k) + (U_k - U_{k - 1})}{T_k - T_{k - 1}} \\
&C_k = {y_k}
\end{aligned}
$$

## 版本历史记录

- 在 2025b 推出

### 限制信息

- 初始输入不允许填 INF 和 NAN，也不允许填空值；
- 容差必须是非负实数，且不允许填 INF 和 NAN，也不允许填空值；
- 暂不支持取消勾选允许连续输入。
