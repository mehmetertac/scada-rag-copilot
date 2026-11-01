---
title: Grid-side faults
component: grid
doc_type: fault
tags: [grid, voltage, frequency, reactive power, protection, feeder]
---

# Grid-side faults

A grid-side fault is outside the gearbox and, often, outside the single turbine. The first question is how many turbines tripped, and whether voltage or frequency moved. The sibling project grid-gnn-faults is the electrical classifier for simulated grid faults. This note is the plant-floor version: what the alarm means and who you call.

## Symptoms in SCADA

- Voltage, frequency, or rate-of-change alarms, then a trip, on many turbines in the same minute.
- One turbine only: grid-breaker open, a protection relay trip, or a converter LVRT trip, while neighbors on the same feeder stay online and show normal voltage.
- Reactive-power limit or a power-factor alarm with the turbine still running, often from a set-point the grid operator sent, or from a converter that cannot meet the request.
- Overvoltage at the turbine with low active power and a long cable, versus undervoltage at high power at the end of a weak feeder. Those are operating-point effects until the numbers leave the grid-code band.
- Frequency high or low across the site is a system event. No one at the turbine fixes it with a reset.

## Likely causes

1. Transmission or distribution fault: a dip, a recloser, or a frequency excursion. Many turbines, one timestamp. Log it against the grid operator's event. Do not replace converter modules the next morning because twenty turbines tripped together.
2. Feeder or substation protection: one feeder out, the neighboring feeder still producing. Call the site electrical lead, not the gearbox contractor.
3. Single-turbine breaker, relay, or converter protection. Neighbors healthy. Use the converter trip note and the relay's first-up target.
4. Reactive-power setpoint the turbine cannot hold because of a converter limit, a failed filter, or a setpoint outside the capability curve. The turbine may curtail rather than trip.
5. A voltage sensor or a PT fuse on one turbine. That turbine sees a wild voltage and the neighbor does not. Confirm with a second measurement before you change a tap or a parameter.
6. Islanding or a transfer trip. Follow the electrical procedure. This is not a remote reset from a laptop on the road.

## Discriminating checks

- Count turbines and feeders in the same minute. Write the count down before you form a theory.
- Read voltage and frequency on a turbine that stayed online. If those traces moved, the tripped units may have done what the grid code asked.
- Separate a converter LVRT trip from a breaker fail-to-close. The first may be a setting; the second is hardware or the close circuit.
- Check reactive power against the setpoint and the capability curve. A unit at the curve is not "failing to regulate"; it is at the limit.
- Do not connect this alarm to `Gear_Bear_Temp_Avg` unless the only evidence is a timestamp coincidence.

## Twin evidence to request

The thermal twin has nothing to say about a voltage dip. Use grid measurements and, when the question is a simulated or studied electrical fault, the grid-gnn-faults work. Citing a normal gearbox residual as proof the grid event was "not mechanical" is fair. Citing it as the cause is not.

## Escalation

A site-wide or feeder trip is a call to the electrical lead and, through them, the grid operator. A repeated single-turbine grid-breaker trip with neighbors online is a stop until the relay target is understood. A reactive-power shortfall inside the grid code, with the turbine online, is a controls and converter task for the next working day unless the operator instructs a shutdown. Do not reset protection relays you are not authorized to reset.

## Worked trace

Before any theory, write three numbers: how many turbines tripped, how many feeders, and whether a turbine that stayed online saw voltage or frequency move. Many turbines, one minute, voltage moved: system or feeder event. Use the grid operator's record and the converter LVRT codes as the same event. One turbine, neighbors online, voltage on the neighbor flat: this turbine's breaker, relay, PT, or converter. The converter note has the cooling and DC-link splits. This note owns the "how many turbines" question.

A reactive-power alarm with the turbine still running is not a trip. Compare the setpoint with the capability curve. A unit sitting on the curve is doing what the hardware can do. A unit far inside the curve that still misses the setpoint is a control or a failed filter.

`Gear_Bear_Temp_Avg` does not explain a voltage dip. A calm gearbox residual is only permission to stop looking at the gearbox.

## What to hand the electrical lead

Three numbers, then the first-up code: turbines tripped, feeders involved, and whether an online neighbor saw the voltage or frequency move. Without the count, a single converter LVRT code gets treated as a failed module when the feeder dipped. With the count, a site-wide trip goes to the grid operator through the electrical lead and does not become twenty gearbox inspections. A reactive-power alarm on a turbine that stayed online is a setpoint and capability-curve question for the next working day, unless the operator has already instructed a shutdown. Do not reset a protection relay you are not authorized to reset, and do not describe the event as a bearing fault because the timestamps were close. One turbine offline with the neighbor's voltage flat is this turbine. The whole feeder offline is not.
