# MathOperation
---
&nbsp;

数学函数模块，例如 Gain、Product 和 Sum。

使用 MathOperation 库中的模块进行基本数学函数建模。



| 模块名                                                       | 说明                                                  |
| ------------------------------------------------------------ | ----------------------------------------------------- |
| [MathFunction](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/MathFunction.html) | 执行数学函数                                          |
| [TrigonometricFunction](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/TrigonometricFunction.html) | 指定应用于输入信号的三角函数                          |
| [RoundingFunction](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/RoundingFunction.html) | 对信号应用舍入函数                                    |
| [Sum](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/Sum.html) | 输入信号的加减运算                                    |
| [Product](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/Product.html) | 标量和非标量的乘除运算或者矩阵的乘法和逆运算          |
| [Gain](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/Gain.html) | 将输入乘以常量                                        |
| [Bias](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/Bias.html) | 为输入添加偏差                                        |
| [Sign](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/Sign.html) | 指示输入的符号                                        |
| [Abs](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/Abs.html) | 输出输入信号的绝对值                                  |
| [UnaryMinus](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/UnaryMinus.html) | 对输入求反                                            |
| [Maxmin](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/Maxmin.html) | 输出最小或最大输入值                                  |
| [MinMaxRunningResettable](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/MinMaxRunningResettable.html) | 确定信号随时间而改变的最小值或最大值                  |
| [SineWaveFunction](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/SineWaveFunction.html) | 使用外部信号作为时间源来生成正弦波                    |
| [Sqrt](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/Sqrt.html) | 计算平方根、带符号的平方根或平方根的倒数数            |
| [Reshape](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/Reshape.html) | 更改信号的维度                                        |
| [AdjointOf3x3Matrix](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/AdjointOf3x3Matrix.html) | 计算输入矩阵的伴随矩阵                                |
| [Create3x3Matrix](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/Create3x3Matrix.html) | 根据 9 个输入值创建 3×3 矩阵                          |
| [DotProduct](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/DotProduct.html) | 生成两个向量的点积                                    |
| [CrossProduct](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/CrossProduct.html) | 两个向量的叉积                                        |
| [CreateDiagonalMatrix](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/CreateDiagonalMatrix.html) | 从对角线元素创建方形对角矩阵                          |
| [IdentityMatrix](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/IdentityMatrix.html) | 生成 1 在主对角线上的矩阵，并在其他位置生成 ground 值 |
| [Det3x3](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/Det3x3.html) | 计算矩阵的行列式                                      |
| [Invert3x3Matrix](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/Invert3x3Matrix.html) | 计算 3×3 矩阵的逆                                     |
| [MatrixSquare](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/MatrixSquare.html) | 计算输入矩阵的平方                                    |
| [PermuteMatrix](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/PermuteMatrix.html) | 重新排序矩阵的行或列                                  |
| [SubMatrix](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/SubMatrix.html) | 从矩阵输入中选择元素子集（子矩阵）                    |
| [IsTriangular](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/IsTriangular.html) | 检测输入信号是否为上三角矩阵或下三角矩阵              |
| [QuaternionInterpolation](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/QuaternionInterpolation.html) | 两个四元数之间的四元数插值                            |
| [QuaternionModulus](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/QuaternionModulus.html) | 计算四元数的模                                        |
| [QuaternionNorm](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/QuaternionNorm.html) | 计算四元数的范数                                      |
| [QuaternionNormalize](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/QuaternionNormalize.html) | 规范化四元数                                          |
| [QuaternionRotation](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/QuaternionRotation.html) | 求四元数旋转向量                                      |
| [QuaternionConjugate](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/QuaternionConjugate.html) | 计算四元数的共轭                                      |
| [QuaternionInverse](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/QuaternionInverse.html) | 计算四元数的逆                                        |
| [QuaternionDivision](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/QuaternionDivision.html) | 用一个四元数除以另一个四元数                          |
| [QuaternionMultiplication](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/QuaternionMultiplication.html) | 计算两个四元数的乘积积                                |
| [TypeConversion](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/TypeConversion.html) | 将输入信号转换为指定的数据类型                        |
| [dbGain](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/dbGain.html) | 使用 db 作为增益                                      |
| [RMS](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/RMS.html) | 按照输入信号的指定维度计算均方根                      |
| [RealImagToComplex](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/RealImagToComplex.html) | 将实部/虚部输入转换成复信号                           |
| [MagnitudeAngleToComplex](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/MagnitudeAngleToComplex.html) | 将幅值/相位角输入转换成复信号                         |
| [ComplexToRealImag](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/ComplexToRealImag.html) | 输出复数输入信号的实部和虚部                          |
| [ComplexToMagnitudeAngle](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/ComplexToMagnitudeAngle.html) | 输出复数的幅值和/或相位角                             |
| [WeightedSampleTimeMath](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/WeightedSampleTimeMath.html) | 支持涉及采样时间的计算                                |
| [FindNonzeroElements](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/FindNonzeroElements.html) | 查找数组中的非零元素                                  |
