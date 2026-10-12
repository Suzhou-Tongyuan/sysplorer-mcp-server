# DesignOptPsa Python API 参考

本文根据当前安装包中的 `DesignOptPsa.py`、`psa_demo.py` 和《敏感度分析 Python API 2025b 说明.docx》整理。

使用方式：

```python
import mworks.sysplorer.DesignOptPsa as psa
```

## 启停工具箱

### `InitialApp(modelName: str, instPath: str = "") -> bool`

检查、翻译模型，并将翻译后的模型拷贝至敏感度分析工具箱。

### `CloseApp() -> bool`

关闭敏感度分析工具箱。

### `GetEvaluateStatus() -> int`

获取需求评估状态。`0` 表示需求评估成功结束，`-1` 表示未开始或正在评估，其它数字表示计算错误。

## 会话

### `OpenSession(path: str) -> bool`

打开敏感度分析会话 XML。

### `SaveSession(path: str) -> str`

保存当前会话。`path` 可以是目录，也可以是具体 XML 文件路径。

## 参数集

### `GetTunerParam() -> list`

获取模型可作为敏感度分析输入的调节参数。

### `NewParameterSet(setName: str) -> bool`

创建空参数集。名称必须以字母或下划线开头，并且只能包含字母、数字和下划线。

### `NewParameterSetAttachParam(name: str, param: tuple) -> bool`

创建参数集并选择参数。

```python
psa.NewParameterSetAttachParam("set1", ("Tc", "Tp", "gainK"))
```

### `ConfigParameterSet(setName: str, param: dict) -> bool`

配置参数集，`param` 形如 `{参数名: 参数值}`。

### `SetCurrentParameterSet(setName: str) -> bool`

设置当前参数集。采样分布配置作用于当前参数集。

### `GetCurrentParameterSet() -> str`

获取当前参数集名称。

### `GetParameterSet() -> list`

获取全部参数集名称。

### `DeleteParameterSet(setName: str) -> bool`

删除参数集。

### `ClearParameterSet() -> bool`

清空参数集。

## 参数采样

### `SetSampleOption(number: int = 10, method: str = "Random", overWrite: bool = True) -> bool`

设置采样数量、采样方法和采样结果生成模式。

- `number`：采样点数量。
- `method`：采样方法，目前文档说明仅支持 `"Random"`。
- `overWrite`：`True` 为覆盖模式，`False` 为追加模式。

### `SetParamSampleDistribution(paramName: str, distribute: str, array: tuple) -> bool`

为当前参数集中的某个参数设置概率密度函数。

常见 `distribute` 值包括：

- `"Uniform Distribution"`：`(Lower, Upper)`
- `"Normal Distribution"`：`(mean, sigma)`
- `"Beta Distribution"`：`(alpha, beta)`
- `"Exponential Distribution"`：`(lambda,)`
- `"Gamma Distribution"`：`(a, b)`
- `"Weibull Distribution"`：`(A, B)`

### `GetDistributionType() -> list`

获取支持的采样分布类型。2025b docx 中标题写作 `GetDistributeType()`，当前源码函数名是 `GetDistributionType()`。

### `StartSampling() -> bool`

根据当前参数集和采样配置生成采样数据。

### `GetSamplingResultData() -> dict`

获取采样结果，形如：

```python
{"Tc": [1, 2, 3], "Tp": [0.01, 0.02, 0.03]}
```

### `SetParamSamplingData(paramName: str, samplingData: list)`

将显式采样列表设置到指定参数。

## 采样函数

这些函数可直接生成采样列表，随后传给 `SetParamSamplingData(...)`。

| 函数 | 说明 |
|---|---|
| `UniformSampling(number=10, lower=-0.05, upper=0.05) -> list` | 均匀分布 |
| `NormalSampling(number=10, mean=1, sigma=0.57735, min=-1e100, max=1e100) -> list` | 正态分布 |
| `BetaSampling(number=10, a=1, b=1, min=-1e100, max=1e100) -> list` | 贝塔分布 |
| `BinbaumSaundersSampling(number=10, beta=0.666667, gamma=1, min=-1e100, max=1e100) -> list` | 伯恩鲍姆-桑德斯分布 |
| `BurrSampling(number=10, alpha=1, c=1, k=1, min=-1e100, max=1e100) -> list` | 伯尔 XII 分布 |
| `ExponentialSampling(number=10, lambdaa=1, min=-1e100, max=1e100) -> list` | 指数分布 |
| `ExtremeValueSampling(number=10, mu=0, sigma=1, min=-1e100, max=1e100) -> list` | 极值分布 |
| `GammaSampling(number=10, a=1, b=1, min=-1e100, max=1e100) -> list` | 伽马分布 |
| `GeneralizedExtremeSampling(number=10, k=0, sigma=1, mu=0, min=-1e100, max=1e100) -> list` | 广义极值分布 |
| `GeneralizedParetoSampling(number=10, k=0, sigma=1, theta=0, min=-1e100, max=1e100) -> list` | 广义帕累托分布 |
| `InverseGaussianSampling(number=10, mu=1, lambdaa=1, min=-1e100, max=1e100) -> list` | 逆高斯分布 |
| `LogisticSampling(number=10, mu=0, sigma=1, min=-1e100, max=1e100) -> list` | 逻辑分布 |
| `LoglogisticSampling(number=10, mu=0, sigma=1, min=-1e100, max=1e100) -> list` | 对数逻辑分布 |
| `LogNormalSampling(number=10, mu=0, sigma=1, min=-1e100, max=1e100) -> list` | 对数正态分布 |
| `MultionmialSampling(number=10, probabilitie=[0.5, 0.5], position=[0, 1], min=-1e100, max=1e100) -> list` | 多项分布，源码参数名为 `probabilitie` |
| `PoissonSampling(number=10, lambdaa=1, min=-1e100, max=1e100) -> list` | 泊松分布 |
| `RayleihSampling(number=10, B=1, min=-1e100, max=1e100) -> list` | 瑞利分布，源码拼写为 `RayleihSampling` |
| `WeibullSampling(number=10, A=1, B=1, min=-1e100, max=1e100) -> list` | 威布尔分布 |
| `GeometricSampling(number=10, P=0.5, min=-1e100, max=1e100) -> list` | 几何分布 |
| `GaussianMixtureSampling(number=10, mu=[5, 2], sigma=[10, 3], P=[0.7, 0.3], min=-1e100, max=1e100) -> list` | 混合高斯分布 |

## 变量和变量集

### `GetVariable() -> list`

获取模型内的所有变量。

### `NewVariableSet(setName: str, array: tuple) -> bool`

新建变量集。

```python
psa.NewVariableSet("Set_1", ("y",))
```

### `SetRequirementVariableSet(reqName: str, array: tuple) -> bool`

将变量集与需求绑定。

### `GetVariableSetInRequirement(reqName: str) -> list`

获取某个需求内的变量集。

## 需求

### `GetRequirement() -> list`

获取支持的需求类型。

### `GetCreatedRequirement() -> list`

获取已经创建的需求。

### `SelectRequirement(array: tuple) -> bool`

选择用于敏感度分析计算的需求。

### `DeleteRequirement(reqName: str) -> bool`

删除需求。

### `ClearRequirement() -> bool`

清空需求。

## 变量匹配需求

### `NewVariableMatchingRequirement(reqName: str) -> bool`

创建变量匹配需求。

### `ConfigVariableMatchingRequirement(reqName: str, path: str, variable: dict, fix: dict = {}) -> bool`

配置变量匹配需求。`variable` 是仿真变量到测量数据列的映射：

```python
psa.ConfigVariableMatchingRequirement("req", r"C:\data\eyedata.csv", {"y": "eyedata"})
```

`fix` 为可选固定参数字典。

## 变量属性需求

### `NewVariablePropertyRequirement(reqName: str) -> bool`

创建变量属性需求。

### `ConfigVariablePropertyRequirement(reqName: str, varProperty: str = "Final Value", varType: str = "Minimization", value=0.0) -> bool`

配置变量属性需求。

`varProperty` 可选最大值、最小值、初值、终值、平均值、中值、方差、四分位差、求和、平方和、绝对值求和等。

`varType` 可选 `"Minimization"`、`"Maximization"`、`"Equal to"`、`"Greater or Equal"`、`"Less or Equal"`。

## 阶跃响应需求

### `NewStepResponseRequirement(reqName: str) -> bool`

创建阶跃响应需求。

### `ConfigStepResponseRequirement(reqName: str, initialValue=0, finalValue=1, stepResponseTime=0, riseTime=5, rise=80, settlingTime=7, settling=1, overshoot=10, undershoot=1) -> bool`

配置阶跃响应需求。

## 线性边界需求

### `NewLinearBoundRequirement(reqName: str) -> bool`

创建线性边界需求。注意：PSA 源码的创建函数名是 `NewLinearBoundRequirement`。

### `ConfigVariableLinearBoundRequirement(reqName: str, boundType: str = "<=", array: tuple = (0, 1, 1, 1)) -> bool`

配置线性边界需求。

## 变量追踪需求

### `NewVariableTrackingRequirement(reqName: str) -> bool`

创建变量追踪需求。

### `ConfigVariableTrackingRequirement(reqName: str, time: tuple = (...), value: tuple = (...), method: str = "Mean Absolute Percentage Error") -> bool`

配置变量追踪需求。

## 仿真评估

### `SetSimulateOption(startTime=0, endTime=1, stepNumber: int = 500) -> bool`

设置仿真开始时间、结束时间和仿真步数。

### `SetEvaluateOption(continueEvaluate: bool = True, saveEvaluate: bool = True, parallelNum: int = int(_num_cores / 2)) -> bool`

设置评估计算选项。

### `StartEvaluate() -> bool`

启动需求评估进程。

### `Evaluate() -> bool`

底层评估接口。面向用户脚本通常优先使用 `StartEvaluate()`。

### `GetEvaluateResult() -> list`

获取评估结果名称。

### `GetEvaluateResultData(resultName: str) -> dict`

查看评估结果。返回值通常包含需求名称及对应残差列表。

## 量化分析

### `SelectEvaluateResult(resultName: str) -> bool`

选择一个评估结果作为量化分析输入。

### `SetQuantifiedMethod(correlation: bool = False, standardizedRegression: bool = False, partialCorrelation: bool = False) -> bool`

设置量化分析方法：相关性、标准化回归、偏相关。

### `SetQuantifiedType(linear: bool = False, ranked: bool = False, kendall: bool = False) -> bool`

设置量化分析类型：皮尔逊、斯皮尔曼、肯德尔。

### `StartQuantifiedAnalysis() -> bool`

启动量化分析进程。

### `GetQuantifiedResult() -> list`

获取量化分析结果名称。

### `GetQuantifiedResultData(resultName: str) -> list`

查看量化分析结果数据。

当前源码返回 `list`，结构为：

```python
[量化类型, 需求名称, {参数名称: 相关性数值}]
```

例如可以按如下方式读取：

```python
quant_type, req_name, correlations = psa.GetQuantifiedResultData(result_name)
```

### `GetQuantifiedMethodAndType() -> dict`

查看当前量化分析方法和类型。

## 文档与源码不一致处

- 2025b docx 标题写 `GetDistributeType()`，当前源码函数为 `GetDistributionType()`。
- docx 中若出现 `LogisticsSampling` / `LoglogisticsSampling`，当前源码函数为 `LogisticSampling` / `LoglogisticSampling`。
- docx 中 `ExpoentialSampling` 是拼写错误，当前源码函数为 `ExponentialSampling`。
- docx 中 `NewVariableSet(name: str, ...)` 应以源码 `NewVariableSet(setName: str, ...)` 为准。
- 用户给出的 `DesignOptMro/DesignOptPsa.py` 路径在当前安装中不存在，实际源码位于 `DesignOptPsa/DesignOptPsa.py`。
