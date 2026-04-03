# dBGain
---
&nbsp;

使用 dB 作为增益。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/dbGain/1.jpg')" style="width: 100px; height: auto; transform: scale(1);">

**库：** TYDSPSystem / StatisticsAndLinearAlgebra / ArrayAndMatrixMathematics 

## 描述

dB Gain模块根据以下公式将输入信号的幅度以分贝(db)为单位进行增益或衰减：

$
y_{ij}=u_{ij}*10^{(g_{ij}/k)}
$

其中 u 是模块输入，g 为设置的增益值，k 为增益系数（选择功率，则 k 为 10，选择电压，则 k 为 20），y 是输出。

## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperation/dbGain.mo">dbGain.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/dbGain/2.png')" style="width: 500px; height: auto; transform: scale(1);">

仿真结果如下：

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/MathOperationPng/dbGain/3.png')" style="width: 500px; height: auto; transform: scale(1);">

### 示例说明

- sineWave 模块：生成正弦信号波。
- dB Gain 模块：将输入信号的幅度进行增益或衰减，可以选择的输入信号类型为功率或电压（选择功率，则 k 为 10，选择电压，则 k 为 20）。
- Scope 模块：用于显示模型的输出结果。


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入端口<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

输入信号，向该输入信号进行增益或衰减以创建输出信号。

**数据类型：** double | float | int8 | uint8 | int16 | uint16 | int32 | uint32 | int64 | fixedpoint

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 输出端口<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

输出信号。

**数据类型：** double | float | int8 | uint8 | int16 | uint16 | int32 | uint32 | int64 | fixedpoint

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>增益值<div>分贝</div></summary>
</details>
<div class="details-content">

指定要添加到输入信号的增益值，单位为分贝(db)。

**模块参数**：dB

**类型**：字符向量

**值**：有限实数

**默认值：**-40

</div>
</div>



<div class="details-box">
<details open>
<summary>输入信号类型<div>功率（默认） | 电压</div></summary>
</details>
<div class="details-content">

指定要添加到输入信号的偏移量的值。

**模块参数**：k

**类型**：字符向量

**值**：功率(k=10)或者电压(k=20)

**默认值：** 功率(k=10)

</div>
</div>


## 版本历史记录

- 在 2026a 推出


## 限制信息

- 不支持布尔、总线、枚举类型输入/输出。