# LookupTable1D 模块参数说明

本文档用于说明 `LookupTable1D` 模块的批量参数对象，与参数对话框中“值域和定义域 / 算法 / 数据信息”三个页签之间的对应关系。

## 1. 适用场景

- 读取一维查找表当前表值与断点
- 修改内插、外插、索引搜索方式
- 配置输出数据类型、值域和定义域最小值/最大值

## 2. 已确认字段与对话框映射

当前可确认映射如下：

| 对话框项 | 批量参数对象 key | 示例值 | 说明 |
|---|---|---|---|
| 值域 | `Table` | `"{1, 10, 7, 12, 16}"` | 一维表数据。 |
| 定义域 | `BreakpointsForDimension1` | `"{5, 6, 7, 11, 30}"` | 一维断点数据。 |
| 内插方法 | `InterpMethod` | `"线性点-斜率"` | 算法页签中的插值方式。 |
| 外插方法 | `ExtrapMethod` | `"线性"` | 算法页签中的外插方式。 |
| 索引搜索方法 | `IndexSearchMethod` | `"线性搜索"` | 算法页签中的搜索方式。 |
| 值域最小值 | `TableMin` | `""` | 数据信息页签中的下限。 |
| 值域最大值 | `TableMax` | `""` | 数据信息页签中的上限。 |
| 定义域最小值 | `BreakpointsForDimension1Min` | `""` | 断点最小值。 |
| 定义域最大值 | `BreakpointsForDimension1Max` | `""` | 断点最大值。 |
| 输出数据类型 | `OutDataTypeStr` | `"Inherit: sameAsInput"` | 数据信息页签中的输出类型。 |

## 3. 输入格式约束

### 3.1 Table 与断点必须使用 Modelica 大括号格式

`Table` 和 `BreakpointsForDimension1` 的值必须写成 Modelica 集合格式 `{v1, v2, ...}`，不能使用 Python 列表格式 `[v1, v2, ...]`。

```python
# 正确
new_cfg["Table"] = "{0, 5, 15, 30, 50}"
new_cfg["BreakpointsForDimension1"] = "{0, 1, 2, 3, 4}"

# 错误 —— 后端会拒绝并返回 False
new_cfg["Table"] = "[0, 5, 15, 30, 50]"
```

使用错误格式时 `SetModelParamValues` 返回 `False`，`GetLastErrors()` 报告：
> `无效输入"定义域和值域应为长度大于 1 的一维数组！"。`

### 3.2 数组长度要求

`Table` 与 `BreakpointsForDimension1` 的元素数量须大于 1 且相互匹配；后端在写回时统一校验。

## 4. 推荐 AI 调用方式

```python
import copy
import mworks.sysplorer as ModelingPy

cfg = ModelingPy.GetModelParamValues("model1", "LookupTable1D1")
new_cfg = copy.deepcopy(cfg)

new_cfg["Table"] = "{1, 10, 7, 12, 16}"
new_cfg["BreakpointsForDimension1"] = "{5, 6, 7, 11, 30}"
new_cfg["InterpMethod"] = "线性点-斜率"
new_cfg["ExtrapMethod"] = "线性"
new_cfg["IndexSearchMethod"] = "线性搜索"
new_cfg["OutDataTypeStr"] = "Inherit: sameAsInput"

ok = ModelingPy.SetModelParamValues("model1", "LookupTable1D1", new_cfg)
print("apply:", ok)
```

## 5. 修改建议

- 修改 `Table` 时，建议同步确认 `BreakpointsForDimension1` 的长度与语义是否匹配。
- 修改 `OutDataTypeStr` 时，建议同时保留 `TableMin` / `TableMax` / `BreakpointsForDimension1Min` / `BreakpointsForDimension1Max` 原值一起回写。
- 如果只想试算法切换，也建议以完整对象回写，避免丢掉数值边界字段。

## 6. 最小校验示例

```python
import mworks.sysplorer as ModelingPy

verify = ModelingPy.GetModelParamValues(
    "model1",
    "LookupTable1D1",
    fields=[
        "Table",
        "BreakpointsForDimension1",
        "InterpMethod",
        "ExtrapMethod",
        "IndexSearchMethod",
        "OutDataTypeStr",
    ],
)
print(verify)
```
