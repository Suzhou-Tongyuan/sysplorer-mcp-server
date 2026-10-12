# Goto 模块参数说明

本文档用于说明 `Goto` 模块的批量参数对象，与参数对话框各项控件之间的对应关系，供调用 `GetModelParamValues` / `SetModelParamValues` 时直接参考。

`Goto` 当前应按标准模块 `dict` 处理，不要假设它会自动转换成 DataClass。

## 1. 适用场景

- 读取 `Goto` 当前标签名与标签可见性
- 修改 `Goto` 标签名、标签可见性
- 在保持其余字段不丢失的前提下整体回写配置

## 2. 已确认字段与对话框映射

| 对话框项 | 批量参数对象 key | 示例值 | 说明 |
| --- | --- | --- | --- |
| 标签名 | `GotoTag` | `"TAG_A"` | Goto 标签名 |
| 标签可见性 | `TagVisibility` | `"Global"` | 合法值 `Global` / `Local` / `Scoped` |

> 完整对象共 **2 个 key**：`GotoTag`、`TagVisibility`。无参考字段、无内部处理字段。

## 3. 输入约束

- `TagVisibility` 合法值：`Global` / `Local` / `Scoped`。
- 标签名不能为空，其合法性（标识符、与可见性组合的标签格式）由底层接口校验。

## 4. 顺序敏感行为

- 同时提交 `GotoTag` 与 `TagVisibility` 时，内部**先设置标签名、再设置可见性**。
- 底层设置可见性要求标签名非空；因此需要同时修改两者时，建议一次提交完整字段，避免分两次连续调用导致中间态。
- 只提交 `TagVisibility`（不包含 `GotoTag`）时，保持当前标签名不变。

## 5. 推荐 AI 调用方式

推荐采用"先完整读取，再局部修改，再整体回写"的方式：

```python
import copy
import mworks.sysplorer as ModelingPy

model_name = "model1"
component_name = "Goto1"

cfg = ModelingPy.GetModelParamValues(model_name, component_name)
new_cfg = copy.deepcopy(cfg)

new_cfg["GotoTag"] = "TAG_A"
new_cfg["TagVisibility"] = "Global"

ok = ModelingPy.SetModelParamValues(model_name, component_name, new_cfg)
print("apply:", ok)
```

## 6. 修改建议

- `GotoTag` 与 `TagVisibility` 均可独立提交，也可整体提交。
- 同时修改标签名与可见性时，整体提交最稳妥。
- 标签修改后，相关 `From` 模块的候选标签列表会自动联动更新。

## 7. 最小校验示例

只校验关键字段时，可以在回写后做一次定向读取：

```python
import mworks.sysplorer as ModelingPy

verify = ModelingPy.GetModelParamValues(
    "model1",
    "Goto1",
    fields=["GotoTag", "TagVisibility"],
)
print(verify)
```

注意：传入 `fields=[...]` 时，返回值固定为仅包含所请求字段的 `dict`。

## 8. 测试注意点

- 验证 `Global` / `Local` / `Scoped` 三种可见性均可写入，并读回一致。
- 验证同时提交 `GotoTag` + `TagVisibility` 能成功写入（内部先标签后可见性）。
- 验证非法可见性值被拦截。
- 验证标签为空时设置可见性被拦截。
- 验证标签修改后 `From` 模块候选标签联动同步。