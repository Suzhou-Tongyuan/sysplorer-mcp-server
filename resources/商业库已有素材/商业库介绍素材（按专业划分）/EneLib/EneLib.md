# 能源行业模型库
---
&nbsp;

能源行业模型库需要 License 解锁使用，若有需要，请获取 License 使用许可。

<table>
	<tr bgcolor="#F6F8FA">
	    <th width="12%">主题</th>
	    <th width="20%">模型库名称</th>
		<th width="20%">模型库用户手册</th>
	    <th width="48%">说明</th>
	</tr>
	<tr>
	    <td><a href="#/Doc/EneLib/TYPhotovoltaicPower.html">光伏发电模型库</a></td>
	    <td>TYPhotovoltaicPower V1.1.0</td>
		<td><a :href="$withBase('/Resource/Reference/附录A-10光伏发电模型库V1.1.0产品用户手册-B.pdf')" target="_blank">光伏发电模型库产品用户手册</a></td>
	    <td>TYPhotovoltaicPower 光伏发电模型库包括环境模型、光伏发电设备、电力变换设备、电力输送设备、电能存储设备、控制器、负载、传感器、边界等模型。可用于光伏发电系统建模与分析，分析光伏系统受环境影响后的发电性能，优化光伏系统配置和调度策略，具体应用场景包括光伏电厂数字化建模、太阳能房屋光伏发电系统、航天光伏供电系统、公共设施光伏供电系统、风光互补发电系统等。</td>
	</tr>
	<tr>
	    <td><a href="#/Doc/EneLib/TYWindPower.html">风力发电模型库</a></td>
	    <td>TYWindPower V1.1.0</td>
		<td><a :href="$withBase('/Resource/Reference/附录A-10风力发电模型库V1.1.0产品用户手册-B.pdf')" target="_blank">风力发电模型库产品用户手册</a></td>
	    <td>TYWindPower 风力发电模型库包括环境模型、机械设备、发电设备、电力变换设备、电能存储设备、电力输送设备、负载、控制系统等。支持构建风力发电系统动态仿真模型，对风力发电系统的气动、机械、电气等模块进行仿真分析与设计验证，开展控制策略设计与优化，实现风电数字化试验台建设和运维；同时可结合光伏发电模型库等能源行业相关模型库，开展风光热储场景应用。</td>
	</tr>
    <tr>
	    <td><a href="#/Doc/EneLib/TYIntegratedEnergySys.html">综合能源系统模型库</a></td>
	    <td>TYIntegratedEnergySys V1.1.0</td>
		<td><a :href="$withBase('/Resource/Reference/附录A-10综合能源系统模型库V1.1.0产品用户手册-B.pdf')" target="_blank">综合能源系统模型库产品用户手册</a></td>
	    <td>TYIntegratedEnergySys 综合能源系统模型库提供了多种形式的能源生产、转换、传输、储存等设备，包括能源生产设备库、能源转换设备库、能源传输设备库、能源储存设备库、负荷模型库及基础设备库等，支持源-网-荷-储综合能源场景应用，可应用于区域级综合能源系统拓扑设计与优化，实现多种异质能源子系统、供暖制冷系统、蒸汽供热系统、烟气余热回收系统等多能源系统耦合网络等仿真应用。</td>
	</tr>
	<tr>
	    <td><a href="#/Doc/EneLib/TYBattery.html">电池模型库</a></td>
	    <td>TYBattery V1.0.0</td>
		<td><a :href="$withBase('/Resource/Reference/附录A-10电池模型库V1.0.0产品用户手册-A.pdf')" target="_blank">电池模型库产品用户手册</a></td>
	    <td>TYBattery 电池模型库包括电芯、电池包、电池管理系统、冷却板、充放电循环设备、传感器、边界等模型。电池模型库可以应用于能源、车辆、船舶和核能等领域，实现电池多层级、多粒度建模、电池管理系统研发、支持电热耦合验证；与基础热流体模型库、热流介质模型库配合使用可以实现电池柜、储能站的储能系统热管理；与光伏发电模型库、风力发电模型库配合使用实现能源系统动态仿真与优化。</td>
	</tr>
</table>

