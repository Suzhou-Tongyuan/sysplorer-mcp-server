# Saturation
---
&nbsp;

将输入信号限制在饱和上限和下限值之间


- **库：** Sysblock / Discontinuities


<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/DiscontinuitiesPng/saturation/saturation.png')"  style="width: 100px; height: auto;">



## 描述

Saturation 模块产生输出信号，该信号是在饱和上限和下限值之间的输入信号值。上限和下限由参数**上限**和**下限**指定。

| 输入                 | 输出   |
| :------------------- | :----- |
| 下限 ≤ 输入值 ≤ 上限 | 输入值 |
| 输入值 < 下限        | 下限   |
| 输入值 > 上限        | 上限   |

## 示例

将 sineWave 模块的振幅设置为 5，因为 saturation 上限设置为 3，下限设置为 -3 所以输出被限制为 [-3,3]。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discontinuities/Saturation.mo">Saturation.mo</helpButton>。


<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/DiscontinuitiesPng/saturation/saturation01.png')" style="width: 600px; height: auto;">


<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/DiscontinuitiesPng/saturation/saturation02.png')" style="width: 600px; height: auto;">

## 端口

### 输入


<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

要应用饱和算法的输入信号。

**数据类型：** double | float | int8 | int16 | int32 | uint8 | uint16 | uint32 | fixed point

</div>
</div>

### 输出


<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

输出信号，它可以是输入信号值，也可以是饱和上限或下限值。

**数据类型：** double | float | int8 | int16 | int32 | int64 | uint8 | uint16 | uint32 | fixed point

</div>
</div>

## 参数



### 常设

<div class="details-box">
<details open>
<summary>上限 — 输入信号的饱和上限<div>0.5 （默认） | 标量 | 向量</div></summary>
</details>
<div class="details-content">

指定输入信号的上界。如果输入信号大于此边界，则输出信号将设置为此饱和值。**上限**参数会通过舍入到最邻近整数和饱和处理转换为输入数据类型。**上限**必须大于**输出最小值**参数且小于**输出最大值**参数。

</div>
</div>

<!-- 
#### 编程用法

| **模块参数**：`UpperLimit` |
| -------------------------- |
| **类型**：字符向量         |
| **值**：实数标量或向量     |
| **默认值**：`'0.5'`        | -->



<div class="details-box">
<details open>
<summary>下限 — 输入信号的饱和下限<div>-0.5 （默认） | 标量 | 向量</div></summary>
</details>
<div class="details-content">

指定输入信号的下界。如果输入信号小于此边界，则输出信号将设置为此饱和值。**下限**参数会通过舍入到最邻近整数和饱和处理转换为输入数据类型。**下限**必须大于**输出最小值**参数且小于**输出最大值**参数。

</div>
</div>

<!-- 
#### 编程用法

| **模块参数**：`LowerLimit` |
| -------------------------- |
| **类型**：字符向量         |
| **值**：实数标量或向量     |
| **默认值**：`'-0.5'`       | -->


<!-- 暂无
### `线性化时视为增益` — 指定增益值 `On` （默认） | 布尔



选中此复选框将使得这些命令将增益视为 1。Simulink® 软件中的线性化命令将此模块视为状态空间中的增益。清除该框将使得这些命令将增益视为 0。

#### 编程用法

| **模块参数**：`LinearizeAsGain` |
| ------------------------------- |
| **类型**：字符向量              |
| **值**：`'off'` | `'on'`        |
| **默认值**：`'on'`              | -->


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

### 信号属性

单击**显示数据类型助手**按钮以显示**数据类型助手**，帮助您设置数据类型属性。

<!-- 暂无
### `输出最小值` — 范围检查的最小输出值 `[]` （默认） | 标量



Simulink 检查的输出范围的下限值。

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
<summary>输出数据类型 — 指定输出数据类型<div>Inherit: sameAsInput（默认） | Inherit: backPropagation | double | float | int8 | int32 | uint32 | fixdt(1,16,0) | fixdt(1,16,2^0,0) | fixdt(1,16,1.0,0,0.0) </div></summary>
</details>
<div class="details-content">

为输出选择数据类型。该类型可以继承、直接指定或表示为数据类型对象。

</div>
</div>


<!-- #### 编程用法

| **模块参数**：`输出数据类型`                               |
| ------------------------------------------------------------ |
| **类型**：字符向量                                           |
| **值**：`'Inherit: Same as input'`、`'Inherit: Inherit via back propagation'`、`'single'`、`'int8'`、`'uint8'`、`int16`、`'uint16'`、`'int32'`、`'uint32'`、`'int64'`、`'uint64'`、`fixdt(1,16,0)`、“`fixdt(1,16,2^0,0)`”、`fixdt(1,16,2^0,0)`。`'<data type expression>'` |
| **默认值**：`'Inherit: Same as input'`                       | -->


<!-- 暂无

### `锁定输出数据类型设置以防止被定点工具更改` — 防止定点工具覆盖输出数据类型 `off` （默认） | `on`



选择此参数可防止定点工具覆盖您在模块上指定的**输出**数据类型。有关详细信息，请参阅[Use Lock Output Data Type Setting](https://ww2.mathworks.cn/help/releases/R2022b/fixedpoint/ug/best-practices-for-using-the-fixed-point-tool-to-propose-data-types-for-your-simulink-model.html#br9an48) (Fixed-Point Designer)。

#### 编程用法

| **模块参数**：`LockScale` |
| ------------------------- |
| **类型：**字符向量        |
| **值：**`'off' | 'on'`    |
| **默认值：**`'off'`       | -->


<!-- 暂无
### `整数舍入模式` — 指定定点运算的舍入模式 “`向下`” （默认） | “`向上`” | “`收敛`” | “`最邻近值`” | “`舍入`” | “`最简`” | “`零`”



选择下列舍入模式之一。

- “`向上`”

  将正值和负值朝正无穷方向舍入。等同于 MATLAB® `ceil` 函数。

- “`收敛`”

  将数值舍入到最邻近的可表示值。如果出现结值，则舍入到最邻近的偶数整数。等同于 Fixed-Point Designer™ `convergent` 函数。

- “`向下`”

  将正值和负值朝负无穷方向舍入。等同于 MATLAB `floor` 函数。

- “`最邻近值`”

  将数值舍入到最邻近的可表示值。如果出现结值，则朝正无穷方向舍入。等同于 Fixed-Point Designer `nearest` 函数。

- “`舍入`”

  将数值舍入到最邻近的可表示值。如果出现结值，则将正数朝正无穷方向舍入，将负数朝负无穷方向舍入。等同于 Fixed-Point Designer `round` 函数。

- “`最简`”

  自动选择是向负无穷大方向舍入还是向零舍入，以生成尽可能有效的舍入代码。

- “`零`”

  将数值向零舍入。等同于 MATLAB `fix` 函数。



#### 编程用法

| **模块参数**：`RndMeth`                                      |
| ------------------------------------------------------------ |
| **类型**：字符向量                                           |
| **值**：`'Ceiling'` | `'Convergent'` | `'Floor'` | `'Nearest'` | `'Round'` | `'Simplest'` | `'Zero'` |
| **默认值**：`'Floor'`                                        | 

#### 另请参阅

有关详细信息，请参阅[舍入](https://ww2.mathworks.cn/help/releases/R2022b/fixedpoint/ug/rounding.html) (Fixed-Point Designer)。-->

<!-- ## 模块特性 -->

<!-- 部分特性暂无
| **数据类型**     | `double` \| `fixed point` \| `integer` \| `float` |
| ---------------- | ----------------------------------------------- |
| **直接馈通**     | `是`                                            |
| **多维信号**     | `否`                                            |
| **可变大小信号** | `否`                                            |
| **过零检测**     | `是`                                            | -->

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
1. 参数-常设-线性化时视为增益 — 指定增益值
2. 参数-常设-启用过零检测 — 启用过零检测
3. 参数-常设-采样时间 — -1 以外的采样时间值
4. 参数-信号属性-输出最小值 — 范围检查的最小输出值
5. 参数-信号属性-输出最大值 — 范围检查的最大输出值
6. 参数-信号属性-锁定输出数据类型设置以防止被定点工具更改
7. 参数-信号属性-整数舍入模式 — 指定定点运算的舍入模式
## 另请参阅

[SaturationDynamic](SaturationDynamic.html) | [Backlash](Backlash.html)