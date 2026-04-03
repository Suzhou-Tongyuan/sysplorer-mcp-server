# Utilities
---
&nbsp;

用于字节和内存操作的模块。

配置模块在位和字节级别管理数据流，使用实用程序模块。

## 模块

| 模块名                                                       | 说明                                                        |
| ------------------------------------------------------------ | ----------------------------------------------------------- |
| **[BytePack](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Utilities/BytePack.html)** | 将输入信号转换为 uint8 向量                                 |
| **[ByteUnpack](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Utilities/ByteUnpack.html)** | 将 uint8 向量转换为输入信号                                 |
| **[CCaller](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Utilities/CCaller.html)** | 在 Sysblock 中集成 C 代码                                   |
| **[Display](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Utilities/Display.html)** | 显示输入的值                                                |
| **[Fcn](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Utilities/Fcn.html)** | 将指定的数学表达式应用于其输入                              |
| **[Merge](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Utilities/Merge.html)** | 将多个信号合并为一个信号                                    |
| **[Scope](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Utilities/Scope.html)** | 显示仿真过程中生成的信号                                    |
| **[StopSimulation](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Utilities/StopSimulation.html)** | 当输入为非零值时使仿真停止                                  |
| **[CFunction](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Utilities/CFunction.html)** | 支持将用户编写 C 代码集成外部C语言算法                      |
| **[ToFile](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Utilities/ToFile.html)** | 将数据写入到文件                                            |
| **[ToWorkspace](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Utilities/ToWorkspace.html)** | 将数据从 Sysblock 模型记录到 Syslab 工作区                  |
| **[Terminator](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Utilities/Terminator.html)** | 终止未连接的输出端口                                        |
| **[JuliaObject](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Utilities/JuliaObject.html)** | 使用 Syslab 中的 Julia 对象进行动态系统建模和处理流式数据。 |
| **[JuliaFunction](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Utilities/JuliaFunction.html)** | 在 Sysblock 模型中调用 Julia 函数。                         |
| **[Counter](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Utilities/Counter.html)** | 在指定的数据范围内进行计数                                  |
| **[ExternalOutport](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Utilities/ExternalOutport.html)** | 模型导出 FMU 时，可视为顶层输出端口                         |
| **[ExternalInport](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Utilities/ExternalInport.html)** | 模型导出 FMU 时，可视为顶层输入端口                         |
| **[CANPack](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Utilities/CANPack.html)** | 将单个信号打包到报文中                                      |
| **[CANUnpack](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Utilities/CANUnpack.html)** | 从 CAN 报文中解包单个信号                                   |
