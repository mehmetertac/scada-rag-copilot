---
title: Drivetrain inspection checklist
component: drivetrain
doc_type: procedure
tags: [inspection, checklist, borescope, oil sample, vibration, thermography]
---

# Drivetrain inspection checklist

Use this list to turn a temperature or debris alarm into a visit plan. It is a field checklist, not a permit to open a hot, pressurized gearbox. Stop criteria and who is allowed to isolate the turbine live in the escalation procedure and in the site's safety rules.

## Before anyone climbs

- Print the alarm list and a 14-day trend: `Gear_Oil_Temp_Avg`, `Gear_Bear_Temp_Avg`, `Gen_Bear_Temp_Avg`, `Gen_Bear2_Temp_Avg`, `Hyd_Oil_Temp_Avg`, power, rotor speed, nacelle temperature.
- Note the bearing-minus-oil split and whether it widened at partial load.
- Pull the hybrid twin residual for the gearbox bearing and oil, and write down whether the sustained-alarm flag was set. The residual is a reason to visit. It is not a measurement of crack length.
- Read the last three work orders: oil top-up, filter, regrease, alignment, cooler clean.
- Check the oil-sample due date and the last ISO code, water, viscosity, and ferrous index.
- Decide what the visit must answer. "Bearing versus cooler" needs trends and a cooler inspection. "Debris" needs a filter cut and a sample. Do not climb with a blank question.

## In the nacelle, if the visit is authorized

- Oil level on the sight glass, at a noted nacelle position. Leaks at the HSS labyrinth, the cooler hoses, and the drain fittings.
- Cooler fins: blocked, oily, or a fan that does not turn when commanded.
- Main filter differential-pressure indicator and any bypass flag. Offline filter status.
- Particle counter or debris monitor local display, compared with SCADA.
- Coupling dust and the alignment marks. Fresh red dust after a recent alignment is a finding.
- Generator shaft-grounding brush wear, if the platform has a brush, whenever a generator bearing was the alarm.
- Pitch cabinets only if the alarm was pitch: one cabinet unlike the other two, battery date or accumulator pressure.
- Yaw vane condition and the cable-twist counter if the complaint was a power-curve deficit.
- Hydraulic tank level and fresh leaks if `Hyd_Oil_Temp_Avg` or hydraulic pressure was the alarm.

## Condition-based items, not every visit

- Oil sample: viscosity, water, particle count, Fe, Cu, PQ index. Take it from the documented sample point, not from a random drain.
- Filter cut-open, photographed, when dP, debris, or a metal alarm says the pleats have a story.
- Borescope of the gear teeth and the HSS bearing area when the split, the particles, or the OEM desk says damage is plausible. Borescope is not the first step of a hot-oil afternoon.
- Vibration or CMS spectrum on the named bearing, if the system is installed and someone on the visit can actually read it.
- Thermography of the cooler face and of electrical cabinets when the question is "fan versus sensor" or a hot connection. A camera is not a bearing diagnosis.

## What to bring back

- Photographs of the cooler, the level, the filter indicator, and any leak.
- The sample bottle id and the time, power, and oil temperature when it was taken.
- A one-line answer to the question the visit was meant to close, plus what is still unknown.
- Whether the turbine was left running, curtailed, or stopped, and which procedure allowed that choice.

## What this checklist does not cover

Isolation, locking, and working at height are the site safety system. This note does not authorize a restart after a protection trip. If the escalation procedure says stop, the checklist starts only after the turbine is in the state that procedure requires.

## Questions the visit has to answer

Leave with one of these closed, and say which one:

- Bearing versus cooler: did the split widen while oil stayed put, and is the cooler fan actually moving air?
- Debris: was there metal on the filter, and is the sample bottle labeled with power and oil temperature?
- Generator end: which tag is NDE, was grease added, and is the shaft brush still touching?
- Pitch cabinet: is blade 2's cabinet the one that differs, and is the feather path available?
- Hydraulic circuit: pitch, brake, or yaw, and is the oil on the deck or only on the screen?

A visit that photographs everything and answers none of these will be repeated next week. Write the answer in the work order in one sentence.
