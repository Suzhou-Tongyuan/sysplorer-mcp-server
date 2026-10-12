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

## 网页转换退出状态

`web_to_md.py` 与 `web_to_md.cjs` 采用相同退出码：

- `0`：本批所有 URL 的 Markdown 已成功写入；无参数或 `-h` / `--help` 仅显示帮助，不执行转换。
- `1`：任一 URL 抓取、转换或 Markdown 写入失败，或输入清单无法读取、出现顶层运行异常。批次部分成功时保留已成功写入的文件，并列出失败 URL；不得把该批次记录为全部成功。
- `2`：命令用法错误，例如选项缺少参数、清单为空且没有其他 URL、非 HTTP(S) URL，或多 URL 与单文件 `--output` 同用。

图片下载仍为尽力处理：图片失败产生警告，Markdown 写入成功不等于所有图片均已下载。退出码只说明本次请求的转换状态，不代表网页内容正确或后续模型验证通过。Python 启动依赖缺失仍按运行错误退出；帮助和无参数行为以依赖可加载为前提。
