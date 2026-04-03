# RateLimiter
---
&nbsp;


限制信号变化的速率


- **库：** Sysblock / Discontinuities

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/DiscontinuitiesPng/rateLimiter/rateLimiter.png')" style="width: 100px; height: auto;">

## 描述

Rate Limiter 模块可以限制通过它传递的信号的一阶导数。输出的变化速率不快于指定的限制。


## 示例

将 stpe 模块初始值设置为 0 跃迁时间设置为 1 秒终值为 5 将 rateLimiter 模块上升沿压摆率设置为 2，我们可以看到在 3.5 秒时经过 rateLimiter 的输出才到达 5。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discontinuities/RateLimiter.mo">RateLimiter.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/DiscontinuitiesPng/rateLimiter/rateLimiter01.png')" style="width: 600px; height: auto;">

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/DiscontinuitiesPng/rateLimiter/rateLimiter02.png')" style="width: 600px; height: auto;">


## 端口

### 输入


<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量</div></summary>
</details>
<div class="details-content">

要应用速率限制器算法的输入信号。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | fixed point

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量</div></summary>
</details>
<div class="details-content">

经过速率限制器算法处理后的输出信号。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | fixed point

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>上升沿压摆率 — 递增输入的导数的限制<div>1（默认） | 实数</div></summary>
</details>
<div class="details-content">

指定输入信号的上升沿速率的限制。此参数对于定点输入是可调的。

</div>
</div>


<!-- 暂无
#### 编程用法

| **模块参数**：`RisingSlewLimit` |
| ------------------------------- |
| **类型**：字符向量              |
| **值**：实数                    |
| **默认值**：`'1'`               | -->



<div class="details-box">
<details open>
<summary>下降沿压摆率 — 递减输入的导数的限制<div>-1（默认）| 实数</div></summary>
</details>
<div class="details-content">

指定输入信号的下降沿速率的下限。此参数对于定点输入是可调的。

</div>
</div>

<!-- 暂无
#### 编程用法

| **模块参数**：`FallingSlewLimit` |
| -------------------------------- |
| **类型**：字符向量               |
| **值**：实数                     |
| **默认值**：`'-1'`               | -->


<!-- 暂无
### `采样时间模式` — 采样时间模式 “`继承`” （默认） | “`连续`”



指定采样时间模式，`continuous` 或者从驱动模块 `inherited`。

#### 编程用法

| **模块参数**：`SampleTimeMode`            |
| ----------------------------------------- |
| **类型**：字符向量                        |
| **值**：`'inherited'` | `'continuous'` \| |
| **默认值**：`'inherited'`                 | -->


<div class="details-box">
<details open>
<summary>初始条件 — 初始输出<div>0（默认） | 标量</div></summary>
</details>
<div class="details-content">

设置仿真的初始输出。不允许您将此模块的初始条件设置为 `inf` 或 `NaN`。

</div>
</div>


<!-- 暂无
#### 编程用法

| **模块参数**：`InitialCondition` |
| -------------------------------- |
| **类型**：字符向量               |
| **值**：`scalar`                 |
| **默认值**：`'0'`                |
 -->

<!-- 暂无
### `线性化时视为增益` — 指定增益值 `On` （默认） | 布尔



选中此复选框将使得这些命令将增益视为 1。Simulink 软件中的线性化命令将此模块视为状态空间中的增益。清除该框将使得这些命令将增益视为 0。

#### 编程用法

| **模块参数**：`LinearizeAsGain` |
| ------------------------------- |
| **类型**：字符向量              |
| **值**：`'off'` | `'on'`        |
| **默认值**：`'on'`              | -->

<!-- ## 模块特性 -->

<!-- 部分功能暂无
| **数据类型**     | `double` \| `fixed point` \| `integer` \| `single` |
| ---------------- | ----------------------------------------------- |
| **直接馈通**     | `是`                                            |
| **多维信号**     | `否`                                            |
| **可变大小信号** | `否`                                            |
| **过零检测**     | `否`                                            | -->

<!-- ## 扩展功能 -->


<!-- 
### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。



### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。 -->





## 版本历史记录

- 在 2024b 之前推出

## 另请参阅

[RateLimiterDynamic](RateLimiterDynamic.html) | [Saturation](Saturation.html)