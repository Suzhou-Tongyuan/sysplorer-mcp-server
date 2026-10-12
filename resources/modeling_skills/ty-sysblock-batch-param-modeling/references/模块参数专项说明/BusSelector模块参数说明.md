# BusSelector 模块参数说明

本文档用于说明 `BusSelector` 模块的批量参数对象，与参数对话框各项控件之间的对应关系，供调用 `GetModelParamValues` / `SetModelParamValues` 时参考。

`BusSelector` 当前应按标准模块 `dict` 处理，不要假设它会自动转换成 DataClass。

## 1. 适用场景

- 读取 `BusSelector` 当前完整配置并理解各字段含义
- 按参数对话框含义修改输出信号选择结果
- 调整输出是否为虚拟总线
- 在保留其余字段不丢失的前提下整体回写配置

## 2. 已确认字段与对话框映射

根据当前参数对话框截图和 JSON 参数，可确认映射如下：

| 对话框项 | 批量参数对象 key | 默认初始值 | 说明 |
| --- | --- | --- | --- |
| 总线中的信号 | `AvailableSignals` | `[]`（无连接时） | 参考字段，对应左侧可选信号列表，仅用于展示和选择来源，不是修改字段，不建议主动回写。 |
| 选择的信号 | `OutputSignals` | `["signal1", "signal2"]` | 对应右侧已选输出信号列表，顺序有意义；上移、下移、移除操作最终体现在该字段。 |
| 输出为虚拟总线 | `OutputAsVirtBus` | `"false"` | 对应界面勾选框，建议按字符串布尔值回写，例如 `"true"` / `"false"`。 |

> 完整对象共 **3 个 key**：`AvailableSignals`、`OutputSignals`、`OutputAsVirtBus`。

## 3. 批量接口字段名与单参数接口的差异

`BusSelector` 的批量参数接口与单参数接口使用**不同的字段名**，混用会导致写入无效：

| 字段含义 | 批量接口 key（`GetModelParamValues`） | 单参数接口 key（`SetModelParamValue`） |
|---|---|---|
| 选择的信号列表 | `OutputSignals` | `OutPutSignals`（注意大写 P）|
| 输出为虚拟总线 | `OutputAsVirtBus` | `OutputAsBus` |

调用 `GetModelParamValues` / `SetModelParamValues` 时，应始终使用批量接口字段名，不要按单参数接口字段名臆测。

## 4. 字段使用约束

### 4.1 `AvailableSignals`

- `AvailableSignals` 是参考字段，不是修改字段。
- 它主要对应参数对话框左侧”总线中的信号”列表。
- 该字段用于帮助理解当前输入总线中有哪些可选元素。
- **未连接总线时，该字段为空列表 `[]`**，连接总线后会自动填充为总线中可用的信号名称。
- 回写时应优先保留原值，不建议通过修改该字段来驱动 `BusSelector` 行为变化。

### 4.2 `OutputSignals`

- `OutputSignals` 是主要修改字段。
- 该字段对应参数对话框右侧”选择的信号”列表。
- **默认初始值为 `[“signal1”, “signal2”]`**，表示模块新建时的占位信号名。
- 选择顺序有意义，界面中的上移、下移本质上会改变该数组顺序。
- 如需删除某个输出信号，应直接从该列表中移除对应元素。

### 4.3 `OutputAsVirtBus`

- `OutputAsVirtBus` 对应”输出为虚拟总线”勾选框。
- 修改该字段时，建议连同 `OutputSignals` 一起整体回写。
- 若任务未明确要求调整输出总线形态，建议保持原值。

## 5. 推荐 AI 调用方式

推荐采用“先完整读取，再局部修改，再整体回写”的方式：

```python
import copy
import mworks.sysplorer as ModelingPy

model_name = "model1"
component_name = "BusSelector1"

cfg = ModelingPy.GetModelParamValues(model_name, component_name)
new_cfg = copy.deepcopy(cfg)

new_cfg["OutputSignals"] = ["u5", "u3"]
new_cfg["OutputAsVirtBus"] = "true"

ok = ModelingPy.SetModelParamValues(model_name, component_name, new_cfg)
print("apply:", ok)
```

## 6. 修改建议

- 优先修改 `OutputSignals`，不要把 `AvailableSignals` 当作可写主字段。
- 如需调整输出顺序，应直接调整 `OutputSignals` 中元素顺序。
- 如只修改虚拟总线开关，也建议保留 `AvailableSignals`、`OutputSignals` 等其余字段原值一并回写。
- 对 `BusSelector` 这类列表顺序敏感模块，不建议仅凭多个 `SetModelParamValue(...)` 连续硬写多个字段。

## 7. 最小校验示例

回写后可定向校验关键字段：

```python
import mworks.sysplorer as ModelingPy

verify = ModelingPy.GetModelParamValues(
    "model1",
    "BusSelector1",
    fields=["OutputSignals", "OutputAsVirtBus"],
)
print(verify)
```

注意：传入 `fields=[...]` 时，返回值固定为 `dict`。

## 8. 测试注意点

- **已验证**：批量接口字段名为 `OutputSignals`/`OutputAsVirtBus`，与单参数接口 `OutPutSignals`/`OutputAsBus` 不同，不可混用。
- **已验证**：无总线连接时 `AvailableSignals=[]`（空列表），`OutputSignals` 默认值为 `[“signal1”, “signal2”]`，`OutputAsVirtBus` 默认为 `”false”`。
- **已验证**：将 `OutputAsVirtBus` 修改为 `”true”` 写入成功，读回一致。
- 待验证：连接真实总线后，`AvailableSignals` 填充内容与界面左侧信号列表是否一致。
- 待验证：修改 `OutputSignals` 后，界面右侧”选择的信号”列表内容和顺序是否正确体现。
- 待验证：界面上的上移、下移、移除操作是否最终正确映射到 `OutputSignals` 数组顺序变化。
