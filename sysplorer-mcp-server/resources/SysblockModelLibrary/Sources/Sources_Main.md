# Sources
---
&nbsp;

使用定义和生成信号或加载信号数据的模块为仿真提供输入。


使用 Sources 库中的模块为仿真提供输入信号。

## 模块

| 模块名                                                       | 说明                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| **[Clock](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Sources/Clock.html)** | 显示并提供仿真时间                                           |
| **[Constant](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Sources/Constant.html)** | 生成常量值                                                   |
| **[Step](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Sources/Step.html)** | 生成阶跃函数                                                 |
| **[Ramp](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Sources/Ramp.html)** | 生成持续上升或下降的信号                                     |
| **[SineWave](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Sources/SineWave.html)** | 使用仿真时间作为时间源以生成正弦波                           |
| **[SignalBuilder](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Sources/SignalBuilder.html)** | 创建和生成可互换的分段线性波形信号组                         |
| **[Ground](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Sources/Ground.html)** | 将未连接的输入端口接地                                       |
| **[RepeatingSequence](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Sources/RepeatingSequence.html)** | 生成任意形状的周期信号                                       |
| **[PulseGenerator](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Sources/PulseGenerator.html)** | 按固定间隔生成方波脉冲                                       |
| **[RandomNumber](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Sources/RandomNumber.html)** | 生成正态分布的随机数                                         |
| **[UniformRandomNumber](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Sources/UniformRandomnumber.html)** | 生成均匀分布的随机数                                         |
| **[CounterFreeRunning](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Sources/CounterFreeRunning.html)** | 自由运行的计数器                                             |
| **[CounterLimited](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Sources/CounterLimited.html)** | 计数器                                                       |
| **[BandLimitedWhiteNoise](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Sources/BandLimitedWhiteNoise.html)** | 生成适合在连续系统或混合系统中使用的正态分布随机数           |
| **[FromFile](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Sources/FromFile.html)** | 将 CSV 文件中的数据加载到 Sysblock 模型中                    |
| **[FromWorkspace](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Sources/FromWorkspace.html)** | 从 Syslab 工作区读取数据                                     |
| **[DigitalClock](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Sources/DigitalClock.html)** | 以指定的采样间隔输出仿真时间                                 |
| **[BernoulliBinaryGenerator](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Sources/BernoulliBinaryGenerator.html)** | 生成满足伯努利分布的二进制数                                 |
| **[PoissonIntegerGenerator](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Sources/PoissonIntegerGenerator.html)** | 生成满足泊松分布的随机整数                                   |
| **[RandomIntegerGenerator](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Sources/RandomIntegerGenerator.html)** | 生成在指定范围内均匀分布的随机整数                           |
| **[RepeatingSequenceStair](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Sources/RepeatingSequenceStair.html)** | 输出并重复离散时间序列                                       |
| **[RepeatingSequenceInterpolated](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Sources/RepeatingSequenceInterpolated.html)** | 输出离散时间序列并重复，从而在数据点之间插值                 |
| **[ChirpSignal](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Sources/ChirpSignal.html)** | 生成频率随时间线性变化的正弦波                               |
| DiscretePulseGenerator                                       | 详细内容，请参考 **[PulseGenerator](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Sources/PulseGenerator.html)** 模块 |