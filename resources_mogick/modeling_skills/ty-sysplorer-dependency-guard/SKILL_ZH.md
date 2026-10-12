> 本文件仅用于中文审核参考，实际任务执行请调用 `SKILL.md`。
> 适用范围：**modelica_lite / mols（mogick）**。

# Sysplorer 模型库依赖保障（modelica_lite）

本 Skill 是 `ty-sysplorer-modeling-rules` 的薄附加规则，用于 **modelica_lite** 场景下：
确保建模、打开、检查、翻译、仿真过程中缺失的模型库能先被分析，再按清单下载、安装、刷新、加载并复验。

**平台事实**：modelica_lite **通常不预装**完整 Modelica / TY 商业 `.mol`；`load_library` 静默
`LoadLibrary returned False`（无「模型库未安装」文案）也必须进入本守卫。

## 何时使用

- 平台为 `modelica_lite` / `mols`（mogick）。
- 任务涉及 Modelica、TY、TA、`NPSLibrary`、`SysplorerEmbeddedCoder` 或其它模型库。
- `load_library` 返回 `ok: false` / `LoadLibrary returned False`（含无日志静默失败）。
- 工具返回「模型库未安装」、`library not installed`、`not installed`。
- `load_library(action="plan")` 返回 `action="install_if_missing"`。
- 需要打开 `.mo` 文件、`check_model`、翻译或仿真。

## 硬性规则

- 先 `load_library(action="load")` 试本机。`dependency_download_enabled=false` 只表示不能远程安装，不表示 TA/Modelica 库不存在。
- 不要在本地 load 失败后仍假设库已安装；失败后再 `plan` → `prepare`。
- `load_library(action="load")` 只能加载本机已安装库，不能替代下载；禁止空转重试 load。
- 发现缺库（含静默 False）后不能只提醒用户：
  1. `load_library(action="plan", library_name=...)`
  2. gate 打开时再 `prepare`（`dry_run=false`, `download_missing=true`, `load_after_download=true`）
- `plan` 或 `dry_run=true` 只表示分析，不表示安装完成。
- 下载前必须按可下载清单解析库名；只能用 `resolved_name`。
- 若返回 `ambiguous_library_name` 或 `unknown_library_name`，必须停止自动下载。
- 若返回 `dependency_download_gate.enabled=false`，说明需要以 `--user-workspace` 启动 MCP；
  仍应保留 `plan` 结果列出缺失库，不能声称已下载。
- 下载/安装后必须回到原失败点重新验证。

## 最小参考

| 需要 | 读取 |
|---|---|
| 工具参数模板 | `references/tool-parameter-templates.md` |
| 可下载清单策略 | `references/downloadable-library-catalog-policy.md` |
| 失败信号处理 | `references/failure-signals.md` |

## 交付证据

最终状态应说明：

- 平台为 modelica_lite；是否因静默 False 进入守卫。
- 哪些库已安装、已规划、已下载、已跳过或被阻塞。
- 是否发生库名纠错，包括 `input_name`、`resolved_name`、`matched_by`。
- 是否执行 `UpdateLibrary` / 安装后 `LoadLibrary`。
- 是否重试原始操作。
- 如果失败，明确失败在清单、gate、下载、校验、解压、安装/UAC/helper、刷新或加载阶段。
