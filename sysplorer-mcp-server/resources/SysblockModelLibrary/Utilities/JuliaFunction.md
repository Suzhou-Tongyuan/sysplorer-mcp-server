# JuliaFunction
---
&nbsp;

在 Sysblock 模型中调用 Julia 函数。

**库：** Sysblock 模块库 / Utilities

<img :src="$withBase('/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/JuliaFunction/JuliaFunctionModuleAppearance.png')" style="width: 200px; height: auto; transform: scale(1);border: 1px solid black;">

## 描述

使用 JuliaFunction 可以编写用于 Sysblock 模型的 Julia 函数并将 JuliaFunction 的输入输出数据指定为参数和返回值。

::: warning 注意    
在使用 JuliaFunction 模块前，请确认以下前提条件被满足，否则 JuliaFunction 不可用：
- 当前的 Sysplorer 由相同版本的 Syslab 启动，且当前 Syslab 处于运行状态；
- Sysplorer 的 Syslab Extension for Sysplorer 插件被加载并启用。
::: 

### 编辑 Julia 函数脚本

双击 JuliaFunction 模块， Syslab 窗口将弹出并打开 Julia 函数脚本。您可在该脚本文件中定义多个 Julia 函数，其中第一个函数将被视作对应 JuliaFunction 模块的主函数，其他函数均被视作服务于主函数的辅助函数。

<img :src="$withBase('/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/JuliaFunction/EditingJuliaFunctionScript.png')" style="width: 400px; height: auto; transform: scale(1);border: 1px solid black;">

**端口：**

JuliaFunction 模块的输入、输出端口等信息均取决于主函数的定义情况，而与辅助函数无直接关联。

| **端口类型** | **说明**                           |
| ----------- | ---------------------------------- |
| 输入端口   | 主函数的形参                    |
| 输出端口    | 主函数的返回值                 |

编写函数脚本文件时，请注意：
- 主函数必须使用 function 定义；
- 主函数的输入不可指定类型，不可指定具名参数；
- 主函数、各个辅助函数的名称，在同一个模型范围中须唯一；
- 主函数的输出必须使用 return 指定，且必须为函数体中已经出现的变量符号（例如，”return y1, y2”为合法，而“return y1 * 2””return 3+3””return 6”等为非法）。

### 在模型中使用 Julia 函数

当您完成函数脚本文件的编辑并保存后，对应的 JuliaFunction 模块的输入与输出端口即被自动更新，您可按需将它们连接到其它模块上。

<img :src="$withBase('/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/JuliaFunction/ConnectingPorts.png')" style="width: 700px; height: auto; transform: scale(1);border: 1px solid black;">

选中 JuliaFunction 模块，右键单击并在下拉菜单中选择**编辑参数**，在对话框中配置输入输出端口维度与数据类型。

<img :src="$withBase('/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/JuliaFunction/RightClickMenu.png')" style="width: 700px; height: auto; transform: scale(1);border: 1px solid black;">

弹出的对话框中会列出各个输入输出端口的情况，您可在“数据类型”、“维度”列调整各个端口的数据类型与维度。

数据类型为下拉单选框，其中 inherit 选项表示该端口的数据类型由自动推导得到。
维度为输入框：

- 留空表示该端口数据为标量
- -1 表示该端口的维度由自动推导得到
- [d1,d2,...,dn] 表示该端口的维度为 d1 x d2 x ... x dn，其中 d1, d2, ..., dn 为正整数

输入端口的数据类型与维度支持自动推导（根据与之相连的信号），如您希望使用自动推导，请将数据类型置为“inherit”，维度置为“-1”。

输出端口的数据类型与维度暂不支持自动推导，您需要根据模块输入信号以及 Julia 计算逻辑，自行输入正确的类型与维度。

<img :src="$withBase('/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/JuliaFunction/EditingPorts.png')" style="width: 500px; height: auto; transform: scale(1);border: 1px solid black;">

## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/JuliaFunction_Example.mo">JuliaFunction_Example.mo</helpButton>。

<img :src="$withBase('/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/JuliaFunction/SampleModel.png')" style="width: 700px; height: auto; transform: scale(1);border: 1px solid black;">

JuliaFunction 脚本如下：

```julia
# 主函数
function fcn(x1, x2, x3, x4, x5)
    y1 = x1.fa
    y2 = x1.fb
    y3 = helper(x2, x3)
    y4 = x4
    y5 = [x5.re x5.im]
    return y1, y2, y3, y4, y5
end

# 辅助函数
function helper(u1, u2)
    y = u1 * u2
    return y
end
```

仿真结果如下：

<img :src="$withBase('/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/JuliaFunction/ResultOfSampleModel.png')" style="width: 600px; height: auto; transform: scale(1);border: 1px solid black;">

### 示例说明

- sineWave 模块：生成幅度为 1，频率为 1 的正弦波信号；
- sineWave1 模块：生成幅度为 1，频率为 1 的正弦波信号；
- constant1 模块：生成常量信号，此例中生成的是 3x2 的矩阵；
- constant2 模块：生成常量信号，此例中生成的是 2x1 的矩阵；
- constant3 模块：生成常量信号，此例中生成的是定点类型标量；
- constant4 模块：生成常量信号，此例中生成的是浮点类型标量；
- constant5 模块：生成常量信号，此例中生成的是浮点类型标量；
- realImagToComplex 模块：将 2 个实数信号组合为 1 个复数信号
- juliaFunction 模块：以 Julia 对象所表达的算法，对 3 个输入进行计算，得到 3 个输出；
- outport 模块：计算结果输出端口 1；
- outport1 模块：计算结果输出端口 2；
- outport2 模块：计算结果输出端口 3；
- outport3 模块：计算结果输出端口 4；
- outport4 模块：计算结果输出端口 5。

## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入端口<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

输入端口，指定为标量、向量或矩阵。您创建的每个输入都有一个对应的输入端口。

**依存关系**

要创建输入端口，请双击模块并在 Syslab 的 Julia 函数脚本中，添加函数入口参数。

**数据类型：** inherit | double | float | int8 | uint8 | int16 | uint16 | int32 | uint32 | int64 | uint64 | boolean | Bus | fixedPoint

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 输出端口<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

输出端口，指定为标量、向量或矩阵。您创建的每个输出都有一个对应的输出端口。

**依存关系**

要创建输出端口，请双击模块并在 Syslab 的 Julia 函数脚本中，添加函数返回参数。

**数据类型：** double | float | int8 | uint8 | int16 | uint16 | int32 | uint32 | int64 | uint64 | boolean | fixedPoint

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>端口数据类型 — 指定输入输出端口数据类型<div></div></summary>
</details>
<div class="details-content">

指定此模块输入输出端口可连接信号的数据类型，可选择数据类型：inherit(仅输入端口) | double | float | int8 | uint8 | int16 | uint16 | int32 | uint32 | int64 | uint64 | boolean | Bus(仅输入端口) | fixedPoint

</div>
</div>

<div class="details-box">
<details open>
<summary>端口维度—指定输入输出端口数据维度<div></div></summary>
</details>
<div class="details-content">

指定此模块输入输出端口可连接信号的数据维度。
- 设置端口维度由自动推导得到，请输入 -1 。
- 设置端口维度为标量，请不输入任何字符。
- 设置端口维度为向量，请输入 [d]，d 为正整数。
- 设置端口维度为矩阵，请输入 [d1,d2,d3,...,dn]，其中 d1,d2,d3,...,dn 等均为正整数。 

</div>
</div>

<div class="details-box">
<details open>
<summary>添加触发器 — 创建一个触发信号输入端口<div></div></summary>
</details>
<div class="details-content">

在模块顶部增加一个特殊输入端口，可接收触发信号输入，支持的触发方式包括上升、下降、任一和函数调用四种方式。

</div>
</div>


## 版本历史记录

- 在 2025a 推出，在 2025b 更新

### 限制信息

- 暂不支持输出端口维度与数据类型的推导，需手动配置。
- 暂不支持设置 Paramter Data 参数和 Data Store Memory 参数。
- 暂不支持在同一个 Sysblock 模型中包含重名的 Julia 函数（无论是主函数或辅助函数）。

## 另请参阅

- [JuliaObject](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Utilities/JuliaObject.html)
- [断点调试](/Doc/SyslabIntegration/SyslabDebug.html)