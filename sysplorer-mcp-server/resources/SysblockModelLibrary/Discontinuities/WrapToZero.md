# WrapToZero
---
&nbsp;

如果输入大于阈值，将输出设置为零。


- **库：** Sysblock / Discontinuities

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/DiscontinuitiesPng/wrapToZero/wrapToZero.png')"  style="width: 100px; height: auto;">

## 描述

当输入大于**阈值**值时，WrapToZero 模块将输出设置为零。当输入小于或等于**阈值**时，输出等于输入。

## 示例

将 constant 模块的值为 5，将 WrapToZero 的阈值为 3。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discontinuities/WrapToZero.mo">WrapToZero.mo</helpButton>。


<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/DiscontinuitiesPng/wrapToZero/wrapToZero01.png')" style="width: 600px; height: auto;">


<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/DiscontinuitiesPng/wrapToZero/wrapToZero02.png')" style="width: 600px; height: auto;">


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

输入信号，指定为标量或向量。等于或大于 Threshold 值的信号值设置为零。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | Boolean | fixed point

</div>
</div>

### 输出


<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

设置为输入信号值或零的输出信号。输出的数据类型与输入的数据类型相同。

::: tip 提示
如果输入数据类型不能表示零，将发生参数溢出。要检测此溢出，请转到**配置参数**对话框的**诊断 > 数据有效性**窗格，并将**参数 > 检测上溢**设置为**警告**或**错误**。
:::

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | Boolean | fixed point

</div>
</div>

## 参数


要编辑 WraptoZero 模块的参数，请双击模块图标。

<div class="details-box">
<details open>
<summary>阈值 — 使模块输出零的阈值<div>255 （默认） | 标量</div></summary>
</details>
<div class="details-content">

使模块将输出值设置为零的阈值。

</div>
</div>



<!-- 
#### 编程用法

| **模块参数**：`Threshold` |
| ------------------------- |
| **类型**：字符向量        |
| **值**：`scalar`          |
| **默认值**：`'255'`       | -->

<!-- ## 模块特性 -->

<!--部分功能暂无 
| **数据类型**     | `Boolean` \| `double` \| `fixed point` \| `integer` \| `float` |
| ---------------- | ----------------------------------------------------------- |
| **直接馈通**     | `是`                                                        |
| **多维信号**     | `是`                                                        |
| **可变大小信号** | `否`                                                        |
| **过零检测**     | `否`                                                        | -->

<!-- ## 扩展功能 -->


<!-- 
### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 Verilog 代码和 VHDL 代码。



### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。 -->


<!-- ## 版本历史记录 -->

<!-- **在 R2006a 之前推出** -->

<!-- ### 限制信息 -->

## 版本历史记录

- 在 2024b 之前推出

## 另请参阅

[Saturation](Saturation.html) | [SaturationDynamic](SaturationDynamic.html)