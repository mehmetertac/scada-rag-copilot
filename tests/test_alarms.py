"""Alarm payload and query formulation."""

from __future__ import annotations

from scada_rag.alarms import AlarmPayload, formulate_query, format_alarm_text


def test_formulate_query_includes_alarm_tags_and_shap() -> None:
    payload = AlarmPayload(
        turbine_id="T06",
        alarm_code="Gearbox HSS bearing temperature high",
        timestamp="2026-01-01T00:00:00Z",
        snapshot={"Gear_Bear_Temp_Avg": 78.0, "Gear_Oil_Temp_Avg": 52.0},
        shap_sensors=(),
    )
    q = formulate_query(payload)
    assert "Gearbox HSS bearing temperature high" in q
    assert "Gear_Bear_Temp_Avg" in q
    assert "Gear_Oil_Temp_Avg" in q


def test_format_alarm_text_lists_snapshot() -> None:
    payload = AlarmPayload(
        turbine_id="T01",
        alarm_code="Pitch angle deviation blade 2",
        timestamp="t",
        snapshot={"Blds_PitchAngle_2": 12.5},
    )
    text = format_alarm_text(payload)
    assert "T01" in text
    assert "Blds_PitchAngle_2" in text
