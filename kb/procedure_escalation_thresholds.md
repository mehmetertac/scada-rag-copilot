---
title: Escalation thresholds for temperature and trip alarms
component: operations
doc_type: procedure
tags: [escalation, stop, shutdown, thresholds, gearbox temperature alarm]
---

# Escalation thresholds for temperature and trip alarms

This procedure is how a site decides to watch, curtail, plan a visit, or stop. The numbers below are example site practice from field judgment. They are not OEM trip setpoints. The turbine alarm manual and the site's electrical rules win when they disagree with this note.

## When to stop the turbine

Stop, and leave it stopped, when any of these is true:

- A gearbox temperature alarm at the trip level that returns after one reset. That includes HSS bearing or oil at the platform trip, not a warning that cleared on its own.
- Gearbox oil pressure lost while the rotor is at production speed.
- Metal on the filter, a debris alarm stepping up, and a bearing temperature that is already climbing.
- Emergency feather is not available: pitch battery, ultracapacitor, or hydraulic accumulator below the manual's minimum.
- Converter ground fault, overcurrent, or a trip that reproduces on every start.
- Brake hydraulic pressure lost, or a protection relay target you are not authorized to reset.
- Any alarm the manual itself calls a stop. Do not negotiate with a protection trip from a chat window.

A remote reset is allowed once when the manual says the alarm is resettable and the cause is a grid dip the neighbors also saw. A second return of the same trip is a stop.

## When to restrict power instead of stopping

- Gearbox oil temperature high, bearing-oil split still normal, and the cooler fan has failed or the day is hot. Hold the power the manual allows for that oil temperature. Plan a cooler repair.
- Winding temperature high with power, filters dirty, remaining RTDs in agreement. Curtail to the manual's hot-day limit.
- A slow HSS bearing-oil split that is wider than the sisters but not racing. If the split keeps growing after power is reduced, stop treating it as a curtailment and plan the stop.

## When to plan a visit and keep running

- Warning-level gearbox temperature with a slow trend, pressure normal, no debris. Visit in the next low-wind window with the inspection checklist.
- Generator bearing temperature up after a regrease, not still rising a week later. Inspect grease quantity and the shaft ground at the next planned stop.
- Pitch encoder offset of about a degree below rated wind, feather test passed, batteries healthy.
- Yaw vane offset of a few degrees with a measured energy loss and no protection alarm.
- Filter differential pressure high, gallery pressure still in band, no metal.

## Who to call

- Site technician: first confirmation of fan, leak, filter indicator, and whether the alarm is still active.
- Site lead: any stop, any curtailment that will last past the shift, any repeat trip.
- OEM remote desk: bearing or gear damage suspected, a trip code you cannot decode, a repeat converter fault, a pitch safety path failed.
- Grid operator: only through the electrical lead, and only for a feeder or site-wide voltage or frequency event. A single turbine breaker is not a grid-operator call.

## What the twin is allowed to change

The hybrid twin's sustained-alarm flag and the bearing residual are reasons to move a turbine from "watch" to "plan a visit," or to support a curtailment you were already considering. They are not a certification that the bearing will last a stated number of days. They do not authorize a restart after a protection trip. If the twin is calm and the oil-pressure switch says pressure is gone at speed, believe the pressure switch.

## Lead time

A split that widened over two weeks is a planning problem. A climb of several degrees in an hour is a this-shift problem. Do not quote a remaining-useful-life number from a chat reply. If a probabilistic RUL is available from the twin's RUL path, report it as a band with the model name, and still follow the stop rules above.

## Handover note

Write one line in the log: alarm, turbine, what you did (watch, curtail, stop), who you called, and the next check time. A stop without a log line will be restarted by the next shift.

## Gearbox temperature alarm, worked call

When to stop the turbine for a gearbox temperature alarm is a short decision, not a tour of every cooler on site.

- Trip-level gearbox temperature, bearing or oil, that returns after one reset: stop.
- Oil pressure gone at production speed, with or without a temperature alarm: stop.
- Debris plus a bearing temperature that is already climbing: stop.
- Warning-level oil temperature, split still normal, cooler fan failed: restrict power, visit the fan, do not condemn the gearbox.
- Warning-level HSS bearing split that widened at partial load, pressure normal, no debris: keep running only if the manual's warning band allows it, and book the inspection checklist in the next low-wind window. If the split is still widening after you reduce power, stop treating it as a watch item.

Say the choice out loud in the log using those words: stop, restrict, or plan a visit. "Monitor" with no next check time is not one of the three.
