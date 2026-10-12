# SimulinkImporter Python API 参考

本文根据当前源码 `SimulinkImporter.py`、`simulink_importer_api_demo.py` 和《Simulink模型导入工具 Python API说明.md》整理。

使用方式：

```python
import mworks.sysplorer.SimulinkImporter as slxImporter
```

当前源码提供四个接口：

---

## `ListFunctions()`

列出 SimulinkImporter 中的所有命令函数。

```python
def ListFunctions() -> list:
    pass
```

**参数**：无

**返回**：`list`，每个元素为函数名与描述的字符串。

**示例**：

```python
import mworks.sysplorer.SimulinkImporter as slxImporter
print(slxImporter.ListFunctions())
# OpenSimulinkImporter: 启动SimulinkImporter
# CloseSimulinkImporter: 关闭SimulinkImporter
# ImportSimulinkModel: 导入Simulink模型
```

---

## `OpenSimulinkImporter()`

启动 Simulink 模型导入工具，校验 License 并初始化埋点。

```python
def OpenSimulinkImporter() -> bool:
    pass
```

**参数**：无

**返回**：`bool`，`True` 表示成功，`False` 表示失败。

**说明**：
- 调用 `ImportSimulinkModel` 前必须先调用此函数。
- 重复调用时需先 `CloseSimulinkImporter` 再重新 `OpenSimulinkImporter`。

**示例**：

```python
slxImporter.OpenSimulinkImporter()
```

---

## `CloseSimulinkImporter()`

关闭 Simulink 模型导入工具，结束相关埋点记录。

```python
def CloseSimulinkImporter() -> bool:
    pass
```

**参数**：无

**返回**：`bool`，`True` 表示成功，`False` 表示失败。

**说明**：
- 在完成所有模型导入后调用，释放资源。

**示例**：

```python
slxImporter.CloseSimulinkImporter()
```

---

## `ImportSimulinkModel(...)`

导入 Simulink 模型（`.slx` 文件）为 Sysblock 模型。

```python
def ImportSimulinkModel(
    SimulinkFilePath: str,
    ExportPath: str = "",
    LibraryPath: str = "",
    DataFilePath: str = "",
    ClearBaseWorkSpace: bool = True,
    OpenReport: bool = True
) -> bool:
    pass
```

### 参数

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `SimulinkFilePath` | `str` | 必填 | 导入的 Simulink 模型（`.slx` 文件）的完整路径 |
| `ExportPath` | `str` | `""` | 生成 Sysblock 模型的完整路径；为空时使用 MWORKS.Sysplorer 的工作路径 |
| `LibraryPath` | `str` | `""` | 模型中所有 Link 子系统链接的模型库（`.slx` 文件）所在文件夹；多个文件夹使用分号（`;`）分隔；为空时不导入 Link 子系统 |
| `DataFilePath` | `str` | `""` | 待导入的数据文件（`.slxdata` 文件）完整路径；为空时不导入数据 |
| `ClearBaseWorkSpace` | `bool` | `True` | 导入前是否清空基础工作区 |
| `OpenReport` | `bool` | `True` | 导入后是否自动打开生成的报告 |

### 返回值

`bool`：`True` 表示导入成功，`False` 表示导入失败。

### 说明

- 支持的 Simulink 版本：R2017b–R2024b。
- 调用前需先调用 `OpenSimulinkImporter()`。
- **所有路径参数仅支持绝对路径**。
- 导入成功后，生成的 Sysblock 模型会自动在 MWORKS.Sysplorer 中加载。
- **导入顺序**：如果主模型引用子模型（Link 子系统），子模型须先于主模型导入。

### 调用方式

支持多种参数组合（位置参数和关键字参数可混合使用）：

```python
# 仅指定 .slx 文件（位置参数）
ImportSimulinkModel(SimulinkFilePath)

# 指定 .slx + ExportPath
ImportSimulinkModel(SimulinkFilePath, ExportPath)

# 指定 .slx + ExportPath + LibraryPath
ImportSimulinkModel(SimulinkFilePath, ExportPath, LibraryPath)

# 指定 .slx + ExportPath + LibraryPath + DataFilePath
ImportSimulinkModel(SimulinkFilePath, ExportPath, LibraryPath, DataFilePath)

# 依次指定全部 6 个位置参数
ImportSimulinkModel(SimulinkFilePath, ExportPath, LibraryPath, DataFilePath, ClearBaseWorkSpace, OpenReport)

# 关键字参数混合（位置参数 + 关键字参数）
ImportSimulinkModel(SimulinkFilePath, LibraryPath=lib_path, OpenReport=False)
```

### 示例

**示例 1：默认参数导入**

```python
slxImporter.OpenSimulinkImporter()
slxImporter.ImportSimulinkModel("H:/test_model.slx")
slxImporter.CloseSimulinkImporter()
```

**示例 2：全参数导入**

```python
slxImporter.OpenSimulinkImporter()
slxImporter.ImportSimulinkModel(
    "H:/test_model.slx",
    "H:/output/",
    "H:/custom_lib_dir1;H:/custom_lib_dir2",
    "H:/SimulinkImport_test_model_Data.slxdata",
    True,
    False,
)
slxImporter.CloseSimulinkImporter()
```

**示例 3：混合传参（位置 + 关键字）**

```python
slxImporter.OpenSimulinkImporter()
slxImporter.ImportSimulinkModel(
    "H:/svpwm_section.slx",
    LibraryPath="H:/custom_lib_dir",
    OpenReport=False,
)
slxImporter.CloseSimulinkImporter()
```

---

## 完整工作流（引用模型 + 主模型）

```python
import mworks.sysplorer as eng
import mworks.sysplorer.SimulinkImporter as slxImporter

# 预加载 Sysblock 库
eng.LoadLibrary("SysplorerEmbeddedCoder")

# 启动导入工具
slxImporter.OpenSimulinkImporter()

# 1. 先导入引用模型（带 Link 子系统）
slxImporter.ImportSimulinkModel(
    SimulinkFilePath="H:/svpwm_section.slx",
    LibraryPath="H:/custom_libs",
    OpenReport=False,
)

# 2. 再导入主模型（带数据文件）
slxImporter.ImportSimulinkModel(
    SimulinkFilePath="H:/SVPWM.slx",
    ExportPath="H:/output/",
    LibraryPath="H:/custom_libs",
    DataFilePath="H:/SimulinkImport_SVPWM_Data.slxdata",
    ClearBaseWorkSpace=True,
    OpenReport=False,
)

# 关闭导入工具
slxImporter.CloseSimulinkImporter()
```
