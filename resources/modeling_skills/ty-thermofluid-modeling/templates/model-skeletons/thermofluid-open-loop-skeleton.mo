model ThermofluidOpenLoopSkeleton
  import SI = Modelica.Units.SI;

  replaceable package Medium = Modelica.Media.Water.StandardWater
    constrainedby Modelica.Media.Interfaces.PartialMedium
    "Replace with the actual medium package"
    annotation (choicesAllMatching = true);

  parameter SI.Pressure p_in = 3e5 "Replace with inlet pressure";
  parameter SI.Temperature T_in = 293.15 "Replace with inlet temperature";
  parameter SI.MassFlowRate m_flow_nominal = 1.0 "Replace with nominal flow rate";
  parameter SI.Pressure p_out = 1e5 "Replace with outlet pressure or loop closure condition";

  // Replace the following placeholders with concrete TY library components.
  //
  // Recommended open-loop chain:
  // inlet boundary -> driver/pump/fan -> main pipe -> load/heat exchanger -> outlet boundary
  //
  // Example placeholder slots:
  //   inletBoundary(redeclare package Medium = Medium)
  //   mainDriver(redeclare package Medium = Medium)
  //   mainPipe(redeclare package Medium = Medium)
  //   loadSection(redeclare package Medium = Medium)
  //   outletBoundary(redeclare package Medium = Medium)

annotation (
  Documentation(info = "<html><p>Use this skeleton as the starting point for a minimum open-loop thermo-fluid model. Replace the placeholder component slots with concrete classes from TYThermoFluidSys or TYAirTreatmentAndVentilation, then wire the chain in the same order.</p></html>")
);
end ThermofluidOpenLoopSkeleton;
