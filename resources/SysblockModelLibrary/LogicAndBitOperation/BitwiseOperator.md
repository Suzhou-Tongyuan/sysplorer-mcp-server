# BitwiseOperator
---
&nbsp;

对输入执行指定的按位运算

**库：** Sysblock模块库 / LogicAndBitOperation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/BitwiseOperator/BitwiseOperator.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

BitwiseOperator 模块执行您为一个或多个操作数指定的按位运算。与 [LogicalOperator](LogicalOperator.html) 模块的逻辑运算不同的是，按位运算将操作数视为位向量，而不是单个值。

### 对模块运算的限制

BitwiseOperator 模块不支持移位运算。对于移位运算，请使用 [ShiftArithmetic](ShiftArithmetic.html) 模块。  

当配置为多输入“异或”门时，此模块将按照 IEEE® 逻辑元素标准的规定执行模 2 加法。

## 示例

<!-- 暂无创建示例
[![Bitwise Operator 模块的无符号输入](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/unsignedinputsforthebitwiseoperatorblockexample_01_zh_CN.png)Bitwise Operator 模块的无符号输入此示例说明 Bitwise Operator 模块如何处理无符号输入。](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/unsigned-inputs-for-bitwise-operator-block.html)

[![Bitwise Operator 模块的有符号输入](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/signedinputsforthebitwiseoperatorblockexample_01_zh_CN.png)Bitwise Operator 模块的有符号输入此示例说明 Bitwise Operator 模块如何处理有符号输入。](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/signed-inputs-for-bitwise-operator-block.html)

[![WWV Digital Receiver - Synchronization and Detection](https://ww2.mathworks.cn/help/releases/R2022b/examples/dsp/win64/WWVDigitalReceiverSynchronizationAndDetectionExample_03.png)WWV Digital Receiver - Synchronization and DetectionAn implementation of a digital receiver that synchronizes to the time code information broadcast by radio station WWV and decodes it to display time information. The example uses the Simulink®, DSP System Toolbox™, and Stateflow® products with the MATLAB® Function block to achieve a simple noncoherent digital receiver.](https://ww2.mathworks.cn/help/releases/R2022b/dsp/ug/wwv-digital-receiver-synchronization-and-detection.html) -->

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/BitwiseOperator.mo">BitwiseOperator.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/BitwiseOperator/BitwiseOperator_ex.png')" style="width: 600px;transform: scale(0.8);">

### 示例说明

- Constant 模块：用于提供固定的输入值。在这个例子中，我们提供了两个逻辑值，一个为 true（或1），另一个为 false（或0）；
- LogicalOperator 模块：用于执行逻辑运算。在这个例子中，我们选择了 ‘与’ 运算，这意味着只有当两个输入都是 true（或1）时，输出才会是 true（或1）；
- Scope 模块：用于显示模型的输出。在这个例子中，它显示了 ‘与’ 运算的结果。

## 端口

### 输入

<div class="details-box">
<details open>
<summary>u1 — 输入信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

输入信号，指定为标量或向量。

- “非”运算符仅接受一个输入，该输入可以是标量也可以是向量。如果输入为向量，则输出为相同大小的向量，其中包含输入向量元素的按位逻辑补码；
- 对于单个向量输入，模块会将运算（除“非”运算符外）应用于向量的所有元素；
- 对于两个或更多输入，模块将在所有输入之间执行运算。如果输入为向量，模块将在对应的向量元素之间执行运算以生成向量输出。

**数据类型：** int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | fixedPoint

</div>
</div>



### 输出

####  

<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

指定为输出数据类型的输出信号，模块从驱动模块继承该输出数据类型，且该数据类型必须准确表示零。满足此条件的数据类型包括有符号整数和无符号整数数据类型。

模块输出的大小取决于输入的数量、向量大小以及您选择的运算符。如果您不指定位掩码，则输出为标量。如果您指定位掩码，则输出为向量。

**数据类型：** int8 | int16 | int32 | uint8 | uint16 | uint32 | boolean | fixedPoint

</div>
</div>



## 参数


<div class="details-box">
<details open>
<summary>运算符 — 按位逻辑运算符<div>与 （默认） | 或 | 与非 | 或非 | 异或 | 非</div></summary>
</details>
<div class="details-content">

为模块操作数指定按位逻辑运算符。

您可以选择以下按位运算之一：

| 按位运算 | 描述                                            |
| :------- | :---------------------------------------------- |
| 与      | 如果对应的位全部为 TRUE，则为 TRUE              |
| 或       | 如果至少一个对应的位为 TRUE，则为 TRUE          |
| 或非     | 如果至少一个对应的位为 FALSE，则为 TRUE         |
| 与非      | 如果没有对应的位为 TRUE，则为 TRUE              |
| 异或      | 如果有奇数个对应位为 TRUE，则为 TRUE            |
| 非      | 如果输入为 FALSE，则为 TRUE（仅适用于单个输入） |

</div>
</div>



<!-- 暂无
#### 编程用法

| **模块参数**：logicop                                     |
| ----------------------------------------------------------- |
| **类型**：字符向量                                          |
| **值**：'与'\|'或' \|'或非'\|'与非' \|'异或' \| '非' |
| **默认值**：'与'                                         | -->



<div class="details-box">
<details open>
<summary>使用位掩码 — 选择使用位掩码<div>选中 （默认） | 未选中</div></summary>
</details>
<div class="details-content">

选择要使用位掩码。清除此复选框将启用**输入端口数目**并禁用**位掩码**和**将掩码视为**。

</div>
</div>


<!-- 暂无
#### 编程用法

| **模块参数**：UseBitMask |
| -------------------------- |
| **类型**：字符向量         |
| **值**：'off'\|'on'     |
| **默认值**：'on'         | -->


<div class="details-box">
<details open>
<summary>输入端口数目 — 输入信号的数量<div>1 （默认） | 整数</div></summary>
</details>
<div class="details-content">

指定输入的数量。您可以有多个输入端口。

#### 依存关系

清除**使用位掩码**复选框将启用**输入端口数目**并禁用**位掩码**和**将掩码视为**。

</div>
</div>


<!-- 暂无
#### 编程用法

| **模块参数**：NumInputPorts |
| ----------------------------- |
| **类型**：字符向量            |
| **值**：正整数                |
| **默认值**：'1'             | -->



<div class="details-box">
<details open>
<summary>位掩码 — 要与单个输入关联的位掩码<div>0B11011001 （默认）</div></summary>
</details>
<div class="details-content">


指定要与单个输入关联的位掩码。此参数将值读取为十六进制值。

您可以使用位掩码设置、获取或清除输入位。

| 要执行... | 将 Operator 参数设置为... | 并按此方式创建位掩码...                 |
| :-------- | :------------------------ | :-------------------------------------- |
| 位设置    | 或                        | 对您要设置为 1 的每个对应的输入位使用 1 |
| 位清除    | 与                       | 对您要设置为 0 的每个对应的输入位使用 0 |
| 位获取    | 与                       | 对您要获取的每个对应的输入位使用 1      |

假设您要设置 8 位输入向量的第四位。位掩码将为 00010000，对于**位掩码**参数，您可以将其指定为 2^4。要清除该位，位掩码将为 11101111，对于**位掩码**参数，您可以将其指定为 2^7+2^6+2^5+2^3+2^2+2^1+2^0。


::: tip 提示 
不要使用大于 53 位的掩码。否则，仿真过程中将出现错误消息。
:::


#### 依存关系

仅当您选择**使用位掩码**时，此参数才可用。

</div>
</div>



<!-- 暂无
#### 编程用法

| **模块参数**：BitMask             |
| ----------------------------------- |
| **类型**：字符向量                  |
| **值**：正整数                      |
| **默认值**：0B11011001 | -->


<!-- 暂无
### 将掩码视为 — 将掩码视为真实值还是存储的整数 “存储的整数” （默认） | “真实值”



指定将掩码视为真实值还是存储的整数。

编码方案是 V = SQ + B，如 Fixed-Point Designer™ 文档中的[定标](https://ww2.mathworks.cn/help/releases/R2022b/fixedpoint/ug/scaling.html) (Fixed-Point Designer)部分所述。“真实值”将掩码视为 V。“存储的整数”将掩码视为 Q。

#### 依存关系

仅当您选择**使用位掩码**时，此参数才可用。

#### 编程用法

| **模块参数**：BitMaskRealWorld                  |
| ------------------------------------------------- |
| **类型**：字符向量                                |
| **值**：'Real World Value' \| 'Stored Integer' |
| **默认值**：'Stored Integer'                    | -->


<!-- 暂无
## 模块特性

| **数据类型**                                                 | Booleana \| fixed point \| integer |
| ------------------------------------------------------------ | -------------------------------------- |
| **直接馈通**                                                 | 否                                   |
| **多维信号**                                                 | 是                                   |
| **可变大小信号**                                             | 否                                   |
| **过零检测**                                                 | 否                                   |
| [a]() 建议不要对布尔信号进行位运算。 |                                        | -->


<!-- ## 扩展功能

（与其他模块的关联功能，例如，C/C++代码生成，HDL代码生成，定点转换，数据类型推导。） -->

## 版本历史记录

- 在 2024b 之前推出

### 限制信息

1. 暂不支持将掩码视为真实值或存储的整数；  
2. 输入和输出端口暂不支持 int64 和 uint64 的数据类型。

<!-- 暂无

##扩展功能

### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 Verilog 代码和 VHDL 代码。



HDL Coder™ 提供影响 HDL 实现和综合逻辑的额外配置选项。

**HDL 架构**

此模块具有一个默认 HDL 架构。

**HDL 模块属性**

| **ConstrainedOutputPipeline** | 通过移动设计中现有延迟的方式来放置在输出端的寄存器的数量。分布式流水线处理不会重新分发这些寄存器。默认值为 0。有关详细信息，请参阅[ConstrainedOutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#btp8gmp) (HDL Coder)。 |
| ----------------------------- | ------------------------------------------------------------ |
| **InputPipeline**             | 要在生成的代码中插入的输入流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 0。有关详细信息，请参阅[InputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-25) (HDL Coder)。 |
| **OutputPipeline**            | 要在生成的代码中插入的输出流水线阶段数。分布式流水线处理和受限输出流水线处理可以移动这些寄存器。默认值为 0。有关详细信息，请参阅[OutputPipeline](https://ww2.mathworks.cn/help/releases/R2022b/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-26) (HDL Coder)。 |



### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。 

## 版本历史记录


**在 R2006a 之前推出** -->

## 另请参阅

[LogicalOperator](LogicalOperator.html) | [CompareToConstant](CompareToConstant.html) | [CompareToZero](CompareToZero.html) | [ShiftArithmetic](ShiftArithmetic.html)