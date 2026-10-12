# 介质选择指南

本文件用于在 `TYMedia` 与 `Modelica.Media` 中选择适配介质，并确定介质约束方式。

## 目录

- `选择顺序`：按物理域、组件支持范围和约束层次做介质选择。
- ``TYMedia` 的主要介质来源`：快速定位 `Helmholtz`、`CoolProp`、不可压缩和固体介质。
- ``Modelica.Media` 的常见用法`：识别何时应回到标准库介质。
- `介质基类与可选介质范围`：控制参数面板的可选介质集合。
- `空气处理与通风系统中的介质规则`：处理湿空气、`CO2` 和混合气体。
- `热流体系统中的介质规则`：处理连续回路的介质一致性。
- `特殊注意事项`：记录编译器、浓度定义等边界条件。
- `默认选择建议`：给出常见场景的首选介质路径。
- `来源`：回溯手册来源。

## 选择顺序

1. 先确定物理域。
   - 是单相液体、气体、两相工质、不可压缩流体、固体，还是混合气体。
2. 再看组件支持范围。
   - 尤其是 `TYAirTreatmentAndVentilation` 中的空气处理组件，会对气体成分有要求。
3. 再决定用 `TYMedia` 还是 `Modelica.Media`。
   - 如果 TY 库已有合适介质，优先选 `TYMedia`。
   - 如果需要标准库介质、表格介质或用户明确要求标准库，选 `Modelica.Media`。
4. 最后决定介质基类约束。
   - 约束过宽会导致参数面板选择杂乱。
   - 约束过窄会导致用户无法选到目标介质。

## `TYMedia` 的主要介质来源

- `TYMedia.Helmholtz`
  - 适合 Helmholtz 状态方程介质与常见制冷剂、气体、两相介质。
- `TYMedia.CoolProp`
  - 适合通过 CoolProp 获取物性。
  - 注意外部函数依赖，手册要求使用 VS2015/2017 编译器。
- `TYMedia.Incompressible`
  - 适合铅、铋、铅铋合金等不可压缩介质。
- `TYMedia.Solid`
  - 适合不锈钢、石墨等固体介质。

## `Modelica.Media` 的常见用法

- 标准库常见介质。
- 简化介质或表格介质。
- 用户明确要求标准库介质。
- 需要直接使用 `Modelica.Media.Incompressible.TableBased` 或其他 Modelica 标准库接口时。

## 介质基类与可选介质范围

下表来自 TYMedia 手册的注意事项，可用于限制参数面板中的可选介质种类：

| 基类 | 可选介质 |
| --- | --- |
| `Modelica.Media.Interfaces.PartialMedium` | `TYMedia` 和 `Modelica.Media` 中所有介质 |
| `TYMedia.Interfaces.ExtendedPartialTwoPhaseMedium` | `Helmholtz` 与 `CoolProp` 库中的介质 |
| `TYMedia.Helmholtz.PartialHelmholtz` | `Helmholtz` 库中的介质 |
| `TYMedia.CoolProp.CoolPropInterface` | `CoolProp` 库中的介质 |
| `TYMedia.Incompressible.PartialIncompressible` | 铅、铋、铅铋合金介质 |
| `Modelica.Media.Incompressible.TableBased` | `Glysantin_30/40/50/60` 等表格介质 |
| `Modelica.Media.Interfaces.PartialSimpleMedium` | 乙二醇水溶液、丙二醇水溶液、海水等简单介质 |
| `TYMedia.Solid.PartialSolidMedium` | `Solid` 库中的介质 |

## 空气处理与通风系统中的介质规则

### 必须检查气体成分

- 干燥器、增湿器、分离器、湿度传感器要求气体中包含水蒸气。
- `CO2` 净化器要求混合气体中包含 `CO2`。
- 空气侧与制冷剂侧共同建模时，要确认换热器或压缩机模型确实支持对应介质类型。

### 混合气体

- `TYAirTreatmentAndVentilation` 手册指出库中提供了自定义混合气体介质示例。
- 如果任务涉及湿空气、氧气供给、`CO2` 控制或多组分气体，优先考虑混合气体介质，而不是单组分理想气体。

## 热流体系统中的介质规则

- `TYThermoFluidSys` 支持调用 `TYMedia` 和 `Modelica.Media` 中的介质。
- 系统中相连组件通常应共享同一介质，手册说明可在任一组件中选择介质并通过接口传递给其它相连组件。
- 不相连的支路可以使用不同介质，但不要在同一连续回路中混用不兼容介质。

## 特殊注意事项

- 使用 `TYMedia.CoolProp` 时，注意编译器要求。
- 乙二醇水溶液、丙二醇水溶液等介质需要定义浓度，手册说明通常要通过文本建模实现。
- 如果用户只说“选个合适介质”，默认应解释选择依据，而不是只给出一个包名。

## 默认选择建议

- 蒸汽/两相工质/常见制冷剂优先看 `TYMedia.Helmholtz`。
- 需要 CoolProp 物性时选 `TYMedia.CoolProp`。
- 金属液体或铅铋工况选 `TYMedia.Incompressible`。
- 固体导热材料选 `TYMedia.Solid`。
- 通用标准库水、空气或表格介质场景可选 `Modelica.Media`。
- 湿空气、含 `CO2` 空气处理任务优先选能表达对应组分的混合气体介质。

## 来源

- `references/manuals/media-library-manual.md`
- `references/manuals/thermofluid-library-manual.md`
- `references/manuals/air-treatment-library-manual.md`
