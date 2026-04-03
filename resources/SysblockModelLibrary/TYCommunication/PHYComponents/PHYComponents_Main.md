# 物理层组件
---
&nbsp;

## 源和汇<a id="jump1"></a>

| 模块名                     | 说明                                                         |
| -------------------------- | ------------------------------------------------------------ |
| [BernoulliBinaryGenerator](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYCommunication/PHYComponents/SourcesAndSinks/BernoulliBinaryGenerator.html) | 生成伯努利分布的随机二进制数 |
| [PNSequenceGenerator](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYCommunication/PHYComponents/SourcesAndSinks/PNSequenceGenerator.html) | 生成伪噪声序列 |
| [EyeDiagram](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYCommunication/PHYComponents/SourcesAndSinks/EyeDiagram.html) | 显示时域信号的眼图 |
| [ConstellationDiagram](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYCommunication/PHYComponents/SourcesAndSinks/ConstellationDiagram.html) | 显示输入信号的星座图 |

## 错误检测与校正<a id="jump_error"></a>

| 模块名                     | 说明                                                         |
| -------------------------- | ------------------------------------------------------------ |
| [BinaryCyclicDecoder](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYCommunication/PHYComponents/ErrorDetectionAndCorrection/BinaryCyclicDecoder.html) | 解码系统循环码以恢复二进制矢量数据 |
| [BinaryCyclicEncoder](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYCommunication/PHYComponents/ErrorDetectionAndCorrection/BinaryCyclicEncoder.html) | 从二进制向量数据创建系统循环码 |
| [BinaryLinearDecoder](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYCommunication/PHYComponents/ErrorDetectionAndCorrection/BinaryLinearDecoder.html) | 解码线性块码以恢复二进制矢量数据 |
| [BinaryLinearEncoder](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYCommunication/PHYComponents/ErrorDetectionAndCorrection/BinaryLinearEncoder.html) | 从二进制矢量数据创建线性块码 |
| [HammingDecoder](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYCommunication/PHYComponents/ErrorDetectionAndCorrection/HammingDecoder.html) | 解码汉明码以恢复二进制矢量数据 |
| [HammingEncoder](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYCommunication/PHYComponents/ErrorDetectionAndCorrection/HammingEncoder.html) | 从二进制矢量数据创建汉明码 |

## 信号操作<a id="jump2"></a>

| 模块名                     | 说明                                                         |
| -------------------------- | ------------------------------------------------------------ |
| [Descrambler](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYCommunication/PHYComponents/SignalOperations/Descrambler.html) | 解扰输入信号 |
| [Scrambler](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYCommunication/PHYComponents/SignalOperations/Scrambler.html) | 干扰输入信号 |
| [BittoIntegerConverter](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYCommunication/PHYComponents/SignalOperations/BittoIntegerConverter.html) | 将比特向量映射为对应的整数向量 |
| [FrequencyDivider](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYCommunication/PHYComponents/SignalOperations/FrequencyDivider.html) | 对输入信号进行分频操作 |
| [PhaseDetector](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYCommunication/PHYComponents/SignalOperations/PhaseDetector.html) | 相位检测器 |


## 调制<a id="jump3"></a>

| 模块名                     | 说明                                                         |
| -------------------------- | ------------------------------------------------------------ |
| [PMModulatorPassband](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYCommunication/PHYComponents/Modulation/PMModulatorPassband.html) | 使用相位调制进行调制 |
| [QPSKDemodulatorBaseband](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYCommunication/PHYComponents/Modulation/QPSKDemodulatorBaseband.html) | QPSK 调制信号解调 |
| [QPSKModulatorBaseband](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYCommunication/PHYComponents/Modulation/QPSKModulatorBaseband.html) | 采用正交相移键控方法进行调制 |
| [RectangularQAMDemodulatorBaseband](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYCommunication/PHYComponents/Modulation/RectQAMDemodulator.html) | 解调矩形正交调幅后的进行基带信号 |
| [RectangularQAMModulatorBaseband](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYCommunication/PHYComponents/Modulation/RectQAMModulator.html) | 采用矩形正交调幅法进行调制 |
| [DSBAMDemodulatorPassband](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYCommunication/PHYComponents/Modulation/DSBAMDemodulatorPassband.html) | 解调 DSB AM 调制数据 |
| [DSBAMModulatorPassband](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYCommunication/PHYComponents/Modulation/DSBAMModulatorPassband.html) | 利用双边带调幅进行调制 |
| [DSBSCAMDemodulatorPassband](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYCommunication/PHYComponents/Modulation/DSBSCAMDemodulatorPassband.html) | 解调 DSBSC AM 调制数据 |
| [DSBSCAMModulatorPassband](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYCommunication/PHYComponents/Modulation/DSBSCAMModulatorPassband.html) | 利用双边带抑制载波幅度调制进行调制 |


## 滤波<a id="jump4"></a>

| 模块名                     | 说明                                                         |
| -------------------------- | ------------------------------------------------------------ |
| [RaisedCosineReceiveFilter](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYCommunication/PHYComponents/Filtering/RaisedCosineReceiveFilter.html) | 通过升余弦 FIR 滤波器下采样实现脉冲成形 |
| [RaisedCosineTransmitFilter](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYCommunication/PHYComponents/Filtering/RaisedCosineTransmitFilter.html) | 通过升余弦 FIR 滤波器插值实现脉冲成形 |


## 同步与接收机设计<a id="jump5"></a>

| 模块名                     | 说明                                                         |
| -------------------------- | ------------------------------------------------------------ |
| [AGC](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYCommunication/PHYComponents/SynchronizationAndReceiverDesign/AGC.html) | 自适应调整增益恒定的信号电平输出 |
| [CarrierSynchronizer](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYCommunication/PHYComponents/SynchronizationAndReceiverDesign/CarrierSynchronizer.html) | 补偿载波频率偏移 |
| [CoarseFrequencyCompensator](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYCommunication/PHYComponents/SynchronizationAndReceiverDesign/CoarseFrequencyCompensator.html) | 补偿 PAM、PSK 或 QAM 中的载波频率偏移 |
| [PreambleDetector](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYCommunication/PHYComponents/SynchronizationAndReceiverDesign/PreambleDetector.html) | 检测数据包中的序文 |
| [SymbolSynchronizer](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYCommunication/PHYComponents/SynchronizationAndReceiverDesign/SymbolSynchronizer.html) | 纠正符号计时时钟偏差 |
| [ContinuousTimeVCO](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/TYCommunication/PHYComponents/SynchronizationAndReceiverDesign/ContinuousTimeVCO.html) | 实现连续时间压控振荡器 |
