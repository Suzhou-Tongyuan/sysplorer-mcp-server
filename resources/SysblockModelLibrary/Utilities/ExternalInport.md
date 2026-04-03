# ExternalInport
---
&nbsp;

模型导出 FMU 时，可视为顶层输入端口

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/ExternalInport/ExternalInport.jpg')" style="width:200px; border: 1px solid black;">

**库：** Sysblock/Utilities

## 描述

Sysblock 导出 FMU 时，仅能导出位于顶层的输入或输出端口，无法导出位于子系统内部的端口。而 ExternalInport 模块在模型导出 FMU 时，可视为顶层输入端口。无论模块是否位于子系统内部，均能成功导出。

该模块支持同时连接多个输入端口。

## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/ExternalInport.mo">ExternalInport.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/ExternalInport/ExternalInport_example.jpg')" style="width:800px; border: 1px solid black;">

示例模型中，ExternalInport 模块位于子系统内，将该模型导出 FMU。

### 参考结果

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/ExternalInport/ExternalInport_FMU.jpg')" style="width:600px; border: 1px solid black;">



若将 FMU 模型导入回 Sysplorer，可以看出子系统内部的 ExternalInport 模块与子系统外部的 Outport 模块被成功导出，创建连接时可选择相应的端口。

## 端口

### 输出

<div class="details-box">
<details open>
<summary>Port_1 — 输入信号<div>标量 | 向量 | 矩阵 | 多维数组</div></summary>
</details>
<div class="details-content">

可以指定属性的输入信号。  

**数据类型：** double|float|int8|int16|int32|int64|uint8|uint16|uint32|uint64|boolean|fixed point|enum|bus

</div>
</div>

## 信号属性

双击模块打开信号属性面板，可通过表格设置各端口的名称、数据类型和维度。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Utilities/ExternalInport/ExternalInportDialog.png')" style="width:400px; border: 1px solid black;">

### 表格操作

- **添加**：在表格最后一行下方新增一行条目，新增端口的默认值如下：
  - 名称：按顺序依次为 u1、u2、u3...
  - 数据类型：Inherit: auto
  - 维度：-1（表示继承）

- **删除**：选中表格内某一行条目后，删除该行。

- **上移/下移**：选中表格内某一行条目后，调整该行顺序。

::: tip 提示
当没有选中某一行具体条目时，删除、上移、下移按钮均无效。
:::

### 属性说明

<div class="details-box">
<details open>
<summary>名称 — 端口名称<div></div></summary>
</details>
<div class="details-content">

设置端口的名称。

**默认值：** u1、u2、u3...（按添加顺序）

**命名规则：**
- 首字符必须为字母或下划线；
- 后续每个字符必须是字母、数字或下划线；
- 不能为空字符串。

</div>
</div>

<div class="details-box">
<details open>
<summary>数据类型 — 输出数据类型<div></div></summary>
</details>
<div class="details-content">

设置端口输出信号的数据类型。

**数据类型：** Inherit: auto（默认）|double|float|int8|uint8|int16|uint16|int32|uint32|int64|uint64|boolean|fixed point|enum|bus

</div>
</div>

<div class="details-box">
<details open>
<summary>维度 — 端口维度<div></div></summary>
</details>
<div class="details-content">

设置端口输出信号的维度。-1 表示继承。

**取值：** -1（默认）|整数|[整数 , 整数]|[整数 , 整数 , 整数 ...]

</div>
</div>

## 版本历史记录

- 在 2026a 支持多个端口
- 在 2025a 推出

### 限制信息

- 与 Inport 模块不同，该模块位于子系统内部时不会在外部生成相应端口；
- 仅导出 FMU 时模块生效，其余情况模块会被忽略。

