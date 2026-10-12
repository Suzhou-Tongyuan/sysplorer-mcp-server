# LookupTableDynamic 模块参数说明

本文档用于说明 `LookupTableDynamic` 模块的批量参数对象，与参数对话框中“主要 / 信号属性”页签之间的对应关系。

## 1. 适用场景

- 配置动态查找表的查找方法
- 配置动态查找表输出数据类型

## 2. 已确认字段与对话框映射

当前可确认映射如下：

| 对话框项 | 批量参数对象 key | 默认初始值 | 说明 |
|---|---|---|---|
| 查找方法 | `Combobox_0` | `"插值-使用最终值"` | 主要页签中的查找方式，枚举值，后端有合法性校验。 |
| 输出数据类型 | `DataTypeHelper` | `"double"` | 信号属性页签中的输出类型。 |

> **注意**：文档原示例值 `"内插-外插"` 是可设置的合法值之一，但模块的**默认初始值**为 `"插值-使用最终值"`。

## 3. Combobox_0 输入约束

`Combobox_0` 是枚举字段，后端会校验合法性：输入非法字符串时 `SetModelParamValues` 返回 `False`，`GetLastErrors()` 报告：

> `无效输入"<输入值>"。`

且原值保持不变，不会被覆盖。

当前已确认合法值：

| 合法值 | 含义 |
|---|---|
| `"插值-使用最终值"` | 默认初始值 |
| `"内插-外插"` | 内插并外插 |

其余合法值需从界面下拉列表中读取，不可随意猜测。

## 4. 推荐 AI 调用方式

```python
import copy
import mworks.sysplorer as ModelingPy

cfg = ModelingPy.GetModelParamValues("model1", "LookupTableDynamic1")
new_cfg = copy.deepcopy(cfg)

new_cfg["Combobox_0"] = "内插-外插"
new_cfg["DataTypeHelper"] = "uint32"

ok = ModelingPy.SetModelParamValues("model1", "LookupTableDynamic1", new_cfg)
print("apply:", ok)
```

## 5. 修改建议

- `LookupTableDynamic` 当前对象很小，但仍建议完整读取后回写，避免未来版本扩展字段时被覆盖。
- `Combobox_0` 是通用控件名，不具备语义可读性；AI 写回时应通过本说明把它视为”查找方法”字段。
- 如果用户只描述界面文案而没提供 key，应优先按本映射转换，而不是猜测更语义化的字段名。
- 修改 `Combobox_0` 前，应确认目标值是已知合法枚举，不要直接传入未经确认的字符串。

## 6. 最小校验示例

```python
import mworks.sysplorer as ModelingPy

verify = ModelingPy.GetModelParamValues(
    "model1",
    "LookupTableDynamic1",
    fields=["Combobox_0", "DataTypeHelper"],
)
print(verify)
```
