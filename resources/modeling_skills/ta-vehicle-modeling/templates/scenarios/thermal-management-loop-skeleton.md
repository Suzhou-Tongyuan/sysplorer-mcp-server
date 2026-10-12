# Thermal Management Loop Skeleton

## 定位

- 本文件不是任务入口，不负责判定“是否属于热管理任务”或“主回路该从哪条开始”。
- 只有在 `../../references/library-selection.md` 已将任务收敛到 `TAThermalSystem`，并且已进入 `../../workflows/build-from-scenario.md` 后，才用它快速套热管理回路骨架。
- 它提供的是高频场景的默认骨架，不替代 `../../references/build-rules.md`、`../../references/diagram-layout-rules.md` 和主库卡片中的详细规则。

## 适用范围

- `TAThermalSystem` 主框架热管理任务
- 热泵空调、制冷剂回路、水冷回路、电池热管理、整车热管理网络

## 默认骨架

| 项目 | 默认做法 |
| --- | --- |
| 主库 | `TAThermalSystem` |
| 常见辅助库 | `TABattery`、`TAEngine`、`TAElectronic`、`TAEconomy` |
| 默认思路 | 先按热回路组织，不把局部热源拼接误当整车热管理骨架 |
| 详细规则 | `../../references/build-rules.md`、`../../references/diagram-layout-rules.md` |
| 优先案例来源 | `../../references/library-cards/TAThermalSystem.md` 中的 Samples 与速查起步 |

## 最小闭环

1. 热源、热汇和边界条件闭合
2. 水冷、空气、制冷剂主链分别成链
3. 关键换热器、泵、阀、压缩机接口匹配
4. 顶层图面能看清主回路与附件耦合点

## 首轮必锁信息

| 必锁项 | 说明 |
| --- | --- |
| 主回路类型 | 水冷、空气、制冷剂、舱内热舒适还是综合热管理 |
| 热源与热汇 | 电池、发动机、舱内、环境边界 |
| 关键设备 | 换热器、泵、阀、压缩机、风机 |
| 结果变量 | 温度、流量、压差、换热量、压缩机功耗 |

## 首轮必查

- 回路是否真正闭合
- 容性和阻性元件是否合理交替
- 关键换热器进出口温度、流量、压差变量是否已定位

## 不得做的简化

- 不得把局部热源拼接误写成整车热管理骨架
- 不得让多个关键回路混成一条不可读的主链
- 不得跳过热回路 `Placement` 与 `Line(...)` 的源码级检查
