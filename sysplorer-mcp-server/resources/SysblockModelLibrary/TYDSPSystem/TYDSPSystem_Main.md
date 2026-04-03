# DSP 系统模块库（TYDSPSystem）
---
&nbsp;

DSP 系统模块库用于提供模块满足信号处理系统的设计、仿真与分析。其组成包括：信号产生、处理与分析，滤波器设计与分析，滤波器实现，变换与谱分析， 统计学和线性代数等功能模块。

通过 DSP 系统模块库可用于在时域和频域进行分析、测量及显示信号，设计与分析包括 FIR、IIR、单速率、多速率、多级滤波器， 同时提供傅立叶变换，离散余弦变换，谱分析，线性预测等常用变换和分析方式，流信号系统可以满足变量、数据文件或来自网络的仿真。

:::warning 注意

当前 DSP 系统模块库内模块仅支持 64 位仿真。

:::


## 信号生成、处理与分析

### 信号生成

| 模块名                     | 说明                                                         |
| -------------------------- | ------------------------------------------------------------ |
| [Constant](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYDSPSystem/SignalGenerationManipulationAndAnalysis/SignalGeneration/Constant.html) | 生成常量值 |
| [ColoredNoise](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYDSPSystem/SignalGenerationManipulationAndAnalysis/SignalGeneration/ColoredNoise.html) | 生成有色噪声信号 |
| [Chirp](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYDSPSystem/SignalGenerationManipulationAndAnalysis/SignalGeneration/Chirp.html) | 产生扫频余弦（chirp）信号 |
| [RandomSource](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYDSPSystem/SignalGenerationManipulationAndAnalysis/SignalGeneration/RandomSource.html) | 生成随机分布的数据 |
| [SignalFromWorkspace](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYDSPSystem/SignalGenerationManipulationAndAnalysis/SignalGeneration/SignalFromWorkspace.html) | 从 Syslab 工作区导入信号 |

### 信号操作

| 模块名                     | 说明                                                         |
| -------------------------- | ------------------------------------------------------------ |
| [Repeat](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYDSPSystem/SignalGenerationManipulationAndAnalysis/SignalOperations/Repeat.html) | 通过重复值以更高的速率重新采样输入 |
| [VariableFractionalDelay](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYDSPSystem/SignalGenerationManipulationAndAnalysis/SignalOperations/VariableFractionalDelay.html) | 可变分数延迟 |

### 缓冲、开关和计数器

| 模块名                     | 说明                                                         |
| -------------------------- | ------------------------------------------------------------ |
| [EdgeDetector](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYDSPSystem/SignalGenerationManipulationAndAnalysis/BuffersSwitchesAndCounters/EdgeDetector.html) | 响应从零到非零值的转换，输出一个采样周期的单位幅度脉冲 |
| [Buffer](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYDSPSystem/SignalGenerationManipulationAndAnalysis/BuffersSwitchesAndCounters/Buffer.html) | 将输入序列缓冲为更小或更大的帧大小 |
| [Unbuffer](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYDSPSystem/SignalGenerationManipulationAndAnalysis/BuffersSwitchesAndCounters/Unbuffer.html) | 将缓冲输入帧解除为标量输出序列 |

### 信号属性和索引

| 模块名                     | 说明                                                         |
| -------------------------- | ------------------------------------------------------------ |
| [Convert1Dto2D](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYDSPSystem/SignalGenerationManipulationAndAnalysis/SignalAttributesandIndexing/Convert1Dto2D.html) | 将一维或二维输入转换为具有指定尺寸的二维矩阵 |
| [Convert2Dto1D](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYDSPSystem/SignalGenerationManipulationAndAnalysis/SignalAttributesandIndexing/Convert2Dto1D.html) | 将二维矩阵输入转换为一维向量 |
| [FrameConversion](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYDSPSystem/SignalGenerationManipulationAndAnalysis/SignalAttributesandIndexing/FrameConversion.html) | 指定信号的采样模式 |

### 示波器和数据记录

| 模块名                     | 说明                                                         |
| -------------------------- | ------------------------------------------------------------ |
| [SpectrumAnalyzer](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYDSPSystem/SignalGenerationManipulationAndAnalysis/ScopeAndDataLogging/SpectrumAnalyzer.html) | 显示频谱 |

## 滤波器设计和分析

### 滤波器设计

| 模块名                     | 说明                                                         |
| -------------------------- | ------------------------------------------------------------ |
| [AnalogFilterDesign](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYDSPSystem/FilterDesignandAnalysis/FilterDesign/AnalogFilterDesign.html) | 设计和实现模拟滤波器 |
| [LowpassFilter](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYDSPSystem/FilterDesignandAnalysis/FilterDesign/LowpassFilter.html) | 设计 FIR 或 IIR 低通滤波器 |

## 滤波器实现

### 单速率滤波器

| 模块名                     | 说明                                                         |
| -------------------------- | ------------------------------------------------------------ |
| [BiquadFilter](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYDSPSystem/FilterImplementation/SingleRateFilters/BiquadFilter.html) | 使用 Biquad 结构实现一个通用 IIR 滤波器 |
| [DiscreteFIRFilter](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYDSPSystem/FilterImplementation/SingleRateFilters/DiscreteFIRFilter.html) | 构建 FIR 滤波器模型 |

### 多速率和多级滤波器

| 模块名                     | 说明                                                         |
| -------------------------- | ------------------------------------------------------------ |
| [FIRInterpolation](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYDSPSystem/FilterImplementation/MultirateandMultistageFilters/FIRInterpolation.html) | 构建 FIR 插值器模型 |

## 统计与线性代数

### 测量与统计

| 模块名                     | 说明                                                         |
| -------------------------- | ------------------------------------------------------------ |
| [MovingAverage](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYDSPSystem/StatisticsAndLinearAlgebra/MeasurementsAndStatistics/MovingAverage.html) | 计算移动平均 |
| [Variance](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYDSPSystem/StatisticsAndLinearAlgebra/MeasurementsAndStatistics/Variance.html) | 按照维度计算方差 |
| [Mean](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYDSPSystem/StatisticsAndLinearAlgebra/MeasurementsAndStatistics/Mean.html) | 计算输入的平均值 |
| [RMS](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYDSPSystem/StatisticsAndLinearAlgebra/MeasurementsAndStatistics/RMS.html) | 按照输入信号的指定维度计算均方根 |

### 数组与矩阵数学

| 模块名                     | 说明                                                         |
| -------------------------- | ------------------------------------------------------------ |
| [CreateDiagonalMatrix](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYDSPSystem/StatisticsAndLinearAlgebra/ArrayAndMatrixMathematics/CreateDiagonalMatrix.html) | 从对角线元素创建方形对角矩阵 |
| [MatrixSquare](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYDSPSystem/StatisticsAndLinearAlgebra/ArrayAndMatrixMathematics/MatrixSquare.html) | 计算输入矩阵的平方 |
| [PermuteMatrix](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYDSPSystem/StatisticsAndLinearAlgebra/ArrayAndMatrixMathematics/PermuteMatrix.html) | 重新排序矩阵的行或列 |
| [SubMatrix](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYDSPSystem/StatisticsAndLinearAlgebra/ArrayAndMatrixMathematics/SubMatrix.html) | 从矩阵输入中选择元素子集（子矩阵） |
| [dBGain](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYDSPSystem/StatisticsAndLinearAlgebra/ArrayAndMatrixMathematics/dBGain.html) | 使用 dB 作为增益 |
| [PolynomialEvaluation](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYDSPSystem/StatisticsAndLinearAlgebra/ArrayAndMatrixMathematics/PolynomialEvaluation.html) | 多项式计算 |

## 定点设计

### 量化器

| 模块名                     | 说明                                                         |
| -------------------------- | ------------------------------------------------------------ |
| [Quantizer](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYDSPSystem/FixedPointDesign/Quantizer/Quantizer.html) | 按给定间隔将输入离散化 |
| [ScalarQuantizerEncoder](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYDSPSystem/FixedPointDesign/Quantizer/ScalarQuantizerEncoder.html) | 通过将输入值与用户指定的边界点进行比较，将每个输入值映射到量化区域 |
