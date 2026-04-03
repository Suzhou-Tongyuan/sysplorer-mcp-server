# Derivative
---
&nbsp;

Derivative 模块采用数值差分 Δu/Δt 的方式输出输入信号 u 关于时间 t 的导数

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/Derivative/Derivative.png')" style="width:100px; border: 1px solid black;">

**库：** Sysblock 模块库/ Continuous

## 描述

Derivative 模块采用数值差分 Δu/Δt 的方式输出输入信号 u 关于时间 t 的导数。

## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continuous/Derivative.mo">Derivative.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/Derivative/Derivative_example.png')" style="width:600px; border: 1px solid black;">

### 仿真设置

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/Derivative/setting.png')" style="width:500px; border: 1px solid black;">

### 参考结果

<img :src="$withBase('/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Continues/Derivative/result.png')" style="width:600px; border: 1px solid black;">

## 端口

### 输入

<div class="details-box">
<details open>
<summary>U — 输入信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

接收要进行求导的输入信号，允许为实数标量或向量。

**数据类型：** double

</div>
</div>

### 输出


<div class="details-box">
<details open>
<summary>Y — 输入信号的时间导数<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

​	输出输入信号的时间导数，允许为实数标量或向量。详细计算公式为：
$$
y =\frac{du}{dt} =\frac{u-u_T}{t-t_T}
$$

其中 t 是当前输出时间，T 是上次主时间步时间。

**数据类型：** double

</div>
</div>



## 参数

无

## 版本历史记录

- 在 2025a 推出

### 限制信息

- 输入信号仅支持 double 类型；
- 不支持在触发子系统，离散的 if/switch-case 子系统中使用；
- 不支持嵌入式代码生成。

