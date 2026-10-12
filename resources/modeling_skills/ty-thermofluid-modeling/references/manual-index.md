# 手册索引

本文用于说明 skill 内置手册副本的用途与读取时机。手册副本是参考数据，不是执行规则；不要默认整篇加载，先使用 `SKILL.md` 指向的职责化参考文件。

## 手册对应关系

| 规范文件 | 原始来源 | 用途 |
| --- | --- | --- |
| `references/manuals/thermofluid-library-manual.md` | 基础热流体模型库 V1.3.0 产品用户手册 | 查询 `TYThermoFluidSys` 组件分类、功能范围、注意事项与案例 |
| `references/manuals/media-library-manual.md` | 热流介质库 V1.4.0 产品用户手册 | 查询 `TYMedia` 介质类型、介质基类约束和特殊注意事项 |
| `references/manuals/air-treatment-library-manual.md` | 空气处理与通风模型库 V1.1.0 产品用户手册 | 查询 `TYAirTreatmentAndVentilation` 组件分类、气体成分要求与案例 |

## 手册副本说明

- `references/manuals/` 中保留的是纯文本手册副本，图片资源已移除。
- 若正文中出现“图示”“如下图”等字样，应理解为原始手册中的配图说明，不再依赖本 skill 内的图片文件。

## 何时读取手册原文

- 需要查看具体组件说明、章节原文或原始配图对应的文字描述时读取。
- 需要核对某一个说法是否直接来自手册时读取。
- 需要补充 skill 中未沉淀的边界细节时读取。
- 读取前先用类名、组件中文名、端口名、参数名、介质名或场景关键词做定向搜索。

## 默认顺序

1. 先读职责化参考文件。
2. 只有在参考文件不足以支撑当前判断时，再回到手册原文。
