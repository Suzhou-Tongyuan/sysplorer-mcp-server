# CoulombandViscousFriction

Coulomb and Viscous Friction 模块对值为零时的不连续性以及非零时的线性增益建模。

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/DiscontinuitiesPng/CoulombandViscousFriction/CVF1.png')" style="width: 100px; border: 1px solid black;">

**库：** Sysblock / Discontinuities

## 描述

Coulomb and Viscous Friction 模块用于对库仑（静态）摩擦和粘性（动态）摩擦进行建模。模块输出结果参考如下公式：

```
y = sign(x) .* (Gain .* abs(x) + Offset)
```

其中 `y` 是输出，`x` 是输入，`Gain` 是粘性摩擦系数，`Offset` 是库仑摩擦值。

## 示例

参考示例模型 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/Discontinuities/CoulombandViscousFriction.mo">CoulombandViscousFriction.mo</helpButton>。

**示例**

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/DiscontinuitiesPng/CoulombandViscousFriction/CVF2.png')" style="width: 500px; border: 1px solid black;">

**参考结果**

<img :src="$withBase('Sysblock/SysblockBasicKnowledge/SysblockModelLibrary/DiscontinuitiesPng/CoulombandViscousFriction/CVF3.png')" style="width: 700px; border: 1px solid black;">

## 端口

### 输入

<div class="details-box">
<details open>
<summary>u — 输入信号<div>标量 | 向量 | 多维数组</div></summary>
</details>
<div class="details-content">
输入信号，允许为实数标量或向量或多维数组。

**数据类型：** double| float | int8 | int16 | int32 | int64 | uint8 | uint16 | uint32 | uint64 | fixed point

</div>
</div>


### 输出

<div class="details-box">
<details open>
<summary>y — 输出信号<div>标量 | 向量 | 多维数组</div></summary>
</details>
<div class="details-content">
输出信号，与输入类型保持一致。

**数据类型：** double| float | int8 | int16 | int32 | int64 | uint8 | uint16 | uint32 | uint64 | fixed point

</div>
</div>

## 参数

<div class="details-box">
<details open>
<summary>库伦摩擦值 — 静态摩擦偏移量<div>[1,3,2,0]（默认） | 标量 | 向量 | 多维数组</div></summary>
</details>
<div class="details-content">
指定应用与所有输入值的偏移量。

</div>
</div>

<div class="details-box">
<details open>
<summary>粘性摩擦系数 — 动态摩擦系数<div>1（默认） | 标量 | 向量 | 多维数组</div></summary>
</details>
<div class="details-content">
指定非零输入值的信号增益。

</div>
</div>

## 版本历史记录

- 在 2025a 推出


### 限制信息

- 输入信号支持 double、int 以及细分类型，不支持总线类型和复数类型；
- 若输入或参数存在数组，则数组维度大小必须相同，且输出信号也为与其具有相同维度大小的数组；
- 不支持在 while / for 子系统中使用；
- 不支持在代数环中使用。
