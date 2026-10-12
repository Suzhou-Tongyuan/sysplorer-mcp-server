> 本文件仅用于中文审校参考，实际任务执行请调用 `SKILL.md`。

# Sysblock 批量参数对象配置

## 范围

- **适用**：`GetModelParamValues`、`SetModelParamValues`、模块完整参数对象读取、局部字段读取、`dict` / JSON string / DataClass 形式的参数提交，以及与 `GetModelParamValue` / `SetModelParamValue` 的协同。
- **不适用**：Sysblock 拓扑搭建、DesignOpt 工具箱任务、Modelica 物理建模，以及把 `Utils/param_normalize.py` 当作外部接口直接调用。
- **优先级**：当任务需要一次性读取或提交某个模块的整组参数时，优先使用本 Skill，而不是循环调用多个单参数接口。

## 硬规则

1. 任何 `run_sysplorer_api` 之前，先用 `session_manager(action="health" | "ensure")` 确认 Sysplorer 会话可用。
2. 脚本中不要调用 `ClearAll` 或 `ChangeDirectory`。
3. 对外文档化的批量参数接口只有 `GetModelParamValues` 与 `SetModelParamValues`。
4. `Utils/param_normalize.py` 仅作为内部归一化实现存在，在实际环境中相对于 `sysplorer_api.py` 也是同一套包内相对路径，负责 Python 参数归一化、JSON 与 `dict` / DataClass 转换，不作为外部调用入口。
5. 只改一两个标量字段时，可以继续使用 `SetModelParamValue`；需要整组参数上下文时，应先 `GetModelParamValues` 再整体回写。

## 工具映射

| 需求 | 工具 / 动作 |
|---|---|
| Sysplorer 就绪检查 | `session_manager` |
| 执行 Python API 脚本 | `call_code(mode="run_sysplorer_api")` |
| 打开 / 加载模型 | `model_manager` |
| 修改后检查 / 仿真 / 翻译 | `check_model`、`simulate_model`、`translate_model` |
| 细化文档 | `references/批量参数配置接口说明.md`、`references/模块参数对象映射说明.md`、`references/与单参数接口协同流程.md`、`references/模块参数专项说明/LookupTable模块总览.md`、`references/模块参数专项说明/BusCreator模块参数说明.md` |

## 标准流程

1. 确认 Sysplorer 已连接，目标模型已加载。
2. 在脚本中导入公开入口：

```python
import mworks.sysplorer as ModelingPy
```

3. 读取模块当前配置：

```python
cfg = ModelingPy.GetModelParamValues("model1", "Gain1")
```

4. 对标准模块，返回值通常是 `dict`，直接修改后整体提交：

```python
cfg["Gain"] = "10"
ok = ModelingPy.SetModelParamValues("model1", "Gain1", cfg)
```

5. 对复杂模块，如 `CCaller`，返回值可能自动转为 DataClass：

```python
cfg = ModelingPy.GetModelParamValues("model1", "CCaller1")
cfg.FunctionName = "calc_sum_diff"
cfg.SampleTime = "0.01"
ok = ModelingPy.SetModelParamValues("model1", "CCaller1", cfg)
```

6. 只需要读取部分字段时，传 `fields`，返回值固定为筛选后的 `dict`：

```python
partial_cfg = ModelingPy.GetModelParamValues(
    "model1",
    "CCaller1",
    fields=["FunctionName", "SampleTime"],
)
```

## 返回形态规则

- `GetModelParamValues(modelName, component)` 返回模块完整配置对象。
- 只有在 `block_params.py` 中定义了 DataClass 结构、并且注册进 `BLOCK_PARAM_CLASS_MAP` 的模块类型，才会自动转换成 DataClass。
- 其他所有模块默认返回 `dict`。
- 一旦传入 `fields`，返回值固定是 `dict`，不会再自动转 DataClass。
- `SetModelParamValues(modelName, component, params)` 支持 `dict`、DataClass、JSON string 三种输入形态。

## 稳定模块规则

- `CCaller` 是当前确认的返回 dataclass 的模块。
- `BusCreator`、`BusSelector`、`SubSystem`、`LookupTable` 系列、`CFunction`、 `Goto`、 `From` 、 `GotoTagVisibility` 和普通封装模块应作为 `dict` 处理，除非显式添加了新的 dataclass 映射。
- 默认不要将辅助字段视为可写字段。

已确认示例：

- `BusSelector.AvailableSignals`
  - 引用字段；候选信号列表；非修改字段
- `CCaller.AvailableFunctions`
  - 引用字段；当前 C 文件中可选的 C 函数列表
- `CCaller.Arguments[].CName`
  - 引用字段；原始 C 侧参数名
- `BusCreator.OutDataTypeStr`
  - 支持简化输入：
    - `auto` -> `"inherit: auto"`
    - `Bus1` -> 总线类型名简写
    - 完整字符串如 `"inherit: auto"` 和 `"Bus: Bus1"` 也有效
- `CFunction.SymbolSpec`
  - 数组字段；每个元素代表一个变量（输入/输出/参数）
  - 建议整体回写，适配层以提交的数组整体重建端口与参数，不含按空 `name` 的增量合并
  - `name` 必填；`parameter` / `persistent` / `constant` 作用域必须提供非空 `value`
  - 每个元素包含：`name`、`scope`、`dataType`、`dimension`、`value`
- `Goto`
  - `GotoTag` 可写；Goto标签名
  - `TagVisibility`  可写；合法值为 `Global` / `Local` / `Scoped`
  - 同时提交 `GotoTag` + `TagVisibility` 时，内部先设置标签名，再设置可见性（顺序敏感，见专项说明）
- `From`
  - `GotoTag` 可写；引用的标签名
  - `AvailableTags` 参考字段；只读候选标签列表，回写会被拦截
- `GotoTagVisibility` 
  - `GotoTag` 可写；标签名
  - 作用域固定为组件所在层次前缀、可见性固定为 `Scoped`,均属内部处理，不向调用方暴露

在生成的模块说明中，不要暴露有意对调用者隐藏的内部处理字段。

已确认示例：

- `BusCreator.BusTypeIsAuto`
- `BusCreator.BusTypeName`

这些是内部处理字段，不应在模块说明中暴露，除非未来需求明确更改该规则。

## 2026a 说明

- `fields` 会先序列化成 JSON，再传给底层接口。
- `fields` 为空或不传时，表示读取完整配置对象。
- 完整配置读取后，会通过 `GetComponentTypeName(...)` 判断模块类型，并尝试按映射表转成 DataClass。
- DataClass 返回结构只定义在 `block_params.py` 内，该文件在实际环境中与 `sysplorer_api.py` 处于同一路径层级。
- 当前 `block_params.py` 中已注册 `CCaller -> ExternalCFunctionConfig`。
- 如果模块类型没有在该文件中定义并注册，就按 `dict` 处理。
- `SetModelParamValues` 会先把输入统一归一化成 JSON string，再提交给底层。
- `NormalizeParams`、`ParseParams`、`DictToDataClass` 都属于内部流程实现，对外不单独暴露。

## 排错清单

- 先确认模型已加载，`modelName` 和 `component` 拼写完全正确。
- 使用 `fields` 时，返回值预期应是 `dict`，不要按 DataClass 访问。
- 如果复杂模块没有自动转为 DataClass，优先检查其模块类型是否已注册到 `BLOCK_PARAM_CLASS_MAP`。
- JSON string 的 key 必须与底层参数字段名完全一致。
- 回写前注意区分可写字段和只读辅助字段。

## 维护来源

- `new/sysplorer_api.py`
- `new/block_params.py`
- `Utils/param_normalize.py`
- `modeling_skills/ty-design-opt-exp-modeling/`
- `modeling_skills/ty-sysblock-diagram-modeling/`
