---
title: Pitch system errors
component: pitch
doc_type: fault
tags: [pitch, blade, deviation, encoder, accumulator, battery, Blds_PitchAngle]
---

# Pitch system errors

A pitch angle deviation alarm means one blade does not agree with the pitch reference, or does not agree with the other blades. On the EDP layout the collective signals are `Blds_PitchAngle_Avg`, `_Min`, `_Max`, and `_Std`. A large gap between min and max, or a high standard deviation, is asymmetry. A blade 2 deviation alarm names the blade; confirm the turbine numbers blades the same way the alarm does.

This fault does not heat gearbox oil. Do not start with the cooler.

## Symptoms in SCADA

- Pitch angle deviation alarm on blade 2 (or blade 1 or 3), often with `Blds_PitchAngle_Std` up while collective average still looks plausible.
- The turbine holds a power limit, or it feathers and restarts, with the same blade named each time.
- Asymmetry shows up as tower vibration or a rotor-imbalance alarm, and as a power deficit versus the power curve, not as `Gear_Oil_Temp_Avg`.
- On a hydraulic pitch system: accumulator pressure low, pitch-oil level low, or a slow feather time on the named blade.
- On an electric pitch system: pitch-battery or ultracapacitor cabinet alarm, pitch-converter fault on one blade, or an encoder mismatch.
- Below rated wind, a steady offset of about a degree on one blade can be an encoder bias. Above rated, a multi-degree disagreement is a stop. Those degree figures are site-practice examples. Use the alarm manual.

## Likely causes

1. Encoder or blade-position sensor fault on the named blade. The blade may be mechanically fine while the controller sees a deviation. Compare the local pitch-cabinet reading to the SCADA angle before you pull a cylinder or a motor.
2. Hydraulic pitch: internal leak on that blade's proportional valve or cylinder, so the blade creeps and the pump runs often. Accumulator pre-charge low makes every blade slow, not just blade 2.
3. Electric pitch: battery, ultracapacitor, or blade-cabinet charger failed on one blade, so the emergency feather is not guaranteed. That is a safety stop, not a "watch it" alarm.
4. Limit switch or end-stop misadjusted after a blade bearing job, so the blade never reaches the commanded fine pitch.
5. Cabling or slip ring (where fitted) intermittent as the rotor turns. The deviation alarm comes and goes with rotor position or with humidity.
6. Icing or a heavy aerodynamic imbalance that the pitch loop cannot trim. Look at ambient temperature and at whether the other turbines on the pad are curtailing for ice.

## Discriminating checks

- Read min, max, and standard deviation of pitch, not only the average. The average hides one bad blade.
- Identify hydraulic versus electric pitch from the platform manual before blaming an accumulator or a battery.
- Check accumulator pressure or battery impedance for the named blade, and compare to the other two cabinets. One cabinet different from the other two is the fault location.
- Feather-time test, if the manual includes one: one slow blade is a valve, cylinder, or motor. Three slow blades is oil, pump, or supply.
- Look at rotor speed stability and tower motion. A true aerodynamic offset produces a once-per-revolution signature. A pure encoder bias may not, if the blades are actually together.

## Twin evidence to request

The gearbox thermal twin will look normal during a pitch deviation, and that is useful negative evidence: do not open the gearbox for this alarm. Evidence is the pitch-angle spread and the cabinet alarms. A power-curve deficit versus sisters at the same wind speed supports a real angle error rather than a nuisance encoder bit.

## Escalation

Any alarm that says the emergency feather path is not available (battery, ultracapacitor, accumulator below the manual's minimum) is a stop. A small encoder offset below rated wind, with feather tests passed, can wait for a scheduled encoder calibration if the alarm manual agrees. Repeated blade 2 deviation trips in one shift are a stop and a cabinet inspection, not another remote reset.

## Worked trace

Read `Blds_PitchAngle_Min`, `Blds_PitchAngle_Max`, and `Blds_PitchAngle_Std` for the hour of the alarm, not the collective average. A pitch angle deviation alarm on blade 2 with the standard deviation up, and min and max several degrees apart, is one blade leaving the other two. The average can still look like a normal fine-pitch number and hide it.

Then name the architecture. Hydraulic pitch: compare accumulator pressure and valve command on blade 2's cabinet with blades 1 and 3. One cabinet low is that blade's valve, cylinder, or sensor. All three low is the power pack. Electric pitch: compare the battery or ultracapacitor alarm and the encoder fault on blade 2 only. A safety-path alarm on one cabinet stops the turbine even if the angle error looks small, because the feather you are counting on is the one that failed.

Gearbox oil temperature is not part of this trace. If it is the channel that moved, close this note.

## One cabinet, then the safety path

On a pitch angle deviation alarm for blade 2, compare that blade's cabinet with the other two before you touch the hub. Encoder fault only on blade 2, with the other cabinets quiet, is an encoder or a cable on blade 2. Battery, ultracapacitor, or accumulator below the manual's minimum on any cabinet is not an encoder job and is not left until the next low-wind day. Resetting the deviation alarm without reading the cabinet leaves the same stop an hour later. Record min, max, and standard deviation from the hour of the alarm in the work order so the average cannot hide the blade. A blade 2 deviation that repeats after a reset is the same fault, not a new one.
