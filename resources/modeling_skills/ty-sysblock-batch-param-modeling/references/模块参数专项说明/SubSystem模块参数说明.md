# SubSystem 模块参数说明

本文档用于说明 `SubSystem` 模块的批量参数对象与主要界面配置项之间的对应关系，供 `GetModelParamValues` / `SetModelParamValues` 调用时直接参考。

`SubSystem` 当前应按标准模块 `dict` 处理，不要假设它会自动转换成 DataClass。

## 1. 适用场景

- 读取 `SubSystem` 当前完整参数配置
- 修改子系统常规配置、代码生成相关配置后整组回写
- 验证子系统参数对象在批量读改写流程中是否保持完整

## 2. 返回形态

### 2.1 完整读取

```python
cfg = ModelingPy.GetModelParamValues("model1", "SubSystem1")
```

当前返回值应按 `dict` 处理。

### 2.2 局部字段读取

```python
cfg = ModelingPy.GetModelParamValues(
    "model1",
    "SubSystem1",
    fields=["TreatAsAtomicUnit", "SystemSampleTime"],
)
```

传入 `fields` 时，返回值固定为筛选后的 `dict`。

## 3. 当前已确认字段

已确认完整对象至少包含以下字段：

| 字段 | 默认初始值 | 说明 |
| --- | --- | --- |
| `FunctionFile` | `""` | 代码生成相关文件配置 |
| `FunctionName` | `""` | 代码生成相关函数名配置 |
| `FunctionPackType` | `"FunctionPack.auto"` | 代码生成打包方式；读回值带 `FunctionPack.` 前缀，见第 5 节说明。 |
| `ShowPortLabels` | `"PortName"` | 端口标签显示方式 |
| `SystemSampleTime` | `"-1"` | 子系统采样时间 |
| `TreatAsAtomicUnit` | `"false"` | 是否按原子单元处理 |

> 完整对象共 **6 个 key**，与上表一一对应。

## 4. 字段理解建议

### 4.1 常规配置关注点

| 字段 | 说明 |
| --- | --- |
| `ShowPortLabels` | 影响端口标签显示方式，当前示例值为 `PortName` |
| `SystemSampleTime` | 影响子系统采样时间配置，当前示例值为 `-1` |
| `TreatAsAtomicUnit` | 影响子系统是否按原子单元处理 |

### 4.2 代码生成配置关注点

| 字段 | 说明 |
| --- | --- |
| `FunctionFile` | 与代码生成输出文件相关 |
| `FunctionName` | 与代码生成函数名相关 |
| `FunctionPackType` | 与代码生成打包方式相关，当前示例值为 `FunctionPack.auto` |

### 4.3 生效条件

- 在 `SubSystem` 配置流程内，只有 `TreatAsAtomicUnit="true"` 时，代码生成配置项才有意义。
- 当 `TreatAsAtomicUnit="false"` 时，`FunctionFile`、`FunctionName`、`FunctionPackType` 不应作为主断言对象。

## 5. 输入约束

### 5.1 `FunctionPackType`

- `FunctionPackType` 存在输入约束。
- **读回值带 `FunctionPack.` 前缀**，例如默认值读回为 `"FunctionPack.auto"`。
- 当前已确认的读回值格式：

  | 含义 | 读回值 |
  |---|---|
  | 自动 | `"FunctionPack.auto"` |
  | 内联 | （待补充）|
  | 不可重用 | （待补充）|
  | 可重用 | （待补充）|

- **写入格式待验证**：当前文档列出的 `"auto"`、`"inline"` 等短格式是否能被后端接受，或是否需要带 `FunctionPack.` 前缀，尚未在批量接口层面明确测试。修改 `FunctionPackType` 前，建议先通过 `GetModelParamValues` 读取当前值，再按读回格式类比构造目标值，避免格式不匹配。

### 5.2 `ShowPortLabels`

- `ShowPortLabels` 存在输入约束。
- 合法值包括：
  - `""`
  - `"PortName"`
  - `"PortNumber"`
  - `"SignalName"`
- 输入其他值时，应视为无效输入。

## 6. 推荐读改写方式

推荐按“完整读取 -> 复制对象 -> 修改字段 -> 整组回写”的方式处理：

```python
import copy
import mworks.sysplorer as ModelingPy

model_name = "model1"
component_name = "SubSystem1"

cfg = ModelingPy.GetModelParamValues(model_name, component_name)
new_cfg = copy.deepcopy(cfg)

new_cfg["TreatAsAtomicUnit"] = "true"
new_cfg["SystemSampleTime"] = "0.01"

ok = ModelingPy.SetModelParamValues(model_name, component_name, new_cfg)
print("apply:", ok)
```

## 7. 修改建议

- 修改 `TreatAsAtomicUnit` 时，建议同步检查 `SystemSampleTime` 是否仍符合预期使用场景。
- 如任务涉及代码生成行为，应先确认 `TreatAsAtomicUnit="true"`，再检查 `FunctionFile`、`FunctionName`、`FunctionPackType`。
- 修改 `FunctionPackType` 时，只能使用 `"auto"`、`"inline"`、`"nonreusable"`、`"reusable"` 这些合法值。
- 修改 `ShowPortLabels` 时，只能使用 `""`、`"PortName"`、`"PortNumber"`、`"SignalName"` 这些合法值。
- 如任务只改显示类配置，例如 `ShowPortLabels`，仍建议保留其余字段原值整组回写。

## 8. 最小校验示例

```python
import mworks.sysplorer as ModelingPy

verify = ModelingPy.GetModelParamValues(
    "model1",
    "SubSystem1",
    fields=["TreatAsAtomicUnit", "SystemSampleTime", "ShowPortLabels"],
)
print(verify)
```

注意：这里返回值固定为 `dict`。

## 9. 测试注意点

- **已验证**：`SubSystem` 返回 `dict`，6 个 key，与字段表一致。
- **已验证**：`TreatAsAtomicUnit="true"` 和 `SystemSampleTime="0.01"` 写入成功，读回一致。
- **已验证**：`ShowPortLabels` 默认读回值为 `"PortName"`。
- **已验证**：`FunctionPackType` 默认读回值为 `"FunctionPack.auto"`，带 `FunctionPack.` 前缀。
- 待验证：修改 `FunctionPackType` 时，写入格式是否需要带 `FunctionPack.` 前缀，或短格式（`"auto"`等）是否同样被接受。
- 待验证：`FunctionPackType` 的非法值是否被后端拒绝，错误文案是什么。
- 待验证：`ShowPortLabels` 非法值是否被后端拒绝。
- 待验证：`TreatAsAtomicUnit="true"` 前提下，修改 `FunctionFile`、`FunctionName`、`FunctionPackType` 是否均正常生效。
