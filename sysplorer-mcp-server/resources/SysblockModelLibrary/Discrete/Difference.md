# Difference
---
&nbsp;

计算一个时间步内的信号变化


- **库：** Sysblock / Discrete


<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/Difference/Difference.png')"  style="width: 100px; height: auto;">

## 描述

Difference 模块输出当前输入值减去上一输入值的差值。

## 示例
将 sineWave 模块振幅设置为 3，频率为 1 采样时间为 0.2 然后连接 difference 模块的输入我们可以观察到这个时间步的信号变化。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/Difference.mo">Difference.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/Difference/Difference01.png')" style="width: 600px; height: auto;">
<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discrete/Difference/Difference02.png')" style="width: 600px; height: auto;">


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 向量 | 矩阵 | N 维数组</div></summary>
</details>
<div class="details-content">

输入信号，指定为标量、向量、矩阵或 N 维数组。



**数据类型：** float | double | int8 | int16 | int32 | int64 | uint8 | uint16 | uint32 | Boolean | fixed point

</div>
</div>

### 输出


<div class="details-box">
<details open>
<summary>y — 当前输入减去上一个输入<div>标量 | 向量 | 矩阵 | N 维数组</div></summary>
</details>
<div class="details-content">

当前输入减去上一个输入，指定为标量、向量、矩阵或 N 维数组。

**数据类型：**  float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 |  Boolean | fixed point

</div>
</div>

## 参数



### 常设


<div class="details-box">
<details open>
<summary>上一输入的初始条件 — 初始条件<div>0.0 （默认） | 标量 | 向量 | 矩阵 | N 维数组</div></summary>
</details>
<div class="details-content">

为上一个输入设置初始条件。

</div>
</div>


<!-- 
#### 编程用法

| **参数：**`ICPrevInput`                   |
| ----------------------------------------- |
| **类型：**字符向量                        |
| **值：** 标量 \| 向量 \| 矩阵 \| N 维数组 |
| **默认值：**`'0.0'`                       | -->


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

### 信号属性


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
| **默认值**：`'[ ]'`    | 
-->


<!-- 暂无
### `输出最大值` — 范围检查的最大输出值 `[]` （默认） | 标量



Simulink 检查的输出范围的上限值。

Simulink 使用最大值执行下列操作：

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
| **默认值**：`'[ ]'`    |

-->

 

<div class="details-box">
<details open>
<summary>输出数据类型 — 输出数据类型<div>Inherit: internalRule（默认）| Inherit: backPropagation | double | float | int8 | uint8 | int16 | uint16 | int32 | uint32 | fixdt(1,16) | fixdt(1,16,0) | fixdt(1,16,2^0,0) |</div></summary>
</details>
<div class="details-content">

指定输出数据类型。可以将其设置为：

- 继承数据类型的规则，例如 **Inherit: internalRule**
- 内置数据类型的名称，例如 **float**
- 计算结果为数据类型的表达式，例如 **fixdt(1,16,0)**

单击**显示数据类型助手**按钮以显示**数据类型助手**，帮助您设置数据类型属性。


</div>
</div>

<!-- 
#### 编程用法

| **参数：**`OutDataTypeStr`                                   |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值：**`'Inherit: Inherit via internal rule' | 'Inherit: Inherit via back propagation' | 'double' | 'single' | 'int8' | 'uint8' | 'int16' | 'uint16' | 'int32' | 'uint32' | 'int64' | 'uint64' | 'boolean' | 'fixdt(1,16)' | 'fixdt(1,16,0)' | 'fixdt(1,16,2^0,0)' | '<data type expression>'` |
| **默认值：**`'Inherit: Inherit via internal rule'`           | -->



<!-- 暂无
### `锁定输出数据类型设置以防止被定点工具更改` — 防止定点工具覆盖输出数据类型 `off` （默认） | `on`



选择此参数可防止定点工具覆盖您在模块上指定的**输出**数据类型。有关详细信息，请参阅[Use Lock Output Data Type Setting](https://ww2.mathworks.cn/help/releases/R2022b/fixedpoint/ug/best-practices-for-using-the-fixed-point-tool-to-propose-data-types-for-your-simulink-model.html#br9an48) (Fixed-Point Designer)。

#### 编程用法

| **模块参数**：`LockScale` |
| ------------------------- |
| **类型：**字符向量        |
| **值：**`'off' | 'on'`    |
| **默认值：**`'off'`       |

-->
<!-- 暂无
### `整数舍入模式` — 定点运算的舍入模式 “`向下`” （默认） | “`向上`” | “`收敛`” | “`最邻近值`” | “`舍入`” | “`最简`” | “`零`”



指定定点运算的舍入模式。有关详细信息，请参阅[舍入](https://ww2.mathworks.cn/help/releases/R2022b/fixedpoint/ug/rounding.html) (Fixed-Point Designer)。

模块参数始终舍入到最邻近的可表示值。要控制模块参数的舍入方法，请在封装字段中使用 MATLAB® 舍入函数输入表达式。 -->

<!-- 
#### 编程用法

| **模块参数**：`RndMeth`                                      |
| ------------------------------------------------------------ |
| **类型：**字符向量                                           |
| **值：**`'Ceiling' | 'Convergent' | 'Floor' | 'Nearest' | 'Round' | 'Simplest' | 'Zero'` |
| **默认值：**`'Floor'`                                        | -->

<!--  暂无 

### `发生溢出时饱和处理为最大值或最小值` — 溢出操作的方法 `off` （默认） | `on`



当您选中此复选框时，溢出将饱和处理为数据类型可表示的最大值或最小值。否则，溢出将绕回。

如果选中此复选框，饱和将应用于模块中的每个内部操作，而不仅仅应用于输出或结果。一般情况下，代码生成进程可以检测到何时不可能发生溢出。在这种情况下，代码生成器不会生成饱和代码。

#### 编程用法

| **模块参数**：`DoSatur` |
| ----------------------- |
| **类型：**字符向量      |
| **值：**`'off' | 'on'`  |
| **默认值：**`'off'`     | 
-->


<!-- ## 模块特性 -->

<!-- 暂无
| **数据类型**   | `Booleana` \| `double` \| `fixed point` \| `half` \| `integer` \| `float` |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| **直接馈通**                                                 | `否`                                                         |
| **多维信号**                                                 | `否`                                                         |
| **可变大小信号**                                             | `是`                                                         |
| **过零检测**                                                 | `否`                                                         |
| [a](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/difference.html?s_tid=doc_ta#d125e30042) 建议不要将此模块用于布尔信号。 |                                                              | 
-->

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
1. 参数-常设-输入处理 — 指定基于采样或基于帧的处理
2. 参数-信号属性-输出最小值 — 范围检查的最小输出值
3. 参数-信号属性-输出最大值 — 范围检查的最大输出值
4. 参数-信号属性-锁定输出数据类型设置以防止被定点工具更改 — 防止定点工具覆盖输出数据类型
5. 参数-信号属性-整数舍入模式 — 定点运算的舍入模式
6. 参数-信号属性-发生溢出时饱和处理为最大值或最小值 — 溢出操作的方法

<!-- ## 另请参阅

[`diff`]()

### 主题

- [Sample- and Frame-Based Concepts]() (DSP System Toolbox)  -->