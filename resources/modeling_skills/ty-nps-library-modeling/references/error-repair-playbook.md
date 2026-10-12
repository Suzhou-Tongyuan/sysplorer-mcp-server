# Error Repair Playbook

修复 NPS 模型不是附加步骤，而是主流程的一部分。

---

## 1. 标准修复流程

```text
识别错误现象
-> 提取报错信息
-> 判断错误类别
-> 定位具体问题
-> 若根因未验证且已连续试错两轮以上，则暂停完整模型修改
-> 对未知组件先做组件级最小验证
-> 执行修复
-> 重跑失败步骤
-> 验证修复是否生效
```

---

## 2. 错误分类与修复策略

### A. 连接类错误

典型现象：

- 端口未连接
- 端口连接错误
- 域不匹配
- 信号端与物理端误连

修复策略：

- 补齐缺失连接
- 替换错误连接对象
- 增加转换模块
- 删除无效连接
- 在继续其它修复前，先确认电气参考是否存在且正确，包括 `Ground / Reference` 是否缺失、重复或接错侧
- 再排查单相/三相、一维/三维、标量/向量接口是否误连或缺少转换块
- 如果是文本方式新增连接，必须同步补图面 `annotation(Line(points=...))`

### B. 参数类错误

典型现象：

- 参数缺失
- 参数越界
- 单位错误
- 数量级异常

修复策略：

- 补充默认参数
- 调整参数范围
- 统一单位
- 修正初值

### B1. 未知组件或盲猜迭代

典型现象：

- 连续多轮修改连接、参数或布局，但没有验证根因
- 组件引脚、旋转、内部结构或参数作用仍不清楚
- 直接在完整模型上反复猜接法、猜参数、猜拓扑

修复策略：

- 立即停止完整模型上的继续试错
- 先查组件文档、类说明、接口和参数定义
- 为该组件或局部子电路建立最小验证模型
- 只有最小验证通过后，才允许把接法或参数带回完整模型

### C. 结构类错误

典型现象：

- 缺 `Powergui`
- 缺参考节点
- 存在孤立子系统
- 回路不闭合

修复策略：

- 增加基础配置块
- 重构连接关系
- 重新组织主回路
- 优先检查每个独立电气岛是否都有正确参考，变压器隔离两侧是否需要各自参考
- 仅当孤立部分被证明违背原始拓扑意图时，才允许删除，并必须记录证据

### D. 翻译类错误

典型现象：

- 方程不平衡
- 初始化失败
- 结构不可翻译
- 模型过度约束

修复策略：

- 检查变量与方程关系
- 放松初始化约束
- 第一项先检查接地与参考点是否缺失、重复、接错侧，以及独立电气岛是否缺参考
- 再检查未连接端口、重复连接、方向错误、接口维度和相数不匹配
- 再检查 `Powergui`、边界和测量参考是否缺失
- 仅在确认组件本身与目标拓扑不兼容后，才允许更换兼容组件
- 仅在确认原约束确实多余且非连接问题导致时，才允许减少过度约束
- 若用户明确指定了拓扑或关键组件，必须先继续在 `NPSLibrary` 内查找其它兼容组件、类路径或转换块，再讨论删改

### E. 仿真类错误

典型现象：

- 发散
- 步长过小
- 状态爆炸
- 结果 NaN

修复策略：

- 调整求解器
- 缩小激励幅值
- 修改初始条件
- 增加阻尼/缓冲
- 检查硬开关与不连续问题
- 调整开关频率、采样周期、滤波参数
- 检查 `PLL`、PWM 和坐标变换链路

### F. 结果类错误

典型现象：

- 能跑但结果不对
- 动作方向反了
- 曲线趋势明显异常
- 稳态值不合理

修复策略：

- 检查控制逻辑方向
- 检查连接极性
- 检查参数量级
- 检查边界条件与负载设置
- 检查功率方向、相序与接线方式
- 检查并网点、潮流约束或 `LoadFlowBus`

---

## 2.1 Mandatory Solver Repair Rule

For any NPSLibrary simulation failure, abnormal waveform, wrong steady-state value, NaN, divergence, or result that does not match the scenario goal, check the solver setup before tuning parameters or changing topology:

- Inspect the latest `.mo` model text and confirm the model-level `annotation(experiment(...))` contains `Algorithm=InlineImplicitEuler`.
- Confirm `InlineIntegrator=true`, `InlineStepSize=false`, and explicit `Interval` / `IntegratorStep` values.
- Confirm `Interval` and `IntegratorStep` match unless a case-specific reason is documented.
- Use `5e-5` as the normal default step; reduce to a value such as `1e-5` when required by PWM frequency, physical sampling, control period, or observed numerical behavior.
- Do not switch back to Dassl to bypass NPSLibrary simulation issues.

## 3. 回退规则

- `check` 失败：修复后重跑 `check`
- `layout` / 图面验收失败：按父级 Gate 6 重跑；若写回模型则再次 `check`
- `translate` 失败：按父级闭环回到翻译前的必要阶段
- `simulate` 失败：按父级闭环回到仿真前的必要阶段
- `result verify` 不通过：修复后至少重跑 `simulate -> result verify`；若改了参数、拓扑或图解语义，回退到对应父级 Step 复验

## 4. 禁止性修复动作

- 不得把“删除组件直到报错消失”当作排障方法
- 不得因为方程冗余或方程缺失就直接删除用户要求的传感器、电源、主功率器件或整个子系统
- 不得绕过单相/三相、一维/三维接口不匹配问题去修改无关方程
- 不得只补文本 `connect(...)` 而不补图面连线信息
- 不得因为第一个候选组件实现困难，就擅自删除或替换用户明确指定的拓扑
- 不得在未理解组件行为的情况下持续在完整模型上盲目试错
