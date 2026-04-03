# CCaller
---
&nbsp;

调用自定义 C 代码中的函数。

**库：** Sysblock/CCaller

<img :src="$withBase('/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/CCaller/CCaller.png')" style="width: 150px; height: auto; transform: scale(1);">

## 描述

### 模块说明

CCaller 模块可在框图建模环境与 C 代码之间建立接口，提供一种可靠的机制供框图模型调用 C 语言编写的函数，进行高效的算法执行和数据交换。

### 基本功能

CCaller 模块可导入并列出外部 C 代码中的函数，用户可选择解析到的 C 函数并集成到框图模型中。CCaller 模块具备端口映射能力，可将 CCaller 模块的输入端口或填写参数映射到 C 函数的输入参数，以及将 C 函数的返回值映射到 CCaller 模块的输出端口。CCaller 模块可自动进行数据格式的转换，例如将框图模型的 Bus 数据格式转换为 C 语言能处理的结构体格式。

## 示例

请参阅 [​使用 CCaller 模块集成 C 代码](/Doc/Sysblock/CreateAndSimulate/ExpandWithCustom/CCallerForC.html)​。


::: warning 注意    
- 若调用外部 C 函数的框图模型出现仿真异常或无法仿真的情况，请参阅[​分析运行时异常](/Doc/Sysblock/Modeling/AnalyzeRedesign/ErrorSystemDiagnosis/AnalyzeRuntimeExceptions.html)​。
- 暂无针对所调用的外部 C 函数实现的正确性与合法性检查，需用户自行保证 C 函数的正确性，包括指针的合法性与有效性。 
::: 

## 端口

### 输入

<div class="details-box">
<details open>
<summary>Port 1<div></div></summary>
</details>
<div class="details-content">

输入端口的数量及其名称是通过外部 C 代码中选定的函数推断出来的。要向 C 函数提供数据，请将输入信号连接到其输入端口。
输入标签的名称与输入端口的名称相同，可通过编辑参数对话框内的 **Modelica 函数信息**下的 **Mo 变量**列进行更改。

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>Port 1<div></div></summary>
</details>
<div class="details-content">

输出端口的数量及其名称是通过外部 C 代码中选定的函数推断出来的。要从 CCaller 模块接收数据，请将一个模块连接到 CCaller 模块的输出端口。
输出标签的名称与输出端口的名称相同，可通过编辑参数对话框内的 **Modelica 函数信息**下的 **Mo 变量**列进行更改。

</div>
</div>


### 支持的数据类型

支持解析的外部 C 函数参数的数据类型，及其与框图环境的映射类型如下：

| C 函数数据类型             | 框图建模环境类型 |
| ------------------------- | ---------------- |
| signed char/unsigned char | int8/uint8       |
|uint/char     |        string 类型和 uint8 数组可以相互切换|
|char           |          uint8               |             
|int/unsigned int     |    int32/uint32          |           
|short/unsigned short  |   int16/uint16             |        
|float          |          float                  |          
|double       |            double             |              
|int8_t/uint8_t      |     int8/uint8            |           
|int16_t/uint16_t     |    int16/uint16            |         
|int32_t/uint32_t      |   int32/uint32            |         
|struct AStruct {...};  |  Bus: Astruct              |       
|enum AnEnum {...};   |    Enum: AnEnum            |    

## 参数

### 指定外部 C 资源文件

#### 从模型配置中添加 C 文件

可通过以下两种方式，打开**模型配置**>**集成 C 代码**编辑页，从模型层级添加 C 资源文件，并在模型中重用这些 C 文件。

1. 从 Sysblock 工具栏**建模**页面，选择**模型配置**，在左侧选择**集成 C 代码**；

2. 从 CCaller 对话框单击**集成 C 设置**。

    <img :src="$withBase('/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/CCaller/CCaller02.png')" style="width: 600px; height: auto; border:solid 1px black;">

|    **分类**      | **内容**               | **查找规则**                                         |
| -------- | ---------------------- | ------------------------------------------------------------ |
| 头文件   | 文件名（.h）             | 模型目录 > Sysplorer 工作目录 > 按顺序查找包含路径 |
| C 文件    | 文件名（.c）             | 模型目录 > Sysplorer 工作目录 > 按顺序查找包含路径 |
| 库文件   | 不带后缀的库名         | 模型目录 > Sysplorer 工作目录 > 按顺序查找包含路径 |
| 包含路径 | 绝对路径或相对模型文件的相对路径 |                                    |

::: tip 提示
可以选中包含路径，通过右键菜单选项转换相对路径/绝对路径；或者勾选**以相对的方式存储路径**，将包含路径全部转换为相对路径。
文件列表中标红的是不存在的文件，可以单击**删除不存在文件**，一键删除不存在的文件。
:::

#### 从 CCaller 对话框添加 C 文件

通过 CCaller 包含文件右侧按钮**选择文件**（`.h/.c`），选择后的文件会自动添加到**模型配置**>**集成 C 代码**编辑页，文件名根据头文件和 C 文件不同分别添加到头文件列表和 C 文件列表，路径以绝对路径方式添加到包含路径下。

<img :src="$withBase('/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/CCaller/CCaller03.png')" style="width: 1000px; border:solid black 1px; height: auto; transform: scale(1);">

### 外部 C 函数信息

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
<summary>函数原型<div></div></summary>
</details>
<div class="details-content">

该字段定义了外部 C 函数的签名，包括返回类型和参数列表，导入外部 C 函数文件解析后通过下拉框选取。

</div>
</div>

### Modelica 函数信息

<div class="details-box">
<details open>
<summary>C 变量<div></div></summary>
</details>
<div class="details-content">

外部 C 函数中使用的变量名。

</div>
</div>

<div class="details-box">
<details open>
<summary>Mo 变量<div></div></summary>
</details>
<div class="details-content">

与 C 变量对应的框图建模中的变量名。

</div>
</div>

<div class="details-box">
<details open>
<summary>IO 类型<div></div></summary>
</details>
<div class="details-content">

描述变量的输入输出类型，并支持参数和表达式选项设置。

### 选项类型

| **选项**      | **功能描述**                                   | **使用场景**             | **C语言示例变量**    |
| ------------- | ---------------------------------------------- | ------------------------ | -------------------- |
| `input`       | 数据传递给 C 函数，仅作为输入使用。            | 初始值或配置参数         | `fValue, nByteOrder` |
| `output`      | 数据从 C 函数返回，外部函数负责修改其值。      | 计算结果返回             | `out`                |
| `inputOutput` | 数据既作为输入又作为输出，函数可读写该变量值。 | 输入初始值并返回计算结果 | `Output`             |
| `parameter`   | 仿真过程中保持固定的全局参数，由用户指定。     | 配置常量或比例因子       | `f64Factor`          |
| `expression`  | 动态计算值，基于表达式或其他输入变量派生得出。 | 中间量或公式派生量       | `nBitSize`           |

::: tip 提示

选项设置为 expression 类型时，若需获取数据的维度信息，可使用 Modelica 内置函数 size()。

对于一维数据 A，使用 size(A,1) 获取其维度信息。

对于二维数据 B，分别使用 size(B,1) 和 size(B,2) 获取其一维和二维的维度信息。

可参考使用示例的说明，[​使用 CCaller 模块集成 C 代码](/Doc/Sysblock/CreateAndSimulate/ExpandWithCustom/CCallerForC.html)​内关于指针参数的内容。
:::

</div>
</div>

<div class="details-box">
<details open>
<summary>数据类型<div></div></summary>
</details>
<div class="details-content">

指定变量的类型，与 C 语言中数据类型对应。

</div>
</div>

<div class="details-box">
<details open>
<summary>维度<div></div></summary>
</details>
<div class="details-content">
指定变量的维度（数组大小或单个变量）。

要继承维度，请将此参数设置为 -1。

#### 支持的维度信息

| **数据类型**      | **维度说明**                                                 |
| ----------------- | ------------------------------------------------------------ |
| `double u`        | 空白标识标量，维度信息不可编辑                               |
| `double* u`       | 标量 /[n] `input/paramter` 类型，**必须指定数据维度或者设置维度为 -1**，否则会报维度不匹配的错误。`output`类型，则需要根据使用情况确认数组维度大小，避免造成内存问题。 |
| `const double* u` | [n] 仅能用于 `input/ouput` 类型，**必须指定数据维度或者设置维度为 -1**，否则会报维度不匹配的错误。 |

</div>
</div>

<div class="details-box">
<details open>
<summary>值<div></div></summary>
</details>
<div class="details-content">

当变量的 IO 类型为 parameter 类型时，指定变量的值。

::: tip 提示

当数据类型为 string 的时候，若想要填写的值为资源文件的路径，可以通过在字符串前添加 "file:///"，将相对于当前模型的文件路径传递给 C 函数。

```
"file:///相对于当前模型的文件路径"
```

:::

</div>
</div>

<div class="details-box">
<details open>
<summary>描述<div></div></summary>
</details>
<div class="details-content">
提供变量的简要说明，便于理解变量的功能和用途。

</div>
</div>

<div class="details-box">
<details open>
<summary>采样时间<div></div></summary>
</details>
<div class="details-content">

采样时间命令点之间的离散间隔，指定采样时间间隔。要继承采样时间，请将此参数设置为 -1。

</div>
</div>


<div class="details-box">
<details open>
<summary>数组布局<div></div></summary>
</details>
<div class="details-content">

用于指定如何排列外部函数调用中涉及的数组数据。

#### 选项

- 缺省（默认值）
  - 说明：数组的布局由工具自动决定，通常根据目标平台的默认设置进行排列（例如内存的排列方式）。
  - 适用场景：当开发者对数组布局没有特殊要求时，选择此项即可让系统根据环境自动处理。
- 行主模式
  - 说明：数组按照**行优先顺序**排列，意味着连续的内存位置存储数组中的行数据。
  - 适用场景：大多数 C 语言和系统的默认内存布局，兼容 C 语言标准。
- 列主模式
  - 说明：数组按照**列优先顺序**排列，意味着连续的内存位置存储数组中的列数据。
  - 适用场景：通常用于 Fortran 等环境的兼容性，因为这些环境使用列优先布局。

#### 示例

假设有一个二维数组：

```C
A = [[1, 2, 3],
     [4, 5, 6],
     [7, 8, 9]]

```


- 行主模式内存顺序

    ```C
    [1, 2, 3, 4, 5, 6, 7, 8, 9]
    ```


- 列主模式内存顺序

    ```C
    [1, 4, 7, 2, 5, 8, 3, 6, 9]
    ```

    在设置 CCaller 模块的数据布局时，开发者应根据外部 C 函数的需求和运行环境选择合适的布局。

</div>
</div>



## 查看 C 文件

可以直接在 CCaller 对话框查看 C 文件，对 C 文件进行编辑，并将编辑内容快速应用到 CCaller 模块设置中。

<img :src="$withBase('/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/CCaller/CCaller05.png')" style="width: 500px; height: auto; border:solid black 1px; transform: scale(1);">

单击 **>>** 按钮，展开 C 文件编辑区域，单击 **<<**，收起该区域。

<img :src="$withBase('/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/CCaller/CCaller06.png')" style="width: 900px; height: auto; border:solid black 1px; transform: scale(1);">

查看 C 文件支持显示模型配置中设置的所有头文件和 C 文件，默认显示当前 CCaller 正在使用的文件。



## 模块升级

针对旧版的 CCaller 模块，可以采用原本的方式继续使用已经搭建好的模块，也可以选择模块升级，将旧版本的模块升级成新的 CCaller 模块。

<img :src="$withBase('/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/CCaller/CCaller04.png')" style="width: 500px; height: auto; border:solid black 1px; transform: scale(1);">

**升级当前模块**：仅升级正在编辑的 CCaller 模块；

**升级所有模块**：升级正常编辑的 CCaller 模块所在模型中所有的 CCaller 模块。



## 版本历史记录

- 增加查看 C 文件；
- 增加外部 C 资源文件进行统一管理；
- 在 2025a 推出；  
- 支持根据函数接口的变量和参数数量，自动缩放模块大小，优化显示效果。

### 限制信息

- 不支持返回值为整型，输入为浮点型的情况。
- 混合建模环境下，物理模型最顶层只允许放一个包含 CCaller 模块的控制策略模型。
- 针对外部 C 函数的错误检查与异常处理的提示信息不足，需用户自行保证所调用C函数的正确性。
- 暂无内存管理机制，数组(指针)类型的返回值必须同时作为输入和输出变量处理，外部 C 函数会修改其内容并返回。
- 外部函数的参数和返回值，仅支持使用同一种类型的浮点数，即调用的函数中，浮点数类型必须统一为 float 或者 double，且在代码生成配置中选择浮点数的类型。


## 相关主题

<!-- 总线和枚举类型介绍链接[外部链接]   -->
[​分析运行时异常​](/Doc/Sysblock/Modeling/AnalyzeRedesign/ErrorSystemDiagnosis/AnalyzeRuntimeExceptions.html)  
[​分析运行时性能​](/Doc/Sysblock/Simulation/OptimizePerformance/ManualPerformance/AnalyzeRuntime.html)  
[​使用 CCaller 模块集成 C 代码​](/Doc/Sysblock/CreateAndSimulate/ExpandWithCustom/CCallerForC.html)<br>
[CCaller仿真错误场景说明](/Doc/Sysblock/CreateAndSimulate/ExpandWithCustom/CCallerErrorMessage.html)
[C 编译器警告信息问题说明](/Doc/Sysblock/Modeling/AnalyzeRedesign/ErrorSystemDiagnosis/CCompilerWarningMessages.html)