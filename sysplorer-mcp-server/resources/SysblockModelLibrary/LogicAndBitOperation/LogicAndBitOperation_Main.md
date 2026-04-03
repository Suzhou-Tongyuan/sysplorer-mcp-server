# LogicAndBitOperation
---
&nbsp;

逻辑或位运算模块，例如 LogicalOperator 和 RelationalOperator。

使用 LogicandBitOperations 库中的模块来检测信号值的变化，对输入执行逻辑或关系运算，并将位转换为整数。

## 模块

| 模块名                                                       | 说明                                            |
| ------------------------------------------------------------ | ----------------------------------------------- |
| **[RelationalOperator](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/LogicAndBitOperation/RelationalOperator.html)** | 比较 u1 与 u2 的数值关系，输出布尔值            |
| **[BitwiseOperator](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/LogicAndBitOperation/BitwiseOperator.html)** | 对输入执行指定的按位运算                        |
| **[LogicalOperator](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/LogicAndBitOperation/LogicalOperator.html)** | 逻辑运算符                                      |
| **[IntervalTest](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/LogicAndBitOperation/IntervalTest.html)** | 检查输入值是否在指定区间                        |
| **[IntervalTestDynamic](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/LogicAndBitOperation/IntervalTestDynamic.html)** | 检测输入值是否在指定区间，区间值由输入决定      |
| **[DetectChange](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/LogicAndBitOperation/DetectChange.html)** | 检测信号值的变化                                |
| **[DetectDecrease](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/LogicAndBitOperation/DetectDecrease.html)** | 检测信号值的下降                                |
| **[DetectIncrease](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/LogicAndBitOperation/DetectIncrease.html)** | 检测信号值的增长                                |
| **[DetectFallNegative](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/LogicAndBitOperation/DetectFallNegative.html)** | 检测越过零点的下降沿                            |
| **[DetectFallNonpositive](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/LogicAndBitOperation/DetectFallNonpositive.html)** | 检测越过或抵达零点的下降沿                      |
| **[DetectRisePositive](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/LogicAndBitOperation/DetectRisePositive.html)** | 检测越过零点的上升沿                            |
| **[DetectRiseNonnegative](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/LogicAndBitOperation/DetectRiseNonnegative.html)** | 检测越过或抵达零点的上升沿                      |
| **[CompareToZero](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/LogicAndBitOperation/CompareToZero.html)** | 确定信号与零的比较方式                          |
| **[CompareToConstant](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/LogicAndBitOperation/CompareToConstant.html)** | 确定信号与指定常量的比较方式                    |
| **[ShiftArithmetic](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/LogicAndBitOperation/ShiftArithmetic.html)** | 移动信号的位或二进制小数点                      |
| **[BitSlice](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/LogicAndBitOperation/BitSlice.html)** | 从输入信号返回连续的位域                        |
| **[ExtractBits](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/LogicAndBitOperation/ExtractBits.html)** | 将输入信号转换为 int32 类型，并输出选择的连续位 |
| **[CombinatorialLogic](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/LogicAndBitOperation/CombinatorialLogic.html)** | 真值表                                          |
| **[BitSet](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/LogicAndBitOperation/BitSet.html)** | 将存储的整数的指定位设置为 1                    |
| **[BitClear](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/LogicAndBitOperation/BitClear.html)** | 将存储的整数的指定位设置为 0                    |
| **[FloatExtractBits](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/LogicAndBitOperation/FloatExtractBits.html)** | 用来指定浮点输入的输出位                        |
| **[BitToIntegerConverter](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/LogicAndBitOperation/BitToIntegerConverter.html)** | 将元素为比特的向量映射为元素为整数的向量        |
| **[IntegerToBitConverter](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/LogicAndBitOperation/IntegerToBitConverter.html)** | 将元素为整数的向量映射为元素为比特的向量        |

