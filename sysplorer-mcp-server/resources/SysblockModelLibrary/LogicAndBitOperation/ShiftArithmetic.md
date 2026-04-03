# ShiftArithmetic
---
&nbsp;

对信号进行算数移位

**库：** Sysblock 模块库 / LogicAndBitOperation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/ShiftArithmetic/ShiftArithmetic.png')" style="width: 150px; height: auto; transform: scale(1);">

## 描述

ShiftArithmetic 模块可以对信号做算术移位。

例如，将 sfix ( 8 ) 数据类型的输入信号算术向右和向左移动两位，将得到以下小数值。

| 移位运算                 | 二进制值  | 十进制值 |
| :----------------------- | :-------- | :------- |
| 无移位（原始数字）       | 11001.011 | -6.625   |
| 算术向左移动两位 | 1100101.1 | -26.5    |
| 算术向右移动两位 | 110.01011 | -1.65625 |

## 示例

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/ShiftArithmetic.mo">ShiftArithmetic.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/ShiftArithmetic/ShiftArithmetic_ex.png')" style="width: 600px;transform: scale(0.8);border:solid 1px black;">


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 要对其执行运算的数<div>标量 | 向量 | 数组</div></summary>
</details>
<div class="details-content">

要对其执行运算的数，指定为标量、向量或数组。

**数据类型：** double | float | int8 | int16 | int32 | int64 | uint8 | uint16 | uint32 | uint64 | fixed point

</div>
</div>


<div class="details-box">
<details open>
<summary>s — 要移位的位数<div>标量</div></summary>
</details>
<div class="details-content">

要移位的位数，指定为标量。

**数据类型：** double | float | int8 | int16 | int32 | int64 | uint8 | uint16 | uint32 | uint64 | fixed point

</div>
</div>



## 参数

### 数据和算法

<div class="details-box">
<details open>
<summary>二进制位移位数：源 — 要移位的位的源<div>对话框（默认） | 输入端口</div></summary>
</details>
<div class="details-content">

指定是直接在对话框中输入要移动的位数，还是从输入端口继承值。

</div>
</div>



<!-- 暂无
#### 编程用法

| **模块参数**：BitShiftNumberSource |
| ------------------------------------ |
| **类型**：字符向量、字符串           |
| **值**：'Dialog' | 'Input port'  |
| **默认值**：'Dialog'               | -->


<div class="details-box">
<details open>
<summary>二进制位移位数：方向 — 移位的方向<div>双向（默认）| 左 | 右</div></summary>
</details>
<div class="details-content">

指定移位的方向：向左、向右或双向。

</div>
</div>



<!-- 暂无
#### 编程用法

| **模块参数**：BitShiftDirection               |
| ----------------------------------------------- |
| **类型**：字符向量、字符串                      |
| **值**：'Left' | 'Right' | 'Bidrectional' |
| **默认值**：'Bidrectional'                    | -->


<div class="details-box">
<details open>
<summary>二进制位移位数：数值 — 二进制位移位数<div>8（默认）| 标量 | 向量 | 数组</div></summary>
</details>
<div class="details-content">

指定标量、向量或移位值数组。

| 如果方向为...      | 则...                                    |
| :----------------- | :--------------------------------------- |
| “左”或“右” | 使用正整数指定移位。                     |
| “双向”           | 使用正整数表示右移，使用负整数表示左移。 |

**依赖关系**：要启用此参数，请将**二进制位移位数:源**设置为对话框。

</div>
</div>



<!-- 暂无
#### 编程用法

| **模块参数**：BitShiftNumber |
| ------------------------------ |
| **类型**：字符向量、字符串     |
| **值**：scalar               |
| **默认值**：'9'              | -->

<!-- 暂无
### 二进制小数点移位数:数量 — 二进制小数点移位的位数 0 （默认） | scalar

指定将输入信号中的二进制小数点移动的整数位数。正值表示右移，负值表示左移。

**可调：** No


#### 编程用法

| **模块参数**：BinPtShiftNumber    |
| ----------------------------------- |
| **类型**：字符向量、字符串          |
| **值**：'Dialog' | 'Input port' |
| **默认值**：'Dialog'              | -->


<!-- 暂无
### 超范围移位值的诊断 — 诊断操作 “无” （默认） | “警告” | “错误”



指定当模块包含超出范围的移位值时，是否在仿真过程中生成警告或错误消息。选项包括：

- None - 不执行任何 Simulink® 操作。
- Warning - Simulink 显示警告并继续进行仿真。
- Error - Simulink 终止仿真并显示错误。

有关详细信息，请参阅[超范围移位值的仿真和加速模式结果](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/shiftarithmetic.html#bstdjcz_head)。

#### 编程用法

| **模块参数**：DiagnosticForOORShift      |
| ------------------------------------------ |
| **类型**：字符向量、字符串                 |
| **值**：'None' | 'Warning' | 'Error' |
| **默认值**：'None'                       | -->


<!-- 暂无
### 检查生成代码中是否有超出范围的 '二进制位移位数' — 检查生成代码中是否有超出范围的二进制位移位数 off （默认） | on



如果选中此复选框，将在生成的代码中包含条件语句，以防移位值超出范围。当**二进制位移位数:源**为“输入端口”时，此复选框才可用。

有关详细信息，请参阅[超范围移位值的代码生成](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/shiftarithmetic.html#bstdjf8_head)。

#### 编程用法

| **模块参数**：CheckOORBitShift |
| -------------------------------- |
| **类型**：字符向量、字符串       |
| **值**：'on' | 'off'         |
| **默认值**：'off'              | -->

<!-- 不确定
## 模块特性

| **数据类型**     | double | fixed point | half | integer | single |
| ---------------- | -------------------------------------------------------- |
| **直接馈通**     | 是                                                     |
| **多维信号**     | 否                                                     |
| **可变大小信号** | 否                                                     |
| **过零检测**     | 否                                                     |

### 模块图标变量

Shift Arithmetic 模块图标使用以下变量显示模块行为：

- Q - 存储的整数值
- V - 真实值
- E - 指数
- Qy - 存储的输出整数值
- Qu - 存储的输入整数值
- Vy - 输出值
- Vu - 输入值
- Ey - 输出指数
- Eu - 输入指数

### 右移位的模块输出

下面的[模型](matlab:open_system(docpath(fullfile(docroot,'toolbox','simulink','examples','blocks','ex_shift_arithmetic_block_right_bit_shifts'))))将使用对话框的右移位行为与使用模块输入端口的右移位行为进行了对比。

![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/shift_arithmetic_block_right_bit_shifts_model.png)

Constant 模块的主要模块参数设置如下：

| 模块                      | 参数                                       | 设置  |
| :------------------------ | :----------------------------------------- | :---- |
| Constant 和 Constant1 | **常量值**                                 | 124 |
| **输出数据类型**          | “int8”                                   |       |
| Dynamic bit shift       | **常量值**                                 | 2   |
| **输出数据类型**          | “Inherit: Inherit from 'Constant value'” |       |

Shift Arithmetic 模块的主要模块参数设置如下：

| 模块                    | 参数                  | 设置         |
| :---------------------- | :-------------------- | :----------- |
| Bit shift from dialog | **二进制位移位数:源** | “对话框”   |
| **二进制位移位数:方向** | “右侧”              |              |
| **二进制位移位数:数量** | “2”                 |              |
| Bit shift from input  | **二进制位移位数:源** | “输入端口” |
| **二进制位移位数:方向** | “右侧”              |              |

上面的 Shift Arithmetic 模块接受的输入为 124，对应于二进制格式的 01111100。右移两位得到二进制格式的 00011111。因此，模块输出 31。

下面的 Shift Arithmetic 模块执行的操作与上面的模块相同。但是，下面的模块通过输入端口而不是对话框来接收移位值。通过将此值作为输入信号来提供，您可以在仿真期间更改要移动的位数。

### 二进制小数点移位的模块输出

下面的[模型](matlab:open_system(docpath(fullfile(docroot,'toolbox','simulink','examples','blocks','ex_shift_arithmetic_block_binary_point_shifts'))))显示了二进制小数点移位的效果。

![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/shift_arithmetic_block_binary_point_shifts_model.png)

Constant 模块的主要模块参数设置如下：

| 模块                      | 参数       | 设置  |
| :------------------------ | :--------- | :---- |
| Constant 和 Constant1 | **常量值** | 124 |
| **输出数据类型**          | “int8”   |       |

Shift Arithmetic 模块的主要模块参数设置如下：

| 模块                                       | 参数                  | 设置       |
| :----------------------------------------- | :-------------------- | :--------- |
| Shift binary point 3 places to the right | **二进制位移位数:源** | “对话框” |
| **二进制位移位数:方向**                    | “双向”              |            |
| **二进制位移位数:数量**                    | “0”                 |            |
| **二进制小数点移位数:数量**                | “3”                 |            |
| Shift binary point 3 places to the left  | **二进制位移位数:源** | “对话框” |
| **二进制位移位数:方向**                    | “双向”              |            |
| **二进制位移位数:数量**                    | “0”                 |            |
| **二进制小数点移位数:数量**                | –“3”                |            |

上面的 Shift Arithmetic 模块接受的输入为 124，对应于二进制格式的 01111100。将二进制小数点向右移动三位得到二进制格式的 01111100000。因此，上面的模块输出 995。

下面的 Shift Arithmetic 模块接受的输入也是 124。将二进制小数点向左移动三位得到二进制格式的 01111.100。因此，下面的模块输出 15.5。 -->

<!-- 不确定
## 算法


### 超范围移位

假设 WL 是输入信号的字长。下图中的着色区域显示向左和向右移位的超范围移位值。

![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/shift_arithmetic_block_oor_ranges_left_right_shifts.png)

同样，下图中的着色区域显示双向移位的超范围移位值。

![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/shift_arithmetic_block_oor_ranges_bidirectional_shifts.png)

对超范围移位的诊断响应如下所示，具体取决于操作模式：

| 模式     | 超范围移位值的诊断     |                        |                      |
| :------- | :--------------------- | :--------------------- | -------------------- |
| 无       | 警告                   | 错误                   |                      |
| 仿真模式 | 不报告任何警告或错误。 | 报告警告，但继续仿真。 | 报告错误并停止仿真。 |
| 代码生成 | 不起作用。             |                        |                      |



### 超范围移位值的仿真和加速模式结果

假设 U 为输入信号，WL 为输入信号的字长，Y 为输出。对于向左移位，超范围移位值的输出如下所示：

![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/shift_arithmetic_block_oor_ranges_left_shifts_behavior.png)

同样，对于向右移位，超范围移位值的输出如下所示：

![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/shift_arithmetic_block_oor_ranges_right_shifts_behavior.png)

对于双向移位，超范围移位值的输出如下所示：

![img](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/shift_arithmetic_block_oor_ranges_bidirectional_shifts_behavior.png)



### 超范围移位值的代码生成

对于生成的代码，处理超范围移位值的方法取决于**检查生成代码中是否有超出范围的 '二进制位移位数'** 的设置。

| 复选框设置 | 生成的代码                         | 仿真结果与生成的代码比较                                     |
| :--------- | :--------------------------------- | :----------------------------------------------------------- |
| 选中       | 包含条件语句，以防移位值超出范围。 | 仿真和加速模式结果与代码生成的结果匹配。                     |
| 清除       | 无法防止移位值超出范围。           | 对于在范围内的值，仿真和加速模式的结果与代码生成的结果匹配。对于超出范围的值，代码生成结果特定于编译器。 |

对于有符号负值输入信号的右移位，大多数 C 编译器使用算术移位，而不是逻辑移位。Shift Arithmetic 模块的生成代码取决于此编译器的行为。 -->

## 版本历史记录

- 在 2024b 之前推出


<!-- 暂无
## 扩展功能



### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 Verilog 代码和 VHDL 代码。

HDL Coder™ 提供影响 HDL 实现和综合逻辑的额外配置选项。



当**二进制位移位数:源**为**对话框**或**输入端口**时，您可以生成 HDL 代码。

**HDL 架构**

生成的 VHDL 代码使用 shift_right 函数和 sll 运算符。

生成的 Verilog 代码使用 >>> 和 <<< 移位运算符。

**HDL 模块属性**

| **ConstrainedOutputPipeline** | 通过移动设计中现有延迟的方式来放置在输出端的寄存器的数量。分布式流水线处理不会重新分发这些寄存器。默认值为 0。有关详细信息，请参阅[ConstrainedOutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#btp8gmp) (HDL Coder)。 |
| ----------------------------- | ------------------------------------------------------------ |
| **InputPipeline**             | 要在生成的代码中插入的输入流水线级数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 0。有关详细信息，请参阅[InputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-25) (HDL Coder)。 |
| **OutputPipeline**            | 要在生成的代码中插入的输出流水线级数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 0。有关详细信息，请参阅[OutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-26) (HDL Coder)。 |

**复数数据支持**

此模块支持复信号的代码生成。

**限制**

当 **Bits to shift:源**为**输入端口**时，不支持二进制小数点移位。



### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。

## 版本历史记录

**在 R2006a 之前推出** -->

## 另请参阅

[BitwiseOperator](BitwiseOperator.html) | [CompareToConstant](CompareToConstant.html) | [CompareToZero](CompareToZero.html) | [LogicalOperator](LogicalOperator.html) | [RelationalOperator](RelationalOperator.html)