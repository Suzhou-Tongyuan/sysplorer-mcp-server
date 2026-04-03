# 参数估计 Demo 使用说明

## 1. 文档说明

适用场景：

- 希望快速了解参数估计 API 的典型调用顺序
- 希望基于现有示例改写自己的自动化脚本
- 希望对照接口文档理解每一步操作的意义

## 2. 示例目标

该示例完成了以下工作：

1. 启动 Sysplorer 并加载模型库
2. 打开示例模型文件
3. 初始化参数估计环境
4. 选择并配置调节参数
5. 创建试验并绑定测量数据
6. 配置固定参数与变量映射
7. 设置仿真时间
8. 评估当前参数
9. 选择优化算法并启动参数估计
10. 读取估计结果和估计报告
11. 关闭参数估计应用

## 3. 示例脚本整理版

下面是按阅读习惯整理后的示例代码，逻辑与原始脚本保持一致。

```python
import mworks.sysplorer as sysplorer
import mworks.sysplorer.DesignOptMpe as mpe

# 启动 Sysplorer
sysplorer.StartSysplorer("-gui", r"E:\Sysplorer\Sysplorer 2024b\Bin64\mworks.exe")
sysplorer.SetCompileSolver64(1)
sysplorer.LoadLibrary("Modelica", "2.2.2")

# 加载模型文件
sysplorer.OpenModelFile(r"E:\Sysplorer\Sysplorer 2024b\Docs\Samples\Utilities.mo")
sysplorer.OpenModelFile(r"E:\Sysplorer\Sysplorer 2024b\Docs\Samples\ObsoleteModelica3.mo")
sysplorer.OpenModelFile(r"E:\Sysplorer\Sysplorer 2024b\Docs\Samples\SimpleCar.mo")

# 初始化参数估计环境
mpe.InitialApp("SimpleCar")

# 获取并选择调节参数
print(mpe.GetTunerParam())
mpe.SelectTunerParam(("engineTorque.tau_0", "gearBox.lossTable[1,2]"))

# 配置调节参数
mpe.ConfigTunerParam("engineTorque.tau_0", 100, 400, 320)
mpe.ConfigTunerParam("gearBox.lossTable[1,2]", 0, 1, 1)

# 新建试验并绑定测量文件
mpe.NewExpAttachPath("exp", r"E:\Sysplorer\Sysplorer 2024b\Docs\Samples\Acceleration_measurements.csv")

# 设置估计试验
mpe.SetEstimateExp("exp")

# 选择并配置固定参数
mpe.SelectFixParam("exp", ("gearBox.i",))
mpe.ConfigFixParam("exp", "gearBox.i", 2.34)

# 绑定仿真变量和测量变量
mpe.SetSimulateVariable("exp", "carBody.a", "acc")

# 设置仿真时间与估计时间窗
mpe.SetSimulateOption(3.8, 6, 3.8, 6)

# 评估当前参数
mpe.StartEvaluate()
print("GetEvaluateResultData", mpe.GetEvaluateResultData())

# 获取支持的算法并选择 PSO
print(mpe.GetAlgorithm())
mpe.SelectAlgorithm("PSO")
mpe.ConfigPSOAlgorithm()
print(mpe.GetCurrentAlgorithm())

# 启动参数估计
mpe.StartEstimate()

# 获取估计结果
result_names = mpe.GetEstimateResult()
print(result_names)

best_param = mpe.GetEstimateParamData(result_names[0])
print(best_param)

report = mpe.GetEstimateReport()
print(report)

# 关闭参数估计应用
mpe.CloseApp()
```

## 4. 示例分步说明

### 4.1 启动 Sysplorer

```python
sysplorer.StartSysplorer("-gui", r"E:\Sysplorer\Sysplorer 2024b\Bin64\mworks.exe")
sysplorer.SetCompileSolver64(1)
sysplorer.LoadLibrary("Modelica", "2.2.2")
```

这一步用于启动 Sysplorer，并设置编译求解器及基础模型库。

说明：

- `StartSysplorer(...)` 启动 Sysplorer 主程序
- `SetCompileSolver64(1)` 设置 64 位编译求解器
- `LoadLibrary("Modelica", "2.2.2")` 加载所需模型库

如果这一步失败，后续模型加载和参数估计都无法继续。

### 4.2 加载模型文件

```python
sysplorer.OpenModelFile(r"E:\Sysplorer\Sysplorer 2024b\Docs\Samples\Utilities.mo")
sysplorer.OpenModelFile(r"E:\Sysplorer\Sysplorer 2024b\Docs\Samples\ObsoleteModelica3.mo")
sysplorer.OpenModelFile(r"E:\Sysplorer\Sysplorer 2024b\Docs\Samples\SimpleCar.mo")
```

这一步用于加载参数估计所依赖的模型文件。

本示例最终使用的模型是：

- `SimpleCar`

### 4.3 初始化参数估计环境

```python
mpe.InitialApp("SimpleCar")
```

对应接口：

- `InitialApp(modelName, instPath="")`

说明：

- `modelName` 为模型名称
- 这里传入的是 `SimpleCar`
- 初始化成功后，后续才能获取可调参数、创建试验和执行估计

### 4.4 获取并选择调节参数

```python
print(mpe.GetTunerParam())
mpe.SelectTunerParam(("engineTorque.tau_0", "gearBox.lossTable[1,2]"))
```

对应接口：

- `GetTunerParam()`
- `SelectTunerParam(array)`

说明：

- `GetTunerParam()` 用于查看模型中哪些参数可用于调节
- 本示例选择了两个调节参数：
  - `engineTorque.tau_0`
  - `gearBox.lossTable[1,2]`

### 4.5 配置调节参数范围

```python
mpe.ConfigTunerParam("engineTorque.tau_0", 100, 400, 320)
mpe.ConfigTunerParam("gearBox.lossTable[1,2]", 0, 1, 1)
```

对应接口：

- `ConfigTunerParam(paramName, minVal, maxVal, initialVal)`

说明：

- 第 1 个参数是参数名称
- 第 2 个参数是最小值
- 第 3 个参数是最大值
- 第 4 个参数是初始值

本示例含义如下：

- `engineTorque.tau_0` 的搜索范围是 `100 ~ 400`，初始值为 `320`
- `gearBox.lossTable[1,2]` 的搜索范围是 `0 ~ 1`，初始值为 `1`

### 4.6 创建试验并绑定测量数据

```python
mpe.NewExpAttachPath("exp", r"E:\Sysplorer\Sysplorer 2024b\Docs\Samples\Acceleration_measurements.csv")
mpe.SetEstimateExp("exp")
```

对应接口：

- `NewExpAttachPath(expName, path)`
- `SetEstimateExp(expName)`

说明：

- `NewExpAttachPath(...)` 会新建试验并同时绑定测量文件
- 这里的试验名称为 `exp`
- 测量文件为 `Acceleration_measurements.csv`
- `SetEstimateExp("exp")` 将该试验设为估计试验

补充说明：

- 从示例注释看，新建试验时通常也会自动设为估计试验
- 这里显式调用 `SetEstimateExp("exp")`，更适合做成标准示例

### 4.7 配置固定参数

```python
mpe.SelectFixParam("exp", ("gearBox.i",))
mpe.ConfigFixParam("exp", "gearBox.i", 2.34)
```

对应接口：

- `SelectFixParam(expName, array)`
- `ConfigFixParam(expName, paramName, initialVal)`

说明：

- 固定参数是不参与优化、但需要指定取值的参数
- 本示例将 `gearBox.i` 作为固定参数
- 并将其值设置为 `2.34`

### 4.8 绑定仿真变量和测量变量

```python
mpe.SetSimulateVariable("exp", "carBody.a", "acc")
```

对应接口：

- `SetSimulateVariable(expName, simulateVariable, measureVariable)`

说明：

- `carBody.a` 是模型仿真输出变量
- `acc` 是测量文件中的变量名
- 这一步的作用是告诉参数估计模块，应该拿哪个仿真量去对比哪个测量量

### 4.9 设置仿真时间与估计时间窗

```python
mpe.SetSimulateOption(3.8, 6, 3.8, 6)
```

对应接口：

- `SetSimulateOption(SimStartTime, SimEndTime, estimateStartTime, estimateEndTime, stepNumber=500)`

说明：

- 仿真开始时间：`3.8`
- 仿真结束时间：`6`
- 估计开始时间：`3.8`
- 估计结束时间：`6`
- `stepNumber` 未显式传入，因此使用默认值

这表示估计时只对 `3.8s ~ 6s` 时间段内的数据进行比较和优化。

### 4.10 评估当前参数

```python
mpe.StartEvaluate()
print("GetEvaluateResultData", mpe.GetEvaluateResultData())
```

对应接口：

- `StartEvaluate()`
- `GetEvaluateResultData()`

说明：

- `StartEvaluate()` 用于在当前参数配置下先做一次评估
- `GetEvaluateResultData()` 用于读取评估结果
- 返回结果通常包含残差、时间序列及相关变量数据

这一步的意义是：

- 在正式优化前，先看当前参数初值是否合理
- 便于快速检查变量映射、试验数据和时间窗配置是否正确

### 4.11 选择优化算法

```python
print(mpe.GetAlgorithm())
mpe.SelectAlgorithm("PSO")
mpe.ConfigPSOAlgorithm()
print(mpe.GetCurrentAlgorithm())
```

对应接口：

- `GetAlgorithm()`
- `SelectAlgorithm(name)`
- `ConfigPSOAlgorithm(...)`
- `GetCurrentAlgorithm()`

说明：

- `GetAlgorithm()` 可查看当前支持的算法
- 本示例选择的是 `PSO`
- `ConfigPSOAlgorithm()` 这里直接使用默认参数
- `GetCurrentAlgorithm()` 用于确认当前选中的算法

### 4.12 启动参数估计

```python
mpe.StartEstimate()
```

对应接口：

- `StartEstimate()`

说明：

- 该接口会启动参数估计并等待任务完成
- 相比底层接口，`StartEstimate()` 更适合业务脚本直接调用

### 4.13 读取估计结果

```python
result_names = mpe.GetEstimateResult()
print(result_names)

best_param = mpe.GetEstimateParamData(result_names[0])
print(best_param)

report = mpe.GetEstimateReport()
print(report)
```

对应接口：

- `GetEstimateResult()`
- `GetEstimateParamData(resultName)`
- `GetEstimateReport()`

说明：

- `GetEstimateResult()` 用于获取估计结果名称
- 示例中默认读取第一个结果 `result_names[0]`
- `GetEstimateParamData(...)` 用于读取对应结果下的参数值
- `GetEstimateReport()` 用于读取完整的估计迭代报告

通常可以从这些结果中获取：

- 最优参数值
- 每轮迭代的残差变化
- 参数收敛过程

### 4.14 关闭参数估计应用

```python
mpe.CloseApp()
```

对应接口：

- `CloseApp()`

说明：

- 在脚本结束前关闭参数估计应用
- 建议作为示例脚本的收尾步骤保留

## 5. 这个示例用到了哪些接口

本示例实际使用了以下接口：

- `InitialApp`
- `GetTunerParam`
- `SelectTunerParam`
- `ConfigTunerParam`
- `NewExpAttachPath`
- `SetEstimateExp`
- `SelectFixParam`
- `ConfigFixParam`
- `SetSimulateVariable`
- `SetSimulateOption`
- `StartEvaluate`
- `GetEvaluateResultData`
- `GetAlgorithm`
- `SelectAlgorithm`
- `ConfigPSOAlgorithm`
- `GetCurrentAlgorithm`
- `StartEstimate`
- `GetEstimateResult`
- `GetEstimateParamData`
- `GetEstimateReport`
- `CloseApp`

## 6. 使用这个示例时需要替换的内容

在复用该示例到自己的模型时，通常需要替换以下内容：

### 6.1 Sysplorer 安装路径

```python
sysplorer.StartSysplorer("-gui", r"E:\Sysplorer\Sysplorer 2024b\Bin64\mworks.exe")
```

请替换为本机实际安装路径。

### 6.2 模型文件路径

```python
sysplorer.OpenModelFile(...)
```

请替换为自己的模型库和模型文件路径。

### 6.3 模型名称

```python
mpe.InitialApp("SimpleCar")
```

请替换为待估计的模型名称。

### 6.4 调节参数名称和范围

```python
mpe.SelectTunerParam(...)
mpe.ConfigTunerParam(...)
```

请根据自己的模型参数名称和合理范围进行修改。

### 6.5 测量文件路径与试验名称

```python
mpe.NewExpAttachPath("exp", r"...csv")
```

请替换为自己的测量文件路径和试验名称。

### 6.6 固定参数名称

```python
mpe.SelectFixParam(...)
mpe.ConfigFixParam(...)
```

如果你的模型没有固定参数，也可以不使用这一步。

### 6.7 变量映射关系

```python
mpe.SetSimulateVariable("exp", "carBody.a", "acc")
```

请确保：

- 左侧是模型中的仿真变量名
- 右侧是测量文件中的变量名

### 6.8 仿真时间和估计时间窗

```python
mpe.SetSimulateOption(3.8, 6, 3.8, 6)
```

请根据测量数据实际有效区间进行设置。

## 7. 使用建议

1. 推荐先执行 `StartEvaluate()`，确认初始参数和测量映射没有问题，再执行 `StartEstimate()`。
2. 参数范围不要设置得过大，否则可能导致优化效率较低。
3. 测量文件中的变量名应与 `SetSimulateVariable(...)` 中的测量变量名称一致。
4. 如果 `GetEstimateResult()` 返回多个结果，建议逐个读取并比较参数值和残差表现。
5. 如果估计失败，优先检查模型是否能正常仿真、测量文件是否有效、变量映射是否正确。

## 8. 可作为模板的简化版本

如果只想保留最核心的估计流程，可以参考下面这份最小模板：

```python
import mworks.sysplorer as sysplorer
import mworks.sysplorer.DesignOptMpe as mpe

sysplorer.StartSysplorer("-gui", r"你的mworks.exe路径")
sysplorer.SetCompileSolver64(1)
sysplorer.LoadLibrary("Modelica", "2.2.2")

sysplorer.OpenModelFile(r"你的模型文件路径")

mpe.InitialApp("你的模型名")

mpe.SelectTunerParam(("参数1", "参数2"))
mpe.ConfigTunerParam("参数1", 最小值, 最大值, 初始值)
mpe.ConfigTunerParam("参数2", 最小值, 最大值, 初始值)

mpe.NewExpAttachPath("试验名", r"你的测量文件.csv")
mpe.SetEstimateExp("试验名")

mpe.SetSimulateVariable("试验名", "仿真变量名", "测量变量名")
mpe.SetSimulateOption(仿真开始时间, 仿真结束时间, 估计开始时间, 估计结束时间)

mpe.SelectAlgorithm("PSO")
mpe.ConfigPSOAlgorithm()

mpe.StartEstimate()

print(mpe.GetEstimateResult())
print(mpe.GetEstimateReport())

mpe.CloseApp()
```
