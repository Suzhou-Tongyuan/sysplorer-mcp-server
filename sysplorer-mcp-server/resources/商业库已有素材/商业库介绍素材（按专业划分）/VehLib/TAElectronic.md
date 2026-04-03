# 车辆电子模型库
---
&nbsp;

## 概述
<br>
TAElectronic 车辆电子模型库包括照明/风暖系统、行车系统和舒乐系统。用户可根据实际的工况，构建整车低压负载系统模型，可应用于不同道路、发动机转速、天气工况下的产品设计验证和 DCDC 控制策略虚拟标定。


## 功能要点

- 提供丰富的子系统

	提供丰富的子系统供用户选择，并且可以对子系统本身进行测试。

- 支持构建自定义模型

	支持通过继承和重申明替换关键组件类型，快速完成低压负载模型的构建。
	
- 提供常见电子负载模型

	如 LED 灯、大灯、雨刮器、车窗除霜器、喷油系统和通用负载模型。


## 模型库目录

车辆电子模型库包括座舱域、动力域、车身域、底盘域的低压用电设备模型，总线模型和公共组件。

<table>
	<tr bgcolor="#F6F8FA">
	    <th colspan="3" width="58%">名称</th>
	    <th>描述</th>  
	</tr>
	<tr>
	    <td>UserGuide</td>
	    <td colspan="2">用户指南</td>
	    <td>提供模型库概述、联系方式、版本说明等介绍文档</td>
	</tr>
    <tr>
	    <td>CockpitDomain</td>
	    <td colspan="2">座舱域</td>
	    <td>包括座椅系统、后视镜系统和扬声器</td>
	</tr>
        <tr>
	    <td>DynamicDomain</td>
	    <td colspan="2">动力域</td>
	    <td>包括霍尔电机、波纹电机、起动机和电容</td>
	</tr>
    <tr>
	    <td>BodyDomain</td>
	    <td colspan="2">车身域</td>
	    <td>包括电动车门锁、车窗升降系统、通风系统、除霜器、电动尾门、电动前舱盖、车门把手系统、雨刮器、照明系统、燃油泵、喷油系统、通用负载等电子器件</td>
	</tr>
    <tr>
	    <td>ChassisDomain</td>
	    <td colspan="2">底盘域</td>
	    <td>包括助力转向系统、安全气囊和雷达</td>
	</tr>
    <tr>
	    <td>Bus</td>
	    <td colspan="2">总线</td>
	    <td>电子电器总线</td>
	</tr>
    <tr>
	    <td>Utilities  </td>
	    <td colspan="2">公用组件</td>
	    <td>传感器、电机模型、储液箱模型等</td>
	</tr>
    <tr>
	    <td> Controller </td>
	    <td colspan="2">控制器</td>
	    <td>包括控制器模板、控制器模型、电子负载控制器参数包</td>
	</tr>
</table>


## 主要模型

<img :src="$withBase('/VehLib/TAElectronic/1.png')" style="width:400px;border:black 1px solid;">

## 应用场景

- DCDC 控制策略虚拟标定

	支持对 DCDC 控制策略进行验证和优化，提高整车低压电网动态性能。

- 整车复杂工况仿真分析

	根据整车不同低压负载工作状态配置构建整车实际复杂低压耗能工况，如发动机不同转速工况、不同道路等级工况、不同天气状况。


## 应用案例

如下图所示，对车辆电子模型模拟信号建立模型进行测试，设置 LED 相对发光强度为 2240 cd，矩形灯行列数均为 2；大灯的额定功率 60 W，峰值电流 10 A；车窗峰值电流 15 A，额定电流 5 A，阻断电流 20 A；除霜器峰值电流 3 A，额定电流 2.5 A；车速 150 km/h，暴雨工况，老旧路面，引擎转速为 2000 r/min，最后电压设定为 14 V。

系统模型：

<img :src="$withBase('/VehLib/TAElectronic/2.png')" style="width:768px;border:black 1px solid;">

输出电流：

<img :src="$withBase('/VehLib/TAElectronic/3.png')" style="width:498px;">