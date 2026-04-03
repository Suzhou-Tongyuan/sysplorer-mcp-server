# sysplorer-mcp-server
---
&nbsp;

`sysplorer-mcp-server` 是面向 MCP 协议的 Sysplorer API 服务化能力封装层。它将 Sysplorer 中的关键对象与关键能力，以标准化方式开放给 AI 客户端。装备工程智能体、企业 AI 助手，以及 Claude、Opencode、Codex 等通用 AI 客户端，都可以通过 MCP 协议连接 Sysplorer，读取系统模型上下文，并在授权范围内调用 Sysplorer 相关能力。

`Sysplorer MCP Server` 的核心作用，是把原本依赖本地软件环境才能完成的模型操作和知识检索能力，以 MCP 工具的形式开放给客户端调用。

## 系统要求

- Windows 10/11 64 位；具备使用大模型能力的 Linux 系统，例如 CentOS 8、Ubuntu 20.04及以上
- 已安装 Sysplorer V26.2.0 版本

## 安装方式

安装 Sysplorer 时会自动安装 Sysplorer MCP Server，默认给Claude code、OpenCode、Codex 三 类 agent 配置。如果失败可以参考以下方式手动执行。

当需要手动安装 sysplorer mcp 服务时，可以通过“<Sysplorer安装目录>/Tools/sysplorer_mcp”内的 “install_mcp.ps1” 一键安装 Windows Sysplorer MCP Server、“install_mcp.sh” 一键安装 Linux Sysplorer MCP Server。

下文以 Windows 为例：
1. 在 “<Sysplorer安装目录>/Tools/sysplorer_mcp” 内右键 “install_mcp.ps1”安装脚本选择“通过 PowerShell 运行”或在当前目录启动 PowserShell 后执行执行如下命令：

```powershell
.\install_mcp.ps1
```

2. 按提示输入 Sysplorer 安装路径以及平台标签，具体信息如下

| 项 | 含义 | 典型示例 |
|----|------|----------|
| **Sysplorer 安装路径** | 写入各客户端配置，并作为 MCP 进程参数 `--mworks-install-dir` | `C:\Program Files\MWORKS\Sysplorer 2026a` |
| **Sysplorer 平台标签** | 参数 `--sysplorer-platform-label`，用于标识平台/版本展示 | `Sysplorer 2026a` |

脚本会校验路径下是否存在 **`External\python64\python.exe`**；MCP 实际由该解释器执行本目录中的 **`main.py`** 启动。

Python 与依赖环境说明

- **解释器**：必须使用 **当前所选 Sysplorer 安装目录** 下的 `External\python64\python.exe`，以保证与 `mworks.sysplorer` 等接口一致。如需使用自定义Python，请确保安装了 Sysplorer Python API 及 MCP 库。

- **Python 包**：服务端依赖 **`mcp`** 以及 **`fastmcp`、`anyio`** 等（与仓库 `sysplorer-mcp-server` 要求一致）。安装脚本在写配置结束后会执行一次 **`python.exe -m pip list`**，检查是否存在名为 **`mcp`** 的包；若缺失，会提示使用 **PowerShell** 下正确的调用方式安装（路径含空格时必须使用 **`&`**）：

  ```powershell
  & "C:\你的\Sysplorer\根目录\External\python64\python.exe" -m pip install mcp
  ```

- 在 **PowerShell** 中切勿仅输入 `"...\python.exe" -m pip ...`（会被解析为字符串而非启动程序），必须使用 **`& "路径\python.exe" -m pip ...`**。

3. 脚本会自动将 MCP 配置添加到 Claude、OpenCode、Codex 的配置文件中
4. 重启 Claude Code / OpenCode / Codex 客户端即可使用

如果一键部署脚本运行失败，也可以手动配置。

#### Claude Code（JSON）

- **文件**：`%USERPROFILE%\.claude.json`  
- **节点**：`mcpServers.sysplorer_mcp`  
- **本包（Python 布局）典型形态**：  
  - `command`：`Sysplorer` 的 `External\python64\python.exe` 绝对路径  
  - `args`：`["<本包main.py绝对路径>", "--mworks-install-dir", "<Sysplorer根目录>", "--sysplorer-platform-label", "<标签>"]`

#### OpenCode（JSON）
- **文件**：`%USERPROFILE%\.config\opencode\opencode.json`  
- **节点**：`mcp.sysplorer_mcp`  
- **字段**：`type` 一般为 `local`；`command` 为数组，首元素为 `python.exe`，其后为 `main.py` 路径及与上相同的参数。

#### Codex（TOML）
- **文件**：`%USERPROFILE%\.codex\config.toml`  
- **节名**：`[mcp_servers.sysplorer_mcp]`  
- **字段**：`command` 指向 `python.exe`；`args` 为多行字符串数组，内容顺序与 Claude 侧 `args` 一致。

## MCP Tools

Sysplorer MCP Server 共提供 13 个工具，覆盖 Sysplorer 的启动、建模到仿真全流程，工具能力可以按用途分为以下几类。

### 1. 会话与连接

<table>
  <colgroup>
    <col style="width: 34%;" />
    <col style="width: 18%;" />
    <col style="width: 48%;" />
  </colgroup>
  <thead>
    <tr>
      <th>工具英文名</th>
      <th>工具中文描述</th>
      <th>工具具体功能描述</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>mworks_sysplorer_session_manager</code></td>
      <td>会话管理工具</td>
      <td>用于启动、连接、探测、重连和关闭 Sysplorer 会话，是所有后续工具调用的基础入口。</td>
    </tr>
  </tbody>
</table>

### 2. 建模全流程工具

<table>
  <colgroup>
    <col style="width: 34%;" />
    <col style="width: 18%;" />
    <col style="width: 48%;" />
  </colgroup>
  <thead>
    <tr>
      <th>工具英文名</th>
      <th>工具中文描述</th>
      <th>工具具体功能描述</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>mworks_sysplorer_load_library</code></td>
      <td>库加载工具</td>
      <td>用于加载 Modelica 标准库或商业库，为后续打开模型、查询类文档和仿真准备运行环境。</td>
    </tr>
    <tr>
      <td><code>mworks_sysplorer_model_manager</code></td>
      <td>模型管理工具</td>
      <td>用于执行模型打开、新建、加载文件、卸载、保存、导出原理图，以及组件、端口和类文本等内省查询。</td>
    </tr>
    <tr>
      <td><code>mworks_sysplorer_check_model</code></td>
      <td>模型检查工具</td>
      <td>用于对一个或多个模型执行实例化和编译检查，可结合 Smart Layout 写回与重载流程做建模前校验。</td>
    </tr>
    <tr>
      <td><code>mworks_sysplorer_translate_model</code></td>
      <td>模型翻译工具</td>
      <td>用于调用 TranslateModel 完成代码生成与翻译流程，可用于生成仿真代码或后续部署所需的中间结果。</td>
    </tr>
    <tr>
      <td><code>mworks_sysplorer_simulate_model</code></td>
      <td>模型仿真工具</td>
      <td>用于执行自动、独立或实时仿真，并在仿真后校验结果变量是否可读取，是模型运行阶段的核心入口。</td>
    </tr>
          <tr>
      <td><code>mworks_sysplorer_smart_layout</code></td>
      <td>自动布局工具</td>
      <td>用于计算布局、整合生成结果并将 Placement 和连线信息写回系统级 <code>.mo</code> 文件，适合自动建模后的版式整理。</td>
    </tr>
  </tbody>
</table>


### 3. 脚本与自动化

<table>
  <colgroup>
    <col style="width: 34%;" />
    <col style="width: 18%;" />
    <col style="width: 48%;" />
  </colgroup>
  <thead>
    <tr>
      <th>工具英文名</th>
      <th>工具中文描述</th>
      <th>工具具体功能描述</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>mworks_sysplorer_call_code</code></td>
      <td>脚本调用工具</td>
      <td>用于执行 <code>run_script</code>、异步任务、就绪分派和 CAD 工具箱等能力，其中 <code>mode=&quot;run_script&quot;</code> 是 Sysblock 程序化建图和脚本化操作的重要入口。</td>
    </tr>
  </tbody>
</table>


### 4. 文档与资源检索

<table>
  <colgroup>
    <col style="width: 34%;" />
    <col style="width: 18%;" />
    <col style="width: 48%;" />
  </colgroup>
  <thead>
    <tr>
      <th>工具英文名</th>
      <th>工具中文描述</th>
      <th>工具具体功能描述</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>mworks_sysplorer_resources_retrieval</code></td>
      <td>资源检索工具</td>
      <td>用于检索 <code>resources/</code> 中的规则、案例和语料，适合查询流程建议、选型经验、排障知识和示例资料。</td>
    </tr>
    <tr>
      <td><code>mworks_sysplorer_get_api_document</code></td>
      <td>接口文档工具</td>
      <td>用于查询 Sysplorer Python API 的帮助说明，适合确认命令名、参数含义和官方接口用法。</td>
    </tr>
    <tr>
      <td><code>mworks_sysplorer_get_lib_model_document</code></td>
      <td>模型库文档工具</td>
      <td>用于查询已加载库模型类的真实说明、参数、端口和导出文档内容，适合核对组件级上下文。</td>
    </tr>
  </tbody>
</table>

### 5. 结果与可视化

<table>
  <colgroup>
    <col style="width: 34%;" />
    <col style="width: 18%;" />
    <col style="width: 48%;" />
  </colgroup>
  <thead>
    <tr>
      <th>工具英文名</th>
      <th>工具中文描述</th>
      <th>工具具体功能描述</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>mworks_sysplorer_result_manager</code></td>
      <td>结果读取工具</td>
      <td>用于打开结果文件、列出变量、读取时序数据、读取指定时刻值以及获取时间轴信息。</td>
    </tr>
    <tr>
      <td><code>mworks_sysplorer_plot_manager</code></td>
      <td>绘图动画工具</td>
      <td>用于在 Sysplorer 中执行结果绘图与动画创建，支持变量可视化和动态展示。</td>
    </tr>
  </tbody>
</table>

## 许可证

本项目采用 MIT 许可证授权，有关详细信息，请参阅 [LICENSE](https://mohub.net/mcp/26004/file/%E6%9C%80%E6%96%B0/blob/LICENSE) 文件。 
