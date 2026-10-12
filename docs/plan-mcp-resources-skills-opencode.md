# 计划：MCP 初始化与语料 Skills 化及 OpenCode 同步

> 文档性质：需求分析与实施计划（非已交付变更说明）  
> 拟定日期：2026-04-20  
> 关联仓库路径：`resources/`、`resources/modeling_skills/`、`sysplorer-mcp-server/`、`install/`

---

## 1. 背景与目标

当前 MCP 在启动时通过读取旁置 `resources/resources_manifest.json`，将「旁置文档语料」摘要拼入 FastMCP 的 `instructions`（见 `sysplorer-mcp-server/mcp_instance.py` 与 `core/resources_manifest.py` 中 `browse_resources_manifest_for_instructions`）。计划改为：**初始化 instructions 不再依赖 resources 内任何文件**；语料仍保留在 `resources/`，供 **`resources_retrieval` 等 RAG 工具**按需检索。

同时，将 **`modeling_rules`**、**`design_opt_mpe_api`**（正文已收敛至对应 Skill `references/`）与 **`SysblockModelLibrary`** 等语料中的**可执行知识**提炼并改造为符合 **`resources/modeling_skills` 既有规范**的 Agent Skills，并更新清单文档；安装流程需按 **OpenCode 官方 skills 发现规则**，把 skills 部署到其可自动发现的**全局**位置。

---

## 2. 需求 1：MCP 初始化不再读取 resources 文件

### 2.1 现状

- `mcp_instance.py` 在成功导入时调用 `browse_resources_manifest_for_instructions()`，将返回的 Markdown 片段 `_DOC_CORPORA_FRAG` 追加到 `instructions`。
- 失败或缺失 manifest 时仍有降级片段（提示用 `resources_retrieval`）。
- `_PATH_HINT` 中仍包含对 `get_resources_root()` 的路径说明及「Agent Skill 语料」段落，其中明确引用 `resources_manifest.json` 生成的摘要。

### 2.2 目标行为

- **禁止**在默认 `instructions` 中嵌入来自 `resources/` 下任意文件的内容（包括但不限于 `resources_manifest.json`、从 manifest 衍生的类别列表、索引路径列表等）。
- **`resources/` 目录及 `resources_manifest.json` 仍须存在**（或与现有打包/部署约定一致地旁置），供：
  - `resources_retrieval`（及依赖 manifest 路径解析的其它工具）在 AI **主动调用**时使用；
  - 索引重建脚本等运维流程使用。

### 2.3 建议实施步骤

1. **修改 `mcp_instance.py`**  
   - 移除或条件关闭对 `browse_resources_manifest_for_instructions` 的调用，使 `instructions` 仅保留 `_BASE_INSTRUCTIONS`、**必要的**路径与安全约束（`ClearAll` / `ChangeDirectory` 等），以及**不读取磁盘语料文件**写死的简短指引（例如：需要文档时调用 `resources_retrieval`，勿在会话开头全文扫描语料）。
2. **审阅 `_PATH_HINT`**  
   - 保留「工作区 / 语料根目录」路径提示是否有价值（仅路径、不读文件一般可接受）；若其中句子仍暗示「必须读 manifest」，改为与工具调用一致的表述。
3. **回归与文档**  
   - 确认 `resources_retrieval(action="corpora")` 在无 manifest 时的错误提示仍清晰（`tools/docs.py` 等）。  
   - 更新 `resources/README.md`、`MCP工具与Skills测试说明.md` 等若仍写「instructions 内含 manifest 摘要」的表述。
4. **可选：日志**  
   - 若移除浏览 manifest，可去掉或降级 `resources manifest browsed` 类 WARNING，避免误导运维认为仍在注入 instructions。

### 2.4 风险与注意

- 依赖「会话一开 instructions 里就有完整语料 id 列表」的客户端行为将消失；需在 instructions 中**一两句话**引导使用 `corpora`/`search`，并与产品侧预期对齐。
- `core/resources_manifest.py` 本身可保留，供 RAG 与脚本使用；仅切断「instructions 装配」这条链路。

---

## 3. 需求 2：语料 Skills 化并放入 `modeling_skills`

### 3.1 源语料范围

| 来源 | 路径（仓库内） | 知识类型（概括） |
|------|------------------|------------------|
| DesignOpt / MPE | `resources/modeling_skills/ty-design-opt-mpe-modeling/references/*.md`（RAG：`corpus_id=design_opt_mpe_api`） | 参数设计、参数估计、优化相关脚本与流程说明 |
| 建模规则 | `resources/modeling_skills/ty-sysplorer-modeling-rules/references/*.md`（RAG：`corpus_id=modeling_rules`） | **须遵守**的 Modelica / Sysblock 风格、七门闸、路径分流、与 MCP 工具分工 |
| Sysblock 模块库说明 | `resources/SysblockModelLibrary/**/*.md` | 各模块文档化说明（体量大、偏参考手册） |

### 3.2 目标形态（与现有 `modeling_skills` 一致）

每个新 Skill **一个子目录**，且满足 `resources/modeling_skills/Skill文件清单.md` 中的五项核心交付物：

- `SKILL.md`（英文 + YAML frontmatter，`name` 与目录名一致且符合 OpenCode 命名：`^[a-z0-9]+(-[a-z0-9]+)*$`）
- `SKILL_ZH.md`
- `版本说明.md`
- `使用说明.md`
- `skill_info.json`

可另设 `references/`、`workflows/`、`docs/` 等，通过 `SKILL.md` 内链接引用（与现有 `ty-*` skills 一致）。

### 3.3 建议拆包策略（待评审）

为避免单个 Skill 过载，建议**至少**拆为两个独立 Skill（名称仅为建议，实施时以 `skill_info.json` 与 frontmatter 为准）：

1. **`ty-design-opt-mpe-modeling`（建议名）**  
   - 吸收 `ty-design-opt-mpe-modeling/references/` 内流程、API 要点、常见错误与 demo 说明。  
   - 原文档可迁入 `references/` 或 `docs/` 作为附录，**`SKILL.md` 写可执行摘要**（何时用何工具、与 `session_manager` / 仿真脚本等配合）。

2. **`ty-sysplorer-modeling-rules`**（建模**必须遵守**的规范，语料同 `modeling_rules`）  
   - 定位：**总规则与范式路由**，覆盖 `modeling_rules` 全量：会话/任务**开头**即判断当前应走 **Sysplorer Modelica** 路线还是 **Sysblock 框图**路线（及与之相关的风格、工具链与禁忌），再进入对应领域 Skill；**不等同于** Sysblock 子域专用规则。  
   - 吸收 `modeling_rules` 四条（Modelica / Sysblock 风格、七门闸、路径路由、与 MCP 工具分工等），在 `SKILL.md` 中把「范式选择 → 再选下游 skill / 语料」写清。  
   - **与现有 Sysblock 系列 skills 的边界**：本 Skill 负责**选路与通用约束**；`ty-sysblock-diagram-modeling` / `ty-sysblock-signal-modeling` 等负责框图域内**具体操作、模板与验证闭环**；通过交叉引用避免重复维护。

**`SysblockModelLibrary`**：全文搬进 Skill 不现实。推荐做法：

- 在 Skill 中写 **「如何查块」**：优先 MCP 的 `get_lib_model_document`、必要时 `resources_retrieval` 指定 `sysblock_model_library` 语料与索引；**不在 SKILL 正文堆全库**。  
- 可选：增加 **`references/sysblock-library-index.md`**（仅高层分类与检索策略），或保留语料于原 RAG 路径，Skill 只描述策略。

### 3.4 与 `resources_manifest.json` 的关系（Skills 化之后）

- 若各语料的知识已浓缩进 skills，可考虑在 manifest 中**降低重复**或仅保留 Skill `references/` 作 RAG 细查（产品决策项，本计划不强制）。  
- **`sysblock_model_library`** 大概率仍以 RAG 大块语料存在；Skill 负责教「怎么查」。

### 3.5 质量与维护

- 中英文 `SKILL.md` / `SKILL_ZH.md` 与 `版本说明.md` 初始版本对齐。  
- 触发词、禁止项（如 `SetModelText`、`ClearAll`）与现有 `modeling_path_router.md` 等**一致**，避免 skills 与 rules 文档矛盾。

---

## 4. 需求 3：更新 `Skill文件清单.md` 与 `Skills汇总.md`

- 路径：`resources/modeling_skills/Skill文件清单.md`、`resources/modeling_skills/Skills汇总.md`（若根目录另有同名文件，以实际权威路径为准，与需求描述一致即可）。
- 内容更新要点：
  - 增加新 Skill 条目：中文名、英文名、短描述、版本、触发场景。
  - 调整 **Skill 总数**、分类表（若新增「设计优化 / 通用规则」类）。
  - 若有「仅 RAG、非 Skill」的说明，与需求 1 后的 instructions 行为一致化。

---

## 5. 需求 4：安装 MCP 时同步 `modeling_skills` 至 OpenCode 全局 skills

### 5.1 OpenCode 官方规则（摘要）

依据 [OpenCode Agent Skills 文档](https://opencode.ai/docs/skills)：

- 全局路径之一：**`~/.config/opencode/skills/<skill-name>/SKILL.md`**（Windows 即 `%USERPROFILE%\.config\opencode\skills\...`）。
- 每个 skill 为**独立子目录**，目录名须与 `SKILL.md` frontmatter 中 `name` 一致，且符合小写 kebab-case 等规则。
- Skills 通过 OpenCode 的 **`skill` 工具**按需加载；可与 `opencode.json` 中 `permission.skill` 配合。

### 5.2 与仓库目录的映射、版本更新与「整包 + 版本号」是否可递归

仓库中为：`resources/modeling_skills/<skill-dir>/SKILL.md`（如 `ty-sysblock-diagram-modeling/`）。

安装时应将 **每个** `<skill-dir>` **复制或同步**到全局：

- **目标父目录**：`%USERPROFILE%\.config\opencode\skills\`（Linux/macOS：`$HOME/.config/opencode/skills/`）。
- **目标结构**：`.../skills/ty-sysblock-diagram-modeling/SKILL.md`（与 OpenCode 要求一致）。

#### 5.2.1 扁平同步是否会带来「版本」问题？

**会，这是刻意与 OpenCode 发现规则折衷后的工程问题**：全局目录里是**部署快照**，不自动与仓库或 MCP 安装包版本绑定。若用户长期不重新执行安装/同步，OpenCode 里看到的 skills 可能**落后于**当前 `resources/modeling_skills` 或新版 MCP 包。

**已确认（安装策略）**：在 `~/.config/opencode/skills/` 下，**先删除由 Sysplorer MCP 随包维护的全部旧版 skill 子目录，再拷贝当前随包 `modeling_skills` 中对应一级子目录**，实现**全量替换**（避免残留已下线或重命名的目录）。删除范围**仅限**本 MCP 登记的一组目录名（与随包 `resources/modeling_skills/` 下**一级** skill 包名一致，或维护显式「受管 skill 名单」），**不得**清空整个 `skills/` 根目录，以免误删用户自行安装的其它 OpenCode skill。

#### 5.2.1a 删除操作的安全性（硬要求，须重点落实）

删除 Global skills 目录下的子文件夹属于**不可逆高风险操作**，误删会直接毁掉用户其它 Agent skill。**本 MCP 安装脚本必须把「只删 Sysplorer MCP 自己的 skills」作为安全红线**，建议实现上至少满足：

- **白名单删除，禁止广域匹配**：仅允许删除**路径已解析为** `skills_root / <name>` 且 `<name>` **严格属于**随安装包内置的**受管名单**（例如与随包 `modeling_skills/` 一级子目录**完全一致**的集合，或单独随包的 `managed_opencode_skills.json` 等**只读清单**）。**禁止**对 `skills/` 执行 `*` 通配删除、`find … -delete`、或删除「不在名单里但名字相似」的目录。
- **禁止删除 `skills` 根本身**：不得对 `~/.config/opencode/skills` 这一层做 `rm -rf`；仅允许对名单内**单个子目录**逐个删除（且每个路径须经 `realpath`/规范化后仍以 `skills_root` 为前缀，防止 `..` 逃逸）。
- **删除前二次确认（对机器而言）**：对拟删目录，可选要求存在 **Sysplorer 可识别标记**再删（例如在随包规范中规定受管 `SKILL.md` 的 `metadata` 内含固定键如 `managed-by: sysplorer`；若缺标记则**跳过删除并告警**，避免删掉用户自建但同名的目录）。若采用「仅白名单、不验文件」策略，则名单**必须**唯一来源于安装包，**不得**从用户磁盘动态猜测。
- **日志与可审计**：安装日志中记录本次删除的**完整路径列表**与版本号，便于出问题时追溯；可选在删除前对受管目录做备份（§5.2.1 上文已述）。
- **代码评审与回归**：含删除逻辑的安装路径应作为发布前检查项；单测或集成测覆盖「skills 根下存在非受管目录时安装后仍存在」等用例。

建议在计划/实现层明确一种或多种策略（可组合）：

- **安装/升级 MCP 时幂等同步**：在按上款完成「先删后拷」后，各 `<skill-dir>` 与随包 `modeling_skills` **完全一致**；可选在删除前对**将被移除的受管目录**做带时间戳备份（整目录打包到用户缓存路径等）。
- **可追溯而不改路径**：在随包资源或同步脚本写入的 **`SKILL.md` frontmatter `metadata`**（或 `版本说明.md`）中携带 **MCP / 资源包版本号**；OpenCode 仍按目录名加载 skill，用户肉眼或 Agent 可读版本，无需把版本写进目录名。
- **侧车标记文件（可选）**：在 `~/.config/opencode/skills/` 下放只读文件如 `.sysplorer_mcp_skills_source_version`（内容为同步时的包版本与时间），便于排障；**不参与** OpenCode 发现逻辑。

#### 5.2.2 能否把整个 skills 放在 `.../skills/sysplorer-mcp-<版本号>/` 下并指望递归发现？

依据 [OpenCode Agent Skills 文档](https://opencode.ai/docs/skills) 的表述，发现规则是 **`~/.config/opencode/skills/*/SKILL.md`**（项目侧亦为 `.opencode/skills/*/SKILL.md`）：通配符**只有一层**，即「`skills` 的直接子目录」内必须有 **`SKILL.md`**，且该子目录名须与 frontmatter 里的 **`name` 一致**。

因此：

- 若布局为 `skills/sysplorer-mcp-1.2.3/ty-foo/SKILL.md`，则对官方描述而言，第一层目录是 **`sysplorer-mcp-1.2.3`**，期望的文件是 **`skills/sysplorer-mcp-1.2.3/SKILL.md`**，**不会**按文档保证去读更深一层的 `ty-foo/SKILL.md`。
- **不应默认假设「整包带版本号的子树可递归注册多个 skill」**；若某版本 OpenCode 实现做了递归，属于**未在文档中承诺**的行为，安装脚本不应依赖。

**若必须在磁盘上保留「带版本号的整包」**（例如审计、多版本并存），可与「OpenCode 可发现」解耦，例如：

- 将版本化副本放在**其他路径**（如 `%USERPROFILE%\.cache\sysplorer-mcp\skills-v1.2.3\`），再由安装脚本把其中每个 `<skill-dir>` **展开/同步**到 `~/.config/opencode/skills/<skill-dir>/`；或  
- 仅保留**一份**当前生效的扁平同步结果于 `skills/`，版本信息只写入 metadata / 侧车文件。

#### 5.2.3 小结

| 布局 | OpenCode 按官方文档是否可发现 |
|------|------------------------------|
| `skills/<skill-name>/SKILL.md` | 是 |
| `skills/<bundle>-<ver>/<skill-name>/SKILL.md` | **否**（多一层，不匹配 `skills/*/SKILL.md`） |
| `skills/modeling_skills/<skill-name>/SKILL.md` | **否**（同上） |

实施前若团队使用的 OpenCode 版本与文档不一致，可用本地一次验证（列出 skill 工具可见技能集）作为补充，但**产品化安装脚本应以文档单层规则为准**。

### 5.3 建议修改的安装入口

- **Windows**：`install/build_publish.ps1`、`install/install_mcp_silent.py` 或专用 post-install 步骤中增加「同步 skills」函数：**删除与拷贝均须满足 §5.2.1a**——仅对随包白名单内的 `skills_root\<name>` 逐个删除（**禁止**清空整个 `skills` 或其它广域删除），再将要安装的各一级子目录 **完整复制**到 `%USERPROFILE%\.config\opencode\skills\`。
- **Linux**：`install/linux/scripts/install_mcp.sh` 中已有 `~/.config/opencode` 与 `opencode.json` 合并逻辑，可并列增加：同上，**白名单逐目录删除**后再 **cp -a / rsync** 到 `$HOME/.config/opencode/skills/`。
- **文档**：`install/windows/README.md`、`install/linux/README.md` 增加「OpenCode 全局 skills 已同步」说明及路径；必要时在 `install/common/templates/opencode.json.example` 中注释 `permission.skill` 范例。

### 5.4 与需求 1 的协同

- OpenCode 侧通过 **skill 工具**加载结构化指导；MCP 侧 **instructions 不再塞 manifest**。  
- RAG 仍查 `resources/`；二者分工：**Skill = 流程与约束摘要**，**RAG = 原文与大块参考**。

---

## 6. 建议实施顺序（里程碑）

| 阶段 | 内容 | 产出 |
|------|------|------|
| M1 | 切断 instructions 对 manifest 的依赖 | `mcp_instance.py`（及必要文案）变更 + 简单自测 |
| M2 | 新建/编写两个（或经评审后的个数）skills 目录 | `resources/modeling_skills/<new>/` 全套规范文件 |
| M3 | 更新清单与汇总 | `Skill文件清单.md`、`Skills汇总.md` |
| M4 | 安装脚本同步 OpenCode 全局 skills（**遵守 §5.2.1a 白名单删除**） | Windows/Linux 可重复执行；非受管目录不被删 |
| M5 | 联调 | OpenCode 中可见 skill；Cursor/其它客户端连接 MCP 验证 instructions 体积与工具行为 |

---

## 7. 未决问题（实施前建议确认）

1. 新建 Skill 的 **`name` 与目录名**最终命名表（需全局唯一，且不与用户 `~/.config/opencode/skills` 已有第三方 skill 冲突时的策略）。  
2. `SysblockModelLibrary` 是**仅策略进 Skill** 还是**额外**维护一个「索引类」markdown 的接受度。  
3. **（已确认）** 安装时 OpenCode skills：在 `~/.config/opencode/skills/` 下**仅删除可证明为 Sysplorer MCP 受管的目录后，再全量拷贝新版**（见 §5.2.1、**§5.2.1a**、§5.3）；删除逻辑须通过安全评审与回归。**是否提供** `--no-sync-opencode-skills` 开关仍可产品定夺。  
4. 除 OpenCode 外，是否需同步到 `~/.claude/skills` 或 `~/.agents/skills`（OpenCode 文档列出的兼容路径）；若需要，在 M4 一并列出。

---

## 8. 参考代码与文件索引

- MCP instructions 装配：`sysplorer-mcp-server/mcp_instance.py`  
- Manifest 浏览供 instructions：`sysplorer-mcp-server/core/resources_manifest.py` → `browse_resources_manifest_for_instructions`  
- Skill 规范：`resources/modeling_skills/Skill文件清单.md`  
- 现有 Skill 示例：`resources/modeling_skills/ty-sysblock-diagram-modeling/`  
- OpenCode 安装与配置：`install/install_mcp_silent.py`、`install/linux/scripts/install_mcp.sh`  
- OpenCode skills 发现规则：<https://opencode.ai/docs/skills>
