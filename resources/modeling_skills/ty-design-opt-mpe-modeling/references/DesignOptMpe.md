# DesignOptMpe 使用说明

## 1. 简介

`DesignOptMpe` 用于通过 Python 调用 Sysplorer 的参数估计能力，适合以下工作场景：

- 初始化参数估计环境
- 打开、保存参数估计会话
- 配置调节参数和固定参数
- 创建试验并导入测量数据
- 建立仿真变量与测量变量的对应关系
- 选择并配置优化算法
- 执行参数评估、参数估计、参数验证
- 查看估计报告、参数结果和验证结果
- 对数据进行预处理并导出结果

本文档面向最终用户，重点说明接口用途、使用顺序和参数含义。

> **参数估计实操与常见问题**（工作流、残差与命名等）：见同目录 **`参数估计使用说明.md`**。Demo 步骤见 **`参数估计demo说明.md`**。

## 2. 使用前准备

在使用 `DesignOptMpe` 前，建议先确认以下条件：

- 已安装并可正常调用 Sysplorer 相关运行环境
- 模型名称、会话文件、测量文件路径都已准备好
- 需要参与估计的参数、固定参数和测量数据已经明确

常见导入方式如下：

```python
from mworks.sysplorer.DesignOptMpe.DesignOptMpe import *
```

若希望在脚本中**枚举本工具箱全部接口**或**按需查看内建帮助**，推荐使用模块别名（与主建模 API 的 `ListFunctions` 区分）：

```python
import mworks.sysplorer.DesignOptMpe as mpe
RUN_SCRIPT_RESULT = mpe.ListFunctions()   # 列出 MPE 工具箱中的命令函数及简短说明
# help(mpe.InitialApp)                      # 查看某一 MPE API 函数的 help 文档
```

说明：Sysplorer 主建模会话里 `ModelingPy.ListFunctions()` 列出的是主命令空间，**不会**包含 `DesignOptMpe` 中的函数；MPE 相关开发请始终通过 `mpe.ListFunctions()` / `help(mpe.xxx)` 或本文档与语料检索定位接口。

## 3. 典型操作流程

推荐按下面的顺序使用接口。

### 3.1 初始化环境

先初始化参数估计环境。

使用接口：

- `InitialApp(modelName, instPath="")`

### 3.2 打开或保存会话

如果已经存在会话文件，可以直接打开；完成配置后也可以保存。

使用接口：

- `OpenSession(path)`
- `SaveSession(path)`

### 3.3 配置调节参数

先查看有哪些可调参数，再选择需要参与估计的参数，并设置上下界和初始值。

使用接口：

- `GetTunerParam()`
- `SelectTunerParam(...)`
- `GetSelectedTunerParam()`
- `ConfigTunerParam(...)`

### 3.4 创建并配置试验

建立试验对象，并为试验绑定测量文件。

使用接口：

- `NewExp(...)`
- `NewExpAttachPath(...)`
- `GetExp()`
- `SetEstimateExp(...)`
- `SetValidateExp(...)`
- `ConfigExp(...)`
- `ConfigSteadyStateExp(...)`
- `ConfigMultiBoundaryExp(...)`

注意：`ConfigMultiBoundaryExp(...)` 多边界工况不可以设置固定参数。`SelectFixParam(...)` / `ConfigFixParam(...)` 只允许非多边界参数估计流程使用。

### 3.5 配置固定参数和变量映射

如果模型中有不参与优化、但需要指定初值的参数，可以作为固定参数配置。同时还需要建立仿真变量与测量变量的映射关系。

使用接口：

- `SelectFixParam(...)`
- `GetFixParam()`
- `GetSelectedFixParam(...)`
- `ConfigFixParam(...)`
- `SetSimulateVariable(...)`

### 3.6 配置算法和仿真选项

选择优化算法，并设置仿真时间、估计时间窗、残差计算方式、并行数等。

使用接口：

- `GetAlgorithm()`
- `SelectAlgorithm(...)`
- `ConfigPSOAlgorithm(...)`
- `ConfigGAAlgorithm(...)`
- `SetSimulateOption(...)`
- `SetValidateSimulateOption(...)`
- `GetResidualFunc()`
- `SetEstimateOption(...)`

### 3.7 执行评估、估计或验证

在配置完成后，可以启动任务。

推荐直接使用以下对外接口：

- `StartEvaluate()`
- `StartEstimate()`
- `StartValidate()`

源码中还包含 `EvaluateCurrentParam()`、`Estimate()`、`Validate()` 三个底层启动接口。业务脚本通常优先使用上面的 `Start...` 接口，因为它们会等待任务结束后再返回。

### 3.8 查看结果

任务完成后，可读取迭代报告、参数结果、评估结果和验证结果。

使用接口：

- `GetEstimateReport()`
- `GetEvaluateResultData()`
- `GetEstimateResult()`
- `GetEstimateResultData()`
- `GetEstimateParamData(...)`
- `SelectEstimateResult(...)`
- `GetValidateResultData()`

### 3.9 数据预处理

如果需要对测量数据做偏移、缩放、截取、重采样或滤波，可以使用数据预处理接口。

数据预处理接口是独立的辅助能力，作用对象是测量/CSV 数据；不要把它们和参数估计主流程接口混淆。标准参数估计仍应通过试验、变量映射、仿真选项、估计选项和启动接口完成，例如 `NewExpAttachPath`、`SetSimulateVariable`、`SetSimulateOption`、`SetEstimateOption`、`StartEvaluate`、`StartEstimate`。预处理完成后，可将处理后的数据再导出或绑定到普通估计试验中。

使用接口：

- `ImportData(...)`
- `ChangeOffsetData(...)`
- `ScaleData(...)`
- `ExtractData(...)`
- `ResampleData(...)`
- `LowFilterData(...)`
- `HighFilterData(...)`
- `BandFilterData(...)`
- `GetDataProcessResult()`
- `GetDataProcessResultData(...)`
- `ExportData(...)`

## 4. 接口使用说明

### 4.1 状态与环境

#### `GetSimStatus() -> int`

获取当前任务状态。

- 返回值：
  - `int`：状态码

#### `CloseApp() -> bool`

关闭参数估计应用。

- 返回值：
  - `bool`：是否关闭成功

#### `InitialApp(modelName: str, instPath: str = "") -> bool`

初始化参数估计环境。

- 参数：
  - `modelName`：模型名称
  - `instPath`：实例路径，默认空字符串
- 返回值：
  - `bool`：是否初始化成功

### 4.2 会话管理

#### `OpenSession(path: str) -> bool`

打开会话文件。

- 参数：
  - `path`：会话路径
- 返回值：
  - `bool`：是否打开成功

#### `SaveSession(path: str) -> str`

保存会话。

- 参数：
  - `path`：保存路径或会话名称
- 返回值：
  - `str`：返回会话路径或名称

### 4.3 调节参数

#### `GetTunerParam() -> list`

获取全部调节参数。

- 返回值：
  - `list`：调节参数列表

#### `SelectTunerParam(array: tuple) -> bool`

选择需要参与估计的调节参数。

- 参数：
  - `array`：待选择的调节参数名称元组，每个元素都应为字符串
- 返回值：
  - `bool`：是否选择成功

#### `GetSelectedTunerParam() -> dict`

获取已选择调节参数的配置。

- 返回值：
  - `dict`：键为参数名，值为参数配置

示例：

```python
{
    "length": {
        "min": 0,
        "max": 2,
        "value": 1,
        "description": "矩形长度"
    }
}
```

#### `ConfigTunerParam(paramName: str, minVal=-1e100, maxVal=1e100, initialVal=0) -> bool`

配置调节参数范围和初始值。

- 参数：
  - `paramName`：待配置的调节参数名称
  - `minVal`：最小值，默认 `-1e100`
  - `maxVal`：最大值，默认 `1e100`
  - `initialVal`：初始值，默认 `0`
- 返回值：
  - `bool`：是否配置成功
- 说明：
  - `minVal`、`maxVal`、`initialVal` 支持 `int` 或 `float`
  - 非法类型会返回 `False`

#### `DeleteTunerParam(paramName: str) -> bool`

删除指定调节参数。

- 参数：
  - `paramName`：参数名称
- 返回值：
  - `bool`：是否删除成功

#### `ClearTunerParam() -> bool`

清空全部调节参数。

- 返回值：
  - `bool`：是否清空成功

### 4.4 试验管理

#### `NewExp(expName: str) -> bool`

新建试验。

- 参数：
  - `expName`：试验名称
- 返回值：
  - `bool`：是否创建成功

#### `NewExpAttachPath(expName: str, path: str) -> bool`

新建试验并绑定测量文件。

- 参数：
  - `expName`：试验名称
  - `path`：测量文件路径
- 返回值：
  - `bool`：是否创建成功

#### `GetExp() -> list`

获取当前已创建的试验名称。

- 返回值：
  - `list`：试验名称列表

#### `GetCurrentEstimateExp() -> str`

获取当前估计试验名称。

- 返回值：
  - `str`：试验名称

#### `GetCurrentValidateExp() -> str`

获取当前验证试验名称。

- 返回值：
  - `str`：试验名称

#### `SetEstimateExp(expName: str) -> bool`

将指定试验设置为估计试验。

- 参数：
  - `expName`：试验名称
- 返回值：
  - `bool`：是否设置成功

#### `SetValidateExp(expName: str) -> bool`

将指定试验设置为验证试验。

- 参数：
  - `expName`：试验名称
- 返回值：
  - `bool`：是否设置成功

#### `ConfigExp(expName: str, path: str) -> bool`

为试验配置测量文件。

- 参数：
  - `expName`：试验名称
  - `path`：测量文件路径
- 返回值：
  - `bool`：是否配置成功

#### `ConfigSteadyStateExp(expName: str, boundaryPath: str, steadyStatePath: str, steadyStateTime) -> bool`

配置稳态试验，适用于多边界-导入配置场景。使用此接口前必须先新建试验。

- 参数：
  - `expName`：试验名称
  - `boundaryPath`：边界数据文件绝对路径，路径不应包含中文
  - `steadyStatePath`：稳态数据文件绝对路径，路径不应包含中文
  - `steadyStateTime`：稳态时间，源码会将 `int` 或 `float` 转为 `float`
- 返回值：
  - `bool`：是否配置成功
- 说明：
  - `steadyStateTime` 必须是数字类型，否则返回 `False`
  - 典型流程是先 `NewExp(...)`，再调用本接口绑定边界数据和稳态数据
  - 稳态估计时，`SetSimulateOption(...)` 的估计时间窗通常靠近仿真末端，例如源码示例使用 `SetSimulateOption(0, 1000, 999, 1000, 500)`
- 示例：

```python
NewExp("exp1")
ConfigSteadyStateExp(
    "exp1",
    r"C:\path\boundary.csv",
    r"C:\path\steady_state.csv",
    1000,
)
SetSimulateOption(0, 1000, 999, 1000, 500)
StartEstimate()
result = GetEstimateResultData()
print(result["Residual"])
print(result["SimResultData"])
```

#### `ConfigMultiBoundaryExp(expName: str, path: str, boundaryParameter: list, boundaryParameterVal: list, BoundaryVar: list) -> bool`

配置多边界工况试验。使用此接口前必须先新建试验。

多边界工况不允许设置固定参数，不要在该流程中调用 `SelectFixParam(...)` 或 `ConfigFixParam(...)`。随工况变化的值应放入 `boundaryParameter` / `boundaryParameterVal`；所有工况恒定的值应保留在模型默认参数或模型预配置中。

- 参数：
  - `expName`：试验名称
  - `path`：测量文件或实验文件路径，路径不应包含中文
  - `boundaryParameter`：边界参数名称列表
  - `boundaryParameterVal`：边界参数取值列表，通常为二维列表
  - `BoundaryVar`：每个边界对应的仿真变量与测量变量映射列表
- 返回值：
  - `bool`：是否配置成功
- 说明：
  - `boundaryParameter` 给出边界参数名称，例如 `["CarBody.L", "gearBox.ratio"]`
  - `boundaryParameterVal` 按工况逐行给出每组边界参数取值，例如每行对应一组 `CarBody.L` 和 `gearBox.ratio`
  - `BoundaryVar` 是仿真变量到测量变量的映射字典列表；源码示例使用 `[{"CarBody.a": "acc"}]`
  - 多边界配置同样需要先 `NewExp(...)`，再调用本接口
- 示例：

```python
NewExp("exp1")
ConfigMultiBoundaryExp(
    "exp1",
    path=r"C:\path\Acceleration_measurements.csv",
    boundaryParameter=["CarBody.L", "gearBox.ratio"],
    boundaryParameterVal=[
        [4.7, 4.17],
        [4.7, 2.34],
        [3.8, 4.17],
        [3.8, 2.34],
        [2.3, 4.17],
        [2.3, 2.34],
    ],
    BoundaryVar=[{"CarBody.a": "acc"}],
)
SetSimulateOption(3.8, 6, 3.8, 6, 500)
StartEvaluate()
print(GetEvaluateResultData())
```

#### `DeleteExp(expName: str) -> bool`

删除指定试验。

- 参数：
  - `expName`：试验名称
- 返回值：
  - `bool`：是否删除成功

#### `ClearExp() -> bool`

清空全部试验。

- 返回值：
  - `bool`：是否清空成功

### 4.5 固定参数

#### `SelectFixParam(expName: str, array: tuple) -> bool`

仅非多边界试验允许使用本接口；多边界工况不要调用 `SelectFixParam(...)`。

为试验选择固定参数。

- 参数：
  - `expName`：试验名称
  - `array`：固定参数名称元组，每个元素都应为字符串
- 返回值：
  - `bool`：是否选择成功

#### `GetFixParam() -> list`

获取全部固定参数。

- 返回值：
  - `list`：固定参数列表

#### `GetSelectedFixParam(expName: str) -> list`

获取试验中已选择的固定参数。

- 参数：
  - `expName`：试验名称
- 返回值：
  - `list`：固定参数列表

#### `ConfigFixParam(expName: str, paramName: str, initialVal=0) -> bool`

仅非多边界试验允许使用本接口；多边界工况不要调用 `ConfigFixParam(...)`。

配置固定参数初始值。

- 参数：
  - `expName`：试验名称
  - `paramName`：固定参数名称
  - `initialVal`：初始值，默认 `0`
- 返回值：
  - `bool`：是否配置成功
- 说明：
  - `initialVal` 支持 `int` 或 `float`
  - 非法类型会返回 `False`

#### `DeleteFixParam(expName: str, paramName: str) -> bool`

删除试验中的固定参数。

- 参数：
  - `expName`：试验名称
  - `paramName`：固定参数名称
- 返回值：
  - `bool`：是否删除成功

#### `ClearFixParam(expName: str) -> bool`

清空试验中的固定参数。

- 参数：
  - `expName`：试验名称
- 返回值：
  - `bool`：是否清空成功

### 4.6 变量映射

#### `GetVariable() -> list`

获取全部仿真变量。

- 返回值：
  - `list`：仿真变量列表

#### `GetMeasureVariable(expName: str) -> list`

获取试验对应的测量变量。

- 参数：
  - `expName`：试验名称
- 返回值：
  - `list`：测量变量列表

#### `SetSimulateVariable(expName: str, simulateVariable: str, measureVariable: str) -> bool`

绑定仿真变量和测量变量。

- 参数：
  - `expName`：试验名称
  - `simulateVariable`：仿真变量名称
  - `measureVariable`：测量变量名称
- 返回值：
  - `bool`：是否绑定成功

### 4.7 优化算法

#### `GetAlgorithm() -> list`

获取支持的优化算法。

- 返回值：
  - `list`：算法名称列表

#### `SelectAlgorithm(name: str = "Bobyqa") -> bool`

选择优化算法。

- 参数：
  - `name`：算法名称，默认 `Bobyqa`
- 返回值：
  - `bool`：是否选择成功

#### `GetCurrentAlgorithm() -> str`

获取当前算法名称。

- 返回值：
  - `str`：算法名称

#### `ConfigPSOAlgorithm(relativeTolerance=0.001, convergenceTime: int = 3, maxIterStep: int = 100, populationSize: int = 20, parameterAdaptive: bool = True, w=0.6, c1=1.5, c2=2) -> bool`

配置 PSO 算法参数。

- 参数：
  - `relativeTolerance`：相对容差，默认 `0.001`
  - `convergenceTime`：收敛判定次数，默认 `3`
  - `maxIterStep`：最大迭代步数，默认 `100`
  - `populationSize`：种群大小，默认 `20`
  - `parameterAdaptive`：是否启用自适应参数，默认 `True`
  - `w`：惯性权重，默认 `0.6`
  - `c1`：个体学习因子，默认 `1.5`
  - `c2`：群体学习因子，默认 `2`
- 返回值：
  - `bool`：是否配置成功

#### `ConfigGAAlgorithm(relativeTolerance=0.001, convergenceTime: int = 5, maxIterStep: int = 100, crossoverRate=0.8, mutationRate=0.25, populationSize: int = 30) -> bool`

配置 GA 算法参数。

- 参数：
  - `relativeTolerance`：相对容差，默认 `0.001`
  - `convergenceTime`：收敛判定次数，默认 `5`
  - `maxIterStep`：最大迭代步数，默认 `100`
  - `crossoverRate`：交叉率，默认 `0.8`
  - `mutationRate`：变异率，默认 `0.25`
  - `populationSize`：种群大小，默认 `30`
- 返回值：
  - `bool`：是否配置成功

### 4.8 仿真与估计选项

#### `SetSimulateOption(SimStartTime=0.0, SimEndTime=1, estimateStartTime=0, estimateEndTime=1, stepNumber: int = 500) -> bool`

设置估计阶段仿真选项。

- 参数：
  - `SimStartTime`：仿真开始时间
  - `SimEndTime`：仿真结束时间
  - `estimateStartTime`：估计开始时间
  - `estimateEndTime`：估计结束时间
  - `stepNumber`：仿真步数，默认 `500`
- 返回值：
  - `bool`：是否设置成功

#### `SetValidateSimulateOption(simStartTime=0.0, simEndTime=1.0, validateStartTime=0.0, validateEndTime=1.0, stepNumber: int = 500) -> bool`

设置验证阶段仿真选项。

- 参数：
  - `simStartTime`：仿真开始时间
  - `simEndTime`：仿真结束时间
  - `validateStartTime`：验证开始时间
  - `validateEndTime`：验证结束时间
  - `stepNumber`：仿真步数，默认 `500`
- 返回值：
  - `bool`：是否设置成功

#### `GetSimulateOption() -> dict`

获取当前仿真选项。

- 返回值：
  - `dict`：仿真选项数据

#### `GetResidualFunc() -> list`

获取可用残差计算方式。

- 返回值：
  - `list`：残差计算方式列表

#### `SetEstimateOption(residualFunc: str = "Mean Absolute Percentage Error", parallelNum: int = int(_num_cores / 2), continueEstimate: bool = True) -> bool`

设置估计选项。

默认残差函数为 `Mean Absolute Percentage Error`。外部自定义优化器在用户未显式指定残差函数时，也应使用该默认值，以保持与工具箱 `SetEstimateOption(...)` 行为一致。工具箱支持的残差函数包括 `Mean Error`、`Mean Absolute Error`、`Mean Percentage Error`、`Mean Absolute Percentage Error`、`Mean Squared Error`。

- 参数：
  - `residualFunc`：残差计算方式
  - `parallelNum`：并行数目
  - `continueEstimate`：仿真失败后是否继续估计
- 返回值：
  - `bool`：是否设置成功

#### `GetEstimateOption() -> dict`

获取当前估计选项。

- 返回值：
  - `dict`：估计选项数据

### 4.9 任务执行

#### `EvaluateCurrentParam() -> bool`

启动当前参数评估。

- 返回值：
  - `bool`：是否启动成功
- 说明：
  - 源码建议优先使用 `StartEvaluate()`

#### `StartEvaluate() -> bool`

评估当前参数，并等待任务结束。

- 返回值：
  - `bool`：是否执行成功

#### `Estimate() -> bool`

启动参数估计流程。

- 返回值：
  - `bool`：是否启动成功
- 说明：
  - 源码建议优先使用 `StartEstimate()`

#### `StartEstimate() -> bool`

开始参数估计，并等待任务结束。

- 返回值：
  - `bool`：是否执行成功

#### `Validate() -> bool`

启动参数验证流程。

- 返回值：
  - `bool`：是否启动成功
- 说明：
  - 源码建议优先使用 `StartValidate()`

#### `StartValidate() -> bool`

开始参数验证，并等待任务结束。

- 返回值：
  - `bool`：是否执行成功

### 4.10 结果查看

#### `GetEstimateReport() -> list`

获取参数估计报告。

- 返回值：
  - `list`：每个元素通常对应一次迭代结果

#### `GetEvaluateResultData() -> dict`

获取当前参数评估结果数据。

- 返回值：
  - `dict`：常见键包括 `Residual`、`time` 和各变量名称

#### `GetEstimateResult() -> str`

获取参数估计结果名称。

- 返回值：
  - 源码注解为 `str`
  - 实际使用中建议以实际返回结果为准

#### `GetEstimateResultData() -> dict`

获取最新一次估计结果数据。

- 返回值：
  - `dict`：常见键包括变量名称、`time`、`Residual`

#### `GetEstimateParamData(resultName: str) -> dict`

获取指定估计结果对应的参数值。

- 参数：
  - `resultName`：结果名称
- 返回值：
  - `dict`：参数名到参数值的映射

#### `SelectEstimateResult(resultName: str) -> bool`

选择一个估计结果用于参数验证。

- 参数：
  - `resultName`：结果名称
- 返回值：
  - `bool`：是否选择成功

#### `GetValidateResultData() -> dict`

获取参数验证结果数据。

- 返回值：
  - `dict`：验证结果数据

### 4.11 数据预处理

#### `ImportData(path: str, dataName: str) -> bool`

导入数据预处理数据。

- 参数：
  - `path`：文件路径
  - `dataName`：本次导入数据的自定义名称
- 返回值：
  - `bool`：是否导入成功

#### `ChangeOffsetData(dataName: str, lineName: str, resultName: str, offsetValue: str) -> bool`

对数据执行偏移处理。

- 参数：
  - `dataName`：数据名称
  - `lineName`：线段名称，也可传入 `all`
  - `resultName`：结果名称
  - `offsetValue`：偏移量，可输入数字、`Initial Value`、`Mean Value`
- 返回值：
  - `bool`：是否处理成功

#### `ScaleData(dataName: str, lineName: str, resultName: str, scaleValue: str) -> bool`

对数据执行缩放处理。

- 参数：
  - `dataName`：数据名称
  - `lineName`：线段名称，也可传入 `all`
  - `resultName`：结果名称
  - `scaleValue`：缩放因子，可输入数字、`Max Value`、`Initial Value`
- 返回值：
  - `bool`：是否处理成功

#### `ExtractData(dataName: str, lineName: str, resultName: str, startTime=0, endTime=1) -> bool`

提取指定时间段数据。

- 参数：
  - `dataName`：数据名称
  - `lineName`：线段名称，也可传入 `all`
  - `resultName`：结果名称
  - `startTime`：开始时间
  - `endTime`：结束时间
- 返回值：
  - `bool`：是否处理成功

#### `ResampleData(dataName: str, lineName: str, resultName: str, resamplePeriod=0.002) -> bool`

对数据进行重采样。

- 参数：
  - `dataName`：数据名称
  - `lineName`：线段名称，也可传入 `all`
  - `resultName`：结果名称
  - `resamplePeriod`：重采样周期
- 返回值：
  - `bool`：是否处理成功

#### `LowFilterData(dataName: str, lineName: str, resultName: str, cutoffFrequency=0.2, filterOrder: int = 4) -> bool`

对数据执行低通滤波。

- 参数：
  - `dataName`：数据名称
  - `lineName`：线段名称，也可传入 `all`
  - `resultName`：结果名称
  - `cutoffFrequency`：截止频率
  - `filterOrder`：滤波器阶数
- 返回值：
  - `bool`：是否处理成功

#### `HighFilterData(dataName: str, lineName: str, resultName: str, cutoffFrequency=0.2, filterOrder: int = 4) -> bool`

对数据执行高通滤波。

- 参数：
  - `dataName`：数据名称
  - `lineName`：线段名称，也可传入 `all`
  - `resultName`：结果名称
  - `cutoffFrequency`：截止频率
  - `filterOrder`：滤波器阶数
- 返回值：
  - `bool`：是否处理成功

#### `BandFilterData(dataName: str, lineName: str, resultName: str, startCutoffFrequency=0.2, endCutoffFrequency=0.9, filterOrder: int = 4) -> bool`

对数据执行带通滤波。

- 参数：
  - `dataName`：数据名称
  - `lineName`：线段名称，也可传入 `all`
  - `resultName`：结果名称
  - `startCutoffFrequency`：截止开始频率
  - `endCutoffFrequency`：截止结束频率
  - `filterOrder`：滤波器阶数
- 返回值：
  - `bool`：是否处理成功

#### `GetDataProcessResult() -> list`

获取全部数据预处理结果名称。

- 返回值：
  - `list`：结果名称列表

#### `GetDataProcessResultData(resultName: str) -> dict`

获取指定预处理结果的数据。

- 参数：
  - `resultName`：结果名称
- 返回值：
  - `dict`：结果数据

#### `ExportData(path: str, resultName: str) -> bool`

导出处理结果为 CSV 文件。

- 参数：
  - `path`：导出路径
  - `resultName`：结果名称
- 返回值：
  - `bool`：是否导出成功

## 5. 常见结果结构

### 5.1 调节参数配置

```python
{
    "paramName": {
        "min": 0.0,
        "max": 1.0,
        "value": 0.5,
        "description": "参数说明"
    }
}
```

### 5.2 估计报告

```python
[
    {
        "iteration": 1,
        "residual": 0.123,
        "paramA": 10.0
    }
]
```

### 5.3 估计选项

```python
{
    "ResidualFunc": ...,
    "ParallelNumber": ...,
    "ContinueEstimate": ...
}
```

## 6. 使用建议

1. 建议先完成参数、试验、变量映射和算法配置，再执行估计。
2. 推荐优先使用 `StartEvaluate()`、`StartEstimate()`、`StartValidate()` 作为对外执行入口。
3. 如果接口返回 `False`，优先检查参数类型、路径合法性和试验配置是否完整。
4. 数据预处理接口中的 `lineName` 通常支持具体线段名，也支持 `all`。

## 7. 示例

```python
from mworks.sysplorer.DesignOptMpe.DesignOptMpe import *

InitialApp("MyModel")
OpenSession(r"D:\demo.session")

SelectTunerParam(("param1", "param2"))
ConfigTunerParam("param1", minVal=0, maxVal=10, initialVal=1)
ConfigTunerParam("param2", minVal=-5, maxVal=5, initialVal=0)

NewExpAttachPath("exp1", r"D:\measure.csv")
SetEstimateExp("exp1")

SelectAlgorithm("Bobyqa")
SetSimulateOption(0.0, 10.0, 0.0, 10.0, 1000)
SetEstimateOption("Mean Absolute Percentage Error", parallelNum=4, continueEstimate=True)

ok = StartEstimate()
if ok:
    print(GetEstimateReport())
    print(GetEstimateResultData())
```
