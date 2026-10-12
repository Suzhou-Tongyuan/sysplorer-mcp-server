# mdsSearch query examples

`query` = ~100-character **hypothetical answer** in natural language. Taxonomy seeds inform content; they are not the query string.

## ✅ Good: concept / workflow

User:「Modelica 里 connector 和普通变量有什么区别？」

```json
{
  "query": "在 Modelica 中，connector 用于定义组件之间的物理接口，携带势变量与流变量并遵循连接方程；普通变量只在组件内部使用，不参与跨组件连接。connector 出现在 connect 语句中以建立拓扑连接，而普通 Real/Integer 等变量用于内部计算与状态。正确区分二者有助于避免连接错误与接口设计混乱。"
}
```

## ✅ Good: troubleshooting

User:「仿真一开始就发散怎么办？」

```json
{
  "query": "仿真启动即发散常见原因包括初始条件不一致、刚性系统步长过大、代数环未处理、以及连接或方程导致的奇异系统。排查时应先检查初始化日志与残差，确认初始值是否满足约束；再尝试减小步长或更换求解器，并检查是否存在错误的 connect 或过约束方程。文档通常建议从初始一致性与求解器配置两方面入手。"
}
```

## ✅ Good: best practice

User:「怎么组织大型 Modelica 库比较好？」

```json
{
  "query": "大型 Modelica 库宜按领域分包，用 package.mo 建立层次，公共接口放在顶层可见包中，实现细节放在内部包。命名应稳定且避免循环依赖；版本与依赖用注解或库清单管理。文档与示例模型应与库结构对应，便于检索与复用。遵循清晰分层可降低耦合并提升可维护性。"
}
```

## ✅ Good: product how-to (help-center column)

User:「FMU 怎么导入到 Sysplorer？」

```json
{
  "query": "在 Sysplorer 中导入 FMU 需使用仿真集成工具中的 FMU 导入功能，选择符合 FMI 标准的 FMU 文件并完成接口映射后加载到模型环境。导入后应检查端口类型与求解模式是否匹配，必要时调整仿真配置。帮助文档通常按导入步骤与注意事项说明常见失败原因。"
}
```

## ❌ Bad: keyword concatenation

```json
{ "query": "connector 变量 区别 Modelica connect" }
```

## ❌ Bad: paste user question

```json
{ "query": "Modelica 里 connector 和普通变量有什么区别？" }
```

## ❌ Bad: use as function handbook

```json
{ "query": "TranslateModel 函数的参数列表和返回值是什么" }
```

Use `get_api_document` / `ListFunctions` instead—not `mdsSearch`.

## ❌ Bad: empty / whitespace

```json
{ "query": "   " }
```

Host returns 未提供搜索查询.

## Retry rule

If the first call returns no hits or fails, rewrite the hypothetical answer (different angle, add product terms from `doc-taxonomy.md`, drop filler)—**never** resend the identical `query`.
