# DeadZoneDynamic
---
&nbsp;

提供零输出的动态区域。

- **库:** Sysblock / Discontinuities

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/DiscontinuitiesPng/deadZoneDynamic/deadZoneDynamic.png')" style="width: 100px; height: auto;">

## 描述
DeadZoneDynamic 模块根据指定上限和下限的动态输入信号生成零输出区域。模块输出取决于输入 **u**，以及输入信号 **up** 和 **lo** 的值。

| 输入                   | 输出     |
| :---------------------- | :--------- |
| `u >= lo` and `u <= up` | Zero       |
| `u > up`                | `u` – `up` |
| `u < lo`                | `u` – `lo` |

DeadZoneDynamic 模块是一个封装子系统，没有任何参数。

## 示例
我们可以设置 DeadZoneDynamic 模块上下限分别使用 constant 模块设置为 [-1,1]，然后使用 sineWave 模块作为动态信号输入。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discontinuities/DeadZoneDynamic.mo">DeadZoneDynamic.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/DiscontinuitiesPng/deadZoneDynamic/deadZoneDynamic01.png')" style="width: 600px; height: auto;">

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/DiscontinuitiesPng/deadZoneDynamic/deadZoneDynamic02.png')" style="width: 600px; height: auto;">


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号标量<div>标量 |向量</div></summary>
</details>
<div class="details-content">

死区算法的输入信号。

**数据类型:** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | fixed point

</div>
</div>


<div class="details-box">
<details open>
<summary>lo — 盲区标量的下限<div>向量</div></summary>
</details>
<div class="details-content">

动态值提供零输出区域的下限。当 input 小于 **lo** 时，输出值将向下移动 **lo** 的值。

**数据类型:** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | fixed point

</div>
</div>



<div class="details-box">
<details open>
<summary>up — 死区标量的上限<div></div></summary>
</details>
<div class="details-content">

动态值提供零输出区域的上限。当 input 大于 **up** 时，输出值将向下移动 **up** 的值。

**数据类型:** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32

</div>
</div>

### 输出


<div class="details-box">
<details open>
<summary>y — 输出信号标量<div></div></summary>
</details>
<div class="details-content">

将动态死区算法应用于输入信号后的输出信号。


**数据类型:** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 

</div>
</div>

<!-- ## 参数

## 模块特性 -->

<!-- 部分功能未实现
| **数据类型**     | `double` \| `fixed point` \| `integer` \| `float` |
| ---------------- | ----------------------------------------------- |
| **直接馈通**     | `是`                                            |
| **多维信号**     | `否`                                            |
| **可变大小信号** | `否`                                            |
| **过零检测**     | `否`                                            | -->


<!-- ## 扩展功能 -->
<!-- 
### C/C++ Code Generation Generate C and C++ code using Simulink® Coder™.



### HDL Code Generation Generate VHDL, Verilog and SystemVerilog code for FPGA and ASIC designs using HDL Coder™.



HDL Coder™ provides additional configuration options that affect HDL implementation and synthesized logic.

**HDL Architecture**

This block has one default HDL architecture.

**HDL Block Properties**

| **ConstrainedOutputPipeline** | Number of registers to place at the outputs by moving existing delays within your design. Distributed pipelining does not redistribute these registers. The default is `0`. For more details, see [ConstrainedOutputPipeline](https://ww2.mathworks.cn/help/hdlcoder/ug/block-implementation-parameters.html#btp8gmp) (HDL Coder). |
| ----------------------------- | ------------------------------------------------------------ |
| **InputPipeline**             | Number of input pipeline stages to insert in the generated code. Distributed pipelining and constrained output pipelining can move these registers. The default is `0`. For more details, see [InputPipeline](https://ww2.mathworks.cn/help/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-25) (HDL Coder). |
| **OutputPipeline**            | Number of output pipeline stages to insert in the generated code. Distributed pipelining and constrained output pipelining can move these registers. The default is `0`. For more details, see [OutputPipeline](https://ww2.mathworks.cn/help/hdlcoder/ug/block-implementation-parameters.html#bsmj7ju-26) (HDL Coder). |



### PLC Code Generation Generate Structured Text code using Simulink® PLC Coder™.



### Fixed-Point Conversion Design and simulate fixed-point systems using Fixed-Point Designer™. -->


## 版本历史记录

- 在 2024b 之前推出

<!-- ### 限制信息 -->

## 另请参阅
[DeadZone](DeadZone.html) 