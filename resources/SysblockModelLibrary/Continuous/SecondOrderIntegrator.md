# SecondOrderIntegrator
---
&nbsp;

输入信号的二阶积分

**库：** Sysblock 模块库 / Continuous

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/SecondOrderIntegrator/SecondOrderIntegrator.png')" style="width: 100px; height: auto; transform: scale(1); border: solid 1px black;">

## 描述

Second-Order Integrator 模块和 Second-Order Integrator Limited 模块用来求解二阶初始值问题：
$$
\frac{d^{2}x}{dt^{2}} = u,
$$

$$
\left.\frac{dx}{dt}\right|_{t=0} = dx_{0},
$$

$$
\left.x\right|_{t=0} = x_{0}.
$$

其中 u 是系统的输入信号。因此，此模块是一个动态系统，它具有两个连续状态： x 和 dx/dt。这两个状态存在一种数学关系，即，dx/dt 是 x 的导数。为了在整个仿真过程中满足这种关系，Sysblock 对模块的参数和行为进行了诸多限制。

Second-Order Integrator Limited 模块除了默认情况下基于指定的上限和下限值来限制状态外，它与 Second-Order Integrator 模块完全相同。

Sysblock 可以使用若干不同的数值积分方法来计算模块的输出。每一种方法都有适用于特定情景的优点。使用**仿真设置**对话框的积分算法窗格可以选择最适合您的应用方法。所选求解器使用当前输入值计算 Second-Order Integrator 模块在当前时间步的状态。

使用模块参数对话框可以：

- 指定每个状态初始条件的来源是内部还是外部
- 为状态初始条件指定值
- 为一个或两个状态定义上限和下限
- 为每个状态指定绝对容差
- 选择外部重置条件
- 启用过零检测
- 当 x 达到饱和时重新初始化 dx/dt

### 初始条件

可以在模块对话框上将每个状态的初始条件逐个定义为参数，或者从外部信号输入一个或两个初始条件。

- 要将状态 x​ 的初始条件定义为模块参数，请从 **x 初始条件来源** 下拉菜单中选择**内部**，并在 **x 初始条件** 字段中输入值。
- 要从状态 x 的外部源提供初始条件，请将 **初始条件来源** 参数指定为**外部**。模块上出现一个额外的输入端口。
- 要将状态 dx/dt 的初始条件定义为模块参数，请从 **dx/dt 初始条件来源** 下拉菜单中选择**内部**，并在 **dx/dt 初始条件**字段中输入值。
- 要从外部源为状态 dx/dt 提供初始条件，请将 **dx/dt 初始条件来源** 指定为**外部**。模块上出现一个额外的输入端口。

如果您为两个状态初始条件都选择使用外部源，您的模块将如下所示。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/SecondOrderIntegrator/SecondOrderIntegrator_x0_dx0.png')" style="width: 100px; height: auto; transform: scale(1); border: solid 1px black;">

::: warning 注意 
如果您通过指定饱和界限来限制状态 x 或状态 dx/dt，而一个或多个初始条件位于对应的范围外，则相应的状态将被初始化为最接近的有效值，并计算一组初始条件。
:::



### 限制输出

为二阶系统建模时，您可能需要限制模块的状态。使用 Second-Order Integrator 模块，您可以限制状态 x 和 dx/dt，使它们相互独立。您甚至可以在仿真过程中更改限制。一个重要的原则是，上限必须严格大于对应的下限。

当您限制了一个或两个状态时，模块的外观将发生变化。在这两种状态都受限制的情况下，模块显示如下。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/SecondOrderIntegrator/SecondOrderIntegrator_limited.png')" style="width: 100px; height: auto; transform: scale(1); border: solid 1px black;">

对于每个状态，您可以使用模块参数对话框设置适当的饱和界限范围。

### 仅限制 x

如果您使用 Second-Order Integrator Limited 模块，默认情况下会限制两个状态。但是，您可以通过选择 **x 限制**并在相应的参数字段中输入范围，手动限制 Second-Order Integrator 模块上的状态 x。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/SecondOrderIntegrator/SecondOrderIntegratorLimited.png')" style="width: 300px; height: auto; transform: scale(1); border: solid 1px black;">

这样，模块将按如下方式确定状态的值：

- 当 x 小于或等于下限值时，x 的值保持在下限值，dx/dt 设置为零。
- 当 x 介于下限值和上限值之间时，两个状态都按照二阶 ODE 给出的轨迹变化。
- 当 x 大于或等于上限值时，x 的值保持在上限值，dx/dt 设置为零。

您可以选择在 x 达到饱和时将 dx/dt 重新初始化为新的值。

### 仅限制 dx/dt

与状态 x 一样，状态 dx/dt 默认情况下在 Second-Order Integrator Limited 模块对话框的 **dx/dt** 窗格上设置为受限制。您可以在 Second-Order Integrator 模块上手动设置参数 **dx/dt 限制**。在任一情况下，都必须为 dx/dt 输入适当的限制。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/SecondOrderIntegrator/SecondOrderIntegrator_limited_dxdt.png')" style="width: 300px; height: auto; transform: scale(1); border: solid 1px black;">

如果您只限制状态 dx/dt，模块将按如下方式确定 dx/dt 的值：

- 当 dx/dt 小于或等于下限值时，dx/dt 的值保持在下限值。
- 当 dx/dt 介于下限值和上限值之间时，两个状态都按照二阶 ODE 给出的轨迹变化。
- 当 dx/dt 大于或等于上限值时，dx/dt 的值保持在上限值。

当状态 dx/dt 保持在上限值或下限值时，x 的值受一阶初始值问题制约：
$$
\frac{dx}{dt} = L,
$$

$$
x(t_L) = x_L.
$$

其中 L 是 dx/dt 的限制值（上限或下限），$t_L$ 是 dx/dt 达到此限制值的时间，$x_L$ 是状态 x 在该时间的值。

### 限制两个状态

当您限制两个状态时，Sysblock 将通过限制允许的 dx/dt 上限和下限值，使状态在数学意义上保持一致。这种限制对于满足以下约束很有必要：

- 当 x 达到饱和限制值时，dx/dt 的值必须为零。
- 要使 x 离开上限值，dx/dt 的值必须严格为负。
- 要使 x 离开下限值，dx/dt 的值必须严格为正。

对于这些情况，dx/dt 的上限值必须严格为正，dx/dt 的下限值必须严格为负。

当两个状态都受限制时，模块将按如下方式确定状态：

- 当 x 达到其限制值时，产生的行为与“仅限制 x”中描述的相同。
- 当 dx/dt 达到其限制值之一时，产生的行为与“仅限制 dx/dt”中描述的相同 - 包括当 dx/dt 保持在其限制值时使用一阶 ODE 计算 x。在这种情况下，当 x 达到其限制值之一时，它会保持在该限制值并将 dx/dt 设置为零。
- 当二者同时达到各自的限制值时，状态 x 的行为将覆盖 dx/dt 的行为，以保持状态的一致性。

如果您限制了两个状态，可以选择在状态 x 达到饱和时重新初始化 dx/dt。如果重新初始化后的值超出了 dx/dt 的指定范围，则将 dx/dt 重新初始化为最接近的有效值，并计算一组初始条件。

### 重置状态

模块可以根据外部信号将其状态重置为指定的初始条件。要使模块重置其状态，请选中其中一个**外部重置**选项。模块输入端口下方将显示一个触发端口，并指示触发类型。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/SecondOrderIntegrator/SecondOrderIntegrator_reset.png')" style="width: 100px; height: auto; transform: scale(1); border: solid 1px black;">

- 选择**上升沿**可在重置信号从负值或零上升到正值时重置状态；
- 选择**下降沿**可在重置信号从正值下降到零或负值时重置状态；
- 选择**任一沿**可在重置信号从零变为非零值、从非零值变为零或改变符号时重置状态；

重置端口具有直接馈通。如果模块输出直接或通过一系列带有直接馈通的模块反馈到此端口中，则会产生代数环。

### 启用过零检测

此参数控制是否为此模块启用过零检测。

### 当 x 达到饱和时重新初始化 dx/dt

对于某些建模应用程序，当状态 x 达到其限制值时，必须重新初始化 dx/dt，以使 x 立即退出饱和状态。您可以通过在**属性**窗格上选择**当 x 达到饱和时重新初始化 dx/dt** 来实现这一目的。

如果启用了此选项，当 x 达到饱和的那一刻，Sysblock 将检查 dx/dt 初始条件（参数或信号）的当前值是否允许状态 x 立即退出饱和。如果允许，Sysblock 将使用那一刻的初始条件（参数或信号）值重新初始化状态 dx/dt。如果不允许，Sysblock 将在当前时刻忽略此参数，并将 dx/dt 设置为零，以使模块状态保持一致。

只有在 x 真正达到饱和限制的那一刻，此参数才适用。在那之后的任何时间，即在 x 保持饱和时，此参数并不适用。

### 指定模块输出的绝对容差

默认情况下，Sysblock 会使用在**仿真设置**对话框中指定的容差值来计算模块的输出。如果此值不能提供足够的误差控制，请在参数对话框的 **x 绝对容差**字段中为状态 x 指定更合适的值，在 **dx/dt 绝对容差**字段中为状态 dx/dt 指定更合适的值。Sysblock 将使用您指定的值来计算模块的状态值。

### 指定输出端口的显示

您可以控制是显示 x 还是 dx/dt 输出端口。您可以显示一个输出端口，也可以显示两个；但必须至少选择一个。



## 示例

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continuous/SecondOrderIntegrator.mo">SecondOrderIntegrator.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/SecondOrderIntegrator/SecondOrderIntegrator_example.png')" style="width: 500px; height: auto; transform: scale(1); border: solid 1px black;">

**参考结果**

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/SecondOrderIntegrator/SecondOrderIntegrator_output.png')" style="width: 800px; height: auto; transform: scale(1);border: solid 1px black;">

## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号 u<div>标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">


指向积分器系统的输入信号 u，指定为标量、向量、矩阵或多维数组。

**数据类型：** double

</div>
</div>



<div class="details-box">
<details open>
<summary>External Reset — 将状态重置为初始条件的信号 <div>标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">

外部重置信号是布尔标量、向量或矩阵，用于将模块状态重置为初始条件。

此端口直接馈通。

**依存关系：** 要启用此端口，请选择**外部重置**。  

**数据类型：** Boolean

</div>
</div>



<div class="details-box">
<details open>
<summary>x0 — 初始条件 x0<div>标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">


外部信号，用于为积分器系统指定初始条件 x0。您可以将初始条件指定为标量、向量、矩阵或多维数组。 

**数据类型：** double

</div>
</div>



<div class="details-box">
<details open>
<summary>dx0 — 初始条件 dx0<div>标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">


外部信号，用于为积分器系统指定初始条件 dx0。您可以将初始条件指定为标量、向量、矩阵或多维数组。

**数据类型：** double

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>x—输出信号 x<div>标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">


x 状态输出信号，以标量、向量、矩阵或多维数组形式提供。

**数据类型：** double

</div>
</div>



<div class="details-box">
<details open>
<summary>dx—输出信号 dx<div>标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">


dx 状态输出信号，指定为标量、向量、矩阵或多维数组。

**数据类型：** double

</div>
</div>



## 参数

### 参数 x

<div class="details-box">
<details open>
<summary>x 初始条件来源 — 状态 x 的初始条件来源<div>内部 (默认) | 外部</div></summary>
</details>
<div class="details-content">

指定状态 x 的初始条件的来源。

- **内部** — 从 **x 初始条件** 参数获取状态 x 的初始条件。
- **外部** — 从连接到 **x0** 输入端口的外部模块获取状态 x 的初始条件。

</div>
</div>

<div class="details-box">
<details open>
<summary>x 初始条件 — 状态 x 的初始条件<div>0 (默认) | 标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">


指定状态 x 的初始条件。

</div>
</div>



<div class="details-box">
<details open>
<summary>x 限制— 状态 x 的范围值<div>off  | on</div></summary>
</details>
<div class="details-content">

将模块的状态 x 限制为介于 **x 下限**和 **x 上限**参数之间的值。Second-Order Integrator 模块的默认值为 off。Second-Order Integrator Limited 的默认值为 on。

</div>
</div>

<div class="details-box">
<details open>
<summary>x 上限 — 状态 x 的上限<div>1 | 1e7 | 标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">


指定状态 x 的上限值。Second-Order Integrator 模块的默认值为 1e7。Second-Order Integrator Limited 模块的默认值为 1。

</div>
</div>

<div class="details-box">
<details open>
<summary>x 下限 — 状态 x 的下限<div>0 | -1e7 | 标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">


指定状态 x 的下限值。Second-Order Integrator 模块的默认值为 -1e7。Second-Order Integrator Limited 模块的默认值为 0。

</div>
</div>



<div class="details-box">
<details open>
<summary>绕回 x — 启用 x 的绕回<div>off(默认) | on</div></summary>
</details>
<div class="details-content">


在 **x 绕回上限值**和 **x 绕回下限值**参数之间启用 x 绕回。启用 x 绕回可在对旋转和循环状态轨迹建模时消除对过零检测的需求，减少求解器重置，提高求解器性能和准确性，并增加仿真时间范围。

</div>
</div>

<div class="details-box">
<details open>
<summary>x 绕回上限值 — 绕回 x 的上限值<div>pi (默认) | 标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">


指定绕回 x 的上限。

</div>
</div>

<div class="details-box">
<details open>
<summary>x 绕回下限值 — 绕回 x 的下限值<div>pi（默认值）| 标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">


指定绕回 x 的下限值。

</div>
</div>

<div class="details-box">
<details open>
<summary>x 绝对容差 — 用于计算状态 x 的绝对容差<div>-1（默认值）| 标量 | 向量</div></summary>
</details>
<div class="details-content">


指定用于计算状态 x 的绝对容差。

- 可以输入 -1、正实数标量或向量。
- 如果输入 -1，则 Sysblock 会使用**仿真设置**对话框中的容差值来计算模块状态 x。
- 如果输入实数标量值，则该值会覆盖**仿真设置**对话框中的容差且用于计算所有 x 状态。
- 如果输入实数向量，则该向量的维度必须匹配状态 x 的维度。这些值将覆盖**仿真设置**对话框中的容差。

</div>
</div>

### 参数 dx/dt

<div class="details-box">
<details open>
<summary>dx/dt 初始条件来源 — 状态 dx/dt 的初始条件来源<div>内部 (默认) | 外部</div></summary>
</details>
<div class="details-content">

指定状态 dx/dt 的初始条件的来源。

</div>
</div>

<div class="details-box">
<details open>
<summary>dx/dt 初始条件 — 状态 dx/dt 的初始条件<div>0 (默认) | 标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">


指定状态 dx/dt 的初始条件。

</div>
</div>

<div class="details-box">
<details open>
<summary>dx/dt 限制— 状态 dx/dt 的范围值<div>off  | on</div></summary>
</details>
<div class="details-content">

将模块的状态 dx/dt 限制为介于 **dx/dt 下限**和 **dx/dt 上限**参数之间的值。Second-Order Integrator 模块的默认值为 off。Second-Order Integrator Limited 的默认值为 on。如果您为 x 设置了饱和界限值，则 **dx/dt 上限**和 **dx/dt 下限**定义的区间必须包含零。

</div>
</div>

<div class="details-box">
<details open>
<summary>dx/dt 上限 — 状态 dx/dt 的上限<div>1e7（默认） | 标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">


指定状态 dx/dt 的上限值。如果您限制 x，则此参数的值必须严格为正。

</div>
</div>

<div class="details-box">
<details open>
<summary>dx/dt 下限 — 状态 dx/dt 的下限<div>-1e7（默认） | 标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">


指定状态 dx/dt 的下限值。如果您限制 x，则此参数的值必须严格为负。

</div>
</div>

<div class="details-box">
<details open>
<summary>dx/dt 绝对容差 — 用于计算状态 dx/dt 的绝对容差<div>-1（默认值）| 标量 | 向量</div></summary>
</details>
<div class="details-content">

指定用于计算状态 dx/dt 的绝对容差。

- 可以输入-1、正实数标量或向量。
- 如果输入-1，则 Sysblock 会使用**仿真设置**对话框中的容差值来计算模块状态 dx/dt。
- 如果输入一个数值，则该值会覆盖**仿真设置**对话框中的容差。

</div>
</div>

### 属性

<div class="details-box">
<details open>
<summary>外部重置 — 将状态重置为其初始条件<div>无  (默认) | 上升沿 | 下降沿 | 任一沿</div></summary>
</details>
<div class="details-content">

当重置信号中发生触发事件时，将状态重置为其初始条件。

- 选择**无**不将状态重置为初始条件；


- 选择**上升沿**可在重置信号从负值或零上升到正值时重置状态；

- 选择**下降沿**可在重置信号从正值下降到零或负值时重置状态；

- 选择**任一沿**可在重置信号从零变为非零值、从非零值变为零或改变符号时重置状态；

  

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

<div class="details-box">
<details open>
<summary>显示输出 — 要显示的输出端口<div> “两者”（默认值）| “x” | “dxdt”</div></summary>
</details>
<div class="details-content">


指定模块上的输出端口。

- **两者** — 同时显示 x 和 dx/dt 输出端口。
- **x** — 只显示 x 输出端口。
- **dx/dt** — 只显示 dx/dt 输出端口。

</div>
</div>


## 版本历史记录

- 在 2026a 推出

### 限制信息

- 暂不支持嵌入式代码生成
- 不支持总线、枚举值类型