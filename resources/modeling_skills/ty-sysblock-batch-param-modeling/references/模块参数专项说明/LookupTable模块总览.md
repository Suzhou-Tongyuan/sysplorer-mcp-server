# LookupTable 模块参数总览

本文档用于汇总 `LookupTable` 系列模块的批量参数对象说明，作为 AI 调用 `GetModelParamValues` / `SetModelParamValues` 时的总入口。

## 1. 适用范围

当前已补充以下模块类型：

- `LookupTable1D`
- `LookupTable2D`
- `LookupTableDynamic`
- `LookupTableND`

每个 JSON 文件对应一个具体模块类型，建议按模块类型分别读取说明，不要把不同类型的字段直接混用。

## 2. 共通规则

- `LookupTable` 系列当前都按标准模块 `dict` 处理，不要假设会自动转成 DataClass。
- 优先使用 `GetModelParamValues(...) -> 修改 dict -> SetModelParamValues(...)` 的整对象回写流程。
- `Table`、断点、算法、输出数据类型、最小值/最大值等字段通常存在联动，修改其中一项时要注意相关字段是否也需要同步更新。
- 如果只需要核对关键字段，可在回写后通过 `fields=[...]` 做最小化校验；此时返回值固定为 `dict`。
- **各子类型之间字段名不完全一致**，应以实际 `GetModelParamValues(...)` 返回的 key 为准，不要跨类型推测字段名。典型差异：`OutDataTypeStr`（1D）vs `OutDataType`（2D、ND）；`InterpMethod`（1D/2D）vs `InterpolationMethod`（ND）；1D/2D 无 `Axis` 字段而 ND 有。

## 3. 分模块参考文档

- `references/模块参数专项说明/LookupTable1D模块参数说明.md`
- `references/模块参数专项说明/LookupTable2D模块参数说明.md`
- `references/模块参数专项说明/LookupTableDynamic模块参数说明.md`
- `references/模块参数专项说明/LookupTableND模块参数说明.md`

## 4. 数值格式对照（各子类型差异）

`Table` 与断点字段的数值格式因子类型而异，混用格式将被后端拒绝：

| 子类型 | Table 格式 | 断点格式 | 说明 |
|---|---|---|---|
| `LookupTable1D` | `"{v1, v2, ...}"` | `"{v1, v2, ...}"` | 均用 Modelica 大括号 |
| `LookupTable2D` | `"{{r1c1, ...}, {r2c1, ...}}"` | `"{v1, v2, ...}"` | Table 嵌套双括号，断点同 1D |
| `LookupTableND` | `"{{{...}, ...}, ...}"` | `"[v1, v2, ...]"` | **AxisN 断点用 Python 中括号**，Table 仍用 Modelica 嵌套大括号 |
| `LookupTableDynamic` | 无（运行时动态传入） | 无 | 只有查找方法和输出类型两个字段 |

> `LookupTableND` 的 `Axis` 断点格式与其他三种模块相反，是最容易出错的跨类型混用点。

## 5. 通用读改写示例

```python
import copy
import mworks.sysplorer as ModelingPy

model_name = "model1"
component_name = "LookupTable1D1"

cfg = ModelingPy.GetModelParamValues(model_name, component_name)
new_cfg = copy.deepcopy(cfg)

# LookupTable1D 的 Table 和断点均用 Modelica 大括号格式
new_cfg["Table"] = "{10, 20, 30, 40}"
new_cfg["BreakpointsForDimension1"] = "{0, 1, 2, 3}"

ok = ModelingPy.SetModelParamValues(model_name, component_name, new_cfg)
print("apply:", ok)
```

## 7. 选择说明文档的建议

- 模块名里带 `1D` 时，优先看 `LookupTable1D模块参数说明.md`
- 模块名里带 `2D` 时，优先看 `LookupTable2D模块参数说明.md`
- 模块名里带 `Dynamic` 时，优先看 `LookupTableDynamic模块参数说明.md`
- 模块名里带 `ND` 时，优先看 `LookupTableND模块参数说明.md`

如果用户只说“LookupTable”，但没有说明具体类型，AI 应先确认实际模块类型或先读取完整参数对象后再决定引用哪份说明。
