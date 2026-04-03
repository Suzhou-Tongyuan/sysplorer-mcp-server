# SpectrumAnalyzer
---
&nbsp;

显示频谱。

- **库:**  TYDSPSystem / SignalGenerationManipulationAndAnalysis / ScopeAndDataLogging 

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYDSPSystem/SignalGeneration/Scope/SpectrumAnalyzer/1.png')" style="width: 100px; border:black 1px solid;height: auto; transform: scale(1);">

## 描述

SpectrumAnalyzer 模块可用于显示信号的频谱。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYDSPSystem/SignalGeneration/Scope/SpectrumAnalyzer/2.png')" style="width:700px;border:black 1px solid;"> 

支持在普通或快速仿真模式下运行的模型中使用的 SpectrumAnalyzer 模块，同时支持在子系统中使用 SpectrumAnalyzer 模块。

SpectrumAnalyzer 模块有一个输入端口，可实时绘制一个实数输入信号的频谱，该模块接受实数标量或向量输入信号。


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

输入信号，指定为实数标量或向量。

**数据类型：** double 

</div>
</div>


## 参数

### 属性配置面板 -> 显示

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
<summary>显示网格 — 显示绘图网格线<div>on（默认）| off</div></summary>
</details>
<div class="details-content">

选择此选项显示绘图网格线。

</div>
</div>

<div class="details-box">
<details open>
<summary>Y 轴界限（最小） — 最小 Y 轴界限值<div>-80（默认）| 实数标量</div></summary>
</details>
<div class="details-content">

最小 Y 轴界限值，指定为实数标量。

</div>
</div>

<div class="details-box">
<details open>
<summary>Y 轴界限（最大） — 最大 Y 轴界限值<div>20（默认）| 实数标量</div></summary>
</details>
<div class="details-content">

最大 Y 轴界限值，指定为实数标量。

</div>
</div>

<div class="details-box">
<details open>
<summary>Y 轴标签 — 指定 Y 轴标签<div>""（默认）| 字符串</div></summary>
</details>
<div class="details-content">

Y 轴标签，指定为中英文字符串。

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

### 频谱设置 -> 主选项

<div class="details-box">
<details open>
<summary>输入域 — 指定信号输入域<div>时域（默认）| 频域</div></summary>
</details>
<div class="details-content">

指定可视化的输入信号的定义域。如果输入时域信号，则根据**类型**参数指定的算法将信号转换为频谱。

</div>
</div>

<div class="details-box">
<details open>
<summary>类型 — 指定计算时域信号的频谱类型<div>Power（默认）| Power density</div></summary>
</details>
<div class="details-content">

指定计算时域信号的频谱类型，可选项为 Power、Power density。仅当**输入域**参数设置为**时域**时该参数可用。

- Power -- 显示功率谱；

- Power density -- 显示功率谱密度，功率谱密度是频谱归一化到带宽为 1 赫兹的幅度。

</div>
</div>

<div class="details-box">
<details open>
<summary>抽样频率（Hz） — 设置信号的采样频率<div>44100（默认）| 正实数标量</div></summary>
</details>
<div class="details-content">

设置信号的采样频率，指定为正实数标量。

</div>
</div>

<div class="details-box">
<details open>
<summary>方法 — 指定频谱估计算法<div>Welch（默认）</div></summary>
</details>
<div class="details-content">

指定频谱估计算法，当前仅支持 Welch 方法。仅当**输入域**参数设置为**时域**时该参数可用。

</div>
</div>

<div class="details-box">
<details open>
<summary>窗长度 — 指定频谱估计时的窗长度<div>1024（默认）| 大于 2 的整数标量</div></summary>
</details>
<div class="details-content">

指定频谱估计时的窗长度，用来控制频率分辨率和计算频谱估计。窗长度必须是大于 2 的整数。仅当**输入域**参数设置为**时域**时该参数可用。

</div>
</div>

<div class="details-box">
<details open>
<summary>NFFT 来源 — 指定 FFT 点数来源<div>Auto（默认）| Property</div></summary>
</details>
<div class="details-content">

指定 NFFT 来源，可选项为 Auto、Property。

- Auto -- 指定为 Auto 时，自动将**窗长度** 指定为 FFT 点数；

- Property -- 指定为 Property 时，将通过 **NFFT** 参数指定 FFT 点数。

</div>
</div>

<div class="details-box">
<details open>
<summary>NFFT — 指定 FFT 点数<div>1024（默认）| 正整数</div></summary>
</details>
<div class="details-content">

指定用于计算频谱估计的 FFT 的点数，指定为正整数。**NFFT** 值必须大于或等于**窗长度**参数的值。当该参数设置为正整数时，该参数相当于 fft 函数的 n 参数。当且仅当 **NFFT 来源**被设置为 Auto 时会启用该选项。

</div>
</div>

### 频谱设置 -> 窗选项

<div class="details-box">
<details open>
<summary>重叠（%） — 指定分段重叠率<div>0（默认）| 0 ~ 100 之间的实数标量</div></summary>
</details>
<div class="details-content">

指定之前和当前缓冲数据段之间的重叠量。重叠创建了一个窗口段，用于计算频谱谱估计。指定为大于等于 0 且小于 100 的标量。

</div>
</div>

<div class="details-box">
<details open>
<summary>窗 — 指定加窗方法<div>Hann （默认） | Rectangular | Chebyshev | Flat Top | Hamming | Kaiser | Blackman-Harris</div></summary>
</details>
<div class="details-content">

指定加窗方法。加窗是用来控制频谱估计中旁瓣的影响。可选项有 Hann、Rectangular、Chebyshev、Flat Top、Hamming、Kaiser、Blackman-Harris。

</div>
</div>

<div class="details-box">
<details open>
<summary>旁瓣衰减 — 指定旁瓣衰减<div>60 （默认） | 大于等于 45 的实数标量</div></summary>
</details>
<div class="details-content">

以 dB 为单位设置旁瓣衰减，指定为大于等于 45 的实数标量。

</div>
</div>

### 频谱设置 -> 频率输入选项

<div class="details-box">
<details open>
<summary>输入单位 — 指定频谱单位<div>dBm（默认）| dBV | dBW | Vrms | Watts</div></summary>
</details>
<div class="details-content">

指定频谱输入信号的单位，默认为 dBm。当且仅当**输入域**被设置为频域时会启用该选项。

</div>
</div>

### 频谱设置 -> 轨迹选项

<div class="details-box">
<details open>
<summary>单位 — 指定频谱单位<div>dBm（默认）| dBW | Watts 或者其他单位</div></summary>
</details>
<div class="details-content">

指定频谱的单位。可用的值取决于**输入域**和**类型**参数的设置值。

当**输入域**被设置为时域，且**类型**被设置为 Power 时，可以选择输入 dBm ，dBW 或 Watts。

当**输入域**被设置为时域，且**类型**被设置为 Power density 时，可以选择输入 dBm/Hz ，dBW/Hz 或 Watts/Hz。

当**输入域**被设置为频域时，可以选择输入 Auto ， dBm ， dBV ， dBW ， Vrms 或 Watts。当选择输入 Auto 时，频谱显示单位将与频率输入选项中的**输入单位**参数一致。

</div>
</div>

<div class="details-box">
<details open>
<summary>参考负载 — 指定参考负载<div>1（默认） | 正实数标量</div></summary>
</details>
<div class="details-content">

以欧姆为单位的参考负载。

</div>
</div>

<div class="details-box">
<details open>
<summary>双边带频谱 — 控制是否显示双边带频谱<div>2（默认） | 正实数标量</div></summary>
</details>
<div class="details-content">

选中此复选框可启用双边带频谱视图。在双边带频谱视图中，显示了负频率和正频率。如果不选中复选框，频谱分析仪将显示只有正频率的单侧频谱。

</div>
</div>

### 频谱绘图样式面板

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
<summary>绘图种类 — 指定绘图种类<div>Line（默认）| Stem</div></summary>
</details>
<div class="details-content">

指定是显示线图或针状图。

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
<summary>线条 — 指定线图类型、颜色和线宽<div></div></summary>
</details>
<div class="details-content">

指定线图类型、颜色和线宽。

</div>
</div>

<div class="details-box">
<details open>
<summary>标记 — 指定标记样式<div></div></summary>
</details>
<div class="details-content">

指定标记样式。

</div>
</div>

### 菜单栏 -> 文件

<div class="details-box">
<details open>
<summary>关闭 — 关频谱分析仪界面<div></div></summary>
</details>
<div class="details-content">

关闭频谱分析仪界面按钮。

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
<summary>配置属性 — 打开属性配置面板<div></div></summary>
</details>
<div class="details-content">

打开属性配置面板（模态窗口）。

</div>
</div>

<div class="details-box">
<details open>
<summary>格式 — 打开绘图格式设置面板<div></div></summary>
</details>
<div class="details-content">

打开绘图格式设置面板（模态窗口）。

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
<summary>配置属性 — 打开属性配置面板<div></div></summary>
</details>
<div class="details-content">

打开属性配置面板（模态窗口）。

</div>
</div>

<div class="details-box">
<details open>
<summary>格式 — 打开绘图格式设置面板<div></div></summary>
</details>
<div class="details-content">

打开绘图格式设置面板（模态窗口）。

</div>
</div>

<div class="details-box">
<details open>
<summary>仿真 — 触发仿真按钮<div></div></summary>
</details>
<div class="details-content">

触发执行仿真。

</div>
</div>

<div class="details-box">
<details open>
<summary>停止 — 停止仿真<div></div></summary>
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
<summary>频谱设置 — 显示频谱设置侧边栏<div>on（默认）| off</div></summary>
</details>
<div class="details-content">

选择显示频谱设置侧边栏。

</div>
</div>


## 版本历史记录

- 在 2025b 推出

## 限制信息

- 该模块暂不支持自动识别输入信号维度，需通过**输入信号维度**参数手动设定。
