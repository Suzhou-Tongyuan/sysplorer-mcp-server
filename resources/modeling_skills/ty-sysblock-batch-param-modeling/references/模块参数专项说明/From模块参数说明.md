# From 模块参数说明

本文档用于说明 `From` 模块的批量参数对象，与参数对话框各项控件之间的对应关系，供调用 `GetModelParamValues` / `SetModelParamValues` 时直接参考。

`From` 当前应按标准模块 `dict` 处理，不要假设它会自动转换成 DataClass。

## 1. 适用场景

- 读取 `From` 当前引用的标签名
- 获取可选标签候选列表（只读）
- 修改 `From` 引用的标签名

## 2. 已确认字段与对话框映射

| 对话框项 | 批量参数对象 key | 类型 | 读写 | 示例值 | 说明 |
| --- | --- | --- | --- | --- | --- |
| 标签名 | `GotoTag` | string | 读写 | `"TAG_A"` | From 模块引用的 Goto 标签名 |
| 可选标签 | `AvailableTags` | array | **只读** | `["TAG_A", "TAG_B"]` | 当前可选的标签列表（来自上层 Goto 定义） |

> 完整对象共 **2 个 key**：`GotoTag`、`AvailableTags`。

## 3. 参考字段说明

- `AvailableTags` 是只读参考字段，仅在读取时输出。
- 它虽在批量参数对象中列出，以便 `GetModelParamValues` 支持按名过滤，但 **`SetModelParamValues` / `SetModelParamValue` 回写时会被拦截并提示只读**，并且如果使用`GetModelParamValue` 获取只读参数的数据时会报**参数不存在**。

## 4. 输入约束

- 底层仅保存标签名，不强制标签必须已经存在对应的 `Goto` 模块。

## 5. 推荐 AI 调用方式

读取当前配置与候选标签：

```python
import mworks.sysplorer as ModelingPy

cfg = ModelingPy.GetModelParamValues("model1", "From1")
print(cfg["GotoTag"])
print(cfg["AvailableTags"])
```

修改引用的标签名：

```python
import copy

new_cfg = copy.deepcopy(cfg)
new_cfg["GotoTag"] = "TAG_B"
ok = ModelingPy.SetModelParamValues("model1", "From1", new_cfg)
print("apply:", ok)
```

## 6. 修改建议

- 只设置 `GotoTag` 字段。
- 不要尝试写入 `AvailableTags`（只读字段，回写会被拦截）。

## 7. 最小校验示例

```python
import mworks.sysplorer as ModelingPy

partial = ModelingPy.GetModelParamValues(
    "model1",
    "From1",
    fields=["GotoTag", "AvailableTags"],
)
print(partial)
```

注意：传入 `fields=[...]` 时，返回值固定为仅包含所请求字段的 `dict`。

## 8. 测试注意点

- 验证写入 `GotoTag` 后读回一致。
- 验证 `AvailableTags` 为只读：回写时被拦截。
- 验证相邻 `Goto` 标签变化后，`AvailableTags` 候选列表同步更新。