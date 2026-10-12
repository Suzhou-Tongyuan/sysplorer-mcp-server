# DesignOptMro Python API 参考

本文根据当前安装包中的
`mworks/sysplorer/DesignOptMro/DesignOptMro.py`、矩形面积示例脚本，以及《响应优化 Python API 2024b 说明.docx》整理。

使用方式：

```python
import mworks.sysplorer.DesignOptMro as mro
```

## 启停工具箱

### `InitialApp(modelName: str, instPath: str = "") -> bool`

翻译模型并初始化响应优化工具箱。

- `modelName`：模型名称，例如 `"rectangle_area"`。
- `instPath`：可选的 `simdata-result.msr` 路径。
- 返回 `True`/`False` 表示是否成功。

### `CloseApp() -> bool`

关闭响应优化工具箱。调用后不能继续进行响应优化操作。

### `GetOptimizeStatus()`

查询优化状态。2024b 文档说明：`0` 表示优化成功结束，`-1` 表示未开始或正在进行，其它数字表示优化错误。

## 会话

### `OpenSession(path: str) -> bool`

加载本地保存的响应优化会话 XML。需与当前模型匹配。

### `SaveSession(path: str) -> str`

保存当前响应优化会话。`path` 可以是目录，也可以是具体 XML 文件路径。

## 调节参数

### `GetTunerParam() -> dict`

获取模型可用调节参数。源码文档返回形如：

```python
{
    "length": {
        "value": 10.0,
        "unit": "",
        "min": 0.0,
        "max": 100.0,
        "description": "..."
    }
}
```

### `SelectTunerParam(array: tuple) -> bool`

选择调节参数。参数名放在 tuple 中：

```python
mro.SelectTunerParam(("length",))
mro.SelectTunerParam(("dampingPhysical.mass2.L", "dampingPhysical.mass2.m"))
```

### `GetSelectedTunerParam() -> dict`

获取已选择的调节参数及其配置。

### `ConfigTunerParam(paramName: str, minVal=-1e100, maxVal=1e100, initialVal=0.0) -> bool`

配置调节参数的下限、上限和初值。`minVal`、`maxVal`、`initialVal` 必须是 `int` 或 `float`。

### `DeleteTunerParam(paramName: str) -> bool`

删除一个已选择的调节参数。

### `ClearTunerParam() -> bool`

清空已选择的调节参数。

## 固定参数

调节参数和固定参数互斥。

### `GetFixParam() -> list`

获取可选固定参数。通常返回除已选调节参数之外的参数。

### `SelectFixParam(array: tuple) -> bool`

选择固定参数。

### `GetSelectedFixParam() -> dict`

获取已选择固定参数及其数值。

### `ConfigFixParam(paramName: str, initialVal=0.0) -> bool`

配置固定参数值。`initialVal` 必须是 `int` 或 `float`。

### `DeleteFixParam(paramName: str) -> bool`

删除一个固定参数。

### `ClearFixParam() -> bool`

清空固定参数。

## 需求

### `GetRequirement() -> list`

获取支持的需求类型。2024b 文档列出：

```python
["Timedomain_property", "Timedomain_step_response", "Timedomain_bound", "Timedomain_tracking"]
```

### `SelectRequirement(array: tuple) -> bool`

选择参与优化的需求。不调用时，默认创建的需求为全选状态。

### `GetCreatedRequirement() -> list`

获取已经创建的需求名称。

### `GetRequirementData(reqName: str) -> dict`

获取指定需求的配置数据。

### `DeleteRequirement(reqName: str) -> bool`

删除一个需求。

### `ClearRequirement() -> bool`

清空全部需求。

## 变量属性需求

### `NewVariablePropertyRequirement(reqName: str) -> bool`

新建变量属性需求。

### `ConfigVariablePropertyRequirement(reqName: str, varProperty: str = "Final Value", varType: str = "Minimization", value=0.0) -> bool`

配置变量属性需求。

- `varProperty` 可选值包括：`"Maximum"`、`"Minimum"`、`"Initial Value"`、`"Final Value"`、`"Average"`、`"Median"`、`"Variance"`、`"Quartiles"`、`"Sum"`、`"Sum of Squares"`、`"Sum of Absolute Values"`。
- `varType` 可选值包括：`"Minimization"`、`"Maximization"`、`"Equal to"`、`"Greater or Equal"`、`"Less or Equal"`。
- 当 `varType` 为等于、大于等于或小于等于类约束时，`value` 是边界值。

示例：

```python
mro.NewVariablePropertyRequirement("Req_1")
mro.ConfigVariablePropertyRequirement("Req_1", "Final Value", "Maximization")
```

## 阶跃响应需求

### `NewStepResponseRequirement(reqName: str) -> bool`

新建阶跃响应需求。

### `ConfigStepResponseRequirement(reqName: str, initialValue=0, finalValue=1, stepResponseTime=0, riseTime=5, rise=80, settlingTime=7, settling=1, overshoot=10, undershoot=1) -> bool`

配置阶跃响应需求。

- `initialValue`：初始值。
- `finalValue`：终值。
- `stepResponseTime`：阶跃响应时间。
- `riseTime` / `rise`：上升时间和上升百分比。
- `settlingTime` / `settling`：稳态时间和稳定百分比。
- `overshoot` / `undershoot`：超调和下冲百分比。

## 变量线性边界需求

当前 Python 源码中的函数名是 `NewVariableLinearBoundRequirement` 和 `ConfigVariableLinearBoundRequirement`。2024b docx 目录中出现的 `NewLinearBoundRequirement` / `ConfigLinearBoundRequirement` 可视为旧称或文档称呼，写脚本时以源码名称为准。

### `NewVariableLinearBoundRequirement(reqName: str) -> bool`

新建变量线性边界需求。

### `ConfigVariableLinearBoundRequirement(reqName: str, boundType: str = "<=", array: tuple = (0, 1, 1, 1)) -> bool`

配置变量线性边界需求。

- `boundType`：`">="` 或 `"<="`。
- `array`：`(开始时间, 开始幅值, 结束时间, 结束幅值)`。

示例：

```python
mro.NewVariableLinearBoundRequirement("Req_3")
mro.ConfigVariableLinearBoundRequirement("Req_3", "<=", (0, 1, 1, 1))
```

## 变量追踪需求

### `NewVariableTrackingRequirement(reqName: str) -> bool`

新建变量追踪需求。

### `ConfigVariableTrackingRequirement(reqName: str, time: tuple = (...), value: tuple = (...), method: str = "Mean Absolute Percentage Error") -> bool`

配置变量追踪需求。

`method` 可选值包括：

- `"Mean Error"`
- `"Mean Absolute Error"`
- `"Mean Percentage Error"`
- `"Mean Absolute Percentage Error"`
- `"Mean Squared Error"`
- `"Mean Absolute Deviation"`

示例：

```python
vec_time = (0, 0.1, 0.2, 0.3, 0.4, 0.5)
vec_value = (1.0, 2.0, 3.0, 4.0, 5.0, 6.0)
mro.NewVariableTrackingRequirement("Req_4")
mro.ConfigVariableTrackingRequirement("Req_4", vec_time, vec_value, "Mean Absolute Percentage Error")
```

## 变量集

### `GetVariable() -> list`

获取模型中的变量名。

### `NewVariableSet(setName: str, array: tuple) -> bool`

新建变量集。

```python
mro.NewVariableSet("Set_1", ("area",))
```

### `GetVariableInSet(setName: str) -> list`

获取变量集中的变量。

### `GetVariableSet() -> list`

获取所有变量集名称。

### `SetRequirementVariableSet(reqName: str, array: tuple) -> bool`

将需求关联到一个或多个变量集。

```python
mro.SetRequirementVariableSet("Req_1", ("Set_1",))
```

### `GetVariableSetInRequirement(reqName: str) -> list`

获取某个需求关联的变量集。

### `DeleteVariableSet(setName: str) -> bool`

删除变量集。

### `ClearVariableSet() -> bool`

清空变量集。

## 仿真与优化配置

### `SetSimulationOption(startTime=0, endTime=1, stepNumber: int = 500) -> bool`

设置仿真开始时间、结束时间和步数。源码参数名是 `stepNumber`；2024b docx 中的 `stepNum` 是文档写法。

### `SetOptimizeOption(continueOptimize: bool = True, parallelNum: int = int(_num_cores / 2)) -> bool`

设置优化选项。

- `continueOptimize`：仿真失败后是否继续优化。
- `parallelNum`：并行数，默认约为 CPU 核心数的一半。源码参数名是 `parallelNum`；2024b docx 中的 `parallelNumber` 是文档写法。

### `GetAlgorithm() -> list`

获取支持的算法。2024b 文档列出：`["Auglag", "Cobyla", "GA", "PSO"]`。

### `SelectAlgorithm(name: str) -> bool`

选择算法，例如 `mro.SelectAlgorithm("PSO")`。

### `GetCurrentAlgorithm() -> str`

获取当前算法名称。

### `ConfigPSOAlgorithm(relativeTolerance=0.001, convergenceTime: int = 3, maxIterStep: int = 100, populationSize: int = 20, parameterAdaptive: bool = False, w=0.6, c1=1.5, c2=2) -> bool`

配置 PSO 算法。

### `ConfigGAAlgorithm(relativeTolerance=0.001, convergenceTime: int = 5, maxIterStep: int = 100, crossoverRate=0.8, mutationRate=0.25, populationSize: int = 30) -> bool`

配置 GA 算法。

## 执行接口

### `StartEvaluate() -> bool`

评估当前参数，阻塞接口。建议在首次优化前调用，用于检查变量名、参数边界、需求配置和变量集绑定是否正确。

### `StartOptimize() -> bool`

开始响应优化，阻塞接口。

## 结果与数据

### `GetEvaluateResultData(reqName: str) -> dict`

获取评估当前参数后的指定需求结果数据。

### `GetOptimizeResult() -> list`

获取所有优化结果名称。

### `GetOptimizeParamData(resultName: str) -> dict`

获取指定优化结果中的调节参数终值。

### `GetOptimizeParamIterData(paramName: str) -> dict`

获取指定参数的迭代数据，返回形如 `{迭代次数: 参数值}`。

### `GetOptimizeReqIterData(reqName: str) -> dict`

获取需求内变量的迭代序列结果，返回形如 `{迭代次数: {变量名: 变量值}}`。

### `GetOptimizeReqTimeData(reqName: str) -> dict`

获取需求内变量的时序结果数据。

### `GetOptimizeData() -> dict`

获取全部优化数据。

- `res["params"]`：参数迭代数据，形如 `{迭代次数: {参数名: 参数值}}`。
- `res["reqs"]`：需求数据。变量属性需求通常是 `{需求名: {迭代次数: {变量名: 变量值}}}`；其它时域需求可能包含时序数组和迭代值。

### `DeleteOptimizeResult(resultName: str) -> bool`

删除指定优化结果。

### `ClearOptimizeResult() -> bool`

清空优化结果。

## 不建议在 MCP 脚本中使用的清理方式

2024b docx 的矩形面积案例末尾包含 `pyapi.ClearAll()`。在 MCP 工作流中不要调用它，因为会清空库、缓存和结果。优先使用：

```python
mro.CloseApp()
# 如果脚本自己启动并拥有 Sysplorer 进程，可以再调用：
pyapi.Exit()
```
