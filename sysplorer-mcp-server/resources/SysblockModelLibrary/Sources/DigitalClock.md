# DigitalClock
---
&nbsp;
以指定的采样间隔输出仿真时间。

- **库：** Sysblock / Sources

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/digitalClock/1.png')" style="width:100px;border:black 1px solid;"> 

## 描述

Digital Clock 模块仅以指定的采样间隔输出仿真时间。在其他时间，此模块保留输出的上一个值。要控制此模块的精度，请使用模块对话框中的采样时间参数。

当需要离散系统中的当前仿真时间时，请使用此模块，而不是 **Clock** 模块（它输出连续时间）。

## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/digitalClock.mo">digitalClock.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/digitalClock/2.png')" style="width:500px;border:black 1px solid;"> 

### 仿真结果

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Sources/digitalClock/3.png')" style="width:800px;border:black 1px solid;"> 

## 端口

### 输出

<div class="details-box">
<details open>
<summary>Port_1 — 采样时间<div>标量</div></summary>
</details>
<div class="details-content">

采用指定的采样间隔的采样时间（以秒为单位）。在其他时间，此模块保留输出的上一个值。

**数据类型：** double

</div>
</div>



## 参数

<div class="details-box">
<details open>
<summary>采样时间 — 采样间隔<div>标量</div></summary>
</details>
<div class="details-content">

指定采样间隔（以秒为单位）。指定为双精度数据类型的实数值标量。

</div>
</div>
 

## 版本历史记录

- 在 2025a 推出

## 限制信息

- 参数类型均只能为 double。