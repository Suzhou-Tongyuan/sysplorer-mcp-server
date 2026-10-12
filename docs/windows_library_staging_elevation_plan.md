# Windows 模型库 Staging 与提权安装方案

## 1. 背景

当前模型库自动下载流程会把 `.tar.zst` 下载、校验、解压和安装都放在 Sysplorer 安装目录的 `Library` 下。

如果 Sysplorer 安装在 Windows 受保护目录，例如：

```text
C:\Program Files\MWORKS\...\Library
```

普通权限启动的 MCP 进程通常没有写权限，可能在以下阶段失败：

- 写入 `.tar.zst`
- 写入 `.sha256`
- 创建临时解压目录
- 解压文件
- 创建 `MWORKSCustomLibrary.ini`
- 删除下载文件
- 移动临时目录到正式库目录

因此需要把“下载解压准备”和“写入 Sysplorer Library”拆开。

## 2. 目标

第一版只考虑 Windows。

目标流程：

```text
普通权限 MCP
  -> 下载到用户可写 staging 目录
  -> 校验 sha256
  -> 解压到 staging 目录
  -> 创建 MWORKSCustomLibrary.ini
  -> 解析 uses.ini
  -> 生成安装 manifest
  -> 检查 Sysplorer Library 是否可写
      -> 可写：MCP 直接提交安装
      -> 不可写：调用 Windows 提权 install-helper.exe
  -> UpdateLibrary
  -> LoadLibrary / CheckModel
```

## 3. 推荐 Staging 目录

Windows 默认 staging 根目录：

```text
%LOCALAPPDATA%\MWORKS\sysplorer-mcp-server\library-staging
```

典型展开：

```text
C:\Users\<用户名>\AppData\Local\MWORKS\sysplorer-mcp-server\library-staging
```

该目录属于当前用户配置区域，正常情况下当前用户可写。但代码仍必须做 preflight，不应盲信。

每次安装使用一个 transaction 子目录：

```text
library-staging\
  install-20260710-153000-8f3a2c\
    downloads\
      TYDriveline-2.1.0-noarch.tar.zst
      TYDriveline-2.1.0-noarch.tar.zst.sha256
    packages\
      TYDriveline 2.1.0\
        uses.ini
        MWORKSCustomLibrary.ini
    manifest.json
    result.json
```

transaction 目录只作为临时工作区。一次依赖准备结束后，无论提交到 `Library` 成功还是失败，MCP 都应删除整个 transaction 目录，避免大型模型库长期占用用户磁盘。

### 3.1 Staging preflight

下载前检查：

```text
1. 创建 staging 根目录
2. 创建 transaction 目录
3. 写入测试文件
4. 删除测试文件
5. 创建测试子目录
6. 删除测试子目录
```

失败则直接返回：

```json
{
  "ok": false,
  "stage": "staging_preflight",
  "error": "staging directory is not writable",
  "staging_root": "..."
}
```

## 4. Library 安装根目录

最终安装目录仍然是：

```text
<SysplorerInstallDir>\Library
```

每个模型库最终目录：

```text
<SysplorerInstallDir>\Library\<库名> <版本号>
```

示例：

```text
C:\Program Files\MWORKS\...\Library\TYDriveline 2.1.0
```

## 5. 安装提交策略

### 5.1 先检查 Library 是否可写

安装提交前，MCP 检查：

```text
<LibraryRoot>\.mcp_write_test_<随机>
<LibraryRoot>\.mcp_write_test_dir_<随机>
```

需要验证：

- 能创建文件
- 能删除文件
- 能创建目录
- 能删除目录

如果可写，MCP 直接提交安装，不需要提权 helper。

如果不可写，返回 `needs_elevation=true`，并走提权 helper。

### 5.2 可写时直接提交

直接提交也不要把包目录直接复制到正式目录。

推荐流程：

```text
source = <staging>\packages\<name> <version>
tmp_target = <LibraryRoot>\.mworks_mcp_installing\<name> <version>
target = <LibraryRoot>\<name> <version>

如果 target 已存在：
  返回 already_installed

复制 source 到 tmp_target
复制完成后 rename tmp_target -> target
```

好处：

- 避免 Sysplorer 看到半成品目录；
- 拷贝失败时可以清理 `.mworks_mcp_installing`；
- 正式目录只在安装完成后出现。

## 6. Windows 提权 Helper

### 6.1 UAC 是什么

UAC 是 Windows 的用户账户控制。

当普通权限进程需要执行管理员操作时，Windows 可以弹出确认窗口：

```text
是否允许此应用对你的设备进行更改？
```

用户确认后，指定程序以管理员权限运行。

本方案中，不提权 MCP 本体，也不提权 host，只提权一个功能很窄的安装 helper。

### 6.2 Helper 来源

`install-helper.exe` 需要由本项目提供，不是系统自带程序。

第一版建议：

```text
install/helpers/install_library_helper.py
```

再通过 PyInstaller 打包为：

```text
install-helper.exe
```

后续正式发行时，helper 应随 MCP Server 一起打包和分发。

### 6.3 Helper 启动方式

当 Library 不可写时，MCP 在 Windows 上启动：

```powershell
Start-Process install-helper.exe -Verb RunAs -ArgumentList "--manifest <manifest.json>" -Wait
```

`-Verb RunAs` 会触发 UAC。

用户点击确认后：

```text
install-helper.exe
  -> 以管理员权限运行
  -> 读取 manifest.json
  -> 把 staging packages 复制到 Library
  -> 写 result.json
```

MCP 等 helper 退出后读取 `result.json`。

## 7. Manifest 设计

MCP 不应让 helper 接收任意 source/target 参数，避免 helper 变成管理员权限的任意复制工具。

helper 只接收 manifest：

```json
{
  "schema_version": 1,
  "operation": "install_model_libraries",
  "staging_root": "C:\\Users\\me\\AppData\\Local\\MWORKS\\sysplorer-mcp-server\\library-staging\\install-...",
  "install_root": "C:\\Program Files\\MWORKS\\...\\Library",
  "packages": [
    {
      "name": "TYDriveline",
      "version": "2.1.0",
      "source_dir": "C:\\Users\\me\\...\\packages\\TYDriveline 2.1.0",
      "target_dir": "C:\\Program Files\\MWORKS\\...\\Library\\TYDriveline 2.1.0"
    }
  ],
  "result_path": "C:\\Users\\me\\...\\result.json"
}
```

## 8. Helper 安全校验

helper 必须做严格校验。

允许：

- 只执行 `install_model_libraries`
- 只从 `staging_root` 下读取包目录
- 只写入 `install_root` 下的目标目录
- 目标目录名必须等于 `<name> <version>`
- 目标已存在时默认跳过
- 使用 `.mworks_mcp_installing` 作为临时目标目录

禁止：

- 执行任意命令
- 复制任意路径
- 删除任意路径
- 覆盖已存在正式库目录
- 接受包含 `..`、盘符跳转、路径分隔符注入的库名或版本
- 跟随 source 包目录中的符号链接或 junction

路径校验规则：

```text
resolved(source_dir) 必须位于 resolved(staging_root) 下
resolved(target_dir) 必须位于 resolved(install_root) 下
basename(target_dir) 必须等于 "<name> <version>"
```

## 9. MCP 侧代码改造

当前 `install_package(...)` 需要拆成两个阶段。

### 9.1 阶段一：prepare/stage

新增或改造 helper：

```python
stage_package(
    name: str,
    version: str,
    staging_root: Path,
) -> dict
```

职责：

```text
1. 解析下载 URL
2. 下载 tar.zst 到 staging/downloads
3. 下载 sha256 到 staging/downloads
4. 校验 sha256
5. 解压到 staging/packages/<name> <version>
6. 创建 MWORKSCustomLibrary.ini
7. 读取 uses.ini
8. 删除 tar.zst 和 sha256
9. 返回 staged package 信息
```

### 9.2 阶段二：submit/install

新增 helper：

```python
submit_staged_packages(
    staged_packages: list[dict],
    install_root: Path,
    allow_elevation: bool = True,
) -> dict
```

职责：

```text
1. 检查 install_root 是否可写
2. 可写则直接复制提交
3. 不可写且 allow_elevation=true，则生成 manifest 并调用 install-helper.exe
4. 不可写且 allow_elevation=false，则返回 needs_elevation
5. 返回每个 package 的安装结果
```

批量依赖准备时，MCP 应先完成所有可安装依赖的 staging，再一次性调用 `submit_staged_packages([...])`。因此一次依赖准备最多生成一个安装 manifest，最多触发一次 `install-helper.exe` / UAC。不要每下载一个库就调用一次 helper。

提交结束后必须清理 staging transaction。清理失败需要写入返回 JSON 的 `staging_cleanup` 字段，不能静默吞掉。

返回示例：

```json
{
  "ok": true,
  "stage": "submit",
  "install_root": "C:\\Program Files\\MWORKS\\...\\Library",
  "elevation": {
    "needed": true,
    "used": true,
    "method": "windows_uac_helper"
  },
  "results": {
    "TYDriveline@2.1.0": {
      "ok": true,
      "status": "installed",
      "target_dir": "..."
    }
  }
}
```

权限不足且未允许提权：

```json
{
  "ok": false,
  "stage": "submit",
  "needs_elevation": true,
  "install_root": "C:\\Program Files\\MWORKS\\...\\Library",
  "error": "install root is not writable"
}
```

## 10. dependency_manager 参数建议

建议新增或明确以下参数：

```python
staging_root: str = ""
install_root: str = ""
allow_elevation: bool = True
elevation_mode: str = "auto"
```

含义：

- `staging_root`：用户可写 staging 根目录；空值时使用 `%LOCALAPPDATA%\MWORKS\sysplorer-mcp-server\library-staging`
- `install_root`：最终 Sysplorer `Library` 根目录；空值时使用当前 `MWORKS_LIBRARY_ROOT`
- `allow_elevation`：Library 不可写时是否允许调用 helper
- `elevation_mode`：
  - `auto`：可写则直接安装，不可写则 helper
  - `never`：不可写直接返回 `needs_elevation`
  - `require`：强制走 helper

第一版建议默认：

```python
allow_elevation = True
elevation_mode = "auto"
```

## 11. 与 Codex/AI 权限确认的关系

Codex 或其他 MCP host 的工具确认，不等同于 Windows 管理员权限。

```text
Host 工具确认：
  允许 AI 调用某个 MCP tool

Windows UAC：
  允许某个进程以管理员权限修改系统目录
```

即使用户在 host 中允许调用 `dependency_manager`，MCP 普通进程仍然不能写入：

```text
C:\Program Files\...
```

因此最终写入 `Library` 时，如果当前 MCP 进程不可写，仍需要 UAC helper。

## 12. 用户体验

推荐用户看到的行为：

```text
1. AI/MCP 先输出将安装哪些库
2. 用户确认或工具参数允许下载
3. MCP 下载、校验、解压到用户 staging
4. MCP 发现 Sysplorer Library 需要管理员权限
5. Windows 弹出 UAC
6. 用户确认
7. helper 安装模型库
8. MCP 调用 UpdateLibrary
9. MCP 继续 LoadLibrary / CheckModel
```

如果用户取消 UAC：

```json
{
  "ok": false,
  "stage": "elevated_install",
  "cancelled": true,
  "error": "user cancelled elevation"
}
```

## 13. 测试建议

至少覆盖：

- staging 目录可写 preflight 成功；
- staging 目录不可写时返回明确错误；
- Library 可写时不调用 helper，直接安装；
- Library 不可写时返回 `needs_elevation=true`；
- Library 不可写且 `allow_elevation=true` 时调用 helper；
- helper 拒绝 source 不在 staging 下的 manifest；
- helper 拒绝 target 不在 install_root 下的 manifest；
- helper 拒绝覆盖已存在目录；
- helper 安装成功后 `UpdateLibrary` 被调用；
- 用户取消 UAC 时返回结构化错误；
- 下载失败、校验失败、解压失败均不污染 Library。

## 14. 当前结论

第一版 Windows 推荐方案：

```text
下载、校验、解压、uses.ini 递归解析：
  普通权限，在用户 staging 目录完成

最终写入 Sysplorer Library：
  可写则 MCP 直接提交
  不可写则调用受限 install-helper.exe，通过 UAC 提权
```

不推荐：

```text
要求整个 host 管理员启动
```

原因：

- 用户体验差；
- host / MCP / AI 工具链整体权限过大；
- 用户同意安装模型库，不等于同意 AI 以管理员权限执行其他操作；
- 只对最终安装提交动作提权更符合最小权限原则。

## 15. 当前实施状态

已在 MCP 代码中落地的部分：

- 新增 Windows 默认 staging 根目录解析；
- 新增 staging preflight；
- 新增 `stage_package(...)`，负责下载、sha256 校验、解压、创建 `MWORKSCustomLibrary.ini` 和解析 `uses.ini`；
- 新增 `submit_staged_packages(...)`，负责检查 Library 是否可写；
- Library 可写时，MCP 直接从 staging 复制到 `<LibraryRoot>/<name> <version>`；
- Library 不可写时，生成 `manifest.json`，并按 Windows UAC helper 协议调用安装 helper；
- 安装提交结束后清理 staging transaction，成功失败都清理；
- 新增 helper 源码 `install/helpers/install_library_helper.py`；
- `dependency_manager`、`model_manager(action="load_file")` 和 `run_with_ready(action="load_file")` 已透传 staging / elevation 相关参数。

仍需发布侧完成的部分：

- 将 `install/helpers/install_library_helper.py` 打包为 `install-helper.exe`；
- 在 MCP 安装包中随带 `install-helper.exe`；
- 确认 `install-helper.exe` 的最终部署路径，或通过 `MCP_INSTALL_HELPER_EXE` 指定；
- 在真实 `C:\Program Files\MWORKS\...\Library` 权限不足场景下做 UAC 端到端测试。
