---
title: Gearbox oil over-temperature
component: gearbox
doc_type: fault
tags: [gearbox, oil, cooler, temperature, Gear_Oil_Temp_Avg]
---

# Gearbox oil over-temperature

Bulk oil temperature (`Gear_Oil_Temp_Avg`) going high while the HSS bearing stays in its normal band above the oil is a sump, cooler, or flow problem. It is not the HSS bearing damage pattern. If the bearing is the channel that runs away, use the HSS bearing note instead.

## Symptoms in SCADA

- `Gear_Oil_Temp_Avg` is high. `Gear_Bear_Temp_Avg` is also warmer than a cool day, but the split `delta_bear_oil` stays in the normal few degrees.
- Both channels move together with a hot afternoon, a long full-load run, or a cooler that stopped.
- Oil temperature stays high after power is reduced, which means heat is not leaving the sump.
- Nacelle temperature (`Nac_Temp_Avg`) is high on the whole pad, and sister turbines show the same oil rise. That is ambient load on the coolers, not a failed gearbox.
- Oil temperature high but bearing normal is the phrase to remember: the bearing probe is not the alarm.

A sump heater left on, where the platform has one, can heat oil at low power with almost no bearing response. Check the heater contactor before condemning the cooler.

## Likely causes

1. Cooler fan failed, or the fan contactor dropped out. Oil temperature rises over one or two hours at power. The bearing follows the oil with a normal split.
2. Radiator or plate cooler fouled with bugs, dust, or oil mist. Common after a dry, high-wind month. Sister turbines with clean coolers run cooler in the same wind.
3. Thermostat or bypass valve stuck so oil recirculates to the sump and skips the cooler. Fan may still be running. Oil stays hot from moderate power upward.
4. Oil pump flow low (wear, relief valve dumping, clogged suction strainer). Pressure is often low or unstable as well, especially once the oil is hot and thin. See the lubrication alarms note if pressure is the first symptom.
5. Wrong oil or degraded oil (viscosity down, water up), so the cooler and the bearings both run hotter. An oil sample decides this. Do not change oil on temperature alone.
6. Sustained operation above the rated power curve in hot ambient. The cooler is doing what it can. Restrict power before opening the gearbox.

## Discriminating checks

- Confirm the cooler fan is actually turning, not only commanded. Look at fan current if it is on SCADA, or at the nacelle on the next visit.
- Compare oil temperature against nacelle temperature and against two sister turbines at the same power. A 10 °C gap versus the sisters at the same power is a cooler or flow fault. A 2 °C gap on a hot day is not.
- Read oil pressure at operating speed. Pressure that collapses only when oil is hot points at viscosity or a relief valve, not at a seized pump.
- Check the last oil sample for water, viscosity, and particle count.
- Look at filter differential pressure. A filter in bypass can coincide with temperature trouble but is a separate defect.

## Twin evidence to request

Ask the twin for the physics and hybrid expectation of `Gear_Oil_Temp_Avg` at the current rotor speed and nacelle temperature. If the measured oil sits well above both expectations and the bearing residual is small, the heat balance is broken in the cooler or the flow path. If the bearing residual is the one that grows, you are in the wrong note.

## Escalation

A failed cooler fan with oil still below the platform alarm is a power restriction and a next-day visit, not an automatic gearbox condemnation. Oil at the trip level, oil pressure lost at speed, or an alarm that returns immediately after reset is a stop. Example site practice only: do not copy a setpoint out of this note. Use the escalation procedure and the turbine alarm manual.

## Worked trace

Oil high, bearing normal, same wind as the neighbors. At a steady power, this turbine's `Gear_Oil_Temp_Avg` sits about 10 °C above two sisters. `Gear_Bear_Temp_Avg` is higher too, by about the same 10 °C, so the split is unchanged. `Nac_Temp_Avg` matches the sisters, so the nacelle is not the extra heat. That is a cooler or a flow path on this turbine, not an HSS race.

Check the fan before you change oil. A fan that is commanded and drawing no current is the visit. A fan that runs, with fins packed with seed and dust, is the same visit with a brush instead of a contactor. A fan that runs and a radiator that is clean, with oil still hot from moderate power up, is the bypass valve or the pump flow, and oil pressure versus the sisters tells those two apart.

If the split had widened and the oil had stayed put, leave this note. That trace belongs to the HSS bearing note.

## Cooler visit, not a gearbox opening

The job is the fan, the fins, the bypass valve, or the flow. Opening the inspection cover because the sump is hot, with a normal bearing-oil split and a dirty cooler, is the wrong repair. Clean or replace the cooling path, run the turbine back to the same power, and compare `Gear_Oil_Temp_Avg` with the sisters again. If the gap closes, the sump was the cooler. If the gap stays and the split then widens, stop and move to the bearing note. Do not change the oil on the first hot afternoon. A sample can wait for the cooler to be proven. If the sisters are just as hot at the same power and the same nacelle temperature, there may be nothing to repair on this turbine that day.
