# CANPack
---
&nbsp;

将单个信号打包到报文中

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/CANPack/CANPack.png')" style="width: 200px;border: 1px solid black;">

**库：** Sysblock / Utilities

## 描述

CAN Pack 模块在仿真期间以指定的间隔将信号数据加载到一条 CAN 报文中。并可通过 CAN Unpack 模块输出结果。

## 示例

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/CANPack.mo">CANPack.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/CANPack/CANPack_ex.png')" style="width: 900px; height: auto;border: 1px solid black;">


## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — CAN 报文信号输入<div>标量</div></summary>
</details>
<div class="details-content">


CAN Pack 模块默认有一个输入端口。模块输入的数量是动态的，取决于您为模块指定的信号数量。例如，如果您的报文有四个信号，则该模块可以有四个输入端口。

**数据类型：** double | float | int8 | uint8 | int16 | uint16 | int32 | uint32 | int64 | uint64 | boolean

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>y — CAN 报文输出<div>标量</div></summary>
</details>
<div class="details-content">


该模块有一个输出端口 CAN Msg。CAN Pack 模块接受指定的输入信号并将其打包为一个 CAN 报文。输出数据类型由**作为总线输出**参数设置确定。勾选**作为总线输出**参数，输出类型为 CAN_MESSAGE_BUS。

**数据类型：** CAN_MESSAGE | CAN_MESSAGE_BUS

</div>
</div>




## 参数

<div class="details-box">
<details open>
<summary>数据库文件 — CAN 数据库文件<div></div></summary>
</details>
<div class="details-content">

单击**浏览**以在您的系统上找到数据库文件。数据库文件中指定的报文列表将填充对话框的**报文**部分。数据库文件还会填充所选报文的**信号**表。

包含非字母数字字符（如等号、& 符号等）的文件名不是有效的数据库文件名。在使用数据库文件之前，请重命名那些带有非字母数字字符的名称。

</div>
</div>



<div class="details-box">
<details open>
<summary>报文列表 — CAN 报文列表<div></div></summary>
</details>
<div class="details-content">


在**数据库文件**字段中指定数据库文件后此选项可用。选择要在**信号**表中显示信号详细信息的报文。

</div>
</div>



<div class="details-box">
<details open>
<summary>名称 — CAN 报文名称<div></div></summary>
</details>
<div class="details-content">


指定 CAN 报文的名称。默认值为 CAN Msg。当前直接从数据库文件中获取，不可编辑。

</div>
</div>



<div class="details-box">
<details open>
<summary>标识符类型 — CAN 标识符类型<div></div></summary>
</details>
<div class="details-content">


指定 CAN 报文标识符是 Standard 还是 Extended 类型。默认值为 Standard 。标准标识符是 11 位标识符，扩展标识符是 29 位标识符。当前直接从数据库文件中继承类型，不可编辑。

</div>
</div>



<div class="details-box">
<details open>
<summary>CAN标识符 — CAN 报文 ID<div></div></summary>
</details>
<div class="details-content">


指定 CAN 报文 ID。对于标准标识符，此数字必须是 [0, 2047] 之间的正整数。对于扩展标识符，此数字必须是 [0, 536870911] 之间的正整数。当前直接从数据库文件中获取，不可编辑。

</div>
</div>



<div class="details-box">
<details open>
<summary>长度 — CAN 报文长度<div></div></summary>
</details>
<div class="details-content">


指定 CAN 报文的长度，范围为 0~8 个字节，默认为 8。当前直接从数据库文件中获取，不可编辑。

</div>
</div>



<div class="details-box">
<details open>
<summary>名称 — CAN 报文名称<div></div></summary>
</details>
<div class="details-content">


指定 CAN 报文的名称。默认值为 CAN Msg。当前直接从数据库文件中获取，不可编辑。

</div>
</div>



<div class="details-box">
<details open>
<summary>远程帧 — CAN 报文作为远程帧<div></div></summary>
</details>
<div class="details-content">


将 CAN 报文指定为远程帧。

</div>
</div>



<div class="details-box">
<details open>
<summary>作为总线输出 — CAN 报文作为总线<div></div></summary>
</details>
<div class="details-content">


勾选时可使模块将 CAN 报文作为总线信号输出，输出数据类型为 CAN_MESSAGE_BUS。

</div>
</div>



<div class="details-box">
<details open>
<summary>信号— 报文参数列表<div></div></summary>
</details>
<div class="details-content">


**名称**

为信号指定说明性名称。模块的输入端口标签会显示此名称。

**开始位**

指定数据的开始位。开始位是从报文数据的开头计数的最低有效位。开始位必须是 0~63 之间的整数。

**长度（位）**

指定信号在报文中占用的位数。长度必须是 1~64 之间的整数。

**字节顺序**

选择以下任一选项：

- LE：字节顺序为小端 little-endian 格式。在这种格式中，从最低有效位先存储。

- BE：字节顺序为大端 big-endian 格式。在这种格式中，从最高有效位先存储。

**数据类型**

指定信号如何解释分配的位中的数据。从下列各项中选择：

- signed（默认值）

- unsigned

- float

- double

**多路复用类型**

指定模块在每个时间步将信号打包到 CAN 报文中的方式：

- Standard：在每个时间步都打包信号；
- **多路复用器**：打包**多路复用器**信号，即模式信号。对每条报文，只能指定一个**多路复用器**信号。
- **多路复用**：如果在运行时**多路复用器**信号（模式信号）的值与为此信号配置的**多路复用值**匹配，则打包信号。

例如，一条报文包含下列具有以下类型和值的信号：

| 信号名称 | 多路复用类型 | 多路复用值 |
| -------- | ------------ | ---------- |
| Signal-A | 标准         | 不适用     |
| Signal-B | 多路复用     | 1          |
| Signal-C | 多路复用     | 0          |
| Signal-D | 多路复用器   | 不适用     |

在此示例中：

- 模块在每个时间步中打包 Signal-A（标准信号）和 Signal-D（多路复用器信号）。
- 如果 Signal-D 的值在特定时间步为 1，则模块在该时间步中将 Signal-B 与 Signal-A 和 Signal-D 一起打包。
- 如果 Signal-D 的值在特定时间步为 0，则模块在该时间步中将 Signal-C 与 Signal-A 和 Signal-D 一起打包。
- 如果 Signal-D 的值不是 1 或 0，则模块不会在该时间步中打包任一复用信号。

**多路复用值**

仅当您选择的**多路复用类型**为 Multiplexed 时，此选项才可用。您提供的值必须与运行时的**多路复用器**信号值匹配，模块才会打包**多路复用**信号。**多路复用值**必须是正整数或零。

**因子**

指定将物理值（信号值）转换为报文中打包的原始值时要应用的**因子**值。

**偏移量**

指定将物理值（信号值）转换为报文中打包的原始值时要应用的**偏移量**值。

**最小值、最大值**

定义一个信号值范围。默认设置分别为 -Inf（负无穷）和 Inf。默认情况下，这些设置不会对超过设置的信号值进行裁剪。

</div>
</div>




## 版本历史记录

- 在 2025b 之前推出

### 限制信息

CAN Pack 模块最高支持 64 条信号数据输入。
