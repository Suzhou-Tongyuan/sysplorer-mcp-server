within ${PACKAGE_PATH};
model ${MODEL_NAME}
  annotation(
    Diagram(coordinateSystem(extent={{-200,-120},{200,120}}, preserveAspectRatio=false)),
    Icon(coordinateSystem(extent={{-200,-120},{200,120}}, preserveAspectRatio=false)));

  // Add instances with reviewable placement annotations.
  // Example:
  // NPSLibrary.Sources.SomeSource src
  //   annotation(Placement(transformation(extent={{-160,-20},{-120,20}})));

equation
  // Add real connections first.
  // Each diagram-visible connection should keep a matching Line(points=...) annotation.
  // Example:
  // connect(src.p, load.p)
  //   annotation(Line(points={{-120,0},{0,0}}, color={0,0,255}));

annotation (
  experiment(
    Algorithm=InlineImplicitEuler,
    InlineIntegrator=true,
    InlineStepSize=false,
    Interval=5e-5,
    StartTime=0,
    StopTime=2,
    Tolerance=0.0001,
    IntegratorStep=5e-5,
    StoreEventValue=0),
  uses(NPSLibrary(version="*"))
);
end ${MODEL_NAME};
