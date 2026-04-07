# SYSPLORER API LIST (2026a)

- Generated: 2026-03-10T23:47:33+08:00
- Source: Sysplorer 2026a local offline docs (page-data-list.json)
- API Count: 154
- Fields: Interface Name / Description / Syntax / Input Parameters / Returns

## ModelingPy

### EnvironmentalCustomization

#### ChangeCacheDirectory

- Interface Name: `ChangeCacheDirectory`
- Description: 用于设置缓存目录，并打印（设置后的）缓存目录到命令窗口。 cacheDirectory：缓存目录更改为此目录，如果是空字符串，则显示当前缓存目录。
- Syntax:
```text
ChangeCacheDirectory(cacheDirectory)
```
- Input Parameters:
```text
cacheDirectory - 更改的缓存目录
   数据类型： str
```
- Returns:
```text
bool：表示函数执行的成功或失败状态
```

#### ChangeDirectory

- Interface Name: `ChangeDirectory`
- Description: 用于设置工作目录，并打印（设置后的）当前目录到命令窗口，如果是空字符串，则显示当前工作目录。
- Syntax:
```text
ChangeDirectory(workDir)
```
- Input Parameters:
```text
workDir - 工作目录
   数据类型： str
```
- Returns:
```text
bool：表示函数执行的成功或失败状态
```

#### ChangeSimResultDirectory

- Interface Name: `ChangeSimResultDirectory`
- Description: 用于将仿真结果目录更改为此目录，如果是空字符串，则显示当前仿真结果目录。
- Syntax:
```text
ChangeSimResultDirectory(simResultDirectory)
```
- Input Parameters:
```text
simResultDirectory - 仿真结果目录
   数据类型： str
```
- Returns:
```text
bool：表示函数执行的成功或失败状态
```

#### ClearAll

- Interface Name: `ClearAll`
- Description: 软件恢复到启动状态，恢复成功返回 True，恢复失败返回 False。
- Syntax:
```text
ClearAll()
```
- Input Parameters:
```text
无参数
```
- Returns:
```text
bool：表示函数执行的成功或失败状态
```

#### Echo

- Interface Name: `Echo`
- Description: 用于设置/获取是否打开 “反馈每条语句的执行结果” 功能，打开则传入 True，关闭则传入 False，如果不传入参数，则返回当前状态。
- Syntax:
```text
Echo(on)
```
- Input Parameters:
```text
on - 设置状态
   数据类型： bool  None
```
- Returns:
```text
bool：表示该功能是否开启
```

#### Exit

- Interface Name: `Exit`
- Description: 用于退出 Sysplorer，若此时存在修改但未保存的实例或模型时，不会弹出是否保存提示框。
- Syntax:
```text
Exit()
```
- Input Parameters:
```text
无参数
```
- Returns:
```text
bool：表示程序是否正常退出
```

#### GetCacheDirectory

- Interface Name: `GetCacheDirectory`
- Description: 用于获取缓存目录。
- Syntax:
```text
GetCacheDirectory()
```
- Input Parameters:
```text
无参数
```
- Returns:
```text
str：缓存目录路径
```

#### GetDirectory

- Interface Name: `GetDirectory`
- Description: 用于获取工作目录。
- Syntax:
```text
GetDirectory()
```
- Input Parameters:
```text
无参数
```
- Returns:
```text
str：工作目录
```

#### GetInstallationDirectory

- Interface Name: `GetInstallationDirectory`
- Description: 用于获取软件安装目录。
- Syntax:
```text
GetInstallationDirectory()
```
- Input Parameters:
```text
无参数
```
- Returns:
```text
str：安装目录
```

#### GetKernelVersion

- Interface Name: `GetKernelVersion`
- Description: 用于获取软件内核版本号。
- Syntax:
```text
GetKernelVersion()
```
- Input Parameters:
```text
无参数
```
- Returns:
```text
str：内核版本号
```

#### GetLanguage

- Interface Name: `GetLanguage`
- Description: 用于获取当前系统语言。
- Syntax:
```text
GetLanguage()
```
- Input Parameters:
```text
无参数
```
- Returns:
```text
str：当前系统语言
```

#### GetLastErrors

- Interface Name: `GetLastErrors`
- Description: 用于获取上一条命令的错误信息，若上一条的命令是正确的，既没有错误信息，将返回空。
- Syntax:
```text
GetLastErrors()
```
- Input Parameters:
```text
无参数
```
- Returns:
```text
list：上一条错误信息
```

#### GetOption

- Interface Name: `GetOption`
- Description: 用于获取某个具体首选项的值，未获取到时，取默认值，此时将默认值设到系统中。
- Syntax:
```text
GetOption(name)
GetOption(name,defaultValue)
```
- Input Parameters:
```text
name - 首选项的名称
   数据类型： str
  defaultValue - 未获取到时，取的默认值
   数据类型： str  int  bool  list  None
```
- Returns:
```text
Any：目标首选项的值
```

#### GetSimResultDirectory

- Interface Name: `GetSimResultDirectory`
- Description: 用于获取仿真结果目录。
- Syntax:
```text
GetSimResultDirectory()
```
- Input Parameters:
```text
无参数
```
- Returns:
```text
str：仿真结果目录
```

#### GetVersion

- Interface Name: `GetVersion`
- Description: 用于获取软件版本号。
- Syntax:
```text
GetVersion()
```
- Input Parameters:
```text
无参数
```
- Returns:
```text
str：软件版本号
```

#### Help

- Interface Name: `Help`
- Description: Help() 用于显示 Sysplorer API 的帮助。
Help(cmd) 用于显示指定命令的帮助。
- Syntax:
```text
Help()
Help(cmd)
```
- Input Parameters:
```text
cmd - 命令名
   数据类型：str
```
- Returns:
```text
str  表示 Sysplorer API 或指定命令的帮助。
```

#### License

- Interface Name: `License`
- Description: 依据传入的不同的 ltype 进行不同的许可证相关操作，函数会依据传入 ltype 的不同进行不同的处理并返回不同的结果。
- Syntax:
```text
License(ltypestr, lparamsdict = {})
```
- Input Parameters:
```text
ltype - 操作的类型
   "activate", 激活许可证 "deactivate", 移除许可证 "device_code", 获取设备码 "feature_list", 获取特征项列表 "expired_days", 获取许可证或特征项剩余时间 'info' 获取许可证信息 数据类型： str
  lparams - 依据 ltype 传入不同的lparams
   ltype = "activate"： 单服务器激活 {"type""server","server1""IPPort"} 主从服务器激活 {"type""server","server1""IPPort","server2""IPPort","server3""IPPort"} 文件激活 {"type""file","path""许可证文件的绝对路径"} 账号激活 {"type""account"} ltype = "deactivate" 无需参数 ltype = "device_code" 无需参数 ltype = "feature_list" 无需参数 ltype = "expired_days" 获取基础环境许可证剩余时间 无需参数 获取特定特征项剩余事件 {"name""特征项名称"} ltype = "info" 无需参数
   数据类型： int  bool  str
```
- Returns:
```text
Any：依据 ltype 返回不同的结果
```

#### ListFunctions

- Interface Name: `ListFunctions`
- Description: ListFunctions() 用于列出所有命令函数，结果每行每个元素表示函数的名字和描述。
- Syntax:
```text
ListFunctions()
```
- Input Parameters:
```text
无
```
- Returns:
```text
str：每个元素表示函数的名字和描述，并使用 '\n' 分割。
```

##### 参数设计 / 优化 / MPE 工具箱（DesignOptMpe）

会话内主建模 API 的 `ListFunctions()`（例如通过 `call_code` 的 `run_script` 注入的 `ModelingPy.ListFunctions()`）列出的是**主命令空间**的函数，**不包含** `DesignOptMpe`（参数设计、优化、参数估计等）工具箱内的接口。

当使用**参数设计、优化工具、MPE** 等相关能力时，应在脚本中先：

```python
import mworks.sysplorer.DesignOptMpe as mpe
```

然后：

- 使用 **`mpe.ListFunctions()`** 获取 MPE 工具箱中的全部命令函数（形式与主 API 的 `ListFunctions` 类似：每行/每项为函数名与简短描述）。
- 使用 **`help(mpe.函数名)`**（例如 `help(mpe.InitialApp)`）查看该 MPE API 函数的 Python 帮助文档。

主建模命令的说明仍可通过 MCP **`get_api_document(api_function_name="...")`**（对应运行时 `Help(cmd)`）获取；MPE 侧优先在脚本内使用 `help(mpe.xxx)`，并可配合旁置语料 **`resources/design_opt_mpe_api/`** 与检索索引 **`design_opt_mpe_api`**：实操流程与常见问题见 **`参数估计使用说明.md`**，各函数接口与参数见 **`DesignOptMpe.md`**，Demo 步骤见 **`参数估计demo说明.md`**。

##### CAD 工具箱（CADToolbox）

会话内主建模 API 的 `ListFunctions()`（例如通过 `call_code` 的 `run_script` 注入的 `ModelingPy.ListFunctions()`）列出的是**主命令空间**的函数，**不包含** **CAD 工具箱**（`CADToolbox`）内的接口。

当使用 **CAD 相关**能力时，应在脚本中先：

```python
import mworks.sysplorer.CADToolbox as cadtool
```

然后：

- 使用 **`cadtool.ListFunctions()`** 获取 CAD 工具箱中的全部命令函数（形式与主 API 的 `ListFunctions` 类似：每行/每项为函数名与简短描述）。
- 使用 **`help(cadtool.函数名)`** 查看该 CAD API 函数的 Python 帮助文档。

主建模命令的说明仍可通过 MCP **`get_api_document(api_function_name="...")`**（对应运行时 `Help(cmd)`）获取；CAD 工具箱侧优先在脚本内使用 `help(cadtool.xxx)`，**请勿**先对 CAD 函数名调用 `get_api_document`（常见无有效文档），并可配合工作区 **`resources/cad_toolbox_api/`** 语料与检索索引 **`cad_toolbox_api`**。

##### Simulink 导入工具箱（SimulinkImporter）

会话内主建模 API 的 `ListFunctions()`（例如通过 `call_code` 的 `run_script` 注入的 `ModelingPy.ListFunctions()`）列出的是**主命令空间**的函数，**不包含** **Simulink 导入工具箱**（`SimulinkImporter`）内的接口。

当使用 **Simulink / SLX 导入**等相关能力时，应在脚本中先：

```python
import mworks.sysplorer.SimulinkImporter as slximport
```

然后：

- 使用 **`slximport.ListFunctions()`** 获取 Simulink 导入工具箱中的全部命令函数（形式与主 API 的 `ListFunctions` 类似：每行/每项为函数名与简短描述）。
- 使用 **`help(slximport.函数名)`** 查看该 API 函数的 Python 帮助文档。

**Simulink 导入工具箱的推荐用法（顺序固定）**：**必须先**调用 **`OpenSimulinkImporter()`** 启动导入工具；**再**调用 **`ImportSimulinkModel(SimulinkFilePath, ...)`**，其中 **`SimulinkFilePath`** 为待导入 **`.slx` 的绝对路径**（必选），其余参数 **`ExportPath`、`LibraryPath`、`DataFilePath`、`ClearBaseWorkSpace`、`OpenReport`** 均为可选（默认值与含义以 `help(slximport.ImportSimulinkModel)` 为准）。完成后可按需调用 **`CloseSimulinkImporter()`**。详见工作区 **`resources/simulink_importer_api/SimulinkImporter.md`**。

主建模命令的说明仍可通过 MCP **`get_api_document(api_function_name="...")`**（对应运行时 `Help(cmd)`）获取；Simulink 导入工具箱侧优先在脚本内使用 `help(slximport.xxx)`，**请勿**先对导入工具箱函数名调用 `get_api_document`（常见无有效文档），并可配合工作区 **`resources/simulink_importer_api/`** 语料与检索索引 **`simulink_importer_api`**。

#### ListOptions

- Interface Name: `ListOptions`
- Description: 用于打印所有系统首选项。
- Syntax:
```text
ListOptions()
```
- Input Parameters:
```text
无参数
```
- Returns:
```text
dict：包含系统首选项及对应的值
```

#### ListVariables

- Interface Name: `ListVariables`
- Description: ListVariables() 用于列出所有变量，这些变量用于部分命令的参数别名。
- Syntax:
```text
ListVariables()
```
- Input Parameters:
```text
无
```
- Returns:
```text
str：每个元素表示变量的名字和描述，并使用 '\n' 分割。
```

#### SendHeart

- Interface Name: `SendHeart`
- Description: 用于保持 Sysplorer API 客户端与服务端的连接。
- Syntax:
```text
SendHeart()
```
- Input Parameters:
```text
无参数
```
- Returns:
```text
bool：连接是否存活
```

#### SetLanguage

- Interface Name: `SetLanguage`
- Description: 用于设置系统语言。
- Syntax:
```text
SetLanguage(language)
```
- Input Parameters:
```text
language - 要设置的目标语言
   数据类型： str
```
- Returns:
```text
bool：表示函数执行的成功或失败状态
```

#### SetLicensePath

- Interface Name: `SetLicensePath`
- Description: SetLicensePath(path) 用于设置许可证路径。多个路径之间以“ ; ”分割，许可证文件全路径中，不允许有 @ 符号，True表示应用成功。
- Syntax:
```text
SetLicensePath(path)
```
- Input Parameters:
```text
path - 指定的使用许可路径
   数据类型： str
```
- Returns:
```text
int：错误代码， 0 表示应用成功，其他错误代码按照 Sysplorer 软件补充完毕。
```

#### SetMainLogLevel

- Interface Name: `SetMainLogLevel`
- Description: 用于设置 Sysplorer 的日志级别。
- Syntax:
```text
SetMainLogLevel(level)
```
- Input Parameters:
```text
level - 日志级别
   数据类型： int
```
- Returns:
```text
bool：是否设置成功
```

#### SetMainLogWriteMode

- Interface Name: `SetMainLogWriteMode`
- Description: 用于设置 Sysplorer 日志的写入模式。
- Syntax:
```text
SetMainLogWriteMode(mode)
```
- Input Parameters:
```text
mode - 写入模式
   数据类型： int
```
- Returns:
```text
bool：是否设置成功
```

#### SetOption

- Interface Name: `SetOption`
- Description: 用于设置某个具体首选项的值，name 表示首选项的名称，value 表示目标选项的值，设置成功返回 True，失败返回 False。
- Syntax:
```text
SetOption(name,value)
```
- Input Parameters:
```text
name - 首选项的名称
   数据类型： str
  value - 目标选项的值
   数据类型： int  bool  str  list
```
- Returns:
```text
bool：表示函数执行成功或失败
```

#### SetPanelVisiable

- Interface Name: `SetPanelVisiable`
- Description: SetPanelVisiable(name, flag) 用于设定指定窗口显示还是隐藏。
- Syntax:
```text
SetPanelVisiable(name, flag)
```
- Input Parameters:
```text
name - 窗口英文名称
   数据类型：str
   支持的名称选项(name)
   窗口名                     格式    示例
   Library Browser         str   "Library Browser"
   User Models             str   "User Models"
   Component Browser       str   "Component Browser"
   Info Browser            str   "Info Browser"
   Code Browser            str   "Code Browser"
   Categorize Display      str   "Categorize Display"
   Data Dictionary         str   "Data Dictionary"
   Sysblock Model Finder   str   "Sysblock Model Finder"
   Break Points            str   "Break Points"
   Component Parameters    str   "Component Parameters"
   Component Variables     str   "Component Variables"
   Command Window          str   "Command Window"
   Output Window           str   "Output Window"
   CAD Browser             str   "CAD Browser"
   File Explorer           str   "File Explorer"
  flag - 显示或关闭
   数据类型：bool
```
- Returns:
```text
bool ：表示是否显示成功。
```

### ModelCheckingAndCompilation

#### CheckModel

- Interface Name: `CheckModel`
- Description: 用于检查模型。
- Syntax:
```text
CheckModel(modelName)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
```
- Returns:
```text
bool：检查模型是否成功
```

#### ExportFMU

- Interface Name: `ExportFMU`
- Description: 将模型导出为 FMU，指定 FMI 类型，选择 FMI 版本，手动选择 FMU 文件的保存路径，选择 FMU 文件的平台，选择积分算法，并选择积分步长，对于定步长算法设置固定积分步长，对于变步长算法设置初始积分步长。
- Syntax:
```text
ExportFMU(modelName)
ExportFMU(modelName, fmuType, fmuVersion, fmuPath, platform, algo, integralStep)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
  fmuType - FMI类型
   数据类型： str
  fmuVersion - FMI版本
   数据类型： str
  fmuPath - FMU文件保存路径
   数据类型： str
  platform - FMI平台
   数据类型： str
  algo - 积分算法
   可选积分算法如下：
积分算法名称                          缩写
Integration.Dassl               Dassl
Integration.Radau5              Radau5
Integration.Dop853              Dop853
Integration.Dopri5              Dopri5
Integration.Mebdf               Mebdf
Integration.Mebdfi              Mebdfi
Integration.Lsode               Lsode
Integration.Lsodar              Lsodar
Integration.Cvode               Cvode
Integration.Ida                 Ida
Integration.Sdirk34             Sdirk34
Integration.Esdirk23            Esdirk23
Integration.Esdirk34            Esdirk34
Integration.Esdirk45            Esdirk45
Integration.Euler               Euler
Integration.Rkfix2              Rkfix2
Integration.Rkfix3              Rkfix3
Integration.Rkfix4              Rkfix4
Integration.Rkfix6              Rkfix6
Integration.Rkfix8              Rkfix8
Integration.lmplicitEuler       lmplicitEuler
Integration.lmplicitTrapezoid   lmplicitTrapezoid
Integration.Custom              Custom
  integralStep - 积分步长
   数据类型： int  float
```
- Returns:
```text
bool：表示模型是否成功导出
```

#### ExportFMUEx

- Interface Name: `ExportFMUEx`
- Description: 将模型导出为 FMU，其余参数按默认值。相比 ExportFMU() 增加了可设置的选项。
- Syntax:
```text
ExportFMUEx(modelName, options)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
  options - 导出设置
   数据类型： str  bool  list  int  float
```
- Returns:
```text
bool：表示模型是否成功导出
```

#### ExportVeristand

- Interface Name: `ExportVeristand`
- Description: 用于把模型导出为 Veristand 模型，指定文件保存路径和名称。
- Syntax:
```text
ExportVeristand(modelName, headFile, veristandFile)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
  headFile - 头文件
   数据类型： str
  veristandFile - Veristand 模型文件
   数据类型： str
```
- Returns:
```text
bool：表示是否导出成功
```

#### GetCompileFmu64

- Interface Name: `GetCompileFmu64`
- Description: 用于获取 fmu 导出时编译器平台位数。
- Syntax:
```text
GetCompileFmu64()
```
- Input Parameters:
```text
无参数
```
- Returns:
```text
int：表示编译器平台的位数，32 位为 0，64 位为 1
```

#### GetCompileSolver64

- Interface Name: `GetCompileSolver64`
- Description: 用于获取翻译时编译器平台位数。
- Syntax:
```text
GetCompileSolver64()
```
- Input Parameters:
```text
无参数
```
- Returns:
```text
int：表示编译器平台的位数，32 位为 0，64 位为 1
```

#### ImportFMU

- Interface Name: `ImportFMU`
- Description: 用于导入 FMU 文件，fmuPath 为 FMU 文件的全路径，within 表示 FMU 模型要插入的父模型，modelName 表示导入的 FMU 模型名，默认为空，表示由系统设定。
- Syntax:
```text
ImportFMU(fmuPath)
ImportFMU(fmuPath, within)
ImportFMU(fmuPath, within, modelName)
```
- Input Parameters:
```text
fmuPath - FMU文件全路径
   数据类型： str
  within - 导入的 FMU 模型要插入的父模型
   数据类型： str
  modelName - 导入的 FMU 模型名
   数据类型： str
```
- Returns:
```text
bool：表示导入是否成功
```

#### SetCompileFmu64

- Interface Name: `SetCompileFmu64`
- Description: 用于设置 fmu 导出时编译器平台位数，i = 1 表示 64 位编译器，i = 0 表示 32 位编译器，i = 其他也表示 32 位编译器。
- Syntax:
```text
SetCompileFmu64(i)
```
- Input Parameters:
```text
i - 设置编译器平台位数
   数据类型： int
```
- Returns:
```text
bool：表示是否设置成功
```

#### SetCompileSolver64

- Interface Name: `SetCompileSolver64`
- Description: 用于设置翻译时编译器平台位数，i = 1 时表示 64 位平台，i = 0 时表示 32 位平台，i 为其他数值时也表示 32 位平台。
- Syntax:
```text
SetCompileSolver64(i)
```
- Input Parameters:
```text
i - 设置编译器平台位数
   数据类型： int
```
- Returns:
```text
bool：表示是否设置成功
```

#### TranslateModel

- Interface Name: `TranslateModel`
- Description: 用于翻译模型。
- Syntax:
```text
TranslateModel(modelName)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
```
- Returns:
```text
bool：翻译模型是否成功
```

### ModelEditorPy

#### AddComponent

- Interface Name: `AddComponent`
- Description: 用于在指定模型 modelName 下以指定的坐标位置和长宽大小添加 typeName 类型的组件。
- Syntax:
```text
AddComponent(typeName, modelName, name)
AddComponent(typeName, modelName, name, x, y, width, height)
```
- Input Parameters:
```text
typeName - 组件的类型
   数据类型： str
  modelName - 组件要插入的模型
   数据类型： str
  name - 组件名
   数据类型： str
  x - 组件位置的x坐标
   数据类型： float  int
  y - 组件位置的y坐标
   数据类型： float  int
  width - 组件位置的宽度
   数据类型： float  int
  height - 组件位置的高度
   数据类型： float  int
```
- Returns:
```text
bool：表示添加是否成功
```

#### AddFromComponent

- Interface Name: `AddFromComponent`
- Description: 用于以指定的位置和大小创建 FROM 组件。
- Syntax:
```text
AddFromComponent(gotoName, modelName, name)
AddFromComponent(gotoName, modelName, name, x, y, width, height)
```
- Input Parameters:
```text
gotoName - 要连接的 GOTO 组件名
   数据类型： str
  modelName - 要添加到的模型全名
   数据类型： str
  name - 生成的组件名，已有重名则报错
   数据类型： str
  x - 组件位置的 x 坐标，默认为 0
   数据类型： float  int
  y - 组件位置的 y 坐标，默认为 0
   数据类型： float  int
  width - 组件的宽度，为0时表示不显示图形
   数据类型： float  int
  height - 组件的高度，为0时表示不显示图形
   数据类型： float  int
```
- Returns:
```text
bool：表示创建是否成功
```

#### AddGotoComponent

- Interface Name: `AddGotoComponent`
- Description: 用于指定各个参数并创建 GOTO 组件。
- Syntax:
```text
AddGotoComponent(modelName, name, portType)
AddGotoComponent(modelName, name, portType, portDimension, x, y, width, height, tagVisibility)
```
- Input Parameters:
```text
modelName - 要添加到的模型全名
   数据类型： str
  name - 生成的组件名，已有重名则报错
   数据类型： str
  portType - 端口类型，目前仅支持Real、Boolean、Integer
   数据类型： str
  portDimension - 维度，使用一维数组表示，例如2, 3表示二维，的2  3 的矩阵
   数据类型： int
  x - 组件位置的 x 坐标，默认为 0
   数据类型： float  int
  y - 组件位置的 y 坐标，默认为 0
   数据类型： float  int
  width - 组件的宽度，为0时表示不显示图形
   数据类型： float  int
  height - 组件的高度，为0时表示不显示图形
   数据类型： float  int
  tagVisibility - 可见性，用于Sysblock，物理建模中默认为Local，如果不是需要报错
   数据类型： str
```
- Returns:
```text
bool：表示创建是否成功
```

#### ClassExist

- Interface Name: `ClassExist`
- Description: 用于判断给定的名字是否为已加载的类型，函数返回 bool 表示是否绘制成功。
- Syntax:
```text
ClassExist(className)
```
- Input Parameters:
```text
className - 类型全名
   数据类型： str
```
- Returns:
```text
bool：表示是否为已加载的类型
```

#### ClearShapes

- Interface Name: `ClearShapes`
- Description: 用于清空指定模型视图的所有图形，函数返回 bool 表示是否绘制成功。
- Syntax:
```text
ClearShapes(modelName, graphicsLayer)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
  graphicsLayer - 图形视图或图标视图，"diagram"、"icon"
   数据类型： str
```
- Returns:
```text
bool：表示清空是否成功
```

#### CompareModel

- Interface Name: `CompareModel`
- Description: 用于图形化模型对比。
- Syntax:
```text
CompareModel(firstModel, secondModel, isFile)
```
- Input Parameters:
```text
firstModel - 模型文件名或模型全名
   数据类型： str
  secondModel - 模型文件名或模型全名
   数据类型： str
  isFile - 对比模型文件还是已加载的模型全名
   数据类型： bool
```
- Returns:
```text
bool：表示是否导出成功
```

#### ConnectPort

- Interface Name: `ConnectPort`
- Description: 用于在指定模型下，连接指定两个端口。
- Syntax:
```text
ConnectPort(modelName, leftPort, rightPort)
ConnectPort(modelName, leftPort, rightPort, gripPoints, manhattanize, smooth)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
  leftPort - 连接左端口名字
   数据类型： str
  rightPort - 连接右端口名字
   数据类型： str
  gripPoints - 连接夹点链表
   数据类型： int  float
  manhattanize - 进行曼哈顿化处理
   数据类型： bool
  smooth - 显示为 Bezier 光顺曲线
   数据类型： bool
```
- Returns:
```text
bool：表示是否连接成功
```

#### CopyComponent

- Interface Name: `CopyComponent`
- Description: 用于从目标模型中选择组件名称并复制到源模型中，并重新设置组件名称。
- Syntax:
```text
CopyComponent(srcModelName, tarModelName, name)
CopyComponent(srcModelName, tarModelName, name, tarName)
```
- Input Parameters:
```text
srcModelName - 源模型全名
   数据类型： str
  tarModelName - 目标模型全名。若两个模型名相同，则在当前模型下复制
   数据类型： str
  name - 生成的组件名，已有重名则报错
   数据类型： str
  tarName - 目标组件名，默认为空 ，表示使用相同的组件名
   数据类型： str
```
- Returns:
```text
bool：表示复制是否成功
```

#### CopyModel

- Interface Name: `CopyModel`
- Description: 用于复制模型，srcParentModel 表示源父模型全名，若为顶层模型，此项为空，modelName 表示模型简名，tarParentModel 表示目标父模型全名，默认为空，表示复制到顶层，newModelName 表示新模型简名，默认为空，表示与原模型一致。
- Syntax:
```text
CopyModel(srcParentModel, modelName, tarParentModel, newModelName)
```
- Input Parameters:
```text
srcParentModel - 源父模型全名，若为顶层模型，此项为空
   数据类型： str
  modelName - 模型简名
   数据类型： str
  tarParentModel - 目标父模型全名，默认为空，表示复制到顶层
   数据类型： str
  newModelName - 新模型简名，默认为空，表示与原模型一致
   数据类型： str
```
- Returns:
```text
bool：表示是否复制成功
```

#### DrawBitmap

- Interface Name: `DrawBitmap`
- Description: 用于在指定模型视图绘制位图，并指定图形样式。
- Syntax:
```text
DrawBitmap(modelName, graphicsLayer, x, y, path, saveToModel, width, height)
DrawBitmap(modelName, graphicsLayer, x, y, path, saveToModel, width, height, style)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
  graphicsLayer - 图形视图或图标视图，"diagram"、"icon"
   数据类型： str
  x - 中心横坐标
   数据类型： float
  y - 中心纵坐标
   数据类型： float
  path - 图片的路径
   数据类型： str
  saveToModel - 图片数据是否保存到模型
   数据类型： bool
  width - 宽
   数据类型： float
  height - 高
   数据类型： float
  style - 图形样式
   数据类型： MwShapeStyle
```
- Returns:
```text
bool：表示绘制是否成功
```

#### DrawEllipse

- Interface Name: `DrawEllipse`
- Description: 用于在指定模型视图绘制椭圆，并指定图形样式。
- Syntax:
```text
DrawEllipse(modelName, graphicsLayer, x, y, width, height)
DrawEllipse(modelName, graphicsLayer, x, y, width, height, style)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
  graphicsLayer - 图形视图或图标视图，"diagram"、"icon"
   数据类型： str
  x - 中心横坐标
   数据类型： float
  y - 中心纵坐标
   数据类型： float
  width - 宽
   数据类型： float
  height - 高
   数据类型： float
  style - 图形样式
   数据类型： MwShapeStyle
```
- Returns:
```text
bool：表示绘制是否成功
```

#### DrawLine

- Interface Name: `DrawLine`
- Description: 用于在指定模型视图绘制线段，并指定图形样式。
- Syntax:
```text
DrawLine(modelName, graphicsLayer, leftEnd, rightEnd)
DrawLine(modelName, graphicsLayer, leftEnd, rightEnd, style)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
  graphicsLayer - 图形视图或图标视图，"diagram"、"icon"
   数据类型： str
  leftEnd - 左端点
   数据类型： int  float
  rightEnd - 右端点
   数据类型： int  float
  style - 图形样式
   数据类型： MwShapeStyle
```
- Returns:
```text
bool：表示绘制是否成功
```

#### DrawLines

- Interface Name: `DrawLines`
- Description: 用于在指定模型视图绘制多段线，并指定图形样式。
- Syntax:
```text
DrawLines(modelName, graphicsLayer, gripPoints)
DrawLines(modelName, graphicsLayer, gripPoints, style)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
  graphicsLayer - 图形视图或图标视图，"diagram"、"icon"
   数据类型： str
  gripPoints - 夹点列表，格式为 x0,y0,x1,y1,...,xn,yn，两两组合构成坐标，至少为 4
   数据类型： int  float
  style - 图形样式
   数据类型： MwShapeStyle
```
- Returns:
```text
bool：表示绘制是否成功
```

#### DrawPolygon

- Interface Name: `DrawPolygon`
- Description: 用于在指定模型视图绘制多边形，并指定图形样式。
- Syntax:
```text
DrawPolygon(modelName, graphicsLayer, vertex)
DrawPolygon(modelName, graphicsLayer, vertex, style)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
  graphicsLayer - 图形视图或图标视图，"diagram"、"icon"
   数据类型： str
  vertex - 顶点列表，格式为 x0,y0,x1,y1,...,xn,yn，两两组合构成坐标，至少为 6
   数据类型： int  float
  style - 图形样式
   数据类型： MwShapeStyle
```
- Returns:
```text
bool：表示绘制是否成功
```

#### DrawRectangle

- Interface Name: `DrawRectangle`
- Description: 用于在指定模型视图绘制矩形，并指定图形样式。
- Syntax:
```text
DrawRectangle(modelName, graphicsLayer, x, y, width, height)
DrawRectangle(modelName, graphicsLayer, x, y, width, height, style)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
  graphicsLayer - 图形视图或图标视图，"diagram"、"icon"
   数据类型： str
  x - 中心横坐标
   数据类型： float
  y - 中心纵坐标
   数据类型： float
  width - 宽
   数据类型： float
  height - 高
   数据类型： float
  style - 图形样式
   数据类型： MwShapeStyle
```
- Returns:
```text
bool：表示绘制是否成功
```

#### DrawShape

- Interface Name: `DrawShape`
- Description: 用于在指定模型视图绘制图元，并指定图形选项和图形样式。
- Syntax:
```text
DrawShape(modelName, shapeType, graphicsLayer)
DrawShape(modelName, shapeType, graphicsLayer, options, style)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
  shapeType - 形状类型，包括 "Line","Lines","Polygon","Triangle","Rectangle","Ellipse","Text","Bitmap"
   数据类型： str
  graphicsLayer - 图形视图或图标视图，"diagram"、"icon"
   数据类型： str
  options - 图形选项，根据不同的形状类型，输入不同的字典
   数据类型： Any
  style - 图形样式
   数据类型： MwShapeStyle
```
- Returns:
```text
bool：表示绘制是否成功
```

#### DrawText

- Interface Name: `DrawText`
- Description: 用于在指定模型视图绘制文本，并指定图形样式。
- Syntax:
```text
DrawText(modelName, graphicsLayer, x, y, text)
DrawText(modelName, graphicsLayer, x, y, text, width, height, style)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
  graphicsLayer - 图形视图或图标视图，"diagram"、"icon"
   数据类型： str
  x - 中心横坐标
   数据类型： float
  y - 中心纵坐标
   数据类型： float
  text - 文本
   数据类型： str
  width - 宽
   数据类型： float
  height - 高
   数据类型： float
  style - 图形样式
   数据类型： MwShapeStyle
```
- Returns:
```text
bool：表示绘制是否成功
```

#### DrawTriangle

- Interface Name: `DrawTriangle`
- Description: 用于在指定模型视图绘制三角形，并指定图形样式。
- Syntax:
```text
DrawTriangle(modelName, graphicsLayer, vertex1, vertex2, vertex3)
DrawTriangle(modelName, graphicsLayer, vertex1, vertex2, vertex3, style)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
  graphicsLayer - 图形视图或图标视图，"diagram"、"icon"
   数据类型： str
  vertex1 - 顶点1
   数据类型： int  float
  vertex2 - 顶点2
   数据类型： int  float
  vertex3 - 顶点3
   数据类型： int  float
  style - 图形样式
   数据类型： MwShapeStyle
```
- Returns:
```text
bool：表示绘制是否成功
```

#### EditModelText

- Interface Name: `EditModelText`
- Description: 用于编辑模型的 Modelica 文本内容，只能编辑整行，将从第 beginLine 末尾到第 endLine 行末尾的文本替换为 modelText 的内容。
- Syntax:
```text
EditModelText(modelName, modelText, beginLine, endLine)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
  modelText - Modelica 文本
   数据类型： str
  beginLine - 起始行号
   数据类型： int
  endLine - 终止行号
   数据类型： int
```
- Returns:
```text
bool：表示是否成功编辑
```

#### EncryptClass

- Interface Name: `EncryptClass`
- Description: 使用加密登记 modelEncryptLevel，许可证 modelLicenseFeature 发布模型，dependsResourcePaths 为资源文件路径（当发布的模型为单模型时生效），copyResourceInLibrary 为选择是否拷贝模型库资源（当发布的模型为非单模型时生效）。
- Syntax:
```text
EncryptClass(className, publishPath, modelEncryptLevel,modelLicenseFeature,dependsResourcePaths,copyResourceInLibrary)
```
- Input Parameters:
```text
className - 模型名
   数据类型： str
  publishPath - 发布路径
   数据类型： str
  modelEncryptLevel - 模型加密等级
   数据类型： str
  modelLicenseFeature - 模型加密特征
   数据类型： str
  dependsResourcePaths - 附加资源路径（当发布的模型为单模型时生效）
   数据类型： str
  copyResourceInLibrary - 是否拷贝资源（当发布的模型为非单模型时生效）
   数据类型： bool
```
- Returns:
```text
bool：发布是否成功
```

#### EraseClasses

- Interface Name: `EraseClasses`
- Description: 用于删除子模型或卸载顶层模型。
- Syntax:
```text
EraseClasses(classList)
```
- Input Parameters:
```text
classList - 模型名列表
   数据类型： str
```
- Returns:
```text
bool：表示是否删除成功
```

#### ExportDiagram

- Interface Name: `ExportDiagram`
- Description: 用于把模型名为 modelName 的模型图形视图导出到 path 路径下，图片长宽根据 width 和 height 指定。
- Syntax:
```text
ExportDiagram(modelName, path, width, height)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
  path - 图片文件路径
   数据类型： str
  width - 图片宽度，默认为包围盒的大小（400）
   数据类型： int  float
  height - 图片高度，默认为包围盒的大小（400）
   数据类型： int  float
```
- Returns:
```text
bool：表示图片是否成功保存
```

#### ExportDocumentation

- Interface Name: `ExportDocumentation`
- Description: 用于把模型文档信息导出到文件中，指定文件保存路径和名称。
- Syntax:
```text
ExportDocumentation(modelName, docFile)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
  docFile - 文档文件名
   数据类型： str
```
- Returns:
```text
bool：表示文档是否成功保存
```

#### ExportIcon

- Interface Name: `ExportIcon`
- Description: 用于把模型名为 modelName 的模型图标视图导出到 path 路径下，图片长宽根据 width 和 height 指定。
- Syntax:
```text
ExportIcon(modelName, path, width, height)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
  path - 图片文件路径
   数据类型： str
  width - 图片宽度，默认为包围盒的大小（400）
   数据类型： int  float
  height - 图片高度，默认为包围盒的大小（400）
   数据类型： int  float
```
- Returns:
```text
bool：表示图片是否成功保存
```

#### GetClasses

- Interface Name: `GetClasses`
- Description: 用于获取指定模型的嵌套类型。当给定空字符串时，则获取模型浏览器上所有顶层模型列表。
- Syntax:
```text
GetClasses(modelName)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
```
- Returns:
```text
list：模型的嵌套类型构成的列表
```

#### GetComponentDescription

- Interface Name: `GetComponentDescription`
- Description: 用于获取指定模型 modelName 中组件 componentName 的描述文字。
- Syntax:
```text
GetComponentDescription(modelName, componentName)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
  componentName - 组件名
   数据类型： str
```
- Returns:
```text
str：指定模型中组件的描述文字
```

#### GetComponentInfo

- Interface Name: `GetComponentInfo`
- Description: 是通用的获取组件属性的接口。
- Syntax:
```text
GetComponentInfo(modelName, component, infoType)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
  component - 组件名
   数据类型： str
  infoType - 信息的字段类型
   数据类型： str
```
- Returns:
```text
str：返回的值
```

#### GetComponentPorts

- Interface Name: `GetComponentPorts`
- Description: 用于获取组件端口。如果不传组件名，获取顶层连接器。函数返回值 list 表示列表形式的组件端口。
- Syntax:
```text
GetComponentPorts(modelName, componentName, portDirection)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
  componentName - 组件名
   数据类型： str
  portDirection - 端口流向，0 表示所有，1 表示输入，2 表示输出，3 表示无方向性的
   数据类型： int
```
- Returns:
```text
list：列表形式的组件端口
```

#### GetComponentTypeName

- Interface Name: `GetComponentTypeName`
- Description: 用于获取指定模型中组件的类型名字 ，模型返回 str 表示组件的类型名字。
- Syntax:
```text
GetComponentTypeName(modelName, componentName, fullName)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
  componentName - 组件名
   数据类型： str
  fullName - 是否返回类型全名
   数据类型： bool
```
- Returns:
```text
str：组件的类型名字
```

#### GetComponents

- Interface Name: `GetComponents`
- Description: 用于获取指定模型 modelName 的嵌套组件。
- Syntax:
```text
GetComponents(modelName)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
```
- Returns:
```text
list：模型的嵌套组件构成的列表
```

#### GetConnectionInfo

- Interface Name: `GetConnectionInfo`
- Description: 用于获取连接线信息通用的获取连线属性的接口。
- Syntax:
```text
GetConnectionInfo(modelName, connection, infoType)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
  connection - 连接，使用左右端口名表示
   数据类型： str
  infoType - 信息的字段类型
   数据类型： str
```
- Returns:
```text
str：返回的值
```

#### GetModelDescription

- Interface Name: `GetModelDescription`
- Description: 用于获取指定模型的描述文字。
- Syntax:
```text
GetModelDescription(modelName)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
```
- Returns:
```text
str：指定模型的描述文字
```

#### GetModelExperiment

- Interface Name: `GetModelExperiment`
- Description: 用于获取模型仿真配置。
- Syntax:
```text
GetModelExperiment(modelName)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
```
- Returns:
```text
dict：字典格式的仿真设置
  startTime，stopTime：仿真开始和结束时间
   数据类型：float
  numberOfIntervals：仿真输出步数
   数据类型：int
  isIntervalLength：是否使用输出步长
   数据类型：bool
  algorithm：算法名
   数据类型：string
  isPieceWiseStep：是否保存时刻点
   数据类型：bool
  pieceWiseStep：设置某段时间节点采用的积分步长，pieceWiseStep = ((0, xxx), (m, xxx), (n, xxx), ...), pieceWiseStep 以二维数组表示，第一个数为时间节点，"xxx" 为从当前时间节点开始的步长。
   数据类型：list
  fixedOrInitStepSize：固定或初始化积分步长，当算法为定步长算法、离散积分算法时表示固定积分步长，为变步长算法时表示初始积分步长
   数据类型：float
  tolerance：精度
   数据类型：float
  inlineIntegrator：是否使用内联积分器
   数据类型：bool
  storeEvent：是否存储事件时刻的变量值
   数据类型：bool
```

#### GetModelInfo

- Interface Name: `GetModelInfo`
- Description: 是通用的获取模型信息的接口。
- Syntax:
```text
GetModelInfo(modelName, infoType)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
  infoType - 信息的字段类型，例如前缀、组件列表、子模型列表、描述等等，所有模型信息均可通过这个接口获取。包含以下字段：
    Specialization（限定类型）
    Description（描述）
    NestClasses（子类）
    Text（全文本）
    Prefixes（前缀列表）
    Experiment（试验属性）
    Imports（引用类型列表）
    Extends（基类列表）
    Equations（方程列表）
    Algorithm（算法文本）
    Connections（连线列表）
    Components（组件列表，含基本类型变量）
     数据类型： str
```
- Returns:
```text
str：返回的值
```

#### GetModelParamList

- Interface Name: `GetModelParamList`
- Description: 用于获取模型中某个组件的参数列表，函数返回一个列表形式的参数名。
- Syntax:
```text
GetModelParamList(modelName, component)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
  component - 组件名
   数据类型： str
```
- Returns:
```text
list：列表形式的组件参数名
```

#### GetModelParamValue

- Interface Name: `GetModelParamValue`
- Description: 用于获取参数值。返回值是参数变型表达式的字符串表示，而非估算后的数值。支持 Sysblock，每个 Sysblock 可以返回的参数，通过 Sysblock 的模块帮助，获取失败返回 None。
- Syntax:
```text
GetModelParamValue(modelName, component, paramName)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
  component - 组件名
   数据类型： str
  paramName - 参数名
   数据类型： str
```
- Returns:
```text
str：参数变型表达式的字符串表示
```

#### GetModelText

- Interface Name: `GetModelText`
- Description: 用于获取模型文本。函数返回值为模型文本内容。
- Syntax:
```text
GetModelText(modelName)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
```
- Returns:
```text
str：模型文本内容
```

#### GetParamList

- Interface Name: `GetParamList`
- Description: 用于获取指定组件前缀层次中的参数列表。返回值列表中的元素为：的键-值对。preName 若为空，表示获取模型顶层参数。
- Syntax:
```text
GetParamList(preName)
```
- Input Parameters:
```text
preName - 组件前缀名
   数据类型： str
```
- Returns:
```text
list：指定组件前缀层次中的参数列表
```

#### GetParamValue

- Interface Name: `GetParamValue`
- Description: 用于获取参数值。返回值是参数变型表达式的字符串表示，而非估算后的数值。
- Syntax:
```text
GetParamValue(paramName)
```
- Input Parameters:
```text
paramName - 参数全名
   数据类型： str
```
- Returns:
```text
str：参数变型表达式的字符串表示
```

#### GetRestriction

- Interface Name: `GetRestriction`
- Description: 用于获取给定类型的限定类型 ， 返回 class 、 record 、 type 、 model 、 block 、 function 、 connector 、 package 、 operator 、 operator record 或 operator function，函数返回 str 表示给定类型的限定类型。
- Syntax:
```text
GetRestriction(className)
```
- Input Parameters:
```text
className - 类型全名
   数据类型： str
```
- Returns:
```text
str：给定类型的限定类型
```

#### LoadLibrary

- Interface Name: `LoadLibrary`
- Description: 用于加载指定模型库 libraryName 的指定 libraryVersion 版本。
- Syntax:
```text
LoadLibrary(libraryName)
LoadLibrary(libraryName, libraryVersion = "")
```
- Input Parameters:
```text
libraryName - 模型库名
   数据类型： str
  libraryVersion - 模型库版本
   数据类型： str  None
```
- Returns:
```text
bool：表示模型库是否成功加载
```

#### MessageText

- Interface Name: `MessageText`
- Description: MessageText() 用于获取上一条命令的日志信息。
- Syntax:
```text
MessageText()
```
- Input Parameters:
```text
无
```
- Returns:
```text
返回上一条命令的日志信息。
```

#### NewModel

- Interface Name: `NewModel`
- Description: 用于新建模型，函数返回 str 表示新建的模型名。modelName 为新建模型的全名，restriction 为新建模型的限定类型，description 为新建模型的描述，base 为基类全名，parent 为插入的父模型全名，saveInOneFile 为保存为单个文件，partial 为是否为抽象类。
- Syntax:
```text
NewModel(modelName, restriction, description, base, parent, saveInOneFile, partial)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
  restriction - 模型的限定类型
   数据类型： str
  description - 模型描述
   数据类型： str
  base - 基类全名
   数据类型： str
  parent - 插入的父模型全名
   数据类型： str
  saveInOneFile - 保存为单个文件
   数据类型： bool
  partial - 是否为抽象类
   数据类型： bool
```
- Returns:
```text
str：返回新建的模型名
```

#### OpenModel

- Interface Name: `OpenModel`
- Description: 用于打开模型窗口，viewType 指定打开视图类别。
- Syntax:
```text
OpenModel(modelName)
OpenModel(modelName, viewType)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
  viewType - 视图类别
视图类别      描述
icon      图标视图
diagram   图形视图
text      文本视图
info      文档视图
```
- Returns:
```text
bool：表示模型窗口是否成功打开
```

#### OpenModelFile

- Interface Name: `OpenModelFile`
- Description: 加载指定的 Modelica 模型文件，支持 .mol 和 .mo 文件，并指定加载重复模型时，是否自动重新加载模型。 默认情况下，不指定 autoReload 加载重复模型时，会自动重新加载模型。
- Syntax:
```text
OpenModelFile(path)
OpenModelFile(path, autoReload)
```
- Input Parameters:
```text
path - Modelica模型文件的全路径
   数据类型： str
  autoReload - 已经加载是否自动重新加载
   数据类型： bool
```
- Returns:
```text
bool：表示模型是否成功打开
```

#### RemoveComponent

- Interface Name: `RemoveComponent`
- Description: 用于移除组件，并指定是否移除链接。
- Syntax:
```text
RemoveComponent(modelName, name)
RemoveComponent(modelName, name, withConnect)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
  name - 组件名
   数据类型： str
  withConnect - 同时删除组件的连线，默认为True
   数据类型： bool
```
- Returns:
```text
bool：表示删除是否成功
```

#### RemoveConnect

- Interface Name: `RemoveConnect`
- Description: 用于移除连接，模型返回 bool 表示是否设置成功。
- Syntax:
```text
RemoveConnect(modelName, leftPort, rightPort)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
  leftPort - 连接左端口名字
   数据类型： str
  rightPort - 连接右端口名字
   数据类型： str
```
- Returns:
```text
bool：表示删除是否成功
```

#### RenameModel

- Interface Name: `RenameModel`
- Description: 用于重命名模型，函数返回值 bool 表示是否改名成功。
- Syntax:
```text
RenameModel(srcModelName, newModelName, parentModel)
```
- Input Parameters:
```text
srcModelName - 原模型简名
   数据类型： str
  newModelName - 新模型简名
   数据类型： str
  parentModel - 父模型全名，缺省为空，表示顶层模型改名
   数据类型： str
```
- Returns:
```text
bool：表示是否改名成功
```

#### SaveAllModels

- Interface Name: `SaveAllModels`
- Description: 用于保存所有模型。
- Syntax:
```text
SaveAllModels()
```
- Input Parameters:
```text
无参数
```
- Returns:
```text
bool：表示是否保存成功
```

#### SaveModel

- Interface Name: `SaveModel`
- Description: 用于保存指定模型。
- Syntax:
```text
SaveModel(modelName)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
```
- Returns:
```text
bool：表示是否保存成功
```

#### SaveModelAs

- Interface Name: `SaveModelAs`
- Description: 用于另存指定模型。
- Syntax:
```text
SaveModelAs(modelName, path, newModelName)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
  path - 保存路径
   数据类型： str
  newModelName - 新的模型简名，默认为空，表示与原模型一致
   数据类型： str
```
- Returns:
```text
bool：表示是否保存成功
```

#### SetComponentDescription

- Interface Name: `SetComponentDescription`
- Description: 用于设置指定模型中组件的描述文字，注意，对于模型库或加密模型该命令不可用。
- Syntax:
```text
SetComponentDescription(modelName, componentName, description)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
  componentName - 组件名
   数据类型： str
  description - 描述文字
   数据类型： str
```
- Returns:
```text
bool：表示是否设置成功
```

#### SetComponentInfo

- Interface Name: `SetComponentInfo`
- Description: 是通用的设置模型属性的接口。
- Syntax:
```text
SetComponentInfo(modelName, component, infoType, value)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
  component - 组件名
   数据类型： str
  infoType - 信息的字段类型
   数据类型： str
  value - 值
   数据类型： str
```
- Returns:
```text
bool：是否设置成功。设置失败返回false。部分属性无法设置的，也返回false
```

#### SetConnectionInfo

- Interface Name: `SetConnectionInfo`
- Description: 用于设置连线属性的接口。
- Syntax:
```text
SetConnectionInfo(modelName, connection, infoType, value)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
  connection - 连接，使用左右端口名表示
   数据类型： str
  infoType - 信息的字段类型
   数据类型： str
  value - 值
   数据类型： str
```
- Returns:
```text
bool：表示是否设置成功
```

#### SetModelDescription

- Interface Name: `SetModelDescription`
- Description: 用于设置指定模型 modelName 的描述文字，替换原来的描述。注意，对于模型库或加密模型该命令不可用。
- Syntax:
```text
SetModelDescription(modelName, description)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
  description - 描述文字
   数据类型： str
```
- Returns:
```text
bool：表示是否成功设置
```

#### SetModelExperiment

- Interface Name: `SetModelExperiment`
- Description: 用于设置某个模型的仿真配置。函数返回 bool 表示是否设置成功。
- Syntax:
```text
SetModelExperiment(modelName, experiment)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
  experiment - 以字典格式输入的仿真配置
   数据类型： int  float  str  list
```
- Returns:
```text
bool：表示是否成功配置设置
```

#### SetModelInfo

- Interface Name: `SetModelInfo`
- Description: 是通用的设置模型信息的接口。
- Syntax:
```text
SetModelInfo(modelName, infoType, value)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
  infoType - 信息的字段类型
   数据类型： str
  value - 值
   数据类型： str
```
- Returns:
```text
bool：是否设置成功。设置失败返回 false。部分属性无法设置的，如 components，也返回 false。
```

#### SetModelParamValue

- Interface Name: `SetModelParamValue`
- Description: 用于设置指定模型指定参数的值，支持设置内置类型属性。支持 Sysblock。
- Syntax:
```text
SetModelParamValue(modelName, component, paramName, value)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
  component - 组件名
   数据类型： str
  paramName - 参数名
   数据类型： str
  value - 参数值
   数据类型： str
```
- Returns:
```text
bool：表示修改是否成功
```

#### SetModelText

- Interface Name: `SetModelText`
- Description: 用于修改模型的 Modelica 文本内容。
- Syntax:
```text
SetModelText(modelName, modelText)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
  modelText - Modelica 文本
   数据类型： str
```
- Returns:
```text
bool：表示是否成功设置
```

#### SetParamValue

- Interface Name: `SetParamValue`
- Description: 用于设置当前模型指定参数的值，支持设置内置类型属性。
- Syntax:
```text
SetParamValue(paramName, value)
```
- Input Parameters:
```text
paramName - 参数全名
   数据类型： str
  value - 参数值
   数据类型： str
```
- Returns:
```text
bool：表示是否设置成功
```

#### SetParamValues

- Interface Name: `SetParamValues`
- Description: SetParamValues(paramValues) 用于批量设置当前模型指定参数的值，支持设置内置类型属性。
- Syntax:
```text
SetParamValues(paramValues)
```
- Input Parameters:
```text
paramValues - 参数全名与值的键值对
   数据类型： int  float  str  list
```
- Returns:
```text
bool：表示是否设置成功
```

### ModelSimulation

#### AnimationSpeed

- Interface Name: `AnimationSpeed`
- Description: 用于设置动画播放速度。speed 为加速因子，大于 1 表示加速，小于 1 表示减速，在播放的过程中设置为 0 则停止播放。
- Syntax:
```text
AnimationSpeed(speed)
```
- Input Parameters:
```text
speed - 加速因子
   数据类型： int  float
```
- Returns:
```text
bool：表示操作是否成功
```

#### ClearPlot

- Interface Name: `ClearPlot`
- Description: 用于清除曲线窗中当前子窗口内容。如果 remove 为 True，则移除当前子窗口。最后一个子窗口不会被移除。
- Syntax:
```text
ClearPlot(remove, id)
```
- Input Parameters:
```text
remove - 是否移除子窗口
   数据类型： bool
  id - 窗口编号
   数据类型： int
```
- Returns:
```text
bool：表示是否清除成功
```

#### CloseHandleVarsCBFunction

- Interface Name: `CloseHandleVarsCBFunction`
- Description: 关闭实时获取仿真结果回调函数的调用，仿真停止后调用
- Syntax:
```text
N/A
```
- Input Parameters:
```text
N/A
```
- Returns:
```text
N/A
```

#### CreateAnimation

- Interface Name: `CreateAnimation`
- Description: 用于新建动画窗口。
- Syntax:
```text
CreateAnimation()
```
- Input Parameters:
```text
无参数
```
- Returns:
```text
bool：True表示操作成功，False表示失败
```

#### CreateLayout

- Interface Name: `CreateLayout`
- Description: CreateLayout() 用于创建界面窗口布局。
- Syntax:
```text
CreateLayout(row,column)
CreateLayout(row,column,widths,heights)
CreateLayout(row,column,widths,heights,window)
```
- Input Parameters:
```text
row - 布局行数
   数据类型： int
  column - 布局列数
   数据类型： int
  widths - 每个格子宽度大小
   数据类型： int  float
  heights - 每个格子高度大小
   数据类型： int  float
  window - 布局的窗口，默认为后处理窗口
   数据类型： str
```
- Returns:
```text
bool：表示是否成功创建布局
```

#### CreateLayoutEx

- Interface Name: `CreateLayoutEx`
- Description: CreateLayoutEx() 用于创建界面窗口布局。
- Syntax:
```text
CreateLayoutEx(position)
CreateLayoutEx(position, columnSize, rowSize)
```
- Input Parameters:
```text
position - 窗口位置
   用一个 int 数组来表示窗口的位置，每四位数字为一组分别表示一个窗口的位置： x0 表示窗口占用的布局器范围的最左边区域的 index 值（左上角第一格为 1, 1）
   y0 表示窗口占用的布局器范围的最上边区域的 index 值（左上角第一格为 1, 1）
   x1 表示窗口占用的布局器范围的最右边区域的 index 值（左上角第一格为 1, 1）
   y1 表示窗口占用的布局器范围的最下边区域的 index 值（左上角第一格为 1, 1）
   数据类型： int
  columnSize - 列宽
   分别对应每一列的宽度 数据类型： int  float
  rowSize - 行宽
   分别对应每一行的宽度 数据类型： int  float
```
- Returns:
```text
bool：表示是否成功创建布局
```

#### CreatePlot

- Interface Name: `CreatePlot`
- Description: 用于新建曲线窗口。当 x 使用默认参数时，创建 y(time) 窗口。当 x 被设置时，检查 x 与所有 y 是否都来自同一个实例，来自同一个实例则创建 y(x) 窗口，否则创建失败。如果 id 和 sub_plot 所唯一指定的子窗口已存在，则清空子窗口中已有变量。
- Syntax:
```text
CreatePlot()
CreatePlot(id, position, x, y, heading, grid, legendLayout, legendFrame, legend, xDisplayUnit, yDisplayUnit, yAxis, leftTitleType, leftTitle, bottomTitleType, bottomTitle, rightTitleType, rightTitle, curveVernier, fixTimeRange, fixTimeRangeValue, resultFile, subPlot)
```
- Input Parameters:
```text
id - 窗口编号
   id = 0，表示新建曲线窗口；id > 0，表示创建编号 id 的曲线，若指定 id 的窗口已存在且窗口类型一致，直接覆盖创建，否则新建窗口。
   数据类型： int
  position - 窗口位置（最新曲线窗口暂不支持设置该参数，保留参数为了兼容旧版调用）
   数组变量依次为 x0, y0, width, height；以左上角坐标为位置坐标，宽和高表示窗口大小。电脑屏幕的最左上角为原点即坐标为 0,0，屏幕上边界向右为 x 轴正方向，屏幕左边 y 轴正方向。
   数据类型： int  float
  x - 自变量
   默认是time。
   数据类型： str
  y - 变量列表
   数据类型： str
  heading - 标题
   数据类型： str
  grid - 显示网格
   数据类型： bool
  legendLayout - 图例位置
   1-嵌入上方，2-嵌入下方，3-嵌入左方，4-嵌入右方，5-浮动于左上，6-浮动于正上方，7-浮动于右上，8-浮动于左边中央，9-浮动于右边中央，10-浮动于左下，11-浮动于正下方，12-浮动于右下，13-隐藏，默认 6
   数据类型： int
  legendFrame - 是否绘制图例边框
   数据类型： bool
  legend - 图例列表
   数据类型： str
  xDisplayUnit - x轴显示单位
   数据类型： str
  yDisplayUnit - 变量的显示单位
   数据类型： str
  yAxis - 该曲线属于左/右坐标轴1左，-1右
   数据类型： int
  leftTitleType - 左纵坐标标题类型
   可选变量如下：
    AxisTitleType.None_ 无轴标题
    AxisTitleType.Default 使用默认的轴标题
    AxisTitleType.Custom 自定义的轴标题
   数据类型： int
  leftTitle - 自定义的左纵坐标标题
   数据类型： str
  bottomTitleType - 横坐标标题类型
   可选变量如下：
    AxisTitleType.None_ 无轴标题
    AxisTitleType.Default 使用默认的轴标题
    AxisTitleType.Custom 自定义的轴标题
   数据类型： int
  bottomTitle - 自定义的横坐标标题
   数据类型： str
  rightTitleType - 右纵坐标标题类型
   可选变量如下：
    AxisTitleType.None_ 无轴标题
    AxisTitleType.Default 使用默认的轴标题
    AxisTitleType.Custom 自定义的轴标题
   数据类型： int
  rightTitle - 自定义的右纵坐标标题
   数据类型： str
  curveVernier - 显示曲线游标
   数据类型： bool
  fixTimeRange - 限定时间范围
   数据类型： bool
  fixTimeRangeValue - 限定的时间范围值
   数据类型： int  float
  resultFile - 结果文件，需填写结果文件的全路径
   数据类型： str
  zoomX - x坐标轴的刻度范围
   数据类型： int  float
  zoomY - y左坐标轴的刻度范围
   数据类型： int  float
  subPlot - 子窗口序号
   数据类型： int
  zoomYR - y右坐标轴的刻度范围
   数据类型： int  float
```
- Returns:
```text
bool：表示是否成功新建窗口
```

#### CreatePlotEx

- Interface Name: `CreatePlotEx`
- Description: CreatePlotEx(data) 基于 data 这个二维向量中第一个向量的数据作为 x 轴，绘制第二个向量之后的数据。
CreatePlotEx(data, variables, position) 在 position 位置绘制 data。
CreatePlotEx(data, variables, position, option) 使用 option 配置，在 position 位置绘制 data。
CreatePlotEx(variables=variables) 基于当前结果的 variables 变量绘制数据，其横坐标为当前结果的时间。
CreatePlotEx(variables=variables, position=position) 在 position 位置绘制当前结果中的 variables 变量。
CreatePlotEx(variables=variables, position=position, option=option) 使用 option 中的绘图属性配置绘制当前结果中的 variables 变量。
若 data 和 variables 均不为空时，以 data 为准。
- Syntax:
```text
CreatePlotEx(data)
CreatePlotEx(data,variables
CreatePlotEx(data,variables,position)
CreatePlotEx(data,variables,position,option)
```
- Input Parameters:
```text
data - 绘图数据
   数据类型 list (2d)，每个元素是一个向量，对应变量的值。
   数据类型： list
  variables - 变量名列表
   变量名列表，当 data 有数据时视为每组数据的变量名。
   数据类型： str
  position - 窗口位置，需要先使用 CreateLayout 或 CreateLayoutEx 创建出对应的窗口布局
   用一个长度为 5 的 int 数组来表示窗口的类型和位置：
    第 1 位表示 type 窗口的布局，分为平铺和独立窗口，平铺模式为 1， 独立窗口为 2；
    第 2 位表示 x0 在平铺模式下，表示窗口占用的布局器范围的最左边区域的 index 值（左上角第一格为 1, 1）；在独立窗口模式下，表示窗口的左侧边的屏幕坐标（屏幕左上角为 0, 0）
    第 3 位表示 y0 在平铺模式下，表示窗口占用的布局器范围的最上边区域的 index 值（左上角第一格为 1, 1）；在独立窗口模式下，表示窗口的上侧边的屏幕坐标（屏幕左上角为 0, 0）
    第 4 位表示 x1 在平铺模式下，表示窗口占用的布局器范围的最右边区域的 index 值（左上角第一格为 1, 1）；在独立窗口模式下，表示窗口的右侧边的屏幕坐标（屏幕左上角为 0, 0）
    第 5 位表示 y1 在平铺模式下，表示窗口占用的布局器范围的最下边区域的 index 值（左上角第一格为 1, 1）；在独立窗口模式下，表示窗口的下侧边的屏幕坐标（屏幕左上角为 0, 0）
     数据类型： int
  option - 窗口设置
   用一组字典来表示窗口属性
    id int，窗口编号。id=0，表示新建窗口；id>0，表示创建编号 id 的窗口，若指定 id 的窗口已存在且窗口类型一致，直接覆盖，否则报错
    plotType str，窗口的类型，分为'Curve-yt'，'Curve-yx'，'Table'。分别表示 yt 曲线、yx 曲线、表格
    x 横坐标变量名字，仅在 'Curve-yx' 类型下生效，此时横坐标将不再使用输入数据的第一列
    heading str，窗口标题
    grid bool，是否显示网格
    legendLayout int，1 表示嵌入上方， 2 表示嵌入下方， 3 表示嵌入左方， 4 表示嵌入右方， 5 表示浮动于左上， 6 表示浮动于正上方， 7 表示浮动于右上， 8 表示浮动于左边中央， 9 表示浮动于右边中央， 10 表示浮动于左下， 11 表示浮动于正下方， 12 表示浮动于右下， 13 表示隐藏，默认 6
    legends list, 图例列表，与变量一一对应
    xDisplayUnit str, x 轴显示单位
    yDisplayUnit list, 变量显示单位，与变量一一对应
    yAxis list 该曲线属于左/右坐标轴，与变量一一对应, 1 表示左，-1 表示右
    leftTitleType int, 左纵坐标标题类型 可选变量如下：
      AxisTitleType.None_ 无轴标题
      AxisTitleType.Default 使用默认的轴标题
      AxisTitleType.Custom 自定义的轴标题
    leftTitle str，自定义的左纵坐标标题
    bottomTitleType int, 可选变量如下：横坐标标题类型
      AxisTitleType.None_ 无轴标题
      AxisTitleType.Default 使用默认的轴标题
      AxisTitleType.Custom 自定义的轴标题
    bottomTitle str，自定义的横坐标标题
    rightTitleType int，右纵坐标标题类型 可选变量如下：
      AxisTitleType.None_ 无轴标题
      AxisTitleType.Default 使用默认的轴标题
      AxisTitleType.Custom 自定义的轴标题
    rightTitle str, 自定义的右纵坐标标题
    curveVernier bool, 显示曲线游标
    fixTimeRange bool, 限定时间范围
    fixTimeRangeValue float, 限定的时间范围值
    resultFile str, 结果文件，需填写结果文件的全路径，该选项可以指定结果数据，而不只是当前结果
    subPlot list，子窗口序号，1,1 表示该窗口的第一行第一列的子窗口
     数据类型： list  bool  int  str  float  dict
```
- Returns:
```text
bool：表示是否成功新建窗口
```

#### ExportInitial

- Interface Name: `ExportInitial`
- Description: 用于导出初值文件，指定初值文件的路径为 initialFile，初值文件一般采用 txt 或 csv 格式。
- Syntax:
```text
ExportInitial(initialFile)
```
- Input Parameters:
```text
initialFile - 初值文件路径
   数据类型： str
```
- Returns:
```text
bool：表示是否导出成功。
```

#### ExportPlot

- Interface Name: `ExportPlot`
- Description: 用于指定窗口编号、图片宽度和图片高度将指定图形导出到指定文件中。
- Syntax:
```text
ExportPlot(filePath, fileFormat)
ExportPlot(filePath, fileFormat, id, w, h)
```
- Input Parameters:
```text
filePath - 存储路径
   数据类型： str
  fileFormat - 文件格式
   可选变量如下：
    PlotFileFormat.Image 曲线窗口导出为图片，命令中可缩写为 "1"；
    PlotFileFormat.Csv 曲线导出为 csv 文件，命令中可缩写为 "2"；
    PlotFileFormat.Mat 曲线导出为 mat 文件，命令中可缩写为 "3"；
    PlotFileFormat.Text 曲线导出为文本文件，命令中可缩写为 "4"。
   数据类型： int
  id - 窗口编号
   数据类型： int
  w - 图片宽度
   数据类型： int
  h - 图片高度
   数据类型： int
```
- Returns:
```text
bool：表示是否导出成功
```

#### ExportResult

- Interface Name: `ExportResult`
- Description: 用于导出结果文件，支持 csv、mat、msr 格式，并支持导出整个实例，结果文件的路径 path 是必须指定的，其余参数可按默认值。
- Syntax:
```text
ExportResult(path, formatType, vars, withUnit)
```
- Input Parameters:
```text
path - 结果文件的路径
   数据类型： str
  formatType - 文件格式
   可选变量如下：
    ResultFormat.Csv csv文件格式，命令中可缩写为"csv"；
    ResultFormat.Mat mat文件格式，命令中可缩写为"mat"；
    ResultFormat.Default msr结果文件格式，命令中可缩写为"msr"。
   数据类型： str
  vars - 变量名
   数据类型： str
  withUnit - 变量名后是否跟随单位
   数据类型： bool
```
- Returns:
```text
bool：表示是否导出成功
```

#### ExportResultEx

- Interface Name: `ExportResultEx`
- Description: ExportResultEx() 用于按默认配置导出全部结果文件。
  ExportResultEx(variables) 用于按默认配置导出指定的变量列表。
  ExportResultEx(option) 用于按给定配置导出全部结果文件。
  ExportResultEx(variables,option) 用于按给定配置导出指定的变量列表。
- Syntax:
```text
ExportResultEx()
ExportResultEx(variables)
ExportResultEx(option)
ExportResultEx(variables,option)
```
- Input Parameters:
```text
variables - 要导出的变量名列表，为空表示导出所有可见变量
   数据类型： str
  option - 导出结果选项配置
   可选配置如下
    timeRange：导出的时间段，使用元组 (t1, t2) 表示，缺省为导出全部时间段。数据类型：tuple
    sampleScale：采样倍率，表示等间隔采样后，剩余点数为原来的几分之一，使用正整数表示，缺省为不采样。数据类型：Int
    withUnit：是否带单位导出，使用 bool 表示，缺省为 False。数据类型：bool
    withDescription：是否带描述导出，使用 bool 表示，缺省为 False。数据类型：bool
    unitType：导出单位类型，withUnit 为 True 时生效，使用整数 1，2 表示，1 表示显示单位，2 表示国标单位，缺省为 1。数据类型：Int
    order：导出变量顺序，使用整数1 ，2 表示，1 表示变量声明顺序，2 表示按首字母排序，缺省为1。数据类型：Int
    target：导出为本地文件还是 Syslab 工作区，使用整数 1，2 表示，表示导出为本地文件，2 表示导出到工作区，缺省为 1。数据类型：Int
    filePath：本地文件的绝对路径，不含文件名，target 为 1 时生效，缺省为软件工作路径。数据类型：str
    formatType：文件后缀，可选变量如下，缺省为 msr
      ResultFormat.Txt txt文件格式，命令中可缩写为 "txt"
      ResultFormat.Csv csv文件格式，命令中可缩写为 "csv"
      ResultFormat.Mat mat文件格式，命令中可缩写为 "mat"
      ResultFormat.Default msr 结果文件格式,命令中可缩写为 "msr" 。选择 target 为1，且导出为 msr 时，timeRange、sampleScale、withUnit、withDescription、unitType、order 均不生效
   数据类型： int  tuple  bool  str
```
- Returns:
```text
bool：表示是否导出成功
```

#### GetCurrentSimTime

- Interface Name: `GetCurrentSimTime`
- Description: 用于获取当前仿真时刻，非仿真状态下，返回上一次仿真的停止时间，若尚未进行过仿真，则会返回 NONE 配合 StartSimulate() 函数，并加入实时仿真配置使用。
- Syntax:
```text
GetCurrentSimTime()
```
- Input Parameters:
```text
无参数
```
- Returns:
```text
float：表示当前仿真的时刻
```

#### GetExperiment

- Interface Name: `GetExperiment`
- Description: 用于获取后处理仿真设置，包括仿真开始时间，结束时间，数据点数，使用输出步长，算法，精度，初始积分步长。
- Syntax:
```text
GetExperiment()
```
- Input Parameters:
```text
无参数
```
- Returns:
```text
dict：python字典格式的仿真设置
startTime，stopTime：仿真开始和结束时间
数据类型：float
intervalLength：仿真输出步长
数据类型：float
numberOfIntervals：仿真输出步数
数据类型：int
algorithm：算法名
数据类型：string
tolerance：精度
数据类型：float
fixedOrInitStepSize：固定或初始化积分步长，当算法为定步长算法、离散积分算法时表示固定积分步长，为变步长算法时表示初始积分步长
数据类型：float
```

#### GetInitialValue

- Interface Name: `GetInitialValue`
- Description: 用于获取指定参数 varName 的仿真参数初始值。
- Syntax:
```text
GetInitialValue(varName)
```
- Input Parameters:
```text
varName - 参数全名
   数据类型： str
```
- Returns:
```text
float：该参数的仿真结果初值
```

#### GetResultVariableInfo

- Interface Name: `GetResultVariableInfo`
- Description: 用于获取当前仿真结果的指定变量信息，包括 Type、Description、Unit、DisplayUnit、Variability。
- Syntax:
```text
GetResultVariableInfo(varName, infoType)
```
- Input Parameters:
```text
varName - 变量全名
   数据类型： str
  infoType - 信息字段名
   数据类型： str
```
- Returns:
```text
str：该变量的描述信息
```

#### GetResultVariables

- Interface Name: `GetResultVariables`
- Description: 用于获取结果中的变量列表，varType 控制获取的变量类型，为 0 则获取所有参量和变量，为 1 则获取所有参量，为 2 则获取所有变量。
- Syntax:
```text
GetResultVariables(varType)
```
- Input Parameters:
```text
varType - 变量类型
   数据类型： int
```
- Returns:
```text
list：变量名列表
```

#### GetSimulationExitState

- Interface Name: `GetSimulationExitState`
- Description: 用于获取仿真的推出状态，正常退出为 0，用户主动停止为 1，仿真失败为 2，未知错误为 -1。
- Syntax:
```text
GetSimulationExitState()
```
- Input Parameters:
```text
无参数
```
- Returns:
```text
int：表示仿真的退出状态
```

#### GetSimulationState

- Interface Name: `GetSimulationState`
- Description: 用于获取当前的仿真状态，包括 "Idle"、 "Running"、 "Paused" 三种状态。
- Syntax:
```text
GetSimulationState()
```
- Input Parameters:
```text
无参数
```
- Returns:
```text
str：表示当前的仿真状态
```

#### GetVarValueAt

- Interface Name: `GetVarValueAt`
- Description: 用于获取变量在特定时刻的值，带查询时刻可以是数值或 SimulationTime.Begin 和 SimulationTime.End。
- Syntax:
```text
GetVarValueAt(varName)
GetVarValueAt(varName, time)
```
- Input Parameters:
```text
varName - 变量名
   数据类型： str
  time - 待查询的时刻
   数据类型： str  int  float
```
- Returns:
```text
float：变量在特定时刻的值
```

#### GetVarValues

- Interface Name: `GetVarValues`
- Description: 用于获取给定变量的所有时刻值，如果 varName="time"，则返回时间序列。
- Syntax:
```text
GetVarValues(varName)
```
- Input Parameters:
```text
varName - 变量名或 "time"
   数据类型： str
```
- Returns:
```text
list：给定变量的所有时刻值或时间序列
```

#### GetVarsValueAt

- Interface Name: `GetVarsValueAt`
- Description: GetVarsValueAt(varNames) 用于批量获取给定变量在默认仿真结束时刻的值。
GetVarsValueAt(varNames, time) 用于批量获取给定变量在特定时刻的值，带查询时刻可以是数值或 SimulationTime.Begin 和 SimulationTime.End。
- Syntax:
```text
GetVarsValueAt(varNames)
GetVarsValueAt(varNames, time)
```
- Input Parameters:
```text
varNames - 变量名
   数据类型： str
  time - 待查询的时刻
   数据类型： str  int  float
```
- Returns:
```text
list：变量在特定时刻的值
```

#### GetVarsValues

- Interface Name: `GetVarsValues`
- Description: 用于批量获取所有给定变量的所有时刻值，如果含有 "time"，则返回的是时间序列。
- Syntax:
```text
GetVarsValues(varNames)
```
- Input Parameters:
```text
varNames - 变量名或 "time"
   数据类型： str
```
- Returns:
```text
list：给定所有变量的所有时刻值或时间序列
```

#### ImportInitial

- Interface Name: `ImportInitial`
- Description: 用于导入初值文件。
- Syntax:
```text
ImportInitial(path)
```
- Input Parameters:
```text
path - 初值文件路径
   数据类型： str
```
- Returns:
```text
bool：表示是否导入成功
```

#### ListSimulationOptions

- Interface Name: `ListSimulationOptions`
- Description: 用于获取所有的仿真设置。
- Syntax:
```text
ListSimulationOptions()
```
- Input Parameters:
```text
无参数
```
- Returns:
```text
dict：所有的仿真设置以及对应参数的类型
```

#### OpenHandleVarsCBFunction

- Interface Name: `OpenHandleVarsCBFunction`
- Description: 开启实时获取仿真结果回调函数的调用，仿真前调用
- Syntax:
```text
N/A
```
- Input Parameters:
```text
N/A
```
- Returns:
```text
N/A
```

#### OpenResult

- Interface Name: `OpenResult`
- Description: 用于打开已有的仿真结果文件，需包含 Result.msr。
- Syntax:
```text
OpenResult(path)
```
- Input Parameters:
```text
path - 结果文件路径
   数据类型： str
```
- Returns:
```text
bool：表示是否打开成功
```

#### PauseSimulate

- Interface Name: `PauseSimulate`
- Description: 用于配合函数 StartSimulate() 使用，暂停仿真，暂停成功后，GetSimulationState 的值会成为 "Paused"
- Syntax:
```text
PauseSimulate()
```
- Input Parameters:
```text
无参数
```
- Returns:
```text
bool：表示是否成功暂停仿真
```

#### Plot

- Interface Name: `Plot`
- Description: 用于以默认设置在最后一个窗口中绘制曲线，如果没有窗口则按系统默认设置新建一个窗口。
- Syntax:
```text
Plot()
Plot(y, legend, colors, lineStyles, markerStyles, thicknesses, displayUnits, verticalAxes)
```
- Input Parameters:
```text
y - 变量名列表
   数据类型： str
  legend - 图例列表
   数据类型： str
  colors - 曲线颜色
   可选变量如下：
    LineColor.Black 黑色
    LineColor.Brown 棕色
    LineColor.Green 绿色
    LineColor.Magenta 洋红
    LineColor.Purple 紫色
    LineColor.Red 红色
    LineColor.Yellow 黄色
     数据类型： str  int
  lineStyles - 曲线线型
   可选变量如下：
    LineStyle.DashDot 点划线
    LineStyle.DashDotDot 双点划线
    LineStyle.Dashed 虚线
    LineStyle.Dotted 点线
    LineStyle.Solid 实线
     数据类型： int
  markerStyles - 曲线数据点样式
   可选变量如下：
    MarkerStyle.Circle 圆形
    MarkerStyle.Cross 交叉形
    MarkerStyle.Diamond 菱形
    MarkerStyle.FilledCircle 实心圆
    MarkerStyle.FilledSquare 实心正方形
    MarkerStyle.None_ 不显示数据点
    MarkerStyle.Square 正方形
    MarkerStyle.TriangleDown 倒三角形
    MarkerStyle.TriangleUp 正三角形
     数据类型： int
  thicknesses - 线宽
   可选变量如下：
    LineThickness.Double 双倍线宽
    LineThickness.Quad 四倍线宽
    LineThickness.Single 单倍线宽
     数据类型： int
  displayUnits - 显示单位列表
   数据类型： str
  verticalAxes - 纵轴类型
   可选变量如下：
    VerticalAxis.Left 左纵轴
    VerticalAxis.Right 右纵轴
     数据类型： int
```
- Returns:
```text
bool：表示是否成功绘制曲线
```

#### RegisterHandleVarsCBFunction

- Interface Name: `RegisterHandleVarsCBFunction`
- Description: RegisterHandleVarsCBFunction(handle, userdata) 用来注册处理通知数据的函数，在 TranslateModel 之后、StartSimulate 前调用 SetWatchVariables，则在仿真过程中会循环调用通过 RegisterHandleVarsCBFunction 注册的 handle 函数，以通知仿真数据。
- Syntax:
```text
RegisterHandleVarsCBFunction(handle, userdata)
```
- Input Parameters:
```text
handle - 处理通知数据的回调函数
   数据类型：function
   handle 函数的格式为：handle(vars list, last_datas, userdata)
   其中：
    vars 为 liststr，表示变量列表。其值为 SetWatchVariables 函数设置的通知变量的变量名列表，并在第一个元素插入 'time'
    last_datas 为 float 二维数组，表示从上一次处理到本次处理期间的仿真数据。其值为列主数据，即每个元素为某个变量在这一时间段内的所有数据，变量顺序与 vars 一致
    userdata 为任意类型，表示用户数据。其值来自于 RegisterHandleVarsCBFunction 注册时传入的自定义数据
  userdata - 传给回调函数的自定义数据
   数据类型：任意
   用于将外部的数据传到回调函数中
```
- Returns:
```text
N/A
```

#### RemoveAnimations

- Interface Name: `RemoveAnimations`
- Description: 用于关闭所有动画窗口。
- Syntax:
```text
RemoveAnimations()
```
- Input Parameters:
```text
无参数
```
- Returns:
```text
bool：True 表示操作成功，False 表示失败。
```

#### RemovePlots

- Interface Name: `RemovePlots`
- Description: 用于关闭所有曲线窗口。
- Syntax:
```text
RemovePlots()
```
- Input Parameters:
```text
无参数
```
- Returns:
```text
bool：表示是否关闭成功
```

#### RemoveResult

- Interface Name: `RemoveResult`
- Description: 用于移除最后一个仿真结果，不保存，也不询问用户。
- Syntax:
```text
RemoveResult()
```
- Input Parameters:
```text
无参数
```
- Returns:
```text
bool：表示是否清除成功
```

#### RemoveResults

- Interface Name: `RemoveResults`
- Description: 用于清除所有实例，包括未保存的。
- Syntax:
```text
RemoveResults()
```
- Input Parameters:
```text
无参数
```
- Returns:
```text
bool：表示是否清除成功
```

#### ResimulateCurrentResult

- Interface Name: `ResimulateCurrentResult`
- Description: 用于以仿真设置 option 重新仿真当前结果，当 option 为空时，以当前结果的仿真设置重新仿真。 该命令为同步命令，仿真结束后，该命令才会返回。 注意：
  若当前结果的算法是离散求解算法（如 InlinelmplicitEuler 或 InlinelmplicitTrapezoid）时，则仅允许修改仿真时间；
  若当前结果的算法不是离散求解算法，则不允许切换为离散求解算法。
- Syntax:
```text
ResimulateCurrentResult(option)
```
- Input Parameters:
```text
options - 仿真设置
   支持的参数（options）
参数名                   格式      示例                              说明
algorithm             str     'Dassl'                         算法名
fixedOrInitStepSize   float   0.002                           固定或初始化积分步长，当算法为定步长算法、离散积分算法时表示固定积分步长，为变步长算法时表示初始积分步长
interval              float   0.002                           输出区间长度（不可设为-1）
pieceWiseStep         tuple   ((0.0, 0.001), (1.0, 0.002),)   分段固定步长
startTime             float   0.0                             仿真开始时间
stopTime              float   1.0                             仿真停止时间
tolerance             float   0.0001                          精度
```
- Returns:
```text
bool：表示是否成功启动仿真
```

#### ResumeSimulate

- Interface Name: `ResumeSimulate`
- Description: 用于恢复仿真，配合函数 PauseSimulate() 使用，只有当 GetSimulationState 为 "Paused" 时有效。继续成功后，GetSimulationState 的值会成为 "Running"。
- Syntax:
```text
ResumeSimulate()
```
- Input Parameters:
```text
无参数
```
- Returns:
```text
bool：表示是否成功恢复仿真
```

#### RunAnimation

- Interface Name: `RunAnimation`
- Description: 用于播放动画。
- Syntax:
```text
RunAnimation()
```
- Input Parameters:
```text
无参数
```
- Returns:
```text
bool：表示是否播放成功。
```

#### SetInitialValue

- Interface Name: `SetInitialValue`
- Description: 用于设置仿真结果参数 varName 的初值为 varValue。
- Syntax:
```text
SetInitialValue(varName, varValue)
```
- Input Parameters:
```text
varName - 参数全名
   数据类型： str
  varValue - 待设置的参数值
   数据类型： int  float
```
- Returns:
```text
bool：表示参数设置是否成功
```

#### SetPauseTimeForSimulation

- Interface Name: `SetPauseTimeForSimulation`
- Description: SetPauseTimeForSimulation() 用于清空仿真暂停时间设置。
SetPauseTimeForSimulation(pauseTime) 用于设置仿真暂停时间。
- Syntax:
```text
SetPauseTimeForSimulation()
SetPauseTimeForSimulation(pauseTime)
```
- Input Parameters:
```text
pauseTime - 暂停时间
   数据类型： float
```
- Returns:
```text
bool：表示是否成功设置仿真时暂停时间
```

#### SetWatchVariables

- Interface Name: `SetWatchVariables`
- Description: 用于设置要通知的监视变量，在 TranslateModel 之后、StartSimulate 前调用 SetWatchVariables，则在仿真过程中会循环调用通过 RegisterHandleVarsCBFunction 注册的 handle 函数，以通知仿真数据。
- Syntax:
```text
SetWatchVariables(vars)
```
- Input Parameters:
```text
vars - 要实时通信的监视变量
   vars 的元素形式为变量全名的字符串 数据类型： str
```
- Returns:
```text
bool：表示是否成功设置
```

#### SimulateModel

- Interface Name: `SimulateModel`
- Description: 用于仿真模型，参数 modelName 必须指定，其余参数可按默认值。
- Syntax:
```text
SimulateModel(modelName)
SimulateModel(modelName, startTime, stopTime, interval, tolerance, algo, integralStep, storeDouble, storeEvent, simMode, isPieceWiseStep, path, pieceWiseStep)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
  startTime - 仿真开始时间
   数据类型： int  float  None
  stopTime - 仿真终止时间
   数据类型： int  float  None
  interval - 输出区间长度
   数据类型： int  float  None
  algo - 积分算法
   可选积分算法如下：
积分算法名称                          缩写
Integration.Dassl               Dassl
Integration.Radau5              Radau5
Integration.Dop853              Dop853
Integration.Dopri5              Dopri5
Integration.Mebdf               Mebdf
Integration.Mebdfi              Mebdfi
Integration.Lsode               Lsode
Integration.Lsodar              Lsodar
Integration.Cvode               Cvode
Integration.Ida                 Ida
Integration.Sdirk34             Sdirk34
Integration.Esdirk23            Esdirk23
Integration.Esdirk34            Esdirk34
Integration.Esdirk45            Esdirk45
Integration.Euler               Euler
Integration.Rkfix2              Rkfix2
Integration.Rkfix3              Rkfix3
Integration.Rkfix4              Rkfix4
Integration.Rkfix6              Rkfix6
Integration.Rkfix8              Rkfix8
Integration.lmplicitEuler       lmplicitEuler
Integration.lmplicitTrapezoid   lmplicitTrapezoid
Integration.Custom              Custom
  integralStep - 初始积分步长
   数据类型： int  float  None
  storeDouble - 结果是否存为双精度
   数据类型： bool  None
  storeEvent - 结果是否存为双精度
   数据类型： bool  None
  simMode - 设置仿真模式，0为使用当前仿真模式，1为独立仿真，2为实时仿真
   数据类型： int  None
  isPieceWiseStep - 是否使用分段固定积分步长
   数据类型： bool  None
  path - 仿真结果文件存放的文件夹路径
   数据类型： str  None
  pieceWiseStep - 设置某段时间节点采用的积分步长。pieceWiseStep = ((0, xxx), (m, xxx), (n, xxx), ...), pieceWiseStep以二维数组表示，第一个数为时间节点，"xxx"为从当前时间节点开始的步长。
   数据类型： int  float
```
- Returns:
```text
bool：表示是否仿真成功
```

#### SimulateModelEx

- Interface Name: `SimulateModelEx`
- Description: 用于基于设置进行仿真，相比 SimulateModel() 增加了可设置的选项。
- Syntax:
```text
SimulateModelEx(modelName,options)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
  options - 仿真设置
   支持的参数(options)
   参数名                                                             格式      示例                              说明
   algorithm                                                       str     'Dassl'                         算法名
   compileSolver64                                                 int     1                               是否使用64位编译
   compileOptions                                                  int     1                               选择编译策略 (0仿真效率优先, 1翻译效率优先, 2 均衡)
   cCompileWarningMessage                                          bool    True                            C编译选项是否开启警告信息
   cCompileAllowSymbolRedef                                        bool    True                            C编译选项是否允许符号重定义
   debugIncludeFunctionCallInErrorMessages                         bool    True                            调试信息-错误信息中包含函数调用环境
   debugLinearSolution                                             bool    True                            调试信息-诊断线性求解结果
   debugLoggingDynamicStateSelection                               bool    True                            调试信息-记录动态状态变量选择
   debugLoggingEventsDuringSimulation                              bool    True                            调试信息-记录仿真中的事件
   debugLoggingNormalWarningMessage                                bool    True                            调试信息-记录正常的警告信息
   debugMixedIteration                                             bool    True                            调试信息-记录混合方程迭代过程
   debugNonlinearIteration                                         bool    True                            调试信息-诊断非线性迭代过程
   debugNonlinearSolution                                          bool    True                            调试信息-诊断非线性求解结果
   debugNonlinearStatistic                                         bool    True                            调试信息-诊断非线性统计信息
   debugSingularLinearSolution                                     bool    True                            调试信息-诊断线性奇异解
   fixedOrInitStepSize                                             float   0.002                           固定或初始化积分步长，当算法为定步长算法、离散积分算法时表示固定积分步长，为变步长算法时表示初始积分步长
   inlineIntegrator                                                bool    True                            内联离散积分步长算法
   inlineStepSize                                                  bool    True                            内联积分步长
   interval                                                        float   0.002                           输出区间长度（-1 表示auto, 仅限Sysblock模型）
   outputContinuePointsTime(s) (not supported)                    list    1.0, 2.0                      自定义接续仿真的接续时刻点(暂不支持)
   outputGenerateStepsOfPointsBeforeSimulationStops                int     10                              仿真停止前接续仿真的接续时刻点数量
   outputGenerateTheContinueSimulationResultFile                   bool    True                            是否生成接续仿真文件
   outputGeneratingIsFixedContinueInterval                         bool    True                            是否生成固定区间的接续时刻点
   outputGeneratingIsSaveBeforeStop                                bool    True                            是否在仿真停止前生成接续时刻点
   outputMaximumNumberOfSimulationVariables                        int     1000000                         最大仿真变量数
   outputNumberOfContinuePoints                                    int     10                              固定区间的接续时刻点数量
   outputNumberOfResultsToKeep                                     int     2                               仿真面板上保持的结果数量
   Path                                                            str     'D/Smiulation'                  仿真结果路径
   pieceWiseStep                                                   tuple   ((0.0, 0.001), (1.0, 0.002),)   分段固定步长
   realtimeSimulationMode                                          int     1                               实时仿真模式，0为使用当前仿真模式，1表示自动，2表示实时
   realtimeSlowdownFactor                                          float   1.0                             实时仿真减速比
   startTime                                                       float   0.0                             仿真开始时间
   steadyStateInitialization                                       bool    True                            是否使用稳态初始化
   steadyStateOmitFixedStartOfContinuousVariable                   bool    True                            是否忽略连续变量的 fixed、start属性
   steadyStateOmitInitialEquationAlgorithm                         bool    True                            是否忽略初始化方程算法
   steadyStateSearchSettingDetectionTolerance                      float   0.0001                          稳态查找的容差
   steadyStateSearchSettingStartTimeForSearching                   float   0.1                             稳态查找的开始时间
   steadyStateSimulationMode                                       int     1                               稳态仿真模式，0表示动态仿真，1表示静态仿真，2表示动态稳态查找
   stopTime                                                        float   1.0                             仿真停止时间
   storeDouble                                                     bool    True                            是否以双精度保存结果
   storeEvent                                                      bool    True                            是否存储事件时刻变量值
   tolerance                                                       float   0.0001                          精度
   translationCheckConnection_Strictly                             bool    True                            翻译-严格检查连接
   translationDeduceUnits                                          bool    True                            翻译-自动推导单位
   translationEvaluateParametersToReduceModels                     bool    True                            翻译-参数估值以提升效率
   translationGenerateFlat_ModelicaCodeInMofFile                   bool    True                            翻译-生成平坦化Modelica模型到mof文件
   translationListContinuousTimeStatesSelected                     bool    True                            翻译-记录所选的连续时间状态变量
   translationLogInformationWhenDifferentiatingForIndexReduction   bool    True                            翻译-输出指标约简时的微分方程信息
   translationLogNonlinearIterationVariableAndTheInitialValue      bool    True                            翻译-记录非线性迭代变量及其初值
   translationLogSelectedDefaultInitialConditons                   bool    True                            翻译-记录所选的缺省初值条件
   optimizationRuntimeCheck                                        bool    True                            调试-运行时检查错误
```
- Returns:
```text
bool：表示是否成功仿真
```

#### StartSimulate

- Interface Name: `StartSimulate`
- Description: 用于基于设置进行异步仿真，modelName 表示模型全名，options 表示扩展选项设置，参考 SimulateModelEx 命令，函数返回值为仿真时的相关信息。
- Syntax:
```text
StartSimulate(modelName,options)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
  options - 仿真设置
   可参见 SimulateModelEx
     数据类型： str  int  bool  float  list  tuple
```
- Returns:
```text
bool：表示是否成功启动仿真
```

#### StopSimulate

- Interface Name: `StopSimulate`
- Description: 用于停止仿真，停止成功后，GetSimulationState 的值会成为 'Idle'，配合 StartSimulate() 或者 PauseSimulate() 使用。 未传入超时时间时（或超时时间小于 0），一直等待仿真停止并于 2.5 秒后弹出确认是否立即终止的窗口 传入超时时间时（大于等于 0），若停止仿真超时则直接终止仿真不弹窗确认，等于 0 时强制终止。
- Syntax:
```text
StopSimulate()
StopSimulate(timeout)
```
- Input Parameters:
```text
timeout - 停止仿真的超时时间（单位秒）
   数据类型： int  float  None
```
- Returns:
```text
bool：表示是否成功停止仿真
```

## SysblockPy

### BasicModelingOperationsPy

#### BindDataDictionary

- Interface Name: `BindDataDictionary`
- Description: 用于绑定数据字典文件。
- Syntax:
```text
BindDataDictionary(strModelName, strPath, bSaveDict)
```
- Input Parameters:
```text
strModelName - 模型全名
   数据类型： str
  strPath - 文件路径
   数据类型： str
  bSaveDict - 是否保存当前编辑内容到被替换的字典文件中
   数据类型： bool
```
- Returns:
```text
bool：表示是否绑定成功
```

#### ClearWorkspace

- Interface Name: `ClearWorkspace`
- Description: 用于清空指定工作区数据。 strModelName 为空时，表示清空基础工作区数据；strModelName 不为空时，它只能是 Sysblock 模型，表示清空该 Sysblock 模型的模型工作区数据。 若该工作区已经没有数据了，仍然会返回 True。
- Syntax:
```text
ClearWorkspace(strModelName)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
```
- Returns:
```text
bool：表示是否清空
```

#### ExportModelDataFile

- Interface Name: `ExportModelDataFile`
- Description: 用于导出工作区数据到文件中。 strModelName 为空时，表示导出基础工作区数据到文件中；strModelName 不为空时，它只能是 Sysblock 模型，导出该模型的模型工作区数据到文件中。
- Syntax:
```text
ExportModelDataFile(strModelName, strPath)
```
- Input Parameters:
```text
strModelName - 模型全名
   数据类型： str
  strPath - 文件路径
   数据类型： str
```
- Returns:
```text
bool：表示是否导出成功
```

#### GenerateModelCode

- Interface Name: `GenerateModelCode`
- Description: 用于设置使用模型的代码生成配置进行代码生成。
- Syntax:
```text
GenerateModelCode(modelName)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
```
- Returns:
```text
bool：表示是否操作成功
```

#### GetModelCodeGenerationOptions

- Interface Name: `GetModelCodeGenerationOptions`
- Description: 用于获取 Sysblock 代码生成配置，modelName 表示模型全名。
- Syntax:
```text
GetModelCodeGenerationOptions(modelName)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
```
- Returns:
```text
dict：模型的 Sysblock 代码生成配置
```

#### GetWorkspaceEntryProperty

- Interface Name: `GetWorkspaceEntryProperty`
- Description: 用于获取模型工作区数据项属性。
- Syntax:
```text
GetWorkspaceEntryProperty(modelName, entryName, propertyName)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
  entryName - 数据项名
   数据类型： str
  propertyName - 属性名
   数据类型： str
```
- Returns:
```text
str：数据项属性值
```

#### ImportModelDataFile

- Interface Name: `ImportModelDataFile`
- Description: 用于导入工作区文件到工作区中。 strModelName 为空时，表示将文件导入到基础工作区中；strModelName 不为空时，它只能是 Sysblock 模型，表示将文件导入到该模型的模型工作区中。 若工作区中已存在同名数据，旧的数据会被新导入的数据覆盖。
- Syntax:
```text
ImportModelDataFile(strModelName, strPath)
```
- Input Parameters:
```text
strModelName - 模型全名
   数据类型： str
  strPath - 文件路径
   数据类型： str
```
- Returns:
```text
bool：表示是否导入成功
```

#### ListCodeGenerationOptions

- Interface Name: `ListCodeGenerationOptions`
- Description: 获得 Sysblock 代码生成配置。
- Syntax:
```text
ListCodeGenerationOptions()
```
- Input Parameters:
```text
无参数
```
- Returns:
```text
dict：Sysblock 代码生成配置
```

#### OpenModelFile

- Interface Name: `OpenModelFile`
- Description: OpenModelFile(path) 加载指定的 Modelica 模型文件，支持.mol 和.mo文件。 OpenModelFile(path, autoReload) 加载指定的 Modelica 模型文件，支持.mol 和.mo文件，并指定加载重复模型时，是否自动重新加载模型。 默认情况下，不指定 autoReload 加载重复模型时，会自动重新加载模型。
- Syntax:
```text
OpenModelFile(path)
OpenModelFile(path, autoReload)
```
- Input Parameters:
```text
path - Modelica模型文件的全路径
   数据类型： str
  autoReload - 已经加载是否自动重新加载
   数据类型： bool
```
- Returns:
```text
bool表示模型是否成功打开
```

#### SetModelCodeGenerationOptions

- Interface Name: `SetModelCodeGenerationOptions`
- Description: 用于设置 Sysblock 代码生成配置，modelName 表示模型全名，options 表示代码生成配置全文本。
- Syntax:
```text
SetModelCodeGenerationOptions(modelName, options)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
  options - 代码生成配置全文本
   数据类型： dict
```
- Returns:
```text
bool：表示是否设置成功
```

#### SetWorkspaceEntryProperty

- Interface Name: `SetWorkspaceEntryProperty`
- Description: SetWorkspaceEntryProperty(modelNamestr, entryNamestr, propertyNamestr, propertyValuestr) 用于设置模型工作区数据项属性。
- Syntax:
```text
SetWorkspaceEntryProperty(modelNamestr, entryNamestr, propertyNamestr, propertyValuestr)
```
- Input Parameters:
```text
modelName - 模型全名
   数据类型： str
  entryName - 数据项名
   数据类型： str
  propertyName - 属性名
   数据类型： str
  propertyValue - 属性值
   数据类型： str
```
- Returns:
```text
bool：表示是否设置成功
```

#### UnbindDataDictionary

- Interface Name: `UnbindDataDictionary`
- Description: 用于解绑数据字典文件。
- Syntax:
```text
UnbindDataDictionary(strModelName, bSaveDict)
```
- Input Parameters:
```text
strModelName - 模型全名
   数据类型： str
  bSaveDict - 是否保存当前编辑内容到即将解绑的字典文件中
   数据类型： bool
```
- Returns:
```text
bool：表示是否解绑成功
```
