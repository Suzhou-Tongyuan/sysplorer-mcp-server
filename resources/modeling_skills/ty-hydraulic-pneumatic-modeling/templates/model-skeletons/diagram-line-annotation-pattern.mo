partial model DiagramLineAnnotationPattern
  // Pattern only. Do not load this file as a runnable TY model.
  // Replace component classes, ports, and coordinates with the selected TY components.
  //
  // Required instance pattern:
  //
  //   SelectedSource pSrc
  //     annotation(Placement(transformation(origin={-110,40}, extent={{-10,-10},{10,10}})));
  //   SelectedValve dcv
  //     annotation(Placement(transformation(origin={0,20}, extent={{-12,-12},{12,12}})));
  //   SelectedActuator act
  //     annotation(Placement(transformation(origin={90,20}, extent={{-18,-10},{18,10}})));
  //   SelectedTank tank
  //     annotation(Placement(transformation(origin={0,-60}, extent={{-12,-12},{12,12}})));
  //
  // Required connection pattern:
  //
  // equation
  //   connect(pSrc.port, dcv.P)
  //     annotation(Line(points={{-100,40},{-50,40},{-50,20},{-12,20}}, color={0,0,255}));
  //   connect(dcv.A, act.A)
  //     annotation(Line(points={{12,26},{45,26},{45,30},{72,30}}, color={0,0,255}));
  //   connect(dcv.B, act.B)
  //     annotation(Line(points={{12,14},{45,14},{45,10},{72,10}}, color={0,0,255}));
  //   connect(dcv.T, tank.port)
  //     annotation(Line(points={{0,8},{0,-25},{0,-48}}, color={0,0,255}));
  //
  annotation(
    Diagram(coordinateSystem(extent={{-140,-100},{140,100}})),
    Icon(coordinateSystem(extent={{-140,-100},{140,100}})));
end DiagramLineAnnotationPattern;
