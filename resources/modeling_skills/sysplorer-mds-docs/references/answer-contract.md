# Answer contract

## Completion gate (read first)

A successful `mdsSearch` turn is **incomplete** until the user-visible reply ends with a **three-column** Markdown table:

`| 序号 | 描述 | 链接 |`

Critical field split (product UI already follows this):

| Field | What it is | Use in reply |
|-------|------------|--------------|
| `metadata.external_link` | Real http(s) hyperlink | **链接** column |
| `metadata.location` | Internal path / tag id (`sysplorer-docs-2.0/…`, `tags:案例库, topic_id:348`) | **Not** a hyperlink — do not put in 链接 |
| `metadata.title` | Document title | **描述** column |

Putting `location` into 链接 makes the table look like “another description column” — that is a skill failure.

## Required shape

1. **Direct answer** — short paragraph, bullets, or a compact table for the user question.
2. **参考链接 three-column table (mandatory on MDS hits)** — template below.
3. **Availability note** — only if MDS was skipped/failed.

## Using the success payload

`mdsSearch` returns a JSON array in `content[0].text`. Prefer higher `score` items; paraphrase `content`; quote at most 1–3 short lines for menu names or critical wording. Do not dump the raw JSON array to the user.

Example hit shape:

```json
{
  "content": "文档摘要…",
  "score": 0.87,
  "metadata": {
    "title": "仿真设置-输出",
    "external_link": "https://www.tongyuan.cc/docs/sysplorer/2026b/Help/.../SimulationSettingsOutput.html",
    "location": "sysplorer-docs-2.0/sysplorerHelpSourceCode/projects/DevelopingModels/Doc/.../SimulationSettingsOutput.md"
  }
}
```

## Mandatory link table (only this shape)

```markdown
参考链接：

| 序号 | 描述 | 链接 |
|:----:|------|------|
| 1 | 《仿真设置-输出》——控制结果输出与存储 | https://www.tongyuan.cc/docs/sysplorer/.../SimulationSettingsOutput.html |
| 2 | 《仿真实例管理》——清理结果与实例 | https://chat.tongyuan.cc/topic/348 |
```

### Column rules

| Column | Content |
|--------|---------|
| **序号** | 1…N (prefer hits that have `external_link`; typically 1–3) |
| **描述** | `《metadata.title》` + optional ≤30-char relevance clause from `content` |
| **链接** | `metadata.external_link` verbatim (`http://` / `https://`) |

If `external_link` is missing: skip the row **or** write `（无外部链接）`. Never invent a URL. Never use `location` / `tags:…` / `.md` paths as 链接.

Optional: 链接 cell may be a Markdown autolink so the UI stays clickable, but the URL text must remain visible in that column.

### Forbidden styles

```markdown
❌ | 序号 | 描述 | 链接 |
❌ | 1 | 《标题》——说明 | tags:案例库, topic_id:348 |
❌ | 1 | 《标题》——说明 | sysplorer-docs-2.0/.../faq_simulating.m |

❌ | 序号 | 文档 |
❌ | 1 | [《标题》](https://…) |

❌ 命中文档 1：《标题》
https://…
```

### Pre-send self-check

1. Ends with `| 序号 | 描述 | 链接 |`?
2. Every 链接 cell is `https://…` / `http://…` or `（无外部链接）`?
3. Any 链接 cell still shows `tags:` / `topic_id:` / `sysplorer-docs-2.0` / `.md` path? → Replace with `external_link` or `（无外部链接）` before sending.

Failing this check means the answer is not ready.

## Rules

| Do | Don’t |
|----|--------|
| Fill 链接 from `metadata.external_link` | Fill 链接 from `metadata.location` |
| Keep 描述 = title + short note | Treat location/tags as the hyperlink |
| Prefer 1–3 hits that have real external links | Dump every hit or raw JSON |
| Keep the table when handing off to modeling | Wait for the user to ask for links |

## Do / don’t (routing)

| Do | Don’t |
|----|--------|
| Call MDS for official-help Q&A when that is the main goal | Primary-trigger on「怎么建/生成模型并仿真」execution tasks |
| Separate “文档说法” from “我将执行的建模步骤” | Present memory as help-center fact when MDS was unused |
| Hand off modeling execution to modeling rules | Block Gate/check/simulate because MDS failed |
| Route API signatures to `get_api_document` | Use `mdsSearch` as a function handbook |
| On no-hit, rewrite `query` once | Resend identical arguments |
| Check tool list for `mdsSearch` availability | Invent login/account reasons for missing tools |

## Modeling handoff

1. Keep MDS-derived constraints (workflow steps, tool names) as requirements.
2. Keep the three-column 参考链接 table (with real `external_link` URLs) in the reply when handing off.
3. Execute with `ty-sysplorer-modeling-rules` and the domain skill.
