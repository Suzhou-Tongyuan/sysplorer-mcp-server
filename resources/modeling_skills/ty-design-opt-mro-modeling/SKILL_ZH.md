# DesignOptMro - 响应优化 Python API

> 中文说明文件，对应 `SKILL.md`。

## 适用范围

- 适用于 Sysplorer 中 `mworks.sysplorer.DesignOptMro` 响应优化工具箱。
- 覆盖初始化工具箱、调节参数、固定参数、需求、变量集、算法配置、评估、优化、结果读取和会话保存/加载。
- 不适用于 DesignOptMpe 参数估计、敏感度分析或普通 ModelingPy 建模接口。

## 使用规则

1. 运行会触碰 Sysplorer 的脚本前，先确认会话健康：`session_manager(action="health" | "ensure")`。
2. 生成脚本中不要调用 `ClearAll` 或 `ChangeDirectory`。关闭响应优化用 `mro.CloseApp()`；如果脚本自己启动了 Sysplorer，可在最后调用 `pyapi.Exit()`。
3. DesignOptMro 不是主 ModelingPy `Help()` 命名空间下的接口，不要用 `get_api_document` 查它。应使用：

```python
import mworks.sysplorer.DesignOptMro as mro
print(mro.ListFunctions())
help(mro.StartOptimize)
```

## 独立脚本启动模式

生成 MCP 外部可直接运行的 `.py` 脚本时，DesignOptMro 默认使用 `-q` 无界面方式启动 Sysplorer，并建议显式设置编译器、加载 Modelica、打开模型文件：

```python
import mworks.sysplorer as eng
import mworks.sysplorer.DesignOptMro as mro

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
- 用 `DesignOptMro` 将响应需求转为优化问题。
- 优化前可用 PSA 筛选关键参数；需要测量数据标定时可接 MPE。

## 标准流程

1. 加载或打开目标模型。
2. `mro.InitialApp(modelName, instPath="")` 初始化响应优化。
3. 用 `GetTunerParam()`、`GetFixParam()`、`GetVariable()` 查询可用名称。
4. `SelectTunerParam(...)` 选择调节参数，再用 `ConfigTunerParam(...)` 设置上下限和初值。
5. 如需固定参数，先 `SelectFixParam(...)`，再 `ConfigFixParam(...)`。
6. 新建需求：变量属性、阶跃响应、变量线性边界或变量追踪。
7. 调用对应的 `Config...Requirement(...)` 配置需求。
8. `NewVariableSet(...)` 新建变量集。
9. `SetRequirementVariableSet(...)` 将需求和变量集关联。
10. 可选调用 `SelectRequirement(...)` 指定参与优化的需求；不调用时默认已创建需求全选。
11. 设置仿真、优化、算法选项。
12. 建议先 `StartEvaluate()` 验证配置，再 `StartOptimize()`。
13. 用结果接口读取参数迭代、需求迭代、需求时序和最终参数。
14. `CloseApp()` 关闭响应优化。

## 常用需求类型

- 变量属性需求：`NewVariablePropertyRequirement` + `ConfigVariablePropertyRequirement`。
- 阶跃响应需求：`NewStepResponseRequirement` + `ConfigStepResponseRequirement`。
- 变量线性边界需求：`NewVariableLinearBoundRequirement` + `ConfigVariableLinearBoundRequirement`。注意源码使用这个名称，2024b docx 中的 `NewLinearBoundRequirement` / `ConfigLinearBoundRequirement` 是旧称或文档称呼。
- 变量追踪需求：`NewVariableTrackingRequirement` + `ConfigVariableTrackingRequirement`。

## 排错提示

- 参数名、变量名、需求名、变量集名大小写敏感。
- 调节参数和固定参数互斥。
- 需求必须绑定变量集，否则配置不完整。
- 优化失败时先运行 `StartEvaluate()`，再查看 `GetEvaluateResultData(reqName)`。
- `GetOptimizeStatus()` 返回 `0` 表示优化成功，`-1` 表示未开始或进行中，其它值表示错误。
