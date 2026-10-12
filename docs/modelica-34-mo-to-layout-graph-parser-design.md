# Modelica 3.4 `.mo` 到 Smart Layout Graph 解析器设计

## 1. 背景与目标

当前自动布线在未显式传入 `graph_json` 时，会从 `.mo` 文本中用正则提取组件声明和 `connect(...)` 语句，再生成 Smart Layout graph。该方式实现简单，但无法严格处理 Modelica 3.4 的语法结构，例如多声明、数组、修饰符、嵌套类、`public` / `protected` 分区、复杂 `annotation(...)`、字符串和注释中的分隔符等。

本文设计一个基于 Modelica 3.4 语法规则的 `.mo` 解析器，用于从 Modelica 源码生成 Smart Layout graph。解析器目标不是替代 Modelica 编译器，也不负责方程求值、类型检查或模型实例化；目标是严格按 Modelica 3.4 词法和语法切分源码，可靠抽取布局所需的结构信息。

目标：

- 严格遵守 Modelica 3.4 语法定义中的词法、`stored_definition`、`class_definition`、`composition`、`component_clause`、`equation`、`connect_clause`、`annotation` 等规则。
- 在不显式传入 `graph_json` 时，从 `.mo` 文件自动生成兼容现有 Smart Layout 的 graph。
- 覆盖常见 Modelica 建模写法：多组件声明、数组组件、复杂 modifier、嵌套 package/model、`public` / `protected` 分区、`connect` 注解、已有 `Placement` / `Line` 注解。
- 保持容错：未知或暂不使用的语法节点可保留原文并记录诊断，不应破坏可解析部分。
- 保持现有工具链兼容：`run_smart_layout_for_fast_workflow()`、`check_model()`、`translate_model()`、`simulate_model()` 的调用方式不变。

非目标：

- 不执行 Modelica 类型检查、维度推导、连接平衡检查。
- 不展开 `extends` 继承得到的 inherited connectors。
- 不求值参数表达式、条件声明、数组维度表达式。
- 不替代 Sysplorer / MWorks 的官方加载、检查和仿真能力。

## 2. 依据与约束

实现必须以 Modelica 3.4 规范为准，优先遵守官方语法定义：

- Modelica Association, *Modelica Language Specification 3.4*, HTML 版：`https://specification.modelica.org/v3.4/MLS.html`
- Modelica 3.4 Appendix B, *Modelica Concrete Syntax*：`https://specification.modelica.org/v3.4/A2.html`

实现约束：

- 第一版不新增强依赖。当前 `sysplorer-mcp-server/requirements.txt` 仅包含 `mcp>=1.0.0`，因此建议用 Python 标准库实现 lexer 与 recursive-descent parser。
- 解析器应是源码级 parser，不依赖 Sysplorer 已加载模型对象；这样可在预检布线阶段直接处理磁盘 `.mo`。
- 解析器输出必须兼容 `core.smart_layout._smart_layout_engine()` 和 `_apply_layout_graph_to_modelica_code()` 当前使用的 graph 结构。
- 解析结果必须包含 source span，便于后续精准写回和调试。

## 3. 当前实现痛点

当前实现位于 `sysplorer-mcp-server/tools/layout.py` 的 `_parse_modelica_to_graph()`，核心行为是：

- 正则匹配组件声明。
- 正则匹配 `connect(a.b, c.d)`。
- 将组件名首字母大写的实例过滤掉。
- 基于连接端点反推组件端口。

主要问题：

- 不能区分声明、方程、注解、字符串和注释中的伪匹配。
- 无法可靠处理多声明：`Resistor r1, r2(R=2);`。
- 无法可靠处理数组：`Resistor r[3];`、`connect(r[1].p, ground.p);`。
- 无法处理复杂 modifier：`redeclare package Medium = ...`、嵌套括号、花括号数组表达式。
- 不能正确选择嵌套 package 中的目标 class。
- 过滤首字母大写实例名会漏掉 `R1`、`C1`、`Pump1` 等常见组件实例。
- 无法读取已有 `Placement` / `Line` 作为布局初值。

## 4. 总体架构

建议新增四层模块：

```text
sysplorer-mcp-server/core/
  modelica_lexer.py          # Modelica 3.4 词法扫描
  modelica_ast.py            # AST 数据结构
  modelica_parser.py         # Modelica 3.4 结构语法解析
  modelica_graph_builder.py  # AST -> Smart Layout graph
```

数据流：

```text
.mo text
  -> ModelicaLexer
  -> Token stream
  -> ModelicaParser
  -> Source-level AST
  -> ModelicaGraphBuilder
  -> Smart Layout graph
  -> smart_layout(writeback_mo)
```

与现有代码集成：

```python
def _parse_modelica_to_graph(modelica_code: str, model_name: str = ""):
    result = build_graph_from_modelica_34_source(
        modelica_code,
        model_name=model_name,
    )
    if result.ok:
        return True, result.graph, ""
    return False, {}, result.error
```

## 5. 词法设计

### 5.1 Token 类型

Lexer 必须遵守 Modelica 3.4 词法约束，至少输出以下 token：

- `IDENT`：普通标识符。
- `Q_IDENT`：quoted identifier，例如 `'x-y'`。
- `STRING`：字符串字面量。
- `UNSIGNED_NUMBER`：数值字面量。
- `KEYWORD`：Modelica 关键字。
- `SYMBOL`：`;`, `,`, `.`, `:`, `:=`, `=`, `(`, `)`, `[`, `]`, `{`, `}` 等。
- `EOF`：文件结束。

Token 必须携带：

- `kind`
- `value`
- `start_offset`
- `end_offset`
- `line`
- `column`

### 5.2 注释与空白

Lexer 应跳过：

- 单行注释：`// ...`
- 块注释：`/* ... */`
- 空白、换行

要求：

- 注释中的 `connect(...)`、`;`、`annotation(...)` 不能进入 parser。
- 字符串中的 `//`、`/*`、`;`、`)` 不能被当作语法结构。
- 块注释未闭合应产生 fatal diagnostic。

### 5.3 关键字

关键字至少包括：

```text
algorithm, and, annotation, block, break, class, connect, connector,
constant, constrainedby, der, discrete, each, else, elseif, elsewhen,
encapsulated, end, enumeration, equation, expandable, extends, external,
false, final, flow, for, function, if, import, impure, in, initial, inner,
input, loop, model, not, operator, or, outer, output, package, parameter,
partial, protected, public, pure, record, redeclare, replaceable, return,
stream, then, true, type, when, while, within
```

说明：关键字集合应集中定义，并通过测试锁定，避免局部解析逻辑硬编码。

## 6. AST 设计

### 6.1 基础结构

```python
@dataclass
class SourceSpan:
    start: int
    end: int
    line: int
    column: int

@dataclass
class Diagnostic:
    severity: Literal["info", "warning", "error"]
    code: str
    message: str
    span: SourceSpan | None = None
```

### 6.2 顶层定义

```python
@dataclass
class StoredDefinition:
    within: QualifiedName | None
    classes: list[ClassDefinition]
    diagnostics: list[Diagnostic]

@dataclass
class ClassDefinition:
    kind: str                 # model, block, package, connector, class, record, ...
    name: str
    prefixes: ClassPrefixes
    partial: bool
    encapsulated: bool
    composition: Composition
    span: SourceSpan
    full_name_hint: str | None = None
```

### 6.3 Composition

```python
@dataclass
class Composition:
    elements: list[Element]
    public_elements: list[Element]
    protected_elements: list[Element]
    equations: list[Equation]
    initial_equations: list[Equation]
    algorithms: list[Any]
    annotations: list[AnnotationNode]
```

### 6.4 元素与声明

```python
@dataclass
class ComponentClause:
    type_specifier: QualifiedName
    type_prefixes: TypePrefixes
    declaration_prefixes: DeclarationPrefixes
    declarations: list[ComponentDeclaration]
    visibility: Literal["public", "protected"]
    span: SourceSpan

@dataclass
class ComponentDeclaration:
    name: str
    array_subscripts: list[TokenSpan]
    modification: TokenSpan | None
    condition: TokenSpan | None
    comment: Comment | None
    annotation: AnnotationNode | None
    span: SourceSpan
```

声明解析必须支持：

- `component_clause` 中的多 `component_declaration`。
- `condition_attribute`：`if expression`。
- `comment` 中的 description string 与 annotation。
- `constraining_clause`、`replaceable`、`redeclare`、`final`、`inner`、`outer`、`each` 等前缀。

### 6.5 方程与 connect

```python
@dataclass
class ConnectEquation:
    lhs: ComponentReference
    rhs: ComponentReference
    comment: Comment | None
    annotation: AnnotationNode | None
    span: SourceSpan

@dataclass
class ComponentReference:
    parts: list[ComponentRefPart]
    raw: str
    span: SourceSpan

@dataclass
class ComponentRefPart:
    name: str
    subscripts: list[TokenSpan]
```

Parser 只需要结构化提取 `connect_clause`，其他 equation 可保存为 `RawEquation` 并跳过。

## 7. Parser 设计

### 7.1 解析范围

Parser 需严格识别以下 Modelica 3.4 语法层级：

- `stored_definition`
- `within_clause`
- `class_definition`
- `class_specifier`
- `composition`
- `element_list`
- `element`
- `import_clause`
- `extends_clause`
- `component_clause`
- `component_list`
- `component_declaration`
- `declaration`
- `modification`
- `equation_section`
- `equation`
- `connect_clause`
- `comment`
- `annotation`
- `component_reference`

对布局无关但语法合法的片段，例如普通 equation、algorithm statement、external function body，可用 balanced-token 跳过并记录原文 span。

### 7.2 容错原则

严守语法不等于一处错误全盘失败。建议：

- 词法错误：一般 fatal，例如字符串未闭合、块注释未闭合。
- class `end Name` 不匹配：fatal 或 error，不能确信 AST 边界。
- 单个 element 解析失败：跳到下一个顶层 `;`，记录 warning。
- 单个 equation 解析失败：跳到下一个顶层 `;`，记录 warning。
- `annotation(...)` 内部解析失败：保存原文，布局字段置空，记录 warning。

### 7.3 Balanced Token Span

对于 modifier、表达式、annotation 参数，第一版不需要完全建表达式 AST，但必须严格按括号层级跳过：

```text
(
  redeclare package Medium = Modelica.Media.Water.StandardWater,
  m_flow_start = if useNominal then 1 else 0
)
```

跳过规则：

- 进入 `(`、`[`、`{` 增加对应栈。
- 遇到匹配闭括号弹栈。
- 只在栈为空时识别 `,`、`;`、`then`、`else` 等外层分隔符。
- 字符串与注释已在 lexer 层处理，不参与括号栈。

## 8. Graph Builder 设计

### 8.1 目标 class 选择

输入 `model_name` 可能是：

- 空字符串：选择文件中唯一可建模 class；若多个 class，优先选择最后一个非 package 的 `model` / `block` / `class`。
- 简名：匹配 `ClassDefinition.name`。
- 全限定名：结合 `within` 与嵌套 class 路径匹配。

若无法唯一选择，返回错误：

```text
无法唯一确定目标 Modelica class，请传入 model_name 或 smart_layout_model_path 对应的完整模型名。
```

### 8.2 组件节点抽取

从目标 class 的 `public_elements` 和 `protected_elements` 中抽取 `ComponentClause`。

布局节点包括：

- 非基本类型的普通组件实例。
- 顶层 connector 实例可配置为 boundary node。
- `input` / `output` connector 可作为边界端口。

默认排除：

- `parameter`
- `constant`
- `discrete`
- 基本内建类型：`Real`, `Integer`, `Boolean`, `String`
- 类型别名、import、extends、class definition

注意：不能再用“实例名首字母是否大写”判断是否组件。Modelica 语法允许实例名首字母大写，是否参与布局应根据声明上下文、类型和连接使用情况判断。

### 8.3 数组策略

第一版建议：

- 声明 `Resistor r[3];` 生成一个节点 `r`。
- 连接端点 `r[1].p` 保留完整端口 id。
- owner 解析为 `r`。

可选增强：

- 当数组维度是静态整数且维度较小，可展开为 `r[1]`, `r[2]`, `r[3]`。
- 默认不展开，避免 graph 规模爆炸和与写回逻辑不兼容。

### 8.4 端口抽取

端口来源：

- 首选：从所有 `connect` 端点反推组件端口。
- 可选：若 class 内声明了 connector 类型实例，可将其加入边界端口。
- 暂不从库类型中解析组件 icon connector；那需要依赖库源码或 Sysplorer 类型信息。

端口 id 保留完整 component reference：

```text
r1.p
r[1].p
bus.signal[2]
controller.u
```

### 8.5 边抽取

每个 `connect(lhs, rhs)` 生成一条 edge：

```python
{
    "id": "connect:<stable-index>",
    "sources": [lhs.raw],
    "targets": [rhs.raw],
    "metadata": {
        "lhs_owner": "r1",
        "rhs_owner": "ground",
        "source_span": ...
    }
}
```

说明：

- Modelica `connect` 本身是无向连接语义；Smart Layout 需要 source/target 时，按源码顺序填入 `sources` / `targets`，不声明物理方向。
- 如果任一端点 owner 不在组件节点中，仍保留 edge，并记录 warning，便于后续诊断。

### 8.6 annotation 抽取

需要识别的布局相关 annotation：

- 组件：`annotation(Placement(...))`
- 连接：`annotation(Line(...))`
- 类：`annotation(Diagram(coordinateSystem(...)))`

第一版只需抽取：

- `Placement.transformation.extent`
- `Placement.transformation.origin`
- `Placement.transformation.rotation`
- `Line.points`
- `Line.color`
- `Diagram.coordinateSystem.extent`

如果 annotation 参数结构复杂或包含表达式，保存原文，不阻断 graph 生成。

### 8.7 Graph 输出

输出结构：

```python
{
    "id": target_full_name,
    "children": [
        {
            "id": component.name,
            "type": str(component.type_specifier),
            "width": width,
            "height": height,
            "ports": [{"id": port_id, "name": local_port_name}],
            "placement": optional_placement,
            "metadata": {
                "visibility": component.visibility,
                "span": component.span,
                "array_subscripts": ...
            }
        }
    ],
    "edges": [
        {
            "id": stable_connect_id,
            "sources": [lhs.raw],
            "targets": [rhs.raw],
            "line": optional_line,
            "metadata": {
                "span": connect.span,
                "is_modelica_connect": True
            }
        }
    ],
    "metadata": {
        "parser": "modelica_34_ast",
        "modelica_version": "3.4",
        "diagnostics": diagnostics
    }
}
```

## 9. 放入自动布线工具的整体设计

新的 Modelica 3.4 parser 不应作为独立离线功能存在，而应成为自动布线工具的 graph 入口能力。自动布线工具内部应形成固定流水线：

```text
input .mo / modelica_code / graph_json
  -> GraphSourceResolver
  -> Modelica 3.4 parser, when graph_json absent
  -> Smart Layout graph normalization
  -> existing smart layout algorithm
  -> Modelica annotation writeback
  -> optional reload/check/translate/simulate
```

### 9.1 自动布线工具职责边界

自动布线工具应统一承担三件事：

- graph 来源解析：显式 `graph_json` / `graph_json_path` 优先；未显式传入 graph 时，基于 `.mo` 源码自动生成 graph。
- 布局与布线计算：复用现有 `core.smart_layout._smart_layout_engine()`，包括节点布局、端口侧推断和连线路由。
- `.mo` 写回：复用并逐步增强 `_apply_layout_graph_to_modelica_code()`，把 `Placement` 与 `Line` 写回 Modelica annotation。

Parser 的职责只到 AST 和 graph 生成，不直接做坐标分配或连线路由；坐标分配和路由仍归现有 Smart Layout algorithm 负责。

### 9.2 工具模式扩展

现有 `smart_layout` 工具有三个模式：

- `layout_only`：输入 graph，输出 layout graph。
- `finalize_generation`：从生成结果 envelope 中找到 graph 并补充 layout graph。
- `writeback_mo`：可写入 `.mo`，运行布局，回写 `Placement` / `Line`。

建议将 `writeback_mo` 扩展为自动 graph 源解析模式：

```python
smart_layout(
    mode="writeback_mo",
    model_name="MyPackage.MyModel",
    model_output_path="MyPackage/MyModel.mo",
    graph_json="",                 # 缺省
    graph_json_path="",            # 缺省
    auto_layout=True,
    auto_generate_graph=True,      # 新增或内部默认
    graph_parser="modelica_34_ast" # 新增，可选：modelica_34_ast | legacy_regex | off
)
```

行为规则：

1. 若提供 `graph_json`，直接使用该 graph。
2. 否则若提供 `graph_json_path`，读取该 graph。
3. 否则若 `auto_generate_graph=True` 且存在 `model_output_path`，读取 `.mo` 并调用 Modelica 3.4 parser 生成 graph。
4. 若新 parser fatal 失败且 `graph_parser` 允许 fallback，回退旧正则解析器并在 metadata 中记录。
5. 若仍无 graph，返回明确错误，不进入布局算法。

### 9.3 与现有布局算法的接口契约

Modelica parser 生成的 graph 必须满足现有布局算法的输入契约：

- `children` 是组件节点列表，每个节点至少包含 `id`、`width`、`height`、`ports`。
- `edges` 是连接列表，每条边包含 `sources` 和 `targets`，且端点字符串应能通过 `port_to_node` 映射到组件。
- 端口 id 使用 Modelica component reference 原文规范化形式，例如 `R1.p`、`r[1].n`、`bus.signal[2]`。
- graph 中可携带已有 `placement` 和 `line`，但布局算法必须能够在缺省这些字段时自行生成坐标。

现有 `_smart_layout_engine()` 中已有以下能力应继续复用：

- edge 格式归一化：把 `source` / `target` 归一为 `sources` / `targets`。
- `port_to_node` 索引构建：从节点和端口 id 映射连接端点到组件。
- 电路模式分流：当 graph 符合电路特征时，使用 circuit layout engine。
- 端口侧推断：基于 MSL 常见端口名推断 `port.side`。
- satellite node 处理：对单端口附属节点做贴近布局。
- 拓扑布局与正交连线路由：计算节点位置和 edge sections / bend points。

因此 parser 不应输出已经“过拟合”某种坐标的 graph；它应输出语义正确、端点稳定、可被现有算法消费的 graph。

### 9.4 Parser 输出到布局算法的适配层

建议新增 `GraphSourceResolver` 或等价内部函数：

```python
def resolve_layout_graph(
    *,
    graph_json: str = "",
    graph_json_path: str = "",
    modelica_code: str = "",
    model_output_path: str = "",
    model_name: str = "",
    auto_generate_graph: bool = True,
    graph_parser: str = "modelica_34_ast",
) -> GraphResolveResult:
    ...
```

返回：

```python
@dataclass
class GraphResolveResult:
    ok: bool
    graph: dict[str, Any]
    source: Literal["graph_json", "graph_json_path", "modelica_34_ast", "legacy_regex"]
    diagnostics: list[Diagnostic]
    error: str = ""
```

该适配层负责：

- graph 来源优先级判断。
- `.mo` 文件读取。
- 调用 Modelica 3.4 parser。
- 调用 `_normalize_graph_format()`。
- 对接 fallback 策略。
- 把 parser diagnostics 写入 `graph["metadata"]["diagnostics"]`。

### 9.5 自动布线完整执行路径

直接调用自动布线：

```text
smart_layout(writeback_mo)
  -> resolve_layout_graph()
  -> _smart_layout_engine(graph)
  -> _apply_layout_graph_to_modelica_code(modelica_code, layout_graph)
  -> write .mo
  -> optional mworks_load_file(force_reload=True)
```

工作流预检调用：

```text
check_model / translate_model / simulate_model
  -> _preflight_smart_layout_reload()
  -> run_smart_layout_for_fast_workflow()
  -> smart_layout(writeback_mo)
  -> reload .mo
  -> official check/translate/simulate
```

快速工作流调用：

```text
fast_workflow
  -> load .mo
  -> preflight smart layout, when enabled
  -> check
  -> simulate
  -> KPI
  -> optional post smart layout
```

这样 parser 与已有布线算法的结合点只有 graph，不改变检查、翻译、仿真的官方调用链。

### 9.6 兼容性与可观测性

自动布线工具返回值建议补充：

```python
{
    "success": True,
    "mode": "writeback_mo",
    "graph_source": "modelica_34_ast",
    "layout_engine": "smart_layout",
    "nodes": 12,
    "edges": 15,
    "components_updated": 12,
    "connects_updated": 15,
    "diagnostics": [...]
}
```

兼容性要求：

- 显式 `graph_json` 行为保持不变。
- 未显式 graph 且无法生成 graph 时，错误信息必须说明缺少 `.mo`、目标 class 不唯一，还是 parser fatal。
- fallback 到旧正则时必须显式标记，避免用户误以为已使用 Modelica 3.4 parser。
- `check_model` / `translate_model` / `simulate_model` 的 `preflight_steps` 中应包含 `graph_source` 和 parser diagnostics 摘要。

### 9.7 布局算法不应承担的职责

为保持边界清晰，现有 Smart Layout algorithm 不应被扩展为 Modelica parser：

- 不在 `_smart_layout_engine()` 中读取 `.mo`。
- 不在布局算法中解析 Modelica annotation 语法。
- 不在布局算法中决定目标 class。
- 不在布局算法中做类型检查或继承展开。

这些职责都属于 parser / graph resolver。布局算法只接收 graph，输出带坐标和路由的 layout graph。

## 10. 与 Smart Layout 写回的关系

当前写回逻辑 `_apply_layout_graph_to_modelica_code()` 依赖 graph 中的组件 id 和 connect 端点。新 parser 必须保证：

- `children[*].id` 等于源码组件实例名。
- `edges[*].sources[0]` / `targets[0]` 等于源码中的 component reference 原文规范化结果。
- 不改变 `.mo` 源码中的声明顺序。

后续增强建议：

- 写回也迁移到 AST + source span 模式。
- 对没有 `annotation(Placement(...))` 的组件插入 annotation。
- 对已有 `annotation(Placement(...))` 的组件只替换 transformation 子树。
- 对已有 `connect(...) annotation(Line(...))` 的连接只替换 Line 子树。

## 11. 测试计划

新增测试文件：

```text
sysplorer-mcp-server/tests/test_modelica_lexer.py
sysplorer-mcp-server/tests/test_modelica_parser.py
sysplorer-mcp-server/tests/test_modelica_graph_builder.py
```

必测样例：

1. 简单电路：
   - `Resistor R1;`
   - `Capacitor C1;`
   - `connect(R1.p, C1.n);`
2. 多声明：
   - `Resistor r1(R=1), r2(R=2);`
3. 多行 modifier：
   - 嵌套括号、数组表达式、字符串。
4. 数组组件：
   - `Resistor r[3];`
   - `connect(r[1].p, ground.p);`
5. 注释干扰：
   - 注释中包含伪 `connect(a,b);`。
6. 字符串干扰：
   - description 中包含 `;`、`)`、`connect(...)`。
7. 嵌套 package：
   - `within A; package B model C ... end C; end B;`
8. `public` / `protected`：
   - protected 组件是否按配置参与布局。
9. annotation：
   - `Placement`
   - `Line`
   - `Diagram(coordinateSystem(...))`
10. 非 connect 方程：
   - `v = p.v - n.v;` 应被跳过，不影响 connect 抽取。

验收标准：

- 上述样例 graph 的节点数、边数、端口 id 与预期一致。
- 解析结果不受注释和字符串中的伪语法影响。
- 首字母大写实例名不再漏掉。
- 对于无法唯一选择目标 class 的文件，返回明确错误。
- 与现有 `run_smart_layout_for_fast_workflow()` 集成后，未传 `graph_json` 时仍能完成 graph 生成和写回。

## 12. 迁移计划

阶段 1：新增 parser，不替换默认路径。

- 新增 `build_graph_from_modelica_34_source()`。
- 增加单元测试。
- 在开发调试入口中对比旧正则与新 parser 输出。

阶段 2：灰度接入自动布线。

- `_parse_modelica_to_graph()` 先调用新 parser。
- 新 parser fatal 失败时，回退旧正则实现。
- 在返回结果 metadata 中标记 `parser: modelica_34_ast` 或 `parser: legacy_regex`。

阶段 3：移除旧正则默认路径。

- 当测试覆盖主要商业库/标准库样例后，默认只用新 parser。
- 旧正则保留为 emergency fallback。

阶段 4：AST 写回。

- 将 `_apply_layout_graph_to_modelica_code()` 改造成基于 source span 的精准写回。
- 避免正则写回误伤相似组件名或注解。

## 13. 风险与缓解

- 风险：Modelica 3.4 完整语法复杂，手写 parser 容易遗漏。
  - 缓解：第一版只结构化布局相关语法；表达式和 modifier 用 balanced span 严格跳过。
- 风险：不同库源码风格差异大。
  - 缓解：建立样例语料集，至少覆盖 MSL、商业库常见声明、自动生成模型。
- 风险：无类型信息时无法知道组件真实端口。
  - 缓解：从 `connect` 端点反推端口；需要完整端口时再结合 Sysplorer introspection。
- 风险：数组展开策略影响 graph 规模和写回。
  - 缓解：默认不展开数组，仅保留端点原文。
- 风险：annotation 语法中表达式复杂。
  - 缓解：只解析常见 `Placement` / `Line` 字段，失败时保存原文并继续。

## 14. 开放问题

- 是否将 protected 组件默认纳入布局？建议默认纳入，因为 `protected` 组件仍可能出现在 diagram 和 connect 中。
- 顶层 connector 是生成 boundary node，还是作为 graph-level port？建议第一版生成 boundary node，便于现有 layout engine 处理。
- 是否需要调用 Sysplorer 查询组件类型端口？建议作为可选增强，不作为 parser 第一版依赖。
- 是否默认展开小数组？建议第一版不展开，后续通过参数控制。

