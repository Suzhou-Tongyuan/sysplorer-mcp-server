# Quantizer
---
&nbsp;

按给定间隔将输入离散化。


- **库：** TYDSPSystem / FixedPointDesign / Quantizer 

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


## 版本历史记录

- 在 2026a 推出

## 限制信息
不支持部分
1. 参数-线性化时视为增益 — 指定增益值
2. 参数-采样时间 — -1 以外的采样时间值

## 另请参阅

[Relay](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Discontinuities/Relay.html) | [RateLimiter](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Discontinuities/RateLimiter.html) 
