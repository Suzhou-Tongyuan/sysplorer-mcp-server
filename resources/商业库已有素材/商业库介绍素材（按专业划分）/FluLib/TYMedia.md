# 热流介质模型库
---
&nbsp;

## 概述

TYMedia 热流介质模型库，提供了多种热流系统中的常用介质，包括基于 Helmholtz 方程的介质、CoolProp 介质、不可压缩流体介质和固体介质，支持用户同时调用 TYMedia 和 Modelica.Media 中的介质，如理想气体、Water_IF97 等。该模型库主要应用于热流相关模型库对介质物性的调用，可计算工作介质在单相或两相状态下的物性参数，实现介质物性最大程度的复用，满足不同场景下热流系统的建模需求。

## 功能要点

- 提供多种介质模型，包括基于 Helmholtz 方程的介质、CoolProp 介质、不可压缩流体介质和固体介质；

- 描述介质在不同热力学过程中的行为特征；

- 模拟设备中流动与传热过程中的介质状态；

- 配合其他专业库实现在能源、航空、船舶、综合能源等领域的应用。

## 模型库目录

TYMedia 热流介质模型库提供了热流系统中常见的介质模型，主要包括基于 Helmholtz 方程的介质、CoolProp 介质、不可压缩流体介质和固体介质。采用可替换重申明（replaceable/redeclare）机制，将设备模型与介质模型分离，开发设备模型时调用介质模型模板，实例化设备时，将具体介质与设备关联，便可得到带有介质的实例化设备模型。

<table>
	<tr bgcolor="#F6F8FA">
	    <th colspan="2"  width="50%">名称</th>
	    <th>描述</th>  
	</tr>
	<tr>
	    <td>UsersGuide</td>
	    <td>用户指南</td>
	    <td>提供模型库概述、联系方式、版本说明等介绍文档</td>
	</tr>
	<tr>
        <td>Interfaces</td>
        <td >接口库</td>
        <td>提供模型库组件的接口模型，可用于模型组件的开发</td>
    </tr>
	<tr>
	    <td>Helmholtz</td>
	    <td>基于 Helmholtz 方程的介质库</td>
        <td>提供了 CO2、R134a、R410a、R1234yf 等多种制冷剂介质</td>
     </tr>
	<tr>
	    <td>CoolProp</td>
	    <td>CoolProp 介质库</td>
        <td>调用 CoolProp 开源库，提供了液氢、液氧、甲烷、R22 等介质</td>
     </tr>
	<tr>
	    <td>Incompressible</td>
	    <td>不可压缩流体介质库</td>
        <td>提供了铅铋合金、铅、铋、乙二醇水溶液等介质</td>
     </tr>
	<tr>
	    <td>Solid</td>
	    <td>固体介质库</td>
        <td>提供了石墨、不锈钢、碳化硼、铝等常用固体介质</td>
     </tr>               
</table>


## 应用场景

- 介质物性计算

    支持建立和模拟多种介质的物性参数计算，包括密度、粘度、比热、导热系数等，可以准确计算介质在不同状态下的物性值。

- 热流系统仿真计算

    支持热流系统获取和设置介质的物理特性参数，比如密度、粘度、比热、导热系数等，对于热流系统的设计具有重要意义，可用于计算和仿真介质在系统中的流动和传热性能。

## 应用案例

水箱系统模型如下图所示，液体介质从水箱流出，经三通接头分流后，分别流经管道和阀门，而后在三通内汇流通过泵流回水箱，实现循环。

系统模型：

<img :src="$withBase('/FluLib/TYMedia/1.png')" style="width:868px;">

密度曲线：

<img :src="$withBase('/FluLib/TYMedia/2.png')"  style="width:498px;">

导热系数曲线：

<img :src="$withBase('/FluLib/TYMedia/3.png')"  style="width:498px;">


