# LookupTableND 模块参数说明

本文档用于说明 `LookupTableND` 模块的批量参数对象，与参数对话框中“表和断点 / 算法 / 数据类型”页签之间的对应关系。

## 1. 适用场景

- 读取和修改 n 维表数据
- 修改多维断点 `Axis1 ... AxisN`
- 配置插值、外插、索引搜索方法
- 配置表数据类型、各断点数据类型、输出类型和中间类型

## 2. 已确认字段与对话框映射

当前可确认映射如下：

| 对话框项 | 批量参数对象 key | 示例值 | 说明 |
|---|---|---|---|
| 表维数 | `N` | `”3”`（默认）| 当前对象中的维数设置；新建模块默认为 `”3”`。 |
| 表数据 | `Table` | `”{{{4, 4}, {16, 16}, {10, 10}}, ...}”` | n 维表值，**使用 Modelica 嵌套大括号格式**。 |
| 断点1 | `Axis1` | `”[10, 22, 31]”` | **使用 Python 中括号格式**，与 Table 不同。 |
| 断点2 | `Axis2` | `”[10, 22, 31]”` | 同上。 |
| 断点3 | `Axis3` | `”[5, 7]”` | 同上。 |
| 断点4 ... 断点N | `Axis4` ... `AxisN` | `”[v1, v2, ...]”` | 其余维度按相同规律扩展；对象中只包含 Axis1 至 AxisN 范围内的字段。 |
| 内插方法 | `InterpolationMethod` | `"线性点-斜率"` | 算法页签中的插值方法。 |
| 外插方法 | `ExtrapolationMethod` | `"裁剪"` | 算法页签中的外插方法。 |
| 索引搜索方法 | `IndexSearchMethod` | `"线性搜索"` | 算法页签中的搜索方法。 |
| 表数据类型 | `TableType` | `"Inherit: sameAsInput"` | 数据类型页签中的表类型。 |
| 表最小值 | `TableMin` | `""` | 表数据最小值。 |
| 表最大值 | `TableMax` | `""` | 表数据最大值。 |
| 断点i数据类型 | `Axis1Type` ... `Axis30Type` | `"Inherit: backPropagation"` | 每个断点各自的数据类型。 |
| 断点i最小值 | `Axis1Min` ... `Axis30Min` | `""` | 每个断点的最小值。 |
| 断点i最大值 | `Axis1Max` ... `Axis30Max` | `""` | 每个断点的最大值。 |
| 分数数据类型 | `FractionType` | `"Inherit: sameAsInput"` | 数据类型页签中的分数类型。 |
| 中间结果数据类型 | `IntermediateResultsType` | `"Inherit: sameAsInput"` | 数据类型页签中的中间类型。 |
| 输出数据类型 | `YType` | `"Inherit: sameAsFirstInput"` | 输出类型。 |
| 输出最小值 | `YMin` | `""` | 输出最小值。 |
| 输出最大值 | `YMax` | `""` | 输出最大值。 |
| 内部规则优先级 | `InternRulePriority` | `"速度"` | 内部规则偏向。 |
| 要求输入同类型 | `RequireInputSameType` | `"true"` | 输入类型一致性开关。 |

## 3. 关键格式说明与行为约束

### 3.1 Axis 断点使用 Python 中括号，Table 使用 Modelica 嵌套大括号

这是 `LookupTableND` 与其他 LookupTable 子类型最容易混淆的差异：

```python
# Table：Modelica 嵌套大括号（与 LookupTable2D 一致）
new_cfg["Table"] = "{{{1, 2}, {3, 4}}, {{5, 6}, {7, 8}}}"

# Axis：Python 中括号（与 LookupTable1D/2D 的断点格式相反）
new_cfg["Axis1"] = "[0, 1]"
new_cfg["Axis2"] = "[0, 5]"
```

混用格式（如将 Axis 写成 `{0, 1}`）可能被后端接受也可能被拒绝，应始终以中括号格式写入 Axis 字段。

### 3.2 对象中只包含当前维度范围内的 Axis 字段

`GetModelParamValues` 返回的对象中，`AxisN` 字段仅包含 `Axis1` 至当前 `N` 值所对应的范围，不会包含更高维度的字段。  
例如 N=3 时，对象总 key 数约为 27，仅包含 `Axis1`、`Axis2`、`Axis3` 及其对应的 Type/Min/Max；`Axis10` 等返回 `None`。

### 3.3 降维时旧 Axis 字段不会自动清空

将 `N` 从较大值改小（如 3→2）时，超出新维度范围的旧 Axis 字段（如原 `Axis3`）**不会被自动清空**，其旧值会保留在对象中。若业务逻辑要求清除，需在写回前手动将其置为空字符串或合适默认值。

## 4. 推荐 AI 调用方式

以下示例基于默认 N=3 的三维查找表（新建模块的默认维数）：

```python
import copy
import mworks.sysplorer as ModelingPy

cfg = ModelingPy.GetModelParamValues("model1", "LookupTableND1")
new_cfg = copy.deepcopy(cfg)

# N=3：三维，Table 为 3×3×2，Axis1/2 各 3 个元素，Axis3 为 2 个元素
new_cfg["N"] = "3"
new_cfg["Table"] = "{{{4, 4}, {16, 16}, {10, 10}}, {{5, 5}, {19, 19}, {18, 18}}, {{6, 6}, {20, 20}, {23, 23}}}"
new_cfg["Axis1"] = "[10, 22, 31]"   # Python 中括号格式
new_cfg["Axis2"] = "[10, 22, 31]"
new_cfg["Axis3"] = "[5, 7]"
new_cfg["InterpolationMethod"] = "线性点-斜率"
new_cfg["ExtrapolationMethod"] = "裁剪"
new_cfg["IndexSearchMethod"] = "线性搜索"
new_cfg["TableType"] = "Inherit: sameAsInput"
new_cfg["YType"] = "Inherit: sameAsFirstInput"

ok = ModelingPy.SetModelParamValues("model1", "LookupTableND1", new_cfg)
print("apply:", ok)
```

## 5. 修改建议

- 修改 `N` 时，必须同步调整 `Table` 和 `Axis1 ... AxisN` 的维度，使其与新 `N` 值匹配。
- **降维（N 减小）时**，超出新维度范围的旧 Axis 字段不会自动清空；如有必要，应手动清除。
- 修改某个 `AxisiType` 时，通常应保留对应的 `AxisiMin` / `AxisiMax` 原值一起回写。
- `RequireInputSameType`、`FractionType`、`IntermediateResultsType`、`InternRulePriority` 这类类型和规则字段建议保留原值，除非用户明确要求修改。
- **Axis 断点始终用 Python 中括号** `[v1, v2, ...]`；Table 始终用 Modelica 嵌套大括号 `{...}`。

## 6. 最小校验示例

```python
import mworks.sysplorer as ModelingPy

verify = ModelingPy.GetModelParamValues(
    "model1",
    "LookupTableND1",
    fields=[
        "N",
        "Table",
        "Axis1",
        "Axis2",
        "Axis3",
        "InterpolationMethod",
        "ExtrapolationMethod",
        "IndexSearchMethod",
        "TableType",
        "YType",
    ],
)
print(verify)
```
