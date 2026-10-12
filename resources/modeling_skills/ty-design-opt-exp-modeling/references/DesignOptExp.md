# DesignOptExp Python API 参考

本文根据当前安装包中的 `DesignOptExp.py`、`bs_demo.py` 和《批量仿真 Python API 2026a 接口说明.docx》整理。

使用方式：

```python
import mworks.sysplorer.DesignOptExp as exp
```

当前源码提供两个核心接口：

## `InitialBatchSimulate(modelName: str, solverPath: str, storePath: str, instNum: int = 50, options: dict = {}) -> bool`

初始化批量仿真。返回 `True` 表示成功。

参数：

- `modelName`：模型名称。2026a 新增参数，需传入已加载模型的名称或全名。
- `solverPath`：求解器目录。2026a 支持在该路径下自动生成求解器，也支持复用用户提前准备好的求解器。
- `storePath`：仿真工作目录，使用计算机任意合法可写路径。
- `instNum`：实例池数目，默认 `50`。
- `options`：批量仿真选项字典，非必填，按需添加 key/value。

常用 `options`（均可选，按需挑用）：

```python
{
    "startTime": 0,
    "stopTime": 1,
    "outputStep": 0.02,
    "saveEvent": False,
    "algorithm": "Dassl",
    "tolerance": 1e-6,
}
```

其它可选项包括：

- `"algorithm"`：仿真算法。
- `"tolerance"`：仿真精度。

说明：

- 调用前建议先完成 `LoadLibrary()`、`OpenModelFile()`。
- `solverPath` 下没有可用求解器时，2026a 可根据 `modelName` 自动生成。
- 旧流程中手动准备好的求解器目录仍可作为 `solverPath` 传入。

## `BatchSimulate(param: list, resultName: list)`

执行批量仿真。

参数：

- `param`：仿真参数，类型为 `list[dict[str, number]]`。
- `resultName`：每次仿真的结果变量名称，类型为 `list[list[str]]`。

返回：

- `list[dict[str, list]]`。
- 外层 `list` 为每次仿真的结果。
- 每个 `dict` 中，key 是结果变量名称，value 是该变量的时序值。
- 可通过 `res[index]["变量名"]` 或 `res[index]["time"]` 读取。

示例：

```python
param = [{"length": 100}, {"length": 50}]
result_name = [["area"], ["area"]]
res = exp.BatchSimulate(param, result_name)
print(res[0]["area"])
```

`resultName` 自动补齐规则：

```python
param = [{"length": 100}, {"length": 50}]
result_name = [["area"]]
res = exp.BatchSimulate(param, result_name)
```

当 `resultName` 的长度为 1 时，接口会自动补全为：

```python
[["area"], ["area"]]
```

即对每一组参数都读取相同的结果变量。

## 完整示例

```python
import mworks.sysplorer as sysplorer
import mworks.sysplorer.DesignOptExp as exp

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
    [{"PI1.k": 1, "PI1.T": 1}, {"PI1.k": 1.2, "PI1.T": 1.2}],
    [["y"], ["y", "PI1.y"]],
)

print(res[0]["y"])
```
