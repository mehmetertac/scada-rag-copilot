---
title: Generator bearing faults
component: generator
doc_type: fault
tags: [generator, bearing, NDE, DE, shaft current, Gen_Bear_Temp_Avg, Gen_Bear2_Temp_Avg]
---

# Generator bearing faults

Generator bearing temperature is not a gearbox bearing temperature. On the EDP SCADA layout the channels are `Gen_Bear_Temp_Avg` and `Gen_Bear2_Temp_Avg`. Which tag is drive end (DE, coupling side) and which is non-drive end (NDE, opposite the gearbox) has to be read from that turbine's signal list. Do not assume `Gen_Bear2_Temp_Avg` is the NDE bearing without the drawing.

## Symptoms in SCADA

- One generator bearing temperature trends up over days. The other generator bearing, the gearbox oil, and `Gear_Bear_Temp_Avg` stay on their normal tracks.
- The rise continues at modest power, not only at full load. Winding temperature, by contrast, follows current and usually falls when power is reduced.
- After a regrease visit, one bearing steps up several degrees and then settles over a day or two. That is often too much grease, not a failed race.
- Both generator bearings and the gearbox HSS rise together after a coupling job or a new alignment. Think misalignment or soft foot before you condemn a single race.
- NDE bearing temperature trend with DE stable, on a platform known to use shaft grounding, is the electrical pattern until the brush and the insulation are checked.

A generator NDE bearing temperature trend should be plotted against power, generator speed (`Gen_RPM_Avg`), nacelle temperature, and the other generator bearing. A trend that ignores power is mechanical or electrical. A trend that is a copy of power is more often cooling air or a sensor scaling issue.

## Likely causes

1. Lubrication: under-greased bearing, grease dried out, or the wrong grease mixed at the last service. Slow climb over weeks.
2. Over-grease from the last visit. Temperature step the day of the service, then a plateau. Do not keep adding grease to a hot bearing.
3. Mechanical damage: denting, skidding, or a turned inner ring. Temperature and, if fitted, bearing CMS amplitudes rise together.
4. Shaft current and fluting, classically discussed on the NDE when the grounding brush is worn, the shaft ground path is painted over, or the insulated bearing was bridged by a sensor conduit. The temperature rise can be modest until the race is badly fluted. Vibration or a shaft-voltage check decides this, not the temperature alone.
5. Misalignment or coupling lock-up. Both generator ends run hot, and the gearbox HSS may join them. Check the alignment report and coupling dust under the guard.
6. Sensor or cable fault on one bearing probe. Compare to the second bearing and to a contact measurement on the next visit before you order a bearing.

## Discriminating checks

- Confirm DE versus NDE from the signal list, then say "NDE" only after that confirmation.
- Compare the slope to the sister turbines. Generator bearings do not all age together unless the grease spec or the shaft-grounding maintenance was missed on the whole pad.
- Read the regrease log. A hot bearing the morning after a grease round is a grease fault until the trend says it is still climbing a week later.
- Inspect the shaft grounding brush or the insulated-end hardware if the platform has it. A worn brush with an NDE-only trend is a finding, not a footnote.
- If CMS exists, look for bearing frequencies on that end. Fluting often shows a raised noise floor rather than a clean bearing tone.
- Do not explain this alarm with pitch, yaw, or grid voltage. Those do not heat one generator bearing.

## Twin evidence to request

The drivetrain thermal twin is built for the gearbox oil and HSS bearing, not for `Gen_Bear_Temp_Avg`. Do not treat a calm gearbox residual as evidence that the generator bearing is healthy. Use the generator channels directly. A future generator-bearing residual would be a different model.

## Escalation

A slow single-ended climb with grease history is a planned visit: check the bearing, the grease quantity, and the shaft ground. A rapid climb, noise reported by the technician, or a trip-level generator bearing alarm is a stop. Fluting confirmed on the NDE is a planned bearing replacement, not another grease round. Setpoints come from the alarm manual, not from this note.

## Worked trace

Confirm the end before you say NDE. Open the signal list, find `Gen_Bear_Temp_Avg` and `Gen_Bear2_Temp_Avg`, and write which tag is drive end and which is non-drive end. Then plot the named end against power for 14 days, and plot the other end underneath it.

A generator NDE bearing temperature trend that ignores power, while the DE bearing still follows power, is the trace this note is for. If the site log shows a grease round on the morning the temperature stepped up, wait out the settle only if the slope goes flat. A slope that is still positive a week later is no longer a grease-quantity story.

If both generator ends and `Gear_Bear_Temp_Avg` stepped up together after a coupling or alignment visit, stop calling it a single bearing and read the alignment report. Shaft-current fluting stays on the list when the insulated end is the hot one and the brush maintenance is overdue. Temperature alone does not prove fluting. It tells you which end to measure.

## After the end is named

Write the tag, the end (DE or NDE), and the slope in the work order before anyone orders a bearing. A generator NDE bearing temperature trend that is still climbing after a week, with the other end quiet, is a planned stop for that end: grease quantity, shaft ground, then the bearing if those two are already correct. Another grease tube on a fluted race makes the temperature worse. If the signal list was never opened, the work order is not ready. Say "the tag" until the drawing says drive end or non-drive end. NDE is a location, not a guess from the number 2 in `Gen_Bear2_Temp_Avg`.
