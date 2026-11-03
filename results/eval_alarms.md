# Alarm eval (grounded RAG vs no-retrieval baseline)

Model: `qwen2.5:3b`. Scenarios: 12 from `eval/alarms.yaml`.

## Summary

| Metric | RAG | No retrieval |
| --- | --- | --- |
| Top-1 cause hit rate | 67% | — |
| Top-3 cause hit rate | 67% | — |
| Grounding check pass rate | 67% | — |
| Answers citing a `.md` manual section | — | 0% |
| Answers naming labelled note (specificity) | — | 83% |

## Per scenario (RAG)

| id | expected | top-1 | top-3 | grounding | cited |
| --- | --- | --- | --- | --- | --- |
| hss_bearing_partial_load | gearbox_hss_bearing_overtemp.md | no | no | no | no grounded cause found |
| gearbox_oil_high_bearing_normal | gearbox_oil_overtemp.md | yes | yes | yes | gearbox_oil_overtemp.md, gearbox_oil_overtemp.md |
| gearbox_lube_pressure | gearbox_lubrication_alarms.md | yes | yes | yes | gearbox_lubrication_alarms.md, gearbox_lubrication_alarms.md |
| pitch_blade2_deviation | pitch_system_errors.md | yes | yes | yes | pitch_system_errors.md, pitch_system_errors.md |
| generator_nde_bearing | generator_bearing_faults.md | no | no | no | no grounded cause found |
| generator_winding | generator_winding_overtemp.md | yes | yes | yes | generator_winding_overtemp.md, generator_winding_overtemp.md |
| converter_igbt_trip | converter_trips.md | yes | yes | yes | converter_trips.md, converter_trips.md, converter_trips.md |
| grid_voltage_dip | grid_side_faults.md | no | no | no | no grounded cause found |
| yaw_misalignment | yaw_misalignment.md | yes | yes | yes | yaw_misalignment.md |
| hydraulic_oil_temp | hydraulic_system_alarms.md | yes | yes | yes | hydraulic_system_alarms.md, hydraulic_system_alarms.md |
| escalation_stop_gearbox | procedure_escalation_thresholds.md | yes | yes | yes | procedure_escalation_thresholds.md, procedure_escalation_thresholds.md |
| obstruction_light_out_of_kb | abstain | no | no | no | gearbox_hss_bearing_overtemp.md |

## Per scenario (baseline)

| id | hallucinated .md | names note |
| --- | --- | --- |
| hss_bearing_partial_load | no | yes |
| gearbox_oil_high_bearing_normal | no | yes |
| gearbox_lube_pressure | no | yes |
| pitch_blade2_deviation | no | yes |
| generator_nde_bearing | no | yes |
| generator_winding | no | yes |
| converter_igbt_trip | no | yes |
| grid_voltage_dip | no | yes |
| yaw_misalignment | no | yes |
| hydraulic_oil_temp | no | yes |
| escalation_stop_gearbox | no | no |
| obstruction_light_out_of_kb | no | no |
