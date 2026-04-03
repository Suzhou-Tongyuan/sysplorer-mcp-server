# ColoredNoise
---

根据用户定义的功率谱密度对噪声源进行建模。

**库：** TYMixedSignal / SDUtilities

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYMixedSignal/SDUtilities/ColoredNoise/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

ColoredNoise 模块用于建模具有用户定义功率谱密度（PSD）的噪声源。

电路输出噪声（如运算放大器噪声）由于滤波效应和闪烁噪声（1/f 噪声）的影响，通常无法视为白噪声。但由于采样过程的存在，高于采样频率（fs）的频谱成分会被折叠回[0, fs]频段。根据闪烁噪声强度、采样频率、带宽（即过采样率）以及采样频率与系统主极点频率的比值，采样操作可能足以使噪声白化。若白噪声近似成立，可使用白噪声源建模开关电容（SC）Σ-Δ调制器中主动模块的噪声。
 
若白噪声近似不成立（如窄带低通 Σ-Δ 调制器），则需采用更精确的模型。
 
大多数晶体管级仿真器提供的噪声功率谱密度（PSD，单位：V²/Hz）可视为多个任意相位正弦波的叠加（根据傅里叶定理），每个正弦波的功率等于PSD曲线上对应频率段的面积（频段宽度为 $f_{MAX}/N$，即频率分辨率）。
 
此简单原理构成了有色噪声模型的基础。具体实现为：
 - 仿真数据重构：对晶体管级仿真器（如Cadence Ocean命令）生成的波形进行采样，并在重构 PSD 函数。
 - 解析建模：基于对噪声 PSD 形状的先验知识进行建模。由于噪声功率具有叠加性，PSD 可分解为闪烁噪声项和经电路传递函数低通滤波后的热噪声项之和。
 
通过提供两个特征点：拐角频率 $(f_{C}, y_{C})$ 和极点频率 $(f_{P}, y_{P})$，可估计参数 $k_{1}$ 和 $c$。

 
获得解析 PSD 函数后，可定义其傅里叶级数。为降低模型复杂度，在初始化阶段计算采样对噪声谱的影响，定义 [0, fs/2] 频段内的等效包络。此方法可减少所需正弦波数量，或在相同正弦波数量下提升频率分辨率。
 
该模型可集成电路仿真数据，因此可用于评估自零（Auto-Zero）或相关双采样（CDS）等技术对 Σ-Δ 调制器整体性能的影响。只需在噪声模型输出端连接对应的 z 域传递函数即可实现。


## 端口


### 输出

<div class="details-box">
<details open>
<summary>y — 输出有色噪声信号<div>实数标量</div></summary>
</details>
<div class="details-content">
 
根据设置参数输出有色噪声信号。

**数据类型：** double

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>正弦波数量 — 正弦波数量<div> 正整数标量 </div></summary>
</details>
<div class="details-content">

用于近似目标噪声功率谱密度的正弦波数量。

</div>
</div>


<div class="details-box">
<details open>
<summary>折叠次数 — 折叠次数<div> 正整数标量 </div></summary>
</details>
<div class="details-content">

原始噪声 PSD 被折叠的次数。


</div>
</div>


<div class="details-box">
<details open>
<summary>采样频率 — 采样频率<div> 正实数标量 </div></summary>
</details>
<div class="details-content">

采样信号频率（fs = 1/Ts，Ts 为采样周期）

</div>
</div>


<div class="details-box">
<details open>
<summary>第一拐角频率 — 第一拐角频率<div> 正实数标量 </div></summary>
</details>
<div class="details-content">

目标 PSD 第一拐角频率 ${f_{C}$。

</div>
</div>


<div class="details-box">
<details open>
<summary>第一拐角 PSD — 第一拐角 PSD<div> 正实数标量 </div></summary>
</details>
<div class="details-content">

目标 PSD 第一拐角处 PSD 值 $y_{C}$。

</div>
</div>

<div class="details-box">
<details open>
<summary>第二拐角频率 — 第二拐角频率<div> 正实数标量 </div></summary>
</details>
<div class="details-content">

目标 PSD 第二拐角频率 $f_{P}$。

</div>
</div>


<div class="details-box">
<details open>
<summary>第二拐角 PSD — 第二拐角 PSD<div> 正实数标量 </div></summary>
</details>
<div class="details-content">

目标 PSD 第二拐角处 PSD 值 $y_{P}$。

</div>
</div>

<div class="details-box">
<details open>
<summary>随机数种子 — 随机数种子<div> 整数标量 </div></summary>
</details>
<div class="details-content">

随机数生成器种子（不同种子保证不同模块的随机序列无相关性）。

</div>
</div>

## 版本历史记录

- 在 2025b 推出
