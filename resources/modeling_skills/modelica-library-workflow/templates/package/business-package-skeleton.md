# 业务 Package 骨架

仅在本轮已采用模板或项目需要相应业务分层时选用；保留已有兼容结构，不强制所有业务包新增 Basics 或空子包。

```text
{{BusinessPackageName}}
  Basics
  {{SubPackage1}}
  {{SubPackage2}}
  {{SubPackage3}}
```

## 使用说明

1. `Basics` 只放该业务包内部复用的基础模型，中文显示名默认写为“基础模型库”。
2. 跨全库复用内容改放 `Interfaces` 或 `Utilities`。
3. 子包名优先按领域语义命名，不用泛化占位名。
4. 业务功能包的中文显示名也优先按“XX库”命名，如“泵库”“阀库”“执行机构库”。
