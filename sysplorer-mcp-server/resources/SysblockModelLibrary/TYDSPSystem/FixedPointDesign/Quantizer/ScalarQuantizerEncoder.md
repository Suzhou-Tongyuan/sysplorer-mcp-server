# ScalarQuantizerEncoder
---
&nbsp;

通过将输入值与用户指定的边界点进行比较，将每个输入值映射到量化区域。

**库：** TYDSPSystem / FixedPointDesign / Quantizer 

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/TYDSPSystem/FixedPointDesign/Quantizer/ScalarQuantizerEncoder/1.png')" style="width: 100px; height: auto; transform: scale(1);">

## 描述

ScalarQuantizerEncoder 模块通过将输入值与边界点参数中定义的量化器边界点进行比较，将每个输入值映射到量化区域。模块输出关联区域的从零开始的索引。

## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div> 实数向量</div></summary>
</details>
<div class="details-content">

输入信号，指定为实数向量。输入数据、边界点、码本值、量化输出值和量化错误无论何时出现，都必须具有相同的数据类型。

**数据类型：** double 

</div>
</div>

### 输出

<div class="details-box">
<details open>
<summary>yout — 输出索引<div>实数向量</div></summary>
</details>
<div class="details-content">
 
索引值，作为与输入数据大小相同的向量返回。

**数据类型：** Int32 

</div>
</div>

<div class="details-box">
<details open>
<summary>quantv — 量化输出<div>实数向量 </div></summary>
</details>
<div class="details-content">

量化输出值，作为与输入数据大小相同的向量返回。这些是对应于每个索引值的码字值。

输入数据、边界点、码本值、量化输出值和量化错误无论何时出现，都必须具有相同的数据类型。

**依赖关系：** 要使用此端口，勾选**输出码字**参数

**数据类型：** double 

</div>
</div>

<div class="details-box">
<details open>
<summary>err — 量化误差<div>实数向量 </div></summary>
</details>
<div class="details-content">

量化误差，作为与输入数据大小相同的向量返回。量化误差是输入值与量化输出值之间的差值。

输入数据、边界点、码本值、量化输出值和量化错误无论何时出现，都必须具有相同的数据类型。

**依赖关系：** 要使用此端口，选择**输出量化误差**参数

**数据类型：** double 

## 参数

</div>
</div>

<div class="details-box">
<details open>
<summary>量化器参数来源  — 量化参数源<div>Specify via dialog（默认）</div></summary>
</details>
<div class="details-content">

使用参数对话框中的参数输入边界点和码字。

</div>
</div>

<div class="details-box">
<details open>
<summary>分区  — 分区方法<div>Bounded（默认）| Unbounded</div></summary>
</details>
<div class="details-content">

指定一种划分方法来解释您输入的边界点：

- Bounded -- 选择此选项可创建有界量化器；

- Unbounded -- 选择此选项可创建无界量化器。

</div>
</div>

<div class="details-box">
<details open>
<summary>边界点  — 边界点<div>1:10（默认）| 实数向量</div></summary>
</details>
<div class="details-content">

按升序输入表示量化器区域边界点的值向量。这些值用于将一组输入数字划分为多个区域。每个区域由索引号指定。

</div>
</div>


<div class="details-box">
<details open>
<summary>码本  — 量化码本<div>1.5:9.5（默认）| 实数向量</div></summary>
</details>
<div class="details-content">

输入与每个指标值对应的量化输出值向量。

如果将**分区**参数设置为 Bounded，并且边界点向量的长度为 N，则必须指定长度为 N−1 的码本。如果将**分区**参数设置为 Unbounded，并且边界点向量的长度为 N，则必须指定长度为 N+1 的码本。

</div>
</div>

<div class="details-box">
<details open>
<summary>搜索方法  — 指定搜索方法<div>Linear（默认）| Binary</div></summary>
</details>
<div class="details-content">

指定块用于确定输入值所在区域的搜索方法（量化索引）：

- Linear --该块将输入值与由前两个边界点定义的第一个区域进行比较。如果输入值不在该区域内，则块将输入值与下一个区域进行比较。这个过程一直持续，直到确定输入值在一个区域内，并与适当的索引值相关联。该过程的计算代价为 P 阶，其中 P 为边界点的个数；

- Binary --  该块将输入值与边界点向量的中间值进行比较。当输入值大于该边界点时，块将丢弃小于该中间值的边界点。然后，块将输入值与由剩余边界点定义的新范围的中间边界点进行比较。这个过程一直持续到输入值与适当的索引值相关联为止。该过程的计算代价为 $\log_{2}{P}$阶，其中 P 为边界点的个数。

</div>
</div>

<div class="details-box">
<details open>
<summary>平局规则  — 边界值重合时索引选取方式<div>Choose the lower index（默认）| Choose the higher index</div></summary>
</details>
<div class="details-content">

指定当输入值与边界点相同时要执行的这些操作之一。该参数决定分配该值的区域。

- Choose the lower index -- 块将输入值分配给较低的索引区域；

- Choose the higher index -- 块将输入值分配给较高索引的区域。

</div>
</div>

<div class="details-box">
<details open>
<summary>输出码字  — 输出码字<div>off（默认）| on</div></summary>
</details>
<div class="details-content">

选择此复选框可输出与端口 quantv 上的每个索引值对应的码字值。

</div>
</div>

<div class="details-box">
<details open>
<summary>输出量化误差  — 输出量化误差<div>off（默认）| on</div></summary>
</details>
<div class="details-content">

选择此复选框可输出端口 err 上每个输入值的量化错误。量化误差是输入值与量化输出值之间的差值。

</div>
</div>

<div class="details-box">
<details open>
<summary>输入信号维度 — 指定输入信号维度<div>{1}（默认）| 长度为 1 的整型向量</div></summary>
</details>
<div class="details-content">

指定输入信号的维度。指定为长度为 1 的整型向量。

</div>
</div>


## 版本历史记录

- 在 2025b 推出

## 限制信息

- 该模块暂不支持自动识别输入信号维度，需通过**输入信号维度**参数手动设定
