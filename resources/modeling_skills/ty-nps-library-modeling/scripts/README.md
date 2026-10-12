# Sysplorer Modeling Toolset

本目录放置建模 skill 直接调用的脚本。

## Script Index

| Area | Primary scripts | Purpose |
|------|-----------------|---------|
| Source conversion | `pdf_to_md.py`, `doc_to_md.py`, `ppt_to_md.py`, `web_to_md.py`, `web_to_md.cjs` | 将用户源材料统一转换为 Markdown |
| Project bootstrap | `init_modeling_project.py` | 创建建模任务目录结构 |

## High-Frequency Commands

```bash
python3 scripts/pdf_to_md.py <file.pdf>
python3 scripts/doc_to_md.py <file.docx>
python3 scripts/ppt_to_md.py <deck.pptx>
python3 scripts/web_to_md.py <url>
node scripts/web_to_md.cjs <url>
python3 scripts/init_modeling_project.py <project_name>
```

## Recommendations

- Step 1 完成后，优先保留转换后的 Markdown 作为后续唯一主输入
- 多个源材料时，先全部转换，再做归并分析
- Sysplorer 建模动作优先通过 MCP，不要把 MCP 已有能力再重复造脚本
