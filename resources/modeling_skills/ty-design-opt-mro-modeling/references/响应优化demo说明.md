# 响应优化 Demo：矩形面积

示例目标：通过调节矩形长度 `length`，使变量 `area` 的终值最大化。

原始参考脚本位于：

`<Sysplorer 安装目录>/sys/python/win64/Lib/site-packages/mworks/sysplorer/矩形面积example.py`

下面是适合 MCP 文档和自动化脚本使用的安全版本。与 2024b docx 示例相比，去掉了 `ClearAll()`。

```python
import mworks.sysplorer as pyapi
import mworks.sysplorer.DesignOptMro as optimize

# 如脚本需要自行启动 Sysplorer，可按实际安装路径启用：
# path = r"C:\Program Files\MWORKS\Sysplorer 2024b\Bin64\mworks.exe"
# pyapi.StartSysplorer(processPath=path, start_mode="-gui")

file_path = r"C:\path\to\rectangle_area.mo"

pyapi.LoadLibrary("Modelica", "4.0.0")
pyapi.OpenModelFile(file_path)

optimize.InitialApp("rectangle_area")

optimize.SelectTunerParam(("length",))
optimize.ConfigTunerParam("length", minVal=0.001, maxVal=199.99, initialVal=10.0)

optimize.NewVariablePropertyRequirement("Req_1")
optimize.ConfigVariablePropertyRequirement("Req_1", "Final Value", "Maximization")

optimize.NewVariableSet("Set_1", ("area",))
optimize.SetRequirementVariableSet("Req_1", ("Set_1",))

# 首次调试脚本时建议先评估当前参数。
optimize.StartEvaluate()

res = optimize.StartOptimize()
print("StartOptimize", res)

data = optimize.GetOptimizeData()
print("优化后的参数迭代:", data["params"])
print("优化后的需求数据:", data["reqs"])

optimize.CloseApp()

# 如果脚本自己启动并拥有 Sysplorer 进程，可以在最后调用：
# pyapi.Exit()
```

## 关键 API 对应关系

- 初始化工具箱：`InitialApp("rectangle_area")`
- 选择调节参数：`SelectTunerParam(("length",))`
- 配置调节参数：`ConfigTunerParam("length", minVal=0.001, maxVal=199.99, initialVal=10.0)`
- 新建变量属性需求：`NewVariablePropertyRequirement("Req_1")`
- 配置最大化终值：`ConfigVariablePropertyRequirement("Req_1", "Final Value", "Maximization")`
- 新建变量集：`NewVariableSet("Set_1", ("area",))`
- 绑定需求和变量集：`SetRequirementVariableSet("Req_1", ("Set_1",))`
- 执行优化：`StartOptimize()`
- 读取结果：`GetOptimizeData()`
