---
title: Gearbox lubrication alarms
component: gearbox
doc_type: fault
tags: [gearbox, lubrication, oil pressure, filter, particle count, oil level]
---

# Gearbox lubrication alarms

Lubrication alarms are about pressure, level, filter differential pressure, and debris. Temperature alarms are related but not the same fault. A gearbox can run a normal oil temperature and still be a minute away from a bearing failure if pressure is gone at speed.

## Symptoms in SCADA

- Gearbox oil pressure low while `Rtr_RPM_Avg` and `Gen_RPM_Avg` show the turbine is producing, not idling.
- Pressure normal at startup, then falling as `Gear_Oil_Temp_Avg` rises. Hot thin oil, a relief valve, or a worn pump.
- Filter differential pressure (dP) high, or a filter bypass switch.
- Oil level switch low. Level alarms that appear only at a particular nacelle position can be oil sitting away from the switch on a tilt, but treat a persistent low level as real.
- Particle counter or oil-debris monitor stepping up an ISO code, or a ferrous-debris counter incrementing.
- Offline filter (kidney loop) fault or a clogged offline filter, with the main pressure still normal. That is a maintenance alarm, not a stop, unless the main filter is also in bypass.

Pressure collapse at high oil temperature is often viscosity, not a pump that suddenly seized. Read the oil temperature before you change the pump.

## Likely causes

1. Oil level actually low: leak at the HSS labyrinth, a cooler hose, or a drain plug. Look for oil on the tower top and the cooler deck before adjusting the switch.
2. Main filter loaded or in bypass. dP high with pressure at the bearing gallery low means the bearings may be seeing unfiltered or low flow.
3. Pump wear, coupling failure, or a suction strainer blocked. Pressure low at all temperatures once the turbine is at speed.
4. Relief valve stuck open or set low. Pressure caps at a low value and does not rise with speed.
5. Water or the wrong oil, so hot viscosity is too low to hold pressure. Confirm with a sample, not with a guess from the temperature trend.
6. Sensor or wiring on the pressure transmitter. A value that freezes, drops to zero in one sample, or disagrees with a mechanical gauge on the manifold is the transmitter until proven otherwise.
7. Particle-count rise from a damaged bearing or gear. This supports the HSS bearing note when `Gear_Bear_Temp_Avg` is also climbing. Debris with normal temperatures still needs a sample and a filter cut-open.

## Discriminating checks

- Record pressure against rotor speed and oil temperature. A curve that matches the sisters is not a fault. A curve that falls off above a temperature threshold is viscosity or relief.
- Cut the filter only with a planned method. Photograph the pleats. Shiny flakes are bearing or gear material; black sludge is oil varnish or a bypass that has been open for weeks.
- Check the level sight glass at operating attitude if it is safe to do so. Do not open a hot sump.
- Compare the debris monitor to the last laboratory sample (Fe, Cu, PQ index, water).
- Confirm the offline filter is not the only device in alarm. A kidney-loop clog with a healthy main gallery is scheduled work.

## Twin evidence to request

The thermal twin does not see oil pressure. Do not ask it to explain a pressure alarm. Use it only as context: if the bearing residual on `Gear_Bear_Temp_Avg` is already high, treat the debris or low-pressure alarm as the same failure, not as a second unrelated job.

## Escalation

Low oil pressure at production speed is a stop. A filter dP alarm with pressure still in band is a short-dated visit and a filter, and the turbine can usually keep running if the alarm manual says so. A jumping particle count plus a widening bearing-oil split is a stop pending the sample result and the OEM desk. Follow the escalation procedure for who calls the OEM.

## Worked trace

Read pressure against oil temperature at production rotor speed, not at idle. A pump that makes normal pressure when the oil is cold and loses it only after `Gear_Oil_Temp_Avg` has climbed is a hot-viscosity or relief-valve problem. A pump that is low at every temperature, as soon as `Rtr_RPM_Avg` is in the production band, is the pump, the coupling, the suction strainer, or the transmitter.

Then read the debris channel on its own. An ISO code that steps up on the same days the HSS split widens is one fault described twice: the bearing note plus this note. An ISO code that steps up with flat temperatures still gets a sample and a filter cut. It does not get a "wait for the temperature" delay. Debris is allowed to lead temperature.

A kidney-loop alarm with main gallery pressure in band and a quiet debris count is scheduled filter work. Write that distinction in the log so the next shift does not stop the turbine for the offline loop.

## Pressure is not a temperature

Do not close a low-pressure alarm because `Gear_Oil_Temp_Avg` looks normal. Pressure at production speed is the protection. Temperature can stay ordinary until the film is already gone. If the only tool on the desk is the temperature trend, say that the pressure channel was not in the export, and do not invent a pressure value from the oil temperature. The gallery either had pressure at speed or it did not. Write the rotor speed next to the pressure in the log. A low reading at idle, with the rotor nearly stopped, is not the same alarm as a low reading while `Rtr_RPM_Avg` is in the production band.
