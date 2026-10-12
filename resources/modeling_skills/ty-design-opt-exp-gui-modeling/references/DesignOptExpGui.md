# DesignOptExpGui Python API 参考

本文以安装包中的 `DesignOptExpGui/DesignOptExpGui.py` 为准，并对照《模型试验 Python API 2025b 接口说明.docx》和配套示例整理。

```python
import mworks.sysplorer.DesignOptExpGui as exp
```

## 初始化与会话

| API | 说明 |
|---|---|
| `InitialApp(modelName: str) -> bool` | 初始化模型试验。 |
| `OpenSession(path: str) -> bool` | 打开模型试验会话。 |
| `SaveSession(path: str) -> bool` | 保存模型试验会话。 |

## 参数与变量

| API | 说明 |
|---|---|
| `GetParameter() -> list` | 获取模型全部参数。 |
| `GetVariable() -> list` | 获取模型全部变量。 |
| `SelectParameter(parameters: list) -> bool` | 选择研究输入参数。 |
| `SelectVariable(variables: list) -> bool` | 选择结果变量。 |

## 研究类型

| API | 说明 |
|---|---|
| `NewBatch(name: str) -> bool` | 新建固定参数组合/批量研究。 |
| `NewExperimentDesign(name: str) -> bool` | 新建实验设计研究。 |
| `NewMentoCarlo(name: str) -> bool` | 新建蒙特卡洛研究。源码名称为 `Mento`，脚本须保持此拼写。 |
| `NewTimeParameter(name: str) -> bool` | 新建时变参数研究。 |
| `GetStudyName() -> list` | 获取已创建研究名称。 |

## 配置与执行

### `SetParameterMatrix(name: str, parameters: dict) -> bool`

为研究设置参数矩阵。不同研究类型使用不同形状，详见 `模型试验使用说明.md`。

### `SetSimulationOption(name: str, startTime=0, stopTime=1, outputStep=0.002, algorithm: str = "Dassl", tolerance=0.0001, saveEvent: bool = True)`

设置单个研究的仿真选项。

### `SetExperimentOption(resultPath: str, parallel: int = 10, longestSimulateTime = 864000)`

设置模型试验工作选项，包括结果路径、并行数和允许的最长仿真时间。`longestSimulateTime` 超过后仿真自动终止；当前源码默认值为 `864000`。

### `StartSimulation(name: str) -> bool`

启动指定研究的仿真。

### `GetResultData(studyName: str, varName: str)`

获取指定研究、指定变量的数据。示例中结果含 `"time"` 与 `"area-Run1"` 一类运行轨迹键。

### `ListFunctions() -> list`

列出当前 `DesignOptExpGui` 模块的接口名称和中文说明，适合在脚本中核查当前安装版本公开的 API。

## 实验设计

| API | 说明 |
|---|---|
| `EquallySpacedSampling(initialValue=100, stepLength=5, lowerNum: int=2, upperNum: int=1) -> list` | 等间距采样。 |
| `FullFactorialDesign(level: list) -> list` | 全因子设计。 |
| `OrthogonalDesign(level: list) -> list` | 正交设计。 |
| `LatinHypercubeDesign(number: int, minValue: list, maxValue: list) -> list` | 拉丁超立方设计。 |
| `CenterCompositeDesign(minValue: list, maxValue: list, centerNum: list=[1, 1], typeFace: int=0, typeAlpha: int=0) -> list` | 中心复合设计。 |
| `DOptimalDesign(minValue: list, maxValue: list, number: int=10, algoType: int=0) -> list` | D 最优设计。 |

## 蒙特卡洛采样

各采样接口返回 `list`。当前源码默认采样数通常为 `20`，并带可选随机种子 `seed=0.612702`。

| API | 说明 |
|---|---|
| `UniformSampling(number=20, lower=-0.05, upper=0.05, seed=0.612702) -> list` | 均匀分布。 |
| `NormalSampling(number=20, mean=1, sigma=0.57735, seed=0.612702, min=-1e100, max=1e100) -> list` | 正态分布。 |
| `BetaSampling(number=20, a=1, b=1, seed=0.612702, min=-1e100, max=1e100) -> list` | 贝塔分布。 |
| `BinbaumSaundersSampling(number=20, beta=0.666667, gamma=1, seed=0.612702, min=-1e100, max=1e100) -> list` | 伯恩鲍姆-桑德斯分布。 |
| `BurrSampling(number=20, alpha=1, c=1, k=1, seed=0.612702, min=-1e100, max=1e100) -> list` | 伯尔 XII 分布。 |
| `ExponentialSampling(number=20, lambdaa=1, seed=0.612702, min=-1e100, max=1e100) -> list` | 指数分布。 |
| `ExtremeValueSampling(number=20, mu=0, sigma=1, seed=0.612702, min=-1e100, max=1e100) -> list` | 极值分布。 |
| `GammaSampling(number=20, a=1, b=1, seed=0.612702, min=-1e100, max=1e100) -> list` | 伽马分布。 |
| `GeneralizedExtremeSampling(number=20, k=0, sigma=1, mu=0, seed=0.612702, min=-1e100, max=1e100) -> list` | 广义极值分布。 |
| `GeneralizedParetoSampling(number=20, k=0, sigma=1, theta=0, seed=0.612702, min=-1e100, max=1e100) -> list` | 广义帕累托分布。 |
| `InverseGaussianSampling(number=20, mu=1, lambdaa=1, seed=0.612702, min=-1e100, max=1e100) -> list` | 逆高斯分布。 |
| `LogisticSampling(number=20, mu=0, sigma=1, seed=0.612702, min=-1e100, max=1e100) -> list` | 逻辑分布。 |
| `LoglogisticSampling(number=20, mu=0, sigma=1, seed=0.612702, min=-1e100, max=1e100) -> list` | 对数逻辑分布。 |
| `LogNormalSampling(number=20, mu=0, sigma=1, seed=0.612702, min=-1e100, max=1e100) -> list` | 对数正态分布。 |
| `MultionmialSampling(number=20, probabilitie=[0.5, 0.5], position=[0, 1], seed=0.612702, min=-1e100, max=1e100) -> list` | 多项分布；保留源码拼写。 |
| `PoissonSampling(number=20, lambdaa=1, seed=0.612702, min=-1e100, max=1e100) -> list` | 泊松分布。 |
| `RayleihSampling(number=20, B=1, seed=0.612702, min=-1e100, max=1e100) -> list` | 瑞利分布；保留源码拼写。 |
| `WeibullSampling(number=20, A=1, B=1, seed=0.612702, min=-1e100, max=1e100) -> list` | 威布尔分布。 |
| `GeometricSampling(number=20, P=0.5, seed=0.612702, min=-1e100, max=1e100) -> list` | 几何分布。 |
| `GaussianMixtureSampling(number=20, mu=[5, 2], sigma=[10, 3], P=[0.7, 0.3], seed=0.612702, min=-1e100, max=1e100) -> list` | 混合高斯分布。 |

## 返回值说明

- `SetSimulationOption(...)` 和 `SetExperimentOption(...)` 的源码签名未标注返回类型，但 docstring 声明返回 `bool`。
- `GetResultData(studyName, varName)` 的源码 docstring 声明返回 `dict`。
- `ListFunctions()` 的源码 docstring 声明返回 `list`，每个元素格式为 `接口名: 中文注释`。

## 兼容的批量仿真接口

安装模块同时公开：

- `InitialBatchSimulate(solverPath: str, storePath: str, instNum: int=50, options: dict={})`
  - 注意：该 GUI 模块签名不包含 `modelName`，与 `DesignOptExp` 2026a 批量仿真模块不同。
- `BatchSimulate(param: list, resultName: list)`

对仅使用这两个接口的任务，优先参考 `ty-design-opt-exp-modeling`。

## 文档同步记录

《模型试验 Python API 2025b 接口说明.docx》此前已按当时源码同步修正以下历史差异：

- 示例脚本曾混用 `DesignOptExp` 与 `DesignOptExpGUI`；现统一使用源码模块路径 `DesignOptExpGui`。
- 曾写作 `ExpoentialSampling`、`LogisticsSampling`、`LoglogisticsSampling`；现同步为 `ExponentialSampling`、`LogisticSampling`、`LoglogisticSampling`。
- 多个采样接口默认值曾为 `number=10`；现同步为源码中的 `number=20`。
- `BetaSampling` 默认值曾为 `b=0.57735`；现同步为 `b=1`。
- `GammaSampling` 默认值曾为 `a=0`；现同步为 `a=1`。
- `GeometricSampling` 参数曾写为 `A`、`B`；现同步为 `P=0.5`。
- `SetExperimentOption(resultPath, parallel)` 曾未标默认值；现同步为 `parallel=10`。
- 原文档未说明的兼容接口 `InitialBatchSimulate(...)`、`BatchSimulate(...)` 及返回值边界说明已补充。
- 最新 `DesignOptExpGui.py` 已将接口扩展为 `SetExperimentOption(resultPath, parallel=10, longestSimulateTime=864000)`；该新增参数和 `ListFunctions()` 现已同步写入 2025b docx。
