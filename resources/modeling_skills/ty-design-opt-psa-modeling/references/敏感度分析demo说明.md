# 敏感度分析 Demo：EyeTracking

原始参考脚本位于：

`<Sysplorer 安装目录>/sys/python/win64/Lib/site-packages/mworks/sysplorer/DesignOptPsa/psa_demo.py`

示例目标：对 `EyeTracking.eyeTrackingModel` 中的 `Tc`、`Tp`、`gainK` 三个参数采样，使用变量匹配需求比较仿真输出 `y` 与测量数据列 `eyedata`，再进行量化敏感度分析。

下面是适合 MCP 文档和自动化脚本使用的安全版本。

```python
import mworks.sysplorer as sysplorer
import mworks.sysplorer.DesignOptPsa as psa

# 如脚本需要自行启动 Sysplorer，可按实际安装路径启用：
# sysplorer.StartSysplorer("-gui", r"C:\Program Files\MWORKS\Sysplorer 2025b\Bin64\mworks.exe")

sysplorer.SetCompileSolver64(1)
sysplorer.LoadLibrary("Modelica")
sysplorer.OpenModelFile(r"C:\path\to\EyeTracking.mo")

psa.InitialApp("EyeTracking.eyeTrackingModel")

print(psa.GetTunerParam())

psa.NewParameterSetAttachParam("set1", ("Tc", "Tp", "gainK"))
psa.SetCurrentParameterSet("set1")

psa.SetParamSamplingData("Tc", psa.NormalSampling(100, 15, 3))
psa.SetParamSamplingData("Tp", psa.UniformSampling(100, 0.005, 0.05))
psa.SetParamSamplingData("gainK", psa.UniformSampling(100, 0.2, 1))

print(psa.GetSamplingResultData())

psa.NewVariableMatchingRequirement("req")
psa.ConfigVariableMatchingRequirement(
    "req",
    r"C:\path\to\eyedata.csv",
    {"y": "eyedata"},
)
psa.SelectRequirement(("req",))

psa.SetSimulateOption(endTime=14)

psa.StartEvaluate()
evaluate_results = psa.GetEvaluateResult()
print("evaluate results:", evaluate_results)

psa.SelectEvaluateResult(evaluate_results[0])

psa.SetQuantifiedMethod(True, True, True)
psa.SetQuantifiedType(True, True, True)

psa.StartQuantifiedAnalysis()
quantified_results = psa.GetQuantifiedResult()
print("quantified results:", quantified_results)

quantified_data = psa.GetQuantifiedResultData(quantified_results[0])
print(quantified_data)

# 返回结构:
# [量化类型, 需求名称, {参数名称: 相关性数值}]

psa.CloseApp()
```

## 关键 API 对应关系

- 初始化工具箱：`InitialApp("EyeTracking.eyeTrackingModel")`
- 创建参数集：`NewParameterSetAttachParam("set1", ("Tc", "Tp", "gainK"))`
- 设置显式样本：`SetParamSamplingData(...)`
- 查看采样结果：`GetSamplingResultData()`
- 创建变量匹配需求：`NewVariableMatchingRequirement("req")`
- 配置测量数据和变量映射：`ConfigVariableMatchingRequirement("req", csvPath, {"y": "eyedata"})`
- 执行评估：`StartEvaluate()`
- 获取评估结果：`GetEvaluateResult()` / `GetEvaluateResultData(resultName)`
- 选择量化分析输入：`SelectEvaluateResult(resultName)`
- 设置量化方法和类型：`SetQuantifiedMethod(...)` / `SetQuantifiedType(...)`
- 执行量化分析：`StartQuantifiedAnalysis()`
- 读取量化结果：`GetQuantifiedResult()` / `GetQuantifiedResultData(resultName)`，其中数据结构为 `[量化类型, 需求名称, {参数名称: 相关性数值}]`
