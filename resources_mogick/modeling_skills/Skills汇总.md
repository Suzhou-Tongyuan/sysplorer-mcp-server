# Sysplorer Skills 汇总

> 版本：1.6.1 | 更新日期：2026-08-24
>
> **modelica-lite / mols 覆盖层**：本目录随 `resources_mogick/` 叠加到 exe 包资源。依赖相关规则以 **`ty-sysplorer-dependency-guard`** 为准（静默 `LoadLibrary returned False` → 先 `plan` 再 `prepare`）。本包**不包含** `ty-cadtool-modeling`、`sysplorer-mds-docs` 与 `cad_toolbox_api`。

---

## 概述

Sysplorer Skills 是面向不同建模领域和工程场景的专用技能集合。每个 Skill 封装了特定领域的**建模规则**、**组件选型经验**、**典型工作流程**和**排障知识**，为 AI 客户端提供结构化的领域专家指导。

**与 MCP 语料的分工**：Skill 提供**可执行的流程与约束摘要**；`resources/` 下大块文档（如 **SysblockModelLibrary**、历史 manifest 注册的 RAG 条目）仍通过 **`resources_retrieval`** 按需检索。MCP 服务端启动时的 **`instructions` 不嵌入** `resources_manifest.json` 摘要。

---

## Skill 分类一览

Sysplorer Skills 当前按领域分为 **6 大类**，共包含 **19 个 Skill**：

### 一、流程与指南类（1 个）

| Skill 名称 | 中文名称 | 短描述 |
|------------|----------|--------|
| `modelica-library-workflow` | Modelica 模型库开发流程 | 按标准流程规划、搭建与评审 Modelica 模型库 |

### 二、建模必须遵守的规范类（2 个）

| Skill 名称 | 中文名称 | 短描述 |
|------------|----------|--------|
| `ty-sysplorer-modeling-rules` | Sysplorer 建模必须遵守的规范 | **须遵守**的分流、七门闸、风格与 MCP 工具分工；`modelica_diagram_connect_semantics`（图解 connect/Placement/Line）、Gate 6 在检查通过后与仿真前；非「仅供参考」的选路建议 |
| `ty-sysplorer-dependency-guard` | Sysplorer 模型库依赖保障 | 针对缺失模型库执行可下载清单解析、库名纠错、真实下载/安装、刷新、加载验证与原失败点重试 |

### 三、设计优化与参数估计类（5 个）

| Skill 名称 | 中文名称 | 短描述 |
|------------|----------|--------|
| `ty-design-opt-mpe-modeling` | DesignOpt 与 MPE 参数设计估计 | DesignOptMpe 参数设计、估计与优化脚本及与 MCP 工具协同 |
| `ty-design-opt-exp-gui-modeling` | DesignOptExpGui 模型试验 | 批量研究、实验设计、蒙特卡洛、时变参数研究与结果读取 |
| `ty-design-opt-exp-modeling` | DesignOptExp 批量仿真 | 批量仿真初始化、参数扫描、结果变量选择与结果读取 |
| `ty-design-opt-mro-modeling` | DesignOptMro 响应优化 | 调节参数、需求、变量集、算法配置、评估优化与结果读取 |
| `ty-design-opt-psa-modeling` | DesignOptPsa 敏感度分析 | 参数集、采样、需求评估、量化分析与结果读取 |

### 四、物理模型建模与调试类（5 个）

| Skill 名称 | 中文名称 | 短描述 |
|------------|----------|--------|
| `ty-mechanical-modeling` | TY 机械系统建模 | 使用 TY 商业库进行机械系统自动建模 |
| `ty-hydraulic-pneumatic-modeling` | TY 液压气动建模 | 使用 TY 内置库进行液压、热液压、气动系统建模与图面校核 |
| `ty-nps-library-modeling` | NPS 电气系统建模 | 使用 NPSLibrary 进行电力系统、电力电子与电机建模 |
| `ty-thermofluid-modeling` | TY 热流体系统建模 | 在 MWORKS/Sysplorer 中执行 TY 热流体、换热、空气处理与通风系统的建模、修复与验证 |
| `ta-vehicle-modeling` | TA 车辆库建模 | 在已应用 `ty-sysplorer-modeling-rules` 后，于 TA 六库范围内完成整车与车辆子系统建模、修复、仿真与结果核验 |

### 五、能源系统建模与调试类（1 个）

| Skill 名称 | 中文名称 | 短描述 |
|------------|----------|--------|
| `ty-energy-modeling` | TY 能源系统建模 | 在已应用 `ty-sysplorer-modeling-rules` 后，于 TY 光伏/风电/电池/综合能源库及 `Modelica 4.0.0.TY.1` 范围内完成能源系统建模、修复与验证 |

### 六、Sysblock 框图模型建模与调试类（5 个）

| Skill 名称 | 中文名称 | 短描述 |
|------------|----------|--------|
| `ty-sysblock-diagram-modeling` | Sysblock 框图建模 | 使用 SysplorerEmbeddedCoder 进行框图建模、修复与仿真验证 |
| `ty-sysblock-signal-modeling` | Sysblock 信号与通信建模 | 用于 Sysblock 信号处理、通信链路建模与验证闭环 |
| `ty-sysblock-batch-param-modeling` | Sysblock 批量参数对象配置 | 通过 GetModelParamValues / SetModelParamValues 整组读写模块参数对象 |
| `ty-sysblock-svdpi-codegen` | Sysblock SV-DPI 代码生成 | 为 Sysblock 代码生成结果生成和校验 SV-DPI 包装 |
| `ty-simulink-importer-modeling` | Simulink 模型导入 | 将 Simulink `.slx` 导入为 Sysblock 模型，配置 Link 库与数据文件 |

---

## 各 Skill 详细说明（节选）

### `ty-sysplorer-modeling-rules`

- **版本**：1.1.0  
- **触发**：任何建模/改模型任务均须**遵守**本 Skill 与 **`modeling_rules`** 语料所规定的范式、**七门闸**、路径与工具分工。  
- **边界**：**必须遵守**的约束与 `references/` 正文；框图域内操作细则见 **`ty-sysblock-*`**。  
- **附录**：`references/` 含**须遵守的**分流/门禁/风格/**`modelica_diagram_connect_semantics`（图解与连接语义）** 全文与 **`sysblock-library-index.md`**（RAG：`corpus_id=modeling_rules`）。

### `ty-sysplorer-dependency-guard`

- **版本**：1.1.0（mogick / **modelica_lite**）
- **触发**：平台为 modelica_lite/mols；加载、打开、检查、翻译、仿真涉及 Modelica、TY、TA 等库；或 `load_library` 返回 `ok:false` / `LoadLibrary returned False`（含静默失败）；或出现「模型库未安装」、`install_if_missing` 等信号。
- **要点**：modelica_lite **不假设库已预装**；失败后 **先 `plan` 再 `prepare`**；真实下载必须 `dry_run=false` + `download_missing=true`；无 `--user-workspace` 时仍应 `plan` 列清缺失项。

### `ty-design-opt-mpe-modeling`

- **版本**：1.0.0  
- **触发**：参数估计、MPE、DesignOptMpe、优化脚本、`run_script` 标定等。  
- **要点**：`session_manager` → `resources_retrieval(design_opt_mpe_api)` / `references/` → `call_code(run_sysplorer_api)`；禁止 `ClearAll` / `ChangeDirectory`。

### `ty-design-opt-exp-gui-modeling` / `ty-design-opt-exp-modeling`

- **版本**：1.4.0 / 1.1.0  
- **触发**：模型试验、实验设计、蒙特卡洛、批量仿真、参数扫描等。  
- **要点**：ExpGui 负责研究设计与样本生成，Exp 负责执行批量仿真与结果读取；详见各包 `references/`。

### `ty-design-opt-mro-modeling` / `ty-design-opt-psa-modeling`

- **版本**：1.1.0 / 1.0.0  
- **触发**：响应优化、敏感度分析、需求评估、量化分析等。  
- **要点**：分别对应 `DesignOptMro` 与 `DesignOptPsa` Python API；详见各包 `references/`。

### `ty-simulink-importer-modeling`

- **版本**：1.0.0  
- **触发**：Simulink 模型导入、`.slx` → Sysblock、Link 子系统库、`.slxdata` 数据文件等。  
- **要点**：`SimulinkImporter` Python API；详见 `references/SimulinkImporter.md`。

### `ty-sysblock-batch-param-modeling`

- **版本**：1.4.0  
- **触发**：`GetModelParamValues` / `SetModelParamValues`、模块整组参数对象读写、复杂块（CCaller、LookupTable、Bus 等）参数映射、模块参数专项说明编写。  
- **要点**：优先整对象读取后回写；单字段标量仍可用 `SetModelParamValue`；详见 `references/批量参数配置接口说明.md` 与 `references/模块参数专项说明/`。

### `ta-vehicle-modeling`

- **版本**：1.1  
- **触发**：车辆/整车/汽车子系统、动力性/经济性/续航/操稳/平顺性/热管理等；或明确 `TAEconomy`、`TADynamics`、`TAThermalSystem`、`TAEngine`、`TABattery`、`TAElectronic` / TA 车辆库。  
- **要点**：在 `ty-sysplorer-modeling-rules` 之后作为车辆域薄补丁；优先 TA 六库，简单集总参数任务仍做领域分流与验证；详见包内 `references/` 与 `workflows/`。

### `ty-energy-modeling`

- **版本**：1.1  
- **触发**：明确要求使用 TY 光伏发电库、风力发电库、电池库、综合能源系统库或限定在上述库与 `Modelica 4.0.0.TY.1` 范围内的能源系统建模/修复/验证。  
- **要点**：仅出现「光伏」「风机」「储能」等场景词且未明确 TY 能源库范围时不单独触发；与 `ty-nps-library-modeling`（NPSLibrary）分流；详见包内 `references/` 与 `workflows/`。

### `modelica-library-workflow` — `ty-sysblock-svdpi-codegen`

（其余各 Skill 说明从略；详见各包内 `SKILL.md` / `使用说明.md`。）

---

## Skill 目录结构概览

```
modeling_skills/
├── modelica-library-workflow/
├── ty-sysplorer-modeling-rules/
├── ty-sysplorer-dependency-guard/
├── ty-design-opt-mpe-modeling/
├── ty-design-opt-exp-gui-modeling/
├── ty-design-opt-exp-modeling/
├── ty-design-opt-mro-modeling/
├── ty-design-opt-psa-modeling/
├── ty-mechanical-modeling/
├── ty-hydraulic-pneumatic-modeling/
├── ty-nps-library-modeling/
├── ty-thermofluid-modeling/
├── ta-vehicle-modeling/
├── ty-energy-modeling/
├── ty-sysblock-diagram-modeling/
├── ty-sysblock-signal-modeling/
├── ty-sysblock-batch-param-modeling/
├── ty-sysblock-svdpi-codegen/
├── ty-simulink-importer-modeling/
├── Skills汇总.md
└── Skill文件清单.md
```

每个 Skill 目录内通常包含：`SKILL.md`、`SKILL_ZH.md`、`版本说明.md`、`使用说明.md`、`skill_info.json`，以及 `references/`、`workflows/` 等。

---

## 安装说明

配置时需要**拷贝整个 skill 目录**，不能只拷贝 `SKILL.md`。

### OpenCode（全局，安装 MCP 包时脚本可自动同步）

**用户级（推荐与安装脚本一致）**：

```
~/.config/opencode/skills/        # Linux/macOS
%USERPROFILE%\.config\opencode\skills\  # Windows
```

安装程序会将随包 **`resources/modeling_skills/<name>/`** 同步到上述目录（**白名单逐目录**替换，不清空 `skills` 根）。跳过：环境变量 **`NO_SYNC_OPENCODE_SKILLS=1`**。

### Modelex（全局，安装 MCP 包时脚本可自动写入）

**用户级**：

```
~/.modelex/mcp.json              # Linux/macOS
%USERPROFILE%\.modelex\mcp.json  # Windows
```

安装程序会写入 **`servers.sysplorer`** 节点（并清理旧版 `sysplorer_mcp` / `mworks_mcp` 键）。

**用户级 Skills 目录**：

```
~/.modelex/skills/              # Linux/macOS
%USERPROFILE%\.modelex\skills\  # Windows
```

安装程序会将随包 **`resources/modeling_skills/<name>/`** 同步到上述目录（**白名单逐目录**替换，不清空 `skills` 根）。跳过：环境变量 **`NO_SYNC_OPENCODE_SKILLS=1`**（同时跳过 OpenCode 与 Modelex skills 同步）。

### Codex

**项目级**：`your-project/.codex/skills/`  
**用户级**：`~/.codex/skills/`（Windows：`%USERPROFILE%\.codex\skills\`）

### Claude Code

**项目级**：`your-project/.claude/skills/`  
**用户级**：`~/.claude/skills/`

### OpenCode（项目级）

`<your-project>/.opencode/skills/`

---

## 建议

- 若仅当前仓库使用，可选**项目级安装**；若希望多项目共用或与 MCP 安装脚本对齐，选**用户级 / 全局 OpenCode 路径**。
- 大块参考仍以 **`resources_retrieval`** 为主，避免在对话中粘贴整库文档。
