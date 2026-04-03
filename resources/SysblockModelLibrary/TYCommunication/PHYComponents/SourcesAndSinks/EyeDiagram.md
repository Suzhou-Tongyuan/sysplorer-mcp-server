# EyeDiagram
---
显示时域信号的眼图。

- **库:**  TYCommunication / PHYComponents / SourcesAndSinks

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYCommunication/PHYComponents/SourcesAndSinks/EyeDiagram/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

眼图模块显示调制信号的多条轨迹，从而生成眼图。您可以使用该模块来揭示信号的调制特性，例如脉冲整形或信道失真的影响。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYCommunication/PHYComponents/SourcesAndSinks/EyeDiagram/2.png')" style="width:700px;border:black 1px solid;"> 

眼图模块有一个输入端口。该模块接受列向量或标量输入信号。目前该模块仅能接受复数类型的输入信号。


## 端口

### 输入

<div id="u—信号输入" class="jump-target"></div>
<div class="details-box">
<details open>
<summary>u — 信号输入<div>标量 | 向量 </div></summary>
</details>
<div class="details-content">

输入数据信号，指定为标量或向量形式，输入数据类型限定为复数。

**数据类型：** complexf64

</div>
</div>

## 参数

### 属性配置面板

##### 主要

<div id="显示模式—指定眼图显示的模式" class="jump-target"></div>
<div class="details-box">
<details open>
<summary>显示模式 — 指定眼图显示的模式<div>线图（默认）| 二维颜色直方图 </div></summary>
</details>
<div class="details-content">

眼图显示的模式，可指定为以下选项之一：

- 线图 —— 使用线图显示眼图；

- 二维颜色直方图 —— 使用二维颜色直方图绘制眼图。

</div>
</div>

<div id="开启测量—是否启动测量面板" class="jump-target"></div>
<div class="details-box">
<details open>
<summary>开启测量 — 是否启动测量面板<div>off（默认）| on </div></summary>
</details>
<div class="details-content">

指定是否启动测量面板的参数。

</div>
</div>

<div id="显示眼图—眼图显示的轴类型" class="jump-target"></div>
<div class="details-box">
<details open>
<summary>显示眼图 — 眼图显示的轴类型<div>只显示实轴（默认）| 实轴和虚轴都显示</div></summary>
</details>
<div class="details-content">

眼图显示的轴类型，可指定为以下选项之一：

- 只显示实轴 —— 只显示输入信号眼图的实轴部分；

- 实轴和虚轴都显示 —— 同时显示输入信号眼图的实轴和虚轴部分。

**依赖关系：**

要选择“实轴和虚轴都显示”选项，需关闭“开启测量”。

</div>
</div>


<div id="每符号抽样数—指定每个符号内的样本数量" class="jump-target"></div>
<div class="details-box">
<details open>
<summary>每符号抽样数 — 指定每个符号内的样本数量<div>8（默认）| 正整数</div></summary>
</details>
<div class="details-content">

每个符号内的样本数量，指定为正整数。

</div>
</div>


<div id="抽样延迟—指定输入信号的抽样延迟" class="jump-target"></div>
<div class="details-box">
<details open>
<summary>抽样延迟 — 指定输入信号的抽样延迟<div>0（默认）| 非负整数</div></summary>
</details>
<div class="details-content">

输入信号的抽样延迟，指定为非负整数。

</div>
</div>


<div id="每条轨迹符号数—指定眼图显示的符号数" class="jump-target"></div>
<div class="details-box">
<details open>
<summary>每条轨迹符号数 — 指定眼图显示的符号数<div>2（默认）| 正整数</div></summary>
</details>
<div class="details-content">

眼图显示的符号数，指定为正整数。

**依赖关系：**
当选择“开启测量”时，需要将该项设置为 2。

</div>
</div>


<div id="显示轨迹数—指定线图显示的轨迹数" class="jump-target"></div>
<div class="details-box">
<details open>
<summary>显示轨迹数 — 指定线图显示的轨迹数<div>40（默认）| 正整数</div></summary>
</details>
<div class="details-content">

线图显示的轨迹数，指定为正整数。

**依赖关系：**
要设置该项，需要将“显示模式”设置为“线图”。

</div>
</div>


<div id="抽样频率—指定输入信号的抽样频率" class="jump-target"></div>
<div class="details-box">
<details open>
<summary>抽样频率 — 指定输入信号的抽样频率<div>1.0（默认）| 正实数</div></summary>
</details>
<div class="details-content">

输入信号的抽样频率，指定为正实数。

</div>
</div>


<div id="输入信号维度—指定输入信号的长度" class="jump-target"></div>
<div class="details-box">
<details open>
<summary>输入信号维度 — 指定输入信号的长度<div>{1}（默认）| 长度为 1 的整型向量</div></summary>
</details>
<div class="details-content">

输入信号的长度，指定为长度为1的正整数向量。

</div>
</div>


##### 坐标轴

<div id="标题—眼图标题" class="jump-target"></div>
<div class="details-box">
<details open>
<summary>标题 — 眼图标题<div>（默认为空）| 字符串</div></summary>
</details>
<div class="details-content">

眼图的标题，指定为字符串。

</div>
</div>


<div id="显示网格—是否显示网格" class="jump-target"></div>
<div class="details-box">
<details open>
<summary>显示网格 — 是否显示网格<div>off（默认）| on</div></summary>
</details>
<div class="details-content">

指定是否在眼图中显示网格的参数。

</div>
</div>


<div id="Y 轴界限（最小值）—Y 轴范围的最小值" class="jump-target"></div>
<div class="details-box">
<details open>
<summary>Y 轴界限（最小值） — Y 轴范围的最小值<div>-1.1（默认）| 双精度标量</div></summary>
</details>
<div class="details-content">

Y 轴显示范围的最小值，指定为双精度标量。

</div>
</div>


<div id="Y 轴界限（最大值）—Y 轴范围的最大值" class="jump-target"></div>
<div class="details-box">
<details open>
<summary>Y 轴界限（最大值） — Y 轴范围的最大值<div>1.1（默认）| 双精度标量</div></summary>
</details>
<div class="details-content">

Y 轴显示范围的最大值，指定为双精度标量。

</div>
</div>


<div id="实轴标签—实轴显示的标签" class="jump-target"></div>
<div class="details-box">
<details open>
<summary>实轴标签 — 实轴显示的标签<div>Real Amplitude（默认）| 字符串</div></summary>
</details>
<div class="details-content">

实轴显示的标签，指定为字符串。

</div>
</div>


<div id="虚轴标签—虚轴显示的标签" class="jump-target"></div>
<div class="details-box">
<details open>
<summary>虚轴标签 — 虚轴显示的标签<div>Imaginary Amplitude（默认）| 字符串</div></summary>
</details>
<div class="details-content">

虚轴显示的标签，指定为字符串。

</div>
</div>


##### 二维直方图

**依赖关系：**

该页面仅在“显示模式”被设置为“二维颜色直方图”时出现。

<div id="颜色标度—直方图的颜色标度" class="jump-target"></div>
<div class="details-box">
<details open>
<summary>颜色标度 — 直方图的颜色标度<div>线性（默认）| 对数</div></summary>
</details>
<div class="details-content">

直方图的颜色标度，指定为线性或对数。如果眼图的某些区域包含不成比例的点数，请将色标设置为对数。

</div>
</div>


### 绘图格式设置

<div id="背景颜色—眼图图窗的背景颜色" class="jump-target"></div>
<div class="details-box">
<details open>
<summary>背景颜色 — 眼图图窗的背景颜色<div>黑色（默认）| 其他颜色</div></summary>
</details>
<div class="details-content">

眼图图窗的背景颜色。

</div>
</div>


<div id="坐标区颜色（填充）—眼图坐标区填充的颜色" class="jump-target"></div>
<div class="details-box">
<details open>
<summary>坐标区颜色（填充） — 眼图坐标区填充的颜色<div>黑色（默认）| 其他颜色</div></summary>
</details>
<div class="details-content">

眼图坐标区填充的颜色。在**显示模式**被设置为**二维颜色直方图**时，该参数恒定为黑色。

</div>
</div>


<div id="坐标区颜色（线条）—眼图坐标区线条的颜色" class="jump-target"></div>
<div class="details-box">
<details open>
<summary>坐标区颜色（线条） — 眼图坐标区线条的颜色<div>白色（默认）| 其他颜色</div></summary>
</details>
<div class="details-content">

眼图坐标区线条的颜色。

</div>
</div>


<div id="线条（类型）—线图线条的类型" class="jump-target"></div>
<div class="details-box">
<details open>
<summary>线条（类型） — 线图线条的类型<div>直线（默认）| 其他类型</div></summary>
</details>
<div class="details-content">

线图线条的类型。

**依赖关系：**

要设置该项，需要将“显示模式”设置为“线图”。

</div>
</div>


<div id="线条（颜色）—线图线条的颜色" class="jump-target"></div>
<div class="details-box">
<details open>
<summary>线条（颜色） — 线图线条的颜色<div>黄色（默认）| 其他颜色</div></summary>
</details>
<div class="details-content">

线图线条的颜色。

**依赖关系：**

要设置该项，需要将“显示模式”设置为“线图”。

</div>
</div>


<div id="线条（宽度）—线图线条的宽度" class="jump-target"></div>
<div class="details-box">
<details open>
<summary>线条（宽度） — 线图线条的宽度<div>0.5（默认）| 不超过5的其他选项</div></summary>
</details>
<div class="details-content">

线图线条的宽度。

**依赖关系：**

要设置该项，需要将“显示模式”设置为“线图”。

</div>
</div>


<div id="标记—线图线条的标记点类型" class="jump-target"></div>
<div class="details-box">
<details open>
<summary>标记 — 线图线条的标记点类型<div>None（默认）| 其他类型</div></summary>
</details>
<div class="details-content">

线图线条的标记点类型。

**依赖关系：**

要设置该项，需要将“显示模式”设置为“线图”。

</div>
</div>


<div id="颜色图—二维颜色直方图的颜色图类型" class="jump-target"></div>
<div class="details-box">
<details open>
<summary>颜色图 — 二维颜色直方图的颜色图类型<div>hot（默认）| 其他类型</div></summary>
</details>
<div class="details-content">

二维颜色直方图的颜色图类型。

**依赖关系：**

要设置该项，需要将“显示模式”设置为“二维颜色直方图”。

</div>
</div>


### 测量

##### 设置

<div id="水平边界—计算眼图水平值的时间范围" class="jump-target"></div>
<div class="details-box">
<details open>
<summary>水平边界 — 计算眼图水平值的时间范围<div>{40, 60}（默认）| 长度为 2 的向量</div></summary>
</details>
<div class="details-content">

计算眼图水平值的时间范围，指定为长度为2的向量。这些值表示为符号持续时间的百分比。

</div>
</div>


<div id="判决边界—幅度水平阈值" class="jump-target"></div>
<div class="details-box">
<details open>
<summary>判决边界 — 幅度水平阈值<div>0（默认）| 正实数标量</div></summary>
</details>
<div class="details-content">

幅度电平阈值（以 V 为单位），指定为标量。此参数用于区分水平（抖动）直方图的不同信号区域。

对于非归零 (NRZ) 信号，将决策边界设置为 0。对于归零 (RZ) 信号，将决策边界设置为最大幅度的一半。

</div>
</div>


<div id="上升/下降阈值—上升沿和下降沿的幅度水平范围" class="jump-target"></div>
<div class="details-box">
<details open>
<summary>上升/下降阈值 — 上升沿和下降沿的幅度水平范围<div>{10, 90}（默认）| 长度为 2 的向量</div></summary>
</details>
<div class="details-content">

上升和下降跳变的幅度水平，指定为一个长度为2的向量。这些值表示为眼图幅度的百分比。

</div>
</div>


##### 幅值测量

<div id="眼高—眼图水平值间的统计最小距离" class="jump-target"></div>
<div class="details-box">
<details open>
<summary>眼高 — 眼图水平值间的统计最小距离<div></div></summary>
</details>
<div class="details-content">

眼高是眼图上平面 $μ – 3σ$ 与眼图下平面 $μ + 3σ$ 之间的距离。$μ$ 是眼图水平值的平均值，$σ$ 是标准差。

</div>
</div>


<div id="SNR—信噪比" class="jump-target"></div>
<div class="details-box">
<details open>
<summary>SNR — 信噪比<div></div></summary>
</details>
<div class="details-content">

眼部信噪比是眼部水平差与每个眼部水平对应的垂直标准差之差的比值：

$SNR = \frac{L_1 - L_0}{σ_1 - σ_0}$

其中 $L_1$ 和 $L_0$ 表示眼图上水平和下水平的均值，$σ_1$ 和 $σ_0$ 表示它们的标准差。

</div>
</div>


##### 时间测量

<div id="眼宽—眼图交叉值间的统计最小距离" class="jump-target"></div>
<div class="details-box">
<details open>
<summary>眼宽 — 眼图交叉值间的统计最小距离<div></div></summary>
</details>
<div class="details-content">

眼宽是左侧交叉时间的 $μ + 3σ$ 与右侧交叉时间的 $μ – 3σ$ 之间的水平距离。$μ$ 是抖动直方图的平均值，$σ$ 是标准差。

</div>
</div>


## 版本历史记录

- 在 2025b 推出

### 限制信息

- 该模块暂不支持自动识别输入信号维度，需通过**输入信号维度**参数手动设定