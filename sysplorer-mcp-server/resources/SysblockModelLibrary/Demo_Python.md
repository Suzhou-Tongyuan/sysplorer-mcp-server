# 脚本化建模

---

&nbsp;

本示例完全使用 Sysplorer API 搭建弹跳小球 Sysblock 模型，并进行仿真，获取小球位置的仿真结果。

示例代码见 <a href="Samples/ExampleFile/Demo_MonteCarloAnalysis/BounceBallTest.py" target="_blank">BounceBallTest.py </a>（右击 -> 弹出上下文菜单 -> 将链接另存为）。

将示例代码拖拽到 Sysplorer 的命令窗口中即可运行。若要在独立的 Python 解释器中运行代码，需要在文件头导入 mworks 包，并添加启动 Sysplorer 的代码，代码如下所示。

```python
from mworks.sysplorer import *

StartSysplorer()
```

## 示例说明

弹球模型是混合动态系统的一个示例。混合动态系统是既包括连续动态又包括离散转移的系统，其中系统动态可能会发生变化，状态值可能会有跳跃。弹球的连续动态特性由以下方程给出：
$$
dv/dt=-g
$$

$$
dx/xt=v
$$

其中，g 为重力加速度，x 是球的位置，v 是球的速度。该模型的混合系统方面源于球与地面碰撞的建模。假设球与地面发生部分弹性碰撞，则碰撞前的速度 v- 与碰撞后的速度 v+ 可以通过球的恢复系数 κ 来关联。
$$
v^+ = -κv^-
$$

$$
x=0
$$

因此，弹球在转移条件 x=0 下显示连续状态（速度）下出现一个跳跃。

本模型使用两个 Integrator 模块对弹球进行建模。左边的 Integrator 模块是对第一个方程建模的速度积分器。右边的 Integrator 模块是位置积分器。此外，对位置积分器设置参数饱和下限为 0，表示存在一个限制：球无法降到地面以下。

<img :src="$withBase('/Example/Example.assets/Ballmodel.png')" style="width:600px; border:black 1px solid;">

## 命令说明

将以下命令复制到 Sysplorer 的命令窗口以运行示例。

Step 1：新建模型 BounceBall

```python
NewModel("BounceBall", "Sysblock")
```

Step 2：添加模块

- 速度积分器

```python
AddComponent("SysplorerEmbeddedCoder.Continuous.Integrator", "BounceBall", "velocity", 0, 0, 40, 40)
SetModelParamValue("BounceBall", "velocity", "InitCondSourceType", "外部")
SetModelParamValue("BounceBall", "velocity", "ExternalResetType", "上升沿")
```

- 位置积分器

```python
AddComponent("SysplorerEmbeddedCoder.Continuous.Integrator", "BounceBall", "displacement", 60, 0, 40, 40)
SetModelParamValue("BounceBall", "displacement", "LimitOutput", "true")
SetModelParamValue("BounceBall", "displacement", "UpperSaturationLimit", "10")
SetModelParamValue("BounceBall", "displacement", "LowerSaturationLimit", "0")
SetModelParamValue("BounceBall", "displacement", "InitCond", "10")
```

- 重力加速度

```python
AddComponent("SysplorerEmbeddedCoder.Sources.Constant", "BounceBall", "gravitational_acceleration", -45, 13.5)
SetModelParamValue("BounceBall", "gravitational_acceleration", "Value", "-9.8")
```

- 反弹判断条件

```python
AddComponent("SysplorerEmbeddedCoder.LogicAndBitOperation.RelationalOperator", "BounceBall", "relational_operator", 60, 38, width=-20)
SetModelParamValue("BounceBall", "relational_operator", "Operator", ">=")
AddComponent("SysplorerEmbeddedCoder.Sources.Constant", "BounceBall", "constant1", 120, 43, width=-20)
SetModelParamValue("BounceBall", "constant1", "Value", "0.001")
```

- 反弹速度反馈

```python
AddComponent("SysplorerEmbeddedCoder.MathOperation.Gain", "BounceBall", "gain", 0, -40, width=-20)
SetModelParamValue("BounceBall", "gain", "Gain", "-0.8")
AddComponent("SysplorerEmbeddedCoder.Discrete.UnitDelay", "BounceBall", "delay1", -40, -40, width=-20)
```

- 结果观察器

```python
AddComponent("SysplorerEmbeddedCoder.Utilities.Scope", "BounceBall", "scope", 110, 0)
```

Step 3：连接信号

- 积分运算

```python
ConnectPort("BounceBall", "gravitational_acceleration.y", "velocity.u1")
ConnectPort("BounceBall", "velocity.y", "displacement.u1")
```

- 反弹判断条件信号线

```python
ConnectPort("BounceBall", "constant1.y", "relational_operator.u1")
ConnectPort("BounceBall", "displacement.y", "relational_operator.u2", (80, 0, 90, 0, 90, 33, 70, 33))
ConnectPort("BounceBall", "relational_operator.y", "velocity.u2", (50, 38, -30, 38, -30, 0, 0, -20))
```

- 反弹速度反馈信号线

```python
ConnectPort("BounceBall", "velocity.y", "gain.u", (20, 0, 30, 0, 30, -40, 10, -40))
ConnectPort("BounceBall", "gain.y", "delay1.u1")
ConnectPort("BounceBall", "delay1.y", "velocity.u3", (-50, -40, -60, -40, -60, -13.5, -20, -13.5))
```

- 结果观察器信号线

```python
ConnectPort("BounceBall", "displacement.y", "scope.u1")
```

Step 4：仿真

```python
SimulateModelEx("BounceBall", {"stopTime": 20.0, "interval": 0.002})
```

Step 5：查看结果

```python
res = GetVarValues("displacement.y")
print(res)
CreatePlot(y = ["displacement.y"])
```


<img :src="$withBase('/Example/Example.assets/Simulateresult.png')" style="width:600px; border:black 1px solid;">