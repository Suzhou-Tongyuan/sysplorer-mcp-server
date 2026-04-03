# 流体模型库
---
&nbsp;

流体模型库需要 License 解锁使用，若有需要，请获取 License 使用许可。

<table>
	<tr bgcolor="#F6F8FA">
	    <th width="12%">主题</th>
	    <th width="20%">模型库名称</th>
		<th width="20%">模型库用户手册</th>
	    <th width="48%">说明</th>
	</tr>
	<tr>
	    <td><a href="#/Doc/FluLib/TYHydraulics.html">液压模型库</a></td>
	    <td>TYHydraulics V2.4.0</td>
		<td><a :href="$withBase('/Resource/Reference/附录A-10液压模型库V2.4.0产品用户手册-C.pdf')" target="_blank">液压模型库产品用户手册</a></td>
	    <td>TYHydraulics 液压模型库包括泵源、液压阀类、执行机构、管路、流阻、液压辅件、边界源和各种传感器等模型。该库可用于航空、航天、车辆船舶、工程机械等领域液压系统的设计、仿真及优化，例如开展飞机液压能源系统的功率计算、验证挖掘机液压系统的关键指标等。</td>
	</tr>
	<tr>
	    <td><a href="#/Doc/FluLib/TYHydraulicComponents.html">液压元件设计模型库</a></td>
	    <td>TYHydraulicComponents V2.5.0</td>
		<td><a :href="$withBase('/Resource/Reference/附录A-10液压元件设计模型库V2.5.0产品用户手册-C.pdf')" target="_blank">液压元件设计模型库产品用户手册</a></td>
	    <td>TYHydraulicComponents 液压元件设计模型库包括活塞、滑阀芯、锥阀芯、球阀芯、喷嘴挡板阀芯、隔膜、密封摩擦泄漏和控制容积等模型，主要用于搭建各种复杂的液压模型。用户可根据液压柱塞泵、溢流阀、换向阀等液压元件的物理拓扑结构，搭建结构化的液压模型，可与液压库配合用于更多场景的液压系统设计与验证。</td>
	</tr>
    <tr>
	    <td><a href="#/Doc/FluLib/TYOilMedia.html">液压介质模型库</a></td>
	    <td>TYOilMedia V2.3.0</td>
		<td>/</td>
	    <td>TYOilMedia 液压介质模型库，包括 Oil 液压油模型和 ThermalOil 热液压油介质模型两种，主要满足液压系统建模需求，能够实现液压系统中油液介质的物性计算。</td>
	</tr>
      <tr>
	    <td><a href="#/Doc/FluLib/TYPneumatics.html">气动模型库</a></td>
	    <td>TYPneumatics V2.1.0</td>
		<td><a :href="$withBase('/Resource/Reference/附录A-10气动模型库V2.1.0产品用户手册-C.pdf')" target="_blank">气动模型库产品用户手册</a></td>
	    <td>TYPneumatics 气动模型库包括压气机、汽轮机、执行机构、压力控制阀、流量控制阀、方向阀、管路、流阻、换热器及辅件等模型。该库广泛应用于各个领域，包括航空航天、工程机械、制造业、自动化生产线、气压控制系统等，可用于气动设备和气动系统的设计验证、功率匹配、故障注入以及可靠性分析等。</td>
	</tr>
    <tr>
	    <td><a href="#/Doc/FluLib/TYPneumaticComponents.html">气动元件设计模型库</a></td>
	    <td>TYPneumaticComponents V2.3.0</td>
		<td><a :href="$withBase('/Resource/Reference/附录A-10气动元件设计模型库V2.3.0产品用户手册-C.pdf')" target="_blank">气动元件设计模型库产品用户手册</a></td>
	    <td>TYPneumaticComponents 气动元件设计模型库，包括活塞、滑阀阀芯、锥阀阀芯、球阀阀芯、孔板阀芯、隔膜、流量控制阀、气体容腔和其他公用组件等模型。可搭建高粒度气动模型。该模型库和气动模型库配合使用，可应用于更多场景的气动系统的设计与分析，例如起落架应急系统、救生防护服系统等。</td>
	</tr>
    <tr>
	    <td><a href="#/Doc/FluLib/TYGasMedia.html">气体介质模型库</a></td>
	    <td>TYGasMedia V2.1.0</td>
		<td>/</td>
	    <td>TYGasMedia 气体介质模型库基于 Modelica 语言开发，包括各种状态下的气体介质类型。用户可根据实际需求选择气体介质模型，用于系统设计、控制算法验证等辅助分析。模型库可应用于各类工程机械、汽车、航空航天等领域中的气动系统的设计，例如工程流水线常用的气动机械手、汽车自动门系统、飞机的燃油通气系统等。</td>
	</tr>    
    <tr>
	    <td><a href="#/Doc/FluLib/TYThermalHydraulics.html">热液压模型库</a></td>
	    <td>TYThermalHydraulics V1.3.0</td>
		<td><a :href="$withBase('/Resource/Reference/附录A-10热液压模型库V1.3.0产品用户手册-C.pdf')" target="_blank">热液压模型库产品用户手册</a></td>
	    <td>TYThermalHydraulics 热液压模型库包括泵源、液压阀类、执行机构、管路、流阻、换热器库、液压辅件、边界源和各种传感器等模型。该库可用于航空、航天、车辆船舶、工程机械等领域液压系统的设计、仿真及优化，例如开展飞机液压能源系统的功率计算、验证挖掘机液压系统的关键指标等。</td>
	</tr>
    <tr>
	    <td><a href="#/Doc/FluLib/TYThermalHydraulicComponents.html">热液压元件设计模型库</a></td>
	    <td>TYThermalHydraulicComponents V1.5.0</td>
		<td><a :href="$withBase('/Resource/Reference/附录A-10热液压元件设计模型库V1.5.0产品用户手册-C.pdf')" target="_blank">热液压元件设计模型库产品用户手册</a></td>
	    <td>TYThermalHydraulicComponents 热液压元件设计模型库包括活塞、滑阀芯、锥阀芯、球阀芯、喷嘴挡板阀芯、隔膜、密封摩擦泄漏和控制容积等模型，主要用于搭建各种复杂的液压模型。用户可根据液压柱塞泵、溢流阀、换向阀等液压元件的物理拓扑结构，搭建结构化的液压模型，可与热液压库配合用于更多场景的液压系统设计与验证，并可开展对液压系统的热故障、压焓图计算等场景的应用。</td>
	</tr>
    <tr>
	    <td><a href="#/Doc/FluLib/TYThermals.html">热模型库</a></td>
	    <td>TYThermals V1.1.0</td>
		<td><a :href="$withBase('/Resource/Reference/附录A-10热模型库V1.1.0产品用户手册-C.pdf')" target="_blank">热模型库产品用户手册</a></td>
	    <td>TYThermals 热模型库，包括固体材料、热容、热传导、热对流、热辐射、换热器基础模块、0 维湿空气、边界以及传感器等模型。该模型库可应用于实现热演化、热传输、热能储存和辐射传热等计算，可与实际设计相结合，预测和解决工程中出现的热问题等。</td>
	</tr>
    <tr>
	    <td><a href="#/Doc/FluLib/TYThermoFluidSys.html">基础热流体模型库</a></td>
	    <td>TYThermoFluidSys V1.3.0</td>
		<td><a :href="$withBase('/Resource/Reference/附录A-10基础热流体模型库V1.3.0产品用户手册-C.pdf')" target="_blank">基础热流体模型库产品用户手册</a></td>
	    <td>TYThermoFluidSys 基础热流体模型库包括管道、阀门、接头、机械转动设备、换热器、热组件和传感器等模型。该库可用于搭建大型复杂热流系统，进行动态仿真分析，覆盖热流系统的设计仿真验证、运行模拟、状态预测和数字化验证等多个应用场景，可用于核能、火电、船舶、液体动力和综合能源等多个领域。</td>
	</tr>
    <tr>
	    <td><a href="#/Doc/FluLib/TYMedia.html">热流介质模型库</a></td>
	    <td>TYMedia V1.4.0</td>
		<td><a :href="$withBase('/Resource/Reference/附录A-10热流介质库V1.4.0产品用户手册-C.pdf')" target="_blank">热流介质模型库产品用户手册</a></td>
	    <td>TYMedia 热流介质模型库，提供了多种热流系统中的常用介质，包括基于 Helmholtz 方程的介质、CoolProp 介质、不可压缩流体介质和固体介质，支持用户同时调用 TYMedia 和 Modelica.Media 中的介质，如理想气体、Water_IF97 等。该模型库主要应用于热流相关模型库对介质物性的调用，可计算工作介质在单相或两相状态下的物性参数，实现介质物性最大程度的复用，满足不同场景下热流系统的建模需求。</td>
	</tr>
	<tr>
	    <td><a href="#/Doc/FluLib/TYAirTreatmentAndVentilation.html">空气处理与通风模型库</a></td>
	    <td>TYAirTreatmentAndVentilation V1.1.0</td>
		<td><a :href="$withBase('/Resource/Reference/附录A-10空气处理与通风模型库V1.1.0产品用户手册-B.pdf')" target="_blank">空气处理与通风模型库产品用户手册</a></td>
	    <td>TYAirTreatmentAndVentilation 空气处理与通风模型库包括阀类、管路、压缩机和风扇、空气处理、换热器、控制器、传感器、边界等，同时提供模型库应用的典型示例库以及二次开发必要的接口和开发模板。空气处理与通风库与基础热流体库、热流介质库配合使用可以构建各类建筑的暖通系统和航空、航天、船舶和轨道交通等领域的环控系统，实现暖通系统设计优化，室内（舱内）环境控制优化，环境温度湿度动态模拟分析等。</td>
	</tr>
  
</table>

