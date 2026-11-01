---
title: Converter trips
component: converter
doc_type: fault
tags: [converter, IGBT, DC link, LVRT, cooling, trip]
---

# Converter trips

A converter trip is an electrical stop. Read the trip code before you look at the gearbox. The same SCADA "converter fault" bit covers IGBT temperature, DC-link voltage, grid undervoltage, ground fault, and cooling. Those are different jobs.

## Symptoms in SCADA

- A trip code or a first-up alarm: IGBT over-temperature, coolant flow, DC-link overvoltage, LVRT or grid undervoltage, chopper, ground fault, or a cabinet-fan alarm.
- The turbine stops and restarts, and production for that hour is a notch rather than a slow thermal trend.
- Farm-wide trips in the same minute, with the same grid-voltage dip on neighboring turbines, are a grid event. One turbine tripping while the neighbors keep producing is this turbine's converter, breaker, or settings.
- IGBT temperature high before the trip, with cabinet temperature high, points at cooling. A trip with cold IGBTs and a voltage code points at the grid or the DC link.
- Repeated trips on gusts, with DC-link overvoltage, while grid voltage is inside the band, point at the chopper or the DC-link control, not at the gearbox oil cooler.

## Likely causes

1. Cooling: cabinet filters plugged, cabinet fan failed, or liquid-cooling flow lost so an IGBT module overheats under load. Often the module that sits at the top of the cabinet or at the end of a partially blocked duct.
2. Grid disturbance: a voltage dip the turbine should ride through, or a dip deeper or longer than the LVRT curve. If the whole feeder dips, start with the grid note and the grid operator's event, not with a converter module replacement.
3. DC-link overvoltage on a gust or a fast stop, with the chopper resistor open, the chopper IGBT failed, or the brake chopper disabled by parameter.
4. Ground fault or insulation alarm on the generator-side or grid-side bridge. This is a stop for a technician with the right isolation procedure. It is not a remote reset to "see if it holds."
5. A failed IGBT or a driver board, usually after a cooling fault was ignored, or after a grid fault the protection did not clear cleanly. One module's fault code, the others healthy.
6. Parameter or firmware mismatch after a board swap. The trip appears immediately on the first start, with a code the sister turbines do not have.

## Discriminating checks

- Record the first-up code and the time. Count how many turbines on the same feeder tripped inside the same minute.
- Read grid voltage and frequency around the trip. A dip that the neighbors rode through, while this unit tripped, is a ride-through setting or a weak converter, not a transmission fault.
- Check cabinet temperature, fan command versus fan feedback, and coolant flow before you order a stack.
- Do not reset a ground-fault or overcurrent trip repeatedly. Two resets that reproduce the trip are enough; the third one is how stacks fail.
- Separate generator winding temperature from IGBT temperature. They share the word "hot" and nothing else.

## Twin evidence to request

The gearbox twin will be quiet during a converter trip. That only tells you the drivetrain temperature was not the cause. For a farm-wide electrical event, the grid fault-classification work in grid-gnn-faults is the relevant sibling project. This knowledge base does not classify the feeder.

## Escalation

A single undervoltage trip that matches a known grid dip, with a successful restart and no repeat, is a log entry. IGBT over-temperature with a dead cabinet fan is a stop until the fan and filters are restored. Ground fault, overcurrent, or a trip that returns on every start is a stop and an OEM or a qualified converter technician. Do not bypass the trip.

## Worked trace

Write the first-up code and the minute it happened, then count how many other turbines on the same feeder have a trip in that same minute. Twenty turbines and a voltage dip is the grid note, even if this turbine's code says LVRT. One turbine, neighbors still producing, IGBT temperature already high, cabinet fan alarm on, is a cooling fault that ended in a trip. One turbine, IGBTs cold, DC-link overvoltage on gusts, is the chopper or the DC-link path.

Do not reset a ground fault to "see if it holds." Two identical reproductions are the evidence. The third reset is how a stack gets damaged. A gearbox temperature that did not move is useful only as a reason not to open the gearbox after the trip.

## Trip log to keep

For each converter stop, keep four fields or the next shift will reset it again: the first-up code, the cabinet temperature at that minute, whether the neighbors tripped, and whether a restart held for at least an hour of production. A code you cannot read is a call to the OEM desk with those four fields attached, not a guess that the IGBT module is dead. Filters and the cabinet fan are the parts that fail quietly for weeks before the code appears. Look at them before you order a stack. A cabinet that has been hot for a week with clean production is a filter and a fan. A cabinet that trips cold, on a code the neighbors do not share, is electrical and stays stopped until someone who is allowed to open the converter has read the code.
