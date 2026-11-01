---
title: EDP SCADA tag glossary
component: scada
doc_type: reference
tags: [glossary, EDP, SCADA, tags, sensors]
---

# EDP SCADA tag glossary

These names match the public EDP wind-turbine SCADA layout used in the sibling drivetrain work. A site export can rename them. Confirm the signal list before you write a work order that depends on a tag. Averages are 10-minute unless the site says otherwise. `_Std`, `_Min`, and `_Max` are the same interval's spread, not extra sensors.

## Drivetrain temperatures

- `Gear_Oil_Temp_Avg`: gearbox oil sump temperature. Bulk oil. Not the HSS bearing and not the hydraulic pack.
- `Gear_Bear_Temp_Avg`: gearbox high-speed shaft bearing temperature. The channel in the HSS bearing note. Published EDP gearbox studies treat this tag as the HSS bearing.
- `Gen_Bear_Temp_Avg`: one generator bearing temperature. Drive end or non-drive end must be confirmed on the signal list.
- `Gen_Bear2_Temp_Avg`: the other generator bearing temperature. Do not assume this is the NDE bearing without the drawing.
- `Nac_Temp_Avg`: nacelle air temperature. The thermal model uses it as the ambient proxy for the gearbox. It is not outside air if the nacelle cooler is dumping heat into the same volume.
- `Hyd_Oil_Temp_Avg`: hydraulic group oil temperature. Brake, yaw, or pitch hydraulics depending on the platform. Never the gearbox sump.

## Speed, pitch, power, wind

- `Rtr_RPM_Avg`: rotor speed. A thermal driver in the gearbox model. Near zero means the temperature you see is a hot-soak or a sensor, not load heat.
- `Gen_RPM_Avg`: generator speed. With rotor speed, a rough check that the gearbox ratio is still the ratio you think it is.
- `Blds_PitchAngle_Avg`: collective blade pitch angle. Hides a single-blade fault.
- `Blds_PitchAngle_Min`, `Blds_PitchAngle_Max`, `Blds_PitchAngle_Std`: spread across blades. High standard deviation is asymmetry. This is the pitch-deviation evidence in the pitch note.
- `Grd_Prod_Pwr_Avg`: grid-side active power. Partial load means this is well below rated while a temperature alarm is active. That contrast is the HSS bearing story when the oil is calm.
- `Amb_WindSpeed_Avg`: nacelle or turbine wind speed. Use it for power-curve comparisons. A yaw error shows up as low power at a given wind speed.
- `Amb_WindDir_Avg`: wind direction used with nacelle position to judge yaw error. A constant offset is a vane or a north calibration, not a gearbox.

## Derived checks used in the fault notes

- `delta_bear_oil`: `Gear_Bear_Temp_Avg` minus `Gear_Oil_Temp_Avg`. Widening split with oil flat is the HSS bearing note. Both channels high and the split normal is the oil-cooler note.
- Sister comparison: the same tag on two or three neighboring turbines for the same timestamps. A pad-wide move is weather or the grid. A one-turbine move is a component or a sensor.
- Hybrid twin residual: measured temperature minus the twin's expected temperature from the operating point. Request it for gearbox oil and HSS bearing. Do not invent a residual for pitch, yaw, or grid voltage; those notes do not have one in the current twin.

## Tags this glossary does not define

Converter trip codes, relay targets, oil pressure, filter differential pressure, particle counters, cable-twist count, and accumulator pressure are real alarms and are often missing from the public EDP temperature export. When a note mentions them, they come from the turbine alarm list or the local controller, not from `Gear_Bear_Temp_Avg`. If the historian does not have the tag, say so, and do not substitute a temperature.

## Confirming a renamed tag

Sites export the same physical sensor under another name. Before you trust a retrieval that mentions `Gear_Bear_Temp_Avg`, match the historian name to the signal list and to the unit (°C, not a raw count). A tag that is flat at 0 or stuck at one value for a week is not a healthy bearing. It is a dead channel, and every note that cites it is blocked until the channel is fixed.

If the site has no twin residual, say that too. Do not fill the gap with a hand-drawn "expected temperature." The fault notes ask for the residual only where [wind-digital-twin](https://github.com/mehmetertac/wind-digital-twin) actually computes one: gearbox oil and HSS bearing. Pitch angle, yaw error, hydraulic pressure, and grid voltage do not have that residual. Quoting one for them is a wrong citation, not a cautious one.

## Averages hide spikes

These tags are 10-minute means. A bearing that spikes for one minute and recovers can vanish into `Gear_Bear_Temp_Avg`. A pitch blade that kicks and returns can vanish into `Blds_PitchAngle_Avg` while `_Std`, `_Min`, and `_Max` still show it. When a note says to use the spread, do not substitute the average. When a channel is stuck, say the channel is stuck. A flat line at one value for a week is a dead sensor, and it must not be read as a healthy temperature or a healthy pitch angle. Units matter: a temperature tag delivered as a raw count will rank the wrong note. Confirm °C on the signal list before you compare a number in these pages with the historian. If the export renamed a tag, write the site name next to the EDP name in the work order once, and keep using the site name after that. The notes use the public EDP names so a search for `Gear_Bear_Temp_Avg` or `Blds_PitchAngle_Std` still lands.
