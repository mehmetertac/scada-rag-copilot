# Sanity queries

Embed model: `BAAI/bge-small-en-v1.5` (`huggingface`).
Chunk size 400, overlap 60, top-k checked: 3.

A query passes when the expected source file is in the top 3.

## 1. gearbox HSS bearing temp rising at partial load

Expected: `gearbox_hss_bearing_overtemp.md`. Result: **pass**.

| Rank | Score | Source | Section |
| --- | --- | --- | --- |
| 1 | 0.864 | `gearbox_hss_bearing_overtemp.md` | Likely causes |
| 2 | 0.857 | `gearbox_hss_bearing_overtemp.md` | Overview |
| 3 | 0.836 | `gearbox_oil_overtemp.md` | Overview |

## 2. gearbox oil temperature high but bearing normal

Expected: `gearbox_oil_overtemp.md`. Result: **pass**.

| Rank | Score | Source | Section |
| --- | --- | --- | --- |
| 1 | 0.889 | `gearbox_oil_overtemp.md` | Overview |
| 2 | 0.863 | `gearbox_oil_overtemp.md` | Symptoms in SCADA |
| 3 | 0.862 | `gearbox_hss_bearing_overtemp.md` | Likely causes |

## 3. pitch angle deviation alarm blade 2

Expected: `pitch_system_errors.md`. Result: **pass**.

| Rank | Score | Source | Section |
| --- | --- | --- | --- |
| 1 | 0.867 | `pitch_system_errors.md` | Overview |
| 2 | 0.861 | `pitch_system_errors.md` | One cabinet, then the safety path |
| 3 | 0.841 | `pitch_system_errors.md` | Worked trace |

## 4. generator NDE bearing temperature trend

Expected: `generator_bearing_faults.md`. Result: **pass**.

| Rank | Score | Source | Section |
| --- | --- | --- | --- |
| 1 | 0.873 | `generator_bearing_faults.md` | Symptoms in SCADA |
| 2 | 0.844 | `generator_bearing_faults.md` | Overview |
| 3 | 0.834 | `generator_bearing_faults.md` | After the end is named |

## 5. when to stop the turbine for a gearbox temperature alarm

Expected: `procedure_escalation_thresholds.md`. Result: **pass**.

| Rank | Score | Source | Section |
| --- | --- | --- | --- |
| 1 | 0.889 | `procedure_escalation_thresholds.md` | When to stop the turbine |
| 2 | 0.884 | `procedure_escalation_thresholds.md` | Gearbox temperature alarm, worked call |
| 3 | 0.826 | `generator_winding_overtemp.md` | Escalation |

Passed 5 of 5.
