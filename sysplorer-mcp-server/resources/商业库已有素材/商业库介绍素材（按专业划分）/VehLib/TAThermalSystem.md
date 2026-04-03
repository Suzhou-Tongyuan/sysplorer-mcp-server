# 车辆热管理模型库
---
&nbsp;

## 概述
<br>
车辆热管理模型库可用于常见汽车热管理仿真场景，如乘员舱、空调、水冷回路系统仿真，通过构造不同的换热回路以实现各种不同介质的子系统回路的模拟仿真。模型库架构根据元件大类进行划分，以方便应用工程师快速上手。Examples 案例模型库中包含有多种热管理系统案例以供用户了解模型库使用场景。

TAThermalSystem 模型库包含常见的几大部分：换热器（冷凝器、蒸发器、水水换热器等）、管道（空气、制冷剂、冷却液类管道）、阀（多通阀、膨胀阀、换向阀等）、各类传感器、动力设备（压缩机、泵、风机）。开放大部分代码，为用户提供二次开发的基础。

## 功能要点

模型库对车辆热管理工况进行了针对性构建，提供了高颗粒度的整车热管理系统模型，此外为整车控制功能提供了一系列热管理架构的搭建模板，能够实现快速基于热管理架构模板，自定义开发新的车辆热管理系统。

模型库种类丰富，涵盖水冷、制冷剂两相、空气等组件类型。可满足于热管理系统研发过程中的设备选型、系统架构分析、能量分析、优化控制、整车功能验证等流程。

## 模型库目录

TAThermalSystem 模型库包括案例、阀类、换热器、泵、管道、压缩机、边界等主要构成，通过不同类型热管理回路的搭建，可以实现对各种车辆热管理系统的建模，满足复杂工况构建需求，实施车辆热管理的仿真。

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
	    <td>Media</td>
	    <td colspan="2">介质</td>
        <td>用户自定义介质</td>
	</tr>
    <tr>
	    <td>Valves</td>
	    <td colspan="2">阀门</td>
        <td>提供各种阀类，多通阀、膨胀阀、换向阀等</td>
	</tr>
    <tr>
	    <td>HeatExchangers</td>
	    <td colspan="2">换热器</td>
        <td>提供各类换热器，冷凝器、蒸发器、水水换热器等</td>
	</tr>
    <tr>
	    <td>PumpAndFan</td>
	    <td colspan="2">泵与风机</td>
        <td>提供各类泵与风机</td>
	</tr>
    <tr>
	    <td>Pipes</td>
	    <td colspan="2">管道</td>
        <td>提供各类管道</td>
	</tr>
    <tr>
	    <td>BranchPipe</td>
	    <td colspan="2">三通</td>
        <td>提供三通组件</td>
	</tr>
    <tr>
	    <td>Compressor</td>
	    <td colspan="2">压缩机</td>
        <td>提供各类压缩机</td>
	</tr>
    <tr>
	    <td>Reservoirs</td>
	    <td colspan="2">储液箱</td>
        <td>提供各类储液箱</td>
	</tr>
    <tr>
	    <td>Heating</td>
	    <td colspan="2">加热</td>
        <td>提供各类加热与热源</td>
	</tr>
    <tr>
	    <td>Sources</td>
	    <td colspan="2">源</td>
        <td>提供各类型边界与源</td>
	</tr>
    <tr>
	    <td>Interfaces</td>
	    <td colspan="2">接口</td>
        <td>提供各类接口</td>
	</tr>
    <tr>
	    <td>Sensors</td>
	    <td colspan="2">传感器</td>
        <td>提供各类传感器</td>
	</tr>
    <tr>
	    <td>Utilities</td>
	    <td colspan="2">公共组件</td>
        <td>提供可视化、函数、模块等共用组件</td>
	</tr>
</table>



## 主要模型

<img :src="$withBase('/VehLib/TAThermalSystem/1.png')" style="width:498px;border:black 1px solid;">

## 应用场景

支持整车在概念架构设计阶段，使用模型构建对应的车辆热管理架构，支持乘员舱、热泵空调、电池电机电控冷却等应用场景，满足热管理系统研发过程中的设备选型、系统架构分析、能耗分析、优化控制、整车功能验证等流程。


## 应用案例

以乘员舱换热网络模型为例，该乘员舱颗粒度较细，细化到前排仪表板、挡风玻璃、车顶和车顶帆布、侧板、侧面玻璃、后排玻璃以及车上各种材料传热。不仅考虑外界环境温度、压力、相对湿度对乘员舱的影响，而且包含太阳辐射以及太阳方位角和高度角对辐射影响、内外的对流传热过程。此外，能够对舱内的二氧化碳的浓度进行计算，各种影响传热的材料属性可自定义。对于整个系统，车载的空调回路对空气进行冷却后，再经动力设备风扇带走乘员舱的热量，使乘客处于舒适温度范围。

系统模型：

<img :src="$withBase('/VehLib/TAThermalSystem/2.png')" style="width:498px;border:black 1px solid;">

下图分别为乘员舱温度、乘员舱换热功率、压缩机流量、压缩机进出口压力：

<img :src="$withBase('/VehLib/TAThermalSystem/3.png')" style="width:898px;">
