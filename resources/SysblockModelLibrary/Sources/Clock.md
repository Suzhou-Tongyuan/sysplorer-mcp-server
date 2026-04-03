# Clock
---
显示并提供仿真时间

**库：** Sysblock模块库 / Sources

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/Clock/Clock.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

Clock 模块在每个仿真时间步输出当前仿真时间。此模块对需要仿真时间的其他模块非常有用。

<!-- 当您在离散系统中需要当前时间时，请使用 [Digital Clock](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/digitalclock.html) 模块。 -->

## 示例

<!-- [![使用 Memory 和 Clock 模块计算并显示仿真步长](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/memoryandclockblockcalculatestepsizeexample_01_zh_CN.png)使用 Memory 和 Clock 模块计算并显示仿真步长此示例说明如何使用 Memory 和 Clock 模块来计算和显示仿真中的步长。](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/calculate-and-display-sim-step-size-using-memory-and-clock-blocks.html)

[![用动画演示倒立摆](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/penddemoexample_02_zh_CN.png)用动画演示倒立摆此示例说明如何对倒立摆建模。动画是用 MATLAB® Handle Graphics® 创建的。动画模块是一个封装的 S-Function。有关详细信息，请使用上下文菜单查看 Animation 模块的封装下的内容，并打开 S-Function 进行编辑。](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/inverted-pendulum-with-animation.html)

[![精确的过零检测](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/sldemo_zeroxingexample_02_zh_CN.png)精确的过零检测此示例说明 Simulink® 中过零的工作原理。在此模型中，三个经过偏移的正弦波被馈送到绝对值模块及饱和模块中。在正好 t = 5 时，开关模块的输出从绝对值变为饱和模块。Simulink 中的过零将自动检测到开关模块具体何时更改其输出，求解器将步进到事件发生的确切时间。您可以通过检查示波器输出来查看这些信息。](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/accurate-zero-crossing-detection.html) -->

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/Clock1.mo">Clock1.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/Clock/Clock_ex.png')" style="width: 300px; height: auto; transform: scale(0.8);">

### 示例说明

- Clock 模块：生成一个与仿真时间同步的时间戳信号。这个模块通常用于在仿真中记录事件的时间点，或者在需要时间信息的场景中使用；
- Scope 模块：用于显示模型的输出结果，即随仿真时间变化的时间戳信号。

## 端口

### 输出


<div class="details-box">
<details open>
<summary>y — 采样时间<div>标量</div></summary>
</details>
<div class="details-content">

采样时间，指定为每个仿真时间步的当前仿真时间。

**数据类型：** double

</div>
</div>


<!-- ## 参数


### 显示时间 — 在模块图标上显示仿真时间 off （默认） | on



选中此复选框会将仿真时间显示为 Clock 模块图标的一部分。清除此复选框时，仿真时间不显示在模块图标上。

#### 编程用法

| **模块参数**：DisplayTime |
| --------------------------- |
| **类型：**字符向量          |
| **值：**'off' | 'on'    |
| **默认值：**'off'         |



### 抽取 — 更新模块图标的时间间隔 10 （默认） | 正整数



将 Simulink® 更新 Clock 图标的时间间隔指定为正整数。

假设抽取值为 1000。则对于 1 毫秒的固定积分步长，Clock 图标会在 1 秒、2 秒等时间更新。

#### 依存关系

要在模块图标上显示仿真时间，必须选中**显示时间**复选框。

#### 编程用法

| **模块参数**：Decimation |
| -------------------------- |
| **类型：**字符向量         |
| **值：**标量               |
| **默认值：**'10'         | -->


<!-- ## 模块特性

| **数据类型**     | double |
| ---------------- | -------- |
| **直接馈通**     | 否     |
| **多维信号**     | 否     |
| **可变大小信号** | 否     |
| **过零检测**     | 否     | -->


## 版本历史记录

- 在 2024b 之前推出

### 限制信息

1. 暂不支持在模块图标上显示仿真时间；  
2. 暂不支持更新模块图标的时间间隔。


<!-- ## 扩展功能



### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。

不建议用于生产代码。涉及到嵌入式系统中常见的资源限制以及对速度和内存的限制。生成的代码可以包含动态分配和释放内存、递归、额外的内存开销以及长短不等的执行时间。虽然代码在功能上有效并且在资源丰富的环境中通常可接受，但较小的嵌入式目标通常不能支持此类代码。通常情况下，模块会向适合生产代码的方向发展。因此，适合生产代码的模块仍然适用。

## 版本历史记录

**在 R2006a 之前推出** -->

<!-- ## 另请参阅

[Digital Clock](https://ww2.mathworks.cn/help/releases/R2022b/simulink/slref/digitalclock.html)

### 主题

- [采样时间](https://ww2.mathworks.cn/help/releases/R2022b/simulink/sample-time.html) -->