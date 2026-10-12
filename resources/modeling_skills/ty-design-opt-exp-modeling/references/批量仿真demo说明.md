# 批量仿真 Demo：WaterTank

原始参考脚本位于：

`<Sysplorer 安装目录>/sys/python/win64/Lib/site-packages/mworks/sysplorer/bs_demo.py`

示例目标：对 `WaterTank` 模型中 `PI1.k`、`PI1.T` 两组参数进行批量仿真，并读取变量 `y`、`PI1.y`。

下面是适合 MCP 文档和自动化脚本使用的 2026a 版本。

```python
import mworks.sysplorer as sysplorer
import mworks.sysplorer.DesignOptExp as exp

# 如脚本需要自行启动 Sysplorer，可按实际安装路径启用：
# sysplorer.StartSysplorer("-gui", r"C:\Program Files\MWORKS\Sysplorer 2026a\Bin64\mworks.exe")

sysplorer.SetCompileSolver64(1)
sysplorer.LoadLibrary("Modelica")
sysplorer.OpenModelFile(r"C:\path\to\WaterTank.mo")

options = {
    "startTime": 0,
    "stopTime": 1,
    "outputStep": 0.02,
    "saveEvent": False,
}

exp.InitialBatchSimulate(
    modelName="WaterTank",
    solverPath=r"E:\SolverPath\WaterTank",
    storePath=r"E:\BatchSimRes",
    instNum=10,
    options=options,
)

res = exp.BatchSimulate(
    [
        {"PI1.k": 1, "PI1.T": 1},
        {"PI1.k": 1.2, "PI1.T": 1.2},
    ],
    [
        ["y"],
        ["y", "PI1.y"],
    ],
)

print(res[0]["y"])
```

## 关键 API 对应关系

- 初始化批量仿真：`InitialBatchSimulate(modelName, solverPath, storePath, instNum, options)`
- 执行批量仿真：`BatchSimulate(param, resultName)`
- 参数列表：`[{"PI1.k": 1, "PI1.T": 1}, ...]`
- 结果变量列表：`[["y"], ["y", "PI1.y"]]`
- 读取结果：`res[index]["变量名"]`
