---
title: Gearbox HSS bearing over-temperature
component: gearbox
doc_type: fault
tags: [gearbox, hss, bearing, temperature, partial load, Gear_Bear_Temp_Avg]
---

# Gearbox HSS bearing over-temperature

The high-speed shaft (HSS) bearing is the gearbox temperature channel that should worry you first when it climbs on its own. On the EDP SCADA layout, `Gear_Bear_Temp_Avg` is that HSS bearing temperature. `Gear_Oil_Temp_Avg` is the sump, not the bearing. Treat a rising bearing with a calm sump as a bearing or local-lubrication problem until a check says otherwise.

## Symptoms in SCADA

A healthy gearbox shows the bearing a few degrees above the oil. Both channels follow power (`Grd_Prod_Pwr_Avg`), rotor speed (`Rtr_RPM_Avg`), and nacelle temperature (`Nac_Temp_Avg`).

The bearing signature is different:

- `Gear_Bear_Temp_Avg` ramps over hours or days while `Gear_Oil_Temp_Avg` stays flat.
- The split `delta_bear_oil = Gear_Bear_Temp_Avg - Gear_Oil_Temp_Avg` widens.
- It keeps widening at partial load, when power is well below rated and rotor speed is only in the mid band. Full-load heat that lifts oil and bearing together is a cooling story, not this one.
- The split does not close after the turbine comes back to a lower power setpoint.
- Sister turbines in the same wind and the same nacelle temperature do not show the split.

A step change of many degrees in one 10-minute sample, with no matching oil or power move, is more often a sensor or wiring fault than a bearing that failed between two averages.

## Likely causes

Ranked for a partial-load rise of HSS bearing temperature with oil still normal:

1. HSS bearing damage (spall, skidding, poor lubrication film on the rolling elements). The split widens first. Particles and vibration usually come later, not before the temperature trend.
2. Local lubrication starvation at the HSS bearing: blocked orifice, marginal oil level when the nacelle is tilted, or a jet that no longer reaches the bearing. Oil sump temperature can still look normal.
3. Oil aeration or the wrong oil grade after a top-up, so the film at the HSS collapses under load while the bulk sump is only slightly warmer.
4. Cooler fouling, a failed cooler fan, or a thermostat stuck in bypass. These lift the oil as well. Do not rank them first when `Gear_Oil_Temp_Avg` is flat. See the gearbox oil over-temperature note.
5. Bearing-temperature sensor drift or a loose probe. Look for a step, a frozen value, or a channel that disagrees with a second gearbox temperature reading.

## Discriminating checks

- Plot 7 to 14 days of `Gear_Bear_Temp_Avg`, `Gear_Oil_Temp_Avg`, power, rotor speed, and nacelle temperature. Mark the moment the split started.
- Compare two or three sister turbines for the same hours. A farm-wide rise in both oil and bearing on a hot afternoon is ambient, not an HSS bearing.
- Read gearbox oil pressure, filter differential pressure, oil level, and the latest particle count or ISO code. Low pressure or a climbing ISO code supports starvation or damage. A clean count and normal pressure do not clear the bearing; they only say the sump filter has not caught debris yet.
- If a condition-monitoring system is installed, look at the HSS bearing envelope spectrum rather than the overall gearbox level.
- Check whether anyone topped up oil, changed filters, or aligned the coupling in the last service visit.

## Twin evidence to request

Ask the hybrid drivetrain twin for the residual on `Gear_Bear_Temp_Avg`, not for a cause label. The physics expectation comes from nacelle temperature and rotor speed. A residual that grows while that expectation stays calm means the heat is not explained by the operating point. Also ask whether the sustained-alarm flag is set, and for how many consecutive 10-minute samples. The twin supplies evidence for the visit. It does not replace the oil sample or the borescope.

## Escalation

Follow the escalation thresholds procedure before you decide the turbine stays online. A slow partial-load split is a planned visit in the next low-wind window, with an oil sample and a filter inspection. A climb of several degrees per hour, a trip-level bearing alarm that returns after reset, or metal on the filter is a stop. Do not use a number from this note as an OEM trip setpoint; confirm the alarm manual for the platform.

## Worked trace

A partial-load pattern that has shown up on real gearboxes looks like this. Rated power is not required. Through the afternoon `Grd_Prod_Pwr_Avg` sits near half of rated, `Rtr_RPM_Avg` is steady in the mid band, and `Nac_Temp_Avg` is no hotter than the morning. `Gear_Oil_Temp_Avg` stays within a degree of its value at the same power last week. `Gear_Bear_Temp_Avg` is 8 °C higher than last week at that same power, and the next day it is higher again. The split widened while the operating point did not.

What you write down before calling anyone:

- The clock time the split first left the sister-turbine band.
- Power, rotor speed, and nacelle temperature at that time, so nobody later explains it as a full-load hot day.
- Whether oil pressure and filter dP were normal at that time. Normal pressure does not clear the bearing. It only says the gallery was not already dry.
- The twin residual on `Gear_Bear_Temp_Avg` if the service is up. A growing residual with a flat physics expectation matches this note. A residual that is just the whole pad running hot does not.

What you do not write down: a remaining-life number, or a trip setpoint copied from memory.
