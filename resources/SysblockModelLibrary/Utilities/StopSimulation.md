# StopSimulation
---
&nbsp;

当输入为非零值时使仿真停止

**库：** Sysblock模块库 / Sources

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/StopSimulation/StopSimulation.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

当输入为非零值时，StopSimulation 模块将使仿真停止。在停止之前，仿真会完成当前时间步。如果模块的输入为向量，则任何非零的向量元素都会导致仿真停止。

<!-- 如果您在 [For Iterator](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/foriterator.html) 子系统中使用 Stop Simulation 模块，停止操作将在执行完子系统在一个时间步中的*所有*迭代之后发生。在下一个时间步开始之前，停止操作不会中断仿真。 -->

<!-- 您不能使用 StopSimulation 模块暂停仿真。 -->

<!-- 要创建暂停仿真的模块，请参阅[使用 Assertion 模块暂停仿真](https://ww2.mathworks.cn/help/releases/R2022b/simulink/ug/controlling-execution-of-a-simulation.html#bq0ht63)。 -->

## 示例

<!-- [![Stop Simulation Block with Relational Operator Block](https://ww2.mathworks.cn/help/releases/R2022b/examples/simulink/win64/StopSimulationWithRelationalOperatorExample_01.png)Stop Simulation Block with Relational Operator BlockControl when a simulation stops by using a Stop Simulation block with a Relational Operator block.](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/stop-simulation-block-with-relational-operator-block.html)

[![防抱死制动系统建模](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/modelinganantilockbrakingsystemexample_07_zh_CN.png)防抱死制动系统建模此示例说明如何对防抱死制动系统 (ABS) 进行简单建模。它对车辆在紧急制动情况下的动态行为进行仿真。该模型表示单个车轮，可以重复多次以创建多轮车辆的模型。](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/modeling-an-anti-lock-braking-system.html) -->

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/StopSimulation.mo">StopSimulation.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/StopSimulation/StopSimulation_ex.png')" style="width: 300px; height: auto; transform: scale(0.8);">

### 示例说明

- Step 模块：用于提供一个输入信号，经过一段时间，信号从 0 变为非零；
- StopSimulation 模块：用于在满足特定条件时停止仿真。在这个例子中，当信号非零时，仿真将停止。

## 端口

### 输入


<div class="details-box">
<details open>
<summary>Port_1 — 输入信号<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

当输入信号为非零值时使仿真停止。此端口接受 double 或 boolean 数据类型的实信号。

**数据类型：** double | boolean

</div>
</div>






<!-- ## 模块特性

| **数据类型**     | Boolean | double |
| ---------------- | -------------------- |
| **直接馈通**     | 否                 |
| **多维信号**     | 否                 |
| **可变大小信号** | 否                 |
| **过零检测**     | 否                 | -->

<!-- ## 扩展功能



### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。



### HDL 代码生成 使用 HDL Coder™ 为 FPGA 和 ASIC 设计生成 Verilog 代码和 VHDL 代码。



### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。 -->

<!-- ## 版本历史记录

### 限制信息 -->

<!-- ## 另请参阅

### 主题

- [以交互方式对模型进行仿真]() -->

## 版本历史记录

- 在 2024b 之前推出