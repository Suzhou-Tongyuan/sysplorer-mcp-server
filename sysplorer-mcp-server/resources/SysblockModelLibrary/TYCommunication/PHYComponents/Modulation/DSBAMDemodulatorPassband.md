# DSBAMDemodulatorPassband
---
解调 DSB AM 调制数据

**库：** TYCommunication / PHYComponents / Modulation

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYCommunication/PHYComponents/Modulation/DSBAMDemodulatorPassband/1.png')" style="width: 150px; height: auto; transform: scale(1);">

## 描述

DSBAMDemodulatorPassband 模块对使用双边带调幅调制的信号进行解调。该模块使用包络检测方法。输入是调制信号的通带表示。输入和输出信号都是实标量信号。

在解调过程中，该模块使用一个滤波器，其阶数、系数、通带纹波和阻带纹波由其各自的低通滤波器参数描述。

通常，适当的载波频率值远高于输入信号的最高频率。根据奈奎斯特采样定理，模型采样时间的倒数（由模型的信号源定义）必须超过载波频率参数的两倍。此块仅适用于 double 类型的实际输入。

此块在触发的子系统内不起作用。

## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>实数标量</div></summary>
</details>
<div class="details-content">

输入信号，指定为一个实数标量值。

**数据类型：** double

</div>
</div>



### 输出

<div class="details-box">
<details open>
<summary>y — 输出相位调制后的信号<div>实数标量</div></summary>
</details>
<div class="details-content">
 
输出相位调制后的信号。

**数据类型：** double

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>输入信号延迟 — 输入信号的偏移量<div>1 （默认） | 正整数</div></summary>
</details>
<div class="details-content">

与对应的 DSBAMModulatorPassband 模块中的输入信号延迟参数相同。

</div>
</div>

<div class="details-box">
<details open>
<summary>载波频率(Hz) — 输入信号的载波频率<div>300 （默认） | 正实数</div></summary>
</details>
<div class="details-content">

与对应的 DSBAMModulatorPassband 模块中的载波频率参数相同

</div>
</div>

<div class="details-box">
<details open>
<summary>初始相位 (rad) — 载波的初始相位<div>0 （默认） | 实数</div></summary>
</details>
<div class="details-content">

载波的初始相位，单位为弧度。

</div>
</div>

<div class="details-box">
<details open>
<summary>低通滤波器设计思路 — 采用的低通滤波器设计方法<div>Butterworth （默认） | Chebyshev I | Chebyshev II | Elliptic</div></summary>
</details>
<div class="details-content">

用于生成过滤器的方法。可用的方法有巴特沃斯法、切比雪夫 I 型法、切比雪夫 II 型法和椭圆法。

</div>
</div>

<div class="details-box">
<details open>
<summary>滤波器阶数 — 采用的滤波器阶数<div>4 （默认） | 正整数</div></summary>
</details>
<div class="details-content">

低通滤波器设计方法字段中指定的低通数字滤波器的阶数。

</div>
</div>

<div class="details-box">
<details open>
<summary>截止频率(Hz) — 低通数字滤波器的截止频率<div>300 （默认） | 正实数</div></summary>
</details>
<div class="details-content">

低通滤波器设计方法字段中指定的低通数字滤波器的截止频率，单位为赫兹。

</div>
</div>

<div class="details-box">
<details open>
<summary>通带波纹(dB) — 通带中的峰间波纹<div>0.1 （默认） | 实数</div></summary>
</details>
<div class="details-content">

仅适用于切比雪夫 I 型和椭圆滤波器。这是通带中的峰间波纹，单位为 dB 。

</div>
</div>

<div class="details-box">
<details open>
<summary>阻带衰减(dB) — 阻带中的峰间波纹<div>50 （默认） | 实数</div></summary>
</details>
<div class="details-content">

仅适用于切比雪夫 II 型和椭圆滤波器。这是阻带中的峰间波纹，单位为 dB 。

</div>
</div>

## 版本历史记录

- 在 2026b 推出


