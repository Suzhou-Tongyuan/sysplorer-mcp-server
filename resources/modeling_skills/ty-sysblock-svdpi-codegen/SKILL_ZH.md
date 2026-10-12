> 本文件仅用于中文审核参考,实际任务执行请调用 SKILL.md

---
name: ty-sysblock-svdpi-codegen
description: 用于在已有 Sysplorer Sysblock codegen 目录之上生成、刷新、检查或验证 SV-DPI wrapper,尤其适用于用户提到 dpi.h、dpi.c、dpi_pkg.sv、dpi.sv、tb.sv、simulate.do、wave.do、motrace.json、testpoint getter、ModelSim 或 Questa 的场景。只在可用 codegen 目录已经存在时接管;本技能不负责 Sysplorer 建模或 codegen 本体。
metadata:
  short-description: 为 Sysblock 代码生成结果生成和校验 SV-DPI 包装
  version: 1.0.0
---

# Sysblock SV-DPI 代码生成

> 在已有 Sysplorer Sysblock codegen 结果之上生成和验证 SV-DPI wrapper 的编排层。本技能围绕随包脚本 `scripts/render_svdpi.py` 进行编排;除非用户明确要求手工修改,否则优先调用脚本,不要直接手写生成 wrapper 文件。

**核心闭环**:`边界检查 -> codegen目录检查 -> 运行生成脚本 -> metadata回看 -> testpoint处理 -> 按需仿真 -> 交付`

> [!CAUTION]
> ## 全局执行纪律(必须遵守)
>
> 1. **先确认边界**:必须先确认可用codegen目录已存在;如果codegen还不存在,停下并回到Sysplorer codegen前置步骤。
> 2. **codegen目录为事实来源**:禁止靠记忆臆造端口、step函数或testpoint;必须直接读取codegen目录。
> 3. **脚本优先**:默认运行 `scripts/render_svdpi.py`,不要默认手工改wrapper;仅在用户明确要求时才手工补丁。
> 4. **必须回看metadata**:不得只因为文件生成成功就宣称任务完成;如果`_svdpi_metadata.json`还有unresolved testpoint或关键结构警告,必须说明。
> 5. **启发式必须披露**:自然语言testpoint匹配是启发式的;必须在呈现结果前说明这一点。
> 6. **交付必须可复核**:最终输出必须说明实际完成动作、生成文件、metadata回看结果以及任何警告或未解决项。

> [!IMPORTANT]
> ## 触发与语言规则
>
> - 响应语言应与用户输入语言保持一致,除非用户明确指定其他语言。
> - 本Skill仅在可用Sysplorer codegen目录已存在时适用。
> - 如果用户说"对模型生成代码"或"从模型导出代码",应先完成Sysplorer codegen,再进入本Skill。
> - 不要将本Skill用于泛SystemVerilog DPI理论说明,不涉及Sysplorer wrapper落地时不使用。

## 适用范围

- 从现有codegen目录生成或刷新SV-DPI wrapper文件(dpi.h、dpi.c、dpi_pkg.sv、dpi.sv、tb.sv)
- 从 `motrace.json` 列出或选择标量testpoint候选
- 按需生成 `GetTestpoint_*` 接口
- 生成 `simulate.do` 和 `wave.do` 仿真辅助文件
- 在需要时对生成的wrapper执行ModelSim或Questa smoke test

**不适用场景:**
- Sysplorer建模或codegen本体
- 通过直接修改模型生成的C实现来替代wrapper生成
- 基础smoke test之外的任意仿真环境深度排障

## 关键约束

- 最小可用输入:一份Sysplorer已生成的codegen目录,至少包含 `<model>.h`、`<model>_private.h`、`<model>.c`
- 若用户需要testpoint枚举或getter生成,还应包含 `motrace.json`
- 必须把codegen目录视为事实来源
- 禁止在可读codegen目录的情况下靠记忆臆造端口、step函数或testpoint
- 必须汇报metadata回看结果,包括model stem、输入/输出、testpoints和warnings
- 自然语言testpoint匹配(`--testpoint-nl`)是启发式的;必须在使用前说明

## 工具与边界

### 主脚本
| 脚本 | 用途 |
|------|------|
| `scripts/render_svdpi.py` | 从codegen目录生成SV-DPI wrapper文件 |

### 常用命令
| 命令 | 用途 |
|------|------|
| `python render_svdpi.py --codegen-dir <dir> --api-prefix model --force` | 就地生成wrapper |
| `python render_svdpi.py --codegen-dir <dir> --list-testpoints` | 列出testpoint候选 |
| `python render_svdpi.py --codegen-dir <dir> --testpoint-nl "<描述>" --force` | 按自然语言生成testpoint |
| `vsim -c -do "do ./simulate.do"` | 运行smoke验证 |
| `vsim -view waves.wlf` | 查看波形 |

### 外部工具
| 工具 | 用途 |
|------|------|
| ModelSim / Questa | Smoke test和波形检查 |
| Python | 脚本执行wrapper生成 |

## 辅助脚本

| 脚本 | 用途 |
|------|------|
| `scripts/render_svdpi.py` | 从codegen目录生成SV-DPI wrapper文件的核心生成器 |

## 引用导航

本Skill由脚本驱动,无独立`references/`文件;所有执行指导嵌入在本`SKILL.md`和脚本自带帮助中。

## 任务入口

本Skill无独立workflow文件;所有任务遵循下方核心工作流,由`scripts/render_svdpi.py`驱动。

## 模板与资产

- 随包示例模型:`model/McpComplexMixer.mo` (仅用于复现演示;不是codegen目录)

## 工作流

### 阶段 1:先确认边界

**GATE**:用户已提出SV-DPI wrapper生成、testpoint处理或仿真验证任务。

1. 确认任务是"基于已有codegen目录生成wrapper"。
2. 如果codegen目录还不存在,先停下并回到Sysplorer codegen前置步骤。
3. 如果codegen已存在,就把该目录视为事实来源。

**Checkpoint**:codegen目录存在性已确认;任务边界明确。

### 阶段 2:检查codegen目录

**GATE**:codegen目录已确认存在。

生成前确认必需文件存在:
- `<model>.h`
- `<model>_private.h`
- `<model>.c`

如果任务涉及testpoint,再检查:
- `motrace.json`

只要codegen目录可读,就不要靠记忆臆造端口、step函数或testpoint。

**Checkpoint**:必需文件已存在;codegen目录可读。

### 阶段 3:运行随包生成脚本

**GATE**:codegen目录检查已完成。

默认在codegen目录内就地运行:
```powershell
python <path-to-skill>\scripts\render_svdpi.py `
  --codegen-dir <generated-code-dir> `
  --api-prefix model `
  --force
```

只有在用户明确要求输出到其他目录时,才切换到 `--output-dir`。

**Checkpoint**:wrapper生成脚本已执行。

### 阶段 4:回看metadata

**GATE**:生成已完成。

生成后必须检查 `_svdpi_metadata.json`,至少汇报:
- 推断出的model stem
- 识别到的输入和输出
- 是否支持CSV compare模式
- 选中的testpoint
- warnings

如果 `_svdpi_metadata.json` 里还有unresolved testpoint或关键结构警告,不要只因为文件生成成功就宣称任务完成。

**Checkpoint**:metadata回看完成;任何警告或未解决项已记录。

### 阶段 5:处理testpoint

**GATE**:metadata已回看。

如果用户要testpoint:
- 优先使用精确 `--testpoint` id。
- 如果用户给的是自然语言,只能在先说明"这是启发式匹配"后再用 `--testpoint-nl`。
- 如果自然语言匹配出了结果,先汇报匹配到的 `motrace` id,再给出最终结果。

列出候选:
```powershell
python <path-to-skill>\scripts\render_svdpi.py `
  --codegen-dir <generated-code-dir> `
  --list-testpoints
```

**Checkpoint**:testpoint处理完成;所有启发式和警告已披露。

### 阶段 6:执行仿真与交付

**GATE**:wrapper、testpoint和可选仿真已完成。

按固定顺序推进:

1. **按需仿真**:用户要求验证时,运行 `vsim -c -do "do ./simulate.do"`;除非要求更强校验标准,否则表述为smoke test。
2. **回看生成文件**:确认标准生成产物存在(dpi.h、dpi.c、dpi_pkg.sv、dpi.sv、tb.sv、_svdpi_metadata.json;启用仿真辅助时还包括simulate.do和wave.do)。
3. **交付**:按标准输出格式组织交付(边界检查 -> 检测到的Codegen事实 -> 生成命令 -> 生成文件 -> Metadata回看 -> 验证结果 -> 风险与下一步)。

**Checkpoint**:完整交付,包含执行动作、生成文件、metadata回看和任何风险或下一步。

## 结果要求

- 必须说明边界检查结果和codegen目录事实。
- 必须说明生成命令和生成的文件。
- 必须说明metadata回看结果,包括model stem、输入/输出、testpoints和warnings。
- 如果执行了仿真,必须说明验证结果。
- 必须说明风险、未解决testpoint、启发式警告和下一步建议。

## 当前限制

- testpoint getter目前只支持那些能从 `motrace.json` 稳定映射出来的标量候选。
- 自然语言匹配是启发式的,不应在未回看结果前当作权威结论。
- `tb.sv` 只有在所有根输入都是标量时才会进入CSV compare模式。
- `simulate.do` 默认面向常见Sysplorer codegen布局,定制环境下可能仍需手工调整。
- Julia相关产物目前只做透传,不由本Skill负责构建。
