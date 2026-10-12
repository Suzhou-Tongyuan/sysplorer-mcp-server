# BusCreator 模块参数说明

本文档用于说明 `BusCreator` 模块的批量参数对象，与参数对话框各项控件之间的对应关系，供调用 `GetModelParamValues` / `SetModelParamValues` 时直接参考。

`BusCreator` 当前应按标准模块 `dict` 处理，不要假设它会自动转换成 DataClass。

## 1. 适用场景

- 读取 `BusCreator` 当前完整配置并理解每个字段含义
- 按参数对话框含义修改输入数目、输出数据类型
- 在保持其余必要字段不丢失的前提下整体回写配置

## 2. 已确认字段与对话框映射

当前可确认映射如下：

| 对话框项 | 批量参数对象 key | 默认初始值 | 说明 |
| --- | --- | --- | --- |
| 输入的数目 | `InputsNum` | `"2"` | 建议以字符串形式回写；修改此字段即可调整信号数量，模块会自动同步端口。 |
| 输出数据类型 | `OutDataTypeStr` | `"inherit: auto"` | 支持简化输入（见第 3 节）；读回值始终为全量字符串形式。 |
| 使用信号线名称，而不是端口名称 | `ShowSignalNames` | `"true"` | 选中时，优先使用信号线名称生成总线元素名称；默认已开启。 |

> 完整对象共 **3 个 key**：`InputsNum`、`OutDataTypeStr`、`ShowSignalNames`。`PortConfig`、`BusTypeIsAuto` 和 `BusTypeName` 是内部处理字段，不出现在批量参数对象中，也不应手动写入。

## 3. `OutDataTypeStr` 输入规则

根据当前数据类型下拉数据，`OutDataTypeStr` 支持简化输入，内部会自动处理，也支持全量输入。

### 3.1 `auto` 简化输入（已验证）

- 输入 `auto` 时，内部自动规范化为 `”inherit: auto”`，**读回值为全量字符串 `”inherit: auto”`**，而非 `”auto”`。
- 如果任务语义只是”继承自动”，优先推荐写 `auto`，更简洁。
- 当然也支持直接写全量值 `”inherit: auto”`。

### 3.2 总线类型名简化输入

- 输入 `Bus1` 这类总线类型名时，内部会自动按总线类型处理。
- 从界面下拉来看，其完整展示形式可能类似 `Bus: Bus1`。
- 如果任务已经明确总线类型名，直接写类型名本身即可，例如 `Bus1`。
- 当然也支持写全量形式，例如 `Bus: Bus1`。

### 3.3 全量输入

- 若调用方已经拿到界面或对象中的完整字符串，也可以直接按全量值回写。
- 当前已明确支持的全量示例包括：
  - `"inherit: auto"`
  - `"Bus: Bus1"`

## 4. 推荐 AI 调用方式

推荐采用”先完整读取，再局部修改，再整体回写”的方式：

```python
import copy
import mworks.sysplorer as ModelingPy

model_name = “model1”
component_name = “BusCreator1”

cfg = ModelingPy.GetModelParamValues(model_name, component_name)
new_cfg = copy.deepcopy(cfg)

new_cfg[“InputsNum”] = “4”
new_cfg[“OutDataTypeStr”] = “auto”
new_cfg[“ShowSignalNames”] = “true”

ok = ModelingPy.SetModelParamValues(model_name, component_name, new_cfg)
print(“apply:”, ok)
```

如果任务明确要求指定总线类型名，也可以这样写：

```python
new_cfg[“OutDataTypeStr”] = “Bus1”
```

当然也支持全量写法：

```python
new_cfg[“OutDataTypeStr”] = “inherit: auto”
new_cfg[“OutDataTypeStr”] = “Bus: Bus1”
```

## 5. 修改建议

- 修改信号数量只需设置 `InputsNum`，模块会自动同步端口数，无需手动维护 `PortConfig`。
- 对 `OutDataTypeStr`，推荐优先使用简化输入：
  - 自动继承时用 `auto`
  - 指定总线类型时用总线类型名，例如 `Bus1`
- 对 `BusCreator` 这类有耦合字段的模块，不建议仅凭多个 `SetModelParamValue(...)` 连续硬写多个字段。

## 6. 最小校验示例

只校验关键字段时，可以在回写后做一次定向读取：

```python
import mworks.sysplorer as ModelingPy

verify = ModelingPy.GetModelParamValues(
    "model1",
    "BusCreator1",
    fields=["InputsNum", "OutDataTypeStr", "ShowSignalNames"],
)
print(verify)
```

注意：传入 `fields=[...]` 时，返回值固定为 `dict`。

## 7. 测试注意点

- **已验证**：`OutDataTypeStr="auto"` 写入后读回值为 `"inherit: auto"`，规范化行为已确认。
- **已验证**：`InputsNum` 从 `"2"` 改为 `"3"` 写入成功，读回一致，端口数自动同步。
- 待验证：`OutDataTypeStr="Bus1"` 这类总线类型名简化输入，写入后是否按目标总线类型生效，以及读回格式。
- 待验证：全量输入 `"Bus: Bus1"` 写入后的读回格式。
