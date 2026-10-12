# mdsSearch tool protocol (`sysplorer-search`)

Contract mirrors Sysplorer host `libs/host/mds-search-tool`. This is **not** `user-sysplorer`’s `resources_retrieval`.

## Identity

| Item | Value |
|------|--------|
| MCP namespace | `sysplorer-search` |
| Tool name | `mdsSearch` |
| Agent arguments | **Only** `query: string` (required) |
| Host-injected (do not pass) | `baseUrl`, `storeName`, `appId`, token, `topK`, score threshold, etc. |
| Preconditions | `mdsSearch` appears in the current session tool list. If absent → unavailable (do not invent reasons). |
| Purpose | Tutorials / concepts / principles / troubleshooting / best practices (**documentation Q&A**) |
| Not for | Concrete function signatures; primary modeling execution (build/check/simulate a deliverable model) |

## Call shape

```json
{
  "name": "mdsSearch",
  "arguments": {
    "query": "<约100字的假设性答案，连贯自然语言>"
  }
}
```

## Query rewriting (hard)

`query` **MUST** be a short **hypothetical answer** (~100 Chinese characters, coherent prose) that restates what a good doc paragraph would say.

| Rule | Detail |
|------|--------|
| MUST | Rewrite the user question into an assumed answer |
| MUST NOT | Keyword soup (`connector 变量 区别 Modelica`) |
| MUST NOT | Paste the user question unchanged |
| MUST NOT | Empty string or whitespace-only (host: 未提供搜索查询) |
| On retry | **MUST** change `query`; identical args forbidden |

Use `doc-taxonomy.md` only to **choose which facts** to weave into the hypothetical answer—not as the `query` itself.

Full examples: `query-examples.md`.

## When to call / not call

**Call** when the user’s **main goal** is documentation Q&A: 概念 / 教程步骤 / 原理 / 故障原因 / 官方示例说明 / 最佳实践, or they explicitly ask to consult official help first. User need not say MDS.

**Do not primary-call** when:

- Main goal is to create, author, check, compile, simulate, modify, or debug a concrete model (even if phrased as「怎么建/怎么做」) → modeling skills; MDS only as auxiliary mid-flow
- Named ModelingPy / Sysplorer API usage, parameters, return values → `get_api_document`
- Operating the currently open model / changing parameters without a help-Q&A ask
- `mdsSearch` is not in the tool list

## Success payload

`content[0].text` is a JSON array. Elements roughly:

```json
[
  {
    "content": "文档摘要…",
    "score": 0.87,
    "metadata": {
      "title": "标题",
      "external_link": "https://www.tongyuan.cc/docs/… 或 https://chat.tongyuan.cc/topic/…",
      "location": "内部路径或 tags:案例库, topic_id:348（不是用户超链接）"
    }
  }
]
```

| Field | Role |
|-------|------|
| `metadata.external_link` | **User-facing hyperlink** — same field the product UI opens; put this in the 链接 column |
| `metadata.location` | Internal dedupe / source id (path or tags); **not** for the 链接 column |
| `metadata.title` | Title for the 描述 column |

Host-side (informational; Agent does not configure): default score threshold ~0.5; entries with `image_url` dropped; dedupe by `location`; up to ~10 hits.

After a successful call with ≥1 hit, the Agent’s **first** reply is incomplete until it ends with `| 序号 | 描述 | 链接 |` where **链接 = `metadata.external_link`**. Do not paste `location` / `tags:…` into 链接 — see `answer-contract.md`.

## Failure / empty

| Case | Agent action |
|------|----------------|
| `mdsSearch` not in tool list | Fallback immediately; do not invent availability reasons |
| Structured `toolError`「未找到相关内容」+ suggestions | Rewrite `query` once per suggestions, then fallback / answer |
| Network / timeout (~10s) / HTTP errors | Rewrite `query` at most once, then fallback or answer from other sources with a caveat |
| Same `query` already failed | Never resend identical arguments |

## Fallback chain

1. `resources_retrieval` (local corpora on `user-sysplorer`—different tool)
2. `get_lib_model_document` / `get_api_document` when applicable
3. Skill / modeling-rules `references/`

Never block Gate / check / translate / simulate because MDS failed.

## Relation to other tools

| Need | Tool |
|------|------|
| Help-center RAG (tutorials, concepts, …) | `sysplorer-search` → `mdsSearch` |
| Local MCP corpora | `resources_retrieval` |
| Loaded class doc panel | `get_lib_model_document` |
| ModelingPy / API Help | `get_api_document` |
