# JuliaObject
---
&nbsp;

使用 Syslab 中的 Julia 对象进行动态系统建模和处理流式数据。

**库：** Sysblock 模块库 / Utilities

<img :src="$withBase('/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/JuliaObject/JuliaObjectModuleAppearance.png')" style="width: 200px; height: auto; transform: scale(1);border: 1px solid black;">

## 描述

JuliaObject 将 Syslab 中的 Julia 对象添加到 Sysblock 中，专为仿真输入随时间变化的动态系统而设计，具备以下能力：

- 创建用于算法建模的特定方法和属性；
- 提供了一套结构化的模板流程，可在执行期间自动完成许多管理操作，包括初始化系统、验证数据、单步计算、仿真结束时释放资源等。

::: warning 注意    
在使用 JuliaObject 模块前，请确认以下前提条件被满足，否则 JuliaObject 不可用：
- 当前的 Sysplorer 由相同版本的 Syslab 启动，且当前 Syslab 处于运行状态；
- Sysplorer 的 Syslab Extension for Sysplorer 插件被加载并启用。
::: 

### 为 JuliaObject 模块选择 Julia 对象脚本

双击新创建的 JuliaObject 模块，Julia 对象脚本文件的选择弹框将弹出。您可以单击**新建**按钮以创建一个新的 Julia 对象脚本文件，此时 Syslab 窗口中将打开一个默认的 Syslab 对象模板文件，您可以在此基础上完成您的编码。编码规范详见下节。

您还可以单击右侧的**浏览**按钮选择一个既有的Julia对象脚本文件。

<img :src="$withBase('/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/JuliaObject/SelectingJuliaObjectScriptFile.png')" style="width: 400px; height: auto; transform: scale(1);border: 1px solid black;">

如果您想为一个已经绑定过 Julia 对象脚本文件的 JuliaObject 模块更换脚本文件，可右击该模块，在右键菜单中选择**编辑参数**。

<img :src="$withBase('/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/JuliaObject/RightClickMenu.png')" style="width: 400px; height: auto; transform: scale(1);border: 1px solid black;">

### 编辑 Julia 对象脚本

当您新建 Julia 对象后，将打开一个默认的模板文件，请留意文件注释中的书写规范。

Julia 对象文件中属性分为公共属性 Parameter 和私有属性 Private。

**属性：**

| **属性分类** | **设计用途**               | **特点**    | **支持的数据类型**    |
| ------------ | ------------------------ | --------------------- |--------------------- |
| Parameter    | Julia 对象所描述系统/算法的参数 | 可在 Sysplorer 中赋值（详见后续章节），成员方法可访问 | 基本类型标量，如 gain::Real=1.0 <br>基本类型数组/矩阵，如 gains::Array{Real}=[1 2 3; 4 5 6] <br>自定义类型标量，如 factors::Any=MWStruct(fa=1, fb=[3,2,1])*详见示例模型 |
| Private    | Julia 对象所描述系统/算法的内部状态 | 仅成员方法可访问 | 无限制 |

**方法：**

| **方法**    | **说明**                           |
| ----------- | ---------------------------------- |
| setupImpl   | 执行设置和初始化任务               |
| stepImpl    | 系统输出和状态更新方程             |
| releaseImpl | 释放使用的资源和执行必要的清理任务 |

**端口：**

Julia 对象的 setupImpl、stepImpl 方法将决定其对应的 JuliaObject 模块的输入输出端口情况。

| **端口类型** | **说明**                           |
| ----------- | ---------------------------------- |
| 输入端口   | setupImpl、stepImpl 方法的形参（除 self） |
| 输出端口    | stepImpl 方法的返回值                 |

例如，当您定义了如下的成员方法时：

```julia
function setupImpl(self, u1, u2, u3)
# ...
return nothing

function stepImpl(self, u1, u2, u3)
# ...
return y1, y2
```

其对应的 JuliaObject 模块将具备 3 个输入端口 u1, u2, u3 与 2 个输出端口 y1, y2。

::: warning 注意    
编辑 Julia 对象文件时，请注意以下几点： 
- 请勿删除注释标签，如 # Description、# Methods 等。 
- 请勿删除初始化函数 setupImpl()，单步计算函数 stepImpl()，释放资源函数 releaseImpl()。 
- 类名需要具有唯一性，且与文件名一致。 
- 在修改 Julia 对象脚本并保存后，对应的框图模块不能直接进行仿真，需要进行打开参数对话框或单机对话框的确定按钮操作，使框图模块同步 Julia 对象脚本修改内容。
- setupImpl 与 stepImpl 方法的形参应完全一致。
- 主函数的输出必须使用 return 指定，且必须为函数体中已经出现的变量符号（例如，”return y1, y2”为合法，而“return y1 * 2””return 3+3””return 6”等为非法）。
::: 

**在模型中使用 Julia 对象：**

当您在 Syslab 中完成了 Julia 对象的编辑并保存后，Julia 对象脚本文件的选择弹框将自动填入对应 jl 文件的路径。此时选择确定，即完成了 JuliaObject 模块与 Julia 对象文件的绑定。

<img :src="$withBase('/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/JuliaObject/SavingJuliaObjectFileBinding.png')" style="width: 400px; height: auto; transform: scale(1);border: 1px solid black;">

JuliaObject 模块的输入与输出端口会根据您在 Julia 对象文件中的定义情况自动更新，您可按需将它们连接到其它模块上。

<img :src="$withBase('/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/JuliaObject/SampleModel.png')" style="width: 800px; height: auto; transform: scale(1);border: 1px solid black;">

### 配置 JuliaObject 模块

双击 JuliaObject 模块，将弹出 JuliaObject 模块参数对话框。在参数对话框中，您可以跳转源代码、对模块的端口和参数进行配置。

**跳转到源代码：**

单击“源代码”超链接，即可跳转到 Syslab 中快速打开 Julia 对象脚本。

::: tip 提示

按住 **alt+ctrl** 键，鼠标左键单击 JuliaObject 模块，无需参数对话框也可直接跳转到 Syslab 打开 Julia 对象脚本。

:::

**配置参数：**

参数标签页会列出您在 Julia 对象中`#Parameter`部分声明的成员变量情况。您可在**值**一列为它们赋值，此处赋的值不会影响 Julia 对象对应的`jl`文件内容，并且只对当前 JuliaObject 模块生效。

为参数赋的值应为符合 Sysblock 语义的值表达式，支持引用工作区变量。
特别地，对于自定义类型参数，当前仅支持在 Syslab 中创建这样的变量，同步到 Sysplorer 工作区后，将该变量名赋给对应的参数。参见[工作区同步](/Doc/SyslabIntegration/WorkspaceIntegration.html)。

<img :src="$withBase('/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/JuliaObject/DeclaringMWStruct.png')" style="width: 400px; height: auto; transform: scale(1);border: 1px solid black;"><br>

<img :src="$withBase('/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/JuliaObject/EditingParameters.png')" style="width: 600px; height: auto; transform: scale(1);border: 1px solid black;">

**配置端口：**

端口标签页会列出各个输入输出端口的情况，您可在“数据类型”、“维度”列调整各个端口的数据类型与维度。

数据类型为下拉单选框，其中 inherit 选项表示该端口的数据类型由自动推导得到。
维度为输入框：
- 留空表示该端口数据为标量
- -1 表示该端口的维度由自动推导得到
- [d1,d2,...,dn] 表示该端口的维度为 d1 x d2 x ... x dn，其中 d1, d2, ..., dn 为正整数

输入端口的数据类型与维度支持自动推导（根据与之相连的信号），如您希望使用自动推导，请将数据类型置为“inherit”，维度置为“-1”。

输出端口的数据类型与维度**暂不支持**自动推导，您需要根据模块输入信号以及 Julia 计算逻辑，自行输入正确的类型与维度。

<img :src="$withBase('/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/JuliaObject/EditingPorts.png')" style="width: 600px; height: auto; transform: scale(1);border: 1px solid black;">

## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/JuliaObject_Example.mo">JuliaObject_Example.mo</helpButton>。

<img :src="$withBase('/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/JuliaObject/SampleModel.png')" style="width: 800px; height: auto; transform: scale(1);border: 1px solid black;">

运行示例模型前，请先在 Syslab 中执行以下脚本：
```julia
mygain4 = MWStruct(fa=3,fb=[4 5 6])
```

仿真结果如下：

<img :src="$withBase('/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/JuliaObject/ResultOfSampleModel.png')" style="width: 800px; height: auto; transform: scale(1);border: 1px solid black;">

**Julia 对象脚本**



```julia
using ObjectOriented
@oodef mutable struct SampleSys
    # Description (用于生成Modelica组件描述)
    # Template for syslab object block.

    # Parameter (用于生成 Modelica 组件参数，包括名称、类型、描述)
    # 格式：参数名::参数类型 = 参数值   # 参数注释
    # 例如：
    gain1::Real = 0.3                              # 增益1 (Real标量)
    gain2::Int16 = 5                               # 增益2 (Int16标量)
    gain3::Array{Float32} = [1.1 1.2; 1.3 1.4]     # 增益3 (Float32 2x2 矩阵)
    gain4::Any = MWStruct(fa=2, fb=[3 4 5])        # 增益4 (自定义类型)

    # Private (Julia内部变量)
    # 格式：变量名::类型 = 值   # 变量说明
    # 例如：
    _count::Integer = -1                          # 计数器
    accumulateval::Real = -1                      # 开始到当前时刻输入增益求和的累计结果
    # Methods (主要调用算法，包括setupImpl，stepImpl，releaseImpl)

    # 初始化函数：函数名固定，函数形参与stepImpl函数形参一致
    function setupImpl(self, u1, u2, u3, u4)
        self._count = 0
        self.accumulateval = 0
        # ...
        return nothing
    end #setupImpl

    # 单步计算函数：函数名固定，第一个函数形参必须是self，其余函数形参将作为Modelica组件的输入端口，函数返回值作为输出端口
    function stepImpl(self, u1, u2, u3, u4)
        self._count += 1
        # ...
        self.accumulateval += self.gain1 * u1 + self.gain2 * u2 + self.gain3[1,2] * u3
        y1 = self.accumulateval/self._count
        y2 = self.gain4.fb * u4
        return y1, y2
    end #stepImpl

    # 释放资源函数：函数名固定，且只能有一个函数参数self
    function releaseImpl(self)
        # ...
        return nothing
    end #releaseImpl

    # 其它自定义函数，第一个函数形参数必须是self
    # function xx(self)
    #     ...
    # end

end
```





### 示例说明

- randomNumber 模块：生成均值为 0，方差为 1 且服从正态分布的随机数；
- randomNumber1 模块：生成均值为 0，方差为 1 且服从正态分布的随机数；
- randomNumber2 模块：生成均值为 0，方差为 1 且服从正态分布的随机数；
- constant模块：生成常量信号，此例中生成的是 3x2 的矩阵；
- juliaObject 模块：以 Julia 对象所表达的算法，对 4 个输入进行计算，得到 2 个输出；
- outport 模块：计算结果输出端口 1；
- outport1 模块：计算结果输出端口 2。

## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入端口<div>标量 | 向量 | 矩阵</div></summary>
</details>
<div class="details-content">

输入端口，指定为标量、向量或矩阵。您创建的每个输入都有一个对应的输入端口。

**依存关系**

要创建输入端口，请在 julia 对象脚本的 setupImpl 和 stepImpl 函数，添加函数入口参数。

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

要创建输出端口，请在 julia 对象脚本的 stepImpl 函数，添加函数返回参数。

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
<summary>端口维度 — 指定输入输出端口数据维度<div></div></summary>
</details>
<div class="details-content">

指定此模块输入输出端口可连接信号的数据维度。

- 设置端口维度由自动推导得到，请输入 -1 。
- 设置端口维度为标量，请不输入任何字符。
- 设置端口维度为向量，请输入[d]，d 为正整数。
- 设置端口维度为矩阵，请输入[d1,d2,d3,...,dn]，其中 d1,d2,d3,...,dn 等均为正整数。


</div>
</div>

<div class="details-box">
<details open>
<summary>Julia 对象名称 — Julia 对象名称<div></div></summary>
</details>
<div class="details-content">

指定用户定义的 Julia 对象脚本名称及所在路径，包含文件扩展名。 可以通过以下方式之一来指定 Julia 对象：

- 在文本框中输入带路径的脚本名称。
- 单机文本框旁边的文件夹按钮，浏览包含有效 Julia 对象脚本。

如果您需要创建 Julia 对象，可以通过单击**新建**，使用模板进行创建。

当您保存 Julia 对象脚本之后，名称显示在 JuliaObject 模块名称文本框中。


</div>
</div>

<div class="details-box">
<details open>
<summary>新建 — 从模板创建 Julia 对象<div></div></summary>
</details>
<div class="details-content">

单机 JuliaObject 模块**新建**按钮，会自动跳转到 Syslab 打开新的 Julia 对象脚本。

</div>
</div>


## 版本历史记录

- 在 2025a 推出，在 2025b 更新

### 限制信息

- 暂不支持输出端口维度与数据类型的推导，需手动配置。
- 暂不支持输出 Bus 类型信号。
- 暂不支持仿真执行时框图模块同步脚本修改内容。

## 另请参阅

- [JuliaFunction](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/Utilities/JuliaFunction.html)
- [断点调试](/Doc/SyslabIntegration/SyslabDebug.html)
- [工作区同步](/Doc/SyslabIntegration/WorkspaceIntegration.html)