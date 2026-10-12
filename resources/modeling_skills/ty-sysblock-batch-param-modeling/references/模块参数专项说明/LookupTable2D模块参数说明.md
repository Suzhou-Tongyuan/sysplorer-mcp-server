# LookupTable2D 模块参数说明

本文档用于说明 `LookupTable2D` 模块的批量参数对象，与参数对话框中“值域和定义域 / 算法 / 数据信息”三个页签之间的对应关系。

## 1. 适用场景

- 读取二维查找表值、行断点、列断点
- 修改二维查表的内插方式
- 配置输出数据类型，以及表值和断点的最小值/最大值

## 2. 已确认字段与对话框映射

当前可确认映射如下：

| 对话框项 | 批量参数对象 key | 示例值 | 说明 |
|---|---|---|---|
| 值域 | `Table` | `"{{1, 5, 20, 35}, {3, 5, 6, 35}, ...}"` | 二维表数据。 |
| 定义域(行索引) | `BreakpointsForDimension1` | `"{0.0, 1.0, 2.0, 3.0, 4.0, 5.0}"` | 行断点。 |
| 定义域(列索引) | `BreakpointsForDimension2` | `"{0.0, 1.0, 2.0, 3.0}"` | 列断点。 |
| 内插方法 | `InterpMethod` | `"均一"` | 算法页签中可见。 |
| 值域最小值 | `TableMin` | `""` | 表值下限。 |
| 值域最大值 | `TableMax` | `""` | 表值上限。 |
| 定义域行最小值 | `BreakpointsForDimension1Min` | `""` | 行断点下限。 |
| 定义域行最大值 | `BreakpointsForDimension1Max` | `""` | 行断点上限。 |
| 定义域列最小值 | `BreakpointsForDimension2Min` | `""` | 列断点下限。 |
| 定义域列最大值 | `BreakpointsForDimension2Max` | `""` | 列断点上限。 |
| 输出数据类型 | `OutDataType` | `"Inherit: sameAsFirstInput"` | 数据信息页签中的输出类型。 |

## 3. 与其他 LookupTable 子类型的差异

- 当前对象**没有** `ExtrapMethod` 和 `IndexSearchMethod` 字段，与 `LookupTable1D` 不同，不要强行补写。
- 输出数据类型字段名为 `OutDataType`，**不是** `LookupTable1D` 使用的 `OutDataTypeStr`，混用会导致写回无效。
- 内插方法字段名为 `InterpMethod`，与 `LookupTableND` 使用的 `InterpolationMethod` 不同。
- 对 AI 来说，应以实际 `GetModelParamValues(...)` 返回的 key 为准，不要按其他子类型臆测字段。

## 4. 维度一致性校验

后端在写回时会校验 `Table` 的行列尺寸与两组断点长度是否匹配。若不一致，`SetModelParamValues` 返回 `False`，`GetLastErrors()` 报告：

> `无效输入"值域应为二维数组，且第一个维度应等于定义域（行）的长度，第二个维度应等于定义域（列）的长度！"。`

**修改规则**：
- `Table` 行数 = `BreakpointsForDimension1` 元素数
- `Table` 列数 = `BreakpointsForDimension2` 元素数
- 三者必须同步修改，不能只改其中一项。

## 5. 推荐 AI 调用方式

```python
import copy
import mworks.sysplorer as ModelingPy

cfg = ModelingPy.GetModelParamValues("model1", "LookupTable2D1")
new_cfg = copy.deepcopy(cfg)

new_cfg["Table"] = "{{1, 5, 20, 35}, {3, 5, 6, 35}, {5, 2, 25, 2}, {4, 5, 8, 50}, {5, 3, 2, 3}, {6, 30, 22, 80}}"
new_cfg["BreakpointsForDimension1"] = "{0.0, 1.0, 2.0, 3.0, 4.0, 5.0}"
new_cfg["BreakpointsForDimension2"] = "{0.0, 1.0, 2.0, 3.0}"
new_cfg["InterpMethod"] = "均一"
new_cfg["OutDataType"] = "Inherit: sameAsFirstInput"

ok = ModelingPy.SetModelParamValues("model1", "LookupTable2D1", new_cfg)
print("apply:", ok)
```

## 6. 修改建议

- 修改 `Table` 时，必须同步修改 `BreakpointsForDimension1` 和 `BreakpointsForDimension2` 以保持尺寸一致，否则后端会拒绝整次写入。
- 修改 `OutDataType` 时，保留所有 Min/Max 字段原值一起回写。
- 如果界面里某些算法项灰掉，但对象中没有对应 key，不要强行补写。

## 7. 最小校验示例

```python
import mworks.sysplorer as ModelingPy

verify = ModelingPy.GetModelParamValues(
    "model1",
    "LookupTable2D1",
    fields=[
        "Table",
        "BreakpointsForDimension1",
        "BreakpointsForDimension2",
        "InterpMethod",
        "OutDataType",
    ],
)
print(verify)
```
