> 本文件仅用于中文审核参考，实际任务执行请调用 `SKILL.md`。

# DesignOptExpGui - 模型试验

## Frontmatter 对照

- `name`: `ty-design-opt-exp-gui-modeling`
- `description`: 在 Sysplorer 中使用 `DesignOptExpGui` 完成模型试验任务，包括固定参数批量研究、实验设计、蒙特卡洛、时变参数研究、仿真选项配置和结果读取；也用于维护模型试验 Python API 文档与示例。不要用于仅使用 `DesignOptExp` 的批量仿真任务，也不要用于 MPE、MRO 或 PSA。
- `version`: `1.4.0`

## 适用范围

- **适用**：通过 Python 创建模型试验研究、生成采样矩阵、执行试验、读取结果，或同步 `DesignOptExpGui.py` 相关说明文档。
- **不适用**：用户需要批量仿真功能时，优先使用 `ty-design-opt-exp-modeling` 中的 `DesignOptExp` 接口；仅当模型试验流程明确依赖 GUI 模块兼容接口时才使用此技能。参数估计、响应优化和敏感度分析分别使用对应技能。

## 硬性规则

1. 在触及 Sysplorer 的脚本前先确保会话可用。
2. 禁止调用 `ClearAll` 或 `ChangeDirectory`；需要卸载模型时使用 `model_manager(action="unload")`。
3. 将安装目录中的 `DesignOptExpGui.py` 作为接口签名的最终依据。
4. 在 `run_sysplorer_api` 中显式导入独立工具箱：

```python
import mworks.sysplorer.DesignOptExpGui as exp
```

5. 此工具箱不通过主 ModelingPy `get_api_document` 查询帮助；动态核对接口时使用 `exp.ListFunctions()` 或 `help(exp.xxx)`。
6. 将批量仿真请求优先路由到 `DesignOptExp.InitialBatchSimulate(...)` 与 `DesignOptExp.BatchSimulate(...)`，不要默认使用 `DesignOptExpGui` 中的兼容接口。

## 独立脚本启动模式

生成 MCP 外部可直接运行的 `.py` 脚本时，DesignOptExpGui 模型试验默认使用 `-gui` 方式启动 Sysplorer。模型试验是设计优化工具箱中区别于 MPE、MRO、PSA 和批量仿真的例外，后者默认使用 `-q` 无界面方式。

```python
import mworks.sysplorer as eng
import mworks.sysplorer.DesignOptExpGui as exp

eng.StartSysplorer("-gui", processPath=r"C:\path\to\mworks.exe")
eng.SetCompileSolver64(1)
eng.LoadLibrary("Modelica")
eng.OpenModelFile(model_path)
# 仅嵌套模型或需要显式打开子模型类时调用：
# eng.OpenModel(model_name)
```

单层模型只需要 `OpenModelFile(model_path)`；只有嵌套模型，或工作流明确需要在加载 `.mo` 后打开子模型类时，才调用 `OpenModel(model_name)`。

## 资料入口

- `references/DesignOptExpGui.md`：接口签名、默认值、源码特殊拼写与文档同步记录。
- `references/模型试验使用说明.md`：不同研究类型的参数矩阵结构和运行流程。
- `references/模型试验demo说明.md`：从初始化到读取结果的基础示例分解。
- `references/模型试验示例.md`：实验设计、蒙特卡洛、时变参数等精简脚本片段。

## 标准执行流程

1. 加载或打开模型。
2. 调用 `exp.InitialApp(modelName)` 初始化模型试验。
3. 通过 `exp.GetParameter()`、`exp.GetVariable()` 确认参数和变量真实名称。
4. 使用 `exp.SelectParameter([...])`、`exp.SelectVariable([...])` 选择输入和结果。
5. 按目标创建研究：
   - 固定参数组合：`NewBatch(name)`
   - 实验设计：`NewExperimentDesign(name)`
   - 蒙特卡洛：`NewMentoCarlo(name)`，保留源码中的 `Mento` 拼写
   - 时变参数：`NewTimeParameter(name)`
6. 使用 `SetParameterMatrix(name, parameters)` 设置输入。
7. 按需调用 `SetSimulationOption(...)` 和 `SetExperimentOption(resultPath, parallel=10, longestSimulateTime=864000)`。
8. 调用 `StartSimulation(name)` 执行研究。
9. 调用 `GetResultData(studyName, varName)` 获取轨迹数据。

## 关键接口边界

- `SetExperimentOption` 最新签名包含 `longestSimulateTime=864000`，超时后仿真自动终止。
- `GetResultData(studyName, varName)` 的源码说明返回 `dict`。
- `ListFunctions()` 返回接口名称和中文说明列表。
- 兼容接口 `InitialBatchSimulate(solverPath, storePath, instNum=50, options={})` 不含 `modelName`，不要套用 `DesignOptExp` 2026a 的签名。

## 跨技能组合

五个设计优化技能可以搭配使用。若用户需要“先设计/采样，再批量仿真”，优先采用：

1. 使用本技能的 `DesignOptExpGui` 实验设计或蒙特卡洛采样函数生成参数数据，例如 `LatinHypercubeDesign(...)`、`DOptimalDesign(...)`、`UniformSampling(...)`。
2. 将生成的矩阵或样本数组转换为 `DesignOptExp.BatchSimulate` 所需的 `list[dict[参数名, 参数值]]`。
3. 使用 `ty-design-opt-exp-modeling` 中的 `DesignOptExp.InitialBatchSimulate(...)` 和 `DesignOptExp.BatchSimulate(...)` 执行批量仿真。
4. 后续按目标选择 PSA、MRO 或 MPE 继续分析。

## 排错清单

- 参数名、变量名和研究名大小写敏感，以实际枚举结果为准。
- 在 `SetParameterMatrix` 前先创建研究并完成参数/变量选择。
- 如果固定值、设计矩阵或采样结果的长度不一致，先统一各参数的运行样本数。
- 如需确认当前安装版本提供的接口，优先打印 `exp.ListFunctions()`。
