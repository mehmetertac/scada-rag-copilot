---
title: Yaw misalignment
component: yaw
doc_type: fault
tags: [yaw, misalignment, wind vane, power curve, cable twist]
---

# Yaw misalignment

Yaw error points the rotor off the wind. The production loss is real, and it is not a gearbox temperature fault. A turbine that sits a few degrees off the wind all month will look like a poor power curve and a healthy drivetrain. Fix the vane or the yaw system before you open the gearbox.

## Symptoms in SCADA

- Power below the sister turbines at the same `Amb_WindSpeed_Avg`, with gearbox and generator temperatures normal or even a little low because the rotor is not fully loaded.
- A steady offset between wind direction and nacelle position that does not average out over a day. A few degrees of static yaw error is a wind-vane zero, a twisted vane, or a north offset in the controller. Turbulent error that averages near zero is not a fault.
- Yaw motor current high, or yaw brakes that never fully release, so the nacelle tracks slowly and `Nac_Temp_Avg` runs hot from the brake or the motors.
- Cable-twist counter near the limit. The controller inhibits yaw, the turbine holds a bad heading, and power falls until an untwist is commanded.
- The power curve deficit is worse on one side of the wind rose, which fits a vane bias, a transfer-function error, or a wake the analyst has not separated yet.

## Likely causes

1. Wind-vane zero error or a vane installed 180 degrees out after a lightning repair. The offset is nearly constant.
2. Vane or sonic anemometer seized, iced, or reading a disturbed flow because a bracket was bent. The direction trace is flat, spiky, or unlike the met mast and the neighboring turbines.
3. Yaw brake dragging or yaw motor failing, so the nacelle cannot follow a wind shift. Motor current and yaw-error spikes line up.
4. Cable twist at the limit, yaw inhibited. The untwist is a controlled yaw procedure from the manual, not a converter reset and not a brake release from the ground.
5. Wrong north offset or a site-calibration parameter overwritten during a software load. Several turbines can be wrong after the same campaign, each by a similar angle.
6. Wake. A deficit that appears only in a narrow direction toward the neighbor is not a vane fault. Check the wind rose before you climb.

## Discriminating checks

- Bin power by wind speed against two sisters and against this turbine's own historical curve. A parallel curve that is simply lower in every sector is availability or curtailment. A curve that is low in every sector with a constant yaw offset is the vane.
- Average yaw error by wind-direction sector. A constant bias is calibration. A bias in one sector is wake or terrain.
- Read the cable-twist count before you command a long yaw. Untwist first if the manual says the count is near the stop.
- Inspect the vane for ice, a bent boom, or a shield installed backwards.
- Confirm gearbox temperatures are boring. If `Gear_Bear_Temp_Avg` is the actual alarm, yaw is not the cause just because the power curve is also a bit soft.

## Twin evidence to request

A calm gearbox residual plus a soft power curve supports "the rotor is not taking the power," which is consistent with yaw error, curtailment, or pitch. Ask for the residual so you do not chase a thermal fault. The twin does not estimate yaw offset. The offset comes from nacelle position versus wind direction.

## Escalation

Cable twist at the limit is a controlled untwist, scheduled, not an emergency stop unless the manual says the protection is about to trip. A seized yaw brake with motors overheating is a stop so the motors and the brake are not destroyed. A vane offset of a few degrees with normal protection is a calibration visit in the next low-wind window. Quantify the lost energy first so the visit is justified.

## Worked trace

Bin this turbine's power against `Amb_WindSpeed_Avg` and against two sisters, then split the bins by wind-direction sector. A curve that is low in every sector, with nacelle position sitting a nearly constant angle off `Amb_WindDir_Avg`, is a vane zero or a north offset. A curve that is low in only the sector that points at the neighbor is wake. Do not calibrate the vane for a wake.

Read the cable-twist counter before anyone commands a long yaw. Near the limit, the controller may already be refusing to yaw, which looks like a "lazy nacelle" and is actually a lockout. The untwist procedure in the manual is the work order. A converter reset does not unwind a cable.

Temperatures should look boring or a little low, because the rotor is not fully loaded. If `Gear_Bear_Temp_Avg` is the alarm that started the shift, yaw misalignment is not the cause.

## Making the visit specific

A yaw visit needs a number: the mean offset in degrees, the sectors where power is low, and the cable-twist count. "Yaw error" with none of those is how a vane gets replaced when the turbine was sitting in a wake, or how a crew yaws a nacelle that was already at the twist limit. Calibrate the vane only after the sector plot says the deficit is in every direction. Schedule the untwist only when the counter says the controller is about to inhibit yaw. Those are two different jobs and they should not be on the same line of the work order. Quantify the lost energy against the sisters before you book the climb, so a one-degree offset with no production loss does not jump the queue ahead of a real stop alarm.
