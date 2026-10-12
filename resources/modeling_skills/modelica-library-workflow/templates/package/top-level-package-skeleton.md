# 顶层 Package 骨架

仅用于已采用 `references/template-package-scheme.md` 所述模板的授权建库；其他工程沿用兼容结构，不因本骨架增建空包或迁移原生接口。骨架位置不代表已请求示例/测试运行。

```text
{{LibraryName}}
  UsersGuide
  Examples
  {{BusinessPackage1}}
  {{BusinessPackage2}}
  Sensors
  Sources
  Interfaces
  Utilities
  Tests
```

对应目录式模型库时，顶层 `package.order` 默认也按同样顺序写入。

## 使用说明

1. 先把 `{{BusinessPackageX}}` 替换成正式业务包名。
2. 不要把占位包名直接带入交付。
3. 顶层库名不要与商业库重名，也不要以 `TY` 开头。
4. 只有确有需求时，才继续细分 `Interfaces` 或 `Utilities` 的子包。
5. 顶层功能包中文显示名默认按“XX库”命名，例如 `Interfaces` 写为“接口库”、`Sources` 写为“边界库”、`Sensors` 写为“传感器库”、`Utilities` 写为“公用库”。
6. 如果采用目录式 package，生成骨架时同步创建顶层和关键子包的 `package.order`，不要把排序工作留到交付后补。
