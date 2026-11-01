---
title: Generator winding over-temperature
component: generator
doc_type: fault
tags: [generator, winding, stator, cooling, unbalance]
---

# Generator winding over-temperature

Winding and stator-core temperatures follow current. They should fall when power is reduced. A generator bearing can keep climbing at modest power; a winding usually cannot, unless cooling air is actually blocked. Keep those two faults apart.

## Symptoms in SCADA

- Stator or winding temperature high at high `Grd_Prod_Pwr_Avg`, and clearly lower an hour later at half power.
- Cooling-air inlet to outlet split wider than the sister turbines at the same power. The generator is making the heat; the air path is not taking it out.
- One phase or one RTD hotter than the others by a wide margin. Think cooling distribution, a bad sensor, or current unbalance, not a gearbox.
- Temperature high with a dirty-filter alarm, a closed damper, or a cooling-water flow alarm on liquid-cooled machines.
- Nacelle temperature high and every turbine's winding temperature high together. That is ambient, plus whatever curtailment the manual allows.

If winding temperature rises while power and current stay moderate, and it does not fall when the turbine is idled, suspect a sensor or a cooling fan that is not running. Do not start with a rewind.

## Likely causes

1. Cooling-air filters plugged, dampers left closed after a visit, or the cooling fan stopped. The most common field finding.
2. Liquid-cooling flow low: pump, strainer, air in the circuit, or a cooler blocked on the ambient side. The flow or pressure switch is the confirming alarm.
3. Sustained overload or a poorly set power limit in hot ambient. The winding is inside its thermal model; the setpoint is the problem.
4. Current unbalance or a converter that is loading one phase. Compare phase currents. A winding RTD split that matches a current split is electrical.
5. Recirculation of hot nacelle air into the generator intake, often after a cover was left off or a baffle was removed.
6. A single RTD failed high. The other RTDs in that phase stay normal. Replace the sensor before you restrict the turbine for a week.

## Discriminating checks

- Plot winding temperature against power for this turbine and two sisters. Parallel lines mean the machine is healthy and the day is hot. A line that sits well above the sisters is cooling or loading.
- Check filter condition and fan rotation. A fan that hums and does not move air is a failed capacitor or a seized bearing in the fan, not a stator fault.
- Read phase currents and reactive power. Unbalance belongs with the converter note if the converter is the source.
- On a water-cooled stator, read inlet and outlet water temperature and the flow switch. A normal water split with one hot RTD is the sensor.
- Separate this from `Gen_Bear_Temp_Avg`. If only the bearing channel is hot, you are in the generator bearing note.

## Twin evidence to request

No winding residual is in the gearbox twin. Do not cite a calm `Gear_Bear_Temp_Avg` residual as clearance for the stator. Evidence is the winding-versus-power curve and the cooling-loop readings.

## Escalation

Derate or curtail if the manual gives a power limit for hot windings, and change filters in the next safe window. A cooling fan stopped at high power, a water-flow trip, or a winding alarm at the trip level is a stop. A single RTD that disagrees with the others is a sensor repair, and the turbine can run if the remaining RTDs are in band and the alarm manual allows it.

## Worked trace

Put winding temperature on the same axes as `Grd_Prod_Pwr_Avg` for this turbine and one sister. Two parallel lines on a hot day mean the stator is tracking current and the ambient is the story. A line that peels upward only on this turbine, at the same power, is filters, the fan, a closed damper, or recirculated nacelle air.

A single RTD that sits 20 °C above the other sensors in the same phase, while phase currents are balanced, is that sensor until a contact check says the copper is actually hot. Do not curtail the turbine for a week on one disagreeing RTD if the manual lets you run on the remaining sensors.

If the hot channel is `Gen_Bear_Temp_Avg` and the winding RTDs follow power normally, you are in the generator bearing note. Winding heat falls when you reduce power. A bearing that keeps climbing after the curtailment does not.

## Filters before a stator story

Most winding over-temperature visits end at the cooling path: a mat of dust on the intake filters, a damper left shut, a fan with a failed capacitor, or water flow that the switch says is present and the strainer says is not. Change or clean that path, return to the same power, and read the RTDs again the same day. A stator fault is what remains when cooling is restored and one phase is still hot in line with a current unbalance. Until that test is done, do not write "winding damage" in the log. Curtail to the manual's hot-day limit if the remaining RTDs agree the machine is hot, and say which limit you used.
