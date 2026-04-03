# 信号生成、处理与分析
---
&nbsp;

## 信号生成<a id="jump1"></a>

| 模块名                     | 说明                                                         |
| -------------------------- | ------------------------------------------------------------ |
| [Constant](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYDSPSystem/SignalGenerationManipulationAndAnalysis/SignalGeneration/Constant.html) | 生成常量值 |
| [ColoredNoise](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYDSPSystem/SignalGenerationManipulationAndAnalysis/SignalGeneration/ColoredNoise.html) | 生成有色噪声信号 |
| [Chirp](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYDSPSystem/SignalGenerationManipulationAndAnalysis/SignalGeneration/Chirp.html) | 产生扫频余弦（chirp）信号 |
| [RandomSource](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYDSPSystem/SignalGenerationManipulationAndAnalysis/SignalGeneration/RandomSource.html) | 生成随机分布的数据 |
| [SignalFromWorkspace](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYDSPSystem/SignalGenerationManipulationAndAnalysis/SignalGeneration/SignalFromWorkspace.html) | 从 Syslab 工作区导入信号 |

## 信号操作<a id="jump2"></a>

| 模块名                     | 说明                                                         |
| -------------------------- | ------------------------------------------------------------ |
| [Repeat](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYDSPSystem/SignalGenerationManipulationAndAnalysis/SignalOperations/Repeat.html) | 通过重复值以更高的速率重新采样输入 |
| [VariableFractionalDelay](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYDSPSystem/SignalGenerationManipulationAndAnalysis/SignalOperations/VariableFractionalDelay.html) | 可变分数延迟 |

## 缓冲、开关和计数器<a id="jump3"></a>

| 模块名                     | 说明                                                         |
| -------------------------- | ------------------------------------------------------------ |
| [EdgeDetector](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYDSPSystem/SignalGenerationManipulationAndAnalysis/BuffersSwitchesAndCounters/EdgeDetector.html) | 响应从零到非零值的转换，输出一个采样周期的单位幅度脉冲 |
| [Buffer](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYDSPSystem/SignalGenerationManipulationAndAnalysis/BuffersSwitchesAndCounters/Buffer.html) | 将输入序列缓冲为更小或更大的帧大小 |
| [Unbuffer](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYDSPSystem/SignalGenerationManipulationAndAnalysis/BuffersSwitchesAndCounters/Unbuffer.html) | 将缓冲输入帧解除为标量输出序列 |

## 信号属性和索引<a id="jump4"></a>

| 模块名                     | 说明                                                         |
| -------------------------- | ------------------------------------------------------------ |
| [Convert1Dto2D](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYDSPSystem/SignalGenerationManipulationAndAnalysis/SignalAttributesandIndexing/Convert1Dto2D.html) | 将一维或二维输入转换为具有指定尺寸的二维矩阵 |
| [Convert2Dto1D](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYDSPSystem/SignalGenerationManipulationAndAnalysis/SignalAttributesandIndexing/Convert2Dto1D.html) | 将二维矩阵输入转换为一维向量 |
| [FrameConversion](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYDSPSystem/SignalGenerationManipulationAndAnalysis/SignalAttributesandIndexing/FrameConversion.html) | 指定信号的采样模式 |

## 示波器和数据记录<a id="jump5"></a>

| 模块名                     | 说明                                                         |
| -------------------------- | ------------------------------------------------------------ |
| [SpectrumAnalyzer](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYDSPSystem/SignalGenerationManipulationAndAnalysis/ScopeAndDataLogging/SpectrumAnalyzer.html) | 显示频谱 |