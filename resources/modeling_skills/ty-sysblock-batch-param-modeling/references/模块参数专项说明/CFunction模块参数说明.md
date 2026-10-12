# CFunction 模块参数说明

本文档用于说明 `CFunction` 模块的批量参数对象，与参数对话框各项控件之间的对应关系，供调用 `GetModelParamValues` / `SetModelParamValues` 时直接参考。

`CFunction` 当前应按标准模块 `dict` 处理，不要假设它会自动转换成 DataClass。

## 1. 适用场景

- 读取 `CFunction` 当前完整配置并理解每个字段含义
- 修改输出代码、开始代码、初始化条件代码、终止代码、采样时间
- 配置输入/输出端口和参数变量（SymbolSpec）
- 在保持其余必要字段不丢失的前提下整体回写配置

## 2. 已确认字段与对话框映射

当前可确认映射如下：

| 对话框项 | 批量参数对象 key | 示例值 | 说明 |
| --- | --- | --- | --- |
| 输出代码 | `OutputCode` | `"y = u1 + u2;"` | 每个采样步执行的代码段 |
| 开始代码 | `StartCode` | `"double offset = 0.0;"` | 仿真开始时执行一次的代码 |
| 初始化条件代码 | `InitializeConditionsCode` | `"offset = 1.0;"` | 用于初始化状态变量的代码 |
| 终止代码 | `TerminateCode` | `"printf(\"End\\n\");"` | 仿真结束时执行一次的代码 |
| 采样时间 | `SampleTime` | `"0.01"` | 采样时间，"-1"表示继承父系统采样时间 |
| 端口和参数 | `SymbolSpec` | `[...]` | 变量配置列表（见第 3 节） |

> 完整对象共 **6 个 key**：`OutputCode`、`StartCode`、`InitializeConditionsCode`、`TerminateCode`、`SampleTime`、`SymbolSpec`。

## 3. `SymbolSpec` 字段结构

`SymbolSpec` 是一个参数对象列表，每个元素代表一个变量（输入端口、输出端口或参数）。

### 3.1 数组元素字段

| 字段 | 示例值 | 说明 |
| --- | --- | --- |
| `name` | `"u1"` | 变量名称，必须为合法标识符（字母开头，仅含字母数字） |
| `scope` | `"input"` | 作用域：`input` / `output` / `inputOutput` / `parameter` / `persistent` / `constant` |
| `dataType` | `"double"` | 数据类型：`double` / `float` / `int8` / `uint8` / `int16` / `uint16` / `int32` / `uint32` / `boolean` / `voidPointer` |
| `dimension` | `"[1]"` | 维度定义，格式为 `"[维度1, 维度2, ...]"`，如 `"[1]"`、`"[2,3]"` |
| `value` | `"1.0"` | 初始值；`parameter` / `persistent` / `constant` 作用域必须提供非空值 |

### 3.2 默认值

- `scope` 默认为 `"input"`
- `dataType` 默认为 `"double"`
- `dimension` 默认为 `"1"`（标量简写；界面/读回通常显示为 `"[1]"` 形式）
- `value` 默认为空字符串

## 4. 输入约束

### 4.1 变量名合法性

`SymbolSpec[].name` 必须满足 Modelica 标识符规则：
- 以字母开头
- 仅包含字母和数字
- 不能是 Modelica 保留字
- 不能是内置类型名、函数名或变量名

非法示例：`"1var"`、`"my-var"`、`"if"`、`"Real"`

### 4.2 维度格式

`SymbolSpec[].dimension` 支持以下形式：
- 括号格式 `"[维度1, 维度2, ...]"`，以 `[` 开头、以 `]` 结尾，如 `"[1]"`、`"[2,3]"`
- 标量简写 `"1"`（与默认值一致，按标量处理）
- 各维度取值应为正整数，`0` 维度等非法取值由底层校验拦截

非法示例：`"1.5"`、`"0"`、`"[2,3"`

### 4.3 采样时间

`SampleTime` 必须为：
- `"-1"`：继承父系统采样时间
- 非负实数：指定固定采样时间（如 `"0.01"`）

非法示例：`"-0.1"`、`"abc"`

### 4.4 作用域和数据类型

`scope` 必须是以下值之一：
- `"input"` / `"output"` / `"inputOutput"` / `"parameter"` / `"persistent"` / `"constant"`

`dataType` 必须是以下值之一：
- `"double"` / `"float"` / `"int8"` / `"uint8"` / `"int16"` / `"uint16"` / `"int32"` / `"uint32"` / `"boolean"` / `"voidPointer"`

## 5. 推荐 AI 调用方式

推荐采用"先完整读取，再局部修改，再整体回写"的方式：

```python
import copy
import mworks.sysplorer as ModelingPy

model_name = "model1"
component_name = "CFunction1"

cfg = ModelingPy.GetModelParamValues(model_name, component_name)
new_cfg = copy.deepcopy(cfg)

# 修改代码段
new_cfg["OutputCode"] = "y = u1 * u2 + gain;"
new_cfg["StartCode"] = "double gain = 2.0;"

# 修改采样时间
new_cfg["SampleTime"] = "0.01"

# 修改变量配置
new_cfg["SymbolSpec"] = [
    {
        "name": "u1",
        "scope": "input",
        "dataType": "double",
        "dimension": "[1]",
        "value": ""
    },
    {
        "name": "u2",
        "scope": "input",
        "dataType": "double",
        "dimension": "[1]",
        "value": ""
    },
    {
        "name": "y",
        "scope": "output",
        "dataType": "double",
        "dimension": "[1]",
        "value": ""
    },
    {
        "name": "gain",
        "scope": "parameter",
        "dataType": "double",
        "dimension": "[1]",
        "value": "2.0"
    }
]

ok = ModelingPy.SetModelParamValues(model_name, component_name, new_cfg)
print("apply:", ok)
```

## 6. 修改建议

- 修改 `OutputCode`、`StartCode`、`InitializeConditionsCode`、`TerminateCode` 时，可以直接修改对应字段，无需联动其他字段。
- 修改 `SymbolSpec` 时，建议整体更新数组，确保所有变量配置完整。
- 修改 `SampleTime` 时，确保值为 `"-1"` 或非负实数。
- 如果只想修改某个代码段，可以先读取完整对象，只修改对应字段，其余字段保持原值。

> 说明：适配层在应用 `SymbolSpec` 时，会以提交的数组**整体重建**端口与参数；
> 当前不提供按空 `name` 的增量合并，修改变量配置时建议提供完整变量列表。

## 7. 最小校验示例

只校验关键字段时，可以在回写后做一次定向读取：

```python
import mworks.sysplorer as ModelingPy

verify = ModelingPy.GetModelParamValues(
    "model1",
    "CFunction1",
    fields=["OutputCode", "SampleTime"],
)
print(verify)
```

注意：传入 `fields=["..."]` 时，返回值固定为仅包含所请求字段的 `dict`, 不会返回全量对象。

## 8. 测试

- 验证通过：所有字段独立修改是否能成功写入并读回一致。
- 验证通过：`SymbolSpec` 数组整体修改是否能正确更新端口和参数。
- 验证通过：变量名非法时是否能被拦截并返回正确错误信息。
- 验证通过：维度格式非法时是否能被拦截。
- 验证通过：`SampleTime` 为 `"-1"` 或非负实数时是否能正确处理。
- 验证通过：代码段字段为空字符串时是否正常处理。
- 验证通过：`SymbolSpec` 数组为空`""`时是否正常处理。