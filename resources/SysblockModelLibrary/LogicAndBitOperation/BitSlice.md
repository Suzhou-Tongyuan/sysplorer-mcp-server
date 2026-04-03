# BitSlice
---
&nbsp;

从输入信号返回连续的位域

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/BitSlice/1.jpg')" style="width: 100px; height: auto; transform: scale(1);">

**库：** Sysblock 模块库 / LogicAndBitOperation

## 描述

BitSlice 模块从从输入信号返回连续的位域。通过在 LSB 位置和 MSB 位置参数中使用从零开始的索引来指定位域的下限和上限。对于输入字大小 WS， LSB 位置 和  MSB 位置必须满足以下约束：

```
WS > MSB位置 >= LSB位置 >= 0
```
## 示例

参考模型示例 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/BitSlice.mo">BitSlice.mo</helpButton>。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/BitSlice/2.png')" style="width: 500px; height: auto; transform: scale(1);">

### 参考结果

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/LogicAndBitOperation/BitSlice/3.jpg')" style="width: 800px; height: auto; transform: scale(1);border-top: 1px solid black;">

## 端口

### 输入

<div class="details-box">
<details open>
<summary>Port_1 — 输入信号 <div>标量 | 向量</div></summary>
</details>
<div class="details-content">

输入信号具有最大值为 128。

数据类型：int8 | int16 |int32 | int64| uint8|uint16| uint32| Boolean | fixed point

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>Port_1 — 输出信号<div>标量 | 向量</div></summary>
</details>
<div class="details-content">

输出的字长计算公式为（MSB 位置-LSB 位置） + 1，其中 MSB 位置和 LSB 位置是模块参数。

数据类型： uint8| uint16 | uint32 | uint64 | fixed point

</div>
</div>


## 参数

<div class="details-box">
<details open>
<summary>MSB 位置 —  最高有效位位置<div>7 （默认）</div></summary>
</details>
<div class="details-content">

指定要提取的字段的最高有效位 （MSB） 的位位置 （从零开始）。    
对于输入字大小，MSB 位置必须满足以下约束：WS    
WS > MSB 位置 >= LSB 位置 >= 0

</div>
</div>



<div class="details-box">
<details open>
<summary>LSB 位置 — 最低有效位位置<div>0 （默认）</div></summary>
</details>
<div class="details-content">

指定要提取的字段的最低有效位 （LSB） 的位位置 （从零开始）。    
对于输入字大小 ，LSB 位置必须满足以下约束：WS    
WS > MSB 位置 >= LSB 位置 >= 0

</div>
</div>


## 版本历史记录

- 在 2025a 推出

### 限制信息

- 暂不支持嵌入式代码生成；
- 不支持总线、枚举值类型。