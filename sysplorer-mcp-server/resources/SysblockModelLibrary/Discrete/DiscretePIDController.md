# DiscretePIDController
---
&nbsp;

离散时间 PID 控制器

- **库：** Sysblock / Discrete

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/DiscretePIDController/DiscretePIDController.png')" style="width: 200px; height: auto; border:solid 1px black;">


## 描述

DiscretePIDController 模块实现一个 PID 控制器（PID、PI、PD、仅 P 或仅 I）。该模块与**时域**参数设置为**离散时间**的 PIDController 模块相同。

此模块的输出是输入信号、输入信号积分和输入信号微分的加权和。权重为比例、积分和微分增益参数。

该模块支持多种控制器类型和结构体。此模块中可配置的选项包括：

​     **·** 控制器类型（PID、PI、PD、仅 P 或仅 I）- 请参阅**控制器**参数。

​     **·** 控制器形式（并行或理想） - 请参阅**形式**参数。

​     **·** 时域（连续时间或离散时间）- 请参阅**时域**参数。

​     **·** 初始条件和外部重置 - 请参阅**源和外部重置**参数。

​     **·** 输出饱和限制和抗饱和方法 - 请参阅**限制输出**参数。

​     **·** 无扰动切换和多环控制的信号跟踪 - 请参阅**启用跟踪模式**参数。

## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/DiscretePIDController.mo">DiscretePIDController.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/DiscretePIDController/DiscretePIDController01.png')" style="border: 1px solid black;width: 1000px; height: auto;">

**参考结果**

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/DiscretePIDController/DiscretePIDController02.png')" style="border: 1px solid black;width: 1000px; height: auto;">

## 端口

### 输入

<div class="details-box">
<details open>
<summary>Port_1 (u1) — 输入信号<div>标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">

**数据类型：** double | float | int8 | int16 | int32 | int64 | uint8 | uint16 | uint32 | uint64

</div>
</div>

<div class="details-box">
<details open>
<summary>P (P_In) — 比例增益<div>标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">

比例增益，由模块外部的信号源提供。

**数据类型：** double | float | int8 | int16 | int32 | int64 | uint8 | uint16 | uint32 | uint64

</div>
</div>


<div class="details-box">
<details open>
<summary>I (I_In) — 积分增益<div>标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">

​积分增益，由模块外部的信号源提供。

**数据类型：** double | float | int8 | int16 | int32 | int64 | uint8 | uint16 | uint32 | uint64

</div>
</div>


<div class="details-box">
<details open>
<summary>D (D_In) — 微分增益<div>标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">

微分增益，由模块外部的信号源提供。

**数据类型：** double | float | int8 | int16 | int32 | int64 | uint8 | uint16 | uint32 | uint64

</div>
</div>


<div class="details-box">
<details open>
<summary>N (N_In) — 滤波器系数<div>标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">

​	滤波器系数，由模块外部的信号源提供。

**数据类型：** double | float | int8 | int16 | int32 | int64 | uint8 | uint16 | uint32 | uint64

</div>
</div>


<div class="details-box">
<details open>
<summary>Port_2 (u2) — 外部重置<div>标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">

​	用于将积分器和滤波器重置为其初始条件。

**数据类型：** double | boolean

</div>
</div>


<div class="details-box">
<details open>
<summary>I0 (I0_In) — 积分器初始条件<div>标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">

​	积分器初始条件，由模块外部的信号源提供。

**数据类型：** double

</div>
</div>


<div class="details-box">
<details open>
<summary>D0 (D0_In) — 滤波器初始条件<div>标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">

​	滤波器初始条件，由模块外部的信号源提供。

**数据类型：** double

</div>
</div>


<div class="details-box">
<details open>
<summary>up (up) — 模块输出的饱和上限<div>标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">

​	模块输出的上限，由模块外部的信号源提供。如果比例、积分和微分增益作用于输入信号的加权总和超过此端口上提供的值，则模块输出上限为该值。

**数据类型：** double | float | int8 | int16 | int32 | int64 | uint8 | uint16 | uint32 | uint64

</div>
</div>


<div class="details-box">
<details open>
<summary>Io (Io) — 模块输出的饱和下限<div>标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">

模块输出的下限，由模块外部的信号源提供。如果比例、积分和微分增益作用于输入信号的加权总和低于此端口上提供的值，则模块输出下限为该值。

**数据类型：** double | float | int8 | int16 | int32 | int64 | uint8 | uint16 | uint32 | uint64

</div>
</div>


<div class="details-box">
<details open>
<summary>TR (TR) — 跟踪信号<div>标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">

​	控制器输出要跟踪的信号。

**数据类型：** double | float | int8 | int16 | int32 | int64 | uint8 | uint16 | uint32 | uint64

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>Port_1 (outport) — 输出<div>标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">

控制器的输出信号。

**数据类型：** double

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>控制器 — 指定在控制器中需要包含比例项、积分项和微分项中的哪些项<div>PID (默认) | PI | PD | P | I</div></summary>
</details>
<div class="details-content">

- **PID**

比例、积分和微分增益作用。

- **PI**

仅比例和积分增益作用。

- **PD**

仅比例和微分增益作用。

- **P**

仅微分增益作用。

- **I**

仅积分增益作用。

</div>
</div>


<div class="details-box">
<details open>
<summary>形式 — 指定控制器结构是“并行”还是“理想”<div>并行 (默认) | 理想</div></summary>
</details>
<div class="details-content">

- **并行**

控制器输出是比例、积分和微分增益作用的总和，三者分别用 P、I 和 D 独立进行加权。

- **理想**

比例增益 P 整体作用于所有增益（比例、积分和微分）的总和。

</div>
</div>


<div class="details-box">
<details open>
<summary>时域 — 指定控制器是“连续时间”还是“离散时间”<div>离散时间 (默认) | 连续时间</div></summary>
</details>
<div class="details-content">

指定控制器是“连续时间”还是“离散时间”。

</div>
</div>


<div class="details-box">
<details open>
<summary>采样时间（-1 表示继承）— 采样之间的离散间隔<div>-1 (默认) | 正标量</div></summary>
</details>
<div class="details-content">

通过输入正标量值指定采样时间。默认的离散采样时间为 -1，表示该模块从上游模块继承其采样时间。

</div>
</div>


<div class="details-box">
<details open>
<summary>积分器方法 — 离散时间控制器中积分的计算方法<div>前向欧拉 (默认) | 后向欧拉 | 梯形</div></summary>
</details>
<div class="details-content">

- **前向欧拉 - 正向矩形（左手）逼近方法**

这种方法适合较小的采样时间，此时奈奎斯特限制与控制器带宽相比来说比较大。对于较大的采样时间，前向欧拉方法可能带来不稳定性，即使离散采样的是在连续时间下表现稳定的系统。

- **后向欧拉 - 反向矩形（右手）逼近方法**

使用这种方法离散采样稳定的连续时间系统始终会生成稳定的离散时间结果。

- **梯形 - 双线性逼近法**

使用这种方法离散采样稳定的连续时间系统始终会生成稳定的离散时间结果。在所有可用的积分方法中，梯形方法可在离散化系统与对应的连续时间系统的频域属性之间生成最接近的匹配。

</div>
</div>


<div class="details-box">
<details open>
<summary>滤波器方法 — 离散时间控制器中微分的计算方法<div>前向欧拉 (默认) | 后向欧拉 | 梯形</div></summary>
</details>
<div class="details-content">

- **前向欧拉 - 正向矩形（左手）逼近方法**

这种方法适合较小的采样时间，此时奈奎斯特限制与控制器带宽相比来说比较大。对于较大的采样时间，前向欧拉方法可能带来不稳定性，即使离散采样的是在连续时间下表现稳定的系统。

- **后向欧拉 - 反向矩形（右手）逼近方法**

使用这种方法离散采样稳定的连续时间系统始终会生成稳定的离散时间结果。

- **梯形 - 双线性逼近法**

使用这种方法离散采样稳定的连续时间系统始终会生成稳定的离散时间结果。在所有可用的积分方法中，梯形方法可在离散化系统与对应的连续时间系统的频域属性之间生成最接近的匹配。

</div>
</div>


### 主要


<div class="details-box">
<details open>
<summary>源 — 指定控制器增益和滤波器系数的信号源<div>内部 (默认) | 外部</div></summary>
</details>
<div class="details-content">

- **内部**

使用模块内部参数指定 P、I、D 和 N 控制器增益和滤波器系数。

- **外部**

使用模块输入从外部指定 PID 增益和滤波器系数。

</div>
</div>


<div class="details-box">
<details open>
<summary>比例 (P) — 比例系数<div>1 (默认) | 标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">

通过模块内部参数为比例增益指定有限实数增益值。

</div>
</div>


<div class="details-box">
<details open>
<summary>积分 (I) — 积分系数<div>1 (默认) | 标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">

通过模块内部参数为积分增益指定有限实数增益值。

</div>
</div>


<div class="details-box">
<details open>
<summary>微分 (D) — 微分系数<div>1 (默认) | 标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">

通过模块内部参数为微分增益指定有限实数增益值。

</div>
</div>


<div class="details-box">
<details open>
<summary>滤波器系数 (N)<div>100 (默认) | 标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">

通过模块内部参数为滤波器系数指定有限实数增益值。

</div>
</div>


<div class="details-box">
<details open>
<summary>使用滤波导数<div>on (默认) | off</div></summary>
</details>
<div class="details-content">

将滤波器应用于微分项。

</div>
</div>


### 初始化

<div class="details-box">
<details open>
<summary>源 — 指定积分器和滤波器初始条件的信号源<div>内部 (默认) | 外部</div></summary>
</details>
<div class="details-content">

- **内部**

使用模块内部参数指定积分器和滤波器初始条件。

- **外部**

使用模块输入从外部指定初始条件。

</div>
</div>


<div class="details-box">
<details open>
<summary>积分器 — 通过模块内部参数为积分器指定初始条件<div>0 (默认) | 标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">

通过模块内部参数为积分器指定初始条件。

</div>
</div>


<div class="details-box">
<details open>
<summary>滤波器 — 通过模块内部参数为滤波器指定初始条件<div>0 (默认) | 标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">

通过模块内部参数为滤波器指定初始条件。

</div>
</div>


<div class="details-box">
<details open>
<summary>外部重置 — 用于重置积分器和滤波器值<div>不重置 (默认) | 上升沿 | 下降沿 | 任一沿 | 电平</div></summary>
</details>
<div class="details-content">

指定使模块将积分器和滤波器重置为初始条件的触发条件。选择不重置之外的任何选项都将在模块上启用重置端口以接收外部重置信号。

</div>
</div>


<div class="details-box">
<details open>
<summary>启用跟踪模式 — 激活信号跟踪<div>off (默认) | on</div></summary>
</details>
<div class="details-content">

信号跟踪使模块输出能够跟随 **TR** 端口信号提供的跟踪信号。

</div>
</div>


<div class="details-box">
<details open>
<summary>跟踪系数 (Kt) — 信号跟踪反馈环的增益<div>1 (默认) | 标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">

启用跟踪模式时，**TR** 端口信号与模块输出之间的差异将反馈到具有跟踪系数 **Kt** 的积分器输入中。

</div>
</div>


### 饱和


<div class="details-box">
<details open>
<summary>限制输出 — 将模块输出限制为指定的饱和值<div>off (默认) | on</div></summary>
</details>
<div class="details-content">

将模块输出限制为指定的饱和值。

</div>
</div>


<div class="details-box">
<details open>
<summary>源 — 输出饱和界限的信号源<div>内部 (默认) | 外部</div></summary>
</details>
<div class="details-content">

- **内部**

使用模块内部上限和下限参数指定输出饱和界限。

- **外部**

使用模块输入从外部指定输出饱和界限。

</div>
</div>


<div class="details-box">
<details open>
<summary>上限 — 模块输出的饱和上限<div>100 (默认) | 标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">

指定模块输出的上限值。

</div>
</div>


<div class="details-box">
<details open>
<summary>下限 — 模块输出的饱和下限<div>-100 (默认) | 标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">

指定模块输出的下限值。

</div>
</div>


<div class="details-box">
<details open>
<summary>抗饱和方法 — 选择积分器抗饱和方法<div>无 (默认) | 反算</div></summary>
</details>
<div class="details-content">

即使选择了限制输出，使得模块输出的值保持在指定的限制范围内。但是，模块内部积分器还可以继续增加（积分器饱和），使得模块内部信号可以无限大，导致控制器速度缓慢。因此需要激活抗饱和方法来避免上述问题。

</div>
</div>


<div class="details-box">
<details open>
<summary>反算系数 (Kb) — 抗饱和反馈环的增益系数<div>1 (默认) | 标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">

使用反算系数 (Kb) 参数指定抗饱和反馈电路的增益。

</div>
</div>


<div class="details-box">
<details open>
<summary>限制输出 — 将积分器输出限制为指定的饱和界限<div>off (默认) | on</div></summary>
</details>
<div class="details-content">

当积分器输出值达到指定范围边界时，积分器将关闭防止积分饱和。

</div>
</div>


<div class="details-box">
<details open>
<summary>上限 — 积分器的饱和上限<div>100 (默认) | 标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">

指定积分器输出的上限。一旦积分器输出值高于饱和上限，积分器输出将保持为该上限值。

</div>
</div>


<div class="details-box">
<details open>
<summary>下限 — 积分器的饱和下限<div>-100 (默认) | 标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">

指定积分器输出的下限。一旦积分器输出值低于饱和下限，积分器输出将保持为该下限值。

</div>
</div>


## 版本历史记录

- 在 2025a 推出

### 限制信息

- 输入数据类型不支持定点、枚举和总线
- 输出数据类型仅支持 double
