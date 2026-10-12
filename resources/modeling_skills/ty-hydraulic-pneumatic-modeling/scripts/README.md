# 液压图面离线预检

从 Agent CWD 调用脚本的实际路径，并显式传入模型文件及本次验收目标类：

```powershell
& '<skill-dir>/scripts/check_modelica_diagram_layout.ps1' '<model.mo>' -TargetClass 'Plant.HydLoop' -Json
& '<skill-dir>/scripts/check_modelica_line_annotations.ps1' '<model.mo>' -TargetClass 'Plant.HydLoop' -Json
```

`-TargetClass` 接受完全限定类名或文件内唯一的短类名。文件仅有一个长类时兼容省略参数的旧调用；多个长类未指定目标、目标缺失或短名有歧义时，返回 `undetermined`。每个本次变更目标分别调用，不展开嵌套类、兄弟类或继承图形；类内短类声明的注解也不计入父类。

| status | passed | 退出码 | 含义 |
|---|---|---:|---|
| `passed` | `true` | 0 | 本次目标的可支持局部预检未发现问题 |
| `failed` | `false` | 1 | 发现缺注解、零长度线、包围盒越界、重叠或中心过近等预检问题 |
| `undetermined` | `null` | 2 | 范围或语法不能可靠解释；查看 `diagnostics`，不得当成通过或据此直接改模 |

共享 `modelica_preflight_common.ps1` 只做词法、类范围与注解字段解析，不执行 Modelica 表达式。支持注释、转义字符串、常见长/短类、equation 中的 if/for/when/while 结束语句、注解字段换序及科学计数法。参数化坐标、DynamicSelect、数组/条件组件、引号类名等无法可靠解释的输入返回未确定；它不是完整 Modelica 解析器或官方模型检查的替代品。

布局计算先旋转 extent 四角，再加 origin；`placements` 给出旋转后的轴对齐包围盒和中心。包围盒重叠是保守预检结果，不等于图元像素轮廓相交。明确 `visible=false` 的实例列入 `hidden_instances_not_checked`，是否允许隐藏仍需对照目标计划。

连线数量是目标类直接 `connect(...)` 语句数，不展开 for 循环，也不代表实例化后连接数。零连接可以返回 `passed`，仅表示未发现违规连接；必须另外核对计划数量，不能用零条通过证明计划中的连线已实现。脚本不验证所有关键实例是否存在，也不验证端点锚定和完整可读性。

保留脚本原始状态和证据，依据父级 Gate 6 补充所需结构化复核。`undetermined` 需记录限制并补充适用证据，不能改写为脚本通过；预检失败也不授予修改未触及层级、启动软件或追加仿真的权限。
