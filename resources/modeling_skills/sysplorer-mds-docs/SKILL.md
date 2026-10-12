---
name: sysplorer-mds-docs
description: >-
  当用户的主目标是检索或讲解 MWORKS/Sysplorer 官方帮助内容（概念、教程步骤、原理、故障原因、官方示例说明、最佳实践），或明确要求先查帮助/官方文档再作答时，使用本技能：在 `mdsSearch` 可用时，将问题改写为约 100 字假设性答案作为唯一 `query` 调用 MCP `sysplorer-search` 的 `mdsSearch`，再引用作答。
  完成门禁：只要本轮 `mdsSearch` 有命中，首条回复末尾必须用三列表格输出「参考链接」：`| 序号 | 描述 | 链接 |`。链接列必须用 `metadata.external_link`（http(s) 外链）；`metadata.location` 只是内部路径/标签（如 `tags:… topic_id:…`、`sysplorer-docs-2.0/…`），禁止当作超链接填进链接列。无 `external_link` 时链接列写「（无外部链接）」。没有该三列表 = 未完成。
  不要用作主技能：用户要实际新建、编写、检查、编译、仿真、修改或调试某个具体 Modelica/Sysplorer 模型——即使话里带「怎么建/怎么做」——应走 `ty-sysplorer-modeling-rules` 与领域建模技能；仅当建模过程中需要官方依据时可辅用本技能。也不要用于 API 函数签名/参数（`get_api_document`）或单个已加载类参数面板（`get_lib_model_document`）。`mdsSearch` 是否可用只看当前工具列表；不可用则降级说明，不阻断建模。
metadata:
  short-description: Official help Q&A via mdsSearch; link column = external_link
  version: 1.8.0
  managed-by: sysplorer-mcp
---

# Sysplorer MDS help-center docs (`mdsSearch`)

## Scope

- **In scope**: Retrieve / explain official help — concepts, tutorial steps, principles, failure causes, official example explanations, best practices — via MCP **`sysplorer-search`** / **`mdsSearch`** when the tool is listed.
- **Out of scope (do not primary-trigger)**:
  - Actually create, author, check, compile, simulate, modify, or debug a concrete model → `ty-sysplorer-modeling-rules` + domain skills
  - API signatures / parameters → `get_api_document` / `ListFunctions`
  - One loaded class’s params/ports → `get_lib_model_document`

All `references/...` paths are relative to **this skill directory**.

## Trigger boundary (avoid stealing modeling skills)

| User intent | Primary skill | Role of this skill |
|-------------|---------------|--------------------|
| 「帮我建一维传动系，生成 Modelica 并检查仿真」 | Modeling skills | Do **not** primary-trigger |
| 「解释理想齿轮、扭转弹簧在一维传动里的建模原理」 | **This skill** | `mdsSearch` → answer + 参考链接 block |
| 「查官方帮助：齿轮、惯量、支承怎么连接」 | **This skill** | `mdsSearch` → answer + 参考链接 block |
| 「先按官方文档，再帮我实际搭建并仿真」 | Modeling primary | Auxiliary: search first (with links), then hand off modeling |

**Rule**: main goal = **查/讲官方帮助** → this skill. Main goal = **落地建/检/仿/改模型** → modeling skills (MDS only if official text is needed mid-flow).

Do **not** treat bare「是什么/为什么/怎么做」+ Modelica as enough to steal execution tasks like「怎么用 Modelica 开发传动系统」when the user wants a deliverable model.

Topic hints (only when the ask is documentation-Q&A): `references/trigger-scenarios.md`, `references/doc-taxonomy.md`.

## Hard rules

1. **Completion gate — source links in the same turn**: if `mdsSearch` returned ≥1 hit, the **first** user-visible reply is incomplete until it ends with a **三列** Markdown table「参考链接」：`序号 | 描述 | 链接`. The **链接** column must use `metadata.external_link` (real http(s) URL). Do **not** put `metadata.location` (internal path / `tags:…, topic_id:…`) in 链接 — that is not a hyperlink. Full template: `references/answer-contract.md`.
2. **Tool identity**: MCP `sysplorer-search`, tool **`mdsSearch`**. Pass **only** `{ "query": "<string>" }`. Do not invent `baseUrl` / `storeName` / `appId` / token / `topK`.
3. **Availability**: if `mdsSearch` is **not** in the current tool list → unavailable → fallback; do not speculate why.
4. **`query`**: ~100-character **hypothetical answer** in coherent prose — not keywords, not the raw user question. See `references/query-examples.md`.
5. **Empty / whitespace `query` invalid**. Retry after no-hit/failure **must rewrite** `query` (no identical args).
6. **Not API / class handbook**; not primary modeling executor.
7. **Never block modeling** on MDS absence or failure.

### Required link table (only this shape)

```markdown
参考链接：

| 序号 | 描述 | 链接 |
|:----:|------|------|
| 1 | 《仿真设置-输出》——控制结果输出与存储 | https://www.tongyuan.cc/docs/sysplorer/.../SimulationSettingsOutput.html |
| 2 | 《仿真实例管理》——清理结果与实例 | https://www.tongyuan.cc/docs/sysplorer/... |
```

Column rules:
- **序号**: 1…N (prefer 1–3 top-score hits that have `external_link`; dedupe by `external_link` or `location`)
- **描述**: `《metadata.title》` + optional short relevance clause (≤30 chars) from `content`
- **链接**: **`metadata.external_link` only** — paste the http(s) URL verbatim in its own cell

Field map (do not confuse):

| Payload field | Meaning | Put in 链接? |
|---------------|---------|--------------|
| `metadata.external_link` | User-facing http(s) hyperlink (same field the product UI uses) | **Yes** |
| `metadata.location` | Internal id/path (`sysplorer-docs-2.0/…`, `tags:案例库, topic_id:348`) | **No** |
| `metadata.title` | Document title | 描述 column |

If a hit has no `external_link`: either skip that row, or put `（无外部链接）` — never dump `location` / tags into 链接. Do not invent URLs.

Forbidden: two-column `| 序号 | 文档 |`; stacking `命中文档 N`; treating `location` as the hyperlink.

## Workflow

1. Decide primary intent: help-Q&A vs modeling execution. If execution → modeling skills; optionally return here only for official citations.
2. If `mdsSearch` listed → rewrite hypothetical-answer `query` → call `mdsSearch`.
3. Draft the answer (bullets/table OK) **then** append the **三列** 参考链接 table (`序号 | 描述 | 链接`) using **`external_link`**. Pre-send check: 链接 cells look like `https://…` (or `（无外部链接）`), not `tags:…` / `sysplorer-docs-2.0/…`? If wrong field used → fix before sending. On failure: rewrite once, then fallback.
4. Hand off any build/check/simulate to modeling rules + domain skills; keep the 参考链接 table in the reply.

## Fallback (`mdsSearch` missing / failed after rewrite)

1. `resources_retrieval` (local corpora; not MDS)
2. `get_lib_model_document` / `get_api_document` when those needs apply
3. Skill / modeling-rules `references/`

State that help-center text was not used.

## Reference map

| Need | Read |
|------|------|
| Good/bad `query` examples | `references/query-examples.md` |
| Tool contract / errors | `references/tool-protocol.md` |
| Doc-Q&A trigger examples | `references/trigger-scenarios.md` |
| Help-center columns | `references/doc-taxonomy.md` |
| Answer / citation format + completion gate | `references/answer-contract.md` |
