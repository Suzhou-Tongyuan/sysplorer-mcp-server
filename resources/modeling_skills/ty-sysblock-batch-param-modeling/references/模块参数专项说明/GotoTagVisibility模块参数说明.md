# GotoTagVisibility 模块参数说明

本文档用于说明 `GotoTagVisibility` 模块的批量参数对象，与参数对话框各项控件之间的对应关系，供调用 `GetModelParamValues` / `SetModelParamValues` 时直接参考。

`GotoTagVisibility` 当前应按标准模块 `dict` 处理，不要假设它会自动转换成 DataClass。

## 1. 适用场景

- 读取 `GotoTagVisibility` 的标签名
- 设置 `GotoTagVisibility` 的标签名

## 2. 已确认字段与对话框映射

| 对话框项 | 批量参数对象 key | 类型 | 示例值 | 说明 |
| --- | --- | --- | --- | --- |
| 标签名 | `GotoTag` | string | `"TAG_A"` | 标签名 |

> 完整对象共 **1 个 key**：`GotoTag`。

## 3. 内部处理字段

- 该模块的作用域固定为组件所在层次前缀，可见性固定为 `Scoped`。
- 作用域与可见性由模块内部处理，**不向调用方暴露**，用户只能设置标签名 `GotoTag`。

## 4. 推荐 AI 调用方式

```python
import copy
import mworks.sysplorer as ModelingPy

model_name = "model1"
component_name = "GotoTagVisibility1"

cfg = ModelingPy.GetModelParamValues(model_name, component_name)
new_cfg = copy.deepcopy(cfg)
new_cfg["GotoTag"] = "TAG_A"

ok = ModelingPy.SetModelParamValues(model_name, component_name, new_cfg)
print("apply:", ok)
```

## 5. 修改建议

- 仅设置 `GotoTag` 字段，不要尝试写入其他字段。
- 标签修改后，相关 `Goto` / `From` 模块的标签与可见性会联动更新。

## 6. 最小校验示例

```python
import mworks.sysplorer as ModelingPy

partial = ModelingPy.GetModelParamValues(
    "model1",
    "GotoTagVisibility1",
    fields=["GotoTag"],
)
print(partial)
```

注意：传入 `fields=[...]` 时，返回值固定为仅包含所请求字段的 `dict`。

## 7. 测试注意点

- 验证 `GotoTag` 可写入，并读回一致。
- 验证未知参数名、空标签被拦截。
- 验证作用域固定为组件所在层次前缀、可见性固定为 `Scoped`，不对外暴露。