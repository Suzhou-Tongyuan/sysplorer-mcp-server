# 模型依赖解析与下载方案

## 0. 启动级下载授权

新增启动参数：

```text
--user-workspace <path>
```

该参数表示用户工作空间，也是依赖下载/安装流程的启动级授权开关。只有启动 MCP Server 时显式传入
`--user-workspace` 后，`model_manager(action="load_file")` 默认接入的依赖准备流程才允许执行
`GetModelDependencies`、TOML 合并、latest 查询、下载、解压安装、`UpdateLibrary` 和自动 `LoadLibrary`。

未传入 `--user-workspace` 时：

- `model_manager(action="load_file")` 不启动本文档描述的新依赖准备/下载流程；
- `dependency_manager(action="prepare" 或 "download", dry_run=false, download_missing=true)` 会被集中拦截；
- 无副作用的 `resolve` / `plan` / `dry_run=true` 调试路径仍可保留；
- 返回结果中应包含 `dependency_download_gate`，说明当前下载被禁用及需要通过 `--user-workspace` 启用。

路径使用规则：

- `--workspace-dir` 继续表示 MCP/Agent 工程根，用于 `src`、`private_lib`、模型输出等；
- `--user-workspace` 表示用户工作空间，不与部署目录混用；
- `--user-workspace` 指向的目录在依赖流程首次使用时可自动创建，创建失败则拒绝下载；
- 未显式传 `dependency_toml_path` 时，依赖清单优先读取 `<user-workspace>/Manifest.toml`；
- 依赖库最终安装目录仍遵循 `dependency_download_dir` / `MWORKS_LIBRARY_ROOT` / MWorks 安装目录下 `Library`
  的既有优先级，不因 `--user-workspace` 自动改写。

`Manifest.toml` 是当前确认的最终依赖清单文件名。该文件由 MOLS API 生成，MCP 只读使用，不回写，也不建议用户直接编辑。文件可以不存在；不存在时不报错，依赖流程继续使用 `GetModelDependencies`、remote latest 和已安装库检测。

最终格式如下：

```toml
# This file is machine-generated - editing it directly is not advised.
# This file contains the loaded model library content returned by the MOLS API.

manifest_format = "2.0"

[[dependencies]]
name = "TAElectronic"
licenseFeature = "MW_Lib_TAElectronic"
version = "1.3.0"

[[dependencies]]
name = "TAEconomy"
licenseFeature = "MW_Lib_TAEconomy"
version = "1.3.2"
```

读取规则：

- 仅支持 `manifest_format = "2.0"`；
- 第一版只读取全局 `[[dependencies]]`；
- 每条依赖至少需要 `name`，`version` 和 `licenseFeature` 可参与后续计划；
- `Manifest.toml` 中的版本优先级高于 `GetModelDependencies` 返回版本；
- `licenseFeature` 作为商业库授权信息随依赖计划透传；
- 文件存在但格式错误时，按 `stop_on_error` 决定直接失败或记录 warning 后继续。

## 1. 背景

当前 MCP Server 在加载 `.mo` 文件时，已经有一套“依赖预加载”逻辑。入口是
`model_manager(action="load_file")`，实现位于：

```text
sysplorer-mcp-server/tools/model_ops.py
```

当前流程：

```text
model_manager(action="load_file", file_path=..., auto_load_deps=true)
  -> _mm_load_file()
  -> _extract_dep_libs(.mo)
  -> driver.load_library(...)
  -> OpenModelFile(...)
```

这套逻辑只是 best-effort 的“预加载依赖库”，还不是完整的“依赖解析、版本补全、缺失库下载、刷新 Sysplorer 库索引、再加载模型”的闭环。

## 2. 当前实现

### 2.1 依赖解析

当前依赖解析函数是：

```text
sysplorer-mcp-server/core/utils.py::_extract_dep_libs
```

它会把 `.mo` 文件当文本读取，然后从两个来源推断依赖库：

1. `annotation(uses(...))`
2. 代码中出现的顶层限定命名空间，例如 `Modelica.xxx`、`TYMultibody.xxx`

之后会做这些处理：

- 跳过模型自身的顶层包名；
- 跳过内置类型根：`Real`、`Integer`、`Boolean`、`String`、`Enumeration`；
- 如果本地有 Sysplorer 库元数据，就用元数据过滤已知库；
- 去重；
- 如果存在 `Modelica`，把 `Modelica` 放到最前面。

### 2.2 依赖加载

在 `sysplorer-mcp-server/tools/model_ops.py::_mm_load_file` 中，当
`auto_load_deps=true` 时，服务端会遍历 `_extract_dep_libs` 返回的依赖，然后调用：

```text
driver.load_library(library_name=lib_fqname)
```

最终会映射到：

```text
mworks.sysplorer.LoadLibrary(...)
```

依赖加载结果会写入返回 JSON 的 `auto_loaded_libs` 字段。

### 2.3 当前限制

当前实现存在这些限制：

- 没有调用新的官方 `mworks.sysplorer` 依赖解析 API；
- 不会下载缺失模型库；
- 没有结构化区分“库未安装”和其他 `LoadLibrary` 失败；
- 依赖预加载失败时，默认仍会继续执行 `OpenModelFile`；
- 对大部分商业库来说，`uses(version="...")` 中的版本信息不会真正传给 `LoadLibrary`；
- 依赖解析依赖正则和文本启发式规则，可能漏报或误报。

## 3. 新需求

目标功能：

1. 通过 Sysplorer API 获取模型依赖。
2. 将依赖与工作区配置、本地已安装库、远端 latest 版本进行合并。
3. 下载缺失模型库。
4. 下载后刷新 Sysplorer 软件的库索引。
5. 再执行 `LoadLibrary`、打开模型、检查模型。
6. 如果检查阶段暴露出更准确的版本信息，则回到下载流程做一次修复。

## 4. 依赖 API 策略

### 4.1 对外统一名称

本需求上层统一使用正式接口名：

```text
GetModelDependencies(model_name)
```

MCP 文档、MCP 工具参数、内部 helper 名称都先按 `GetModelDependencies` 设计。

已确认：正式 `GetModelDependencies` 最终签名只接收 `modelName`，不再接收 `existingConfigPath`。

正式接口形态：

```python
GetModelDependencies(modelName: str) -> list
```

输入为模型全名 `modelName`，返回结构固定为：

```json
[
  {"name": "...", "version": "..."}
]
```

该返回值用于描述当前模型需要准备的模型库依赖。接口侧负责模型依赖解析；MCP 侧仍需要做结果归一化、TOML 只读版本覆盖、远端 latest 补全、调用 `GetInstalledLibraries()` 做已安装库去重、下载/安装编排以及递归 `uses.ini` 依赖处理。

### 4.2 MCP driver 封装

MCP driver 层实现为：

```text
driver.get_model_dependencies(model_name)
```

内部只调用正式 API：

```text
GetModelDependencies(modelName)
```

建议返回结构：

```json
{
  "api": "GetModelDependencies",
  "data": [
    {"name": "...", "version": "..."}
  ]
}
```

注意：MCP 代码和方案均只保留正式接口路径。正式接口 `GetModelDependencies(modelName)` 按 `[{"name": "...", "version": "..."}]` 结构返回，MCP 侧仍然保留自己的版本合并、下载安装和递归依赖编排能力。

## 5. 推荐总体流程

完整闭环建议如下：

```text
输入 model_name / file_path
  -> 确保模型已加载或可解析出模型名
  -> GetModelDependencies(modelName)
  -> 归一化依赖记录
  -> 只读工作区依赖 TOML，补充或覆盖版本
  -> 对仍缺版本的依赖查询远端 latest
  -> GetInstalledLibraries() 获取 Sysplorer 已安装库集合
  -> 使用 name + version 去重
  -> 下载并安装缺失库
  -> uses.ini 递归依赖继续复用已安装库集合去重，目录检测只作兜底
  -> 调用 Sysplorer UpdateLibrary 刷新库索引
  -> LoadLibrary
  -> OpenModel / CheckModel
  -> 如果诊断中解析到更准确 name + version，回到下载、刷新、加载流程重试一次
  -> 如果诊断中解析不到 name + version，不再下载，直接返回诊断
```

## 6. 模块划分与责任边界

| 模块 | 主要职责 | 实现位置 |
| --- | --- | --- |
| `DependencyResolver` | 统一调用 `GetModelDependencies` | MCP 实现，底层 API 由 Sysplorer 提供 |
| `WorkspaceDependencyLock` | 只读 `<user-workspace>/Manifest.toml`，按 Manifest 补版本或覆盖版本，不回写 | MCP 实现 |
| `InstalledLibraryDetector` | 调用 `GetInstalledLibraries()` 获取已安装模型库，并在 plan/download 前按 `name + version` 去重 | Sysplorer API 为主；MCP 文件系统检测仅作兜底 |
| `RemoteLibraryResolver` | 对缺版本依赖查询远端 latest 版本 | 用户提供 Python/HTTP 代码，MCP 封装调用 |
| `LibraryDownloader` | 下载缺失模型库，已安装或已下载则跳过 | 用户提供 Python 下载代码，MCP 封装调用 |
| `LibraryCatalogRefresher` | 下载后刷新 Sysplorer 软件库索引 | Sysplorer 提供 API；MCP 封装调用 |
| `DependencyRepairLoop` | 从 `OpenModel` / `CheckModel` 失败诊断中提取库版本并重试 | MCP 实现；诊断内容由 Sysplorer 返回 |

## 7. 各模块设计

### 7.1 DependencyResolver

MCP 中新增统一 helper：

```python
def resolve_model_dependencies(
    model_name: str,
) -> dict:
    ...
```

设计要求：

- 对外统一叫 `GetModelDependencies`。
- 只调用正式 API `GetModelDependencies`。
- 返回结果归一化为结构化依赖列表。

建议输出：

```json
{
  "ok": true,
  "api": "GetModelDependencies",
  "model_name": "MyModel",
  "dependencies": [
    {
      "name": "TYMultibody",
      "version": "1.5.0",
      "version_source": "sysplorer_dependency_api",
      "raw": {"name": "TYMultibody", "version": "1.5.0"}
    }
  ],
  "warnings": []
}
```

如果后续正式接口返回完整依赖，则本模块仍只负责“拿到并归一化依赖”，不在这里完成下载。

### 7.2 WorkspaceDependencyLock

当前已确认工作区依赖清单文件为：

```text
<user-workspace>/Manifest.toml
```

`Manifest.toml` 由 MOLS API 生成，描述已加载模型库内容。MCP 只读使用该文件参与版本补全、版本覆盖和
`licenseFeature` 透传，不回写，也不建议用户直接编辑。文件不存在不是错误；不存在时 `used=false`，后续继续使用
`GetModelDependencies`、remote latest 和已安装库检测。

最终格式：

```toml
# This file is machine-generated - editing it directly is not advised.
# This file contains the loaded model library content returned by the MOLS API.

manifest_format = "2.0"

[[dependencies]]
name = "TAElectronic"
licenseFeature = "MW_Lib_TAElectronic"
version = "1.3.0"

[[dependencies]]
name = "TAEconomy"
licenseFeature = "MW_Lib_TAEconomy"
version = "1.3.2"
```

读取和校验规则：

- 仅支持 `manifest_format = "2.0"`；
- 第一版只读取全局 `[[dependencies]]`；
- 每条依赖至少需要 `name`；
- `version` 存在时作为本地锁定版本；
- `licenseFeature` 随依赖计划透传，用于商业库授权信息展示或后续 license 判断；
- 文件存在但 `manifest_format` 错误、`[[dependencies]]` 类型错误或 TOML 语法错误时，按 `stop_on_error` 策略返回错误或 warning。

版本优先级：

```text
Manifest.toml 版本 > GetModelDependencies 返回版本 > 远端 latest
```

也就是说：

- 如果 API 没有返回版本，但 Manifest 有版本，则使用 Manifest 版本。
- 如果 API 和 Manifest 都有版本，则优先使用 Manifest。
- 如果 API 和 Manifest 都没有版本，后续再查远端 latest。
- 如果 latest 仍无法补齐版本，则该依赖不能进入下载队列，应在 plan 中标记为 `missing_version`。

第一版不实现 `install=false`、按模型/profile 分组或多套版本组合；这些能力后续如有明确业务输入再扩展。

### 7.3 InstalledLibraryDetector

用于在下载前判断本地已安装模型库，第一版必须优先使用 Sysplorer 官方 API。

理由：最终 `LoadLibrary` 能否加载，取决于 Sysplorer 当前可识别的模型库集合。磁盘上存在某个文件，不一定代表 Sysplorer 已能识别。

已确认官方接口：

```python
GetInstalledLibraries() -> list
```

官方返回结构：

```json
[
  {
    "name": "TYMultibody",
    "version": "1.5.0",
    "is_load": false
  }
]
```

MCP 归一化输出：

```json
{
  "ok": true,
  "api": "GetInstalledLibraries",
  "installed": [
    {
      "name": "TYMultibody",
      "version": "1.5.0",
      "is_load": false
    }
  ],
  "installed_keys": [
    "tymultibody@1.5.0"
  ]
}
```

执行规则：

- `GetModelDependencies(modelName)` 只负责获取模型依赖入口；
- TOML 与 latest 补齐版本后，MCP 调用 `GetInstalledLibraries()`；
- 用 `name.lower() + "@" + version` 生成 installed set；
- `plan` 阶段如果依赖已在 installed set 中，标记为 `skip / already_installed`，不进入下载队列；
- `uses.ini` 递归依赖也必须先查 installed set，避免重复下载已安装库；
- 文件系统安装目录检测只作为兜底和并发保护，不作为主判断来源。

文件系统兜底路径：

```text
<LibraryRoot>/<模型库名> <版本号>/
```

如果 `GetInstalledLibraries()` 不存在或调用失败：

- `stop_on_error=true` 时直接返回明确错误；
- `stop_on_error=false` 时记录 warning，并继续使用文件系统兜底判断；
- 该 fallback 只是“磁盘检测”，权威性低于 Sysplorer API。

### 7.4 RemoteLibraryResolver

用于对缺失版本的依赖查询远端 latest 版本。

特殊规则：

- `Modelica` 没有远端 latest；
- 当依赖名为 `Modelica` 且没有传入明确版本时，MCP 不访问 `/latest`；
- MCP 直接填充默认版本 `4.0.0.TY.1`；
- 返回结果中 `version_source` 标记为 `default_version`。

输入：

```json
[
  {"name": "TYMultibody", "version": ""}
]
```

输出：

```json
[
  {
    "name": "TYMultibody",
    "version": "1.5.0",
    "version_source": "remote_latest"
  }
]
```

固定输入：

```json
{
  "name": "TYMultibody"
}
```

固定输出：

```json
{
  "ok": true,
  "name": "TYMultibody",
  "version": "1.5.0",
  "version_source": "remote_latest",
  "url": "https://...",
  "visibility": "private",
  "bucket": "modelica"
}
```

`Modelica` 默认版本输出：

```json
{
  "ok": true,
  "name": "Modelica",
  "version": "4.0.0.TY.1",
  "version_source": "default_version",
  "url": null,
  "visibility": "public",
  "bucket": "modelica",
  "skipped_remote_latest": true
}
```

失败时固定输出：

```json
{
  "ok": false,
  "name": "TYMultibody",
  "error": "...",
  "url": "https://...",
  "visibility": "private",
  "bucket": "modelica"
}
```

注意：最终“是否已安装”建议在 latest 版本补齐后再做一次，因为此时才有完整的 `name + version`。

### 7.5 LibraryDownloader

下载和安装逻辑由 MCP 内部 Python helper 封装。MCP 负责传入结构化依赖列表，并返回固定结构化结果。

下载前输入应该已经是完整版本：

```json
[
  {"name": "TYMultibody", "version": "1.5.0"}
]
```

下载/安装器应具备幂等行为：

- 本地已安装：返回 `already_installed`
- 新安装：返回 `installed`
- 失败：返回 `failed`

固定输出：

```json
{
  "ok": true,
  "results": {
    "TYMultibody@1.5.0": {
      "ok": true,
      "status": "installed",
      "name": "TYMultibody",
      "version": "1.5.0",
      "target_dir": "<LibraryRoot>/TYMultibody 1.5.0",
      "uses_ini": {
        "exists": true,
        "dependencies": []
      }
    }
  }
}
```

最小稳定字段为：

```text
ok
status
name
version
target_dir
uses_ini.dependencies
```

### 7.5.1 下载后的安装流程

当前已确认：下载不能只停留在 `.tar.zst` 归档文件，还需要完成安装目录准备、校验、解压、标记文件创建、`uses.ini` 递归依赖发现和临时文件清理。

#### 7.5.1.1 安装目录规则

每个模型库版本对应一个独立安装目录：

```text
<LibraryRoot>/<模型库名> <版本号>/
```

例如：

```text
<LibraryRoot>/TYBase 1.0.8/
<LibraryRoot>/TAEconomy 1.3.2/
<LibraryRoot>/Modelica 4.0.0.TY.1/
```

`LibraryRoot` 当前来源：

```text
优先：dependency_manager(download_dir=...)
其次：环境变量 MWORKS_LIBRARY_ROOT
默认：MWORKS_INSTALL_DIR / "Library"
```

#### 7.5.1.2 已安装判断

安装前先判断目标目录是否已经存在：

```text
<LibraryRoot>/<模型库名> <版本号>/
```

如果目标目录已经存在，则该库视为已安装或已处理，当前流程不再下载、不再解压、不再覆盖。

建议返回状态：

```json
{
  "status": "already_installed",
  "reason": "target directory exists"
}
```

注意：后续如果接入 Sysplorer 官方“已安装库查询接口”，应优先使用官方接口返回的 `name + version` 集合；文件系统目录判断作为 fallback。

#### 7.5.1.3 下载与校验顺序

下载文件包括：

```text
<name>-<version>-<arch>.tar.zst
<name>-<version>-<arch>.tar.zst.sha256
```

严格顺序：

```text
1. 下载 tar.zst
2. 下载 sha256
3. 计算 tar.zst 的 sha256
4. 与 sha256 文件内容比对
5. 校验成功才允许进入解压
6. 校验失败绝不解压
```

校验失败时必须清理：

```text
删除 tar.zst
删除 sha256
返回 sha256_mismatch
```

校验成功后：

```text
删除 sha256
继续解压
```

解压成功后：

```text
删除 tar.zst
```

因此 `.tar.zst` 只是下载和解压过程中的临时缓存，不作为长期安装状态来源。长期状态以安装目录为准。

#### 7.5.1.4 解压策略

解压前需要确认目标目录不存在。目标目录存在则跳过整个安装流程。

推荐安全流程：

```text
target_dir = <LibraryRoot>/<name> <version>
tmp_dir = <LibraryRoot>/.mworks_mcp_installing/<name> <version>

如果 target_dir 存在：
  skip already_installed

否则：
  下载 tar.zst
  校验 sha256
  清理旧 tmp_dir
  创建 tmp_dir
  解压 tar.zst 到 tmp_dir
  创建 tmp_dir/MWORKSCustomLibrary.ini
  读取 tmp_dir/uses.ini
  将 tmp_dir 原子移动/改名为 target_dir
  删除 tar.zst
```

使用临时目录的原因：

- 避免解压失败时污染正式安装目录；
- 避免只创建了 `MWORKSCustomLibrary.ini` 但实际内容没解压完成时被误判为安装成功；
- 目标目录只在完整安装成功后出现。

如果由于跨磁盘或权限原因无法原子移动，则需要返回明确错误，不应留下半安装目录。

#### 7.5.1.5 `MWORKSCustomLibrary.ini`

解压完成后，需要在解压目录下创建空文件：

```text
MWORKSCustomLibrary.ini
```

文件名以此为准，注意不是 `MWORKSCustomLibraary.ini`。

该文件只需要存在，内容为空即可。

建议创建时机：

```text
解压成功后、移动到正式 target_dir 前
```

不建议在解压前创建，因为解压失败会导致目录看起来像已安装。

#### 7.5.1.6 `uses.ini` 递归依赖

解压目录中通常会包含：

```text
uses.ini
```

格式为一行一个依赖，模型库名和版本号之间用空白分隔，例如：

```text
Modelica 4.0.0.TY.1
TYBase 1.0.8
TAEconomy 1.3.2
```

解析规则：

- `uses.ini` 不包含额外注释和空行；
- 每行必须包含模型库名和版本号；
- 第一个字段作为模型库名；
- 第二个字段作为版本号；
- 如果没有版本号，该行不下载；
- 当前已确认 `uses.ini` 正常情况下都会带版本号。

解析出的依赖应继续进入同一套准备流程：

```text
检查是否已安装
  -> 未安装则下载
  -> 校验
  -> 解压安装
  -> 创建 MWORKSCustomLibrary.ini
  -> 继续读取该依赖自己的 uses.ini
```

#### 7.5.1.7 递归去重与循环保护

递归处理时必须使用 `name + version` 作为唯一 key，例如：

```text
TYBase@1.0.8
Modelica@4.0.0.TY.1
```

需要维护至少三个集合：

```text
installed_keys     已安装，跳过
processed_keys     本次流程已经处理完成，跳过
in_progress_keys   当前递归链路中正在处理，防止循环依赖
```

行为建议：

- 如果 key 在 `installed_keys` 中，返回 `already_installed`；
- 如果 key 在 `processed_keys` 中，返回 `already_processed`；
- 如果 key 在 `in_progress_keys` 中，返回 `cycle_skipped`；
- 如果下载、校验、解压任一步失败，按 `stop_on_error` 决定是否继续其他依赖。

#### 7.5.1.8 清理策略

必须清理：

- sha256 校验失败：删除 `.tar.zst` 和 `.sha256`；
- sha256 校验成功：删除 `.sha256`；
- 解压成功：删除 `.tar.zst`；
- 解压失败：删除 `.tar.zst`，并清理临时解压目录。

不应清理：

- 已经成功移动到正式安装目录的内容；
- 原本已经存在的目标目录。

#### 7.5.1.9 解压方式

最终确定使用 Python `zstandard` 库解压 `.tar.zst`，不再依赖系统 `tar`。

原因：

- 跨平台行为更可控，Windows/Linux/macOS 不需要分别判断系统 `tar` 能力；
- MCP 运行时 PATH 被裁剪时不影响解压；
- 依赖可以通过 `requirements.txt` 和打包 spec 固定；
- 代码可以在解压前后统一做安全检查、清理和结构化错误返回。

实现策略：

```text
1. 用 zstandard.ZstdDecompressor().stream_reader(...) 流式解压 zst；
2. 用 Python tarfile 读取解压后的 tar 流；
3. 逐个 tar member 做路径安全检查，禁止绝对路径和目录逃逸；
4. 暂不支持 symlink / hardlink，遇到时返回 unsupported_tar_link；
5. 解压到临时目录，完整成功后再移动到正式安装目录。
```

依赖声明：

```text
zstandard>=0.23.0
```

运行时如果缺少 `zstandard`，应返回明确错误：

```json
{
  "status": "missing_dependency",
  "error": "Python package zstandard is required to extract .tar.zst"
}
```

### 7.6 LibraryCatalogRefresher

下载完成后必须刷新 Sysplorer 软件的模型库索引，否则 `LoadLibrary` 可能看不到刚下载的库。

MCP 侧建议封装为：

```python
driver.update_library()
```

底层 API 名称已确认：

```text
UpdateLibrary
```

该接口不需要传参，下载和安装完成后调用一次，用于刷新 Sysplorer 对模型库目录的识别。

返回值已确认只有 `True` / `False`，没有具体诊断。失败时 MCP 只记录 `ok=false`，不再尝试读取详细诊断，也不做额外修复。

执行位置：

```text
download/install -> UpdateLibrary -> LoadLibrary
```

该模块属于：

```text
Sysplorer 提供刷新 API，MCP 封装调用
```

### 7.7 DependencyRepairLoop

如果前面所有步骤仍未解析出正确版本，最后可通过 `OpenModel` / `CheckModel` 的失败诊断做一次兜底修复。

当前 MCP driver 已有诊断透传能力：

- 底层 API 返回 `False` 时，driver 会调用 `GetLastErrors`
- 同时会尝试调用 `MessageText`
- 诊断文本会拼到返回 JSON 的 `error` 字段中

已确认：`CheckModel` 的缺版本诊断不一定包含模型库名和版本号。因此该能力只能作为可选兜底，不能作为主路径，也不能在提取失败时继续猜测下载。

建议将该能力定义为“可选兜底”，不要作为主路径：

```text
OpenModel / CheckModel 失败
  -> 从 error / GetLastErrors / MessageText 中尝试正则提取 name + version
  -> 如果提取到更可信版本
       -> 回到下载、刷新、LoadLibrary
       -> 最多重试一次
  -> 如果提取不到
       -> 不再下载
       -> 返回原始诊断和依赖准备结果
```

后续为了提高该能力可靠性，MCP 可以新增“完整诊断”获取路径，但行为仍应保持保守：只有解析出明确的 `name + version` 才允许进入一次 repair；解析不到就结束。

## 8. 建议新增 MCP 工具

建议新增独立工具：

```text
dependency_manager
```

用途：单独调试依赖解析、版本补全、下载、刷新、加载，不必每次都走 `model_manager(action="load_file")`。

建议 action：

| action | 行为 |
| --- | --- |
| `resolve` | 只解析依赖，不下载，不刷新，不 LoadLibrary。 |
| `plan` | 解析、合并 TOML、补版本、过滤已安装，只生成执行计划，不产生副作用。 |
| `prepare` | 按执行计划下载、刷新、LoadLibrary。是否真正执行由参数控制。 |
| `repair` | 基于检查诊断尝试提取版本并重试下载/加载。 |

建议参数：

```python
def dependency_manager(
    action: str,
    model_name: str = "",
    file_path: str = "",
    existing_config_path: str = "",
    dependency_toml_path: str = "",
    profile: str = "",
    dry_run: bool = True,
    download_missing: bool = False,
    load_after_download: bool = False,
    refresh_after_download: bool = True,
    respect_toml_install_flags: bool = True,
    stop_on_error: bool = True,
) -> str:
```

副作用控制原则：

- `resolve` 永远不下载、不刷新、不 `LoadLibrary`。
- `plan` 永远不下载、不刷新、不 `LoadLibrary`，只输出将要执行什么。
- `prepare` 只有在 `dry_run=false` 且 `download_missing=true` 时才下载缺失库。
- `prepare` 只有在 `load_after_download=true` 时才执行 `LoadLibrary`。
- `Manifest.toml` 第一版不提供 `install=false` 控制；是否下载由 `dry_run`、`download_missing` 和 `--user-workspace` 启动授权共同决定。
- 单独调用 `dependency_manager` 时默认参数应偏保守：只生成计划，不自动下载。

### 8.1 与 `model_manager` 的关系

`dependency_manager` 是依赖生命周期工具，`model_manager` 是模型生命周期工具。

推荐关系：

```text
dependency_manager
  -> resolve / plan / prepare dependencies

model_manager(action="load_file")
  -> 默认调用 dependency_manager(action="prepare")
  -> OpenModelFile
```

也就是说，`dependency_manager` 可以独立使用，用来查看依赖、生成下载计划或执行依赖准备；`model_manager(action="load_file")` 在加载模型前默认执行依赖准备。

但自动准备依赖必须有总开关，因为不同版本或不同部署形态可能不需要下载/安装依赖。建议 `model_manager(action="load_file")` 增加：

```python
prepare_dependencies: bool = True
```

当 `prepare_dependencies=false` 时，完全跳过 `GetModelDependencies`、TOML、latest、下载、解压安装、`UpdateLibrary` 这一整套新流程，仅保留原有的文件加载行为。

## 9. `model_manager(action="load_file")` 集成方式

加载模型时默认自动准备依赖，但允许通过显式开关关闭整套流程。

建议新增参数：

```python
prepare_dependencies: bool = True
resolve_deps_backend: str = "regex"
download_missing_deps: bool = True
existing_config_path: str = ""
dependency_toml_path: str = ""
dependency_profile: str = ""
dependency_dry_run: bool = False
refresh_libraries_after_download: bool = True
load_dependencies_after_download: bool = True
respect_toml_install_flags: bool = True
stop_on_dep_error: bool = False
repair_dependency_versions: bool = False
```

默认值表示“加载模型时自动准备依赖”：

```text
prepare_dependencies=true
auto_load_deps=true
resolve_deps_backend="api"
dependency_dry_run=false
download_missing_deps=true
stop_on_dep_error=false
repair_dependency_versions=false
```

禁用整套自动依赖准备流程时：

```text
model_manager(
  action="load_file",
  file_path="...",
  model_name="MyModel",
  prepare_dependencies=false
)
```

完整启用时：

```text
model_manager(
  action="load_file",
  file_path="...",
  model_name="MyModel",
  prepare_dependencies=true,
  auto_load_deps=true,
  resolve_deps_backend="api",
  dependency_dry_run=false,
  download_missing_deps=true,
  refresh_libraries_after_download=true,
  load_dependencies_after_download=true,
  stop_on_dep_error=true,
  repair_dependency_versions=true
)
```

## 10. 返回结构建议

`dependency_manager(action="prepare")` 或 `model_manager(action="load_file")` 建议返回分阶段信息：

```json
{
  "dependency_prepare": {
    "ok": true,
    "resolve": {
      "api": "GetModelDependencies",
      "dependencies": []
    },
    "toml_merge": {
      "used": true,
      "path": "Manifest.toml"
    },
    "installed": {
      "source": "sysplorer_api",
      "items": []
    },
    "latest": {
      "queried": []
    },
    "download": {
      "results": {}
    },
    "refresh": {
      "api": "UpdateLibrary",
      "ok": true
    },
    "load": {
      "results": {}
    },
    "repair": {
      "attempted": false
    }
  }
}
```

## 11. 错误处理建议

推荐失败策略：

- 如果 `GetModelDependencies` 不存在，返回明确错误；是否 fallback 到当前 `_extract_dep_libs` 正则解析应由调用方显式配置。
- 如果 TOML 不存在，不作为错误，只记录 `used=false`。
- 如果 TOML 格式错误，应返回 warning 或 error，具体取决于 `stop_on_error`。
- 如果 latest 查询失败且依赖仍无版本，不能下载该依赖，应返回明确错误。
- 如果下载失败且 `stop_on_error=true`，不继续刷新和 `LoadLibrary`。
- 如果刷新库索引失败且 `stop_on_error=true`，不继续 `LoadLibrary`。
- 如果 `LoadLibrary` / `CheckModel` 失败且 `repair_dependency_versions=true`，允许进入一次诊断修复。
- 诊断修复只有在明确解析出 `name + version` 时才下载并重试。
- 如果诊断中没有解析出库名和版本号，则不再下载，直接返回原始诊断和依赖准备结果。
- 诊断修复最多重试一次，避免无限循环。

## 12. 实施步骤

当前已确认并已先行实现的部分：

1. 在 `MWorksDriver` 中注册 `GetModelDependencies`。
2. 新增 `MWorksDriver.get_model_dependencies(...)`，只调用正式 API。
3. 在 `MWorksDriver` 中注册并封装 `GetInstalledLibraries()`，返回 `[{"name": "...", "version": "...", "is_load": ...}]`。
4. 新增依赖结果和已安装库结果归一化 helper。
5. 基于 `d:\git\TongYuan\work\find_library\list_modelica_storage.py` 的逻辑，新增远端 latest 查询与 tar.zst 下载 helper。
6. 新增 Python `zstandard` 解压安装流程：下载、sha256 校验、解压到临时目录、创建 `MWORKSCustomLibrary.ini`、读取 `uses.ini`、移动到正式目录、递归安装 uses 依赖。
7. 新增 `dependency_manager` MCP 工具，支持 `resolve`、`latest`、`plan`、`download`、`prepare`、`repair` action。
8. `dependency_manager` 默认无副作用；只有 `dry_run=false` 且 `download_missing=true` 时才真正下载并安装。
9. 刷新库索引接口已确认名称为 `UpdateLibrary`，已在 driver 层封装并接入下载成功后的 prepare/download 流程。
10. `model_manager(action="load_file")` 已默认自动接入 `dependency_manager(action="prepare")`。
11. 已设计并实现总开关 `prepare_dependencies`，用于按版本或部署场景关闭整套自动依赖准备流程。

仍遗留、等待确认后再实现的部分：

1. 基于 `OpenModel` / `CheckModel` 诊断提取版本号的正则规则；解析不到时不再下载。
2. 真实 Sysplorer 新包和真实远端仓库的端到端集成测试。

## 13. 测试建议

至少覆盖：

- `GetModelDependencies` 存在时调用正式接口；
- `GetModelDependencies` 不存在时返回明确错误；
- Manifest 版本覆盖 API 版本；
- API 和 Manifest 都无版本时查询 remote latest；
- latest 补全后，调用 `GetInstalledLibraries()`，与已安装库做 `name + version` 去重；
- `GetInstalledLibraries()` 返回的已安装库在 plan 阶段标记为 `skip / already_installed`；
- `uses.ini` 递归依赖也复用 `GetInstalledLibraries()` 的 installed set 去重；
- `GetInstalledLibraries()` 失败时按 `stop_on_error` 策略返回错误或降级 warning；
- 下载器对已安装库返回 skipped / already_installed；
- 下载和安装成功后调用 `UpdateLibrary`；
- `UpdateLibrary` 后再调用 `LoadLibrary`；
- `UpdateLibrary` 返回 `False` 时只记录刷新失败，不尝试获取详细诊断；
- `model_manager(action="load_file")` 默认先执行依赖准备，再执行 `OpenModelFile`；
- `prepare_dependencies=false` 时跳过 `GetModelDependencies`、TOML、latest、下载、解压安装和 `UpdateLibrary`；
- `CheckModel` / `LoadLibrary` 失败诊断中提取到 `name + version` 时，触发一次 repair；
- 诊断中提取不到 `name + version` 时，不下载，直接返回诊断；
- repair 后仍失败时返回完整阶段结果，不无限重试；
- `prepare_dependencies=false` 时仍保持现有 `auto_load_deps=true` 的正则预加载行为。

## 14. 待确认问题

1. TOML 文件名、路径和字段结构最终是否采用本文建议格式？
2. `prepare_dependencies` 是否需要支持按 Sysplorer 版本、产品版本或配置文件默认开关？

## 15. 推荐方向

优先采用 MCP 内部 Python helper 封装 HTTP 下载、sha256 校验、`zstandard` 解压安装和 `uses.ini` 递归依赖处理，把 Sysplorer 相关能力限制在：

- 模型依赖发现；
- `GetModelDependencies(modelName)` 依赖解析；
- `GetInstalledLibraries()` 已安装库查询和下载前去重；
- 下载后 `UpdateLibrary` 刷新库索引；
- 模型库加载；
- 模型打开和检查。

MCP Server 负责：

- 编排完整流程；
- 合并版本来源；
- 只读 TOML；
- 调用 latest、下载、校验、解压安装；
- 输出结构化 JSON；
- 实现 fallback 和保守的一次性 repair retry：只有解析出明确 `name + version` 才下载，解析不到则不下载。
