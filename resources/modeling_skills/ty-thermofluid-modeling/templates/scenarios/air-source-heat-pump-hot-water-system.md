# Air-Source Heat-Pump Hot-Water System

## Applicable Scenario

- Build an air-source heat-pump hot-water system that follows the loop:
  `air-side heat absorption -> refrigerant compression and heating -> water-side heat release -> tank thermal storage and hot-water supply`.
- Cover an outdoor heat exchanger, compressor, water-side heat exchanger, expansion valve, insulated storage tank, and user hot-water load.
- Represent dynamic start/stop behavior where the heat pump starts below the tank temperature setpoint and stops above the stop threshold; simulate it only when simulation is in the requested scope.

This template inherits the requested terminal stage. File delivery or offline review does not automatically start Sysplorer; use static checks when no live operation is requested. Explicit live read-only queries follow this skill's common action rules and do not authorize additional model checks, simulation, or edits. Check-only work does not add translation or simulation. Read result variables only when agreed result acceptance requires them.

## Default Structure

- Refrigerant-side main loop:
  `outdoor heat exchanger (evaporator) -> compressor -> water-side heat exchanger (condenser) -> expansion valve -> outdoor heat exchanger`
- Water-side storage loop:
  `cold return / user return -> storage tank -> water-side heat exchanger -> hot-water supply -> user hot-water load -> cold return`
- Control loop:
  `tank average temperature -> start/stop logic with hysteresis -> compressor start/stop or adjustment signal`

## Required Elements

- Outdoor air boundary and outdoor heat exchanger
- Refrigerant compressor
- Water-side heat exchanger
- Expansion valve
- Insulated storage tank
- User hot-water load or equivalent demand branch
- Measurement points for tank temperature, supply/return temperature, compressor power, and heat output

## Recommended Inputs

- Ambient air temperature
- Refrigerant type and phase-state assumptions
- Cold return temperature
- User demand or flow-rate profile
- Tank volume, insulation level, and initial temperature
- Compressor start threshold, stop threshold, or hysteresis band
- Requested result variables such as hot-water outlet temperature, tank average temperature, compressor power, and COP

## Candidate Validation Variables (Only When Result Review Is Required)

- Hot-water outlet temperature
- Tank average temperature
- Cold return temperature
- Compressor power
- Water-side heat output
- System COP

## Modeling Tips

- Build and validate the refrigerant main loop to the requested stage before coupling the water-side tank and user load; do not require a simulation for file or check-only work.
- If the control logic is not fixed yet, first validate the main loop within the requested scope with a simple on/off command, then add tank-temperature start/stop logic.
- Only when COP review is requested, use `COP = water-side heat output / compressor power` unless the user specifies another definition, and state the definition in the delivery.
