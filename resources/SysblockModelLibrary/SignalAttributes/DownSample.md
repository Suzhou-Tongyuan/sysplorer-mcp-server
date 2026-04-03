# DownSample
---
通过采样因子对输入信号进行降采样

**库：** Sysblock /  SingalAttributes

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalAttributes/DownSample/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

DownSample 模块通过删除样本降低输入信号的采样率。当模块执行基于帧的处理时，它会独立地对输入矩阵每列中的数据进行重采样。当模块执行基于样本的处理时，它将输入的每个元素视为一个单独的通道，并在时间上对输入数组的每个通道进行重采样。重采样后的采样率是输入采样率的 1/M，其中 M 是下采样因子的值。DownSample 模块通过在每个输出样本之后丢弃连续的 M–1 个样本来对输入进行重采样。

当您将速率选项参数设置为“强制单采样”时，此模块支持触发子系统。

## 示例

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalAttributes/DownSample.mo">DownSample.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalAttributes/DownSample/2.png')" style="width: 500px; height: auto; transform: scale(0.8);">

### 示例说明

- SineWave 模块：生成一个正弦波信号；
- DownSample 模块：对输入信号进行降采样。降采样因子示例中设置为 3，表示每个输出样本之间丢弃 2 个样本；
- Scope 模块：显示输入信号的波形。

### 仿真结果

- 原始正弦波信号：由 SineWave 模块生成的正弦波信号；
- 降采样后的信号：经过 DownSample 模块降采样后的信号，采样率降低为原来的 1/3。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/SignalAttributes/DownSample/3.png')" style="width: 800px; height: auto; transform: scale(1);border-top: 1px solid black">

## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 数据输入<div>列向量 | 矩阵 | N 维数组</div></summary>
</details>
<div class="details-content">

指定要降低采样率的输入数据，可以是列向量或矩阵。

当您将输入信号处理方法参数设置为“基于样本”时，输入可以是 N 维数组。基于采样的处理将每个元素视为一个独立的通道。

当您将输入信号处理方法设置为“基于帧”并且速率选项设置为“强制单采样”时，模块支持可变大小的输入信号，因此在仿真过程中，帧长度（行数）和通道数（列数）可以发生变化。当模块接受可变大小的输入信号时，它们可以具有任意的帧长度，即输入帧长度不一定是降采样因子的倍数。当指定固定大小的信号时，在某些条件下，帧长度可以是任意的。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | fixedPoint 

</div>
</div>


<!-- ### **M** — 下采样因子 正整数

*自 R2023a 起*

将缩减采样因子 *M* 指定为正值 整数。

#### 屬地

要启用此端口，请设置 **Downsample 因子 source** 参数设置为 .`Input port`

**数据类型：** | | | | | | |`single``double``int8``int16``int32``uint8``uint16``uint32` -->

### 输出

<div class="details-box">
<details open>
<summary>y — 下采样输出<div>列向量 | 矩阵</div></summary>
</details>
<div class="details-content">

采样率降低为输入采样率的 1/M 倍的下采样输出，以列向量或矩阵的形式返回。

当您将 **速率选项** 设置为：

- 强制单采样 –– 该模块保持输入采样率，并通过将输出帧大小减少 M 倍来对信号进行下采样；
- 允许多重采样 –– 该模块对信号进行下采样，使输出采样率比输入采样率慢 M 倍，输出帧大小与输入帧大小相同。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | fixedPoint 

</div>
</div>



## 参数

<!-- ### **缩减采样因子源** — 缩减采样因子 的源 `对话框参数`（默认） |`输入端口`

*自 R2023a 起*

通过以下选项之一指定缩减采样因子：

- `Dialog parameter`–– 块 启用**“缩减采样因子”M**“参数 在 Block （块） 对话框中。
- `Input port`–– 该数据块启用 输入端口 **M**，通过该端口指定 下采样因子。 -->


<div class="details-box">
<details open>
<summary>采样因子（M） — 下采样因子<div>2 （默认） | 正整数</div></summary>
</details>
<div class="details-content">

用于降低输入采样率的整数因子 M。

</div>
</div>



<div class="details-box">
<details open>
<summary>采样偏移量（0 to M−1）— 采样偏移量<div>0 （默认）| 整数</div></summary>
</details>
<div class="details-content">

样本偏移参数会将输出样本延迟整数个样本周期，D，其中 0 ≤ D ≤ (M–1)，以便可以选择 M 种可能的输出相位中的任意一种。例如，当您以 4 为因子对序列 1, 2, 3, ... 进行下采样时，您可以选择四种相位之一。

| 输入序列    | 样品偏移量 D | 输出序列 （M = 4）       |
| :---------- | :------------- | :------------------------- |
| 1,2,3,... | 0              | 1,5,9,13,17,21,25,29,... |
| 1,2,3,... | 1              | 0,2,6,10,14,18,22,26,... |
| 1,2,3,... | 2              | 0,3,7,11,15,19,23,27,... |
| 1,2,3,... | 3              | 0,4,8,12,16,20,24,28,... |

表中最后三个输出序列中的初始零是**初始条件**参数设置为其默认值 0 所致。

</div>
</div>



<div class="details-box">
<details open>
<summary>输入信号处理方法 — 元素或列作为通道的处理方法<div>基于采样（默认） | 基于帧</div></summary>
</details>
<div class="details-content">

指定输入处理的方法：

- 元素作为通道（基于采样） –– 当您将输入处理参数设置为“元素作为通道（基于采样）”时，输入可以是 N 维数组。下采样模块会将输入的每个元素视为一个单独的通道，并随时间对输入的每个通道进行重采样。模块通过在传递每个样本到输出后丢弃 M–1 个样本来对输入数组进行下采样。下采样模块的输入和输出大小是相同的。

- 列作为通道（基于帧） –– 当您将输入处理参数设置为“列作为通道（基于帧）”时，模块会将每个输入列视为包含 Pi 个连续时间样本的独立通道。模块通过在输出每一行后丢弃输入矩阵的 M–1 行来独立地下采样每个通道。

</div>
</div>



<div class="details-box">
<details open>
<summary>速率选项 — 强制单采样或允许多重采样<div>强制单采样 （默认） | 允许多重采样</div></summary>
</details>
<div class="details-content">

指定模块如何调整输出速率以适应样本数量的减少。您可以选择以下选项之一。这些选项的行为取决于“输入处理”参数是设置为“元素作为通道（基于样本）”（基于样本的处理模式）还是“列作为通道（基于帧）”（基于帧的处理模式）。

**元素作为通道（基于采样）**

- 强制单采样  
  模块通过在输出处重复每个第 M 个输入样本 M 次，强制输出采样率与输入采样率匹配。
- 允许多重采样  
  输出的采样周期是输入采样周期的 M 倍。

**列作为通道（基于帧）**

- 强制单采样  
  模块使用比输入小的比例帧大小，在较慢的下采样速率下生成输出。
- 允许多重采样  
  模块通过在输出端口使用比输入端口长的比例帧周期，在较慢的下采样速率下生成输出。对于 M 倍下采样，输出帧周期是输入帧周期的 M 倍，但输入和输出帧大小相等。

</div>
</div>



<!-- ### **允许固定大小输入信号的任意帧长度** — 允许固定大小输入信号 的任意帧长度开启 （默认） |关闭



指定固定大小的输入信号（大小在 simulation）可以具有任意帧长度，其中帧长度 不必是 downsampling factor 的倍数。该块使用 this 参数设置仅适用于固定大小的输入信号，并忽略此项 参数（如果输入具有可变大小）。

当输入信号是可变大小信号时，该信号可以具有 任意帧长度，即帧长度不必为 抽取因子的倍数。

对于固定大小的输入信号，如果您：

- 选择 **Allow arbitrary frame length for 固定大小的 input signals** 参数，帧 length 不必是 下采样因子。如果输入不是 downsampling 因子，则输出通常为 variable-size 信号。因此，要支持任意输入 size，则块还必须支持可变大小的作， 您可以通过选择 **Allow arbitrary fixed size input signals 参数的帧长度**。
- 清除 **Allow arbitrary frame length for （允许任意帧长度） fixed-size input signals** 参数，则输入 帧长度必须是 downsampling 的倍数 因素。

#### 屬地

要启用此参数，请设置：

- **缩减采样 factor source** 设置为 . *（自 R2023a 起）*`Dialog parameter`
- **输入处理**到 .`Columns as channels (frame based)`
- **Rate 选项**设置为 .`Enforce single-rate processing` -->


<div class="details-box">
<details open>
<summary>初始条件 — 初始值<div>0 （默认） | 实数标量 | 数组</div></summary>
</details>
<div class="details-content">

用于非零延迟情况下的初始模块值。您可以指定一个标量或与输入大小相同的数组。

</div>
</div>

## 版本历史记录

- 在 2025a 推出

### 限制信息

1. 暂无降采样因子的输入端口，单支持对话框配置降采样因子；  
2. 暂不支持开启或关闭允许固定大小输入信号的任意帧长度功能；  
3. 输入和输出端口暂不支持 int64、uint64 和 boolean 的数据类型。
