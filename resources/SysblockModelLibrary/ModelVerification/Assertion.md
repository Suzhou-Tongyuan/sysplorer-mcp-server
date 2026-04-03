# Assertion

断言模块，检查信号是否为零

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/ModelVerification/Assertion.png')" style="width: 100px; height: auto;border:solid 1px black;">

**库：** Sysblock / ModelVerification

## 描述

Assertion 模块是用于模型验证和调试的重要工具，其具有一个或两个输入端口，但没有输出端口。当用户将模块参数面板的**错误消息来源选**为**内部**时，模块只有一个输入端口，用于接收断言输入信号。当用户将模块参数面板的**错误消息来源选**为**外部**时，模块有两个输入端口，端口 1 用于接收断言输入信号，端口 2 用于接收断言失败时输出的错误消息。

当断言输入信号中的所有元素全为真时，断言成功，Assertion 模块不执行任何操作。否则，断言失败，Assertion 模块将打印错误消息。若用户勾选了**断言失败时停止仿真**选项，则断言失败后，Assertion 模块将打印错误消息并立即终止仿真。

## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/ModelVerification/Assertion.mo">Assertion.mo</helpButton>。

**示例**

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/ModelVerification/Assertion_example.png')" style="width: 500px; height: auto;border:solid 1px black;">

**参考结果**

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/ModelVerification/Example_output.png')" style="width: 700px; height: auto;border:solid 1px black;">

## 端口

### 输入

<div class="details-box">
  <details open>
  <summary>u1 — 断言输入<div>标量 | 向量 | 矩阵 | 多维数组</div></summary>
  </details>
  <div class="details-content">

断言信号输入，可以为标量、向量、矩阵或多维数组。

 **数据类型：** boolean

</div>
</div>

<div class="details-box">
  <details open>
  <summary>u2 — 错误消息输入<div>标量</div></summary>
  </details>
  <div class="details-content">
错误消息输入，指定为标量。

 **数据类型：** string

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>启用断言 — 启用或禁用断言检查 <div>on (默认) | off</div></summary>
</details>
<div class="details-content">

不勾选此选项将禁用模块，使模型行为与模块不存在时一样。

</div>
</div>

<div class="details-box">
<details open>
<summary>错误消息来源 — 指定断言失败时的错误消息来源<div>内部 (默认) | 外部</div></summary>
</details>
<div class="details-content">


当**错误消息来源**为**内部** 时，用户通过错误消息输入框指定错误消息内容；当**错误消息来源**为**外部** 时，模块会新增一个错误消息端口，用于接收错误消息内容。

</div>
</div>

<div class="details-box">
<details open>
<summary>断言失败时的错误消息 — 指定断言失败时模块输出的错误消息内容<div>"Unexpected value"（默认值）</div></summary>
</details>
<div class="details-content">

仅当**错误消息来源**为**内部**时，此输入框才生效。

</div>
</div>

<div class="details-box">
<details open>
<summary>断言失败时停止仿真 — 指定断言失败时是否立即终止仿真<div>on (默认) | off</div></summary>
</details>
<div class="details-content">

若勾选，断言失败时会输出错误消息并立即终止仿真；若不勾选，断言失败时会输出错误消息，但仿真继续进行。

</div>
</div>

<div class="details-box">
<details open>
<summary>采样时间 — 指定采样时间间隔<div>-1 (默认) | 标量</div></summary>
</details>
<div class="details-content">
 指定采样时间间隔。

</div>
</div>



## 版本历史记录

- 在 2025a 推出


### 限制信息

- 断言输入仅支持 boolean 类型；
- 错误消息输入仅支持 string 类型的标量；
- 模块暂不支持嵌入式代码生成。
