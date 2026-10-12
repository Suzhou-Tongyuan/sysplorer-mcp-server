# 工作表1

| 序号 | 一级类别 | 二级类别 | 三级类别 | 四级类别 | 模型名 | 描述 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | \ | \ | \ | \ | Powergui | 潮流分析器 |
| 2 | PowerElectronics | Converter | \ | \ | BoostConverter | 升压变换器 |
| 3 |  |  |  |  | BuckConverter | 降压变换器 |
| 4 |  |  |  |  | HalfBridgeConverter | 半桥变换器 |
| 5 |  |  |  |  | UniversalBridge | 通用桥 |
| 6 |  |  |  |  | TwoQuarantDCDCConverter | 双向DCDC变换器 |
| 7 |  |  |  |  | ThreeLevelBridge | 三电平变换器 |
| 8 |  |  |  |  | FullBridgeConverter | 全桥变换器 |
| 9 |  |  |  |  | TwoLevelConverter | 两电平变换器 |
| 10 |  |  |  |  | HalfBridgeMMC | 半桥MMC |
| 11 |  |  |  |  | FullBridgeMMC | 全桥MMC |
| 12 |  |  |  |  | ThreeLevelNPCconverter | 三电平NPC变换器 |
| 13 |  |  |  |  | ThreeLevel TNPCConverter | T型三电平NPC变换器 |
| 14 |  | Control | \ | \ | PWMGenerator | PWM发生器 |
| 15 |  |  |  |  | PWMGenerator DCDC | PWM发生器 |
| 16 |  |  |  |  | PWMGenerator Multilevel | 多电平PWM发生器 |
| 17 |  |  |  |  | PWMGenerator FivePhase TwoLevel | 五相两电平PWM发生器 |
| 18 |  |  |  |  | PWMGenerator ThreePhase ThreeLevel | 三相三电平PWM发生器 |
| 19 |  |  |  |  | PWMGenerator ThreePhase TwoLevel | 三相两电平PWM发生器 |
| 20 |  |  |  |  | PWMGenerator TwoLevel | 两电平PWM发生器 |
| 21 |  |  |  |  | PWMGenerator ThreeLevel | 三电平PWM发生器 |
| 22 |  |  |  |  | SVPWMGenerator TwoLevel | 空间矢量脉宽调制器(2电平) |
| 23 |  |  |  |  | SVPWMGenerator ThreeLevel | 空间矢量脉宽调制器(3电平) |
| 24 |  |  |  |  | PWMGenerator PulseAveraging | 平均值PWM发生器 |
| 25 |  | Semiconductor | \ | \ | Diode | 二极管 |
| 26 |  |  |  |  | GTO | 栅极关断晶闸管GTO |
| 27 |  |  |  |  | IdealSwitch | 理想开关 |
| 28 |  |  |  |  | IGBT | 理想IGBT |
| 29 |  |  |  |  | IGBTwithDiode | 带二极管IGBT |
| 30 |  |  |  |  | MOSFET | 理想MOSFET |
| 31 |  |  |  |  | Thyristor | 普通晶闸管 |
| 32 |  |  |  |  | IGBT ideal | 电信号IGBT |
| 33 |  |  |  |  | IdealDiode | 理想二极管 |
| 34 |  |  |  |  | DetailedThyristor | 精细晶闸管 |
| 35 | Motors | Synchronous | \ | \ | Synchronous_Machine_pu_Fundamental | 基础同步电机标幺制模型 |
| 36 |  |  |  |  | Synchronous_Machine_SI_Fundamental | 基础同步电机有名制 |
| 37 |  |  |  |  | SimSynMachine_SI | 简化同步电机有名值模型 |
| 38 |  |  |  |  | Simplified_Synchronous_Machine_pu_Units | 简化同步电机标幺值模型 |
| 39 |  |  |  |  | Permanent_Magnet_Synchronous_machine | 永磁同步电机模型 |
| 40 |  |  |  |  | Synchronous_machine_pu_standard | 标准同步机标幺值模型 |
| 41 |  | Asynchronous | \ | \ | Asynchronous_Machine_pu_Units | 异步电机标幺值模型 |
| 42 |  |  |  |  | Asynchronous_Machine_SI_Units | 异步电机有名值模型 |
| 43 |  |  |  |  | Single_Phase_Asynchronous_Machine | 单相异步电机 |
| 44 |  | WindTurbine | \ | \ | Wind_Turbine | 风力涡轮机 |
| 45 | PowerSystem | RenewableEnergy | PhotovoltaicPowerGeneration | \ | PVarray | 光伏阵列 |
| 46 |  |  | StoragePower | \ | Battery | 电池 |
| 47 |  |  |  |  | Supercapacitor | 超级电容 |
| 48 |  | Generation | \ | \ | ExcitationSystem | 励磁系统 |
| 49 |  |  |  |  | Power_System_Stabilizer | 通用电力系统稳定器 |
| 50 |  |  |  |  | Hydraulic_goverment | 水轮机及调速系统模型 |
| 51 |  |  |  |  | SteamTurbine_Governor | 汽轮机调速器 |
| 52 |  |  |  |  | Power_System_Stabilizer__Discrete | 通用电力系统稳定器-离散 |
| 53 |  | TransmissionAndDistribution | Breaker | \ | CircuitBreaker | 单相断路器 |
| 54 |  |  |  |  | ThreePhaseBreaker | 三相断路器 |
| 55 |  |  |  |  | IdealCircuitBreaker | 理想单相断路器 |
| 56 |  |  |  |  | IdealThreePhaseBreaker | 理想三相断路器 |
| 57 |  |  | Line | \ | PiSectionLine | 单相pi型传输线 |
| 58 |  |  |  |  | Three_Phase_Transmission_Line_Pi_signal_2 | 三相pi型传输线 |
| 59 |  |  |  |  | Distributed_Parameters_Line | 分布式参数线 |
| 60 |  |  | Transformer | \ | Ideal_Transformer | 理想变压器 |
| 61 |  |  |  |  | Linear_Transformer_Twowindings | 单相两绕组线性变压器 |
| 62 |  |  |  |  | Singlephase_linear_transformer_3winding1 | 单相三绕组线性变压器 |
| 63 |  |  |  | NonlinearTransformer | Three_Phase_Nonlinear_Transformer_TwoWindings | 两绕组非线性变压器 |
| 64 |  |  |  |  | Transformer_Twowindings_PU | 标幺两绕组变压器 |
| 65 |  |  |  |  | Three_Phase_Transformer_Inductance_Matrix_Type_TwoWindings | 三相两绕组开短路参数变压器 |
| 66 |  |  |  |  | Three_Phase_Transformer_Inductance_Matrix_Type_ThreeWindings | 三相三绕组开短路参数变压器 |
| 67 |  |  |  |  | Three_Phase_Transformer_ThreeWindings | 三相三绕组变压器 |
| 68 |  |  |  |  | Three_Phase_Transformer_TwoWindings | 三相两绕组变压器 |
| 69 |  |  |  |  | Saturated_Transformer | 饱和变压器 |
| 70 |  |  |  |  | SinglePhase_Transformer_Inductance_Matrix_Type_TwoWindings | 单相两绕组开短路参数变压器 |
| 71 |  |  |  |  | SinglePhase_Transformer_Inductance_Matrix_Type_Three_Windings | 单相三绕组开短路参数变压器 |
| 72 |  |  |  |  | Three_Phase_Saturated_Transformer | 三相饱和变压器 |
| 73 |  |  |  |  | grounding_transformer | 接地变压器 |
| 74 |  |  |  |  | ThreePhaseMutualInductanceZ1Z0 | 三相互感Z1Z0 |
| 75 |  | Load | RLC_Branch | \ | Series_RLC_Branch | 串联RLC支路 |
| 76 |  |  |  |  | Parallel_RLC_Branch | 并联RLC支路 |
| 77 |  |  |  |  | Three_Phase_Series_RLC_Branch | 三相串联RLC支路 |
| 78 |  |  |  |  | Three_Phase_Parallel_RLC_Branch | 三相并联RLC支路 |
| 79 |  |  | RLC_Load | \ | Parallel_RLC_Load | 并联RLC负载 |
| 80 |  |  |  |  | Series_RLC_Load | 串联RLC负载 |
| 81 |  |  |  |  | Three_Phase_Parallel_RLC_Load | 三相并联RLC负载 |
| 82 |  |  |  |  | Three_Phase_Series_RLC_Load | 三相串联RLC负载 |
| 83 |  |  | ConstantPowerLoad | \ | Three Phase Constant Power Load | 三相恒定功率负载 |
| 84 |  |  | DynamicLoad | \ | Dynamic_Load | 动态负荷模型 |
| 85 |  | ControlAndProtection | PLL_Model | \ | PLLdiscrete | 离散锁相环 |
| 86 |  |  |  |  | PLL1ph | 单相锁相环 |
| 87 |  |  |  |  | PLL | 三相锁相环 |
| 88 |  |  | LoadFlowCalculation | \ | LoadFlowBus | 潮流总线 |
| 89 |  |  | Others | \ | current_scaler_beicheng | 电流倍乘 |
| 90 |  |  |  |  | ThreePhaseFault | 三项故障模型 |
| 91 | Sources | \ | \ | \ | AC_Current_Source | 交流电流源 |
| 92 |  |  |  |  | AC_Voltage_Source | 交流电压源 |
| 93 |  |  |  |  | Controlled_Current_Source | 受控电流源 |
| 94 |  |  |  |  | Controlled_Voltage_Source | 受控电压源 |
| 95 |  |  |  |  | DC_Voltage_Source | 直流电压源 |
| 96 |  |  |  |  | Three_Phase_Source | 三相电源 |
| 97 |  |  |  |  | Stair_Generator | 阶梯信号发生器 |
| 98 |  |  |  |  | Three_Phase_Sine_Generator | 三相正弦波发生器 |
| 99 |  |  |  |  | Three_Phase_Programmable_Source | 三相可编程电源 |
| 100 |  |  |  |  | Three_Phase_Programmable_Generator | 三相可编程信号发生器 |
| 101 |  |  |  |  | RepeatingSequence | 按时间/输出值表生成周期信号 |
| 102 | Sensors | \ | \ | \ | CurrentSensor | 电流传感器 |
| 103 |  |  |  |  | VoltageSensor | 电压传感器 |
| 104 |  |  |  |  | CurrentSensor3ph | 多相电流传感器 |
| 105 |  |  |  |  | VoltageSensor_3ph | 多相电压传感器 |
| 106 |  |  |  |  | PowerSensor | 多相功率传感器 |
| 107 |  |  |  |  | ReactivePowerSensor | 三相无功传感器 |
| 108 |  |  |  |  | MultiSensor | 多功能传感器 |
| 109 |  |  |  |  | Meas_PQ_threephase | 有功无功传感器 |
| 110 | Utilities | SensorAndMeasurement | \ | \ | RootMeanSquare | 计算周期为 1/f 的均方根模型 |
| 111 |  | Control | \ | \ | Discrete_PI_Control | 离散PI控制器模型 |
| 112 |  |  |  |  | DiscreteIntegratorWithLim | 带限幅的离散积分器 |
| 113 |  |  |  |  | DiscreteIntegrator | 离散积分器 |
| 114 |  |  |  |  | DiscreteIntegratorWithReset | 带重置的离散积分器 |
| 115 |  |  |  |  | Continuous_PI_Control | 连续PI控制器 |
| 116 |  |  |  |  | Bias | 偏置 |
| 117 |  |  |  |  | Ceil | 向上取整 |
| 118 |  |  |  |  | Floor | 向下取整 |
| 119 |  |  |  |  | Hysteresis | 迟滞环 |
| 120 |  |  |  |  | integrator | 积分器 |
| 121 |  |  |  |  | LeadLag_transfer | 超前滞后环节 |
| 122 |  |  |  |  | Max_min | 最大/小值 |
| 123 |  |  |  |  | Meas_RMS3p | 三相有效值测量 |
| 124 |  |  |  |  | Mod | 取余计算 |
| 125 |  |  |  |  | PeriodMaxMin | 周期最大/小值 |
| 126 |  |  |  |  | PID | PID控制器 |
| 127 |  |  |  |  | Quantizer | 量化器 |
| 128 |  |  |  |  | Ts_transfer | 一阶惯性环节 |
| 129 |  | Reference_System_Transformation | \ | \ | Clarke_Transform | Clarke变换 |
| 130 |  |  |  |  | Inverse_Clarke_Transform | Clarke逆变换 |
| 131 |  |  |  |  | Park_Clarke_Transform | dq-αβ变换 |
| 132 |  |  |  |  | Clarke_Park_Transform | αβ-dq变换 |
| 133 |  |  |  |  | abctodq0 | abc-dq0变换 |
| 134 |  |  |  |  | dq0toabc | dq0-abc变换 |
| 汇总行 | 134 |  |  |  |  |  |
