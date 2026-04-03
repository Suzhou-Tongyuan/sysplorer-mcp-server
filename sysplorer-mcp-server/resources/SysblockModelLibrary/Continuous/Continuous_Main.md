# Continuous
---
&nbsp;

连续函数模块

使用 Continuous 库中的模块进行微分方程建模。您可以使用信号的时间导数。您可以对信号进行积分或延迟信号。您可以使用传递函数或状态空间表示来对 PID 控制器和线性系统建模。

## 模块

| 模块名                                                       | 说明                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| **[Integrator](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Continuous/Integrator.html)** | 对输入信号进行积分                                           |
| **[TransportDelay](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Continuous/TransportDelay.html)** | 延迟输入信号                                                 |
| **[ZeroPole](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Continuous/ZeroPole.html)** | 传递函数的零点和极点                                         |
| **[TransferFcn](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Continuous/TransferFcn.html)** | 将线性系统建模为传递函数                                     |
| **[StateSpace](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Continuous/StateSpace.html)** | 状态空间表示的状态矩阵、输入矩阵和输出矩阵                   |
| **[Derivative](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Continuous/Derivative.html)** | Derivative 模块采用数值差分 Δu/Δt 的方式输出输入信号 u 关于时间 t 的导数 |
| **[VariableTimeDelay](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Continuous/VariableTimeDelay.html)** | 可变时滞建模                                                 |
| **[VariableTransportDelay](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Continuous/VariableTransportDelay.html)** | 可变传输延迟建模                                             |
| **[PIDController](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Continuous/PIDController.html)** | 连续时间 PID 控制器                                          |
| IntegratorLimited                                            | 详细内容，请参考 **[Integrator](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Continuous/Integrator.html)** 模块 |
| **[SecondOrderIntegrator](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Continuous/SecondOrderIntegrator.html)** | 输入信号的二阶积分                                           |
| **[FirstOrderHold](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Continuous/FirstOrderHold.html)** | 在输入信号上实现线性外插一阶保持                             |

