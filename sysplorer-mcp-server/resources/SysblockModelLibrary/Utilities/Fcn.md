# Fcn
---
&nbsp;

将指定的数学表达式应用于其输入

**库：** Sysblock模块库 / Utilities

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/Fcn/Fcn.png')" style="width: 100px; height: auto; transform: scale(1);">


## 描述

Fcn模块允许用户将自定义的数学表达式应用于输入信号。与其他模块不同，Fcn模块将输入视为标量或向量，并根据用户定义的表达式进行计算。

Fcn 模块将指定的数学表达式应用于其输入。表达式可以包括以下一个或多个组件：

- u - 模块的输入。如果 u 是向量，则 u(i) 表示向量的第 *i* 个元素；u(1) 或单独一个 u 表示第一个元素；

- 数值常量；

- 算术运算符 (+ - * / ^)；

- 关系运算符 (== != > < >= <=) - 如果关系为 true，则表达式返回 1；否则，返回 0；

- 逻辑运算符 (&& || !) - 如果关系为 true，则表达式返回 1；否则，返回 0；

- 括号；

- 数学函数 - abs、acos、asin、atan、atan2、ceil、cos、cosh、exp、floor、log、log10、power、rem、sgn（等效于 Syslab 中的 sign）、sin、sinh、sqrt、tan 和 tanh。

  

    ::: warning 注意 
    Fcn 模块不支持 round 和 fix。使用 [RoundingFunction](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/RoundingFunction.html) 模块应用这些舍入模式。
    :::

  

- 工作区变量 - 在前面的项目列表中未识别的变量名称传递给 Syslab 进行计算。矩阵或向量元素必须特意引用。例如，对于矩阵中的第一个元素，须使用 A(1,1) 而不是 A。

Fcn 模块遵循以下运算符优先级规则：

1. ( )
2. ^
3. \+ - （一元）
4. !
5. \* /
6. \+ -
7. \> < <= >=
8. == !=
9. &&
10. ||

该表达式不同于 Syslab 表达式，因为该表达式无法执行矩阵计算。此外，此模块不支持冒号运算符 (:)。

模块输入可以是标量或向量。输出始终为标量。对于向量输出，可考虑使用 [MathFunction](/Doc/Sysblock/SysblockBasic/SysblockModelLibrary/MathOperation/MathFunction.html) 模块。如果模块输入是向量，并且函数对输入元素分别进行操作（例如 sin 函数），则该模块只对第一个向量元素进行操作。

### 对模块运算的限制

Fcn 模块不支持矩阵输入，仅支持标量和向量输入。

## 示例

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/Fcn.mo">Fcn.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/Fcn/Fcn_ex.png')" style="width: 400px; height: auto; transform: scale(0.8);">

### 示例说明

- Ramp 模块：提供线性增加的输入信号，用于模拟实际输入值的变化；
- Fcn 模块：允许用户定义一个自定义的 Modelica 表达式来处理输入信号。在这个示例中，我们使用表达式 u + 5 来将输入信号的每个值增加5；
- Scope 模块：用于显示模型的输出结果，即 Fcn 模块处理后的信号。


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

输入信号，指定为标量或向量。

若输入为一个标量，则用u或u(1)表示该标量。


若输入为一个向量，则u(i)表示向量中的第i个元素。


若输入为矩阵，则会发生报错，表达式不支持矩阵的运算。


在模型资源管理器中新建数据字典，并添加变量 constant，值为2，数据类型为 double。

**数据类型：** float | double

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量</div></summary>
</details>
<div class="details-content">

输出信号为经过数学表达式运算后的值，输出数据类型为标量。

**数据类型：** float | double

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>表达式 — 数学表达式<div>sin(u[1] * exp(2.3 * (-u[2])))（默认值）| 自定义表达式</div></summary>
</details>
<div class="details-content">

为模块操作数指定要应用的数学表达式。表达式可以包括以下一个或多个组件：

| 组件       | 描述                                                     |
| :--------- | :------------------------------------------------------- |
| u        | 模块的输入。如果u是向量，则u(i)表示向量的第i个元素。 |
| 数值常量   | 直接使用的数值。                                         |
| 算术运算符 | +、-、*、/、^。                                |
| 关系运算符 | ==、!=、>、<、>=、<=。                       |
| 逻辑运算符 | &&、\|\|、!。                                        |
| 括号       | 用于改变运算优先级。                                     |
| 数学函数   | abs、sin、cos、sqrt等。                          |

</div>
</div>



## 版本历史记录

- 在 2024b 之前推出

### 限制信息

暂不支持自定义采样时间。
