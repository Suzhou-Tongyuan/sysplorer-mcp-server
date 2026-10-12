# DesignOptExp - 批量仿真 Python API

> 中文说明文件，对应 `SKILL.md`。

## 适用范围

- 适用于 Sysplorer 中 `mworks.sysplorer.DesignOptExp` 批量仿真工具箱。
- 覆盖批量仿真初始化、求解器目录、仿真工作目录、参数批量扫描、结果变量选择和结果读取。
- 当用户希望使用批量仿真功能时，优先使用本技能对应的 `DesignOptExp` 接口，不默认使用 `DesignOptExpGui` 暴露的兼容批量接口。
- 不适用于参数估计、响应优化、敏感度分析或普通建模接口。

## 使用规则

1. 运行会触碰 Sysplorer 的脚本前，先确认会话健康：`session_manager(action="health" | "ensure")`。
2. 生成脚本中不要调用 `ClearAll` 或 `ChangeDirectory`。
3. DesignOptExp 是独立工具箱模块，不要用主 ModelingPy 的 `get_api_document` 查它。应使用：

```python
import mworks.sysplorer.DesignOptExp as exp
print(exp.ListFunctions())
help(exp.BatchSimulate)
```

4. 批量仿真任务优先调用 `DesignOptExp.InitialBatchSimulate(...)` 和 `DesignOptExp.BatchSimulate(...)`；仅当模型试验流程明确要求使用 GUI 模块兼容接口时，才选择 `DesignOptExpGui`。

## 标准流程

1. 加载库并打开模型。
2. 准备批量仿真选项（`options` 为非必填项，按需添加 key/value），如 `startTime`、`stopTime`、`outputStep`、`saveEvent`，可选 `algorithm`、`tolerance`。
3. 调用 `InitialBatchSimulate(modelName, solverPath, storePath, instNum, options)` 初始化批量仿真。该函数返回 `bool`，建议检查返回值。
4. 准备参数列表：`[{"参数名": 参数值}, ...]`。
5. 准备结果变量列表：`[["变量名"], ...]`。
6. 调用 `BatchSimulate(param, resultName)`。
7. 从返回的 `list[dict]` 中读取结果，例如 `res[0]["y"]`、`res[0]["time"]`。
8. 批量仿真结束后，**主动询问用户**是否需要绘制结果图。若用户同意，使用 `matplotlib` 按下方规则绘图。

## 结果绘图

批量仿真结束后，**主动询问**用户：*"批量仿真已完成，是否需要绘制结果图？"*。不得跳过此提示。

用户同意绘图时：

- **使用 `matplotlib`**（`import matplotlib.pyplot as plt`）绘图。
- **直接弹出显示**（`plt.show()`），不保存图片到磁盘（除非用户明确要求）。
- **每个变量一张图**：每个结果变量独立创建一个图窗。
- **所有批次在同一张图上**：对于给定变量，所有批次的曲线叠加在同一坐标轴中，便于横向对比。
- **横轴 = 仿真时间**（`results[i]["time"]`），**纵轴 = 变量值**（`results[i]["var_name"]`）。
- **图例**：每条曲线标注对应的参数值，标识所属批次。

示例绘图脚本：

```python
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

var_names = ["area"]
params = [{"length": 10}, {"length": 12}, {"length": 50}, {"length": 99}]

for var in var_names:
    plt.figure()
    for i, r in enumerate(results):
        label = ", ".join(f"{k}={v}" for k, v in params[i].items())
        if "time" in r:
            plt.plot(r["time"], r[var], label=label)
        else:
            plt.plot(r[var], label=label)
    plt.xlabel("time")
    plt.ylabel(var)
    plt.title(f"Batch Simulation: {var}")
    plt.legend()
    plt.grid(True)
    plt.show()
```

**规则**：
- 不得将不同参数组的点连接成一条连续曲线。
- 若用户只要求特定变量（如 `["area"]`），仅绘制这些变量。
- 若结果中缺少 `time` 数据，用采样序号作为横轴。

## 2026a 注意事项

- `InitialBatchSimulate` 需要传入 `modelName`，返回 `bool`。
- `solverPath` 是求解器目录；2026a 支持在该目录下自动生成求解器，也支持复用手动准备好的求解器。
- `options` 为非必填项，按需添加 key/value。
- 调用初始化前建议先 `LoadLibrary()` 和 `OpenModelFile()`。
- `param` 和 `resultName` 通常长度相同；当 `resultName` 长度为 1 时，会自动补齐到与 `param` 长度相同。

## 排错提示

- 参数名和结果变量名大小写敏感。
- `solverPath` 和 `storePath` 应使用可写的绝对路径。
- 初始化失败时，优先检查模型是否已加载、`modelName` 是否正确。
- `resultName` 长度不为 1 且不等于 `param` 长度时，应先在脚本中归一化。
