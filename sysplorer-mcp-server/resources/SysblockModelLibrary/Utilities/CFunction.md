# CFunction
---
&nbsp;

支持将用户编写 C 代码集成外部 C 语言算法。



- **库：** Sysblock/Utilities

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/CFunction/1.png')" style = "width : 200px">

## 描述

CFunction 模块从 Sysblock 模型集成和调用外部 C 代码。使用此模块可定义外部代码，并通过预处理或后处理数据来自定义代码的集成。此外，您还可以为仿真和 C 代码生成指定自定义代码。您可以有条件地调用代码中定义的函数，也可以在一个块中调用多个函数。

## 示例

Constant 模块输出一个长度为 3 的数组数据，Sine 模块输出随时间正弦变化的信号，将两组数据通过 CFunction 编写的算法进行运算后输出。

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/CFunction.mo">CFunction.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/CFunction/2.png')" style="width: 600px; ">

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/CFunction/3.png')" style="width: 600px; border: 1px solid black;">


## 端口

### 输入


<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">
输入端口，指定为标量或向量。您创建的每个输入都有一个对应的输入端口。

**依存关系**

要创建输入端口，请在 CFunction 对话框符号表中，添加函数入口参数。

**数据类型：** double | float | int8 | uint8 | int16 | uint16 | int32 | uint32 | boolean

</div>
</div>


### 输出


<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

输出端口，指定为标量或向量。您创建的每个输出都有一个对应的输出端口。

**依存关系**

要创建输出端口，请在 CFunction 对话框符号表中，添加函数返回参数。

**数据类型：** double | float | int8 | uint8 | int16 | uint16 | int32 | uint32 | boolean

</div>
</div>


## 参数


<div class="details-box">
<details open>
<summary>C 代码 — 编辑 C 代码用来集成外部 C 语言算法<div></div></summary>
</details>
<div class="details-content">

模块在仿真期间每个时间步执行的输出代码，指定为字符向量或字符串标量。例如，使用此参数从外部 C 代码调用函数，对结果进行修改，并执行作以将结果传递给其他模块。

</div>
</div>


<div class="details-box">
<details open>
<summary>端口和参数符号表 — 符号属性表<div></div></summary>
</details>
<div class="details-content">

C 代码中使用的符号和符号属性，指定为表格。您必须在表中输入每个符号的以下属性：

**名字** — 用在 C 代码中的变量或者参数名称。

**IO类型** — 描述变量的输入输出类型，并支持参数选项设置
  - input — 数据传递给 C 函数，仅作为输入使用；
  - output — 数据从 C 函数返回，外部函数负责修改其值；
  - inputOutput — 数据既作为输入又作为输出，函数可读写该变量值；
  - parameter — 仿真过程中保持固定的参数，由用户指定。

</div>
</div>



<div class="details-box">
<details open>
<summary>数据类型 — 指定变量的类型<div></div></summary>
</details>
<div class="details-content">

与 C 语言中数据类型对应。

</div>
</div>

<div class="details-box">
<details open>
<summary>维度 — 指定变量的维度<div></div></summary>
</details>
<div class="details-content">

数组大小或单个变量。支持利用工作区变量进行参数化配置。

</div>
</div>

<div class="details-box">
<details open>
<summary>值<div></div></summary>
</details>
<div class="details-content">

IO 类型为 parameter 时，设置变量的值。支持利用工作区变量进行参数化配置。

</div>
</div>


<div class="details-box">
<details open>
<summary>包含文件<div></div></summary>
</details>
<div class="details-content">

该字段表示所调用的 C 语言函数所在的源文件，需确保路径正确并文件可访问。

</div>
</div>



<div class="details-box">
<details open>
<summary>包含目录<div></div></summary>
</details>
<div class="details-content">

指定包含 C 语言文件的目录路径，编译器会在该目录中查找需要的源文件。

</div>
</div>



<div class="details-box">
<details open>
<summary>库名<div></div></summary>
</details>
<div class="details-content">

指定外部 C 函数需要依赖的动态链接库或静态链接库的名称。

</div>
</div>



<div class="details-box">
<details open>
<summary>库目录<div></div></summary>
</details>
<div class="details-content">

指定库文件所在的目录路径。

</div>
</div>


## 版本历史记录

在 2025a 版本推出


### 限制信息

- 暂不支持端口维度与数据类型的推导，需手动配置；
- 暂不支持 int64、uint64、总线、枚举和定点类型；
- 暂不支持初始化和终止函数。

## 相关主题

[C 编译器警告信息问题说明](/Doc/Sysblock/Modeling/AnalyzeRedesign/ErrorSystemDiagnosis/CCompilerWarningMessages.html)
