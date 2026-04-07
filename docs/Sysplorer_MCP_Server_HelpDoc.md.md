# Sysplorer MCP Server
`Sysplorer MCP Server` 是面向 MCP 协议的 Sysplorer API 服务化能力封装层。它将 Sysplorer 中的关键对象与关键能力，以标准化方式开放给 AI 客户端。装备工程智能体、企业 AI 助手，以及 Claude、Opencode、Codex 等通用 AI 客户端，都可以通过 MCP 协议连接 Sysplorer，读取系统模型上下文，并在授权范围内调用 Sysplorer 相关能力。

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

| 项                     | 含义                                                         | 典型示例                                  |
| ---------------------- | ------------------------------------------------------------ | ----------------------------------------- |
| **Sysplorer 安装路径** | 写入各客户端配置，并作为 MCP 进程参数 `--mworks-install-dir` | `C:\Program Files\MWORKS\Sysplorer 2026a` |
| **Sysplorer 平台标签** | 参数 `--sysplorer-platform-label`，用于标识平台/版本展示     | `Sysplorer 2026a`                         |

脚本会校验路径下是否存在 **`External\python64\python.exe`**；MCP 实际由该解释器执行本目录中的 **`main.py`** 启动。

Python 与依赖环境说明

- **解释器**：必须使用 **当前所选 Sysplorer 安装目录** 下的 `External\python64\python.exe`，以保证与 `mworks.sysplorer` 等接口一致。如需使用自定义Python，请确保安装了 Sysplorer Python API 及 MCP 库。

- **Python 包**：服务端依赖 **`mcp`** 以及 **`fastmcp`、`anyio`** 等（与仓库 `mworks_mcp_server` 要求一致）。安装脚本在写配置结束后会执行一次 **`python.exe -m pip list`**，检查是否存在名为 **`mcp`** 的包；若缺失，会提示使用 **PowerShell** 下正确的调用方式安装（路径含空格时必须使用 **`&`**）：

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
      <td><code>session_manager</code></td>
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
        <td><code>load_library</code></td>
        <td>库加载工具</td>
        <td>用于加载 Modelica 标准库或商业库，为后续打开模型、查询类文档和仿真准备运行环境。</td>
      </tr>
      <tr>
        <td><code>model_manager</code></td>
        <td>模型管理工具</td>
        <td>用于执行模型打开、新建、加载文件、卸载、保存、导出原理图，以及组件、端口和类文本等内省查询。</td>
      </tr>
      <tr>
        <td><code>check_model</code></td>
        <td>模型检查工具</td>
        <td>用于对一个或多个模型执行实例化和编译检查，可结合 Smart Layout 写回与重载流程做建模前校验。</td>
      </tr>
      <tr>
        <td><code>translate_model</code></td>
        <td>模型翻译工具</td>
        <td>用于调用 TranslateModel 完成代码生成与翻译流程，可用于生成仿真代码或后续部署所需的中间结果。</td>
      </tr>
      <tr>
        <td><code>simulate_model</code></td>
        <td>模型仿真工具</td>
        <td>用于执行自动、独立或实时仿真，并在仿真后校验结果变量是否可读取，是模型运行阶段的核心入口。</td>
      </tr>
            <tr>
        <td><code>smart_layout</code></td>
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
        <td><code>call_code</code></td>
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
        <td><code>resources_retrieval</code></td>
        <td>资源检索工具</td>
        <td>用于检索 <code>resources/</code> 中的规则、案例和语料，适合查询流程建议、选型经验、排障知识和示例资料。</td>
      </tr>
      <tr>
        <td><code>get_api_document</code></td>
        <td>接口文档工具</td>
        <td>用于查询 Sysplorer Python API 的帮助说明，适合确认命令名、参数含义和官方接口用法。</td>
      </tr>
      <tr>
        <td><code>get_lib_model_document</code></td>
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
        <td><code>result_manager</code></td>
        <td>结果读取工具</td>
        <td>用于打开结果文件、列出变量、读取时序数据、读取指定时刻值以及获取时间轴信息。</td>
      </tr>
      <tr>
        <td><code>plot_manager</code></td>
        <td>绘图动画工具</td>
        <td>用于在 Sysplorer 中执行结果绘图与动画创建，支持变量可视化和动态展示。</td>
      </tr>
    </tbody>
  </table>

  ## 

## 示例 1：一维机械传动系统构建

下面给出一个适合直接提交给 AI 客户端的示例提示词，构建一个一维机械传动系统。实际使用时，也可以先用自然语言概述需求，再让 AI 将其整理为类似的结构化提示。

**输入提示词示例：**

1. **背景说明**  
请在 `MWORKS.Sysplorer` 中使用同元商业机械库 `TYMechanics`，构建一个单输入、包含齿轮减速环节和弹性连接环节的一维机械传动系统，并完成动力学建模、模型检查和仿真分析。

2. **建模要求**  
必须使用 `TYMechanics` 库中的相关组件完成建模，模型中至少包含以下部件：
   - 定轴转动驱动源
   - 理想齿轮副
   - 扭转弹簧
   - 扭转阻尼
   - 转动惯量负载
   - 固定支座
   - 转速 / 扭矩传感器
   - 角度传感器

3. **系统结构要求**  
请按照以下拓扑关系构建模型：
   - 驱动端采用恒定转速输入，输入角速度为 `100 rad/s`
   - 传动级采用理想齿轮副，减速比为 `i = 2:1`
   - 齿轮输出端后串联扭转弹簧和扭转阻尼，用于表征传动链柔性与阻尼特性
   - 负载端采用纯转动惯量负载
   - 系统包含全局固定支撑

4. **参数设置**  
请使用以下参数完成模型参数化：
   - 齿轮传动比：`i = 2`
   - 扭转弹簧刚度：`k = 100 N·m/rad`
   - 扭转阻尼系数：`c = 5 N·m·s/rad`
   - 负载转动惯量：`J = 0.1 kg·m²`

5. **仿真任务**  
   请对模型进行仿真，仿真时间范围为 `0 ~ 3 s`，并至少输出以下结果曲线：
   - 驱动端转速
   - 负载端转速
   - 弹簧扭矩
   - 负载角位移

输出结果图片：

<img :src="$withBase('/Example/picture1.png')" style="width:1000px; border:1px solid black;">

AI 生成模型：<helpButton isLink exampleUrl="mworks://ref/../SysplorerAI/Samples/ExampleFile/RotationalDriveSystem.mo">RotationalDriveSystem.mo</helpButton>。

## 示例 2：机电耦合位置控制系统建模

下面给出一个适合直接提交给 AI 客户端的示例提示词。实际使用时，也可以先用自然语言概述需求，再让 AI 将其整理为类似的结构化提示。

**输入提示词示例：**

1. **背景说明**  
请在 `MWORKS.Sysplorer` 中完成一个伺服电机驱动的机电耦合位置控制系统建模与仿真。模型应包含电气驱动、电机、齿轮传动、弹性负载及控制闭环，并完成位置控制性能分析。

2. **建模要求**  
必须使用同元商业库中的相关组件完成建模，至少涉及以下库：
   - `TYElectrical` 电气库
   - `TYMotor` 电机模型库
   - `TYMechanics` 机械库

    请先完成系统方案设计，再进行模型搭建；如对组件选择、参数含义或连接方式存在疑问，可结合资源目录中的资料进行查询。

3. **系统结构要求**  
请构建一个“伺服电机 - 齿轮减速 - 弹性负载”的闭环位置控制系统，至少包含以下部分：
   - 电机电枢回路及驱动部分
   - 伺服电机本体
   - 齿轮减速机构
   - 扭转弹簧与阻尼构成的柔性连接环节
   - 负载惯量
   - 位置反馈与 PID 控制器

4. **参数设置**  
请使用以下参数完成模型参数化：
   - 电机电枢电阻、电感：采用典型小惯性伺服电机参数
   - 齿轮减速比：`i = 3`
   - 扭转弹簧刚度：`k = 80 N·m/rad`
   - 阻尼系数：`c = 4 N·m·s/rad`
   - 负载惯量：`J = 0.2 kg·m²`
   - 给定位置输入：阶跃信号 `1 rad`

5. **仿真任务**  
请搭建完整的机电耦合闭环位置控制系统，并整定 PID 参数，使系统尽量满足以下性能目标：
   - 无稳态误差
   - 超调较小
   - 响应快速且稳定

    仿真时请至少观测并输出以下结果：
   - 负载位置响应
   - 电机转速
   - 齿轮输出扭矩
   - 电机电枢电流

6. **提交内容**  
   请整理并输出以下结果：
   - 机电一体化模型总图（电气 + 机械 + 控制）
   - 位置响应曲线
   - 电机电流与扭矩曲线
   - 对弹性环节引起的系统振荡现象进行简要分析

输出结果图片：

<img :src="$withBase('/Example/picture2.png')" style="width:1000px; border:1px solid black;">

AI 生成模型：<helpButton isLink exampleUrl="mworks://ref/../SysplorerAI/Samples/ExampleFile/ServoPositionControl.mo">ServoPositionControl.mo</helpButton>。
