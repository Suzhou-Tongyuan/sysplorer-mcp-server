# DesignOptPsa - 敏感度分析 Python API

> 中文说明文件，对应 `SKILL.md`。

## 适用范围

- 适用于 Sysplorer 中 `mworks.sysplorer.DesignOptPsa` 敏感度分析工具箱。
- 覆盖工具箱初始化、参数集、参数采样、需求、变量集、评估计算、量化分析和结果读取。
- 不适用于 DesignOptMpe 参数估计、DesignOptMro 响应优化、批量仿真或模型试验 API。

## 使用规则

1. 运行会触碰 Sysplorer 的脚本前，先确认会话健康：`session_manager(action="health" | "ensure")`。
2. 生成脚本中不要调用 `ClearAll` 或 `ChangeDirectory`。敏感度分析结束后使用 `psa.CloseApp()`。
3. DesignOptPsa 是独立工具箱模块，不要用主 ModelingPy 的 `get_api_document` 查它。应使用：

```python
import mworks.sysplorer.DesignOptPsa as psa
print(psa.ListFunctions())
help(psa.StartQuantifiedAnalysis)
```

## 独立脚本启动模式

生成 MCP 外部可直接运行的 `.py` 脚本时，DesignOptPsa 默认使用 `-q` 无界面方式启动 Sysplorer，并建议显式设置编译器、加载 Modelica、打开模型文件：

```python
import mworks.sysplorer as eng
import mworks.sysplorer.DesignOptPsa as psa

eng.StartSysplorer("-q", processPath=r"C:\path\to\mworks.exe")
eng.SetCompileSolver64(1)
eng.LoadLibrary("Modelica")
eng.OpenModelFile(model_path)
# 仅嵌套模型或需要显式打开子模型类时调用：
# eng.OpenModel(model_name)
```

单层模型只需要 `OpenModelFile(model_path)`；只有嵌套模型，或工作流明确需要在加载 `.mo` 后打开子模型类时，才调用 `OpenModel(model_name)`。

只有用户明确需要交互界面时才使用 `-gui`；模型试验由 DesignOptExpGui 技能处理。

## 跨技能组合

五个设计优化技能可以搭配使用：

- 用 `DesignOptExpGui` 生成实验设计矩阵或蒙特卡洛样本。
- 用 `DesignOptExp` 对这些参数组合执行批量仿真。
- 用 `DesignOptPsa` 量化参数对需求或变量的影响。
- 筛选关键参数后可接 MRO 做响应优化，或接 MPE 做参数估计/标定。

## 标准流程

1. 加载或打开目标模型。
2. `psa.InitialApp(modelName, instPath="")` 初始化敏感度分析。
3. 用 `GetTunerParam()` 和 `GetVariable()` 查询可用参数和变量。
4. 创建参数集：`NewParameterSetAttachParam(...)`，或 `NewParameterSet(...)` + `ConfigParameterSet(...)`。
5. `SetCurrentParameterSet(...)` 设置当前参数集。
6. 通过分布配置采样，或直接使用采样函数生成样本后 `SetParamSamplingData(...)`。
7. 新建并配置需求。
8. 对非变量匹配需求，使用 `NewVariableSet(...)` 和 `SetRequirementVariableSet(...)` 绑定变量集。
9. `SelectRequirement(...)` 选择参与计算的需求。
10. `SetSimulateOption(...)` 和 `SetEvaluateOption(...)` 配置仿真/评估。
11. `StartEvaluate()` 执行评估。
12. `GetEvaluateResult()` 和 `GetEvaluateResultData(...)` 读取评估结果。
13. `SelectEvaluateResult(...)` 选择需求偏差。
14. `SetQuantifiedMethod(...)` 和 `SetQuantifiedType(...)` 设置量化分析方法与类型。用户要求“量化分析”或“相关分析”但未指定方法或类型时，默认全部开启：
    `psa.SetQuantifiedMethod(correlation=True, standardizedRegression=True, partialCorrelation=True)` 和
    `psa.SetQuantifiedType(linear=True, ranked=True, kendall=True)`。只有用户明确指定某些方法或类型时，才按用户指定的子集设置。
15. `StartQuantifiedAnalysis()` 执行量化分析。
16. `GetQuantifiedResult()` 和 `GetQuantifiedResultData(...)` 读取量化分析结果；`GetQuantifiedResultData` 返回 `[量化类型, 需求名称, {参数名称: 相关性数值}]`。
17. `CloseApp()` 关闭敏感度分析。

## 常用需求类型

- 变量匹配需求：`NewVariableMatchingRequirement` + `ConfigVariableMatchingRequirement`。
- 变量属性需求：`NewVariablePropertyRequirement` + `ConfigVariablePropertyRequirement`。
- 阶跃响应需求：`NewStepResponseRequirement` + `ConfigStepResponseRequirement`。
- 线性边界需求：源码中创建函数为 `NewLinearBoundRequirement`，配置函数为 `ConfigVariableLinearBoundRequirement`。
- 变量追踪需求：`NewVariableTrackingRequirement` + `ConfigVariableTrackingRequirement`。

## 排错提示

- 参数名、变量名、需求名、变量集名、结果名大小写敏感。
- 分布配置接口作用于当前参数集，调用前应确认 `SetCurrentParameterSet(...)`。
- 每个参数的显式采样列表长度应一致。
- 变量匹配需求中，字典键是仿真变量，值是 CSV 测量列。
- 量化分析前必须先 `SelectEvaluateResult(...)`。
- 量化分析/相关分析的方法与类型默认全选，即 `SetQuantifiedMethod(...)` 与 `SetQuantifiedType(...)` 中所有布尔项为 `True`；除非用户明确指定只选择部分方法或类型。
