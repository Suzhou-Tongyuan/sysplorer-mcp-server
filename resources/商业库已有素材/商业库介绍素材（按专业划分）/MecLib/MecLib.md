# 机械模型库
---
&nbsp;

机械模型库需要 License 解锁使用，若有需要，请获取 License 使用许可。

<table>
	<tr bgcolor="#F6F8FA">
	    <th width="12%">主题</th>
	    <th width="20%">模型库名称</th>
		<th width="20%">模型库用户手册</th>
	    <th width="48%">说明</th>
	</tr>
	<tr>
	    <td><a href="#/Doc/MecLib/TYMultibody.html">多体系统模型库</a></td>
	    <td>TYMultibody V1.5.0</td>
		<td><a :href="$withBase('/Resource/Reference/附录A-10多体系统模型库V1.5.0产品用户手册-C.pdf')" target="_blank">多体系统模型库产品用户手册</a></td>
	    <td>TYMultibody 多体系统模型库是通用的三维多刚体系统建模仿真模型库，应用于多体动力学和复杂多领域系统的运动学和动力学分析，包含各种刚体、柔性梁、关节副、约束、力和传感器模型，可应用于车辆、船舶、航空航天、工程机械等专业领域，满足对多体动力学系统的动态特性分析和性能优化需求。</td>
	</tr>
    <tr>
	    <td><a href="#/Doc/MecLib/TYMechanics.html">基础机械模型库</a></td>
	    <td>TYMechanics V1.2.0</td>
		<td><a :href="$withBase('/Resource/Reference/附录A-10基础机械模型库V1.2.0产品用户手册- B.pdf')" target="_blank">基础机械模型库产品用户手册</a></td>
	    <td>TYMechanics 基础机械模型库包含一维平动机械模型和一维转动机械模型，用于基础机械力学特性建模仿真，提供可变质量与可变转动惯量、非线性弹簧阻尼、多种接触和摩擦、理想齿轮、齿轮齿条等力学模型。满足工程领域对各种机械力学特性，包括线性、非线性和时变特性的建模需求，可应用于各类机电系统建模仿真和各种性能分析，例如车辆、工业装备中的各类直线驱动或减速器传动系统的性能分析。</td>
	</tr>
    <tr>
	    <td><a href="#/Doc/MecLib/TYDriveline.html">传动系统模型库</a></td>
	    <td>TYDriveline V2.1.0</td>
		<td><a :href="$withBase('/Resource/Reference/附录A-10传动系统模型库V2.1.0产品用户手册-C.pdf')" target="_blank">传动系统模型库产品用户手册</a></td>
	    <td>TYDriveline 传动系统模型库是在 TYMechanics 模型库基础上开发的，是面向传动系统建模仿真的专用模型库，包含机构、动力源、齿轮、连接器、刹车、传动附件、执行器、绳索，共 8 类传动模型。该版本模型库在架构和内容上进行了一定优化，包括适配同元标准库 Modelica4.0.0.TY.1，完善模型文档浏览器内容及优化部分模型等。模型库覆盖车辆、船舶、航空航天、工程机械、装备制造等行业的传动系统模型需求，可以实现对机械传动系统多种详细特性的分析和改进需求。</td>
	</tr>
	<tr>
	    <td><a href="#/Doc/MecLib/TYFlexBody.html">柔性体模型库</a></td>
	    <td>TYFlexBody V1.1.0</td>
		<td><a :href="$withBase('/Resource/Reference/附录A-10柔性体模型库V1.1.0产品用户手册-C.pdf')" target="_blank">柔性体模型库产品用户手册</a></td>
	    <td>TYFlexBody 柔性体模型库包括柔性体、模态梁、读取 Mnf 文件信息组件等模型，适用于部分变形不可忽略构件的多体动力学系统的建立。该库可用于航空航天、车辆船舶、工程机械等领域，支持用户在刚柔耦合系统中的方案设计、系统集成阶段的动态特性仿真分析，模拟其中柔性体的物理特性，典型的应用场景包括：工程机械混凝土泵车臂架刚柔耦合仿真、航天器卫星帆板刚柔耦合仿真、车辆动力学刚柔耦合仿真、航空起落架刚柔耦合仿真、机器人运动控制刚柔耦合仿真。</td>
	</tr>
    <tr>
	    <td><a href="#/Doc/MecLib/TYContact.html">接触模型库</a></td>
	    <td>TYContact V1.3.0</td>
		<td><a :href="$withBase('/Resource/Reference/附录A-10接触模型库V1.3.0产品用户手册-C.pdf')" target="_blank">接触模型库产品用户手册</a></td>
	    <td>TYContact 接触模型库包括球体、圆柱体、圆锥体、平面等常用刚体的接触元件，可以模拟不同刚体间的点接触和线接触、面接触功能，也可以模拟其在二维固定平面的简化接触，其作为产品货架体系中一款专业基础库，是机械多体库的功能扩展，研究和解决机械接触领域中的接触状态和接触力的问题。</td>
	</tr>
    <tr>
	    <td><a href="#/Doc/MecLib/TYDriveline3D.html">三维传动系统模型库</a></td>
	    <td>TYDriveline3D V2.1.0</td>
		<td><a :href="$withBase('/Resource/Reference/附录A-10三维传动系统模型库V2.1.0产品用户手册-C.pdf')" target="_blank">三维传动系统模型库产品用户手册</a></td>
	    <td>TYDriveline3D 三维传动系统模型库涵盖了各种机械传动系统零部件建模仿真模型，如绳索传动、链条传动、齿轮传动以及空间机构传动应用于三维传动系统的运动模拟和动力学分析，三维传动系统模型库包含绳索、滑轮、绞盘、链条、链轮、各类齿轮刚体和接触力、行星齿轮、空间机构、弹性轴承以及各种厂商型号的滚动轴承等模型。该库支持航空航天、车辆船舶、工程机械等领域机械传动系统的设计、仿真以及优化，例如三维齿轮建模及啮合传动模拟、验证绳索滑轮传动系统的动力学特性等，满足对三维传动系统动态载荷计算和效率提升需求。</td>
	</tr>
    <tr>
	    <td><a href="#/Doc/MecLib/TYMechanics2D.html">平面机械模型库</a></td>
	    <td>TYMechanics2D V1.1.0</td>
		<td><a :href="$withBase('/Resource/Reference/附录A-10平面机械库V1.1.0产品用户手册-A.pdf')" target="_blank">平面机械模型库产品用户手册</a></td>
	    <td>TYMechanics2D 平面机械模型库，包括多种力源、平面环境重力、平面组件、运动副、传感器等模型。模型支持三个自由度设置，包括沿 x 和 y 轴向的平移以及绕 z 轴的旋转。模型元素可在 3D 视图中进行动画演示。该库可应用于各类平面运动机械的系统设计和运动学及动力学仿真分析，例如挖掘机机械臂模型设计和系统运动学分析、车辆悬架系统振动特性分析等，用户可根据实际需求搭建高粒度平面机械模型及系统模型。</td>
	</tr>
</table>

