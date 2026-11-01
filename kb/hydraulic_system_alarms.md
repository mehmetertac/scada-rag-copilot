---
title: Hydraulic system alarms
component: hydraulic
doc_type: fault
tags: [hydraulic, pressure, accumulator, Hyd_Oil_Temp_Avg, pitch, brake]
---

# Hydraulic system alarms

`Hyd_Oil_Temp_Avg` is the hydraulic group oil temperature on the EDP layout, not the gearbox sump. Gearbox oil is `Gear_Oil_Temp_Avg`. Mixing those two tags sends the technician to the wrong cooler.

Confirm on the platform whether pitch is hydraulic or electric before you blame a pitch manifold. Many turbines use electric pitch and keep hydraulics only for the rotor brake and the yaw brake. Others run hydraulic pitch from the same or a separate power pack.

## Symptoms in SCADA

- Hydraulic oil temperature high, with gearbox oil and HSS bearing normal.
- Hydraulic pressure low, a pump running continuously, or an accumulator pre-charge alarm.
- On hydraulic pitch: slow blade movement and a pitch deviation alarm together with low pressure. On electric pitch: a hydraulic alarm that does not move `Blds_PitchAngle_Std` is the brake or yaw circuit, not the blades.
- Oil level low in the hydraulic tank, often with a leak at a hose, a pitch slip ring (if hydraulic), or the brake caliper.
- Temperature high and pressure low together: the relief valve may be dumping, which heats the oil and collapses useful pressure.

## Likely causes

1. Cooler or fan on the hydraulic pack failed, or the cooler is blocked. Oil temperature rises, pressure stays acceptable until the oil is thin.
2. Relief valve dumping, a pump compensator failed, or a leak that forces the pump to run at full stroke. The oil heats because the pump's energy is going into the tank, not into a cylinder.
3. Accumulator bladder lost its pre-charge. Pressure cycles rapidly, the pump starts often, and pitch or brake response is soft. One accumulator can serve pitch; another can serve the brake. Read the tag on the alarm.
4. Low oil level from an external leak. Find the oil before you top up and walk away. A brake caliper leak and a pitch-cylinder leak are different urgencies.
5. Wrong oil or water in the oil, after a cooler-bundle leak on a water-cooled pack. Temperature and a milky sample.
6. Pressure transmitter fault. Compare to a gauge on the manifold before you replace a pump.

## Discriminating checks

- Write down which circuit is in alarm: pitch, brake, or yaw. The word "hydraulic" on its own is not a work order.
- Compare `Hyd_Oil_Temp_Avg` with `Gear_Oil_Temp_Avg`. Only one of them hot means one cooler.
- Count pump starts per hour. A rapid cycle points at accumulator pre-charge or a leak. A pump that never stops points at a relief valve or a large leak.
- Check pitch-angle standard deviation. If the blades are steady and pitch is electric, stop looking at the pitch cylinders.
- Inspect for fresh oil on the tower, the hub, and the yaw deck. Old black oil stains are not today's leak.

## Twin evidence to request

The gearbox twin does not model `Hyd_Oil_Temp_Avg`. A normal gearbox residual does not clear a hydraulic leak, and a hot gearbox does not explain hydraulic pressure. Use the hydraulic channels and the pitch or brake response.

## Escalation

Loss of brake hydraulic pressure, or loss of the emergency feather accumulator below the manual's minimum, is a stop. High hydraulic oil temperature with pressure still holding is a curtailment or a next-day cooler repair if the manual allows the turbine to run. A continuous pump plus a visible leak is a stop so the tank is not pumped empty. Example practice only: the alarm manual owns the setpoint.

## Worked trace

Start by separating the tags. `Hyd_Oil_Temp_Avg` hot and `Gear_Oil_Temp_Avg` normal means the hydraulic cooler or a dumping relief valve, not the gearbox cooler. Then name the circuit on the alarm text: pitch, rotor brake, or yaw brake. Electric pitch plus a steady `Blds_PitchAngle_Std` means you are not looking for a pitch cylinder even if the word hydraulic is on the screen.

Count pump starts. A pump that clicks on every few seconds is an accumulator that has lost pre-charge or a small leak. A pump that never stops, with oil temperature climbing, is a relief valve or a large leak, and the tank level is the next thing to read. Fresh oil on the deck tells you the leak is real. A transmitter that falls to zero in one sample while a local gauge still reads normal is the transmitter. Topping up a leaking tank without finding the oil is how the same alarm returns on the next shift.

## Name the circuit in the log

Write pitch, rotor brake, or yaw brake in the first line. `Hyd_Oil_Temp_Avg` only says the hydraulic pack is hot. It does not say which actuator is losing the oil. Electric pitch with a steady blade-angle spread means the blades are not the circuit, even when the alarm text says hydraulic. A brake-pressure loss is a stop. A hot pack with pressure holding is a cooler or a relief valve and can often wait for the next safe window if the manual allows the turbine to run. Topping up is not the repair. The repair is the leak, the bladder pre-charge, or the valve that is dumping into the tank. Record `Hyd_Oil_Temp_Avg` separately from `Gear_Oil_Temp_Avg` so the next reader does not open the gearbox cooler for a hydraulic pack.
