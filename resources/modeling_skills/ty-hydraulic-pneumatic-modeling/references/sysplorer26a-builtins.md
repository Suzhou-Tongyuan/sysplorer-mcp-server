# sysplorer26a 内置流体类模型库清单

本文件来自用户提供的资料：
`D:/WXWORK/WXWork/1688856538284074/Cache/File/2026-03/模型库_流体类_详细清单.md`

用途：
- 作为 `sysplorer26a` 环境下内置 `TY*` 流体类库的权威范围
- 当手册、旧索引、历史工程副本出现版本或库名冲突时，以本文件为准
- skill 输出优先使用“英文包名”列

## 权威内置库

| 中文名 | 英文包名 | 版本 | 模型数量 | 备注 |
| --- | --- | --- | ---: | --- |
| 液压介质模型库 | `TYOilMedia` | `V2.3.0` | 66 | 20251230 新增 31 种插值表液压油介质 |
| 液压模型库 | `TYHydraulics` | `V2.3.0` | 149 | 常规液压系统默认系统级库 |
| 液压元件设计模型库 | `TYHydraulicComponents` | `V2.5.0` | 41 | 液压元件设计级库 |
| 热液压模型库 | `TYThermalHydraulics` | `V1.3.0` | 153 | 热液压系统默认系统级库 |
| 热液压元件设计模型库 | `TYThermalHydraulicComponents` | `V1.5.0` | 41 | 热液压元件设计级库 |
| 气体介质模型库 | `TYGasMedia` | `V2.0.2` | 34 | 气动介质库 |
| 气动模型库 | `TYPneumatics` | `V2.1.0` | 86 | 常规气动系统默认系统级库 |
| 气动元件设计模型库 | `TYPneumaticComponents` | `V2.3.0` | 34 | 气动元件设计级库 |
| 热模型库 | `TYThermals` | `V1.1.0` | 47 | 纯热网络补充 |
| 热流介质模型库 | `TYMedia` | `V1.4.0` | 37 | 热流介质库 |
| 基础热流模型库 | `TYThermoFluidSys` | `V1.3.0` | 73 | 基础热流系统库 |
| 空气处理与通风模型库 | `TYAirTreatmentAndVentilation` | `V1.1.0` | 52 | 2025 年新增 |

## 选择规则

以下仅约束父级已选商业流体子系统中的 TY 组件，不是项目整体白名单；保留已选标准库和其他领域组件。实际加载版本需按当前证据核对，本表是资料基线，不能替代当前安装验证。商业路径固定 `Modelica 4.0.0.TY.1`。

1. 常规液压系统只在 `TYHydraulics` 中选系统级块。
2. 涉及温度、焓流、热交换、热边界时，优先 `TYThermalHydraulics`。
3. 气动系统只在 `TYPneumatics` 中选系统级块。
4. 元件设计级任务只在 `TYHydraulicComponents`、`TYThermalHydraulicComponents`、`TYPneumaticComponents` 中选择。
5. 介质必须从 `TYOilMedia`、`TYGasMedia`、`TYMedia` 中选择。
6. 不把历史库或副本冒充当前 TY 商业库；父级已选标准库与其他领域组件允许共存，不据本清单删除它们。

## 常见误区

- 不要把 `Hydraulics_TY`、`OpenHydraulics`、示例工程里的副本包，当成 sysplorer26a 的内置库。
- 不要用中文库名 + 旧版本号覆盖这里的英文包名和版本。
- 手册里的历史版本号可以用于参考示例和说明，但不作为当前内置库选择依据。
