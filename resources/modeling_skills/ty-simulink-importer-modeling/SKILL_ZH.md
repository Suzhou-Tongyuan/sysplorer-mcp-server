# SimulinkImporter - Simulink 模型导入 Python API

> 中文说明文件，对应 `SKILL.md`。

## 适用范围

- 适用于 Sysplorer 中 `mworks.sysplorer.SimulinkImporter` 工具箱。
- 覆盖启停工具箱、导入 `.slx` 文件（R2017b–R2024b 版本）为 Sysblock 模型、配置导出路径、Link 子系统库以及数据文件导入。
- 当用户希望导入 Simulink 模型时，优先使用本技能对应的 `SimulinkImporter` 接口。
- 不适用于通用 Modelica/Sysblock 建模、DesignOpt 批量仿真/优化/敏感度分析或 CAD 工具箱操作。

## 使用规则

1. 运行会触碰 Sysplorer 的脚本前，先确认会话健康：`session_manager(action="health" | "ensure")`。
2. SimulinkImporter 是独立工具箱模块，不要用主 ModelingPy 的 `get_api_document` 查它。应使用：

```python
import mworks.sysplorer.SimulinkImporter as slxImporter
print(slxImporter.ListFunctions())
help(slxImporter.ImportSimulinkModel)
```

3. **必须**在调用 `ImportSimulinkModel()` 之前先调用 `OpenSimulinkImporter()`。导入完成后调用 `CloseSimulinkImporter()` 释放资源。

## 标准流程

1. 确保 Sysplorer 就绪。
2. 预加载 Sysblock 建模库：

```python
import mworks.sysplorer as eng
eng.LoadLibrary("SysplorerEmbeddedCoder")
```

3. 打开导入工具：

```python
import mworks.sysplorer.SimulinkImporter as slxImporter
slxImporter.OpenSimulinkImporter()
```

4. **检查数据文件**：查看 `.slx` 模型所在目录下是否存在 `.slxdata` 或其他数据文件，如存在则询问用户是否需要一并导入。

5. **先**导入引用/子模型（含 Link 子系统），如果没有引用/子模型，这个步骤可以跳过：

```python
slxImporter.ImportSimulinkModel(
    SimulinkFilePath="H:/svpwm_section.slx",
    LibraryPath="H:/custom_libs",
    OpenReport=False,
)
```

6. **再**导入主模型（含数据文件）：

```python
slxImporter.ImportSimulinkModel(
    SimulinkFilePath="H:/SVPWM.slx",
    ExportPath="H:/output/",
    LibraryPath="H:/custom_libs",
    DataFilePath="H:/SimulinkImport_SVPWM_Data.slxdata",
    ClearBaseWorkSpace=True,
    OpenReport=False,
)
```

7. 关闭导入工具：

```python
slxImporter.CloseSimulinkImporter()
```

## 接口概览

| 函数 | 说明 |
|---|---|
| `OpenSimulinkImporter()` | 启动导入工具，校验 License，初始化埋点 |
| `CloseSimulinkImporter()` | 关闭导入工具，结束埋点记录 |
| `ImportSimulinkModel(...)` | 导入 `.slx` 模型为 Sysblock |
| `ListFunctions()` | 列出所有可用函数 |

## ImportSimulinkModel 参数

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `SimulinkFilePath` | `str` | 必填 | `.slx` 文件绝对路径 |
| `ExportPath` | `str` | `""` | 生成 Sysblock 模型的路径；空时使用 Sysplorer 工作路径 |
| `LibraryPath` | `str` | `""` | Link 子系统库文件夹，多个用 `;` 分隔 |
| `DataFilePath` | `str` | `""` | `.slxdata` 数据文件绝对路径 |
| `ClearBaseWorkSpace` | `bool` | `True` | 导入前是否清空基础工作区 |
| `OpenReport` | `bool` | `True` | 导入后是否自动打开报告 |

## 排错提示

- 所有路径参数必须使用**绝对路径**。
- 调用 `ImportSimulinkModel` 前必须先调用 `OpenSimulinkImporter`。
- **导入顺序**：引用/子模型必须**先于**主模型导入，如果模型没有依赖关系可以跳过，如果指定顺序的话，需要按顺序导入。
- 导入前需 `LoadLibrary("SysplorerEmbeddedCoder")` 确保 Sysblock 组件可用。
- 确认 `.slx` 文件存在且版本兼容（R2017b–R2024b）。
- 导入前检查 `.slx` 模型所在目录是否存在 `.slxdata` 等数据文件，若存在则询问用户是否通过 `DataFilePath` 导入。
- `LibraryPath` 使用分号（`;`）分隔多个文件夹。
- `DataFilePath` 为.slxdata格式的文件，如果不是这个格式需要提示用户按帮助文档要求生成该数据文件。
- 导入成功后，生成的模型会在 Sysplorer 中自动加载。
- 导入完成后会在模型生成路径下生成报告文件，可从中获取错误和警告信息。
- 完成后调用 `CloseSimulinkImporter` 释放资源
