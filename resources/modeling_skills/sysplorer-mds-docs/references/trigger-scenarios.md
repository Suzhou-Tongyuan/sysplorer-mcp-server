# Trigger scenarios (documentation Q&A only)

Use these when the user’s **main goal** is to retrieve/explain official help—not when they want a deliverable model built/checked/simulated.

If phrasing is close **and** the ask is doc-Q&A, and `mdsSearch` is listed, call it before answering from memory. If the ask is modeling execution, do **not** primary-trigger this skill.

The right-hand column lists **facts / product terms to weave into a ~100-char hypothetical-answer `query`**—not keywords to pass as `query`. See `query-examples.md`.

## A. 使用 Sysplorer — 核心建模

| User might say | Weave into hypothetical-answer query |
|----------------|--------------------------------------|
| Sysplorer 怎么入门 / 快速上手 | Sysplorer 快速入门 |
| 环境基础知识、界面怎么用、菜单在哪 | Sysplorer 环境基础知识, 操作指南 |
| Modelica 语言基础、语法入门 | Modelica 语言基础 |
| 怎么建模、怎么仿真（产品操作，非“帮我建某某系统”） | 建模, 仿真 |
| 高级建模和调试、文本建模调试 | 高级建模和调试 |
| 外部组件集成、模型导出怎么做 | 外部组件集成与模型导出 |
| Sysblock 快速入门 / 框图怎么建 | Sysblock 快速入门, 框图建模 |
| Sysblock 仿真、HDL 代码生成 | 仿真, HDL 代码生成 |
| 验证、确认和测试 / V&V | 验证、确认和测试 |
| 模块集创建、Sysblock 支持的硬件 | 模块集创建和仿真集成, Sysblock 支持的硬件 |
| 状态机建模环境 / 状态机模块库 | 状态机建模环境, 模块库 |
| 事件建模 | 事件建模, 模块库 |
| MWORKS AI / Skills / MCP 是什么 | Sysplorer AI, Skills, MCP Server |

## B. 仿真集成工具

| User might say | Weave into hypothetical-answer query |
|----------------|--------------------------------------|
| 怎么导入 FMU / 导出 FMU | FMU 导入工具, FMU 导出工具 |
| Simulink 模型怎么导入 Sysplorer | Simulink 模型导入工具 |
| Sysblock 怎么导出成 Simulink / M 脚本 | Simulink 模型导出工具 |
| 半物理仿真接口、生成实时代码 | 半物理仿真接口工具 |
| 半物理仿真管理、HIL 上位机 | 半物理仿真管理工具 |

## C. 高级扩展工具

| User might say | Weave into hypothetical-answer query |
|----------------|--------------------------------------|
| 命令与脚本、API、CMD 启动参数 | 命令与脚本工具 |
| 模型加密、发布模型 | 模型加密发布工具 |
| 三维动画窗口怎么用 | 三维动画工具 |
| 数字仪表 | 数字仪表工具 |
| 求解算法扩展、自定义求解器接口 | 求解算法扩展接口 |

## D. 从 Simulink 到 Sysplorer

| User might say | Weave into hypothetical-answer query |
|----------------|--------------------------------------|
| 从 Simulink 迁移到 Sysplorer / MWORKS | 从 Simulink 迁移到 MWORKS 建模环境 |
| Simulink 和 Sysplorer 环境差异 | Sysplorer 与 Simulink 环境差异说明 |
| 把 Simulink 模型转成 Sysblock | 把 Simulink 模型转换为 Sysblock 模型 |
| Sysblock 框图建模系列教程 | Sysblock 框图建模系列教程 |

## E. 工作流

| User might say | Weave into hypothetical-answer query |
|----------------|--------------------------------------|
| 系统建模仿真流程 / 对象分析到结果分析 | 仿真对象分析, 模型架构确定, 系统模型构建, 模型测试验证, 模型集成联调, 仿真结果分析 |
| 怎么开发模型库、液压组件库案例 | 模型库开发, 案例-液压组件库 |
| 嵌入式代码生成、MISRA-C、数据字典、双向追溯 | 嵌入式代码生成 |
| Sysblock 定点、量化、精度对比 | Sysblock 定点设计工具 |
| AUTOSAR / SWC | AUTOSAR 工具箱 |
| 协同建模、权限管理 | 服务端模型权限管理, 客户端模型协同建模 |
| 设计优化工作流、工程应用示例 | 基于模型的设计优化, 工作流程 |
| 数据建模、模型降阶、数据机理融合 | 数据建模, 模型降阶, 数据机理融合 |
| 模型线性化、频率响应估算、控制系统设计 | 模型线性化, 模型频率响应估算, 模型控制系统设计 |
| 联合仿真、共仿真 | 模型联合仿真, 软件联合仿真 |
| 和 Syslab 怎么集成、Workspace 同步 | 与 Syslab 双向集成, From Workspace, To Workspace |
| 开放系统架构、开放接口 | 开放系统架构, 开放架构和接口 |

## F. 工具箱 / 模型库总览（手册级）

| User might say | Weave into hypothetical-answer query |
|----------------|--------------------------------------|
| CAD 工具 / 机械多体工具箱怎么用 | 机械多体工具箱, CAD 工具 |
| 试验设计、敏感度分析、响应优化、参数估计（工具箱说明） | 设计优化, 模型试验设计, 敏感度分析, 响应优化, 参数估计 |
| 控制器设计工具箱有哪些器 | 控制器设计工具箱, 模型线性化器, 频率响应估算器 |
| 模型降阶及融合仿真工具 | 模型降阶及融合仿真工具 |
| 某行业/领域模型库总览怎么用（非单个类参数） | 对应模型库手册标题（机械/流体/电气/车辆/能源/制造/航空…） |

## G. 官方示例

| User might say | Weave into hypothetical-answer query |
|----------------|--------------------------------------|
| 有哪些官方示例、示例在哪 | 示例, 物理建模, 框图建模, 工程应用 |
| 倒立摆 / 双摆 / 液压缸 / 房屋供暖 等示例怎么打开 | 具体示例名 + 打开示例 |
| 打开示例后图面异常、要不要先加载库 | 打开示例, 检查按钮, 加载模型库 |

## H. Do **not** treat as mdsSearch-first

| User might say | Prefer instead |
|----------------|----------------|
| 「帮我建一维传动系并检查仿真」等落地建模 | modeling rules + domain skills |
| 「怎么用 Modelica 开发某某系统」（要交付模型） | modeling skills；勿因「怎么」抢触发 |
| `TYMultibody.Joints.Revolute` 有哪些参数 | `get_lib_model_document` |
| `AddComponent` / `TranslateModel` / `SimulateModel` 参数与返回值 | `get_api_document` / `ListFunctions` |
| 改当前模型参数 / 直接跑仿真 | modeling MCP tools |
| 工具列表无 `mdsSearch` | Fallback；不要空转探测 |

## Query reminder

When you *do* call `mdsSearch`, `query` must be a ~100-char **hypothetical answer**, not keywords and not the user utterance. See `query-examples.md`.

## One-line rule

**主目标=查/讲官方帮助 → mdsSearch。**  
**主目标=建/检/仿/改具体模型 → 建模技能（MDS 仅可辅查）。**  
**可用性=工具是否在列表中。**
