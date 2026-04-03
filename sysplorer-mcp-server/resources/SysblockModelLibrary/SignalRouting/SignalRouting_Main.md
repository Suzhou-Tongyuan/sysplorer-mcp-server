# SignalRouting
---
&nbsp;

传送信号的模块，例如 BusCreator 和 Switch。

使用 SignalRouting 库中的模块来创建合成信号、管理数据存储以及在输入之间切换。

## 模块

| 模块名                                                       | 说明                                                   |
| ------------------------------------------------------------ | ------------------------------------------------------ |
| **[Mux](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SignalRouting/Mux.html)** | 将相同数据类型和输入信号合并为虚拟向量                 |
| **[DeMux](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SignalRouting/DeMux.html)** | 提取并输出虚拟向量信号的元素                           |
| **[BusCreator](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SignalRouting/BusCreator.html)** | 将输入信号或消息组合到总线中                           |
| **[BusSelector](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SignalRouting/BusSelector.html)** | 从输入总线中选择元素                                   |
| **[BusToVector](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SignalRouting/BusToVector.html)** | 将虚拟总线转换为向量                                   |
| **[Switch](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SignalRouting/Switch.html)** | 基于第二个输入的值在第一个输入和第三个输入之间切换输出 |
| **[MultiportSwitch](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SignalRouting/MultiportSwitch.html)** | 基于控制信号选择输出信号                               |
| **[DataStoreMemory](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SignalRouting/DataStoreMemory.html)** | 定义数据存储                                           |
| **[DataStoreRead](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SignalRouting/DataStoreRead.html)** | 从数据存储中读取数据                                   |
| **[DataStoreWrite](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SignalRouting/DataStoreWrite.html)** | 向数据存储中写入数据                                   |
| **[From](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SignalRouting/From.html)** | 接受来自 Goto 模块的输入                               |
| **[Goto](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SignalRouting/Goto.html)** | 将模块输入传递给 From 模块                             |
| **[GotoTagVisibility](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SignalRouting/GotoTagVisibility.html)** | 定义 Goto 模块标记的作用域                             |
| **[Selector](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SignalRouting/Selector.html)** | 从向量、矩阵或多维信号中选择输入元素                   |
| **[VectorConcatenate](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SignalRouting/VectorConcatenate.html)** | 串联相同数据类型的输入向量以进行迭代处理               |
| **[ManualSwitch](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/SignalRouting/ManualSwitch.html)** | 在两个输入之间切换               |