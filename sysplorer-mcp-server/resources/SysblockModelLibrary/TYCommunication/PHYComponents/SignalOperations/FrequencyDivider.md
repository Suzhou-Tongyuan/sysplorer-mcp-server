# FrequencyDivider
---
对输入信号进行分频操作。

**库：**  TYCommunication / PHYComponents / SignalOperation 

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYCommunication/PHYComponents/SignalOperations/FrequencyDivider/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

FrequencyDivider 模块用于将输入信号频率按比例降低，常用于时钟生成和频率匹配电路中。其原理通常是用计数器或触发器对输入脉冲进行计数后输出较低频率信号。


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入数据信号<div>标量</div></summary>
</details>
<div class="details-content">

输入信号，指定为标量。


**数据类型：** double 

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量</div></summary>
</details>
<div class="details-content">
 
输出信号，指定为标量，将输入信号的频率按一定比例降低，输出频率 = 输入频率 / N。

**数据类型：** double 

</div>
</div>


## 参数


<div class="details-box">
<details open>
<summary>分频倍数 — 分频倍数<div>1（默认）| 正整数</div></summary>
</details>
<div class="details-content">

分频系数是指分频器将输入频率降低的比例数。

**数据类型：** int32

</div>
</div>


## 版本历史记录

- 在 2025b 推出
