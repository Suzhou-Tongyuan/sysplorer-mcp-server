# Whitenoise
---

对具有白色功率谱密度的噪声源进行建模。

**库：** TYMixedSignal / SDUtilities

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYMixedSignal/SDUtilities/Whitenoise/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

Whitenoise 模块用于对具有白色功率谱密度的噪声源进行建模。

可以用一个具有标准差 $V_n$ 的高斯随机过程对白噪声源进行建模，该标准差 $V_n$ 也代表噪声的均方根值（即噪声功率 $V_n^2$ 的平方根）。

噪声功率 $V_n^2$ 可以通过对所考虑的完整开关电容电路（例如 Sigma-Delta 调制器的积分器）在合适的时钟相位下进行晶体管级噪声仿真来评估，仿真过程中需包含反馈、采样和负载电容。需要对所得的输出等效噪声功率谱密度在整个频谱上进行积分，最终需考虑由自动调零（auto-zero）或相关双采样（correlated double sampling）技术引入的热噪声功率谱密度的退化。如果 $1/f$ 噪声较为显著，则最好使用 ColoredNoise 模块。

在本模块中，仅考虑采样噪声的贡献，假设Sigma-Delta调制器中不存在连续时间路径（由于存在锁存量化器，在开关电容 Sigma-Delta 调制器中通常就是这种情况）。


## 端口


### 输出

<div class="details-box">
<details open>
<summary>y — 输出白噪声信号<div>实数标量</div></summary>
</details>
<div class="details-content">
 
根据设置参数输出白噪声信号。

**数据类型：** double

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>采样时间 — 设置模块采样时间<div> 正实数标量 </div></summary>
</details>
<div class="details-content">

信号的采样周期，单位为秒（s）。

</div>
</div>


<div class="details-box">
<details open>
<summary>噪声标准差 — 设置噪声标准差<div> 正实数标量 </div></summary>
</details>
<div class="details-content">

噪声的标准差，单位为伏特（V）。

</div>
</div>


<div class="details-box">
<details open>
<summary>随机数种子 — 随机数种子<div> 整数标量 </div></summary>
</details>
<div class="details-content">

随机数生成器种子，在使用随机数生成器的不同模块中使用不同的种子，可确保生成的随机序列互不相关。

</div>
</div>

## 版本历史记录

- 在 2025b 推出
