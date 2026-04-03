# SaturationDynamic
---
&nbsp;

将输入信号限制在动态饱和上限和下限值之间

- **库：** Sysblock / Discontinuities

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/DiscontinuitiesPng/saturationDynamic/saturationDynamic.png')"  style="width: 100px; height: auto;">


## 描述

SaturationDynamic 模块产生输出信号，该信号是以来自输入端口 `up` 和 `lo` 的饱和值为界的输入信号的值。

| 输入                 | 输出   |
| :------------------- | :----- |
| `lo` ≤ 输入值 ≤ `up` | 输入值 |
| 输入值 < `lo`        | 下限   |
| 输入值 > `up`        | 上限   |

## 示例

添加一个 SineWave 模块，设置其振幅为 5，用于产生一个正弦波信号作为输入。添加一个 Constant 模块和一个 SineWave 模块作为上限和下限值之间。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discontinuities/SaturationDynamic.mo">SaturationDynamic.mo</helpButton>。


<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/DiscontinuitiesPng/saturationDynamic/saturationDynamic01.png')" style="width: 600px; height: auto;">


<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/DiscontinuitiesPng/saturationDynamic/saturationDynamic02.png')" style="width: 600px; height: auto;">



## 端口


### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

要应用饱和算法的输入信号。

**数据类型:** double | float | int8 | int16 | int32 | uint8 | uint16 | uint32 | fixed point

</div>
</div>


<div class="details-box">
<details open>
<summary>up — 提供饱和上限的信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

提供饱和上限的动态值。当输入大于 **up** 时，输出值以 **up** 为界。

**数据类型:** double | float | int8 | int16 | int32 | uint8 | uint16 | uint32 | fixed point

</div>
</div>

<div class="details-box">
<details open>
<summary>lo — 提供饱和下限的信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

提供饱和下限的动态值。当输入小于 **lo** 时，输出值以 **lo** 为界。

**数据类型:** double | float | int8 | int16 | int32 | uint8 | uint16 | uint32 | fixed point

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

输出信号，它可以是输入信号值，也可以是饱和上限或下限值。

**数据类型:** double | float | int8 | int16 | int32 | uint8 | uint16 | uint32 | fixed point

</div>
</div>

## 参数

<!-- 暂无


**输出最小值** — 范围检查的最小输出值 `[]` (默认) | 标量

软件检查的输出范围的下限值。

软件使用最小值执行下列操作：

- 某些模块的参数范围检查。
- 仿真范围检查。
- 定点数据类型的自动定标。
- 从模型生成的代码的优化。此优化可删除算法代码，并影响某些仿真模式（如 SIL 或外部模式）的结果。



#### 提示

**输出最小值**不会对实际输出信号进行饱和处理或截断。

#### 编程用法



| **参数:** | `OutMin`                          |
| --------- | --------------------------------- |
| **值:**   | `'[]'` (默认) \| scalar in quotes |

 -->



<!-- 暂无

**输出最大值** — 范围检查的最大输出值 `[]` (默认) | 标量

软件检查的输出范围的上限值。

软件使用最大值执行下列操作：

- 某些模块的参数范围检查。
- 仿真范围检查。
- 定点数据类型的自动定标。
- 从模型生成的代码的优化。此优化可删除算法代码，并影响某些仿真模式（如 SIL 或外部模式）的结果。



#### 提示

**输出最大值**不会对实际输出信号进行饱和处理或截断。

#### 编程用法

| **参数:** | `OutMax`                          |
| --------- | --------------------------------- |
| **值:**   | `'[]'` (默认) \| scalar in quotes | -->


<div class="details-box">
<details open>
<summary>输出数据类型 — 指定输出数据类型<div>Inherit: sameAsSecondInput（默认） | double | float | int8 | int32 | uint32 | fixdt(1,16,0) | fixdt(1,16,2^0,0) | fixdt(1,16,1.0,0,0.0)  </div></summary>
</details>
<div class="details-content">



为输出选择数据类型。该类型可以继承、直接指定或表示为数据类型对象。

</div>
</div>


<!-- 
#### 编程用法

| **模块参数**：`OutDataTypeStr`                               |
| ------------------------------------------------------------ |
| **类型**：字符向量                                           |
| **值**：`'Inherit: sameAsSecondInput'` | `'Inherit: Inherit via back propagation'` | `'double'` | `'single'` | `'int8'` | `'uint8'` | `int16` | `'uint16'` | `'int32'` | `'uint32'` | `'int64'` | `'uint64'` | `fixdt(1,16)` | `fixdt(1,16,0)` | `fixdt(1,16,2^0,0)` | `'<data type expression>'` |
| **默认值**：`'Inherit: Same as input'`                       | -->




<!-- 暂无


**锁定输出数据类型设置以防止被定点工具更改** — 用于防止定点工具覆盖输出数据类型的选项 `off` (默认) | `on`

选择此参数可防止定点工具覆盖您在模块上指定的**输出**数据类型。

#### 编程用法

| **参数:** | `LockScale`             |
| --------- | ----------------------- |
| **值:**   | `'off'` (默认) | `'on'` |

 -->



<!-- 暂无

**整数舍入模式** — 指定定点运算的舍入模式 **向下** (默认) | **向上** | **收敛** | **最邻近值** | **舍入** | **最简** | **零**

选择下列舍入模式之一。

- **向上**

  将正值和负值朝正无穷方向舍入。等同于 MATLAB® `ceil` 函数。

- **收敛**

  将数值舍入到最邻近的可表示值。如果出现结值，则舍入到最邻近的偶数整数。等同于 Fixed-Point Designer™ `convergent` 函数。

- **向下**

  将正值和负值朝负无穷方向舍入。等同于 MATLAB `floor` 函数。

- **最邻近值**

  将数值舍入到最邻近的可表示值。如果出现结值，则朝正无穷方向舍入。等同于 Fixed-Point Designer `nearest` 函数。

- **舍入**

  将数值舍入到最邻近的可表示值。如果出现结值，则将正数朝正无穷方向舍入，将负数朝负无穷方向舍入。等同于 Fixed-Point Designer `round` 函数。

- **最简**

  自动选择是向负无穷大方向舍入还是向零舍入，以生成尽可能有效的舍入代码。

- **零**

  将数值向零舍入。等同于 MATLAB `fix` 函数。



#### 编程用法

| **模块参数**：`RndMeth`                                      |
| ------------------------------------------------------------ |
| **类型**：字符向量                                           |
| **值**：`'Ceiling'` | `'Convergent'` | `'Floor'` | `'Nearest'` | `'Round'` | `'Simplest'` | `'Zero'` |
| **默认值**：`'Floor'`                                        |

#### 另请参阅
有关详细信息，请参阅[舍入]() (Fixed-Point Designer)。 -->


<!-- 暂无
**对整数溢出进行饱和处理** — 溢出操作的方法 `off` (默认) | `on`

指定对溢出是进行饱和处理还是绕回处理。

- `on` - 将溢出饱和处理为数据类型能够表示的最小值或最大值。
- `off` - 溢出将绕回到数据类型可以表示的合适值。

例如，有符号 8 位整数 `int8` 可以表示的最大值是 127。任何大于此最大值的模块运算结果都会导致 8 位整数溢出。

- 选择此参数后，模块输出将在达到 127 时饱和。类似地，模块输出将在达到最小输出值 -128 时饱和。
- 清除此参数后，软件会将导致溢出的值解释为 `int8`，这可能产生意外结果。例如，以 `int8` 表示的模块结果 130（二进制 1000 0010）为 -126。

#### 提示

- 如果您的模型存在可能的溢出，而您希望在生成的代码中进行显式饱和保护，请考虑选中此参数。
- 如果您希望优化生成的代码的效率，请考虑清除此参数。清除此参数还可以帮助您避免过度地指定信号超出范围时模块的处理方式。
- 如果选中此参数，饱和将应用于模块中的每个内部操作，而不仅仅应用于输出或结果。
- 一般情况下，代码生成进程可以检测到何时不可能发生溢出。在这种情况下，代码生成器不会生成饱和代码。

#### 编程用法

| **模块参数**：`DoSatur` |
| ----------------------- |
| **类型：**字符向量      |
| **值：**`'off' | 'on'`  |
| **默认值：**`'off'`     | -->

<!-- ### 模块特性 -->

<!--部分功能暂无 
| **数据类型**                   | Boolean \| double \| fixed point \| integer \| float |
| ------------------------------ | ----------------------------------------------------- |
| **直接馈通**                   | 否                                                    |
| **多维信号**                   | 否                                                    |
| **可变大小信号**               | 否                                                    |
| **过零检测**                   | 否                                                    |
| 建议不要将此模块用于布尔信号。 |                                                       | -->

<!-- ## 详细信息 -->
<!-- 
### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 VHDL、Verilog 和 SystemVerilog 代码。



HDL Coder™ 提供影响 HDL 实现和综合逻辑的额外配置选项。

**HDL 架构**

此模块具有一个默认 HDL 架构。

**HDL 模块属性**

| **ConstrainedOutputPipeline** | 通过移动设计中现有延迟的方式来放置在输出端的寄存器的数量。分布式流水线不会重新分发这些寄存器。默认值为 `0`。有关详细信息，请参阅[ConstrainedOutputPipeline](https://ww2.mathworks.cn/help/hdlcoder/ug/block-implementation-parameters.html#btp8gmp) (HDL Coder)。 |
| ----------------------------- | ------------------------------------------------------------ |
| **InputPipeline**             | 要在生成的代码中插入的输入流水线阶段数。分布式流水线和受限输出流水线可以移动这些寄存器。默认值为 `0`。有关详细信息，请参阅[InputPipeline](https://ww2.mathworks.cn/help/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-25) (HDL Coder)。 |
| **OutputPipeline**            | 要在生成的代码中插入的输出流水线阶段数。分布式流水线和受限输出流水线可以移动这些寄存器。默认值为 `0`。有关详细信息，请参阅[OutputPipeline](https://ww2.mathworks.cn/help/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-26) (HDL Coder)。 |



### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。 -->
<!-- ## 扩展功能 -->
<!-- 
### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 VHDL、Verilog 和 SystemVerilog 代码。



HDL Coder™ 提供影响 HDL 实现和综合逻辑的额外配置选项。

**HDL 架构**

此模块具有一个默认 HDL 架构。

**HDL 模块属性**

| **ConstrainedOutputPipeline** | 通过移动设计中现有延迟的方式来放置在输出端的寄存器的数量。分布式流水线不会重新分发这些寄存器。默认值为 `0`。有关详细信息，请参阅[ConstrainedOutputPipeline](https://ww2.mathworks.cn/help/hdlcoder/ug/block-implementation-parameters.html#btp8gmp) (HDL Coder)。 |
| ----------------------------- | ------------------------------------------------------------ |
| **InputPipeline**             | 要在生成的代码中插入的输入流水线阶段数。分布式流水线和受限输出流水线可以移动这些寄存器。默认值为 `0`。有关详细信息，请参阅[InputPipeline](https://ww2.mathworks.cn/help/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-25) (HDL Coder)。 |
| **OutputPipeline**            | 要在生成的代码中插入的输出流水线阶段数。分布式流水线和受限输出流水线可以移动这些寄存器。默认值为 `0`。有关详细信息，请参阅[OutputPipeline](https://ww2.mathworks.cn/help/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-26) (HDL Coder)。 |



### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。 -->

## 版本历史记录

- 在 2024b 之前推出

### 限制信息

不支持部分
1. 参数-输出最小值 — 范围检查的最小输出值
2. 参数-输出最大值 — 范围检查的最大输出值
3. 参数-锁定输出数据类型设置以防止被定点工具更改 — 防止定点工具覆盖输出数据类型
4. 参数-整数舍入模式 — 指定定点运算的舍入模式
5. 参数-对整数溢出进行饱和处理 — 选择发生整数溢出时的行为

## 另请参阅
[Saturation](Saturation.html)