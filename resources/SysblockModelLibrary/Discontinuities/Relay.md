# Relay
---
&nbsp;

在两个常量输出之间进行切换

- **库：** Sysblock / Discontinuities


<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/DiscontinuitiesPng/relay/relay.png')"  style="width: 100px; height: auto;">


## 描述

Relay 模块的输出在两个指定值之间切换。打开中继时，它会一直保持打开，直到输入低于**关闭点**参数的值为止。关闭中继时，它会一直保持关闭，直到输入高于**开启点**参数的值为止。此模块接受一个输入并生成一个输出。


::: warning 注意
如果初始输入介于**开启点**与**关闭点**值之间，则初始输出是中继关闭时的值。
:::

## 示例

添加一个 Sin Wave 模块，设置其振幅为 2，频率为 1Hz，采样时间为 0.01 秒，用于生成一个正弦波输入信号。
双击 Relay 模块，设置开启点为 1，关闭点为 -1，Output when on开启时输出为 5，关闭时输出为 0。
当正弦波信号大于 1 时，Relay 模块输出 5；当正弦波信号小于 -1 时，Relay 模块输出 0；而当正弦波信号在 -1 到 1 之间时，Relay 模块保持之前的输出状态。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discontinuities/Relay.mo">Relay.mo</helpButton>。


<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/DiscontinuitiesPng/relay/relay01.png')" style="width: 600px; height: auto;">


<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/DiscontinuitiesPng/relay/relay02.png')" style="width: 600px; height: auto;">



## 端口

### 输入


<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量</div></summary>
</details>
<div class="details-content">

输入信号，用于打开或关闭中继。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | Boolean | fixed point

</div>
</div>

### 输出


<div class="details-box">
<details open>
<summary>y — 输出信号<div></div></summary>
</details>
<div class="details-content">

输出信号在由参数**打开时的输出**和**关闭时的输出**确定的两个值之间切换。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | Boolean | fixed point

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>开启点 — 用于打开中继的输入值<div>1（默认） </div></summary>
</details>
<div class="details-content">

当输入超过此阈值时，中继打开。**开启点**值必须大于或等于**关闭点**。指定的**开启点**值大于**关闭点**可构建磁滞模型，指定两个值相等则可构建以该值为阈值的开关模型。

**开启点**参数会通过舍入到最邻近整数和饱和处理方法自动转换为输入数据类型。

</div>
</div>

<!-- #### 编程用法

| **模块参数**：`开启点` |
| ----------------------------- |
| **类型**：字符向量            |
| **值**：标量                  |
| **默认值**：`'1'`           | -->


<div class="details-box">
<details open>
<summary>关闭点 — 用于关闭中继的输入值<div>1 （默认）</div></summary>
</details>
<div class="details-content">

当输入超过此阈值时，中继关闭。**关闭点**的值必须小于或等于**开启点**。**关闭点**参数会通过舍入到最邻近整数和饱和处理自动转换为输入数据类型。

</div>
</div>

<!-- #### 编程用法

| **模块参数**：`关闭点` |
| ------------------------------ |
| **类型**：字符向量             |
| **值**：标量                   |
| **默认值**：`'1'`            | -->


<div class="details-box">
<details open>
<summary>打开时的输出 — 当中继打开时的输出值<div>1 （默认）</div></summary>
</details>
<div class="details-content">

当中继打开时的输出值。

</div>
</div>

<!-- #### 编程用法

| **模块参数**：`打开时的输出` |
| ----------------------------- |
| **类型**：字符向量            |
| **值**：标量                  |
| **默认值**：`'1'`             | -->


<div class="details-box">
<details open>
<summary>关闭时的输出 — 当中继关闭时的输出值<div>0 （默认）</div></summary>
</details>
<div class="details-content">

当中继关闭时的输出值。

</div>
</div>

<!-- #### 编程用法

| **模块参数**：`关闭时的输出` |
| ------------------------------ |
| **类型**：字符向量             |
| **值**：标量                   |
| **默认值**：`'0'`              | -->


<!-- 暂无
### `输入处理` — 指定基于采样或基于帧的处理 “`元素作为通道(基于采样)`” （默认） | “`列作为通道(基于帧)`”



指定模块是执行基于采样还是基于帧的处理：

- “`列作为通道(基于帧)`” - 将输入信号的每一列视为一个单独的通道（基于帧的处理）。

  

  **注意**

  基于帧的处理需要具有 DSP System Toolbox™ 许可证。

  有关详细信息，请参阅[Sample- and Frame-Based Concepts](https://ww2.mathworks.cn/help/releases/R2022b/dsp/ug/sample-and-frame-based-concepts.html) (DSP System Toolbox)。

- “`元素作为通道(基于采样)`” - 将输入信号的每个元素视为一个单独的通道（基于采样的处理）。

可以使用**输入处理**指定模块是执行基于采样的处理还是基于帧的处理。有关这两种处理模式的详细信息，请参阅[Sample- and Frame-Based Concepts](https://ww2.mathworks.cn/help/releases/R2022b/dsp/ug/sample-and-frame-based-concepts.html) (DSP System Toolbox)。

#### 编程用法

| **模块参数**：`InputProcessing`                              |
| ------------------------------------------------------------ |
| **类型**：字符向量                                           |
| **值**：`'Columns as channels (frame based)'` | `'Elements as channels (sample based)'` |
| **默认值**：`'Elements as channels (sample based)'`          | -->


<!-- 暂无
### `启用过零检测` — 启用过零检测 `on` （默认） | `off`



选择此项以启用过零检测。有关详细信息，请参阅[过零检测](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/zero-crossing-detection.html)。

#### 编程用法

| **模块参数**：`ZeroCross`    |
| ---------------------------- |
| **类型**：字符向量 \| 字符串 |
| **值**：`'off'` | `'on'`     |
| **默认值**：`'on'`           | -->


<!-- 暂无
### `采样时间` — `-1` 以外的采样时间值 `-1` （默认） | 标量 | 向量



将采样时间指定为 `-1` 以外的值。有关详细信息，请参阅[指定采样时间](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/how-to-specify-the-sample-time.html)。

#### 依存关系

此参数不可见，除非将其显式设置为 `-1` 以外的值。要了解详细信息，请参阅[不建议设置采样时间的模块](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/sampletimehiding.html)。

#### 编程用法

| **模块参数：**`SampleTime`     |
| ------------------------------ |
| **类型：**字符串标量或字符向量 |
| **默认值：**`"-1"`             | -->


<!-- 暂无

### `输出最小值` — 范围检查的最小输出值 `[]` （默认） | 标量



Simulink® 检查的输出范围的下限值。

Simulink 使用最小值执行下列操作：

- 某些模块的参数范围检查（请参阅[指定模块参数的最小值和最大值](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/checking-parameter-values.html)）。
- 仿真范围检查（请参阅[指定信号范围](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/signal-ranges.html)和[启用仿真范围检查](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/signal-ranges.html#brdikvq)）。
- 定点数据类型的自动定标。
- 从模型生成的代码的优化。此优化可删除算法代码，并影响某些仿真模式（如 SIL 或外部模式）的结果。有关详细信息，请参阅[Optimize using the specified minimum and maximum values](https://ww2.mathworks.cn/help/releases/R2022b/ecoder/ref/optimizeusingthespecifiedminimumandmaximumvalues.html) (Embedded Coder)。





**注意**

**输出最小值**不会饱和或剪切实际输出信号。请改用 [Saturation](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/saturation.html) 模块。



#### 编程用法

| **模块参数**：`OutMin` |
| ---------------------- |
| **类型**：字符向量     |
| **值**：`'[ ]'`\| 标量 |
| **默认值**：`'[ ]'`    | -->

<!-- 暂无

### `输出最大值` — 范围检查的最大输出值 `[]` （默认） | 标量



Sysblock 检查的输出范围的上限值。

Sysblock 使用最大值执行下列操作：

- 某些模块的参数范围检查（请参阅[指定模块参数的最小值和最大值](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/checking-parameter-values.html)）。
- 仿真范围检查（请参阅[指定信号范围](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/signal-ranges.html)和[启用仿真范围检查](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/signal-ranges.html#brdikvq)）。
- 定点数据类型的自动定标。
- 从模型生成的代码的优化。此优化可删除算法代码，并影响某些仿真模式（如 SIL 或外部模式）的结果。有关详细信息，请参阅[Optimize using the specified minimum and maximum values](https://ww2.mathworks.cn/help/releases/R2022b/ecoder/ref/optimizeusingthespecifiedminimumandmaximumvalues.html) (Embedded Coder)。





**注意**

**输出最大值**不会饱和或剪切实际输出信号。请改用 [Saturation](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/saturation.html) 模块。



#### 编程用法

| **模块参数**：`OutMax` |
| ---------------------- |
| **类型**：字符向量     |
| **值**：`'[ ]'`\| 标量 |
| **默认值**：`'[ ]'`    | -->


<div class="details-box">
<details open>
<summary>输出数据类型 — 输出信号的数据类型<div>Inherit: allPortsSameDataType（默认）| Inherit: backPropagation | double | float | int8 | int32 | uint32 | boolean | fixdt(1,16,0) | fixdt(1,16,2^0,0) | fixdt(1,16,1.0,0,0.0) | </div></summary>
</details>
<div class="details-content">

指定输出数据类型。可以将其设置为：

- 继承数据类型的规则，例如 **Inherit: allPortsSameDataType**
- 内置数据类型的名称，例如 **float**
- 计算结果为数据类型的表达式，例如 **fixdt(1,16,0)**

</div>
</div>

<!-- 
#### 编程用法

| **模块参数**：`显示数据类型助手`                               |
| ------------------------------------------------------------ |
| **类型**：字符向量                                           |
| **值**：`'Inherit: Same as input'`、`'Inherit: Inherit via back propagation'`、`'single'`、`'int8'`、`'uint8'`、`int16`、`'uint16'`、`'int32'`、`'uint32'`、`'int64'`、`'uint64'`、`fixdt(1,16,0)`、“`fixdt(1,16,2^0,0)`”、`fixdt(1,16,2^0,0)`。`'<data type expression>'` |
|                                                              |
| **默认值**：`'Inherit: Same as input'`                       | -->


<!-- 暂无
### `锁定数据类型设置以防止被定点工具更改` — 防止定点工具覆盖数据类型 `off` （默认） | `on`



选择此参数可防止定点工具覆盖您对此模块指定的数据类型。有关详细信息，请参阅[Lock the Output Data Type Setting](https://ww2.mathworks.cn/help/releases/R2022b/fixedpoint/ug/configuring-blocks-with-fixed-point-output.html#f25236) (Fixed-Point Designer)。

#### 编程用法

| **模块参数**：`LockScale` |
| ------------------------- |
| **类型：**字符向量        |
| **值：**`'off' | 'on'`    |
| **默认值：**`'off'`       |
 -->

<!-- 部分特性暂无
## 模块特性

| **数据类型**     | `Boolean` \| `double` \| `fixed point` \| `integer` \| `single` |
| ---------------- | ----------------------------------------------------------- |
| **直接馈通**     | `是`                                                        |
| **多维信号**     | `否`                                                        |
| **可变大小信号** | `否`                                                        |
| **过零检测**     | `是`                                                        | -->

<!-- ## 扩展功能 -->



<!-- 
### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 Verilog 代码和 VHDL 代码。



### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。 -->

## 版本历史记录

- 在 2024b 之前推出

### 限制信息
不支持部分
1. 参数-输入处理 — 指定基于采样或基于帧的处理
2. 参数-启用过零检测 — 启用过零检测
3. 参数-采样时间 — -1 以外的采样时间值
4. 参数-输出最小值 — 范围检查的最小输出值
5. 参数-输出最大值 — 范围检查的最大输出值
6. 参数-锁定数据类型设置以防止被定点工具更改 — 防止定点工具覆盖数据类型

## 另请参阅

[Saturation](Saturation.html) | [Backlash](Backlash.html)

