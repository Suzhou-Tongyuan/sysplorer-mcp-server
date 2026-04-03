# RateTransition
---
处理不同速率和任务之间的数据传输

**库：** Sysblock /  SingalAttributes

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalAttributes/RateTransition/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

Rate Transition 模块可将数据从按某速率运行的模块的输出端口传输到另一个按不同速率运行的模块的输入端口。

## 示例

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalAttributes/RateTransition.mo">RateTransition.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalAttributes/RateTransition/2.png')" style="width: 500px; height: auto; transform: scale(0.8);">

### 示例说明

- SineWave：生成一个正弦波信号，示例中将采样时间设置为 0.01；
- RateTransition：将正弦波信号从一个采样率转换到另一个采样率，示例中将采样时间指定为 0.1；
- Scope：显示原始信号和转换后的信号。

### 仿真结果

- 原始正弦波信号：由 SineWave 模块生成的正弦波信号，采样时间为设定的 0.01 秒；
- 转换后的信号：经过 RateTransition 模块转换后的信号，采样时间为指定的 0.1 秒。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalAttributes/RateTransition/3.png')" style="width: 800px; height: auto; transform: scale(1);border-top: 1px solid black">

## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 向量 | 矩阵 | N 维数组</div></summary>
</details>
<div class="details-content">

要转换为新采样率的输入信号，指定为标量、向量、矩阵或 N 维数组。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | fixedPoint | enum | bus

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 向量 | 矩阵 | N 维数组</div></summary>
</details>
<div class="details-content">

输出信号是转换为您指定的采样率的输入信号。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | fixedPoint | enum | bus

</div>
</div>

## 参数

<!-- ### `确保数据传输的数据完整性` — 确保数据完整性 `on` （默认） | `off`

如果选中此复选框，生成的代码可以在模块传输数据时确保数据的完整性。如果选中此复选框，而传输是不确定的（请参阅**确保确定性数据传输**），根据输入速率和输出速率的优先级，生成的代码将使用正确的算法，使用一个或多个缓冲区来保护数据传输过程中的数据完整性。

否则，Rate Transition 模块要么会简化，要么通过使用复制操作执行数据传输来生成代码。这种不受保护的模式需要较少的内存。但复制操作也可能会中断，从而导致数据传输过程中损失数据完整性。如果您希望生成的代码能够在运行时保证最大的响应性（即，不确定性传输）和数据完整性，请选中此复选框。有关详细信息，请参阅[Rate Transition 模块选项](https://ww2.mathworks.cn/help/releases/R2022b/rtw/ug/handle-rate-transitions.html#f1016724) (Simulink Coder)。



### `确保确定性数据传输(最大延迟)` — 确保确定性数据传输 `on` （默认） | `off`


如果选中此复选框，生成的代码将按照速率较慢的模块的速率传输数据，即确定性传输。如果不选中此复选框，则在源模块上有新数据且接收模块能够接收数据时，会发生数据传输。这样可以避免传输延迟，确保系统以最大的响应性运行。但是，传输的发生具有不可预测性，这在某些应用中是不希望出现的。有关详细信息，请参阅[Rate Transition 模块选项](https://ww2.mathworks.cn/help/releases/R2022b/rtw/ug/handle-rate-transitions.html#f1016724) (Simulink Coder)。 -->


<div class="details-box">
<details open>
<summary>初始条件 — 初始条件<div>0 （默认） | 标量 | 向量 | 矩阵 | N 维数组</div></summary>
</details>
<div class="details-content">

此参数仅适用于慢速到快速转移。它指定当连接到 RateTransition 模块的输入的慢速模块未提供输入信号而导致没有输出信号时，RateTransition 模块在转移初期的初始输出。Sysblock 不允许此模块的初始输出为 Inf 或 NaN。您指定的值必须是标量，或者与输入信号具有相同的维度。

</div>
</div>


<div class="details-box">
<details open>
<summary>输出端口采样时间选项 — 指定输出端口采样时间的模式<div>指定 （默认） | 继承 | 倍数</div></summary>
</details>
<div class="details-content">

指定用于设置输出端口采样时间的模式。选项包括：

- 指定 - 允许您使用**输出端口采样时间**参数来指定 RateTransition 模块将输入速率转移成的输出速率。
- 继承 - 指定 Rate Transition 模块继承输出端口所连接到的模块的输出速率。
- 倍数 - 允许您使用**采样时间倍数 (>0)** 参数来指定 RateTransition 模块的输出采样率是其也都输入速率的几倍。

如果您选择继承，而连接输出端口的所有模块继承采样时间，则会采用模型中最快的采样时间。

</div>
</div>


<div class="details-box">
<details open>
<summary>输出端口采样时间 — 输出速率<div>-1 （默认） | 标量 | 向量</div></summary>
</details>
<div class="details-content">

请输入一个值，指定模块要将其输入速率转换成的输出速率。默认值 (-1) 指定 RateTransition 模块继承输出端口所连接到的模块的输出速率。有关如何指定输出速率的信息，请参阅[指定采样时间](/Doc/Sysblock/Modeling/ConfigureSignals/SampleTime/SpecifyTime.html)。

#### 依存关系

要启用此参数，请将**输出端口采样时间选项**设置为“指定”。

</div>
</div>


<div class="details-box">
<details open>
<summary>采样时间倍数(>0) — 采样时间倍数<div>1 （默认） | 正标量</div></summary>
</details>
<div class="details-content">

请输入一个正值，将输出速率指定为输入端口采样时间的倍数。默认值 (1) 指定输出速率与输入采样率相同。值 0.5 指定输出速率是输入速率的一半。值 2 指定输出速率是输入速率的两倍。

#### 依存关系

要启用此参数，请将**输出端口采样时间选项**设置为“倍数”。

</div>
</div>



## 版本历史记录

- 在 2025a 推出

### 限制信息

1. 暂不支持 RateTransition 模块上将出现一个标签，指示仿真行为；  
2. 暂不支持确保数据传输的数据完整性的复选框；  
3. 暂不支持确保确定性数据传输(最大延迟)的复选框；  
4. 输入和输出信号暂不支持 half、int 64 和 uint64 的数据类型。


## 另请参阅

### 主题

- [指定采样时间](/Doc/Sysblock/Modeling/ConfigureSignals/SampleTime/SpecifyTime.html)
- [采样时间的类型](/Doc/Sysblock/Modeling/ConfigureSignals/SampleTime/TypesTime.html)
