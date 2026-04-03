# 混合信号模块库（TYMixedSignal）
---
&nbsp;

混合信号模块库提供组件和损伤模型，分析和测试工具，用于设计和验证混合信号集成电路。支持在不同的抽象层次上对 PLL、数据转换器和其他系统进行建模。可以自定义模型以包含诸如噪声、非线性、抖动和量化效果等损害。

当前主要提供用于模拟开关电容（SC）Σ-Δ 调制器的性能的建模仿真，全面涵盖了各类关键的非理想特性，具体包括：采样抖动、kT/C 热噪声、内部 ADC/DAC 的参数误差（如器件失配与非线性失真）以及运算放大器的性能限制（如白噪声、1/f 噪声、有限直流增益、有限带宽、压摆率限制和输出饱和电压）等。

:::warning 注意

当前混合信号模块库内模块仅支持 64 位仿真。

:::


## 数据转换器

| 模块名                     | 说明                                                         |
| -------------------------- | ------------------------------------------------------------ |
| [DeltaSigmaModulator](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYMixedSignal/DataConverters/DeltaSigmaModulator.html) | 离散 DeltaSigma 调制器 ADC 建模 |


## SigmaDelta 公共模块

| 模块名                     | 说明                                                         |
| -------------------------- | ------------------------------------------------------------ |
| [JitteredSineWave](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYMixedSignal/SDUtilities/JitteredSineWave.html) | 产生具有采样抖动的正弦波 |
| [ColoredNoise](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYMixedSignal/SDUtilities/ColoredNoise.html) | 根据用户定义的功率谱密度对噪声源进行建模 |
| [REALIntegratorWithDelay](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYMixedSignal/SDUtilities/REALIntegratorWithDelay.html) | 考虑运算放大器非理想特性的离散积分器 |
| [REALIntegratorNoDelay](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYMixedSignal/SDUtilities/REALIntegratorNoDelay.html) | 在考虑运算放大器饱和、有限增益、有限带宽和转换速率的情况下，模拟一个真实的无延迟离散积分器 |
| [REALResonator](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYMixedSignal/SDUtilities/REALResonator.html) | 考虑运算放大器饱和、有限增益、有限带宽和转换速率，对一个真实的带延迟的离散谐振器进行建模 |
| [IDEALIntegratorWithDelay](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYMixedSignal/SDUtilities/IDEALIntegratorWithDelay.html) | 在考虑运算放大器饱和的情况下，建立了一个理想的带延迟的离散积分器模型 |
| [IDEALIntegratorNoDelay](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYMixedSignal/SDUtilities/IDEALIntegratorNoDelay.html) | 在考虑运算放大器饱和的情况下，模拟一个理想的无延迟离散积分器 |
| [IDEALResonator](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYMixedSignal/SDUtilities/IDEALResonator.html) | 建立考虑运放饱和的离散谐振器延迟模型 |
| [kTOrCnoise](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYMixedSignal/SDUtilities/kTOrCnoise.html) | 模拟开关电容 $C_s$ 的 kT/C 噪声 |
| [SamplingJitter](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYMixedSignal/SDUtilities/SamplingJitter.html) | 对输入信号的采样抖动进行建模 |
| [Whitenoise](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYMixedSignal/SDUtilities/Whitenoise.html) | 用白功率谱密度模拟噪声源 |
| [ADC_DAC](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYMixedSignal/SDUtilities/ADC_DAC.html) | 考虑失配的多位 ADC 和 DAC 模型 |
| [SwitchNonLinearity](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYMixedSignal/SDUtilities/SwitchNonLinearity.html) | 对采样开关的非线性 Ron 进行建模 |