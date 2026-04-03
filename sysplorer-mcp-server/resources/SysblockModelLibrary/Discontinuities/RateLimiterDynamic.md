# RateLimiterDynamic
---
&nbsp;

限制信号变化的速率

- **库：** Sysblock / Discontinuities

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/DiscontinuitiesPng/rateLimiterDynamic/rateLimiterDynamic.png')"  style="width: 100px; height: auto;">

## 描述

RateLimiterDynamic 模块限制信号的上升和下降速率。

- 外部信号 `up` 设置信号上升沿速率的上限。
- 外部信号 `lo` 设置信号下降沿速率的下限。

使用 RateLimiterDynamic 模块时，请遵循以下指导原则：

- 确保 `up` 和 `lo` 的数据类型与输入信号 `u` 的数据类型相同。

  如果下限使用有符号类型，而输入信号使用无符号类型，则输出信号将一直增加，而不管输入信号和限制。

- 使用定步长求解器仿真包含此模块的模型。

  因为 RateLimiterDynamic 模块仅支持离散采样时间。


## 示例

将一个 step 模块初值设为 10，终值为 1，跃迁时间为 1，将信号变化速率限制在 [sint,2] 之间，可以看到它的信号变化情况。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discontinuities/RateLimiterDynamic.mo">RateLimiterDynamic.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/DiscontinuitiesPng/rateLimiterDynamic/rateLimiterDynamic01.png')" style="width: 600px; height: auto;">

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/DiscontinuitiesPng/rateLimiterDynamic/rateLimiterDynamic02.png')" style="width: 600px; height: auto;border: 1px solid black;">

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

<div class="details-box">
<details open>
<summary>lo — 递减输入的导数的限制<div>标量</div></summary>
</details>
<div class="details-content">

动态值，用于提供输入信号的下降沿速率的限制。**lo** 的信号数据类型需要与输入信号 **u** 的数据类型相同。

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | fixed point

</div>
</div>


<div class="details-box">
<details open>
<summary>up — 递增输入的导数的限制<div>标量</div></summary>
</details>
<div class="details-content">

动态值，用于提供输入信号的上升沿速率的限制。**up** 的信号数据类型需要与输入信号 **u** 的数据类型相同。

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

**数据类型：** float | double | int8 | int16 | int32 | uint8 | uint16 | uint32 | fixed point | enumerated | bus

</div>
</div>

<!-- ## 模块特性 -->

<!-- 
| **数据类型**     | `double` \| `fixed point` \| `integer` \| `float` |
| ---------------- | ----------------------------------------------- |
| **直接馈通**     | `否`                                            |
| **多维信号**     | `否`                                            |
| **可变大小信号** | `否`                                            |
| **过零检测**     | `否`                                            | -->

<!-- ## 扩展功能 -->

<!-- 

### C/C++ 代码生成 使用 Simulink® Coder™ 生成 C 代码和 C++ 代码。



### PLC 代码生成 使用 Simulink® PLC Coder™ 生成结构化文本代码。



### 定点转换 使用 Fixed-Point Designer™ 设计和仿真定点系统。 -->
<!-- 
## 版本历史记录 -->
<!-- 
**在 R2006a 之前推出** -->

<!-- ### 限制信息 -->

## 版本历史记录

- 在 2024b 之前推出

## 另请参阅
[RateLimiter](RateLimiter.html)