# Sysblock 模型参数扫描

---

&nbsp;

本示例完全使用 Sysplorer API 通过修改参数批量仿真实现参数扫描。

示例代码见 <a href="Samples/ExampleFile/Demo_SysblockParameterSweepScript/SysblockParameterSweep.py" target="_blank">SysblockParameterSweep.py </a>（右击 -> 弹出上下文菜单 -> 将链接另存为）。

将示例代码拖拽到 Sysplorer 的命令窗口中即可运行。若要在独立的 Python 解释器中运行代码，需要在文件头导入 mworks 包，并添加启动 Sysplorer 的代码，代码如下所示。

```python
from mworks.sysplorer import *
from mworks.sysplorer import MwAppOptions

StartSysplorer()
```

## 示例说明

很多情况下，有必要使用不同的参数集来运行仿真模型，通过参数变化对输出变量的影响来观察物理系统的行为，进而深入理解系统的内部机理。

本示例以脚本命令方式支持用户进行这种参数研究，提供建立参数集，并且自动调用求解器得到批次结果的功能。具体的操作步骤结合一个经典的二阶机械动力学系统——弹簧-阻尼-质量系统进行说明。

<img :src="$withBase('/Example/Example.assets/RunMultipleSimulationsExample.png')" alt="弹簧-阻尼-质量系统" style="width:660px;border:black solid 1px;">

示例模型请参见 <helpButton isLink exampleUrl="mworks://ref/../Sysblock/Samples/Sysblock/Simulation/RunningSimulation/RunMultipleSimulations/ParameterSweep.mo">ParameterSweep</helpButton>。 本示例通过多次修改参数 cval 的值，研究弹簧-阻尼-质量系统在欠阻尼、临界阻尼和过阻尼场景下的运行特征。

## 命令说明

将以下命令复制到 Sysplorer 的命令窗口以运行示例。

Step 1：定义模型名、输入参数所在的组件、参数扫描矩阵、输出数据

```python
model_path = GetInstallationDirectory() + r"/Docs/Sysblock/Samples/Sysblock/Simulation/RunningSimulation/RunMultipleSimulations/ParameterSweep.mo"
model_name = 'ParameterSweep'

parameter_name = 'cval.k'
parameter_list = [0.5, 2, 5]
output = []
```

Step 2：预处理

```python
LoadLibrary('SysplorerEmbeddedCoder')
OpenModelFile(model_path)
OpenModel(model_name)
MwAppOptions.SetBoolean("MWorks.Simulation.General.ErasePlotWhenSimulation", False)
MwAppOptions.SetBoolean("MWorks.Simulation.General.AutoReplotAfterSimulation", False)
SimulateModelEx(model_name)
CreateLayoutEx(position=[1,1,1,1,1,2,1,2,1,3,1,3]) #构建1*3的绘图区域
```

Step 3：参数扫描批量仿真

```python
for i in range(len(parameter_list)):
    SetInitialValue(parameter_name, parameter_list[i])

    res = SimulateModelEx(model_name)
    if res:
        CreatePlotEx(variables=['scope.u1'], position=[1, 1, i+1, 1, i+1])
        result = GetVarValues('scope.u1')
        output.append(result)
```

<img :src="$withBase('/Example/Example.assets/Results.png')" alt="仿真结果" style="width:660px;border:black solid 1px;">

通过观察三次仿真结果可以看出：

- 欠阻尼（cval = 0.5）的情况下，物体在达到平衡位置前会发生往复**震荡**，振幅随时间呈指数衰减，最终趋于稳定；
- 临界阻尼（cval = 2）的情况下，系统在**不发生震荡**的前提下，以**最快速度**回到平衡位置；
- 过阻尼（cval  = 5）的情况下，系统**无震荡**。物体缓慢地靠近平衡位置，就像在粘稠的蜂蜜中运动一样，反应较慢。