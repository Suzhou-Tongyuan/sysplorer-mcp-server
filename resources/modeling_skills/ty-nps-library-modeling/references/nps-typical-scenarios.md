# NPS Typical Scenarios

用于高频任务的快速场景识别与最小闭环搭建。

---

## 1. 三相供电网络

- 典型组件：`Three_Phase_Source` + `Three_Phase_Transformer_TwoWindings` + `Three_Phase_Transmission_Line_Pi_signal_2` + `Three_Phase_Series_RLC_Load`
- 关键检查：接线方式、变比、线路长度、负载参数、参考地
- 关键结果：三相电压电流、功率传输、线路压降

## 2. 两电平并网逆变器

- 典型组件：直流源 + `TwoLevelConverter` + 滤波器 + `PLL` + PWM + 电网边界
- 关键检查：并网点、电压电流相位、`id/iq` 控制、采样周期
- 关键结果：并网电流、电压、P/Q、动态响应

## 3. Boost / Buck / DCDC

- 典型组件：直流源 + `BoostConverter` / `BuckConverter` / `TwoQuarantDCDCConverter` + L/C + 传感器 + 控制器
- 关键检查：功率流向、占空比方向、储能元件参数、纹波
- 关键结果：输入输出电压、电流、稳态误差、过冲与纹波

## 4. PMSM 三电平驱动

- 典型组件：直流源 + `ThreeLevelBridge` + `Permanent_Magnet_Synchronous_machine` + 变换模块 + PI 控制器 + PWM
- 关键检查：dq 变换、转速环/电流环、转矩方向、机械负载
- 关键结果：转速、转矩、相电流、dq 电流

## 5. 潮流分析

- 典型组件：`Powergui` + `LoadFlowBus` + 三相电源 + 线路 + 变压器 + 负载
- 关键检查：基准电压、P/Q 边界、节点定义、变压器与线路参数
- 关键结果：节点电压幅值、相角、P/Q 分配
