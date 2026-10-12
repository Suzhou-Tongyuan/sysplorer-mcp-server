# Skill 文件清单

| 字段 | 内容 |
|------|------|
| **创建时间** | 2026-04-16 |
| **版本** | 1.5.0 |

---

每个 Skill 包中**必须**包含以下 5 个核心文件：

| 序号 | 文件名 | 语言要求 | 说明 |
|------|--------|----------|------|
| 1 | `SKILL.md` | **全英文** | Skill 主描述文件，用于 MCP/Agent 系统识别和调用 |
| 2 | `SKILL_ZH.md` | **主要描述为中文** | 中文版本的 Skill 描述，用于中文用户审核参考 |
| 3 | `版本说明.md` | 中文 | 版本变更记录、更新历史 |
| 4 | `使用说明.md` | 中文 | 用户使用指南、快速开始、注意事项 |
| 5 | `skill_info.json` | 中英混合 | 结构化元数据文件 |

---

## 各文件详细要求

### 1. SKILL.md（英文版）

**语言要求**：全英文编写

**必须包含 YAML frontmatter**：
```yaml
---
name: skill-name-kebab-case
description: English description (full feature explanation)
metadata:
  short-description: English short description (≤50 chars)
  version: X.Y.Z
---
```



### 2. SKILL_ZH.md（中文版）

**语言要求**：主要描述为中文，可保留相关英文单词、关键词、代码块、Modelica 标识符等

**必须包含**：
- 文件顶层添加说明：`> 本文件仅用于中文审核参考，实际任务执行请调用 SKILL.md`
- 与 SKILL.md 结构对应
- 保持与英文版功能描述一致

---

### 3. 版本说明.md

**语言要求**：中文

**内容要求**：
- 版本变更记录（日期、版本号、变更内容）
- 首次版本记录格式：
```markdown
## v1.0.0 (2026-04-16)
- 初始版本发布
```

---

### 4. 使用说明.md

**语言要求**：中文

**内容要求**：
- 快速开始指南
- 使用场景说明
- 注意事项与常见问题

---

### 5. skill_info.json

**语言要求**：中英混合

**字段规范**：
```json
{
  "英文名": "skill-name-kebab-case",
  "中文名": "Skill 中文名称",
  "版本号": "X.Y.Z",
  "中文功能定位": "最大50字符的功能描述",
  "英文功能定位": "English description (max 50 words)",
  "中文分类": "流程与指南类 / Sysplorer物理模型建模与调试 / Sysblock框图模型建模与调试 / 文档检索（可选）",
  "英文分类": "Workflow & Guide / Sysplorer Physical Modeling & Debugging / Sysblock Diagram Modeling & Debugging / Documentation Retrieval (Optional)"
}
```

**填写要求**：
- 中文功能定位严格控制在 **40字左右**（35-45字）
- 分类从以下类别中选择：
  - `流程与指南类` / `Workflow & Guide`
  - `Sysplorer物理模型建模与调试` / `Sysplorer Physical Modeling & Debugging`
  - `Sysplorer 能源系统建模与调试` / `Sysplorer Energy-System Modeling & Debugging`
  - `Sysblock框图模型建模与调试` / `Sysblock Diagram Modeling & Debugging`
  - `设计优化与参数估计（脚本）` / `Design Optimization & Parameter Estimation (Scripting)`
  - `建模范式与路径路由` / `Modeling Path Router`
  - `文档检索（可选）` / `Documentation Retrieval (Optional)`

---

## 分类标准参考

| 分类 | 适用场景 | 示例 |
|------|----------|------|
| **流程与指南类** | 提供开发流程、评审规范、最佳实践 | modelica-library-workflow |
| **建模必须遵守的规范** | Modelica / Sysblock 判别、门禁与工具分工（**须遵守**） | ty-sysplorer-modeling-rules |
| **文档检索（可选）** | 产品帮助中心 / MDS 远程检索；登录门禁；失败不阻断建模 | sysplorer-mds-docs |
| **设计优化与参数估计（脚本）** | DesignOptMpe、MPE、批量仿真、模型试验、响应优化、敏感度分析与 MCP 协同 | ty-design-opt-mpe-modeling, ty-design-opt-exp-gui-modeling, ty-design-opt-exp-modeling, ty-design-opt-mro-modeling, ty-design-opt-psa-modeling |
| **Sysplorer物理模型建模与调试** | 针对特定物理领域进行建模与仿真调试；含 CAD 几何驱动建模与 TA 车辆库 | ty-hydraulic-pneumatic-modeling, ty-mechanical-modeling, ty-thermofluid-modeling, ty-nps-library-modeling, ty-cadtool-modeling, ta-vehicle-modeling |
| **Sysplorer 能源系统建模与调试** | TY 光伏/风电/电池/综合能源库范围内的能源系统建模与排障 | ty-energy-modeling |
| **Sysblock框图模型建模与调试** | Sysblock 框图建模、Simulink 导入、代码生成、信号处理、批量参数对象配置与验证 | ty-sysblock-diagram-modeling, ty-sysblock-signal-modeling, ty-sysblock-batch-param-modeling, ty-sysblock-svdpi-codegen, ty-simulink-importer-modeling |
| **建模必须遵守的规范** | Modelica 与 Sysblock 判别、门禁与工具分工，**非建议而是约束**（非域内操作细则） | ty-sysplorer-modeling-rules |

---

## 验收标准

每个 Skill 包最终必须满足：
- ✅ 5 个核心文件齐全（SKILL.md、SKILL_ZH.md、版本说明.md、使用说明.md、skill_info.json）
- ✅ SKILL.md 全英文编写，含标准 YAML frontmatter
- ✅ SKILL_ZH.md 主要描述为中文，与 SKILL.md 结构对应
- ✅ skill_info.json 字段完整，中文功能定位 40 字左右
- ✅ skills目录.md 与各 Skill 信息一致
