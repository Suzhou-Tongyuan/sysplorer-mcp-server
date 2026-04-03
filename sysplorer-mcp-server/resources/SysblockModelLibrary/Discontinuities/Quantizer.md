# Quantizer
---
&nbsp;

按给定间隔将输入离散化


- **库：** Sysblock / Discontinuities

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/DiscontinuitiesPng/Quantizer/Quantizer.png')" style="width: 100px; height: auto;">

## 描述

Quantizer 模块使用量化算法离散化输入信号。该模块使用舍入到最接近整数方法将信号值映射到由**量化区间**定义的输出端的量化值。平滑的输入信号在量化后可能会呈现阶梯形状。

以下方程用数学方法说明舍入到最接近整数方法：

```
y = q * round(u/q) 
```

其中，y 是量化输出，u 是输入，q 是**量化区间**。


## 示例

添加一个 Constant 模块，将值设置为 3.6，添加一个 Quantizer 模块，量化间隔默认为 0.5，不足 0.5 的会被舍去，如 3.6 变为 3.5。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discontinuities/Quantizer.mo">Quantizer.mo</helpButton>。


<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/DiscontinuitiesPng/Quantizer/Quantizer01.png')" style="width: 600px; height: auto;">


<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/DiscontinuitiesPng/Quantizer/Quantizer02.png')" style="border: 1px solid black;width: 600px; height: auto;">

## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 要量化的输入信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

要应用量化算法的输入信号。

**数据类型：** float | double

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>y — 量化后的输出信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

输出信号由离散值组成，用舍入到最邻近整数方法量化：

```
y = q * round(u/q) 
```

其中，y 是输出，u 是输入，q 是**量化区间**。

**数据类型：** float | double

</div>
</div>


## 参数


<div class="details-box">
<details open>
<summary>量化区间 — 定义输出信号量化级别的间隔<div>0.5（默认） | 标量 | 向量</div></summary>
</details>
<div class="details-content">

指定算法中使用的量化间隔。Quantizer 模块输出的量化级别是量化区间的整数倍。

</div>
</div>

<!-- 
#### 编程用法

| **模块参数**：`QuantizationInterval` |
| ------------------------------------ |
| **类型**：字符向量                   |
| **值**：任何实数或复数值             |
| **默认值**：`'0.5'`                  | -->

<!-- 暂无
### `线性化时视为增益` — 指定增益值 `On` （默认） | 布尔

Sysplorer软件中的线性化命令将此模块视为状态空间中的增益。选择此参数将使得这些命令将增益视为 1。清除此参数可使命令将增益视为 0。

#### 编程用法

| **模块参数**：`LinearizeAsGain` |
| ------------------------------- |
| **类型**：字符向量              |
| **值**：`'off'` | `'on'`        |
| **默认值**：`'on'`              |
 -->

<!-- 暂无
### `采样时间` — `-1` 以外的采样时间值 `-1` （默认） | 标量 | 向量

指定采样时间间隔。要继承采样时间，请将此参数设置为 `-1`。有关详细信息，请参阅[指定采样时间](https://ww2.mathworks.cn/help/simulink/ug/how-to-specify-the-sample-time.html)。

#### 依存关系

仅当您将此参数设置为 `-1` 以外的值时才可见。要了解详细信息，请参阅[不建议设置采样时间的模块](https://ww2.mathworks.cn/help/simulink/ug/sampletimehiding.html)。

#### 编程用法

要以编程方式设置模块参数值，请使用 [`set_param`](https://ww2.mathworks.cn/help/simulink/slref/set_param.html) 函数。

| **参数:** | `SampleTime`                                |
| --------- | ------------------------------------------- |
| **值:**   | `"-1"` (默认) \| scalar or vector in quotes | -->


<!-- ## 模块特性 -->

<!-- 部分功能暂无
| **数据类型**     | `double` \| `single` |
| ---------------- | ------------------- |
| **直接馈通**     | `是`                |
| **多维信号**     | `否`                |
| **可变大小信号** | `否`                |
| **过零检测**     | `否`                | -->

<!-- ## 扩展功能 -->


<!-- 
### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。 -->

## 版本历史记录

- 在 2024b 之前推出

### 限制信息
不支持部分
1. 参数-线性化时视为增益 — 指定增益值
2. 参数-采样时间 — -1 以外的采样时间值

## 另请参阅

[Relay](Relay.html) | [RateLimiter](RateLimiter.html) 