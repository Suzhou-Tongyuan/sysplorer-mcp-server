# 模型试验 Demo 使用说明

## 1. 文档说明

本文以 `DesignOptExpGui.py` 与模型试验示例脚本为依据，给出一个从初始化到结果读取的基础固定参数研究流程。实验设计、蒙特卡洛和时变参数的精简片段见 `模型试验示例.md`。

## 2. 示例目标

示例完成以下工作：

1. 加载模型并初始化模型试验应用。
2. 获取并选择模型参数与输出变量。
3. 新建固定参数批量研究。
4. 给出多组参数值。
5. 配置仿真和模型试验选项。
6. 启动研究并读取结果。

## 3. 基础示例

```python
import mworks.sysplorer as sysplorer
import mworks.sysplorer.DesignOptExpGui as exp

sysplorer.SetCompileSolver64(1)
sysplorer.LoadLibrary("Modelica")
sysplorer.OpenModelFile(r"C:\path\to\rectangle_area.mo")

exp.InitialApp("rectangle_area")
print(exp.GetParameter())
print(exp.GetVariable())

exp.SelectParameter(["length"])
exp.SelectVariable(["area"])
exp.NewBatch("batch1")
exp.SetParameterMatrix("batch1", {"length": [50, 35]})

exp.SetSimulationOption(
    "batch1",
    startTime=0,
    stopTime=1,
    outputStep=0.002,
    algorithm="Dassl",
    tolerance=0.0001,
    saveEvent=True,
)
exp.SetExperimentOption(
    r"C:\path\to\results",
    parallel=10,
    longestSimulateTime=864000,
)

exp.StartSimulation("batch1")
result = exp.GetResultData("batch1", "area")
print(result["time"])
print(result["area-Run1"])
```

## 4. 步骤说明

### 4.1 初始化

`InitialApp("rectangle_area")` 绑定当前研究模型。只有初始化完成后，才能查询参数、选择变量并新建研究。

### 4.2 查询与选择

`GetParameter()` 与 `GetVariable()` 用于核对真实名称；参数名和变量名大小写敏感。使用 `SelectParameter(["length"])` 指定研究输入，使用 `SelectVariable(["area"])` 指定结果变量。

### 4.3 创建研究并提供输入

`NewBatch("batch1")` 创建固定参数组合研究。`SetParameterMatrix("batch1", {"length": [50, 35]})` 表示分别使用两组 `length` 值运行两次仿真。

### 4.4 设置选项

`SetSimulationOption(...)` 针对具体研究设置仿真时间、输出步长和求解算法。

最新源码中的模型试验工作选项接口为：

```python
exp.SetExperimentOption(
    resultPath,
    parallel=10,
    longestSimulateTime=864000,
)
```

- `resultPath`：结果目录。
- `parallel`：并行数，源码说明不大于 `20`。
- `longestSimulateTime`：最长允许仿真时间，超过后自动终止。

### 4.5 执行与结果

`StartSimulation("batch1")` 启动研究。`GetResultData("batch1", "area")` 的源码说明返回 `dict`，示例可读取时间轴与单次运行轨迹，例如 `result["time"]`、`result["area-Run1"]`。

## 5. 研究类型切换

- 固定参数组合：使用 `NewBatch(name)`。
- 实验设计：使用 `NewExperimentDesign(name)`，并用 DOE 函数构造输入矩阵。
- 蒙特卡洛：使用 `NewMentoCarlo(name)`，名称按源码保留 `Mento` 拼写。
- 时变参数：使用 `NewTimeParameter(name)`，输入可为内置波形设置或 CSV 数据列绑定。

## 6. 动态核对接口

当前安装版本支持 `ListFunctions()`：

```python
print(exp.ListFunctions())
```

它返回接口名称和中文说明列表。编写脚本或维护文档时，可先用此接口确认当前版本 API，再查阅 `DesignOptExpGui.md` 获取签名与默认值。
