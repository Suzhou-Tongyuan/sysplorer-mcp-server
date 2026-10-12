# Sysplorer Modeling Toolset

本目录放置建模 skill 直接调用的脚本。

## Script Index

| Area | Primary scripts | Purpose |
|------|-----------------|---------|
| Source conversion | `pdf_to_md.py`, `doc_to_md.py`, `ppt_to_md.py`, `web_to_md.py`, `web_to_md.cjs` | 将用户源材料统一转换为 Markdown |
| Project bootstrap | `init_modeling_project.py` | 创建建模任务目录结构 |
| Source audit | `audit_modelica_source.py` | 检查固定 Modelica 版本、授权包依赖、禁止的完整案例继承和连接数 |

## High-Frequency Commands

```bash
python3 scripts/pdf_to_md.py <file.pdf>
python3 scripts/doc_to_md.py <file.docx>
python3 scripts/ppt_to_md.py <deck.pptx>
python3 scripts/web_to_md.py <url>
node scripts/web_to_md.cjs <url>
python3 scripts/init_modeling_project.py <project_name>
```

## 车辆源码审计

独立模型直接审计 `.mo`；包内模型用显式 `--dependency-root` 指定已获准读取的顶层包目录：

```bash
python3 scripts/audit_modelica_source.py path/to/model.mo
python3 scripts/audit_modelica_source.py path/to/VehicleLib/Tests/DriveTest.mo --dependency-root path/to/VehicleLib --allowed-library TAEconomy
```

- 未传 `--dependency-root` 时仅读取目标文件，不自动追溯父目录。传入后仅读取目标至该根之间的 `package.mo`，根和模型须属于已授权范围；解析后越界的链接或不完整包链返回错误，不递归扫描其他包。
- 独立模型或授权包上下文必须绑定 `Modelica 4.0.0.TY.1`；任一可见冲突均报错。包内模型不必重复顶层包依赖，输出列出实际读取的证据文件。
- 完整案例/架构的直接限定名 `extends` 通过词法扫描识别，支持同行、跨注释及绝对限定名；字符串和注释中的示例不参与匹配。该静态审计不替代 Sysplorer 对完整 Modelica 语义的检查。
- `--min-connects` 默认仍为 `1`，原连接数判定规则不变。审计不通过时不得继续检查、翻译或仿真。

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
