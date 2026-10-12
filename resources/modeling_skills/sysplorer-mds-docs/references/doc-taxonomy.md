# Help-center taxonomy (MDS)

Source shape follows Sysplorer Docs homepage (`extend-config` / 帮助中心首页): **使用 Sysplorer**、**工作流**、**工具箱**、**模型库**，以及示例/函数/模块导航。

Map user intent to one primary column; add a second only if the first search is empty or off-topic. Concrete natural-language prompts: `trigger-scenarios.md`.

## 1. 使用 Sysplorer

### 物理建模

| Signal | Query seeds |
|--------|-------------|
| 快速入门、入门 | Sysplorer 快速入门 |
| 应用领域与模型库 | 应用领域与模型库 |
| 环境、界面、基础知识 | Sysplorer 环境基础知识 |
| Modelica 语言 | Modelica 语言基础 |
| 建模 / 仿真（操作） | 建模, 仿真 |
| 高级建模、调试 | 高级建模和调试 |
| 外部组件、导出 | 外部组件集成与模型导出 |
| 参考信息 | 参考信息 |

### 框图建模（Sysblock）

| Signal | Query seeds |
|--------|-------------|
| Sysblock 入门、案例 | Sysblock 快速入门, 应用案例 |
| 环境基础知识 | Sysblock 建模环境基础知识 |
| 建模 / 仿真 | 建模, 仿真 |
| HDL | HDL 代码生成 |
| V&V、测试 | 验证、确认和测试 |
| 模块集、仿真集成、硬件 | 模块集创建和仿真集成, Sysblock 支持的硬件 |
| 注意事项 | 注意事项 |

### 状态机 / 事件

| Signal | Query seeds |
|--------|-------------|
| 状态机 | 状态机建模环境, 模块库 |
| 事件建模 | 事件建模, 模块库 |

### Sysplorer AI

| Signal | Query seeds |
|--------|-------------|
| MWORKS AI、Skills、MCP | MWORKS AI, Sysplorer Skills, Sysplorer MCP Server |

### 仿真集成工具

| Signal | Query seeds |
|--------|-------------|
| FMU 导入/导出 | FMU 导入工具, FMU 导出工具 |
| Simulink 导入/导出 | Simulink 模型导入工具, Simulink 模型导出工具 |
| 半物理接口/管理、HIL | 半物理仿真接口工具, 半物理仿真管理工具 |

### 高级扩展工具

| Signal | Query seeds |
|--------|-------------|
| 命令、脚本、API、CMD | 命令与脚本工具 |
| 加密、发布 | 模型加密发布工具 |
| 三维动画 | 三维动画工具 |
| 数字仪表 | 数字仪表工具 |
| 求解算法扩展 | 求解算法扩展接口 |

### 从 Simulink 到 Sysplorer

| Signal | Query seeds |
|--------|-------------|
| 迁移、转换 | 从 Simulink 迁移到 MWORKS 建模环境, 把 Simulink 模型转换为 Sysblock 模型 |
| 环境差异 | Sysplorer 与 Simulink 环境差异说明 |
| 系列教程 | Sysblock 框图建模系列教程 |

## 2. 工作流

| Signal | Query seeds |
|--------|-------------|
| 系统建模仿真全流程 | 仿真对象分析, 模型架构确定, 系统模型构建, 模型测试验证, 模型集成联调, 仿真结果分析 |
| 模型库开发 | 需求分析, 架构设计, 接口设计, 模型开发, 模型测试, 液压组件库 |
| 代码生成 | 嵌入式代码生成, Sysblock 定点设计工具, AUTOSAR 工具箱 |
| 协同建模 | 服务端模型权限管理, 客户端模型协同建模 |
| 设计优化工作流 | 基于模型的设计优化, 工作流程, 工程应用 |
| 数据建模 | 数据建模, 模型降阶, 数据机理融合 |
| 控制器设计工作流 | 模型线性化, 模型频率响应估算, 模型控制系统设计 |
| 联合仿真 | 模型联合仿真, 软件联合仿真 |
| Syslab 集成 | 与 Syslab 双向集成, From Workspace, To Workspace |
| 开放系统架构 | 开放系统架构, 开放架构和接口 |

## 3. 工具箱

| Signal | Query seeds |
|--------|-------------|
| 机械多体、CAD | 机械多体工具箱, CAD 工具 |
| 设计优化工具箱 | 设计优化, 模型试验设计, 敏感度分析, 响应优化, 参数估计 |
| 控制器设计工具箱 | 控制器设计工具箱, 模型线性化器, 频率响应估算器, 控制系统设计器 |
| 降阶 / 融合仿真 | 模型降阶及融合仿真工具 |

## 4. 模型库（总览手册）

| Signal | Query seeds |
|--------|-------------|
| 同元基础 / Modelica 库总览 | 同元基础模型库 |
| 机械 / 流体 / 电气 | 机械模型库, 流体模型库, 电气模型库 |
| Sysblock 信号处理与无线通信库 | 信号处理和无线通信模型库 |
| 车辆 / 能源 / 制造 / 航空航天 | 车辆行业模型库, 能源行业模型库, 制造行业模型库, 航空航天行业模型库 |

For **one named class’s parameter panel**, prefer `get_lib_model_document` over MDS.

## 5. 示例 / 函数 / 模块（导航型）

| Signal | Query seeds / note |
|--------|-------------------|
| 官方示例、打开示例 | 示例 + 领域或示例名 |
| 函数手册叙事、API 列表页 | 函数；具体签名仍用 `get_api_document` |
| Sysblock/状态机模块说明目录 | 模块 + 库名（Continuous、Discrete…） |

## Routing tips

- “帮我建一个…” → modeling execution first; `mdsSearch` only if they also need official how-to/example text—then rewrite into a hypothetical-answer `query`.
- “FMU / 半物理 / 迁移 / 定点 / AUTOSAR / 协同 / Syslab …” → `mdsSearch` first (product docs).
- Ambiguous “怎么用 Sysplorer” → weave 快速入门 facts into the hypothetical answer.
- Taxonomy seeds belong **inside** the ~100-char hypothetical answer, not as a keyword `query`.
- API function signatures → `get_api_document` / `ListFunctions`, never `mdsSearch`.
