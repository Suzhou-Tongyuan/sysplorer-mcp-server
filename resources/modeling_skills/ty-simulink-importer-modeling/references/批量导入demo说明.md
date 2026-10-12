# 批量导入 Demo：Simulink 模型导入

原始参考源码位于：

`C:\Users\TR\Desktop\ai\simulink_importer_mcp\simulink_importer_api_demo.py`

示例目标：启动 SimulinkImporter，按"先导入引用模型、再导入主模型"的顺序批量导入 `.slx` 文件为 Sysblock 模型，配置 Link 子系统库和数据文件，完成后关闭工具。

## 示例 1：引用模型 + 主模型完整导入（原始 Demo）

```python
import mworks.sysplorer as eng
import mworks.sysplorer.SimulinkImporter as slxImporter

eng.StartSysplorer(start_mode="-gui", processPath=r"D:/MWORKS/Sysplorer_2025a_6478/Bin64/mworks.exe")

# 启动导入工具
slxImporter.OpenSimulinkImporter()

# 预加载 Sysblock 建模库
eng.LoadLibrary("SysplorerEmbeddedCoder")

# Demo 文件根目录
demo_dir = r"C:/Users/TR/Desktop/Slx导入/Pyhton API/Demo/"

# 1. 先导入引用模型（带 Link 子系统自定义库）
slx_file_path1 = demo_dir + r"svpwm_section.slx"
lib_paths = demo_dir + r"自定义库"
slxImporter.ImportSimulinkModel(slx_file_path1, LibraryPath=lib_paths, OpenReport=False)

# 2. 再导入主模型（带数据文件）
slx_file_path2 = demo_dir + r"SVPWM.slx"
export_path = demo_dir
data_file_path = demo_dir + r"SimulinkImport_SVPWM_Data.slxdata"
clear_data = True
open_report = False
slxImporter.ImportSimulinkModel(
    slx_file_path2,
    export_path,
    lib_paths,
    data_file_path,
    clear_data,
    open_report,
)

# 关闭导入工具
slxImporter.CloseSimulinkImporter()

eng.Exit()
```

## 示例 2：MCP 兼容版本（无 ClearAll / Exit）

MCP 环境下禁止调用 `ClearAll` 和 `Exit`，Sysplorer 由会话管理，不需要 `StartSysplorer`：

```python
import mworks.sysplorer.SimulinkImporter as slxImporter

slxImporter.OpenSimulinkImporter()

model_dir = r"C:/path/to/models/"
lib_dir = model_dir + r"custom_libs"
data_file = model_dir + r"SimulinkImport_SVPWM_Data.slxdata"

# 先导入引用模型
slxImporter.ImportSimulinkModel(
    SimulinkFilePath=model_dir + "svpwm_section.slx",
    LibraryPath=lib_dir,
    OpenReport=False,
)

# 再导入主模型
slxImporter.ImportSimulinkModel(
    SimulinkFilePath=model_dir + "SVPWM.slx",
    ExportPath=model_dir,
    LibraryPath=lib_dir,
    DataFilePath=data_file,
    ClearBaseWorkSpace=True,
    OpenReport=False,
)

slxImporter.CloseSimulinkImporter()
```

## 示例 3：批量导入多个模型

```python
import mworks.sysplorer.SimulinkImporter as slxImporter

models = {
    "C:/models/model_a.slx": "C:/libs_a",
    "C:/models/model_b.slx": "C:/libs_b",
    "C:/models/model_c.slx": "",
}

slxImporter.OpenSimulinkImporter()

for model_path, lib_path in models.items():
    slxImporter.ImportSimulinkModel(
        SimulinkFilePath=model_path,
        ExportPath="C:/output/",
        LibraryPath=lib_path,
        ClearBaseWorkSpace=False,
        OpenReport=False,
    )

slxImporter.CloseSimulinkImporter()
```

## 关键 API 对应关系

| 步骤 | API |
|---|---|
| 启动导入工具 | `OpenSimulinkImporter()` |
| 预加载 Sysblock 库 | `LoadLibrary("SysplorerEmbeddedCoder")` |
| 导入引用/子模型 | `ImportSimulinkModel(...)`（先导入） |
| 导入主模型 | `ImportSimulinkModel(...)`（后导入，含数据文件） |
| 关闭导入工具 | `CloseSimulinkImporter()` |
| 列出函数 | `ListFunctions()` |

## 注意事项

- **导入顺序**：引用模型（含 Link 子系统）应先于主模型导入。
- **库预加载**：导入前需 `LoadLibrary("SysplorerEmbeddedCoder")` 确保 Sysblock 建模库可用。
- **混合传参**：`ImportSimulinkModel` 支持位置参数和关键字参数混合使用。如示例中引用模型使用关键字传参 `LibraryPath=lib_paths, OpenReport=False`，主模型使用全部位置参数。
- MCP 环境中：禁止 `ClearAll`、`Exit`、`StartSysplorer`（由 `session_manager` 管理）。
