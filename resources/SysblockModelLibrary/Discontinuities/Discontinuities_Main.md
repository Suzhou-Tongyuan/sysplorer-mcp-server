# Discontinuities
---
&nbsp;

不连续函数模块，例如 Saturation

使用 Discontinuities 库中的模块对不连续时间动态系统的元素（如静态和动态摩擦、穿越以及输入产生零输出的区域）进行建模。

| 模块名                                                       | 说明                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [RateLimiter](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Discontinuities/RateLimiter.html) | 限制信号变化的速率                                           |
| [Relay](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Discontinuities/Relay.html) | 在两个常量输出之间进行切换                                   |
| [Quantizer](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Discontinuities/Quantizer.html) | 按给定间隔将输入离散化                                       |
| [DeadZone](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Discontinuities/DeadZone.html) | 输入位于死区内时输出零。超出死区时，按起始值或结束值对输入信号进行偏移 |
| [DeadZoneDynamic](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Discontinuities/DeadZoneDynamic.html) | 提供零输出的动态区域                                         |
| [SaturationDynamic](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Discontinuities/SaturationDynamic.html) | 将输入信号限制在动态饱和上限和下限值之间                     |
| [RateLimiterDynamic](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Discontinuities/RateLimiterDynamic.html) | 限制信号变化的速率                                           |
| [Backlash](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Discontinuities/Backlash.html) | 对间隙系统行为进行建模                                       |
| [WrapToZero](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Discontinuities/WrapToZero.html) | 如果输入大于阈值，将输出设置为零                             |
| [Saturation](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Discontinuities/Saturation.html) | 将输入信号限制在饱和上限和下限值之间                         |
| [CoulombandViscousFriction](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Discontinuities/CoulombandViscousFriction.html) | 对值为零时的不连续性以及非零时的线性增益建模                 |
| [HitCrossing](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Discontinuities/HitCrossing.html) | 检测穿越点                                                   |