# ConstellationDiagram
---
显示输入信号的星座图。

- **库:**  TYCommunication / PHYComponents / SourcesAndSinks

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYCommunication/PHYComponents/SourcesAndSinks/ConstellationDiagram/1.png')" style="width: 100px; border:black 1px solid;height: auto; transform: scale(1);">

## 描述

星座图模块在 I/Q 平面上显示输入信号的星座图，可使用该模块对调制的单载波信号进行定性和定量分析。

星座图模块有一个输入端口，可绘制一个复数输入信号的星座图，并可为输入信号定义参考星座。该模块接受复数标量或向量输入信号。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYCommunication/PHYComponents/SourcesAndSinks/ConstellationDiagram/2.png')" style="width:700px;border:black 1px solid;"> 


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

输入信号，指定为复数标量或向量。

**数据类型：** double 

</div>
</div>


## 参数

### 配置属性面板 -> 主要

<div class="details-box">
<details open>
<summary>每符号采样数 — 指定每个符号的样本数<div>1（默认）| 正整数标量 </div></summary>
</details>
<div class="details-content">

用于表示每个符号的样本数，指定为正整数。当**每符号采样数**大于 1 时，信号在绘制之前被下采样。

</div>
</div>

<div class="details-box">
<details open>
<summary>偏移（采样） — 指定在绘制星座点之前要跳过的样本数<div>0（默认）| 非负整数标量</div></summary>
</details>
<div class="details-content">

在绘制星座点之前要跳过的样本数，指定为小于**每符号采样数**的非负整数。

</div>
</div>

<div class="details-box">
<details open>
<summary>符号源 — 指定符号源<div>输入帧长度（默认）| 用户自定义</div></summary>
</details>
<div class="details-content">

指定符号源，默认选择**输入帧长度**，可选项为**输入帧长度**和**用户自定义**。

- 输入帧长度 —— 指定为该选项时，显示符号的最大数目为输入帧长度；

- 用户自定义 —— 指定为该选项时，通过**显示符号数**设置显示符号的最大数目。

</div>
</div>

<div class="details-box">
<details open>
<summary>显示符号数 — 指定显示符号数<div>256（默认）| 正整数标量</div></summary>
</details>
<div class="details-content">

指定显示的符号的最大数目，指定为正整数标量。当**符号源**选择为**用户自定义**时，该参数可用。

</div>
</div>

<div class="details-box">
<details open>
<summary>输入信号维度 — 指定输入信号维度<div>{1}（默认）| 长度为 1 的整型向量</div></summary>
</details>
<div class="details-content">

指定输入信号的维度。指定为长度为 1 的整型向量。特别地，{1} 可以兼容表示标量或长度为 1 的向量。

</div>
</div>

### 配置属性面板 -> 显示

<div class="details-box">
<details open>
<summary>显示网格 — 显示绘图网格线<div>on（默认）| off</div></summary>
</details>
<div class="details-content">

选择此选项显示绘图网格线。

</div>
</div>

<div class="details-box">
<details open>
<summary>显示信号轨迹 — 显示信号轨迹<div>on（默认）| off</div></summary>
</details>
<div class="details-content">

选择显示绘制信号星座点之间的轨迹。

</div>
</div>

<div class="details-box">
<details open>
<summary>X 轴界限（最小） — 最小 X 轴界限值<div>-1.375（默认）| 实数标量</div></summary>
</details>
<div class="details-content">

最小 X 轴界限值，指定为实数标量。

</div>
</div>

<div class="details-box">
<details open>
<summary>X 轴界限（最大） — 最大 X 轴界限值<div>1.375（默认）| 实数标量</div></summary>
</details>
<div class="details-content">

最大 X 轴界限值，指定为实数标量。

</div>
</div>

<div class="details-box">
<details open>
<summary>Y 轴界限（最小） — 最小 Y 轴界限值<div>-1.375（默认）| 实数标量</div></summary>
</details>
<div class="details-content">

最小 Y 轴界限值，指定为实数标量。

</div>
</div>

<div class="details-box">
<details open>
<summary>Y 轴界限（最大） — 最大 Y 轴界限值<div>1.375（默认）| 实数标量</div></summary>
</details>
<div class="details-content">

最大 Y 轴界限值，指定为实数标量。

</div>
</div>

<div class="details-box">
<details open>
<summary>标题 — 指定绘图标题<div>""（默认）| 字符串</div></summary>
</details>
<div class="details-content">

绘图标题，指定为中英文字符串。

</div>
</div>

<div class="details-box">
<details open>
<summary>X 轴标签 — 指定 X 轴标签<div>"In-phase Amplitude"（默认）| 字符串</div></summary>
</details>
<div class="details-content">

X 轴标签，指定为中英文字符串。

</div>
</div>

<div class="details-box">
<details open>
<summary>Y 轴标签 — 指定 Y 轴标签<div>"Quadrature Amplitude"（默认）| 字符串</div></summary>
</details>
<div class="details-content">

Y 轴标签，指定为中英文字符串。

</div>
</div>

### 配置属性面板 -> 参考

<div class="details-box">
<details open>
<summary>显示参考星座 — 显示参考星座<div>on（默认）| off</div></summary>
</details>
<div class="details-content">

选择显示参考星座。

</div>
</div>

<div class="details-box">
<details open>
<summary>参考星座 — 指定参考星座类型<div>QPSK（默认） | BPSK | 8-PSK | 16-QAM | 64-QAM | 256-QAM</div></summary>
</details>
<div class="details-content">

参考星座类型，可指定为 BPSK、QPSK、8-PSK、16-QAM、64-QAM、256-QAM。

</div>
</div>

<div class="details-box">
<details open>
<summary>星座标准化 — 指定星座标准化类型<div>最小距离 （默认） | 平均功率 | 峰值功率</div></summary>
</details>
<div class="details-content">

星座标准化类型，可指定为最小距离、平均功率、峰值功率。当**参考星座**设置为 16-QAM、64-QAM、256-QAM 时该参数可用。

</div>
</div>

<div class="details-box">
<details open>
<summary>参考最小距离 — 指定参考最小距离<div>2（默认） | 正实数标量</div></summary>
</details>
<div class="details-content">

参考最小距离，指定为正实数标量。当**参考星座**设置为 16-QAM、64-QAM、256-QAM 且 **星座标准化**设置为时**最小距离**时该参数可用。

</div>
</div>

<div class="details-box">
<details open>
<summary>平均参考功率 — 指定平均参考功率<div>1（默认） | 正实数标量</div></summary>
</details>
<div class="details-content">

平均参考功率，指定为正实数标量。当**参考星座**设置为 BPSK、QPSK、8-PSK 或 **参考星座**设置为 16-QAM、64-QAM、256-QAM 且 **星座标准化**设置为时**平均功率**时该参数可用。

</div>
</div>

<div class="details-box">
<details open>
<summary>峰值参考功率 — 指定峰值参考功率<div>1（默认） | 正实数标量</div></summary>
</details>
<div class="details-content">

峰值参考功率，指定为正实数标量。当**参考星座**设置为 16-QAM、64-QAM、256-QAM 且 **星座标准化**设置为时**峰值功率**时该参数可用。

</div>
</div>

<div class="details-box">
<details open>
<summary>参考相位偏移 — 指定参考相位偏移<div>0（默认） | 实数标量</div></summary>
</details>
<div class="details-content">

参考相位偏移，指定为实数标量。

</div>
</div>

### 星座图样式面板

<div class="details-box">
<details open>
<summary>图窗颜色 — 指定图窗背景颜色<div>黑色（默认）</div></summary>
</details>
<div class="details-content">

在星座图窗内和范围轴外选择背景颜色。

</div>
</div>

<div class="details-box">
<details open>
<summary>坐标区颜色 — 选择绘图区域和坐标区辅助线的颜色<div>黑色（默认背景颜色）| 浅灰色（默认辅助线颜色）</div></summary>
</details>
<div class="details-content">

选择绘图区域和坐标区辅助线的颜色。第一个颜色选项指定绘图区域的背景颜色。第二个选项指定绘图图轴（刻度、标签和网格线）和文本的颜色。

</div>
</div>

<div class="details-box">
<details open>
<summary>显示信号和参考星座 — 显示信号和参考星座<div>on（默认）| off</div></summary>
</details>
<div class="details-content">

选择显示信号和参考星座。

</div>
</div>

<div class="details-box">
<details open>
<summary>符号 — 指定信号符号标记样式、大小、线宽和颜色<div></div></summary>
</details>
<div class="details-content">

指定信号符号标记的样式、大小、线宽和颜色。

</div>
</div>

<div class="details-box">
<details open>
<summary>信号轨迹 — 指定信号轨迹样式、线宽和颜色<div></div></summary>
</details>
<div class="details-content">

指定信号轨迹线的样式、线宽和颜色。当**显示信号轨迹**复选框处于选中状态时，该选项可配置。

</div>
</div>

<div class="details-box">
<details open>
<summary>参考星座 — 指定参考符号标记样式、大小、线宽和颜色<div></div></summary>
</details>
<div class="details-content">

指定参考符号标记的样式、大小、线宽和颜色。

</div>
</div>


### 菜单栏 -> 文件

<div class="details-box">
<details open>
<summary>关闭 — 关闭星座图界面<div></div></summary>
</details>
<div class="details-content">

关闭星座图界面按钮。

</div>
</div>

### 菜单栏 -> 工具

<div class="details-box">
<details open>
<summary>平移 — 选择平移状态<div></div></summary>
</details>
<div class="details-content">

选择平移状态，处于选中状态时可通过长按鼠标左键平移绘图。与**缩放**选中状态互斥。

</div>
</div>

<div class="details-box">
<details open>
<summary>缩放 — 选择缩放状态<div></div></summary>
</details>
<div class="details-content">

选择缩放状态，处于选中状态时可通过框选缩放绘图。与**平移**选中状态互斥。

</div>
</div>

<div class="details-box">
<details open>
<summary>还原默认视图 — 还原默认视图<div></div></summary>
</details>
<div class="details-content">

单击还原默认视图。

</div>
</div>

### 菜单栏 -> 视图

<div class="details-box">
<details open>
<summary>配置属性 — 打开配置属性面板<div></div></summary>
</details>
<div class="details-content">

打开配置属性面板（模态窗口）。

</div>
</div>

<div class="details-box">
<details open>
<summary>样式 — 打开星座图样式面板<div></div></summary>
</details>
<div class="details-content">

打开星座图样式面板（模态窗口）。

</div>
</div>

<div class="details-box">
<details open>
<summary>工具栏 — 控制工具栏显示状态<div></div></summary>
</details>
<div class="details-content">

控制工具栏显示状态。

</div>
</div>

<div class="details-box">
<details open>
<summary>状态栏 — 控制状态栏显示状态<div></div></summary>
</details>
<div class="details-content">

控制状态栏显示状态。

</div>
</div>

### 工具栏

<div class="details-box">
<details open>
<summary>配置属性 — 打开配置属性面板<div></div></summary>
</details>
<div class="details-content">

打开配置属性面板（模态窗口）。

</div>
</div>

<div class="details-box">
<details open>
<summary>样式 — 打开星座图样式面板<div></div></summary>
</details>
<div class="details-content">

打开星座图样式面板（模态窗口）。

</div>
</div>

<div class="details-box">
<details open>
<summary>执行仿真 — 触发仿真按钮<div></div></summary>
</details>
<div class="details-content">

触发执行仿真。

</div>
</div>

<div class="details-box">
<details open>
<summary>停止仿真 — 停止仿真<div></div></summary>
</details>
<div class="details-content">

触发停止仿真。

</div>
</div>

<div class="details-box">
<details open>
<summary>平移 — 选择平移状态<div></div></summary>
</details>
<div class="details-content">

选择平移状态，处于选中状态时可通过长按鼠标左键平移绘图。与**缩放**选中状态互斥。

</div>
</div>

<div class="details-box">
<details open>
<summary>缩放 — 选择缩放状态<div></div></summary>
</details>
<div class="details-content">

选择缩放状态，处于选中状态时可通过框选缩放绘图。与**平移**选中状态互斥。

</div>
</div>

<div class="details-box">
<details open>
<summary>还原默认视图 — 还原默认视图<div></div></summary>
</details>
<div class="details-content">

单击还原默认视图。

</div>
</div>

<div class="details-box">
<details open>
<summary>显示信号轨迹 — 显示信号轨迹<div>on（默认）| off</div></summary>
</details>
<div class="details-content">

选择显示绘制信号星座点之间的轨迹。

</div>
</div>


## 版本历史记录

- 在 2025b 推出

### 限制信息

- 该模块暂不支持自动识别输入信号维度，需通过**输入信号维度**参数手动设定
