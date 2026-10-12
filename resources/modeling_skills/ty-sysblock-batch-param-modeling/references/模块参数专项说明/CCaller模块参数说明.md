# CCaller 模块参数说明

本文档用于说明 `CCaller` 模块的批量参数对象、界面主要配置项与参数对象字段之间的对应关系，供 `GetModelParamValues` / `SetModelParamValues` 调用时直接参考。

`CCaller` 是当前已确认支持 DataClass 返回的模块类型。完整读取时，不要默认按普通 `dict` 处理。

## 1. 适用场景

- 读取 `CCaller` 当前完整配置并理解其字段结构
- 修改外部 C 函数签名、头文件、采样时间或参数列表后整体回写
- 基于 DataClass 方式访问和修改 `CCaller` 参数对象

## 2. 返回形态

### 2.1 完整读取

```python
cfg = ModelingPy.GetModelParamValues("model1", "CCaller1")
```

当前返回值应按 `ExternalCFunctionConfig` DataClass 处理，可按属性方式访问。

### 2.2 局部字段读取

```python
cfg = ModelingPy.GetModelParamValues(
    "model1",
    "CCaller1",
    fields=["FunctionName", "SampleTime"],
)
```

只要传入 `fields`，返回值固定为 `dict`，不再按 DataClass 返回。

## 3. 当前已确认字段

已确认完整对象至少包含以下字段：

| 字段 | 示例值 | 说明 |
| --- | --- | --- |
| `HeaderFile` | `"sil_momodel.c"` | C 文件或头文件配置 |
| `AvailableFunctions` | `[...]` | 参考字段，表示当前 C 文件内可选的 C 函数列表，不是主要修改字段 |
| `FunctionName` | `"void * memset(void * param1,int param2,unsigned long long param3)"` | 当前选中的 C 函数声明或函数签名 |
| `SampleTime` | `"-1"` | 采样时间 |
| `ArrayLayout` | `""` | 数组布局相关配置 |
| `Arguments` | `[...]` | 函数参数列表 |

## 4. 参考字段说明

### 4.1 `AvailableFunctions`

- `AvailableFunctions` 是参考字段，不是主要修改字段。
- 该字段表示当前 C 文件内可选的 C 函数列表。
- 它主要用于帮助理解当前 `HeaderFile` / C 文件中可以选择哪些函数。
- 正常修改时，应优先通过 `FunctionName` 选择目标函数，并保留 `AvailableFunctions` 原值，不建议主动回写该字段。

## 5. `Arguments` 字段结构

`Arguments` 是一个参数对象列表。当前单个参数对象已确认至少包含以下字段：

| 字段 | 示例值 | 说明 |
| --- | --- | --- |
| `CName` | `"param1"` | 参考字段，表示 C 侧参数名，不是主要修改字段 |
| `MoName` | `"param1"` | 模型侧参数名 |
| `IOType` | `"input"` / `"output"` / `"inputOutput"` | 输入输出方向 |
| `DataType` | `"int32"` | 数据类型 |
| `Dimension` | `""` | 维度定义 |
| `Value` | `""` | 缺省值或当前值 |
| `Description` | `""` | 描述信息 |

### 5.1 `Arguments` 内参考字段说明

- `Arguments[].CName` 是参考字段，不是主要修改字段。
- 它表示当前 C 函数签名里的原始参数名，用于帮助理解参数来源和函数定义。
- 正常修改时，应优先关注 `MoName`、`IOType`、`DataType`、`Dimension`、`Value` 这些和模型映射、方向、类型有关的字段。
- 如果任务没有明确要求调整底层 C 参数名，建议保留 `CName` 原值。

## 6. 输入约束

### 6.1 `ArrayLayout`

- `ArrayLayout` 存在输入约束。
- 合法值仅包括：
  - `""`
  - `"columnMajor"`
  - `"rowMajor"`
- 输入其他值时，应视为无效输入。

## 7. 写回前置条件

`SetModelParamValues` 对 `CCaller` 有额外约束：**`HeaderFile` 必须指向有效的 C 文件，写回才能成功**。在 `HeaderFile` 为空（即模块尚未关联任何 C 文件）的情况下，无论传入 DataClass 对象还是 JSON 字符串，写回均会失败，并返回：

> `"Failed to save CCaller block data."`

此时 `SetModelParamValues` 返回 `False`，模块参数不会被修改，可通过 `GetModelParamValues` 读回验证原值保持不变。

**典型流程**：
1. 先通过界面或 `SetModelParamValue("HeaderFile", ...)` 关联 C 文件
2. 再调用 `GetModelParamValues` 读取完整对象（此时 `AvailableFunctions` 应有内容）
3. 按需修改后，再调用 `SetModelParamValues` 整组回写

## 8. 推荐读改写方式

推荐按“完整读取 -> 修改属性 -> 整组回写”的方式处理：

```python
import mworks.sysplorer as ModelingPy

model_name = "model1"
component_name = "CCaller1"

cfg = ModelingPy.GetModelParamValues(model_name, component_name)

cfg.FunctionName = "int calc_sum(const int *arr, size_t n)"
cfg.SampleTime = "0.01"

ok = ModelingPy.SetModelParamValues(model_name, component_name, cfg)
print("apply:", ok)
```

如果需要修改参数列表，应整体更新 `Arguments`，不要只改局部字段后忽略其余参数对象。

## 9. 修改建议

- 不要把 `AvailableFunctions` 当成主要回写字段，它更适合作为函数选择参考列表使用。
- 修改 `FunctionName` 时，应同步检查 `Arguments` 是否仍与函数签名一致。
- 修改 `Arguments` 时，应把 `CName` 视为参考字段，除非任务明确要求，不建议主动改动。
- 修改 `Arguments` 时，应把参数顺序、方向、数据类型一起检查，不要只改单个字段。
- 修改 `ArrayLayout` 时，只能使用 `""`、`"columnMajor"`、`"rowMajor"` 这几个合法值。
- 需要快速校验时，可在回写后用 `fields=["FunctionName", "SampleTime"]` 做定向读取。

## 10. 最小校验示例

```python
import mworks.sysplorer as ModelingPy

verify = ModelingPy.GetModelParamValues(
    "model1",
    "CCaller1",
    fields=["FunctionName", "SampleTime"],
)
print(verify)
```

注意：这里返回值固定为 `dict`。

## 11. 测试注意点

- `CCaller` 是当前唯一明确支持 DataClass 返回的模块，类名为 `ExternalCFunctionConfig`，来自 `mworks.sysplorer.block_params`，测试时应重点验证这一点。
- 未关联 C 文件时，`HeaderFile`、`FunctionName`、`ArrayLayout` 均为空字符串，`AvailableFunctions` 为空列表，`Arguments` 为空列表；此状态下写回固定失败，错误文案为 `"Failed to save CCaller block data."`。
- 关联 C 文件后，写回测试应覆盖 DataClass 属性修改方式和 JSON 字符串方式两种路径。
- `AvailableFunctions` 应作为参考字段验证存在性，不作为主动修改目标验证。
- `Arguments` 是高风险联动字段，修改函数签名后应重点检查参数列表是否仍匹配。
- `Arguments[].CName` 应作为参考字段验证，不应默认纳入主动修改断言。
- `ArrayLayout` 应增加非法值校验，确认除 `""`、`"columnMajor"`、`"rowMajor"` 外的输入会被拦截或判失败。
