# Resources 资源目录说明

本目录存放MWorks MCP Server的外部业务资源文件，与打包后的exe同级，用户可以自行更新和管理。

**与工作区分离**：查阅 RAG 语料时使用本目录（或 `MCP_RESOURCES_DIR`）；新建/保存 Modelica 模型、`src/`、`private_lib/` 等应在 **Agent 工程工作区**（`MCP_WORKSPACE_DIR` / `--workspace-dir`），不要默认写到 exe 目录。

## 目录结构

```
resources/
├── resources_manifest.json    # 资源清单配置文件（核心，AI自动识别资源类别）
├── README.md                  # 本说明文件
├── modeling_rules/            # 建模分流规则 + Modelica 规范副本（exe 旁可读）
│   ├── modeling_path_router.md   # Modelica vs Sysblock 判别与流程
│   └── modelica_style_guide.md   # 与 .claude/modelica_style_guide.md 同步的规范全文
├── design_opt_mpe_api/        # DesignOptMpe（参数设计 / 估计 / 优化）语料
│   ├── DesignOptMpe.md            # 接口用途、顺序与参数
│   ├── 参数估计使用说明.md         # 参数估计与标定实操、流程与常见问题
│   ├── 参数估计demo说明.md         # Demo 步骤说明
│   └── 其他 .py / .json / .html 等示例与辅助材料
├── cad_toolbox_api/           # CAD 工具箱 API 说明（与主 ModelingPy ListFunctions 分离）
│   └── CADToolbox.md 等，供 run_script 中 `cadtool.ListFunctions()` / `help(cadtool.xxx)` 的补充说明与检索
├── simulink_importer_api/     # Simulink 导入（SimulinkImporter）API 说明
│   └── SimulinkImporter.md 等，`slximport.ListFunctions()` / `help(slximport.xxx)` 的补充说明与检索
├── SysplorerAPI/              # （可选）本地 API 说明 Markdown；**未**列入 RAG 清单，请用 MCP `mworks_sysplorer_get_api_document` 等工具
├── private_lib/               # （可选）随包示例；**未**列入 RAG；工程内真实 `private_lib/` 在工作区根，读 `MetaDataLib.json` + `mworks_sysplorer_get_lib_model_document`
├── 商业库已有素材/             # 商业Modelica库素材
│   └── 商业库的模型清单、组件列表、使用说明、文档资料等
├── modelica_libraries/        # 公共Modelica模型库（可选）
│   └── 开源/公共的Modelica模型库文件
├── engineering_docs/          # 工程文档（可选）
│   └── 项目需求、设计文档、规范手册、工程报告等
├── reference_docs/            # 参考文档（可选）
│   └── 技术论文、行业标准、学术资料、参考手册等
└── indexes/                   # AI自动生成的RAG索引文件（无需手动修改）
    └── 各个资源类别的独立索引文件
```

## 资源清单配置 (resources_manifest.json)

该文件是AI识别资源的核心配置，每个资源类别包含以下字段：
- `id`: 唯一标识
- `name`: 显示名称
- `description`: 详细描述
- `path`: 相对于resources目录的路径
- `index_file`: 索引文件存放位置（自动生成）
- `supported_extensions`: 支持的文件扩展名
- `query_keywords`: 触发该类别搜索的关键词列表
- `priority`: 搜索优先级（数字越小优先级越高）

## 使用说明

1. **添加新资源**：将对应文件放入相应目录即可，AI会自动识别并在需要时构建索引
2. **更新资源**：修改文件后，下次搜索时会自动检测变更并重建索引
3. **新增资源类别**：在`resources_manifest.json`中添加新的类别配置
4. **手动重建索引**：调用 `mworks_sysplorer_resources_retrieval(action="search", ...)` 时设置 `rebuild_index=true` 即可

## 搜索规则

AI会根据用户查询内容自动选择最合适的资源类别：
- 用户要**搭建/编辑模型**时 → 先读 `modeling_rules/modeling_path_router.md`，再按需检索 `modeling_rules`；**Sysplorer Python API** 说明请用 **`mworks_sysplorer_get_api_document`**，**已加载库模型类文档**请用 **`mworks_sysplorer_get_lib_model_document`**
- Sysblock **块用法** → 检索语料 **`sysblock_model_library`**（须显式指定 `sources` / 专用索引，见 `modeling_path_router.md`）
- 查询包含「参数估计」「参数优化」「MPE」「DesignOptMpe」或「API」「脚本」「run_script」等 → 搜索 `design_opt_mpe_api`（优先可读 **`design_opt_mpe_api/参数估计使用说明.md`**）；**CAD 工具箱**相关 → 搜索 `cad_toolbox_api`；**Simulink 导入 / SLX** → 搜索 `simulink_importer_api`
- 查询包含"商业库"、"模型清单"等关键词 → 搜索 `商业库已有素材`
- **私有库元数据 / 组件选型** → 使用工作区 **`private_lib/MetaDataLib.json`** 列出候选 **`fqname`**，再 **`mworks_sysplorer_get_lib_model_document`** 拉取 Sysplorer 类文档；**不**再通过本目录 `resources/private_lib/` 做 RAG
- 其他业务相关查询 → 按 `default_sources` 与清单优先级搜索

## 注意事项

- **打包发布**：`install/build.ps1`（及 `install/build_publish.ps1`）将仓库根目录 **`resources/` 整树**复制到发布目录旁的 `resources/`，`design_opt_mpe_api/` 下新增或更新的 Markdown（如 `参数估计使用说明.md`）会**自动**随包同步，无需改 PyInstaller `.spec` 或单独配置复制列表。发布包内的 **`README.md`** 来自 **`install/windows/README.md`**。
- 不要修改`indexes/`目录下的文件，这些是AI自动生成的索引文件
- 大文件（>8MB）会被自动跳过，建议拆分大型文档
- 支持的文件格式：.mo, .md, .txt, .json, .yaml, .yml, .rst, .html, .htm, .pdf, .docx, .doc, .xlsx, .xls
