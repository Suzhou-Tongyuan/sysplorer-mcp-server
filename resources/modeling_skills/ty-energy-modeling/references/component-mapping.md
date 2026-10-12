# Component Mapping

Use this file to narrow class selection before opening the full manuals.

## By Domain

| Need | Prefer |
|---|---|
| 光伏板、MPPT、光伏并网平均值或开关模型 | 光伏发电库 |
| 风机、PMSG、DFIG、风电并网、MPPT | 风力发电库 |
| SOC、CCCV、充放电循环、热管理、电池包效率 | 电池库 |
| 区域综合能源、CHP、锅炉、制氢储氢、多能耦合 | 综合能源系统库 |
| 通用边界源、数学模块、基础接口、标准介质和信号 | `Modelica 4.0.0.TY.1` |

## By Functional Role

| Role | Selection rule |
|---|---|
| Primary source | Choose the domain library matching the actual energy source |
| Converter or subsystem | Prefer the library whose semantics are narrowest and closest to the request |
| Boundary or excitation | Prefer explicit source or boundary classes over equation-level forcing |
| Measurement | Prefer domain-compatible sensors or result probes without changing semantics |
| Cross-domain coordination | Prefer integrated-energy library coordination or auxiliary classes |

## Escalate To Manual

Open the relevant manual when:

- two or more candidate classes remain plausible
- parameter meaning is unclear
- interface compatibility is uncertain
- a typical example is needed for naming or topology confirmation
