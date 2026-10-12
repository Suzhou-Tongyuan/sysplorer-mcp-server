> 本文件仅用于中文审核参考，实际任务执行请调用 SKILL.md

# DesignOptMpe - 参数设计、估计与优化

## Frontmatter 对照

- `name`: `ty-design-opt-mpe-modeling`
- `description`: 在 Sysplorer 内通过 DesignOptMpe 做参数设计、MPE 参数估计、优化与标定脚本、`run_sysplorer_api` 实验循环。覆盖原生 MPE 流程、多边界与稳态估计、统一残差设计、批量仿真驱动的自定义算法与外置算法适配器。不要用于与 DesignOptMpe 无关的 ModelingPy 通用 API 查询（请用 `get_api_document`），也不要用于纯 Modelica / Sysblock 建模范式任务（请先用 `ty-sysplorer-modeling-rules` 再进入领域技能）。
- `metadata.short-description`: DesignOptMpe parameter estimation and custom optimization guidance
- `metadata.version`: `1.4.1`
- `metadata.managed-by`: `sysplorer-mcp`

## 适用范围

- **适用**：需要在 Sysplorer 内使用 DesignOptMpe Python 模块的 DesignOpt / MPE / 参数估计 / 优化任务，包括多边界与稳态估计、统一残差设计、批量仿真驱动的自定义优化，以及实验循环与 Sysplorer 模型集成的任务。
- **不适用**：与 DesignOptMpe 无关的 ModelingPy 表层 API 查询（请用 `get_api_document`）；纯 Modelica / Sysblock 建模执行任务（请使用领域技能和 `modeling_path_router`）；响应优化任务请用 `ty-design-opt-mro-modeling`。

## 硬性规则

1. **会话优先**：任何会触碰 Sysplorer 的 `run_sysplorer_api` 之前，先执行 `session_manager(action="health" | "ensure")`。
2. **禁止**在脚本或工具中调用 `ClearAll` 或 `ChangeDirectory`；需要卸载时使用 `model_manager(action="unload")`。
3. DesignOptMpe **不**通过主 `Help()` 命名空间提供文档；应在 `run_sysplorer_api` 中使用 `import` + `ListFunctions()` / `help()`，并结合 `references/` 中的语料文本，以及语料库 `design_opt_mpe_api` 上的 `resources_retrieval`。
4. 显式导入工具箱：`import mworks.sysplorer.DesignOptMpe as mpe`、`import mworks.sysplorer.DesignOptExp as exp`。
5. **缺数据规则**：不要臆造参数名、边界、变量映射、时间窗、工况值或测量列；无法从模型、输出或 `references/` 得到时，先询问或说明将要使用的默认值。
6. **自定义优化路径**：用户要求自定义算法、高性能外部算法、混合策略，或内置 MPE 算法受限时，切换到本 skill 的自定义批量优化路径。
7. **批量仿真优先**：自定义算法评估大量候选参数时，优先使用 `DesignOptExp.InitialBatchSimulate(...)` 与 `DesignOptExp.BatchSimulate(...)`。
8. **失败惩罚**：任一必需边界仿真失败的候选参数，其目标值直接记为 `1e300`。
9. **模型依赖库规则**：见下文「模型依赖库规则」。
10. **预检顺序**：依赖库推导与加载必须早于 `CheckModel`、`TranslateModel`、`InitialBatchSimulate` 或短仿真检查；缺库时检查/翻译接口可能阻塞。
11. **算法适配器策略**：用户指定未内置算法时，先调研其能否优化昂贵黑盒标量目标，再决定是否接入适配器。
12. **对外措辞**：列举支持的算法时只说原生算法、内置自定义算法和「外置算法适配器」，不暴露内部适配器入口名、配置字段名、回调名或实现类名。

本文与对应 `SKILL.md` 中所有 `references/...` 路径均相对于**本 skill 目录**（包含 `SKILL.md` 的文件夹），不是工作区根目录，也不是上层 `skills/` 目录。

## 工具分工

| 需求 | 工具 / 动作 |
|------|-------------|
| Sysplorer 就绪检查 | `session_manager` |
| 执行估计 / 优化代码 | `call_code`（`mode="run_sysplorer_api"`） |
| 长文档、FAQ、API 表 | `resources_retrieval`，`sources` 包含 `design_opt_mpe_api` |
| 模型打开 / 保存 / 卸载 | `model_manager` |
| 检查 / 翻译 / 仿真受影响模型 | `check_model`、`translate_model`、`simulate_model` |
| 批量仿真执行 | `DesignOptExp.InitialBatchSimulate(...)`、`DesignOptExp.BatchSimulate(...)` |

## 版本

- skill 名称：`ty-design-opt-mpe-modeling`
- 当前版本：`1.4.1`

## 原生内置算法

`SelectAlgorithm()` 支持的内置算法（默认 `Bobyqa`）：

| 算法 | 配置接口 |
|------|----------|
| `Bobyqa` | 无专属配置，使用内部默认值 |
| `Cobyla` | 无专属配置，使用内部默认值 |
| `GA` | `ConfigGAAlgorithm(...)` |
| `PSO` | `ConfigPSOAlgorithm(...)` |
| `Praxis` | 无专属配置，使用内部默认值 |

## 本次更新后的能力边界

- 支持原生 `DesignOptMpe` 参数估计流程
- 支持多边界工况与稳态工况
- 支持统一残差计算逻辑
- 支持基于 `DesignOptExp` 批量仿真的自定义优化路径
- 支持自动选择较优自定义算法
- 支持模型额外依赖库的询问、配置和自动推导
- 支持通过优化算法适配器接入未内置的外置算法

## 模型依赖库规则

- 用户提供模型文件后，先询问该模型是否依赖 `Modelica` 之外的库
- 用户给出依赖库时，将这些库写入运行配置，并在打开、检查、翻译或优化模型前加载
- 用户未给出或不确定依赖库时，从模型文本和 Sysplorer 安装目录中的库名做自动推导，并在流程内部使用
- 依赖库推导和加载必须早于 `CheckModel`、`TranslateModel`、`InitialBatchSimulate` 或短仿真检查；缺库时检查/翻译接口可能阻塞，不能把它们作为第一层缺库探测手段

## 新增的自定义优化路径

当用户提出以下需求时，优先切到自定义路径：

- 需要高性能外部算法
- 内置算法选择受限
- 需要混合优化策略
- 需要大量候选参数的并行/批量仿真
- 需要稳态多边界参数估计

执行主线：

1. 规范化参数、边界、变量映射、测量数据和时间设置
2. 处理模型额外依赖库：优先使用用户提供的库名，未提供时自动推导
3. 将“无边界”场景统一视为 1 个虚拟边界
4. 长时间优化前先执行预检
5. 用 `DesignOptExp.InitialBatchSimulate(...)` 初始化批量仿真
6. 在优化搜索前，先使用参数初始值评估一次，并作为第一条迭代信息
7. 将每组候选参数扩展到全部边界
8. 用 `DesignOptExp.BatchSimulate(...)` 一次性取回仿真结果
9. 按候选参数重新分组
10. 计算总残差
11. 选择或创建优化算法适配器
12. 通过适配器驱动自定义算法搜索最优参数

## 自定义算法策略

支持名称：

- `lshade`
- `basic-de`
- 外置算法适配器

选择规则：

- 用户明确指定 `lshade` 时，直接使用 `lshade`
- 用户明确指定 `basic-de` 时，直接使用 `basic-de`
- 用户提供适配器模块时，走外置算法适配器路径
- 用户只说“自定义算法”“高性能算法”但未指定具体算法时，默认使用 `lshade`
- 用户指定未内置算法时，先调研该算法是否适合昂贵黑盒标量目标优化；适合则创建适配器，不适合则说明阻塞点并建议替代方案

### 优化算法适配器契约

适配器用于把新算法标准化接入“候选参数 -> 批量仿真 -> 残差 -> 反馈算法”的闭环。适配器必须满足：

- 优化目标是越小越好的标量残差
- 生成的候选参数向量必须与待估参数顺序一致
- 尊重有限上下界；若算法本身无界，需要先做变换或修复
- 只能通过共享评估接口评价候选参数，不直接调用 Sysplorer
- 输出与内置算法一致的进度信息和结果结构

本地适配器接收一个优化上下文对象：

- 参数名称、上下界和初始值
- 边界定义和场景设置
- 候选参数修复工具
- 统一批量评估接口
- 进度输出接口

调用外置适配器前，框架会统一执行预检，并先评估一次参数初始值。该结果会作为历史记录的第一项；适配器需要保留它，并继续追加自己的迭代记录。

对外说明规则：

- 用户询问支持哪些优化算法时，只列出原生算法、内置自定义算法和“外置算法适配器”
- 不输出内部适配器入口名、配置字段名、回调名或实现类名，除非用户明确要求查看实现细节或配置文件

适配性判断：

- 适合：无导数、有界、昂贵黑盒优化算法，例如差分进化变体、带边界处理的 CMA-ES、低预算贝叶斯优化、模拟退火、粒子群变体等
- 需谨慎：天然无界、离散变量、或默认假设目标函数很便宜的算法
- 默认不适合：要求解析梯度、Hessian、直接访问模型方程、可微性或超大规模函数调用次数的算法

默认理由：

- `lshade` 比基础 DE 更适合慢仿真黑盒优化
- 在有边界约束的参数估计问题上更稳
- 适合作为 skill 内部的优选自定义算法

推荐长时间优化配置：

- `lshade` 正式优化建议种群规模使用 `20`（推荐值；未显式配置时脚本按参数维数自动取值）
- `lshade` 正式优化建议最大迭代次数使用 `100`
- 批量仿真并行数建议使用 `10`，优先保证长时间运行稳定性

配置分层说明：

- 算法配置包括算法名、种群规模、最大迭代次数和随机种子
- 仿真配置包括求解器、数值仿真容差、仿真时间范围、输出选项和批量仿真并行数
- 随机种子只用于保证随机初始化和进化过程可复现，不是算法必须的固定常数
- 数值仿真容差传给每次模型仿真的求解器，不是 `lshade` 的停止判据
- 求解器配置存在的原因是每组候选参数都需要调用 Sysplorer 模型仿真后才能计算残差

## 统一残差逻辑

支持的残差函数：

- `Mean Error`
- `Mean Absolute Error`
- `Mean Percentage Error`
- `Mean Absolute Percentage Error`
- `Mean Squared Error`

默认残差函数：

- `Mean Absolute Percentage Error`

百分比类残差的分母规则：

- 实测值非 0：分母取实测值
- 实测值为 0：分母取 `1`

### 多边界统一层级

无论单边界、多边界、稳态多边界，都按下面层级处理：

1. 单点偏差  
   `e(b,v,k) = sim - measure`

2. 单变量残差  
   `R(b,v) = phi(e(b,v,k))`

3. 单边界残差  
   `B(b) = mean_v(R(b,v))`

4. 总残差  
   `J = sum_b sum_v abs(w(b,v) * R(b,v))`

规则：

- 单边界残差只用于诊断，不作为最终优化目标
- 总残差不再对边界做二次平均
- 如需强调某边界的重要性，把权重下沉到该边界内的变量权重
- 未指定权重时默认 `1.0`

### 稳态工况规则

- 稳态场景应提供稳态时间
- 若未提供，则默认使用参数估计结束时间作为稳态时间
- 仿真结果没有该时刻时，必须插值
- 稳态只对比该时间点的值

### 动态工况规则

- 仅使用参数估计时间窗内的仿真数据
- 仿真时间点与测量时间点不重合时，将测量值插值到仿真时间点
- 再按选定残差函数汇总为单变量残差

## 批量仿真规则

自定义算法统一走批量仿真：

- 候选参数组数：`N`
- 边界数：`B`
- 平铺后的仿真任务数：`N * B`

流程：

1. 每组候选参数复制到所有边界
2. 叠加对应边界参数
3. 调用 `BatchSimulate(...)`
4. 将平铺结果回组为 `候选参数 -> 边界 -> 变量`
5. 计算该候选参数的总残差

## 仿真失败规则

如果某组参数在任一必需边界上仿真失败，则：

- 该组参数总残差直接赋值为 `1e300`

## 内部脚本资产

本节为 skill 内部实现参考，不对用户输出脚本路径与参数名。

- [`scripts/custom_batch_optimizer.py`](scripts/custom_batch_optimizer.py)

用途：

- 自定义算法统一入口
- 外置算法适配器入口
- L-SHADE / 基础 DE 的泛化执行入口
- 批量仿真结果回组
- 单边界 / 多边界 / 稳态多边界的统一残差计算
- 参数初始值评估，并将其作为第一条迭代信息输出
- 预检配置、路径、参数范围、测量映射和模型文本中的名称
- 额外依赖库配置与自动推导
- 运行时实时写出进度日志，每条迭代信息包含每个边界的残差

## 使用提醒

- 长时间自定义优化前，先使用预检模式确认配置完整
- 对用户提供的模型，先确认是否有额外依赖库；未提供时使用自动推导结果进入预检和优化
- 自定义优化默认把进度日志写到结果文件同目录的 `progress.jsonl`
- 原生 MPE 多边界实验仍然不能混用固定参数接口
- 自定义批量优化路径里，不再区分“有没有显式定义边界”，统一转换为边界列表
- 用户没有指定残差函数时，默认使用 `Mean Absolute Percentage Error`
- 用户没有指定自定义算法时，默认使用 `lshade`

## 执行闭环

1. **澄清目标**：区分参数估计、设计探索还是优化；确认输入，如测量数据、参数边界等。
2. **拉取参考资料**：快速阅读 `references/参数估计使用说明.md` 了解操作流程；阅读 `references/DesignOptMpe.md` 了解 API 顺序；阅读 `references/自定义批量参数估计说明.md` 了解自定义路径；查看 `references/` 下 demo notes 获取可运行示例。
3. **最小脚本**：导入模块，复现最小失败案例，并打印结构化状态。
4. **迭代**：使用 `call_code` 的 stdout/stderr 迭代调试；只有在最小闭环稳定后再扩大范围。

## RAG 提示

调用 `resources_retrieval(action="corpora")` 确认部署清单中 `design_opt_mpe_api` 的路径；当需要超出本技能内容的全文检索时，使用返回的索引路径执行 `action="search"`。
